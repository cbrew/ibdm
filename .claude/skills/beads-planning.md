# Beads Planning and Issue Tracking Skill

This skill enables AI agents to use beads for planning, issue tracking, and task management in the IBDM project.

## About Beads

Beads is a git-backed issue tracker that stores tasks in `.beads/` directory as JSONL files. It provides:
- Distributed task management via Git
- Hash-based IDs (e.g., `bd-a1b2`)
- Hierarchical task organization with parent-child relationships
- Dependency tracking (blocks, related, parent-child)
- Ready work identification (tasks with no blockers)
- JSON output for agent-friendly parsing

## Core Commands

### Creating Issues

```bash
# Basic issue creation
bd create "Task description" -t <type> -p <priority>

# With all options
bd create "Task description" \
  -t <type> \          # bug|feature|task|epic|chore
  -p <priority> \      # 0-4 (0 = highest)
  -a <assignee> \      # username
  -l <labels> \        # comma-separated
  -d "Description" \   # detailed description
  --json               # output JSON for parsing
```

### Creating Child Tasks

```bash
# Create subtask under parent
bd create "Subtask" -t task --parent <parent-id>

# Creates IDs like: bd-a3f8.1, bd-a3f8.2, etc.
```

### Querying Issues

```bash
# Find ready work (no blockers)
bd ready --json

# List all open issues
bd list --json

# Show specific issue
bd show <issue-id> --json

# Filter by criteria
bd list -t feature --status open --json
bd list -p 0 --json  # High priority
bd list -a claude --json  # Assigned to claude
```

### Updating Issues

```bash
# Update status
bd update <issue-id> --status <status>
# Status: open|in_progress|blocked|resolved|closed

# Add labels
bd update <issue-id> -l "phase-1,core"

# Assign
bd update <issue-id> -a claude

# Change priority
bd update <issue-id> -p 1
```

### Managing Dependencies

```bash
# Add blocking relationship
bd update <issue-id> --blocks <other-issue-id>

# Mark as related
bd update <issue-id> --related <other-issue-id>

# Track discovery origin
bd create "Bug found" -t bug --discovered-from <issue-id>
```

### Closing Issues

```bash
bd close <issue-id> --reason "Implementation complete"
```

## Workflow for Development Plans

### 1. Create Epic for Each Phase

```bash
# Phase 1: Core Foundation
bd create "Phase 1: Core Foundation" \
  -t epic \
  -p 1 \
  -l "phase-1" \
  -d "Implement basic data structures and foundation" \
  --json
```

### 2. Create Tasks Under Epics

```bash
# Get epic ID from previous output
EPIC_ID="bd-a1b2"

# Create child tasks
bd create "Implement Question classes" \
  -t task \
  -p 1 \
  -l "phase-1,core" \
  --parent $EPIC_ID \
  --json

bd create "Implement InformationState" \
  -t task \
  -p 1 \
  -l "phase-1,core" \
  --parent $EPIC_ID \
  --json
```

### 3. Track Dependencies

```bash
# Task B depends on Task A
bd update bd-b2c3 --blocks bd-a1b2

# Find what's ready to work on
bd ready --json
```

### 4. Update Progress

```bash
# Start working
bd update bd-a1b2 --status in_progress

# Complete task
bd close bd-a1b2 --reason "Implemented with tests"
```

## Best Practices for IBDM Project

### Task Types
- **epic**: Major phases (Phase 1, Phase 2, etc.)
- **feature**: Significant functionality (Multi-agent system, Burr integration)
- **task**: Specific implementations (Implement WhQuestion class)
- **bug**: Issues discovered during development
- **chore**: Setup, documentation, configuration

### Priority Levels
- **0**: Critical blockers, must do first
- **1**: Important, phase deliverables
- **2**: Standard tasks
- **3**: Nice to have
- **4**: Future/optional

### Labels
Use consistent labels for filtering:
- `phase-1`, `phase-2`, etc. - Phase tracking
- `core`, `rules`, `engine`, `burr`, `multi-agent` - Module areas
- `foundation`, `integration`, `testing` - Work type
- `blocked`, `ready`, `in-review` - Status flags

### Hierarchical Organization

```
bd-abc1 [epic] Phase 1: Core Foundation
├── bd-abc1.1 [task] Implement data structures
│   ├── bd-abc1.1.1 [task] Question classes
│   ├── bd-abc1.1.2 [task] Answer classes
│   └── bd-abc1.1.3 [task] DialogueMove classes
├── bd-abc1.2 [task] Update rule system
└── bd-abc1.3 [task] Unit tests

bd-def2 [epic] Phase 2: Burr Integration
├── bd-def2.1 [task] Design state machine
└── bd-def2.2 [task] Implement actions
```

## Agent Instructions

When asked to create beads tasks from a plan:

1. **Parse the development plan** to identify phases and tasks
2. **Create epics for each phase** with appropriate priority and labels
3. **Create child tasks** for each deliverable under the epic
4. **Set dependencies** where tasks block others
5. **Assign priorities** based on critical path
6. **Add descriptive labels** for filtering
7. **Output task IDs** so they can be referenced later

When asked to find next work:

1. Run `bd ready --json` to get unblocked tasks
2. Filter by priority and current phase
3. Recommend highest-priority ready tasks
4. Update selected task to `in_progress`

When asked to complete work:

1. Update task status to `resolved` or close with reason
2. Check if any blocked tasks are now ready
3. Create new tasks for discovered issues
4. Update parent epic progress

## JSON Parsing Examples

```bash
# Get ready work and parse with jq
bd ready --json | jq -r '.[] | "\(.id): \(.title) [p\(.priority)]"'

# Find high-priority open tasks
bd list -p 0 --json | jq -r '.[] | select(.status == "open")'

# Get all phase-1 tasks
bd list --json | jq '.[] | select(.labels | contains(["phase-1"]))'
```

## Integration with Development Workflow

### Daily Planning
```bash
# Morning: Check what's ready
bd ready -p 0 -p 1 --json

# Start work
bd update <task-id> --status in_progress

# End of day: Update status
bd update <task-id> --status resolved
```

### Weekly Review
```bash
# Check phase progress
bd list -l phase-1 --json | jq 'group_by(.status) | map({status: .[0].status, count: length})'

# Identify blockers
bd list --status blocked --json
```

### Git Integration
Beads automatically syncs with git on a 5-second debounce. Tasks are stored in `.beads/` directory and should be committed with regular code changes.

## Example: Convert IBDM Development Plan to Beads

See the task conversion script that will:
1. Read DEVELOPMENT_PLAN.md
2. Parse phases and tasks
3. Create beads epics and tasks
4. Set up dependencies
5. Output organized task list

This skill enables long-term memory and structured planning for AI agents working on the IBDM project.
