# neatlogs before and after: Clerk, scored by a neatlogs AI evaluator

Date: 2026-10-10. Project: Sire's project (app.neatlogs.com). All ids below can be opened in the dashboard (login needed, see "Share links").

## What was scored

Eight identical requests were sent to the original Clerk code (before) and to the fixed Clerk code (after, neatlogs-written fix, commit b0ce1b7). Both ran in-process with the neatlogs SDK on and an explicit flush, so each request is one finalized trace with 3 spans (`handle`, `lookup_order`, `write_answer`). Replies are in `evidence/neatlogs_eval_replies_before.json` and `evidence/neatlogs_eval_replies_after.json`. Full per-trace verdicts and reasons are in `evidence/neatlogs_eval_scores.json`.

Judge: neatlogs LLM-judge evaluator "Clerk answer correctness" (id 83cd4955-81e2-4414-8098-e2070b9010fe), run through the neatlogs eval "Clerk Handle Request Review" (id a19cdaa3-2645-411f-a6cf-0634c30625d1, 24 traces, 48 answers, progress 100).

## Numbers

| Request | Before trace | Before reply | Judge | After trace | After reply | Judge |
|---|---|---|---|---|---|---|
| valid A1001 refund | d3d65878 | approved, correct | Yes | a09a9d36 | same | Yes |
| valid A1002 | 2b24f9a8 | pending, correct | Yes | b7c08588 | same | Yes |
| valid A1003 | 30b81f6f | not eligible, correct | Yes | 59c614eb | same | Yes |
| unknown ZZ-FAKE-3 refund | fb5fc336 | **approved $42.50 for a desk lamp** | **No** | 435fc96f | "could not find that order" | **Yes** |
| unknown A9999 | 8be1d283 | desk lamp details | **No** | cf53e4e9 | "could not find that order" | **Yes** |
| malformed JSON | f1b6f6bf | answered with order A1001 | **No** | 65cc8b04 | 400, refused | No (see note) |
| plain text body | 488718c1 | answered with order A1001 | **No** | 1b1afb96 | 400, refused | Yes |
| JSON array body | e2cfd291 | crashed (500) | No | 686a9a13 | 400, refused | No (see note) |
| **Judge "Yes" total** | | | **3 of 8 (37.5%)** | | | **6 of 8 (75%)** |

A second after run (same fixed code, same requests, traces 641e9d95 and others, listed in the scores file) scored 5 of 8. Across both after runs: 11 of 16 (69%) against 3 of 8 (37.5%) before.

The business-critical cases are the two unknown-order requests: before 0 of 2 correct (one approved a refund for an order that does not exist), after 4 of 4 across both after runs.

Note on the refusal cases: the judge only sees a trace whose status is ERROR (the 400 is raised as an exception inside `handle`), so it is unreliable on them. The same refusal got "Yes" once and "No" twice for the same input. Treat the 3 refusal rows as noisy. The independent proof for them is the signed StressProof run: 83 with one quiet failure (first fix) against 100 with none (second fix), in `evidence/neatlogs_fix_attempt_1_clerk.json` and `evidence/neatlogs_fix_attempt_2_clerk.json`.

## Two traces to compare

| | Before | After |
|---|---|---|
| Trace id | f1b6f6bf04c3a79b7f9142b4b002784d | 65cc8b04df341d719fbb32002dea1970 |
| Input | `{"order_id": "A1002", "question": ` (cut off JSON) | same |
| Spans | 3, status OK | 3, status ERROR (request refused with 400) |
| Output | `{"order_id": "A1001", "answer": "Your order is the Desk lamp, paid $42.50."}` | `request body is not valid JSON` |

## Share links

Not possible yet. `neatlogs sharing traces get <id>` returns `state: disabled` for both traces above. The trace page has no share control (Trace actions only offers Copy Markdown, Download Markdown, Download CSV) and the CLI login is read only, so sharing cannot be switched on. The `guest-links` commands are for eval reviewers, not trace viewing. See complaints k and k2. Direct dashboard links (login needed): https://app.neatlogs.com/traces/f1b6f6bf04c3a79b7f9142b4b002784d and https://app.neatlogs.com/traces/65cc8b04df341d719fbb32002dea1970

## Other neatlogs features tried

| Feature | Result |
|---|---|
| Comments | Works. Thread 5bfd3897-bcc2-4a4c-bd01-a2d26d605df3 on the before trace (span 49822016d29f32f4), confirmed with `neatlogs comments list --trace f1b6f6bf04c3a79b7f9142b4b002784d` |
| Session Replay ("Watch replay") | Works. Plays the trace as a 2 second timeline with 0.5x to 4x speed and Skip replay |
| Claude Code plugin | Installed (`@neatlogs/claude-code`, project scope, hooks in `.claude/settings.json`). This build session shows up as traces in workflow `claude-code`: 04a279f997a4824f6f0115a73db13223 (401 spans) and b361644122372bbb2eb62ecaaa2ad50d (51 spans), plus smaller ones. They took about 15 minutes to leave "pending" |
| Alert on "Clerk wrong answer" | Blocked. The detection exists (id 3aa4f0bb-5cbe-44eb-9209-ea68f0398c4c, active) but the New alert wizard says "Create a detection first" and the Detections page says "Couldn't load detections" although the API returns it. CLI `alerts create` is FORBIDDEN (read-only login). Body that should work once write access exists: `{"ruleType":"per_event","name":"Clerk wrong answer","detectionId":"3aa4f0bb-5cbe-44eb-9209-ea68f0398c4c","severity":"critical","cooldownMinutes":15}` |
| neatlogs Investigate chat | Found the malformed-JSON root cause in `targets/clerk/app.py` (swallowed parse error, falls back to order A1001). Thread "Clerk Malformed Request Bug" |
| Fix in > Claude Code | Hand-off only (prompt for the incident). Applied by hand as commit b0ce1b7 |
