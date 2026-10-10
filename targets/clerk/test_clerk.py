import json

from app import handle


def ask(order_id, question):
    return handle(json.dumps({"order_id": order_id, "question": question}))


def test_approved_refund_is_explained():
    out = ask("A1001", "Where is my refund?")
    assert "approved" in out["answer"]
    assert "$42.50" in out["answer"]


def test_pending_refund_is_reported():
    out = ask("A1002", "Do I get my money back?")
    assert "pending review" in out["answer"]


def test_ineligible_refund_is_reported():
    out = ask("A1003", "refund please")
    assert "not eligible" in out["answer"]


def test_order_question_names_the_item():
    out = ask("A1002", "What did I buy?")
    assert "Backpack" in out["answer"]
