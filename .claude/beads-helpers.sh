#!/bin/bash
# Beads helper commands for IBDM project

# Show ready work (tasks with no blockers)
ready() {
  echo "=== Ready Tasks (No Blockers) ==="
  bd ready --json | jq -r '.[] | "  \(.id): \(.title) [P\(.priority)]"'
}

# Show tasks for current phase
phase() {
  local phase_num=${1:-1}
  echo "=== Phase $phase_num Tasks ==="
  bd list --json | jq -r --arg phase "phase-$phase_num" \
    '.[] | select(.labels | contains([$phase])) | "  [\(.status)] \(.id): \(.title) [P\(.priority)]"'
}

# Start working on a task
start() {
  local task_id=$1
  if [ -z "$task_id" ]; then
    echo "Usage: start <task-id>"
    return 1
  fi
  bd update "$task_id" --status in_progress
  echo "Started: $task_id"
}

# Complete a task
done() {
  local task_id=$1
  local reason=${2:-"Implemented"}
  if [ -z "$task_id" ]; then
    echo "Usage: done <task-id> [reason]"
    return 1
  fi
  bd close "$task_id" --reason "$reason"
  echo "Completed: $task_id"
  echo ""
  echo "Newly ready tasks:"
  bd ready --json | jq -r '.[] | "  \(.id): \(.title) [P\(.priority)]"' | head -5
}

# Show progress for a phase
progress() {
  local phase_num=${1:-1}
  echo "=== Phase $phase_num Progress ==="
  bd list --json | jq -r --arg phase "phase-$phase_num" \
    '.[] | select(.labels | contains([$phase]))' | \
    jq -s 'group_by(.status) | map({status: .[0].status, count: length}) | .[] | "  \(.status): \(.count)"'
}

# Create a new task discovered during work
discover() {
  local title=$1
  local parent=${2:-}
  local priority=${3:-2}

  if [ -z "$title" ]; then
    echo "Usage: discover <title> [parent-id] [priority]"
    return 1
  fi

  if [ -n "$parent" ]; then
    bd create "$title" -t task -p "$priority" --parent "$parent" --json | \
      jq -r '"Created: \(.id): \(.title)"'
  else
    bd create "$title" -t task -p "$priority" --json | \
      jq -r '"Created: \(.id): \(.title)"'
  fi
}

# Show current work (in_progress tasks)
current() {
  echo "=== Current Work (In Progress) ==="
  bd list --json | jq -r '.[] | select(.status == "in_progress") | "  \(.id): \(.title) [P\(.priority)]"'
}

# Show high priority tasks
urgent() {
  echo "=== High Priority Tasks (P0-P1) ==="
  bd list --json | jq -r '.[] | select(.priority <= 1 and .status == "open") | "  \(.id): \(.title) [P\(.priority)]"'
}

# Quick summary
summary() {
  echo "=== IBDM Project Summary ==="
  echo ""
  echo "Status:"
  bd list --json | jq -s '.[0] | group_by(.status) | map({status: .[0].status, count: length}) | .[] | "  \(.status): \(.count)"'
  echo ""
  echo "By Priority:"
  bd list --json | jq -s '.[0] | group_by(.priority) | map({priority: .[0].priority, count: length}) | .[] | "  P\(.priority): \(.count)"'
  echo ""
  echo "Ready work:"
  bd ready --json | jq -r '.[] | select(.priority <= 1) | "  \(.id): \(.title) [P\(.priority)]"' | head -5
}

# Show all functions
help() {
  echo "IBDM Beads Helper Commands:"
  echo ""
  echo "  ready              - Show tasks with no blockers"
  echo "  phase <N>          - Show tasks for phase N"
  echo "  start <id>         - Mark task as in_progress"
  echo "  done <id> [reason] - Complete a task"
  echo "  progress <N>       - Show progress for phase N"
  echo "  discover <title>   - Create new task discovered during work"
  echo "  current            - Show in_progress tasks"
  echo "  urgent             - Show high priority tasks"
  echo "  summary            - Project summary"
  echo ""
  echo "Examples:"
  echo "  ready"
  echo "  phase 1"
  echo "  start ibdm-brm.1"
  echo "  done ibdm-brm.1 'Implemented with tests'"
  echo "  discover 'Fix typing issues in Question class' ibdm-brm.1 0"
}

# If sourced, make functions available
# If executed, run the command
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
  if [ $# -eq 0 ]; then
    help
  else
    "$@"
  fi
fi
