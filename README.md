# claude-kit

My user-level Claude Code setup: the global `CLAUDE.md`, delegation subagents, the `handoff` skill and the context-check hook. This repo is the single source for all of them, on my machines and in cloud sessions.

`MANIFEST` lists the files that get installed, relative to `~/.claude`. When you add a file, add it there too.

## Local machines

```bash
git clone https://github.com/mathiaco/claude-kit ~/claude-kit
~/claude-kit/install.sh
```

This symlinks each file into `~/.claude`, so editing `~/.claude/agents/foo.md` edits the repo. Commit and push from `~/claude-kit`.

Register the hook once in `~/.claude/settings.json`. The hook is skipped when a project ships its own copy:

```json
"hooks": {
  "UserPromptSubmit": [
    { "hooks": [ {
      "type": "command",
      "command": "[ -f \"$CLAUDE_PROJECT_DIR/.claude/hooks/context-check.py\" ] || python3 ~/.claude/hooks/context-check.py",
      "timeout": 10
    } ] }
  ]
}
```

## Cloud environments

Paste `cloud-setup.sh` into each personal cloud environment's **Setup script** at claude.ai/code. It downloads the manifest files into `~/.claude` before Claude Code starts.

Limits:

- **Public repo only.** A setup script can't reach a private repo that isn't attached to the session. The GitHub proxy returns 403, so the script uses `raw.githubusercontent.com`.
- **Hooks don't carry over.** Anthropic-hosted sessions don't run hooks from user-level settings. Each repo commits its own `.claude/hooks/` and `.claude/settings.json`.
- **Stale for up to about 7 days.** The environment cache snapshots the setup result. A push here reaches new sessions only once the cache rebuilds: after a script edit, a network-host change, or the cache expiring.
- **Shared environments.** Anyone who uses an environment can read its setup script. Put this only on your own environments.
