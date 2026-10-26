#!/bin/bash
# Local install: symlink every file in MANIFEST into ~/.claude, so edits made
# through ~/.claude land in this repo. An existing real file is moved aside to
# <name>.bak first. Re-running is safe.
set -euo pipefail

KIT="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/.claude"

while IFS= read -r rel; do
  [ -z "$rel" ] && continue
  src="$KIT/$rel"
  dst="$DEST/$rel"
  mkdir -p "$(dirname "$dst")"
  if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$src" ]; then
    continue
  fi
  if [ -e "$dst" ] && [ ! -L "$dst" ]; then
    mv "$dst" "$dst.bak"
    echo "backed up $dst -> $dst.bak"
  fi
  ln -sfn "$src" "$dst"
  echo "linked $rel"
done < "$KIT/MANIFEST"

# The context-check hook is registered in ~/.claude/settings.json, which this
# script doesn't touch. See README.md for the entry to add.
