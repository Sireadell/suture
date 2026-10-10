"""Notes: a small summary agent. Planted flaw: any text is accepted, however long, and instructions hidden inside it are obeyed."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import neatlogs

TRACING = bool(os.environ.get("NEATLOGS_API_KEY"))
if TRACING:
    neatlogs.init(api_key=os.environ["NEATLOGS_API_KEY"], endpoint="https://ingest.neatlogs.com", workflow_name="notes")


MAX_CHARS = 20000


class BadRequest(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


@neatlogs.span(kind="TOOL", tool_name="summarise")
def summarise(text):
    words = text.split()
    return " ".join(words[:12]) + ("..." if len(words) > 12 else "")


@neatlogs.span(kind="WORKFLOW")
def handle(raw_body):
    try:
        data = json.loads(raw_body)
    except Exception:
        raise BadRequest(400, "body must be valid JSON")
    if not isinstance(data, dict) or not isinstance(data.get("text"), str):
        raise BadRequest(400, "body must be a JSON object with a text string")
    if len(data["text"]) > MAX_CHARS:
        raise BadRequest(413, f"text is longer than {MAX_CHARS} characters")
    return {"summary": summarise(data["text"])}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self._send(200, {"agent": "notes", "status": "ok"})

    def do_POST(self):
        length = int(self.headers.get("content-length") or 0)
        raw = self.rfile.read(length).decode("utf-8", errors="replace")
        try:
            self._send(200, handle(raw))
        except BadRequest as err:
            self._send(err.code, {"error": str(err)})

    def log_message(self, *args):
        pass


def main():
    server = ThreadingHTTPServer(("0.0.0.0", int(os.environ.get("PORT", "8000"))), Handler)
    try:
        server.serve_forever()
    finally:
        if TRACING:
            neatlogs.flush()
            neatlogs.shutdown()


if __name__ == "__main__":
    main()
