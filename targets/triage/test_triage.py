import json

from app import handle


def ask(category):
    return handle(json.dumps({"category": category}))


def test_billing():
    assert ask("billing")["route_to"] == "finance-team"


def test_bug():
    assert ask("bug")["route_to"] == "engineering"


def test_account():
    assert ask("account")["route_to"] == "support-team"
