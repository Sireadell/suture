"""Quote: a small price calculator. Planted flaw: a quantity sent as text is silently treated as 1."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import neatlogs

TRACING = bool(os.environ.get("NEATLOGS_API_KEY"))
if TRACING:
    neatlogs.init(api_key=os.environ["NEATLOGS_API_KEY"], endpoint="https://ingest.neatlogs.com", workflow_name="quote")

PRICES = {"pen": 1.20, "notebook": 4.50, "bag": 25.00}


def to_qty(value):
    try:
        return int(value)
    except Exception:
        return 1


@neatlogs.span(kind="TOOL", tool_name="price_line")
def price_line(item, qty):
    return round(PRICES.get(item, PRICES["pen"]) * qty, 2)


@neatlogs.span(kind="WORKFLOW")
def handle(raw_body):
    try:
        data = json.loads(raw_body)
    except Exception:
        data = {}
    item = data.get("item", "pen")
    qty = to_qty(data.get("qty", 1))
    return {"item": item, "qty": qty, "total": price_line(item, qty)}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self._send(200, {"agent": "quote", "status": "ok"})

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
