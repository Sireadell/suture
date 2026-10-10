"""Written by Suture from real failing traces in neatlogs. Bad bodies must be refused
with a 4xx and a JSON error, and valid orders must still get their correct answers."""
import json
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

import pytest

import app

BAD_BODIES = ['', '[1, 2', '{"question":"Where is my refund?","order_id":"A1001"', '{garbage']
VALID = {
    "A1001": ("Where is my refund?", ["approved", "$42.50"]),
    "A1002": ("Do I get my money back?", ["pending review"]),
    "A1003": ("refund please", ["not eligible"]),
}


@pytest.fixture(scope="module")
def base():
    server = ThreadingHTTPServer(("127.0.0.1", 0), app.Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_port}"
    server.shutdown()


def post(base, body):
    req = urllib.request.Request(base, data=body.encode(), method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as err:
        return err.code, err.read().decode()


@pytest.mark.parametrize("body", BAD_BODIES)
def test_bad_body_is_refused(base, body):
    status, text = post(base, body)
    assert 400 <= status < 500
    assert "error" in json.loads(text)


@pytest.mark.parametrize("order_id", sorted(VALID))
def test_valid_order_is_still_answered(base, order_id):
    question, words = VALID[order_id]
    status, text = post(base, json.dumps({"order_id": order_id, "question": question}))
    assert status == 200
    answer = json.loads(text)["answer"]
    for word in words:
        assert word in answer
