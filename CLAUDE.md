# How to work across my projects

## Keep the main conversation small

Cost grows with conversation length, because every turn re-reads everything in it. So:

- Don't pull long output into the main conversation: test logs, whole files, PR comment dumps, other sessions' transcripts. Use a subagent that returns a summary.
- When a task or phase is finished, or the topic changes, suggest `/handoff` and a fresh session. Don't carry one session across separate features or for days.

## Delegate

You plan, decide and review. Hand the rest to these subagents:

| Work | Subagent |
|---|---|
| "Where is X / how does Y work / does Z exist" | `code-explorer` |
| Running typecheck, lint, tests or builds | `test-runner` |
| Reading and judging PR review comments | `pr-comment-triage` |
| Writing code for a settled plan, one layer per agent, in parallel when the layers are independent | `plan-implementer` |
| Commit, push, branch, open PR, post replies you've written | `git-shipper` |
| Several web searches or pages: pricing, docs, regulations | `web-researcher` |

Keep for yourself:

- Design and scope decisions.
- Anything where a subtle mistake fails silently (database migrations, security, money).
- Reviewing what subagents return before acting on it.
- Writing meant for other people.

## Review delegated work before building on it

A subagent's report is a claim, not evidence. Before accepting work from `plan-implementer`, or anything else that changed files:

1. **Read the diff yourself** (`git diff`, plus `git status` for new files). Don't rely on the summary.
2. **Check it against the plan.** Is every planned change there? Is anything changed that wasn't planned? Read the "Deviations" and "Stopped at" sections and settle each one.
3. **Review it like a pull request.** Look for correctness, edge cases, the project's conventions from `CLAUDE.md`, and code that duplicates something that already exists.
4. **Then verify** with `test-runner`. Passing tests don't replace step 3.
5. **Fix it or send it back** with a specific brief. Don't let the next step start on top of unreviewed work.

So that parallel work isn't lost or overwritten:

- Give parallel implementers **disjoint files**. If two layers need the same file (a shared `api.ts`, a translation file), give it to one of them or edit it yourself afterwards.
- Never let a subagent run `git stash`, `git checkout -- .`, `git reset` or a rebase while others are working.
- `git-shipper` only commits what you've reviewed. If it reports changes you don't recognise, find out where they came from before committing.

Read-only results (`code-explorer`, `web-researcher`, `pr-comment-triage`) get a lighter check. Open the `path:line` or source behind any finding you're about to act on.

## Delegation size

Don't delegate a small edit or a single grep. A subagent starts with no context and re-reads files, so for small things doing it yourself is cheaper. Give each subagent a complete brief: the goal, the files, the conventions that matter, and what to return.
