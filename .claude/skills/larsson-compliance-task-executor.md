# Larsson Compliance Task Executor Skill

This skill enables AI agents to automatically select, execute, and measure the impact of beads tasks on Larsson framework compliance. It combines task selection heuristics with before/after metrics comparison to demonstrate tangible compliance improvements.

## About This Skill

This skill extends the `larsson-compliance-metrics` skill by adding intelligent task selection and execution capabilities. It helps agents:
- Heuristically identify tasks likely to improve Larsson compliance
- Execute those tasks systematically
- Measure and report the compliance impact

## Workflow Overview

```
┌─────────────────────────────────────┐
│ 1. Take Baseline Compliance Snapshot│
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 2. Analyze Open Beads Tasks         │
│    - Parse .beads/issues.jsonl      │
│    - Apply heuristic scoring        │
│    - Rank by likely impact          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 3. Select Highest-Impact Task       │
│    - Check task is ready (no blocks)│
│    - Verify prerequisites           │
│    - Present selection rationale    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 4. Execute Task                     │
│    - Implement required changes     │
│    - Run quality checks             │
│    - Commit changes                 │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 5. Take Post-Task Snapshot          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 6. Compare & Report Delta           │
│    - Show compliance changes        │
│    - Highlight improvements         │
│    - Recommend next steps           │
└─────────────────────────────────────┘
```

## Task Selection Heuristics

The skill uses a weighted scoring system to identify tasks likely to improve Larsson compliance:

### Priority Scoring Factors

1. **Label-Based Signals (40% weight)**
   - `burr`, `state-extraction`, `stateless`: High impact on Architectural Compliance
   - `rules`, `ibis1`, `update-rules`, `selection-rules`: High impact on Rules Coverage
   - `domain`, `semantic`, `predicates`: High impact on Domain Independence
   - `qud`, `information-state`: High impact on Information State
   - `refactoring`, `larsson-alignment`: General compliance improvements

2. **Task Type (20% weight)**
   - `task`: Direct implementation work (high impact)
   - `bug`: Quality improvements (medium impact)
   - `epic`: Large scope (lower immediate impact, but important)

3. **Priority Level (20% weight)**
   - P0: Critical (highest weight)
   - P1: High priority
   - P2+: Lower priority

4. **Phase Alignment (10% weight)**
   - `phase-2.5`: Current phase (Burr refactoring)
   - `phase-3`: NLU integration
   - Other phases

5. **Dependency Status (10% weight)**
   - Ready tasks (no blockers) scored higher
   - Tasks with blockers scored lower

### Scoring Algorithm

```python
def calculate_impact_score(task: dict) -> float:
    """Calculate likelihood that task will improve Larsson compliance."""
    score = 0.0

    # Label analysis (40%)
    labels = set(task.get('labels', []))
    if labels & {'burr', 'state-extraction', 'stateless', 'architectural'}:
        score += 0.15  # Architectural Compliance
    if labels & {'rules', 'ibis1', 'update-rules', 'selection-rules'}:
        score += 0.15  # Rules Coverage
    if labels & {'domain', 'semantic', 'predicates'}:
        score += 0.10  # Domain Independence
    if labels & {'qud', 'information-state'}:
        score += 0.10  # Information State
    if labels & {'refactoring', 'larsson-alignment'}:
        score += 0.10  # General improvements

    # Task type (20%)
    task_type = task.get('issue_type', 'task')
    type_weights = {'task': 0.20, 'bug': 0.15, 'feature': 0.12, 'epic': 0.05}
    score += type_weights.get(task_type, 0.10)

    # Priority (20%)
    priority = task.get('priority', 2)
    priority_weights = {0: 0.20, 1: 0.15, 2: 0.10}
    score += priority_weights.get(priority, 0.05)

    # Phase alignment (10%)
    if 'phase-2.5' in labels:
        score += 0.10
    elif 'phase-3' in labels:
        score += 0.08

    # Ready status (10%)
    status = task.get('status', 'open')
    if status == 'open':
        score += 0.10

    return score
```

## Usage Instructions

### Agent Command

When asked to "work on Larsson compliance" or "improve compliance metrics":

```bash
# Run the task executor helper
python .claude/compliance-task-executor.py
```

This will:
1. Take baseline metrics snapshot
2. Analyze all open tasks
3. Select highest-impact task based on heuristics
4. Present the selected task and rationale
5. Wait for confirmation
6. Execute the task
7. Take post-task snapshot
8. Report compliance delta

### Options

```bash
# Auto-execute without confirmation
python .claude/compliance-task-executor.py --auto

# Specify minimum impact score threshold
python .claude/compliance-task-executor.py --min-score 0.5

# Show top N candidates instead of just one
python .claude/compliance-task-executor.py --show-top 5

# Dry-run: Show selection without executing
python .claude/compliance-task-executor.py --dry-run
```

