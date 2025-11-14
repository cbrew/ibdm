# Compliance Task Executor Skill - Analysis & Improvements

**Date**: 2025-11-14
**Author**: Claude Code
**Status**: Analysis Complete

## Executive Summary

The Larsson Compliance Task Executor skill successfully selected and tracked a task, but revealed several systemic issues:

1. **Task was already complete** - Selected ibdm-bsr.1 which had already been implemented
2. **No compliance improvement** - Predicted +1.0 point, actual was 0.0 (as expected for already-complete work)
3. **Task metadata is stale** - Beads tasks don't reflect actual codebase state
4. **Metrics are valid** - The tracker IS measuring real code properties (verified)

## What Went Wrong

### Issue 1: Task Completion Not Tracked

**Problem**: Task `ibdm-bsr.1` ("Extract InformationState from engine to Burr State") was scored 0.85/1.00 and selected as highest-impact, but the work was **already done** in previous commits.

**Evidence**:
- `DialogueMoveEngine.__init__()` has NO `self.state` (verified in `dialogue_engine.py:23-33`)
- All methods accept `state: InformationState` as parameter (verified `interpret:72`, `integrate:98`, `select_action:123`)
- `initialize` action creates InformationState in Burr State (verified `actions.py:181-219`)
- Tests pass (533 passed, confirming stateless architecture works)

**Root Cause**: The beads task database (`.beads/issues.jsonl`) has `status: "open"` for tasks that are actually complete. There's no automatic synchronization between task completion in code and task status in beads.

### Issue 2: Impact Prediction Inaccuracy

**Problem**: Predicted +1.0 compliance improvement, actual was 0.0.

**Why This Happened**: This is actually **correct behavior**! Since the task was already complete, no code change → no compliance change. The prediction assumed the task represented unimplemented work.

**Implication**: The heuristic scoring system works correctly, but it relies on accurate task status. Garbage in → garbage out.

### Issue 3: Stale Task Metadata

**Problem**: 172 open tasks reported, but many may be complete, blocked, or obsolete.

**Evidence**:
```bash
$ grep '"status":"open"' .beads/issues.jsonl | wc -l
172
```

But the codebase shows substantial Phase 2.5 work already done (stateless engine, Burr integration, domain layer).

**Impact**:
- Agents waste time on already-complete work
- High-scoring tasks may be low-value (duplicates, obsolete)
- True high-impact tasks may score lower if metadata is wrong

### Issue 4: No Task Completion Detection

**Problem**: The skill has no mechanism to detect if a task is already complete before selecting it.

**What's Missing**:
- Pre-execution validation ("Is InformationState already extracted?")
- Code introspection to check if requirements are met
- Automatic task status updates based on code state

**Current Flow**:
```
1. Score tasks based on metadata ✓
2. Select highest-scoring task ✓
3. Execute task (blindly, no validation) ✗
4. Measure impact ✓
```

**Ideal Flow**:
```
1. Score tasks based on metadata ✓
2. Validate top candidates (check if already done) ← NEW
3. Skip completed tasks ← NEW
4. Select highest-scoring incomplete task ✓
5. Execute with confidence ✓
6. Measure impact ✓
7. Auto-mark task complete in beads ← NEW
```

## What Went Right

### Metrics Are Real ✓

I verified that the Larsson compliance metrics measure **actual code properties**:

**Architectural Compliance** (`larsson_fidelity.py:69-242`):
- ✓ Checks for four-phase architecture (interpret/integrate/select/generate)
- ✓ Verifies explicit state passing (inspects method signatures)
- ✓ Validates single-rule-per-cycle pattern
- ✓ Uses AST/inspect modules to analyze actual code

**Information State Structure** (`larsson_fidelity.py:249-400`):
- ✓ Checks private/shared separation
- ✓ Validates required fields (plan, agenda, qud, etc.)
- ✓ Verifies QUD is a stack (LIFO semantics)
- ✓ Detects hidden state in engines

**Rules Coverage**, **Semantic Operations**, **Domain Independence**:
- All check real code presence/absence
- Count actual implementations vs. required per Larsson (2002)

**Conclusion**: The metrics framework is **solid and trustworthy**. The issue is task selection, not measurement.

### Task Scoring Heuristics Are Reasonable ✓

The scoring algorithm makes sense:

```python
# Label-based (40%)
"burr", "state-extraction" → +15% (Architectural)
"rules", "ibis1" → +15% (Rules Coverage)
"domain", "semantic" → +10% (Domain Independence)

# Priority (20%)
P0 → +20%, P1 → +15%, P2 → +10%

# Type (20%)
task → +20%, bug → +15%, epic → +5%

# Phase (10%)
phase-2.5 → +10% (current focus)

# Ready (10%)
status=open → +10%
```

**This is well-designed** for selecting high-impact work. The problem is the input data (task metadata), not the algorithm.

### Skill Workflow Is Sound ✓

