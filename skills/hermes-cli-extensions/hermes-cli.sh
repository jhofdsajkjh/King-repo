#!/bin/bash
# hermes-cli-extensions wrapper
# Usage: hermes-cli.sh <command> [args...]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

COMMAND="$1"
shift || true

if [ -z "$COMMAND" ]; then
    echo "Usage: hermes-cli.sh <command> [args...]"
    echo "Commands: self-heal-diagnose, self-heal-heal, auto-pr-status, auto-pr-submit, auto-pr-merge, evolve, audit"
    exit 1
fi

SCRIPT_FILE="$SCRIPT_DIR/${COMMAND}.sh"

if [ -f "$SCRIPT_FILE" ]; then
    bash "$SCRIPT_FILE"
else
    echo "Unknown command: $COMMAND"
    exit 1
fi
