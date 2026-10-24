"""Local-only HTTP application with bounded request bodies and no persistent user data."""

from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import threading
import traceback
from .config import AssessmentConfig
from .intake import build_user_input
from .calculation.registry import build_modules
from .calculation.orchestrator import CalculationOrchestrator
from .validator import validate_and_decide
from .demo_cases import CASES, SYNTHETIC

WEB = Path(__file__).parent / "web"


def make_handler(runner, mode):
    """Bind injected services to one HTTP handler; serialize resource-heavy inference."""
    config = AssessmentConfig()
    modules = build_modules(config, runner)
    lock = threading.Lock()

    class Handler(BaseHTTPRequestHandler):
        """Serve fixed assets and an assessment JSON API on loopback only."""

        def send_content(self, status, content, mime="application/json; charset=utf-8"):
            """Send bounded response with explicit MIME and browser security headers."""
            body = (
                content
                if isinstance(content, bytes)
                else json.dumps(content, ensure_ascii=False, allow_nan=False).encode()
            )
            self.send_response(status)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header(
                "Content-Security-Policy",
                "default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' data:; object-src 'none'; frame-ancestors 'none'",
            )
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            """Serve only known assets and read-only configuration metadata."""
            routes = {
                "/": ("index.html", "text/html; charset=utf-8"),
                "/app.js": ("app.js", "text/javascript; charset=utf-8"),
                "/style.css": ("style.css", "text/css; charset=utf-8"),
            }
            if self.path in routes:
                name, mime = routes[self.path]
                return self.send_content(200, (WEB / name).read_bytes(), mime)
            if self.path == "/api/health":
                return self.send_content(200, {"status": "ready", "runner": mode})
            if self.path == "/api/config":
                cases = [
                    {
                        key: value
                        for key, value in case.items()
                        if key not in ("reference_heating_load_kw", "expected_verdict")
                    }
                    for case in CASES
                ]
                return self.send_content(
                    200,
                    {
                        "runner": mode,
                        "modules": [
                            {"key": m.output_key, "requires": m.requires}
                            for m in modules
                        ],
                        "cases": cases,
                        "synthetic": SYNTHETIC,
                    },
                )
            self.send_content(404, {"error": "Nicht gefunden."})

        def do_POST(self):
            """Parse user input, run metrics, then validate; never expose raw payloads in logs."""
            if self.path != "/api/assessments":
                return self.send_content(404, {"error": "Nicht gefunden."})
            expected_hosts = {
                f"localhost:{self.server.server_port}",
                f"127.0.0.1:{self.server.server_port}",
            }
            if self.headers.get("Host") not in expected_hosts:
                return self.send_content(403, {"error": "Nur localhost ist erlaubt."})
            origin = self.headers.get("Origin")
            if origin and origin not in {"http://" + host for host in expected_hosts}:
                return self.send_content(
                    403, {"error": "Fremde Herkunft ist nicht erlaubt."}
                )
            if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
                return self.send_content(415, {"error": "JSON erwartet."})
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= 34 * 1024 * 1024:
                    return self.send_content(
                        413, {"error": "Anfrage zu groß oder leer."}
                    )
                self.connection.settimeout(60)
                payload = json.loads(self.rfile.read(length))
                if not isinstance(payload, dict):
                    raise ValueError("JSON-Objekt erwartet.")
                user_input = build_user_input(payload.get("input", {}))
                disabled = payload.get("disabled_modules", [])
                if not isinstance(disabled, list) or any(
                    not isinstance(key, str) for key in disabled
                ):
                    raise ValueError("Ungültige Modulauswahl.")
                pipeline = CalculationOrchestrator(modules, disabled)
                if not lock.acquire(blocking=False):
                    return self.send_content(
                        429,
                        {
                            "error": "Eine Berechnung läuft bereits. Bitte gleich erneut versuchen."
                        },
                    )
                try:
                    results = pipeline.run(user_input)
                    decision = validate_and_decide(results, config)
                finally:
                    lock.release()
                self.send_content(
                    200,
                    {
                        "metrics": asdict(results),
                        "decision": asdict(decision),
                        "configuration": asdict(config),
                        "version": "0.1.0-demo",
                        "runner": mode,
                    },
                )
            except (ValueError, TypeError) as error:
                self.send_content(400, {"error": str(error)})
            except Exception:
                traceback.print_exc()
                self.send_content(
                    500,
                    {
                        "error": "Interner Berechnungsfehler; siehe lokales Serverprotokoll."
                    },
                )

        def log_message(self, format, *args):
            """Keep request bodies and document contents out of access logs."""
            return None

    return Handler


def serve(runner, mode, port):
    """Run a loopback server until interrupted and reliably close the selected runner."""
    runner.start()
    try:
        with ThreadingHTTPServer(
            ("127.0.0.1", port), make_handler(runner, mode)
        ) as server:
            print(f"Heat Pump Ready: http://localhost:{port} (LLM: {mode})", flush=True)
            server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        runner.close()
