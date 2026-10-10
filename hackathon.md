# hackathon.md

## Project
**Suture** fixes broken AI agents and only hands over a fix once an outside, signed check shows it worked. It reads the failing agent's neatlogs traces, patches a copy, runs the agent's tests, re-checks with StressProof, retries up to 3 times, and opens a pull request only if quiet failures are 0 and the score did not drop. It never merges.
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
| 2026-10-10 | First full run: Clerk 75 to 92, quiet failures 1 to 0, 1 attempt, PR #1 opened. A later re-run scored 100. |
| 2026-10-10 | Failures and run cost now read back from neatlogs (CLI). Found that neatlogs' token count leaves out thinking tokens, so Suture keeps its own counters too. |
| 2026-10-10 | cfo.ai draft plan numbers written, then replaced with real numbers from the run: about $0.11 per accepted fix. |
| 2026-10-10 | Extra target agents (notes, quote, triage) added with held-out checks. Not yet run, not claimed. |

## Demo
Pending. Demo video (max 3:00) not yet recorded. Reproduce the proven run with the steps in `README.md`.

## Known limitations and next steps
- neatlogs Fixes is not used: the CLI has no Fixes command, and the GitHub connection for this project did not work. After installing the neatlogs GitHub app, the callback address https://ingest.neatlogs.com/api/github/app/callback/user is rejected by GitHub ("redirect_uri is not associated with this application"), so the project's repo field stays empty and no Fixes item is raised. The neatlogs MCP answers with our key (whoami shows an empty project_repo, triage_list shows 0 items). The detection "Clerk wrong answer" does flag the bad traces.
- The neatlogs login is read-only, so the verdict cannot be written back.
- One target is fully proven. The other targets are built but not yet run.
- Entire checkpoints: recording from this commit on.
- Next target to run is notes. It needs two public services (the agent and a patched copy) and a place on the StressProof allowlist first; the repair loop is still set up for Clerk only.
- Next: run the other targets, record the demo, post the build log.

## Submission
| Item | State |
|---|---|
| Public repo with in-window commits | Done |
| neatlogs traces | Done (Clerk and Suture traces exist) |
| Entire checkpoint link and ID | Pending |
| cfo.ai plan | Numbers ready, plan screenshot pending |
| Recovery run | Pending |
| #neatHack posts | None confirmed yet |
| Demo video (max 3:00, all three tools) | Pending |
| Quote post of the official neatlogs X post | Pending, due Mon Oct 12 evening IST |
