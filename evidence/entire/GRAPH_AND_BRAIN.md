# Entire Graph and Brain on Suture

2026-10-10, Entire CLI 0.11.4, Windows 11. Raw output in `raw/graph_*.txt`.

| Step | Command | Result |
| --- | --- | --- |
| Install Graph | `entire plugin install graph` | Installed v0.4.0. First blocked by Windows Smart App Control, worked after the founder turned that off: `entire graph version` prints `v0.4.0` |
| Turn on for the repo | `entire graph init-agents --repo .` | Wrote `.entire/graph-agent.md`, created `AGENTS.md` and `CLAUDE.md` with a managed block telling agents to start with graph search |
| Find the Clerk bug | `entire graph search --query "unknown order id falls back to order A1001 in Clerk" --repo . --top-k 3 --format text` | Top two hits are `targets/clerk/app.py:24-28` (`lookup_order`) and `:42-50` (`handle`), the exact two lines behind the bugs. It also printed "LOW CONFIDENCE" because the two scores tied |
| Blast radius | `entire graph impact --symbol lookup_order --repo .` | 6 callers (1 direct, 5 through `handle`), including the `ask` helper in the test files of clerk, notes, quote and triage |
| What the fix changed | `entire graph commit a88cdde --repo .` | Entity-level: `lookup_order` and `write_answer` bodies changed, one new test added |
| Checkpoint to code | `entire graph checkpoint 01M4KBB9J409096N62BZ6AW98Y --repo .` | Lists the Markdown sections added in that checkpoint's commit; skips `.txt` files with a warning each |
| Install Brain | `entire plugin install brain` | Failed: `plugin "brain" is not in the index`. The docs' `curl ... get-brain.sh \| bash` stops with `unsupported OS: mingw64_nt-10.0-26200` in Git Bash. `entire plugin install https://github.com/entireio/entire-brain` sat at "Checking plugin index..." for over 5 minutes |
| Install Brain by hand | Downloaded `entire-brain_0.1.0_windows_amd64.zip` from the project's GitHub release, sha256 matched `checksums.txt`, then `entire plugin install <path>\entire-brain.exe --force` | Installed. `entire brain version` prints `0.1.0` |
| Set up Brain | `entire brain setup --no-backfill --no-daemon` in this folder | Built sessions, history, docs, patterns, entities, memory. Seed and semantic index **failed**: `dirty_worktree: refusing to seed uncommitted content`, because other sessions have uncommitted files here (`.claude/settings.json` etc.). There is no `--worktree` flag in 0.1.0 despite the message hinting at one |
| Set up Brain, clean copy | Same command in a fresh `git clone` of the repo (scratch folder, not committed) | `+ healthy`: 41 files, 786 symbols, all instant parts built. Daemon is "not supported on windows yet" |
| Overview, brief | `entire brain overview`, `entire brain brief "stop Clerk answering an unknown order id with order A1001"` | Brief names `lookup_order` at `targets/clerk/app.py:27-28`, the Clerk tests, and the session `51a6ab9f` / checkpoint `01M4K70B7PHXAKFTC5KK8NGABZ` as history |
| Query | `entire brain query "why does Clerk fall back to order A1001"` | Returns README sections and a history-gaps note, no decision text. Honest: nothing in the sessions explains it, because the session that wrote Clerk was never captured |
| History coverage | `history-gaps.md` in Brain's data folder (`raw/brain_history_gaps.txt`) | 20 commits, **15 pre-session** (made before the oldest captured session, which includes Clerk's commit fa43b7d), 4 covered by a checkpoint trailer, 1 missing. This is the same finding as WHERE_THE_BUG_CAME_FROM.md, found by Brain on its own |
| Remember, recall | `entire brain remember "..." --kind gotcha --path architecture.clerk.fallback`, then `entire brain recall "Clerk fallback"` | Saved `fact:50577421a0ff1ce1e42db6c3` (Clerk's first draft has the fallback and always-200 on purpose; no checkpoint links to fa43b7d). Recall finds it. The `--path` must be `category.subcategory.type`; `decisions.clerk.first-draft` and `project.clerk.first-draft` were rejected |
| Agent instructions | `entire brain init-agents` | Wrote `.entire/agent-guide.md` and a managed block in `AGENTS.md` and `CLAUDE.md` |
| Not done | `entire brain distill`, the background watcher, `entire brain viz`, MCP | Distilling sends session content to a model provider; the watcher is not supported on Windows |

## Honest limits

| Item | Note |
| --- | --- |
| Graph for the bug-origin view | Graph finds and sizes the code. It does not know who wrote it. Entire's `why`/`blame` give the session and checkpoint, and `graph checkpoint` gives the entity changes of a checkpoint's commit. Together they are the "where the bug came from" view. For Clerk the checkpoint half is empty, see WHERE_THE_BUG_CAME_FROM.md |
| Brain | Used for brief, query, history coverage and one saved fact. Facts are not distilled from sessions (`--no-backfill` on purpose, since that sends session content to a model provider). The saved fact lives in Brain's local data, not in git |
