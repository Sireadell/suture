# Suture

An agent that fixes broken agents, and only hands the fix over once an outside check shows it worked.

Built for neatHack, track "Build an agent that works (literally)".

neatlogs finds what broke and can suggest a fix. Suture tests the fix, and only hands it over once a signed outside check shows it worked.

## What it does

You point Suture at an AI agent that sometimes gets things wrong. Suture then:

1. Runs the outside check (StressProof, 12 probes) on the agent and saves the signed "before" report.
2. Reads the failing runs from the agent's neatlogs traces, so it fixes what actually broke, not what it guesses broke.
3. Asks the model for a patch and applies it to a copy of the agent, never the original.
4. Runs the agent's own tests, plus a new test written from the failure that fails on the original code.
5. Puts the patched copy online and runs StressProof again for the signed "after" report.
6. Keeps the fix only if quiet failures (wrong answers that look fine) are 0 and the score did not drop. Otherwise it throws the patch away and tries again, up to 3 times.
7. If a fix is kept, it opens a pull request. It never merges. A person decides.

## One run you can check

Target: Clerk, a small refund-lookup agent (`targets/clerk`). Its first draft answered broken requests with a confident, made-up answer.

| | Before | After |
|---|---|---|
| StressProof score | 75 (PARTIAL) | 92 in the pull request, 100 in the latest re-run |
| Quiet failures | 1 | 0 |
| Attempts used | | 1 of 3 |
| Cost of the fix | | about $0.11 (model about $0.10, two outside checks $0.01) |

The signed reports and the numbers are in `evidence/`. The pull request is [#1](https://github.com/Sireadell/suture/pull/1).

## Try it yourself in one minute

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env      # then fill in your own keys
python -m pytest targets\clerk
python -m suture.loop
```

Open any signed report link in `evidence/scorecard.json`. Each one is a StressProof page anyone can verify.

## How it uses the three event tools

| Tool | Use in Suture |
|---|---|
| neatlogs | Suture traces itself and the target agent. It reads failing runs and its own cost back through the neatlogs command line. |
| Entire | Build sessions are recorded as checkpoints on this repo, linked from the submission. |
| cfo.ai | The business plan: price per accepted fix, cost per fix, revenue and runway. Numbers come from the real run above. |

## What existed before the event

StressProof, the outside checker, is my earlier project (github.com/Sireadell/stressproof). Suture calls it as a service. Everything in this repo (the repair loop, the neatlogs reading, the keep rule, Clerk and the other test agents) was written during the event.

## What this is not

- It does not merge anything. It opens a pull request and stops.
- It does not promise a fix every time. If it cannot prove a fix, it hands back nothing and says so.
- It is not a general bug fixer. It repairs one kind of fault, agents that answer bad input with a confident wrong answer.
- It does not prove the target is perfect. A score of 100 means the 12 probes passed, nothing more.
- Today it has one fully proven target. More are in `targets/` and are not claimed until their runs are in `evidence/`.

## Limits I know about

- neatlogs Fixes is not used yet. The command line has no Fixes command, and connecting GitHub in neatlogs did not work for this project.
- The neatlogs login I have is read-only, so Suture cannot write its verdict back into neatlogs.
- neatlogs cost counts leave out the model's thinking tokens, so Suture also keeps its own counters and reports the larger number.