## Example Session

```
=== Larsson Compliance Task Executor ===

Step 1: Taking baseline compliance snapshot...
Baseline Compliance: 87.5/100 ✗ FAIL
  Architectural Compliance: 95.0/100 ✓
  Information State: 100.0/100 ✓
  Semantic Operations: 75.0/100 ✗
  Rules Coverage: 70.0/100 ✗
  Domain Independence: 85.0/100 ✓

Step 2: Analyzing 172 open tasks...
Applied heuristic scoring to identify high-impact tasks.

Step 3: Selected highest-impact task:
┌─────────────────────────────────────────────────────────┐
│ Task: ibdm-bsr.1                                        │
│ Title: Extract InformationState from engine to Burr     │
│ Priority: P0                                            │
│ Impact Score: 0.85/1.00                                 │
└─────────────────────────────────────────────────────────┘

Selection Rationale:
✓ High-impact labels: burr, state-extraction, architectural
✓ Task type: task (direct implementation)
✓ Priority: P0 (critical)
✓ Phase: phase-2.5 (current focus)
✓ Status: open (ready to work)
✓ Expected impact: +10-15% Architectural Compliance

Predicted Compliance Impact:
  Overall: 87.5 → 92-95 (↑ 5-8%)
  Architectural Compliance: 95.0 → 100.0 (↑ 5%)

Continue with this task? [Y/n] Y

Step 4: Executing task ibdm-bsr.1...
[Implementation details...]
✓ Tests passing
✓ Quality checks passing
✓ Changes committed

Step 5: Taking post-task snapshot...
Post-Task Compliance: 92.3/100 ✓ PASS

Step 6: Compliance Delta Report
================================
Overall: 87.5 → 92.3 (+4.8) ✓ NOW PASSING

Component Changes:
  [+] Architectural Compliance: 95.0 → 100.0 (+5.0) ✓
  [=] Information State: 100.0 → 100.0 (no change) ✓
  [=] Semantic Operations: 75.0 → 75.0 (no change) ✗
  [=] Rules Coverage: 70.0 → 70.0 (no change) ✗
  [=] Domain Independence: 85.0 → 85.0 (no change) ✓

Issues:
  Resolved (2):
    ✓ Hidden state detected in engine
    ✓ Explicit state passing violated

  New (0):
    (none)

Recommendations (3 remaining):
  • Implement remaining IBiS1 update rules
  • Add resolves() semantic operation
  • Register domain plan builders

=== SUCCESS ===
Task ibdm-bsr.1 improved Larsson compliance by +4.8%
Next high-impact task: ibdm-bsr.2 (score: 0.82)
```

## Integration with Development Workflow

### Incremental Compliance Improvement

```bash
# Run repeatedly to incrementally improve compliance
while true; do
  python .claude/compliance-task-executor.py --auto --min-score 0.6
  if [ $? -ne 0 ]; then
    echo "No more high-impact tasks available"
    break
  fi
done
```

### Sprint Goals

```bash
# Target: Reach 90% compliance by end of sprint
python .claude/compliance-task-executor.py --target 90.0 --max-iterations 10
```

### Focused Improvement

```bash
# Focus on specific component
python .claude/compliance-task-executor.py --component "Rules Coverage" --target 80.0
```

## Agent Instructions

### When Asked to "Improve Larsson Compliance"

1. **Run the compliance task executor:**
   ```bash
   python .claude/compliance-task-executor.py
   ```

2. **Follow the guided workflow:**
   - Review the baseline metrics
   - Examine the selected task and rationale
   - Confirm the selection (or request alternatives)
   - Let the executor guide task execution
   - Review the compliance delta

3. **Interpret the results:**
   - Positive delta: Task successfully improved compliance
   - No change: Task may have been prerequisite work
   - Negative delta: Investigate regression (rare, but possible)

4. **Iterate if needed:**
   - If target not reached, select next high-impact task
   - Use the recommendations section to guide next steps

### When Asked to "Work on High-Priority Tasks"

1. **Show task rankings:**
   ```bash
   python .claude/compliance-task-executor.py --show-top 10 --dry-run
   ```

2. **Explain the heuristic scores:**
   - Break down why each task scored as it did
   - Highlight expected compliance impact
   - Consider user preferences and constraints

3. **Execute if approved:**
   ```bash
   python .claude/compliance-task-executor.py --task ibdm-xxx.y
   ```

### When Asked About Compliance Strategy

1. **Take baseline snapshot:**
   ```bash
   python .claude/larsson-metrics-helper.py snapshot --output /tmp/baseline.json --verbose
   ```

