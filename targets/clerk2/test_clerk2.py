import json

from app import handle


def ask(order_id, question="Where is my refund?"):
    return handle(json.dumps({"order_id": order_id, "question": question}))["answer"]


def test_approved_refund():
    answer = ask("A1001")
    assert "approved" in answer and "$42.50" in answer


def test_pending_refund():
    assert "pending review" in ask("A1002")


def test_not_eligible_refund():
    assert "not eligible" in ask("A1003")
