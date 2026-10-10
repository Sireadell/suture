"""Clerk2: a small refund-lookup agent. A customer sends an order id and a question, and gets an answer about the refund."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import neatlogs

TRACING = bool(os.environ.get("NEATLOGS_API_KEY"))
if TRACING:
    neatlogs.init(api_key=os.environ["NEATLOGS_API_KEY"], endpoint="https://ingest.neatlogs.com", workflow_name="clerk2")

ORDERS = {
    "A1001": {"item": "Desk lamp", "paid": 42.50, "refund": "approved"},
    "A1002": {"item": "Phone case", "paid": 19.99, "refund": "pending review"},
    "A1003": {"item": "Gift card", "paid": 50.00, "refund": "not eligible"},
}


class BadRequestError(Exception):
    """Raised for client-side input errors (HTTP 400)."""


@neatlogs.span(kind="TOOL", tool_name="lookup_order")
def lookup_order(order_id):
    # Only query if order_id is a valid hashable type (string)
    if not isinstance(order_id, str):
        return None
    return ORDERS.get(order_id)


@neatlogs.span(kind="TOOL", tool_name="write_answer")
def write_answer(order_id, order, question):
    if order is None:
        return f"Order {order_id} could not be found."

    refund = order["refund"]
    if refund == "approved":
        return f"Your refund for the {order['item']} (order {order_id}) is approved. ${order['paid']:.2f} goes back to your card."
    if refund == "pending review":
        return f"Your refund for the {order['item']} (order {order_id}) is pending review. We will email you once it is decided."
    return f"The {order['item']} (order {order_id}) is not eligible for a refund."


@neatlogs.span(kind="WORKFLOW")
def handle(raw_body):
    try:
        data = json.loads(raw_body)
    except json.JSONDecodeError as err:
        raise BadRequestError("Malformed JSON body") from err

    if not isinstance(data, dict):
        raise BadRequestError("Invalid request body structure")

    if "order_id" not in data:
        raise BadRequestError("Missing order_id")

    order_id = data.get("order_id")
    if not isinstance(order_id, str):
        raise BadRequestError("Invalid order_id type")

    question = data.get("question", "")
    order = lookup_order(order_id)
    return {"order_id": order_id, "answer": write_answer(order_id, order, question)}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self._send(200, {"agent": "clerk2", "status": "ok"})

    def do_POST(self):
        length = int(self.headers.get("content-length") or 0)
        raw = self.rfile.read(length).decode("utf-8", errors="replace")
        try:
            self._send(200, handle(raw))
        except BadRequestError as err:
            self._send(400, {"error": str(err)})
        except Exception as err:
            self._send(500, {"error": str(err)})

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