The overall design is good:
1. Baseline snapshot ✓
2. Task analysis ✓
3. Selection with rationale ✓
4. Execution guidance ✓
5. Post-task snapshot ✓
6. Delta reporting ✓

The issue is Step 3-4 need **validation** before execution.

## Proposed Fixes

### Fix 1: Pre-Execution Validation

Add a validation step before executing tasks:

```python
def validate_task_completion(task: TaskScore) -> tuple[bool, str]:
    """
    Check if task requirements are already met.

    Returns:
        (is_complete, reason)
    """
    task_id = task.task_id

    # Task-specific validators
    validators = {
        "ibdm-bsr.1": validate_state_extraction,
        "ibdm-bsr.2": validate_initialize_action,
        "ibdm-bsr.3": validate_interpret_signature,
        # ... more validators
    }

    validator = validators.get(task_id)
    if validator:
        return validator()

    # Default: assume incomplete
    return False, "No validator available"


def validate_state_extraction() -> tuple[bool, str]:
    """Check if InformationState is extracted from engine."""
    try:
        from ibdm.engine import DialogueMoveEngine
        import inspect

        # Check 1: No self.state in __init__
        source = inspect.getsource(DialogueMoveEngine.__init__)
        if "self.state" in source:
            return False, "Engine still has self.state"

        # Check 2: Methods accept state parameter
        sig = inspect.signature(DialogueMoveEngine.integrate)
        if "state" not in sig.parameters:
            return False, "Methods don't accept state parameter"

        # Check 3: Burr initialize action creates InformationState
        from ibdm.burr_integration.actions import initialize
        init_source = inspect.getsource(initialize)
        if "InformationState(" not in init_source:
            return False, "Initialize action doesn't create InformationState"

        return True, "All requirements met"
    except Exception as e:
        return False, f"Validation error: {e}"
```

**Integration**:
```python
# In main(), after task selection:
is_complete, reason = validate_task_completion(selected)
if is_complete:
    print(f"✓ Task already complete: {reason}")
    print("Skipping to next task...")
    # Select next task and retry
else:
    print(f"✓ Task validation passed: {reason}")
    # Proceed with execution
```

### Fix 2: Task Completion Auto-Detection

After successful execution and metric improvement, auto-mark task as done:

```python
def mark_task_complete(task_id: str, commit_hash: str) -> None:
    """Mark task as complete in beads database."""
    # Read issues.jsonl
    issues = []
    with open(".beads/issues.jsonl") as f:
        for line in f:
            task = json.loads(line)
            if task["id"] == task_id:
                task["status"] = "done"
                task["metadata"] = task.get("metadata", {})
                task["metadata"]["completed_by_skill"] = True
                task["metadata"]["commit"] = commit_hash
                task["metadata"]["completed_at"] = datetime.now().isoformat()
            issues.append(task)

    # Write back
    with open(".beads/issues.jsonl", "w") as f:
        for task in issues:
            f.write(json.dumps(task) + "\n")
```

**When to call**:
```python
# After delta comparison
if actual_delta > 0:
    print(f"✓ Compliance improved by {actual_delta:.1f} points")
    mark_task_complete(selected.task_id, current_commit_hash)
    print(f"✓ Marked {selected.task_id} as complete in beads")
elif actual_delta == 0 and task_was_already_complete:
    # Task was prerequisite work or already done
    mark_task_complete(selected.task_id, current_commit_hash)
    print(f"✓ Marked {selected.task_id} as complete (prerequisite work)")
```

### Fix 3: Improved Task Filtering

Filter out obviously stale tasks:

```python
def filter_stale_tasks(tasks: list[TaskScore]) -> list[TaskScore]:
    """Remove tasks that are likely stale or complete."""
    filtered = []

    for task in tasks:
        # Check 1: Has the task been open for >30 days with no activity?
        # (Would need timestamp metadata)

        # Check 2: Is there a validator that says it's complete?
        is_complete, _ = validate_task_completion(task)
        if is_complete:
            print(f"  Skipping {task.task_id} (already complete)")
            continue

        # Check 3: Are dependencies met?
        # (Would need dependency metadata)

        filtered.append(task)

    return filtered
```

### Fix 4: Better Error Guidance

When task execution finds it's already complete:

```python
# Current behavior:
# - Execute task
# - Find it's done
# - Report "no change"
# - User confused

# Better behavior:
# - Validate before execution
# - If complete: explain what was found
# - If incomplete: execute
# - Update task status either way

if is_complete:
    print(f"""
Task {selected.task_id} Validation Result: ALREADY COMPLETE
================================================================================

Evidence:
{reason}

This task was completed in a previous session. The beads metadata is stale.

Actions:
1. Marking task as complete in beads database
2. Selecting next highest-impact task
3. Re-running selection process

This is expected behavior when task metadata is not synchronized with code state.
Next time, this task will be filtered out automatically.
""")
```

### Fix 5: Periodic Task Audit

Add a command to audit all tasks against current code:

