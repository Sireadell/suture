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
| Set up Brain | `entire brain setup --no-backfill --no-daemon` | **Not run.** The session's safety check refused the command, so Brain is installed but has no memory built for this repo. Needs the founder's go-ahead |

## Honest limits

| Item | Note |
| --- | --- |
| Graph for the bug-origin view | Graph finds and sizes the code. It does not know who wrote it. Entire's `why`/`blame` give the session and checkpoint, and `graph checkpoint` gives the entity changes of a checkpoint's commit. Together they are the "where the bug came from" view. For Clerk the checkpoint half is empty, see WHERE_THE_BUG_CAME_FROM.md |
| Brain | Installed, not used. `--no-backfill` was chosen on purpose, because the default setup sends session content to a model provider and can cost tokens |
