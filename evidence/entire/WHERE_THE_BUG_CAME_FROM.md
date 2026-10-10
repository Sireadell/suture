# Where the Clerk bugs came from

Question: for the two Clerk bugs, which session and which Entire checkpoint wrote the code?

| Bug | Line in `targets/clerk/app.py` | Code |
| --- | --- | --- |
| An unknown order id is answered with order A1001 | 23, 28 | `DEFAULT_ORDER = "A1001"` and `ORDERS.get(order_id, ORDERS[DEFAULT_ORDER])` |
| A bad or empty request is answered 200 with a made-up answer | 47, 63-68 | `data.get("order_id", DEFAULT_ORDER)` and `self._send(200, handle(raw))` |

## What Entire says

Commands run with Entire CLI 0.11.4 (output in `raw/why_clerk.txt`, `raw/blame_clerk_json.txt`, `raw/experts.txt`):

| Command | Answer |
| --- | --- |
| `entire blame targets/clerk/app.py --long` | Every line is `[HU]` (made without checkpoint data), author Sireadell, agent and checkpoint columns empty |
| `entire why targets/clerk/app.py:28` (also :23, :47) | "Written by Sireadell, commit fa43b7da, 2026-10-10. No Entire checkpoint is linked to the commit that last touched this line." |
| `entire experts targets/clerk` | "No agent provenance found" |
| `entire search --code DEFAULT_ORDER` | Finds the three lines (23, 28, 47) in the entire.io code index, no session attached |

**Entire has no checkpoint for the Clerk code. We did not invent one.** The reason is in `ENTIRE_NOTES.md` items 2 and 3: the file was written from a session started in the hackathons folder, outside this repo, before Entire was recording here.

## What we can still prove, from other sources

| Fact | Source |
| --- | --- |
| The file `targets/clerk/app.py` was first committed in `fa43b7d`, "Add Clerk, a small refund-lookup agent with tests", 2026-10-10 11:07 +0100 | `git log` |
| It was written by one Write call in Claude Code session `fef4abba-ced1-4858-aca2-bdb3f1d8d5a8` at 2026-10-10T10:06:06Z, one minute before that commit | The session's own transcript on this PC (not in Entire) |
| The code's own header says it is "the first draft, written the way a quick first version usually is", so the fallback to A1001 and the always-200 answer were the deliberately naive starting point, not a surprise | `targets/clerk/app.py` lines 1-3 |
| Entire does know that session: `entire session list` shows `fef4abba` as ended, Claude Code, claude-sonnet-5-5, 80 turns, 29.2M tokens. Its state file says it was attached by hand to `fa43b7d` but the checkpoint ID it records (`01M4JN47KTJYS3FCWM29CD5MD7`) does not exist (`entire checkpoint explain` finds nothing) | `raw/session_list.txt`, `.git/entire-sessions/` |

So the honest answer today is: session `fef4abba`, commit `fa43b7d`, no checkpoint. Entire names the commit and author, and knows the session, but cannot connect the two.

## Graph and Brain on the same question

See GRAPH_AND_BRAIN.md. `entire graph search` points at lines 24-28 and 42-50, `entire graph impact` sizes the change (6 callers), and `entire brain` reports 15 of 20 commits as made before any captured session, which is where Clerk's commit sits. Brain now also holds a saved fact explaining the gap.

## Why we did not import the session

`entire import claude-code --path <hackathons folder> --session fef4abba-... --dry-run` says it would import 314 turns as read-only checkpoints. That would make them searchable and explainable, but they would not be linked to `fa43b7d`, and that session also holds unrelated hackathon work and a key the founder pasted into chat. Checkpoints in this public repo are public. Founder decision, not made here.

## How this becomes a column in the repair scoreboard

The scoreboard already has one row per target. Add one field, `origin`, filled by a small helper that runs `entire why <file>:<line> --json` on the line the repair loop patches. The command was tested on a line that has a checkpoint (`hackathon.md:32`, saved in `raw/why_json_linked_line.txt`) and on a line that does not (Clerk). The JSON gives these fields:

| Scoreboard field | `entire why --json` field | Linked line | Clerk line |
| --- | --- | --- | --- |
| `origin.commit` | `line.commit_sha` | present | present (`fa43b7da`) |
| `origin.tag` | `line.tag` and `line.authorship` | `[AI]` / `ai` | `[HU]` / `human` |
| `origin.checkpoint` | `line.checkpoint_id` | `01M4K70B7PHXAKFTC5KK8NGABZ` | absent |
| `origin.session` | `line.session_id` | `51a6ab9f-...` | absent |
| `origin.agent`, `origin.model` | `line.agent`, `line.model` | Claude Code, claude-sonnet-5-5 | absent |
| `origin.prompt` | `line.prompt` | the session's opening prompt (long, trim it) | absent |

When `checkpoint_id` is absent the column reads `no checkpoint`. For targets whose code is written in sessions run inside this repo (notes, quote and triage came in cbbc0c9; any new one), the column fills in. For Clerk it shows `no checkpoint`, which is true and is itself the finding: the repair loop could point a person to the commit but not to the reasoning behind it. The pull request Suture opens can then quote the origin line next to the fix.

Not built yet: the helper. It is small, around 30 lines, and it belongs in `suture/` which another session owns, so it is left as a proposal.
