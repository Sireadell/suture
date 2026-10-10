import json

import pytest

from app import BadRequest, handle


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


def test_exact_answers_for_all_valid_orders():
    assert ask("A1001", "Where is my refund?")["answer"] == (
        "Your refund of $42.50 for the Desk lamp is approved and arrives in 3 business days."
    )
    assert ask("A1002", "refund?")["answer"] == "Your refund for the Backpack is pending review."
    assert ask("A1003", "money back please")["answer"] == (
        "Your refund for the Headphones is not eligible, past 30 days."
    )


def test_order_id_is_echoed_back():
    assert ask("A1003", "What did I buy?")["order_id"] == "A1003"


def test_unknown_order_is_not_answered_as_another_order():
    out = ask("ZZ-FAKE-1", "Where is my refund?")
    assert "could not find" in out["answer"]
    assert "approved" not in out["answer"]


@pytest.mark.parametrize("body", ["{not json", "", "[1, 2]", '"text"'])
def test_malformed_body_is_refused(body):
    with pytest.raises(BadRequest):
        handle(body)
