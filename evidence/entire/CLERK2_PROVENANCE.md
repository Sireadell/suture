# Clerk2: provenance from the first line

Clerk2 (`targets/clerk2/`) is a second refund-lookup agent, written inside a session Entire was recording, from the plain description of what Clerk does. The old Clerk file was not opened first. Raw outputs are in `clerk2/`.

| Question | Entire's answer today | File |
| --- | --- | --- |
| Who wrote `app.py`, line by line? | Every line `[AI]`, Claude Code, claude-sonnet-5-5, checkpoint 01M4KPV065SEHQQ4NAPYQD2H2A, session 84b136d5, commit 5b59b0e | `clerk2/blame_clerk2.txt` |
| Where did the lookup code come from (`entire why` on line 14)? | Same checkpoint and session, with a link to the full context | `clerk2/why_lookup_order.txt` |
| Who knows this folder (`entire experts`)? | Claude Code, 1 session, 3 steps, 99 agent-written lines | `clerk2/experts.txt` |

This is the difference from the first Clerk, where all three commands said "no agent provenance found".

## Not done yet

| Item | State |
| --- | --- |
| StressProof before and after for clerk2 | Not run. The two new service addresses must be added to the StressProof allowlist, and the automatic safety check refused that edit from this session. The founder's main session has to apply it. |
| Whether clerk2 has a quiet failure | Not known yet. It was not written with a planted bug, and no claim is made either way until StressProof has scored it. |
| `entire why` on failure lines and fix lines | Waits for the run above. |
