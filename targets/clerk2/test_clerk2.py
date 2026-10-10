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


import pytest

from app import BadRequestError


@pytest.mark.parametrize("body", ["{garbage", "", "[1, 2", "[]", json.dumps({"question": "hi"}), json.dumps({"order_id": {"a": 1}})])
def test_bad_body_is_refused(body):
    with pytest.raises(BadRequestError):
        handle(body)


def test_unknown_order_is_not_found():
    assert "could not be found" in ask("ZZ-FAKE-3")
