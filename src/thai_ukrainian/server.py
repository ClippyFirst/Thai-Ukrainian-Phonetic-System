from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from .batch import analyze_input


def _send(handler: BaseHTTPRequestHandler, status: int, payload: dict[str, Any]) -> None:
    body = json.dumps(payload, ensure_ascii=False, default=str).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")
    handler.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
    handler.end_headers()
    handler.wfile.write(body)


class APIHandler(BaseHTTPRequestHandler):
    server_version = "thai-ua/0.5.0"

    def do_OPTIONS(self) -> None:
        _send(self, 204, {})

    def do_GET(self) -> None:
        if self.path == "/health":
            _send(self, 200, {"status": "ok", "service": "thai-ua"})
            return
        _send(self, 404, {"error": "not_found"})

    def do_POST(self) -> None:
        if self.path != "/analyze":
            _send(self, 404, {"error": "not_found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 1_000_000:
                _send(self, 413, {"error": "request_too_large"})
                return
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            text = payload.get("text")
            if not isinstance(text, str) or not text.strip():
                _send(self, 400, {"error": "field 'text' must be a non-empty string"})
                return
            _send(self, 200, analyze_input(text))
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError, TypeError) as exc:
            _send(self, 400, {"error": "invalid_request", "detail": str(exc)})
        except Exception as exc:
            _send(self, 500, {"error": "analysis_failed", "detail": str(exc)})

    def log_message(self, format: str, *args: object) -> None:
        return


def serve(host: str = "127.0.0.1", port: int = 8787) -> None:
    server = ThreadingHTTPServer((host, port), APIHandler)
    print(f"thai-ua API listening on http://{host}:{port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
