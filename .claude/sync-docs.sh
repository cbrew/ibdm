#!/usr/bin/env bash
# Sync CLAUDE.md to AGENTS.md
# This ensures that AI agent instructions remain consistent

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE="${PROJECT_ROOT}/CLAUDE.md"
TARGET="${PROJECT_ROOT}/AGENTS.md"

if [[ ! -f "$SOURCE" ]]; then
    echo "Error: $SOURCE not found" >&2
    exit 1
fi

# Copy CLAUDE.md to AGENTS.md
cp "$SOURCE" "$TARGET"

echo "Synced CLAUDE.md → AGENTS.md"
