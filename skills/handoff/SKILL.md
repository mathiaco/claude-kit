---
name: handoff
description: Close out a long or finished session so the next one starts small. Writes the current state, decisions and next steps into the project's state file and produces a short prompt to open the next session with. Use when a task or phase is done, when the topic changes, when the session has run for many hours or days, or when the user says "handoff", "wrap up", or "new session".
---

A session's cost grows with its length: every turn re-reads the whole conversation. This skill moves what matters out of the conversation and into the repository, so a fresh session can pick up from a few hundred lines instead of hundreds of thousands of tokens.

## 1. Find the state file

Use the project's existing one if it has one: `docs/TODO.md`, `docs/ROADMAP.md`, `HANDOFF.md`, or whatever `CLAUDE.md` names. Otherwise create `docs/HANDOFF.md`. Don't make a second state file next to an existing one.

## 2. Update it

Write only what the next session can't get from the code or `git log`:

- **Where things stand** — what is done, what is in progress, on which branch and PR.
- **Decisions made**, with the one-line reason for each, especially the non-obvious ones and the alternatives that were rejected.
- **Open questions**, and who has to answer them.
- **Next steps**, in order, specific enough to start on without re-reading this conversation.
- **Gotchas found** — things that cost time and would cost it again. If one is a lasting project rule, put it in `CLAUDE.md` instead.

Edit the existing sections in place. Strike or delete what's finished rather than appending a new dated log each time.

## 3. Commit only if allowed

If the project or the user holds commits until reviewed, leave the change in the working tree and say so. Otherwise commit just the state file, separately from code changes.

## 4. Hand over

Give the user, in this order:

1. One line on what was saved and where.
2. A ready-to-paste opening prompt for the next session, under 10 lines: the goal, the branch, "read `<state file>` first", and the first next step.
3. A reminder to start that in a **new session**, not this one.
