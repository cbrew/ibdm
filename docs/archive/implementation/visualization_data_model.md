# Visualization Data Model

## Overview

The visualization module provides data structures for capturing, comparing, and visualizing dialogue states and rule execution. This enables:

- **State tracking**: Immutable snapshots of InformationState at specific points
- **Delta visualization**: Detailed diffs showing what changed between states
- **Rule execution tracing**: Recording which rules fired and what they did
- **Timeline views**: Historical record of dialogue progression

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ Dialogue Manager                                            │
│  ↓                                                           │
│  InformationState → StateSnapshot (immutable)               │
│                          ↓                                   │
│                     DiffEngine                               │
│                          ↓                                   │
│                     StateDiff (what changed)                 │
│                          ↓                                   │
│                     Visualization Layer                      │
│                    (terminal/web/export)                     │
└─────────────────────────────────────────────────────────────┘
```

## Core Data Structures

### StateSnapshot

**Purpose**: Immutable snapshot of InformationState at a point in time.

**Key Fields**:
- `timestamp`: Monotonic counter for ordering (0, 1, 2, ...)
- `label`: Human-readable description ("Turn 3: After Integration")
- `qud`: Snapshot of QUD stack (tuple for immutability)
- `commitments`: Snapshot of commitments
- `plan`: Snapshot of active plans
- `agenda`: Snapshot of agenda
- `issues`: Snapshot of private issues
- `beliefs`: Snapshot of beliefs dict
- `overridden_questions`: Snapshot of overridden questions
- `actions`: Snapshot of actions
- `last_move`: Last dialogue move

**Usage**:
```python
from ibdm.visualization import StateSnapshot

# Create snapshot from current state
snapshot = StateSnapshot.from_state(
    state=current_state,
    timestamp=3,
    label="Turn 2: After Integration"
)

# Access fields
print(f"QUD has {len(snapshot.qud)} questions")
print(f"Plans: {len(snapshot.plan)}")
```

**Design Notes**:
- Uses tuples instead of lists for immutability (frozen dataclass)
- Shallow copy of beliefs dict is sufficient (contents are immutable)
- Timestamps are monotonic counters, not wall-clock times

### StateDiff

**Purpose**: Represents changes between two state snapshots.

**Key Components**:
- `before`: Snapshot before change
- `after`: Snapshot after change
- `changed_fields`: Dict of field name → ChangedField
- `summary`: High-level summary ("3 changes: QUD +1, commitments +2")

**ChangedField Structure**:
```python
@dataclass
class ChangedField:
    field_name: str
    change_type: ChangeType  # ADDED, REMOVED, MODIFIED, UNCHANGED
    added_items: list[Any]    # Items added to collection
    removed_items: list[Any]  # Items removed from collection
    modified_items: list[tuple[Any, Any]]  # (before, after) pairs
    before_value: Any         # For scalar fields
    after_value: Any          # For scalar fields
    summary: str              # Human-readable summary
```

**ChangeType Enum**:
- `ADDED`: Item added to collection or field set from None
- `REMOVED`: Item removed from collection or field set to None
- `MODIFIED`: Item changed (scalar or nested object)
- `UNCHANGED`: No change

**Usage**:
```python
from ibdm.visualization import compute_diff

# Compute diff between two snapshots
diff = compute_diff(before_snapshot, after_snapshot)

# Check if there are changes
if diff.has_changes():
    print(diff.format_summary())
    # Output: "2 changes: qud +1, commitments +1"

# Examine specific fields
qud_change = diff.get_changed_field("qud")
if qud_change and qud_change.has_changes():
    print(f"QUD: +{len(qud_change.added_items)} -{len(qud_change.removed_items)}")
    for item in qud_change.added_items:
        print(f"  Added: {item}")
```

### DiffEngine

**Purpose**: Computes diffs between StateSnapshots.

**Algorithm**:
1. **Collection fields** (qud, commitments, plan, etc.):
   - Compare by object identity (id())
   - Find added items (in after but not in before)
   - Find removed items (in before but not in after)

2. **Dict fields** (beliefs):
   - Compare keys
   - Find added, removed, and modified keys
   - Track value changes for modified keys

3. **Scalar fields** (agent_id, last_move):
   - Direct equality comparison
   - Determine ADDED/REMOVED/MODIFIED/UNCHANGED

**Usage**:
```python
from ibdm.visualization import DiffEngine

engine = DiffEngine()
diff = engine.compute_diff(before, after)

# Or use convenience function
from ibdm.visualization import compute_diff
diff = compute_diff(before, after)
```

### RuleTrace

**Purpose**: Records rule execution for a single phase.

**Key Components**:
- `phase`: Phase name ("interpret", "integrate", "select", "generate")
- `timestamp`: When trace was captured
- `label`: Human-readable label
- `evaluations`: List of RuleEvaluation (in priority order)
- `selected_rule`: Name of selected rule (if any)
- `state_before`: State snapshot before rule execution
- `state_after`: State snapshot after rule execution
- `diff`: Computed diff showing what changed
- `metadata`: Additional context (current move, user utterance, etc.)

**RuleEvaluation Structure**:
```python
@dataclass
class RuleEvaluation:
    rule_name: str
    priority: int
    preconditions_met: bool
    was_selected: bool
    reason: str  # Explanation of why it was/wasn't selected
