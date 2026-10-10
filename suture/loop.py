"""The repair loop: prove the failure, ask the model for a fix, test it, put it online,
re-prove it with an outside signed check, and only then offer a pull request."""
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import neatlogs
import requests

from . import config, llm, neatlogs_cli, stressproof, tracing

ROOT = config.ROOT
WORK = ROOT / "work" / "repo"
EVIDENCE = ROOT / "evidence"
TARGET_DIR = "targets/clerk"
SOURCE = f"{TARGET_DIR}/app.py"
TESTS = f"{TARGET_DIR}/test_clerk.py"
CANDIDATE_BRANCH = "suture-candidate"
CANDIDATE_SERVICE = "srv-db51aoad0e5s73drii1g"
CANDIDATE_URL = "https://suture-clerk-candidate.onrender.com"
BASELINE = EVIDENCE / "before_clerk_v1_run2.json"
MAX_ATTEMPTS = 3
RENDER_API = "https://api.render.com/v1"
FENCE = "`" * 3


def git(*args: str, check: bool = True) -> str:
    out = subprocess.run(["git", *args], cwd=WORK, capture_output=True, text=True)
    if check and out.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {out.stderr.strip()}")
    return out.stdout.strip()


def render_headers() -> dict:
    key = (Path.home() / ".render" / "api_key_stressproof").read_text().strip()
    return {"Authorization": f"Bearer {key}"}


def wait_for_deploy(commit: str, timeout: int = 600) -> None:
    """Wait until Render reports the candidate service live on this commit."""
    end = time.time() + timeout
    while time.time() < end:
        resp = requests.get(
            f"{RENDER_API}/services/{CANDIDATE_SERVICE}/deploys?limit=5", headers=render_headers(), timeout=30
        )
        for item in resp.json():
            d = item["deploy"]
            if (d.get("commit") or {}).get("id", "").startswith(commit[:7]):
                if d["status"] == "live":
                    return
                if d["status"] in ("build_failed", "update_failed", "canceled", "deactivated"):
                    raise RuntimeError(f"deploy {d['status']}")
        time.sleep(15)
    raise RuntimeError("deploy did not go live in time")


def run_tests() -> tuple[bool, str]:
    env = {**os.environ, "NEATLOGS_API_KEY": ""}  # keep test runs out of the target's real traces
    out = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=WORK / TARGET_DIR, capture_output=True, text=True, env=env,
    )
    return out.returncode == 0, (out.stdout + out.stderr)[-1500:]


def build_prompt(source: str, tests: str, evidence: list[dict], feedback: str) -> str:
    lines = "\n".join(
        f"- trace {e['trace_id']}: request body {e['raw_body']!r} was answered with {e['answer']}"
        for e in evidence
    )
    return (
        "You are fixing a small Python web service. Its traces in neatlogs show requests whose body is\n"
        "not valid JSON, yet the service answered them normally with HTTP 200 and made up an answer:\n"
        f"{lines}\n\n"
        "Meaning: the service must refuse bad input clearly (an HTTP 4xx status with a JSON error\n"
        "message), never answer a bad request with HTTP 200, and keep answering valid requests exactly\n"
        "as before (valid orders A1001, A1002, A1003 must still get their correct answers).\n"
        "Keep the same file layout, port handling and tracing setup. Do not add packages.\n"
        "The existing tests must keep passing.\n\n"
        f"Current file {SOURCE}:\n{FENCE}python\n{source}\n{FENCE}\n\n"
        f"Its tests:\n{FENCE}python\n{tests}\n{FENCE}\n{feedback}\n"
        f"Reply with the COMPLETE replacement for app.py in a single {FENCE}python code block, "
        "and nothing else."
    )


REGRESSION_TEMPLATE = '''"""Written by Suture from real failing traces in neatlogs. Bad bodies must be refused
with a 4xx and a JSON error, and valid orders must still get their correct answers."""
import json
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

import pytest

import app

BAD_BODIES = {bad}
VALID = {{
    "A1001": ("Where is my refund?", ["approved", "$42.50"]),
    "A1002": ("Do I get my money back?", ["pending review"]),
    "A1003": ("refund please", ["not eligible"]),
}}


@pytest.fixture(scope="module")
def base():
    server = ThreadingHTTPServer(("127.0.0.1", 0), app.Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{{server.server_port}}"
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
    status, text = post(base, json.dumps({{"order_id": order_id, "question": question}}))
    assert status == 200
    answer = json.loads(text)["answer"]
    for word in words:
        assert word in answer
'''


def write_regression_tests(evidence: list[dict]) -> None:
    bodies = sorted({e["raw_body"] for e in evidence} | {"{garbage", "", "[1, 2"})
    (WORK / TARGET_DIR / "test_regression.py").write_text(
        REGRESSION_TEMPLATE.format(bad=repr(bodies)), encoding="utf-8"
    )


def extract_code(text: str) -> str:
    m = re.search(FENCE + r"(?:python)?\n(.*?)" + FENCE, text, re.S)
    return (m.group(1) if m else text).strip() + "\n"


