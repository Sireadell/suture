"""Reads the target's failures and the run's cost back from neatlogs through its command line tool.
The login is read-only, so nothing here writes to neatlogs."""
import json
import shutil
import subprocess
from datetime import datetime, timedelta, timezone

CLI = shutil.which("neatlogs") or "neatlogs"


def run(*args: str) -> dict:
    out = subprocess.run([CLI, *args, "--json"], capture_output=True, text=True, timeout=120)
    if out.returncode != 0:
        raise RuntimeError(f"neatlogs {' '.join(args[:2])}: {(out.stdout + out.stderr)[:300]}")
    return json.loads(out.stdout)["data"]


def iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def failing_traces(workflow: str, around_ts: float, before: int = 120, after: int = 60, limit: int = 50) -> list[dict]:
    """Traces of the target whose request body was not a JSON object but which were still answered
    normally (a quiet failure). Skips cut-off previews so big valid bodies are not mistaken for broken ones."""
    frm = iso(around_ts - before)
    to = iso(around_ts + after)
    traces = run("traces", "list", "--workflow", workflow, "--from", frm, "--to", to, "--limit", str(limit))["traces"]
    found = []
    for t in traces:
        spans = run("traces", "raw-spans", t["traceId"])["spans"]
        root = next((s for s in spans if s["spanName"] == "handle"), None)
        if not root or root["input"].get("truncated") or root["status"] != "OK":
            continue
        try:
            raw_body = json.loads(root["input"]["preview"])["raw_body"]
        except (ValueError, KeyError, TypeError):
            continue
        try:
            ok = isinstance(json.loads(raw_body), dict)
        except ValueError:
            ok = False
        if not ok:
            found.append({
                "trace_id": t["traceId"],
                "raw_body": raw_body,
                "answer": root["output"]["preview"],
                "status": root["status"],
            })
    return found


def run_cost(workflow: str, since_ts: float) -> dict:
    """Tokens, cost and model-call time for everything the workflow traced since this moment."""
    frm = iso(since_ts - 5)
    traces = run("traces", "list", "--workflow", workflow, "--from", frm, "--limit", "50")["traces"]
    llm = [t for t in traces if t.get("llmCallsCount")]
    return {
        "trace_ids": [t["traceId"] for t in llm],
        "total_tokens": sum(t["totalTokens"] for t in llm),
        "total_cost_usd": round(sum(t["totalCostUsd"] for t in llm), 6),
        "model_call_seconds": round(sum(t["durationMs"] for t in llm) / 1000),
        "model_calls": len(llm),
    }
