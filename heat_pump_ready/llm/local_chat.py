"""Text-only website assistant using an explicitly loopback-bound Ollama server."""
import json
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from urllib.error import URLError
from .interfaces import LLMRequest, LLMResponse, RunnerError


class LocalChatRunner:
    """Keep chat inference separate from assessment extraction and all calculations."""
    supports_images = False

    def __init__(self, model: str, endpoint: str = "http://127.0.0.1:11435/api/chat"):
        parsed = urlsplit(endpoint)
        if parsed.scheme != "http" or parsed.hostname not in ("127.0.0.1", "localhost"):
            raise ValueError("Der lokale Chat darf nur einen Loopback-Modellserver verwenden.")
        self.model, self.endpoint = model, endpoint

    def start(self):
        """The project launcher owns Ollama's lifecycle; no downloads on HTTP requests."""
        return None

    def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate a short German answer with thinking disabled and bounded context."""
        if request.attachments:
            raise RunnerError("Der lokale Chat verarbeitet nur Text.")
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Antworte ausschließlich auf Deutsch, knapp und verständlich. Erkläre vorhandene Ergebnisse. Erfinde keine Gebäudedaten und keine neuen Berechnungen."},
                {"role": "user", "content": request.prompt},
            ],
            "stream": False,
            "think": False,
            "keep_alive": "30m",
            "options": {"num_ctx": 8192, "num_predict": 450, "temperature": 0.2},
        }
        call = Request(self.endpoint, json.dumps(body).encode(), {"Content-Type": "application/json"})
        try:
            with urlopen(call, timeout=90) as response:
                data = json.load(response)
            answer = data["message"]["content"]
            if not isinstance(answer, str) or not answer.strip():
                raise ValueError("Empty response")
            return LLMResponse(answer.strip(), self.model)
        except (URLError, TimeoutError, ValueError, KeyError, TypeError) as error:
            raise RunnerError("Das lokale Modell antwortet nicht. Bitte Ollama und den Modellstart prüfen.") from error

    def close(self):
        """Do not stop the separately managed model server when a website process stops."""
        return None