```

**Usage**:
```python
from ibdm.visualization import RuleTrace
from ibdm.visualization.rule_trace import RuleEvaluation

# Create trace for a phase
trace = RuleTrace(
    phase="integrate",
    timestamp=5,
    label="Integration phase complete",
    selected_rule="accommodate_skip_question"
)

# Add rule evaluations
trace.evaluations.append(RuleEvaluation(
    rule_name="accommodate_skip_question",
    priority=9,
    preconditions_met=True,
    was_selected=True,
    reason="User requested skip"
))

trace.evaluations.append(RuleEvaluation(
    rule_name="integrate_answer",
    priority=8,
    preconditions_met=False,
    was_selected=False,
    reason="No answer move detected"
))

# Analyze trace
print(trace.format_summary())
# Output: "integrate: accommodate_skip_question (1/2 rules ready)"

print(f"Rules evaluated: {trace.rules_evaluated()}")
print(f"Rules ready: {trace.rules_with_met_preconditions()}")
```

## Complete Workflow Example

```python
from ibdm.core import InformationState, WhQuestion, SharedIS
from ibdm.visualization import StateSnapshot, compute_diff, RuleTrace
from ibdm.visualization.rule_trace import RuleEvaluation

# 1. Capture state before rule execution
state_before = InformationState()
snapshot_before = StateSnapshot.from_state(
    state_before,
    timestamp=0,
    label="Turn 1: Before Integration"
)

# 2. Execute rules (simulated)
question = WhQuestion(predicate="destination", variable="city")
state_after = InformationState(shared=SharedIS(qud=[question]))
snapshot_after = StateSnapshot.from_state(
    state_after,
    timestamp=1,
    label="Turn 1: After Integration"
)

# 3. Compute diff
diff = compute_diff(snapshot_before, snapshot_after)
print(diff.format_summary())
# Output: "1 changes: qud +1"

# 4. Create rule trace
trace = RuleTrace(
    phase="integrate",
    timestamp=1,
    label="Integration complete",
    evaluations=[
        RuleEvaluation(
            rule_name="integrate_question",
            priority=7,
            preconditions_met=True,
            was_selected=True,
            reason="Ask move detected"
        ),
        RuleEvaluation(
            rule_name="integrate_answer",
            priority=8,
            preconditions_met=False,
            was_selected=False,
            reason="No answer move"
        )
    ],
    selected_rule="integrate_question",
    state_before=snapshot_before,
    state_after=snapshot_after,
    diff=diff
)

# 5. Analyze trace
print(f"Phase: {trace.phase}")
print(f"Selected: {trace.selected_rule}")
print(f"Changes: {trace.diff.format_summary()}")
for eval in trace.evaluations:
    status = "✓" if eval.preconditions_met else "✗"
    selected = " [SELECTED]" if eval.was_selected else ""
    print(f"{status} {eval.rule_name} (p={eval.priority}){selected}")
```

## Design Decisions

### Why Immutable Snapshots?

- **Correctness**: Prevents accidental modification of historical state
- **Performance**: Safe to share snapshots across visualization components
- **Debugging**: Guaranteed that snapshots represent exact state at capture time

### Why Object Identity for Diff?

Using `id()` for collection comparison ensures we track actual object changes, not just equality. This is important because:

- Two different Question objects might be equal but represent different instances
- We want to track "was this specific object added/removed"
- Enables precise tracking of QUD stack operations (push/pop)

### Why Separate Snapshot and Diff?

- **Snapshots** are reusable (can diff same snapshot against multiple others)
- **Diffs** are derived data (can be recomputed from snapshots)
- **Flexibility**: Can compute diffs on-demand or cache them
- **Memory**: Can choose to store snapshots only and compute diffs as needed

### Field Coverage

The visualization module tracks all relevant InformationState fields:

**Shared State**:
- `qud` - Questions Under Discussion stack
- `commitments` - Shared commitments

**Private State**:
- `plan` - Active plans
- `agenda` - Next moves to generate
- `issues` - Accommodated but not yet raised questions
- `beliefs` - Agent beliefs
- `overridden_questions` - Skipped optional questions
- `actions` - Actions to perform
- `last_move` - Last dialogue move

**Metadata**:
- `agent_id` - Agent identifier

## Next Steps

With this data model in place, the next tasks will build on it:

- **ibdm-121**: Rich terminal renderer (uses StateSnapshot and StateDiff)
- **ibdm-122**: Delta visualization (uses StateDiff and ChangeType)
- **ibdm-124**: Rule trace visualization (uses RuleTrace and RuleEvaluation)
- **ibdm-123**: Timeline view (uses sequences of StateSnapshots)

## Testing

Comprehensive tests in `tests/unit/test_visualization.py`:

- StateSnapshot creation and immutability
- Diff engine correctness (added/removed/modified detection)
- ChangedField and ChangeType semantics
- RuleTrace construction and analysis
- Full workflow integration

Run tests:
```bash
pytest tests/unit/test_visualization.py -v
```

## API Reference

See module docstrings for complete API documentation:
- `src/ibdm/visualization/state_snapshot.py`
- `src/ibdm/visualization/state_diff.py`
- `src/ibdm/visualization/diff_engine.py`
- `src/ibdm/visualization/rule_trace.py`