def write_scorecard(card: dict) -> None:
    EVIDENCE.mkdir(exist_ok=True)
    (EVIDENCE / "scorecard.json").write_text(json.dumps(card, indent=2) + "\n", encoding="utf-8")


@neatlogs.span(kind="WORKFLOW", name="suture_run")
def repair(card: dict, snapshot) -> None:
    raw_before = json.loads(BASELINE.read_text(encoding="utf-8-sig"))
    baseline = stressproof.parse(raw_before)
    evidence = neatlogs_cli.failing_traces("clerk", raw_before["certificate"]["timestamp"])
    if not evidence:
        raise RuntimeError("no failing traces found in neatlogs for the before run")
    card["failing_trace_ids"] = [e["trace_id"] for e in evidence]

    git("fetch", "origin", "main")
    git("reset", "--hard", "origin/main")
    original = (WORK / SOURCE).read_text(encoding="utf-8")
    tests = (WORK / TESTS).read_text(encoding="utf-8")

    # The new tests must fail on today's Clerk, otherwise they prove nothing.
    write_regression_tests(evidence)
    reproduced, _ = run_tests()
    card["regression_test_fails_on_original"] = not reproduced
    snapshot()
    feedback = ""
    best = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        card["attempts_used"] = attempt
        entry = {"attempt": attempt, "fix_source": f"model {llm.MODEL}", "trace_ids_used": card["failing_trace_ids"]}
        card["attempt_log"].append(entry)
        git("reset", "--hard", "origin/main")
        write_regression_tests(evidence)
        reply = llm.ask(build_prompt(original, tests, evidence, feedback))
        (WORK / SOURCE).write_text(extract_code(reply), encoding="utf-8")

        ok, output = run_tests()
        entry["tests_passed"] = ok
        if not ok:
            feedback = f"\nYour last attempt failed the tests:\n{output}\nFix that.\n"
            entry["result"] = "rejected: target tests failed"
            snapshot()
            continue

        git("add", SOURCE, f"{TARGET_DIR}/test_regression.py")
        git("commit", "-m", "Reject bad requests with a clear error instead of answering 200")
        git("push", "--force", "origin", f"HEAD:{CANDIDATE_BRANCH}")
        sha = git("rev-parse", "HEAD")
        wait_for_deploy(sha)

        result = stressproof.certify(CANDIDATE_URL)
        card["stressproof_runs_used"] += 1
        entry.update(score=result["score"], silent_wrong=result["silentWrongCount"], link=result["permanentUrl"])
        (EVIDENCE / f"attempt_{attempt}_clerk.json").write_text(
            json.dumps(result["raw"], indent=2) + "\n", encoding="utf-8"
        )
        if result["score"] > baseline["score"] and result["silentWrongCount"] == 0:
            entry["result"] = "accepted"
            best = result
            break
        entry["result"] = "rejected: score did not rise or quiet failures remain"
        feedback = (
            f"\nYour last attempt scored {result['score']} (was {baseline['score']}) with "
            f"{result['silentWrongCount']} quiet failures. Remaining problems: "
            + "; ".join(f"{p['probe']} {p['outcome']}" for p in stressproof.failed_probes(result)) + "\n"
        )
        snapshot()

    if best:
        (EVIDENCE / "after_clerk_v2.json").write_text(json.dumps(best["raw"], indent=2) + "\n", encoding="utf-8")
        card.update(
            accepted=True, after_score=best["score"], after_silent_wrong=best["silentWrongCount"],
            after_link=best["permanentUrl"],
        )
        branch = "suture/fix-clerk-" + datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")
        git("push", "origin", f"HEAD:refs/heads/{branch}")
        card["pull_request_branch"] = branch
    else:
        git("reset", "--hard", "origin/main")


def main() -> None:
    started = time.time()
    baseline = stressproof.parse(json.loads(BASELINE.read_text(encoding="utf-8-sig")))
    card = {
        "target": "https://suture-clerk.onrender.com",
        "model": llm.MODEL,
        "failures_found_with": "neatlogs traces (CLI); StressProof used only for the signed before and after proof",
        "neatlogs_fixes": "not used: the neatlogs CLI has no Fixes command",
        "neatlogs_verdict_writeback": "not done: the CLI login is read-only (project:read)",
        "before_score": baseline["score"],
        "before_silent_wrong": baseline["silentWrongCount"],
        "before_link": baseline["permanentUrl"],
        "after_score": None,
        "after_silent_wrong": None,
        "after_link": None,
        "accepted": False,
        "attempts_used": 0,
        "stressproof_runs_used": 0,
        "attempt_log": [],
    }

    def snapshot() -> None:
        card["seconds"] = round(time.time() - started)
        card["own_counters_crosscheck"] = dict(llm.USAGE)
        write_scorecard(card)

    try:
        repair(card, snapshot)
    finally:
        tracing.stop()
    snapshot()
    time.sleep(20)  # let neatlogs finish ingesting this run before reading its cost back
    card["neatlogs_cost"] = neatlogs_cli.run_cost("suture", started)
    write_scorecard(card)
    print(json.dumps({k: v for k, v in card.items() if k != "attempt_log"}, indent=2))


if __name__ == "__main__":
    main()
