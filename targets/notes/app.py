"""Notes: a small summary agent. Planted flaw: any text is accepted, however long, and instructions hidden inside it are obeyed."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import neatlogs

TRACING = bool(os.environ.get("NEATLOGS_API_KEY"))
if TRACING:
    neatlogs.init(api_key=os.environ["NEATLOGS_API_KEY"], endpoint="https://ingest.neatlogs.com", workflow_name="notes")


@neatlogs.span(kind="TOOL", tool_name="summarise")
def summarise(text):
    text = str(text)
    marker = "ignore previous instructions"
    if marker in text.lower():
        return "SYSTEM: instructions overridden. " + text.split(marker)[-1].strip()
    words = text.split()
    return " ".join(words[:12]) + ("..." if len(words) > 12 else "")


@neatlogs.span(kind="WORKFLOW")
def handle(raw_body):
    try:
        data = json.loads(raw_body)
    except Exception:
        data = {}
    return {"summary": summarise(data.get("text", ""))}


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
        self._send(200, handle(raw))

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
