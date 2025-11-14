# Larsson Delta Advisor Skill

This skill runs Larsson compliance metrics before and after task execution, calculates deltas, and provides actionable recommendations on next steps.

## Purpose

Automatically evaluate task impact on Larsson framework compliance and recommend whether to:
- **Declare task closed and successful** - Task improved or maintained compliance
- **Declare task closed and unsuccessful** - Task failed to achieve goals despite effort
- **Modify task and rerun** - Small adjustments could improve outcome
- **Break task down into smaller stages and rerun** - Task is too complex for single iteration

## Workflow

### 1. Take Baseline Snapshot

Before starting any task, capture current compliance state:

```bash
python .claude/larsson-metrics-helper.py snapshot --output /tmp/baseline.json --verbose
```

Store the baseline for comparison.

### 2. Execute the Task

Perform the requested work (implementation, refactoring, bug fix, etc.).

### 3. Take Post-Task Snapshot

After completing the task, capture new compliance state:

```bash
python .claude/larsson-metrics-helper.py snapshot --output /tmp/after.json --verbose
```

### 4. Compare and Analyze Delta

Compare the snapshots to calculate delta:

```bash
python .claude/larsson-metrics-helper.py compare \
  --before /tmp/baseline.json \
  --after /tmp/after.json \
  --format detailed
```

### 5. Make Recommendation

Based on the delta analysis, determine next steps using the decision matrix below.

## Decision Matrix

### Recommendation 1: Declare Task Closed and Successful

**Criteria:**
- Overall score **improved** by ≥2.0 points, OR
- Overall score **maintained** (within ±1.0 points) AND was already ≥90%, OR
- **All** relevant component scores improved or maintained, AND
- **No new critical issues** introduced, AND
- **Tests pass** without regression

**Reasoning to provide:**
```
✓ Task successfully completed

Compliance Impact:
  Overall: {before} → {after} ({delta:+.1f})
  {component_improvements}

The task {improved_or_maintained} Larsson compliance without introducing
regressions. All tests pass and code quality standards are met.

Recommendation: Close task as successful.
```

**Example:**
- Overall: 87.5 → 92.3 (+4.8) ✓
- Architectural: 95.0 → 100.0 (+5.0) ✓
- Rules Coverage: 70.0 → 80.0 (+10.0) ✓
- No new issues

### Recommendation 2: Declare Task Closed and Unsuccessful

**Criteria:**
- Overall score **decreased** by ≥5.0 points, OR
- **Critical component** (Architectural or Information State) score decreased by ≥10 points, OR
- **Multiple attempts** (≥3) with no improvement, OR
- New critical issues introduced **without** offsetting improvements, OR
- Task **fundamentally incompatible** with Larsson framework

**Reasoning to provide:**
```
✗ Task unsuccessful - closing without merge

Compliance Impact:
  Overall: {before} → {after} ({delta:+.1f})
  {component_regressions}

Issues Introduced:
  {new_critical_issues}

The task caused significant compliance regression or introduced critical
issues that cannot be resolved within current scope. The approach is
incompatible with Larsson framework principles.

Recommendation: Close task as unsuccessful. Consider alternative approach.
```

**Example:**
- Overall: 87.5 → 78.3 (-9.2) ✗
- Architectural: 95.0 → 70.0 (-25.0) ✗
- New issues: "Hidden state in engine", "QUD used as set not stack"

### Recommendation 3: Modify Task and Rerun

**Criteria:**
- Overall score **changed** by -2.0 to +2.0 (minor impact), OR
- **One specific component** regressed while others improved, OR
- Tests fail but **fixes are straightforward** (<30 minutes estimated), OR
- **Clear path** to improvement with minor adjustments, OR
- **Partial progress** made (≥1 component improved significantly)

**Reasoning to provide:**
```
⚠ Task needs modification before completion

Compliance Impact:
  Overall: {before} → {after} ({delta:+.1f})

Issues to Address:
  {specific_fixable_issues}

Progress Made:
  {components_that_improved}

The task is on the right track but needs targeted adjustments.
Specific issues can be resolved with focused effort.

Recommended Modifications:
  1. {specific_fix_1}
  2. {specific_fix_2}

Estimated Time: {time_estimate}
Recommendation: Apply modifications and rerun metrics.
```

**Example:**
- Overall: 87.5 → 88.0 (+0.5)
- Semantic Operations: 75.0 → 85.0 (+10.0) ✓
- Domain Independence: 85.0 → 80.0 (-5.0) ✗
- Issue: "Hardcoded predicate in new rule"
- Fix: "Move predicate to domain model (15 min)"

### Recommendation 4: Break Task Down into Smaller Stages and Rerun

**Criteria:**
- Task is **too complex** (affects ≥3 components significantly), OR
- **Mixed results** (≥2 components improved, ≥2 components regressed), OR
- **Scope creep** detected (unintended changes in multiple areas), OR
- **Dependencies unclear** (changes cascade unpredictably), OR
- Multiple issues that **require different expertise/approaches**