2. **Analyze which components need work:**
   - Components < 80%: High priority
   - Components 80-89%: Medium priority
   - Components ≥90%: Maintenance only

3. **Filter tasks by component:**
   ```bash
   python .claude/compliance-task-executor.py --component "Rules Coverage" --show-top 5
   ```

4. **Propose a prioritized roadmap:**
   - Phase 1: Address failing components (< 80%)
   - Phase 2: Bring all to good standing (≥ 80%)
   - Phase 3: Achieve excellence (≥ 90%)

## Task Selection Examples

### High-Impact Tasks (Score ≥ 0.80)

1. **ibdm-bsr.1**: Extract InformationState from engine to Burr
   - Score: 0.85
   - Labels: burr, state-extraction, architectural
   - Expected impact: +5% Architectural Compliance

2. **ibdm-bsr.3**: Convert interpret() to pure function
   - Score: 0.83
   - Labels: burr, stateless, architectural
   - Expected impact: +3-5% Architectural Compliance

3. **Add IBiS1 IntegrateAsk rule**
   - Score: 0.80
   - Labels: rules, ibis1, update-rules
   - Expected impact: +8-10% Rules Coverage

### Medium-Impact Tasks (Score 0.60-0.79)

1. **Domain model refactoring**
   - Score: 0.72
   - Labels: domain, semantic
   - Expected impact: +5-8% Domain Independence

2. **QUD stack implementation improvements**
   - Score: 0.68
   - Labels: qud, information-state
   - Expected impact: +3-5% Information State

### Lower-Impact Tasks (Score < 0.60)

- Documentation improvements
- Minor bug fixes
- Testing infrastructure
- Performance optimizations

These are still valuable but less directly tied to Larsson compliance metrics.

## Best Practices

### For AI Agents

1. **Always run with baseline snapshot** - You need the before state to measure impact
2. **Explain the heuristic reasoning** - Help users understand why a task was selected
3. **Validate the selection** - Check that prerequisites are met before executing
4. **Monitor during execution** - Track progress and catch issues early
5. **Report meaningful deltas** - Focus on compliance changes, not just completion

### For Continuous Improvement

1. **Track cumulative improvements** - Use session tracking to see overall progress
2. **Calibrate heuristics** - Adjust weights if predictions don't match actual results
3. **Document surprising outcomes** - Learn from tasks that had unexpected impact
4. **Balance quick wins with foundational work** - Don't ignore low-scoring but important tasks

## Heuristic Calibration

The task selection heuristics should be calibrated based on historical data:

```python
# After each task execution, record:
task_executions = [
    {
        'task_id': 'ibdm-bsr.1',
        'predicted_score': 0.85,
        'predicted_delta': 5.0,
        'actual_delta': 4.8,
        'accuracy': 0.96
    },
    # ... more executions
]

# Periodically review and adjust weights
```

If predictions consistently overestimate or underestimate, adjust the heuristic weights accordingly.

## Troubleshooting

### No Tasks Score Above Threshold

```bash
# Lower the threshold
python .claude/compliance-task-executor.py --min-score 0.4

# Or show all tasks with scores
python .claude/compliance-task-executor.py --show-top 20 --dry-run
```

### Selected Task Has Hidden Blockers

- The heuristic can't detect all blockers (e.g., missing knowledge, unclear requirements)
- If a task can't be started, skip it and try the next one
- Update the task in beads to mark blockers for future runs

### Compliance Didn't Improve

- Some tasks are prerequisite work that enables future improvements
- Check if the task was correctly implemented (tests passing?)
- Review the compliance report's "Issues" section for clues
- Consider if the task was mislabeled

### Compliance Decreased

- This is rare but can happen during refactoring
- Review the delta report to see which component regressed
- Decide whether to fix immediately or accept temporary regression
- Consider using `--fail-on-regression` to prevent this

## Related Documentation

- `larsson-compliance-metrics.md` - Core metrics skill
- `.claude/larsson-metrics-helper.py` - Metrics measurement tool
- `.claude/beads-helpers.sh` - Beads task management
- `docs/LARSSON_ALGORITHMS.md` - Compliance standards
- `LARSSON_PRIORITY_ROADMAP.md` - Strategic compliance plan

## File Structure

```
.claude/
├── skills/
│   ├── larsson-compliance-metrics.md        # Base metrics skill
│   └── larsson-compliance-task-executor.md  # This skill
├── larsson-metrics-helper.py                # Metrics tool
├── compliance-task-executor.py              # Task executor (NEW)
└── beads-helpers.sh                         # Beads utilities

.beads/
├── issues.jsonl                             # Task database
└── config.yaml                              # Beads config
```

This skill enables data-driven, metrics-focused development where each task's impact on Larsson compliance is measured and reported, ensuring continuous progress toward the ≥90% compliance target.
