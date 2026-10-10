"""The repair loop: prove the failure, ask the model for a fix, test it, put it online,
re-prove it with an outside signed check, and only then offer a pull request."""
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

from . import config, llm, stressproof, tracing

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
    out = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "test_clerk.py"],
        cwd=WORK / TARGET_DIR, capture_output=True, text=True,
    )
    return out.returncode == 0, (out.stdout + out.stderr)[-1500:]


def build_prompt(source: str, tests: str, failures: list[dict], feedback: str) -> str:
    lines = "\n".join(f"- {p['probe']}: {p['outcome']} ({p['reason']})" for p in failures)
    return (
        "You are fixing a small Python web service. An outside tester (StressProof) sent it bad\n"
        f"requests and found these problems:\n{lines}\n\n"
        "Meaning: the service must refuse bad input clearly (an HTTP 4xx status with a JSON error\n"
        "message), never answer a bad request with HTTP 200, and keep working normally for valid\n"
        "requests. Keep the same file layout, port handling and tracing setup. Do not add packages.\n"
        "The existing tests must keep passing.\n\n"
        f"Current file {SOURCE}:\n{FENCE}python\n{source}\n{FENCE}\n\n"
        f"Its tests:\n{FENCE}python\n{tests}\n{FENCE}\n{feedback}\n"
        f"Reply with the COMPLETE replacement for app.py in a single {FENCE}python code block, "
        "and nothing else."
    )


def extract_code(text: str) -> str:
    m = re.search(FENCE + r"(?:python)?\n(.*?)" + FENCE, text, re.S)
    return (m.group(1) if m else text).strip() + "\n"


def write_scorecard(card: dict) -> None:
    EVIDENCE.mkdir(exist_ok=True)
    (EVIDENCE / "scorecard.json").write_text(json.dumps(card, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    started = time.time()
    baseline = stressproof.parse(json.loads(BASELINE.read_text(encoding="utf-8-sig")))
    failures = stressproof.failed_probes(baseline)
    card = {
        "target": "https://suture-clerk.onrender.com",
        "model": llm.MODEL,
        "before_score": baseline["score"],
        "before_silent_wrong": baseline["silentWrongCount"],
        "before_link": baseline["permanentUrl"],
        "after_score": None,
        "after_silent_wrong": None,
        "after_link": None,
        "accepted": False,
        "attempts_used": 0,
        "stressproof_runs_used": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "seconds": 0,
        "attempt_log": [],
    }

    def snapshot() -> None:
        card["input_tokens"] = llm.USAGE["input_tokens"]
        card["output_tokens"] = llm.USAGE["output_tokens"]
        card["seconds"] = round(time.time() - started)
        write_scorecard(card)

    git("fetch", "origin", "main")
    git("reset", "--hard", "origin/main")
    original = (WORK / SOURCE).read_text(encoding="utf-8")
    tests = (WORK / TESTS).read_text(encoding="utf-8")
    feedback = ""
    best = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        card["attempts_used"] = attempt
        entry = {"attempt": attempt}
        card["attempt_log"].append(entry)
        git("reset", "--hard", "origin/main")
        reply = llm.ask(build_prompt(original, tests, failures, feedback))
        (WORK / SOURCE).write_text(extract_code(reply), encoding="utf-8")

        ok, output = run_tests()
        entry["tests_passed"] = ok
        if not ok:
            feedback = f"\nYour last attempt failed the tests:\n{output}\nFix that.\n"
            entry["result"] = "rejected: target tests failed"
            snapshot()
            continue

        git("add", SOURCE)
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
        remaining = stressproof.failed_probes(result)
        feedback = (
            f"\nYour last attempt scored {result['score']} (was {baseline['score']}) with "
            f"{result['silentWrongCount']} quiet failures. Remaining problems: "
            + "; ".join(f"{p['probe']} {p['outcome']}" for p in remaining) + "\n"
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
    snapshot()
    print(json.dumps({k: v for k, v in card.items() if k != "attempt_log"}, indent=2))


if __name__ == "__main__":
    try:
        main()
    finally:
        tracing.stop()