**Reasoning to provide:**
```
⚡ Task too complex - break into stages

Compliance Impact:
  Overall: {before} → {after} ({delta:+.1f})

Complexity Indicators:
  - {complexity_indicator_1}
  - {complexity_indicator_2}

The task scope is too broad for a single iteration. Multiple components
are affected, creating conflicting requirements and unpredictable
interactions.

Recommended Stages:
  Stage 1: {subtask_1}
    Focus: {component_1}
    Target: {target_score_1}

  Stage 2: {subtask_2}
    Focus: {component_2}
    Target: {target_score_2}

  Stage 3: {subtask_3}
    Focus: {component_3}
    Target: {target_score_3}

Recommendation: Break down into stages and tackle incrementally.
Run metrics after each stage.
```

**Example:**
- Overall: 87.5 → 86.0 (-1.5)
- Architectural: 95.0 → 100.0 (+5.0) ✓
- Rules Coverage: 70.0 → 65.0 (-5.0) ✗
- Semantic Operations: 75.0 → 70.0 (-5.0) ✗
- Domain Independence: 85.0 → 90.0 (+5.0) ✓
- Complexity: Refactoring affected 4+ modules, cascading changes

## Special Cases

### Case: No Measurable Change

**Criteria:**
- Overall score changed by <0.5 points
- No component scores changed by >1.0 points
- No new issues, no resolved issues

**Recommendation:**
- If task was **supposed** to improve metrics → Modify task or break down
- If task was **unrelated** to metrics (e.g., docs, tests) → Close successful if tests pass

### Case: High Score Already Achieved

**Criteria:**
- Baseline overall score ≥95%
- All critical components (Architectural, Information State) at 100%

**Recommendation:**
- **Maintain** high compliance
- Any decrease >0.5 points → Modify task and fix
- Otherwise → Close successful

### Case: Tests Fail

**Criteria:**
- pytest exits with errors
- Any test failures unrelated to the task

**Recommendation:**
- **Always** fix failing tests before closing task
- If tests fail after task → Modify task and fix
- Never close task successful with failing tests

## Implementation Guide for AI Agents

When asked to use this skill, follow this exact sequence:

### Step 1: Initialize

```bash
# Create temporary directory for snapshots
mkdir -p /tmp/larsson-snapshots
SESSION_ID="$(date +%s)"
BASELINE="/tmp/larsson-snapshots/baseline-${SESSION_ID}.json"
AFTER="/tmp/larsson-snapshots/after-${SESSION_ID}.json"
```

### Step 2: Take Baseline

```bash
echo "📊 Taking baseline Larsson compliance snapshot..."
python .claude/larsson-metrics-helper.py snapshot \
  --output "$BASELINE" \
  --verbose
```

Parse and store baseline score:
```bash
BASELINE_SCORE=$(jq -r '.overall_score' "$BASELINE")
echo "Baseline Overall Score: ${BASELINE_SCORE}%"
```

### Step 3: Execute Task

Perform the requested task with normal workflow:
- Write code
- Run tests
- Format and lint
- Fix any immediate issues

### Step 4: Take After Snapshot

```bash
echo "📊 Taking post-task Larsson compliance snapshot..."
python .claude/larsson-metrics-helper.py snapshot \
  --output "$AFTER" \
  --verbose
```

### Step 5: Generate Delta Report

```bash
echo "📈 Calculating compliance delta..."
python .claude/larsson-metrics-helper.py compare \
  --before "$BASELINE" \
  --after "$AFTER" \
  --format detailed > /tmp/delta-report.txt

cat /tmp/delta-report.txt
```

### Step 6: Analyze and Recommend

Parse the delta report and apply decision matrix:

```python
# Pseudo-code for analysis
baseline = json.load(open(BASELINE))
after = json.load(open(AFTER))

overall_delta = after['overall_score'] - baseline['overall_score']
component_deltas = calculate_component_deltas(baseline, after)
new_issues = count_new_issues(baseline, after)
resolved_issues = count_resolved_issues(baseline, after)

# Apply decision matrix
if meets_success_criteria(overall_delta, component_deltas, new_issues):
    recommendation = "CLOSE_SUCCESSFUL"
elif meets_failure_criteria(overall_delta, component_deltas, new_issues, attempt_count):
    recommendation = "CLOSE_UNSUCCESSFUL"
elif meets_modification_criteria(overall_delta, component_deltas):
    recommendation = "MODIFY_AND_RERUN"
elif meets_breakdown_criteria(component_deltas, complexity_indicators):
    recommendation = "BREAK_DOWN_AND_RERUN"
```

### Step 7: Report to User

Provide detailed recommendation with:

1. **Summary**: One-line verdict
2. **Compliance Impact**: Scores before/after with deltas
3. **Analysis**: What changed and why
4. **Recommendation**: Specific next steps
5. **Reasoning**: Explanation for recommendation

## Example Session

