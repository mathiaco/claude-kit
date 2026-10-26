#!/usr/bin/env python3
"""UserPromptSubmit hook: nudge toward /handoff once a session's context is large.

Reads the session transcript, takes the context size of the latest main-thread
model call, and, above a threshold, tells Claude to suggest a handoff when the
new prompt starts a different task. Every turn re-reads the whole context, so a
long session costs more per message than a fresh one.

Thresholds (tokens) can be overridden with CLAUDE_HANDOFF_SOFT / CLAUDE_HANDOFF_HARD.
"""
import json
import os
import sys

SOFT = int(os.environ.get("CLAUDE_HANDOFF_SOFT", "150000"))
HARD = int(os.environ.get("CLAUDE_HANDOFF_HARD", "300000"))
TAIL_BYTES = 2_000_000


def context_tokens(transcript_path):
    with open(transcript_path, "rb") as f:
        f.seek(0, os.SEEK_END)
        f.seek(max(0, f.tell() - TAIL_BYTES))
        lines = f.read().decode("utf-8", "ignore").splitlines()
    for line in reversed(lines):
        try:
            entry = json.loads(line)
        except ValueError:
            continue
        if entry.get("type") != "assistant" or entry.get("isSidechain"):
            continue
        usage = (entry.get("message") or {}).get("usage")
        if usage:
            return (
                (usage.get("input_tokens") or 0)
                + (usage.get("cache_read_input_tokens") or 0)
                + (usage.get("cache_creation_input_tokens") or 0)
            )
    return 0


def main():
    try:
        payload = json.load(sys.stdin)
        tokens = context_tokens(payload["transcript_path"])
    except Exception:
        return
    if tokens < SOFT:
        return

    k = round(tokens / 1000)
    advice = (
        f"Session context is about {k}K tokens, and every turn re-reads all of it. "
        "If the user's message starts a different task, feature, or topic from the "
        "current one, first suggest in one or two sentences running /handoff and "
        "continuing in a fresh session, then do what they asked unless they choose "
        "the handoff. If it continues the current task, carry on and suggest "
        "/handoff at the next natural stopping point."
    )
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": advice,
        }
    }
    if tokens >= HARD:
        output["systemMessage"] = (
            f"Context is ~{k}K tokens. Consider /handoff and a new session."
        )
    print(json.dumps(output))


if __name__ == "__main__":
    main()
