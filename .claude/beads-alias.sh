#!/usr/bin/env bash
# Convenience aliases for beads with Larsson tracking
# Source this file in your shell: source .claude/beads-alias.sh

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Primary alias - use beads-larsson for tracked workflow
alias bd-start="${PROJECT_ROOT}/.claude/beads-larsson.sh start"
alias bd-complete="${PROJECT_ROOT}/.claude/beads-larsson.sh complete"
alias bd-measure="${PROJECT_ROOT}/.claude/beads-larsson.sh measure"

# Standard beads commands (untracked)
alias bd-ready="${PROJECT_ROOT}/.claude/beads-helpers.sh ready"
alias bd-current="${PROJECT_ROOT}/.claude/beads-helpers.sh current"
alias bd-summary="${PROJECT_ROOT}/.claude/beads-helpers.sh summary"
alias bd-phase="${PROJECT_ROOT}/.claude/beads-helpers.sh phase"
alias bd-urgent="${PROJECT_ROOT}/.claude/beads-helpers.sh urgent"

# Quick access to full command
alias bdl="${PROJECT_ROOT}/.claude/beads-larsson.sh"

echo "Beads + Larsson aliases loaded:"
echo "  bd-start <task>      - Start task with Larsson baseline & prediction"
echo "  bd-complete <task>   - Complete task with Larsson review"
echo "  bd-measure [label]   - Quick Larsson measurement"
echo "  bd-ready             - Show ready tasks"
echo "  bd-current           - Show in-progress tasks"
echo "  bd-summary           - Project summary"
echo "  bdl                  - Full beads-larsson command"