"""Ward is a demo with fake patients only."""
import json

import pytest

from app import handle


def ask(patient_id):
    return handle(json.dumps({"patient_id": patient_id}))


def test_first_patient_medications():
    out = ask("P-1001")
    assert [m["name"] for m in out["medications"]] == ["Metformin", "Lisinopril"]
    assert "Metformin" in out["answer"]


def test_second_patient_medications():
    assert [m["name"] for m in ask("P-1002")["medications"]] == ["Levothyroxine"]


def test_third_patient_has_three_medications():
    assert len(ask("P-1003")["medications"]) == 3


def test_unknown_patient_is_an_error():
    with pytest.raises(LookupError):
        ask("P-9999")
