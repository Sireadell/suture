import json

from app import handle


def ask(item, qty):
    return handle(json.dumps({"item": item, "qty": qty}))


def test_three_notebooks():
    assert ask("notebook", 3)["total"] == 13.5


def test_one_bag():
    assert ask("bag", 1)["total"] == 25.0


def test_ten_pens():
    assert ask("pen", 10)["total"] == 12.0
