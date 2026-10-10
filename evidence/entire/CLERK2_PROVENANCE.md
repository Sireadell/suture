# Clerk2: where the failures came from, with a checkpoint

Clerk2 (`targets/clerk2/`) is a second refund-lookup agent. It was written inside a session Entire was recording, from the plain description of what Clerk does. The old Clerk file was not opened first. Nothing was planted: it was written the way a quick first version is written, and StressProof then scored it as it came.

## Scores (signed StressProof reports)

| | Before | After |
|---|---|---|
| Score | 64 (PARTIAL) | 100 (RESILIENT) |
| Quiet wrong answers | 0 | 0 |
| Loud crashes (HTTP 500) | 4: bad JSON, missing field, wrong type, scrambled copy | 0 |
| Fix written by | | neatlogs Investigate (incident raised, full new `app.py` written) |
| Keep rule (score up, quiet failures 0) | | Passed |

Honest note: clerk2 has no quiet failure. Its faults are loud crashes, so this run shows Suture handling a different kind of fault than Clerk's, and a refusal-style fix scoring 100. It does not show a quiet failure being caught.

## What Entire shows

| Question | Entire's answer | File in `clerk2/` |
|---|---|---|
| Where did the unknown-order crash come from (line 21, `ORDERS.get`, and line 26, indexing a missing order)? | `[AI]` Claude Code, checkpoint 01M4KPV065SEHQQ4NAPYQD2H2A, session 84b136d5, commit 5b59b0e | `why_failure_unknown_id_lookup.txt`, `why_failure_order_none_indexed.txt` |
| Where did the bad-JSON crash come from (line 36, `json.loads` with no guard)? | Same checkpoint, session and commit | `why_failure_bad_json_unhandled.txt` / `.json` |
| Who wrote the fix lines (refusal on bad JSON, order-type check, "could not be found")? | `[AI]` Claude Code, a second checkpoint 01M4KS486XCH2TXNTZ3CTZVGGX, same session, commit 04fd54d | `why_fix_*.txt` |
| Whole file, line by line | Every line `[AI]`; 77 lines from the first checkpoint, the rest from the fix checkpoint | `blame_clerk2_after_fix.txt` |
| Who knows this folder | Claude Code, 1 session, 290 agent-written lines | `experts_after_fix.txt` |

For the first Clerk all of these said "no agent provenance found". For clerk2 each failing line points to the checkpoint that wrote it, and each fix line points to the checkpoint that fixed it.

## What Entire could not show

| Gap | Detail |
|---|---|
| The reason behind a line | `entire why` names the checkpoint and the session, not the choice. The first checkpoint's opening prompt is the long background brief of the parent session, not "write a refund agent". |
| Wrong prompt on the fix line | The fix checkpoint's prompt reads as a message from another session ("Notice from the founder..."), because the last message this session received before the fix was that one. It does not mention neatlogs or the incident. The link from the neatlogs incident to the fix checkpoint is in `evidence/neatlogs_incident_clerk2.json`, written by hand. |
| neatlogs side | neatlogs gave no incident id or link in the chat reply, and wrote the fix as a pasted code block, not a pull request. |
| Failure lines after the fix | `entire why` reads the current file, so the original failing lines can only be queried on `main`, where the fix is not merged. They are not merged: a person decides. |
