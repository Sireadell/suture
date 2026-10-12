"""Fetch signed StressProof reports for Suture's Clerk and Ward runs and print what they say.

Usage:  python verify.py
Needs:  pip install requests
All links come from evidence/scorecard.json. Nothing is trusted from this repo except that file.
"""
import json
import pathlib
import sys

import requests

card = json.loads((pathlib.Path(__file__).parent / "evidence" / "scorecard.json").read_text(encoding="utf-8"))
attempts = card["neatlogs_fixes"]["attempts"]
ward = card["ward"]

reports = [
    ("--- Clerk run ---", None),
    ("Clerk before", card["before_link"]),
    ("Fix 1 (sent back)", attempts[0]["link"]),
    ("Fix 2 (kept)", attempts[1]["link"]),
    ("--- Ward run ---", None),
    ("Ward before", ward["before_link"]),
    ("Ward after", ward["after_link"]),
]

print(f"{'report':<20} {'score':>5} {'verdict':<10} {'quiet wrong':>11}  signed  ran/judged")
failed = False
for name, url in reports:
    if url is None:
        print(name)
        continue
    try:
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        d = r.json()
        rep = d["report"]
        print(
            f"{name:<20} {d['score']:>5} {d['verdict']:<10} {rep['silentWrongCount']:>11}  "
            f"{'yes' if d.get('valid') and d.get('signedByStressProof') else 'NO':<6}  "
            f"{len(rep['probes'])} ran / {rep['probesCompleted']} judged"
        )
    except Exception as e:
        failed = True
        print(f"{name:<20} could not fetch or read: {e}")

sys.exit(1 if failed else 0)
