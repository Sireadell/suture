"""Triage: a small ticket router. Planted flaw: a ticket with no category goes to billing by default."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import neatlogs

TRACING = bool(os.environ.get("NEATLOGS_API_KEY"))
if TRACING:
    neatlogs.init(api_key=os.environ["NEATLOGS_API_KEY"], endpoint="https://ingest.neatlogs.com", workflow_name="triage")

ROUTES = {"billing": "finance-team", "bug": "engineering", "account": "support-team"}
DEFAULT_CATEGORY = "billing"


@neatlogs.span(kind="TOOL", tool_name="route_ticket")
def route_ticket(category):
    return ROUTES.get(category, ROUTES[DEFAULT_CATEGORY])


@neatlogs.span(kind="WORKFLOW")
def handle(raw_body):
    try:
        data = json.loads(raw_body)
    except Exception:
        data = {}
    category = data.get("category", DEFAULT_CATEGORY)
    return {"category": category, "route_to": route_ticket(category)}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self._send(200, {"agent": "triage", "status": "ok"})

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
