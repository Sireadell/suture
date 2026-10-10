"""Client for the outside StressProof service: warm the target, run the check, parse the verdict."""
import time

import requests

from . import config

STRESSPROOF_URL = config.get("STRESSPROOF_URL", "https://stressproof-6g88.onrender.com").rstrip("/")
SAMPLE_BODY = {"order_id": "A1001", "question": "Where is my refund?"}


def warm(url: str, tries: int = 12, wait: float = 10.0) -> bool:
    """Free Render hosts sleep and answer 502 while waking. Wait until a GET returns 200."""
    for _ in range(tries):
        try:
            if requests.get(url, timeout=30).status_code == 200:
                return True
        except requests.RequestException:
            pass
        time.sleep(wait)
    return False


def certify(target_url: str, sample_body: dict | None = None, retries: int = 2) -> dict:
    """Run one StressProof check against a public https target and return the parsed result."""
    if not warm(target_url):
        raise RuntimeError(f"target never woke up: {target_url}")
    warm(STRESSPROOF_URL + "/about", tries=6)
    payload = {"targetUrl": target_url, "method": "POST", "sampleBody": sample_body or SAMPLE_BODY}
    last = None
    for attempt in range(retries + 1):
        resp = requests.post(STRESSPROOF_URL + "/demo/certify", json=payload, timeout=180)
        if resp.status_code == 200:
            return parse(resp.json())
        last = f"HTTP {resp.status_code}: {resp.text[:300]}"
        time.sleep(10)
    raise RuntimeError(f"StressProof failed: {last}")


def parse(raw: dict) -> dict:
    report = raw["report"]
    return {
        "score": report["score"],
        "verdict": report["verdict"],
        "silentWrongCount": report["silentWrongCount"],
        "probes": [
            {"probe": p["probe"], "outcome": p["outcome"], "points": p["points"], "reason": p["reason"]}
            for p in report["probes"]
        ],
        "permanentUrl": raw.get("permanentUrl"),
        "raw": raw,
    }


def failed_probes(result: dict) -> list[dict]:
    """Probes that lost points or answered quietly wrong (not unclear, not skipped)."""
    return [
        p for p in result["probes"]
        if p["outcome"] in ("SILENT_WRONG", "DEGRADED", "FAIL", "CRASH") or p["outcome"].startswith("LOUD")
    ]
