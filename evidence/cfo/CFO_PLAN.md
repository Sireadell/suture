# Suture business plan in cfo.ai

Built in cfo.ai (Ari, the cfo.ai AI CFO) on 2026-10-10. Two versions of the same plan, kept side by side.

- Guess version: frozen in cfo.ai as the snapshot "Suture guess numbers (before)".
- Real-number version: the Main Scenario, updated by Ari with the measured first run.
- Extra: a scenario "Suture cautious, 70% acceptance" keeps the cautious yield on the real cost base.
- Pages in the plan: Financial plan, Unit economics, Assumptions, Cash and scenarios.

## What was entered
Guess version: $1.00 per accepted fix, 12,000 in and 2,000 out tokens, 1.8 attempts, 70% accepted, $0.005 per outside check at 2.8 runs, $32.26 fixed per month, $500 start, 100 / 1,000 / 10,000 fixes a month.

Real version: same price and fixed costs, with measured values from Suture's first live run (evidence/scorecard.json): 1 attempt, accepted 1 of 1, 1,660 input and 27,099 output tokens (including thinking), 2 outside checks, score 75 to 100, quiet failures 1 to 0, 382 seconds.

## What changed between guess and real (numbers produced by cfo.ai)
| Item | Guess | Real |
|---|---|---|
| Cost per accepted fix, to Dec 2026 | $0.062 | $0.113 |
| Cost per accepted fix, from Jan 2027 | $0.105 | $0.216 |
| Margin at $1.00, to Dec 2026 | 93.76% | 88.71% |
| Margin from Jan 2027 | 89.51% | 78.43% |
| Break-even fixes per month, before / after Jan 2027 | 35 / 37 | 37 / 42 |
| Profit at 100 fixes a month, before / after Jan 2027 | $61.50 / $57.25 | $56.45 / $46.17 |
| Profit at 1,000 fixes a month | $905.31 / $862.88 | $854.87 / $752.01 |
| Profit at 10,000 fixes a month | $9,330.71 / $8,906.43 | $8,839.08 / $7,810.42 |
| Runway on $500, no revenue | 15.50 months | 15.50 months (unchanged, fixed costs same) |
| Cautious case (70% accepted), cost per fix | n/a | $0.161 before / $0.308 after, margin 83.88% / 69.18%, break-even 39 / 47 |

Why the cost went up: the guess assumed 2,000 output tokens, the real run used 27,099 because the model's thinking tokens count. Fewer attempts (1 instead of 1.8) pulled it back down.

## Screenshots
1_guess_plan_top_snapshot.jpg, 2_guess_pricing_rules_snapshot.jpg (guess version, 93.76% and 35 to 37 break-even), 3_real_plan_top.jpg, 4_real_pricing_rules.jpg, 5_real_ari_summary.jpg (real version).
Note: the data grids inside the pages did not render values in the automated browser (grey placeholders), so the screenshots show cfo.ai's written plan text and Ari's summary tables, not the grids.

## cfo.ai gaps found
- The grid tables showed grey placeholder bars and never filled in with numbers in the automated Chrome session, so a visual before and after of the grids was not capturable.
- A snapshot is the only way to keep the earlier version: it pins the plan but later work does not flow into it. Fine, but you must remember to take it before editing.
- Ari had no way to read our scorecard or traces directly; the real numbers had to be pasted into chat.
- No purchase, upgrade or payment control was touched. No limit of the free plan was hit.
