"""Start the localhost application with explicit model configuration."""
import argparse
import os
from .llm.runners import build_runner
from .server import serve
from .llm.local_chat import LocalChatRunner


def main():
    """Parse port and runner options, then launch the single application pipeline."""
    parser = argparse.ArgumentParser(description='Heat Pump Ready – lokale Ersteinschätzung')
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--runner', choices=('disabled', 'api', 'mlx'), default=os.environ.get('LLM_RUNNER', 'disabled'))
    parser.add_argument('--public-origin', default='', help='Genau eine erlaubte öffentliche HTTPS-Origin für einen Demo-Tunnel.')
    parser.add_argument('--chat-model', default='', help='Optionales lokales Ollama-Textmodell für den Website-Chat.')
    parser.add_argument('--chat-url', default='http://127.0.0.1:11435/api/chat', help='Lokaler Ollama-Chat-Endpunkt.')
    args = parser.parse_args()
    if not 1024 <= args.port <= 65535:
        parser.error('Port muss zwischen 1024 und 65535 liegen.')
    chat_runner = LocalChatRunner(args.chat_model, args.chat_url) if args.chat_model else None
    serve(build_runner(args.runner), args.runner, args.port, args.public_origin, chat_runner, args.chat_model)

if __name__ == '__main__':
    main()