```bash
$ # Agent receives task: "Implement IntegrateAsk rule"

$ # Step 1-2: Baseline
$ python .claude/larsson-metrics-helper.py snapshot --output /tmp/baseline.json
$ jq '.overall_score' /tmp/baseline.json
87.5

$ # Step 3: Execute task
$ # ... implement rule, write tests, run tests ...
$ pytest tests/unit/test_integrate_ask.py -v
PASSED

$ # Step 4-5: After snapshot and delta
$ python .claude/larsson-metrics-helper.py snapshot --output /tmp/after.json
$ python .claude/larsson-metrics-helper.py compare \
    --before /tmp/baseline.json \
    --after /tmp/after.json \
    --format detailed

Larsson Compliance Delta Report
================================
Overall: 87.5 → 92.0 (+4.5) ✓ NOW PASSING

Component Changes:
  [+] Rules Coverage: 70.0 → 80.0 (+10.0) ✓
  [=] Architectural: 95.0 → 95.0 (no change)
  [=] Information State: 100.0 → 100.0 (no change)
  [+] Semantic Operations: 75.0 → 77.0 (+2.0)
  [=] Domain Independence: 85.0 → 85.0 (no change)

Issues Resolved: 1
  ✓ Missing IntegrateAsk rule

New Issues: 0

$ # Step 6-7: Recommendation
$ # Analysis: +4.5 overall, +10.0 in Rules Coverage, no regressions, tests pass

✓ Task successfully completed

Compliance Impact:
  Overall: 87.5 → 92.0 (+4.5) ✓ NOW PASSING TARGET
  Rules Coverage: 70.0 → 80.0 (+10.0) ✓ SIGNIFICANT IMPROVEMENT

The task successfully implemented the IntegrateAsk rule, increasing
Rules Coverage by 10 points and pushing overall compliance above the
90% target. All tests pass and no regressions were introduced.

Recommendation: Close task as successful.
```

## Integration with Beads

Track task outcomes in beads:

```bash
# If CLOSE_SUCCESSFUL
bd done <task-id> "Completed successfully (+4.5% Larsson compliance)"

# If CLOSE_UNSUCCESSFUL
bd done <task-id> "Closed unsuccessful (incompatible with Larsson framework)"

# If MODIFY_AND_RERUN
bd update <task-id> --description "Fix hardcoded predicate issue"
# Continue working...

# If BREAK_DOWN
bd create "Stage 1: Refactor engine architecture" --parent <task-id>
bd create "Stage 2: Implement remaining rules" --parent <task-id>
bd create "Stage 3: Add domain independence" --parent <task-id>
```

## Best Practices

### For AI Agents

1. **Always take baseline** before starting work - No baseline = No recommendation
2. **Include verbose output** in snapshots for detailed analysis
3. **Run full test suite** before taking after snapshot
4. **Be honest in assessment** - Don't declare success if scores decreased
5. **Provide specific recommendations** - "Fix X in file Y" not "improve code"
6. **Show your reasoning** - Explain why you chose this recommendation
7. **Track attempts** - After 3 modify-rerun cycles, consider breaking down

### For Development Workflow

1. **Set clear targets** per task (e.g., "Increase Rules Coverage to 80%")
2. **One component focus** per task when possible
3. **Measure frequently** during complex refactoring
4. **Accept partial progress** - Sometimes +2 points is good enough
5. **Learn from unsuccessful tasks** - Document why approach failed

## Thresholds Summary

| Metric | Successful | Modify | Breakdown | Unsuccessful |
|--------|-----------|--------|-----------|--------------|
| Overall Delta | ≥+2.0 | -2.0 to +2.0 | Mixed | ≤-5.0 |
| Component Delta | All ≥0 | 1 regressed | ≥2 regressed | Critical ≤-10 |
| New Issues | 0 | 1-2 fixable | Multiple | Critical |
| Tests | All pass | 1-2 failures | Many failures | Cascading failures |
| Attempts | 1-2 | 1-3 | N/A | ≥3 |
| Complexity | Low | Medium | High | Incompatible |

## Troubleshooting

### Delta Report Shows "No Change" But Code Changed

- Verify changes affect **measured** components
- Check that changes are **architecturally significant**
- Ensure tests actually **exercise** new code
- Consider if changes are **implementation details** vs. architectural

### Recommendation Seems Wrong

- Review **full delta report**, not just overall score
- Check for **hidden regressions** in component details
- Verify **test results** match expectations
- Consider **context**: Is this exploratory work or production-ready?

### Multiple Conflicting Signals

- Prioritize **critical components** (Architectural, Information State)
- Weight **overall score** more heavily than individual components
- Consider **trend**: Is this getting better or worse over attempts?
- When in doubt, **break down** rather than push forward

## Related Skills

- `larsson-compliance-metrics` - Reference guide for metrics system
- `beads-planning` - Task planning and management

## Quick Reference

```bash
# Full workflow in one command
python .claude/larsson-metrics-helper.py wrap-task \
  --command "pytest tests/unit/test_my_feature.py" \
  --description "Implement my feature" \
  --fail-on-regression

# This automatically:
# 1. Takes baseline
# 2. Runs command
# 3. Takes after snapshot
# 4. Reports delta
# 5. Exits with error if compliance decreased
```

Use this skill to make data-driven decisions about task completion and ensure consistent progress toward ≥90% Larsson compliance target.
