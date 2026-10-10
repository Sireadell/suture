import json

from app import handle


def ask(text):
    return handle(json.dumps({"text": text}))


def test_short_text_is_kept():
    assert ask("Meeting moved to Friday")["summary"] == "Meeting moved to Friday"


def test_long_text_is_cut_to_twelve_words():
    out = ask("one two three four five six seven eight nine ten eleven twelve thirteen fourteen")
    assert out["summary"].endswith("...")
