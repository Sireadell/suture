# hackathon.md

## Project
**Suture** fixes broken AI agents and only hands over a fix once an outside, signed check shows it worked. It reads the failing agent's neatlogs traces, patches a copy, runs the agent's tests, re-checks with StressProof, retries up to 3 times, and opens a pull request only if quiet failures are 0 and the score goes up. It never merges.
Problem: AI agents often answer bad input with a confident wrong answer, and a model-suggested fix is not proof the fix worked.
Track: Build an agent that works (literally).

## Team
Sireadell (solo).

## Stack
| Part | What |
|---|---|
| Agent | Python repair loop (`suture/loop.py`) |
| Model | Gemini (`gemini-flash-latest`) through google-genai |
| neatlogs | Tracing for Suture and the target agents; failing runs and run cost read back with the neatlogs CLI |
| Entire | Session checkpoints for this repo |
| cfo.ai | Business plan: price, cost, revenue, runway |
| Outside check | StressProof (my earlier project, called as a service) |
| Hosting | Render for the target agent and the patched copy |

## Build log
| Date (IST) | What happened |
|---|---|
| 2026-10-10 | Project started. Setup, neatlogs tracing, first traced Gemini call confirmed. |
| 2026-10-10 | Clerk (refund-lookup agent) built with neatlogs tracing. First StressProof run: score 50, then 75 with 1 quiet failure. |
| 2026-10-10 | Repair loop built: StressProof client, patch on a copy, tests, re-check, keep rule, pull request. |
| 2026-10-10 | First full run on Clerk with Suture's own model: 75 to 100, quiet failures 1 to 0, 1 attempt, PR #2 opened (PR #1 was an earlier attempt and is closed). |
| 2026-10-10 | Failures and run cost now read back from neatlogs (CLI). Found that neatlogs' token count leaves out thinking tokens, so Suture keeps its own counters too. |
| 2026-10-10 | cfo.ai draft plan numbers written, then replaced with real numbers from the run: about $0.11 per accepted fix when Suture's model writes it, $0.015 when neatlogs writes it and Suture only checks. |
| 2026-10-10 | neatlogs wrote two fixes for Clerk. Fix 1: 83 with 1 quiet wrong answer, sent back. Fix 2: 100 with 0, kept, PR #4. |
| 2026-10-10 | Notes run: 83 to 100, quiet failures 1 to 0. Clerk2 run: 64 to 100 (4 loud crashes before), PR #3. Signed reports for all three are in `evidence/`. |

## Demo
Demo video (max 3:00) not yet recorded. To check the proof without the video, run `python verify.py` (see `README.md`).

## Known limitations and next steps
- neatlogs Fixes was used as a hand-off (PRs #3 and #4): it gives a fix to apply, not a pull request. The GitHub app connection did not work: after installing it, the callback address https://ingest.neatlogs.com/api/github/app/callback/user is rejected by GitHub ("redirect_uri is not associated with this application"), so the project's repo field stays empty. The detection "Clerk wrong answer" does flag the bad traces.
- The neatlogs login is read-only, so the verdict cannot be written back.
- Three targets have signed before and after reports: Clerk (75 to 100), Notes (83 to 100), Clerk2 (64 to 100). A score of 100 means 12 checks ran and the 6 that could be judged all passed. The other agents in `targets/` are not claimed.
- Next: record the demo, post the build log.

## Submission
| Item | State |
|---|---|
| Public repo with in-window commits | Done |
| neatlogs traces | Done (Clerk, Notes, Clerk2 and Suture traces exist) |
| Signed before and after reports | Done: Clerk, Notes, Clerk2, in `evidence/` |
| Entire checkpoint link and ID | Done: ID `01M4K70B7PHXAKFTC5KK8NGABZ`, link https://entire.io/gh/Sireadell/suture/commit/9699aaefe605297591e5b4a22550d126d8cbce6e |
| cfo.ai plan | Done: numbers and screenshots in `evidence/cfo/` |
| Recovery run | Fix 1 refused (83, 1 quiet wrong answer), Fix 2 kept (100, PR #4). Fix 1 was judged by the hand-run check, not by loop output. |
| #neatHack posts | None confirmed yet |
| Demo video (max 3:00, all three tools) | Pending |
| Quote post of the official neatlogs X post | Pending, due Mon Oct 12 evening IST |
