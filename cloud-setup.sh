#!/bin/bash
# Cloud environment setup script. Paste this into the environment's
# "Setup script" box at claude.ai/code.
#
# Setup scripts can't clone through the session's GitHub proxy, so files come
# from raw.githubusercontent.com, which only works because this repo is public.
# Never fails the session: a fetch error leaves ~/.claude as it was.

KIT_RAW="https://raw.githubusercontent.com/mathiaco/claude-kit/main"
DEST="$HOME/.claude"

manifest="$(curl -fsSL "$KIT_RAW/MANIFEST")" || { echo "claude-kit: MANIFEST fetch failed"; exit 0; }

while IFS= read -r rel; do
  [ -z "$rel" ] && continue
  # User-level hooks don't run in Anthropic-hosted sessions; repos ship their own.
  case "$rel" in hooks/*) continue ;; esac
  mkdir -p "$DEST/$(dirname "$rel")"
  curl -fsSL "$KIT_RAW/$rel" -o "$DEST/$rel.tmp" && mv "$DEST/$rel.tmp" "$DEST/$rel" \
    || echo "claude-kit: failed to fetch $rel"
done <<< "$manifest"

exit 0
