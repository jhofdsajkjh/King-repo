#!/bin/bash
# Verify AnySearch CLI scripts exist; copy from WorkBuddy if missing.
# Run before first use each session to ensure scripts are present.

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPTS_DIR="$SKILL_DIR/scripts"
FALLBACK_DIR="$HOME/.workbuddy/skills/anysearch/scripts"
NEEDED=("anysearch_cli.py" "anysearch_cli.js" "anysearch_cli.sh")
MISSING=0

for f in "${NEEDED[@]}"; do
  if [ ! -f "$SCRIPTS_DIR/$f" ]; then
    MISSING=1
    if [ -f "$FALLBACK_DIR/$f" ]; then
      cp "$FALLBACK_DIR/$f" "$SCRIPTS_DIR/$f"
      echo "COPIED: $f (from WorkBuddy)"
    else
      echo "MISSING: $f (not in WorkBuddy either)"
    fi
  fi
done

if [ "$MISSING" -eq 0 ]; then
  echo "OK: All AnySearch CLI scripts present."
fi

exit $MISSING