```python
# New command:
python .claude/compliance-task-executor.py --audit

# Output:
# Auditing 172 open tasks...
#
# COMPLETE (45 tasks):
#   ✓ ibdm-bsr.1 (state extraction done)
#   ✓ ibdm-bsr.2 (initialize action implemented)
#   ...
#
# READY (32 tasks):
#   → ibdm-rules.5 (add IntegrateAsk rule)
#   → ibdm-semantic.2 (implement resolves())
#   ...
#
# BLOCKED (15 tasks):
#   ✗ ibdm-phase4.1 (depends on ibdm-phase3.*)
#   ...
#
# UNCLEAR (80 tasks):
#   ? ibdm-misc.42 (no validator available)
#   ...
#
# Recommendations:
# - Mark 45 complete tasks as done
# - Focus on 32 ready tasks
# - Review 15 blocked tasks for dependency resolution
# - Create validators for 80 unclear tasks
```

## Immediate Actions

### Action 1: Validate Top 10 Tasks Manually

Since we just ran the skill, let's validate the top 5 tasks it identified:

1. **ibdm-bsr.1** - ✓ COMPLETE (just verified)
2. **ibdm-bsr.2** - Need to check
3. **ibdm-bsr.3** - Need to check
4. **ibdm-bsr.4** - Need to check
5. **ibdm-bsr.5** - Need to check

Recommendation: Run validation checks on these before next execution.

### Action 2: Add Basic Validators

Create validators for the BSR (Burr State Refactoring) series:

```python
BSR_VALIDATORS = {
    "ibdm-bsr.1": validate_state_extraction,  # ✓ Complete
    "ibdm-bsr.2": validate_initialize_creates_state,  # Check Burr action
    "ibdm-bsr.3": validate_interpret_signature,  # Check method signature
    "ibdm-bsr.4": validate_integrate_pure,  # Check integrate is pure function
    "ibdm-bsr.5": validate_select_signature,  # Check select_action signature
}
```

### Action 3: Improve Skill Documentation

Update `.claude/skills/larsson-compliance-task-executor.md`:

**Add Section**:
```markdown
## Known Limitations

1. **Task metadata may be stale** - The skill relies on beads task status, which
   may not reflect actual code state. Pre-execution validation coming soon.

2. **No automatic task completion** - After executing a task, you must manually
   mark it complete in beads. Auto-completion feature planned.

3. **Limited validators** - Only some tasks have completion validators. Unknown
   tasks are assumed incomplete.

## Workarounds

If selected task is already complete:
1. Note the evidence (method signatures, test results, etc.)
2. Manually mark task as done: `bd done <task-id> "Already complete"`
3. Re-run skill to select next task
```

### Action 4: Enhance Metrics Report

Add a "Task Validation" section to the output:

```
Step 3: Validating selected task...
--------------------------------------------------------------------------------
Task: ibdm-bsr.1
Validation: ALREADY COMPLETE ✓

Evidence:
  ✓ DialogueMoveEngine has no self.state
  ✓ All methods accept state parameter
  ✓ Burr initialize creates InformationState
  ✓ Tests pass (533/533)

Conclusion: Task completed in commit 8a7e91a (2025-11-12)
Action: Skipping to next task
```

## Long-Term Improvements

### 1. Beads Integration

Enhance the skill to work directly with beads:

```bash
# After task completion
python .claude/compliance-task-executor.py --execute ibdm-bsr.1 --auto-complete

# This would:
# 1. Execute task
# 2. Run tests
# 3. Commit changes
# 4. Run bd done <task-id> "Completed via compliance skill"
```

### 2. Task Dependency Graph

Build a dependency graph from task metadata:

```python
# Parse task descriptions for dependencies
# "Depends on: ibdm-bsr.1, ibdm-bsr.2"
# → Create DAG
# → Only show ready tasks (dependencies met)
```

### 3. AI-Powered Validation

Use LLM to validate task completion:

```python
def ai_validate_task(task: TaskScore) -> tuple[bool, str]:
    """Use LLM to check if task requirements are met."""
    prompt = f"""
    Task: {task.title}
    Description: {task.description}

    Analyze the codebase and determine if this task is already complete.
    Provide evidence from the code.
    """
    # Use Claude to inspect codebase and provide judgment
```

### 4. Metric-Driven Validation

Check if task completion would improve specific metrics:

```python
# If task says "add IntegrateAsk rule"
# → Check if Rules Coverage would increase
# → If already at expected level, task might be done
```

## Conclusion

**The skill design is sound**, but it needs:
1. ✅ Pre-execution validation (to avoid wasted work)
2. ✅ Auto task completion (to keep metadata fresh)
3. ✅ Better error messages (to guide users)
4. ✅ Periodic audits (to detect stale tasks)

**The metrics are trustworthy** - they measure real code properties, not metadata.

**Immediate next steps**:
1. Add basic validators for top 10 tasks
2. Validate ibdm-bsr.2 through ibdm-bsr.5
3. Mark ibdm-bsr.1 as complete in beads
4. Re-run skill to test with updated task list

This analysis provides a clear path forward for improving the skill's reliability and usefulness.
