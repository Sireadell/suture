"""Clerk: a small refund-lookup agent. A customer sends an order id and a question,
Clerk looks the order up and answers. This is the first draft, written the way a
quick first version usually is, and it is the agent Suture is pointed at."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import neatlogs

TRACING = bool(os.environ.get("NEATLOGS_API_KEY"))
if TRACING:
    neatlogs.init(
        api_key=os.environ["NEATLOGS_API_KEY"],
        endpoint="https://ingest.neatlogs.com",
        workflow_name="clerk",
    )

ORDERS = {
    "A1001": {"item": "Desk lamp", "paid": 42.50, "refund": "approved", "days": 3},
    "A1002": {"item": "Backpack", "paid": 89.00, "refund": "pending review", "days": None},
    "A1003": {"item": "Headphones", "paid": 120.00, "refund": "not eligible, past 30 days", "days": None},
}
DEFAULT_ORDER = "A1001"


@neatlogs.span(kind="TOOL", tool_name="lookup_order")
def lookup_order(order_id):
    return ORDERS.get(order_id)


@neatlogs.span(kind="TOOL", tool_name="write_answer")
def write_answer(order, question):
    if order is None:
        return "We could not find that order. Please check the order number and try again."
    text = str(question).lower()
    if "refund" in text or "money back" in text:
        if order["refund"] == "approved":
            return f"Your refund of ${order['paid']:.2f} for the {order['item']} is approved and arrives in {order['days']} business days."
        return f"Your refund for the {order['item']} is {order['refund']}."
    return f"Your order is the {order['item']}, paid ${order['paid']:.2f}."


@neatlogs.span(kind="WORKFLOW")
def handle(raw_body):
    try:
        data = json.loads(raw_body)
    except Exception:
        data = {}
    order_id = data.get("order_id", DEFAULT_ORDER)
    question = data.get("question", "")
    order = lookup_order(order_id)
    return {"order_id": order_id, "answer": write_answer(order, question)}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self._send(200, {"agent": "clerk", "status": "ok"})

    def do_POST(self):
        length = int(self.headers.get("content-length") or 0)
        raw = self.rfile.read(length).decode("utf-8", errors="replace")
        self._send(200, handle(raw))

    def log_message(self, *args):
        pass


def main():
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    try:
        server.serve_forever()
    finally:
        if TRACING:
            neatlogs.flush()
            neatlogs.shutdown()


if __name__ == "__main__":
    main()
