# Larsson Compliance Metrics Skill

This skill enables AI agents to measure Larsson framework compliance before and after task execution, providing delta reporting to track improvements or regressions.

## About Larsson Compliance Metrics

The IBDM project implements Larsson's (2002) Issue-Based Dialogue Management framework. This skill uses the comprehensive metrics system in `src/ibdm/metrics/larsson_fidelity.py` to:
- Measure implementation fidelity across 5 dimensions
- Track compliance improvements during development
- Identify regressions before they reach production
- Guide development toward ≥90% overall compliance target

## Five Core Metric Dimensions

1. **Architectural Compliance (25%)** - Target: 100/100
   - Four-phase architecture (INTERPRET → INTEGRATE → SELECT → GENERATE)
   - Algorithm 2.2 control flow
   - Single rule application per cycle
   - Explicit state passing

2. **Information State (25%)** - Target: 100/100
   - Private/shared separation
   - Required fields (plan, agenda, beliefs, qud, commitments)
   - QUD as LIFO stack
   - No hidden state

3. **Semantic Operations (20%)** - Target: ≥80/100
   - Core operations: resolves(), combines(), relevant(), depends()
   - Optional IBiS4: postcond(), dominates()

4. **Rules Coverage (20%)** - Target: ≥80/100
   - IBiS1 update rules (IntegrateAsk, IntegrateAnswer, etc.)
   - IBiS1 selection rules (SelectFromPlan, SelectAsk, etc.)
   - Optional IBiS3/4 rules

5. **Domain Independence (10%)** - Target: ≥85/100
   - No hardcoded domain predicates in rules
   - Domain model with registered plan builders
   - Rules use domain resources

**Overall Target**: ≥90% (matches py-trindikit baseline of ~95%)

## Core Commands

### Metrics Snapshot

```bash
# Take a compliance snapshot
python .claude/larsson-metrics-helper.py snapshot --output /tmp/before.json

# Output format (JSON):
# {
#   "timestamp": "2025-11-14T10:30:00",
#   "overall_score": 87.5,
#   "passed": false,
#   "components": {
#     "architectural_compliance": {"score": 95.0, "passed": true, ...},
#     "information_state": {"score": 100.0, "passed": true, ...},
#     ...
#   }
# }
```

### Metrics Comparison

```bash
# Compare two snapshots
python .claude/larsson-metrics-helper.py compare \
  --before /tmp/before.json \
  --after /tmp/after.json

# Output (human-readable):
# Larsson Compliance Delta Report
# ================================
# Overall: 87.5 → 92.3 (+4.8) ✓ NOW PASSING
#
# Component Changes:
#   Architectural Compliance: 95.0 → 100.0 (+5.0) ✓
#   Information State: 100.0 → 100.0 (no change) ✓
#   Semantic Operations: 75.0 → 85.0 (+10.0) ✓
#   Rules Coverage: 70.0 → 80.0 (+10.0) ✓
#   Domain Independence: 85.0 → 90.0 (+5.0) ✓
#
# Issues Resolved: 3
# New Issues: 0
# Recommendations: 2 remaining
```

### Wrapped Task Execution

```bash
# Execute task with before/after metrics
python .claude/larsson-metrics-helper.py wrap-task \
  --command "pytest tests/unit/test_questions.py" \
  --description "Run question class tests"

# Automatically:
# 1. Takes before snapshot
# 2. Executes command
# 3. Takes after snapshot
# 4. Reports delta
```

## Workflow for Measuring Compliance

### Method 1: Manual Before/After

```bash
# 1. Take baseline snapshot
python .claude/larsson-metrics-helper.py snapshot --output /tmp/before.json

# 2. Do your work (implement features, fix bugs, etc.)
# ... code changes ...

# 3. Take after snapshot
python .claude/larsson-metrics-helper.py snapshot --output /tmp/after.json

# 4. Compare
python .claude/larsson-metrics-helper.py compare \
  --before /tmp/before.json \
  --after /tmp/after.json \
  --format detailed
```

### Method 2: Wrapped Task Execution

```bash
# Run any command with automatic metrics tracking
python .claude/larsson-metrics-helper.py wrap-task \
  --command "make install && pytest" \
  --description "Full test suite after dependency update"

# The wrapper will:
# - Snapshot before
# - Execute your command
# - Snapshot after
# - Report delta
# - Exit with command's exit code
```

### Method 3: Session Tracking

```bash
# Start session (takes initial snapshot)
python .claude/larsson-metrics-helper.py start-session --session-id "feature-123"

# ... do multiple tasks during session ...

# Check progress at any time
python .claude/larsson-metrics-helper.py check-session --session-id "feature-123"

# End session (final snapshot and full report)
python .claude/larsson-metrics-helper.py end-session --session-id "feature-123"
```

## Helper Script Details

The `.claude/larsson-metrics-helper.py` script provides:

### Commands

- `snapshot` - Capture current Larsson compliance state
- `compare` - Compare two snapshots and report delta
- `wrap-task` - Execute command with before/after metrics
- `start-session` - Begin tracked development session
- `check-session` - Check progress during session
- `end-session` - End session with full report
- `visualize` - Generate visual dashboard (requires matplotlib)

### Options

```bash
# Snapshot
--output PATH         # Where to save snapshot JSON
--components LIST     # Which components to measure (default: all)
--verbose            # Include full details and recommendations

# Compare
--before PATH        # Path to before snapshot
--after PATH         # Path to after snapshot
--format FORMAT      # Output format: summary|detailed|json
--threshold FLOAT    # Highlight changes >= threshold (default: 1.0)

# Wrap-task
--command CMD        # Command to execute (required)
--description TEXT   # Human-readable task description
--fail-on-regression # Exit with error if compliance decreases
--auto-commit        # Create git commit if compliance improves

# Session
--session-id ID      # Unique session identifier
--session-dir DIR    # Where to store session snapshots (default: /tmp/ibdm-sessions)
```

## Integration with Development Workflow

### Pre-commit Hook Integration

```bash
# In .git/hooks/pre-commit or .claude/hooks/pre-commit
python .claude/larsson-metrics-helper.py snapshot --output /tmp/pre-commit.json

# Compare with previous baseline
if [ -f .claude/baseline-metrics.json ]; then
  python .claude/larsson-metrics-helper.py compare \
    --before .claude/baseline-metrics.json \
    --after /tmp/pre-commit.json \
    --fail-on-regression
fi
```

### CI/CD Pipeline

```yaml
# In .github/workflows/ci.yml or similar
- name: Measure Larsson Compliance
  run: |
    python .claude/larsson-metrics-helper.py snapshot \
      --output compliance-report.json

    # Compare with main branch baseline
    python .claude/larsson-metrics-helper.py compare \
      --before baseline-metrics.json \
      --after compliance-report.json \
      --format detailed \
      --fail-on-regression

- name: Upload Metrics
  uses: actions/upload-artifact@v3
  with:
    name: compliance-metrics
    path: compliance-report.json
```

### Daily Development Sessions

```bash
# Morning: Start tracking
python .claude/larsson-metrics-helper.py start-session --session-id "$(date +%Y-%m-%d)"

# Throughout the day: Regular work with tests
ruff format src/ tests/ && ruff check --fix src/ tests/ && pyright src/ && pytest

# Afternoon: Check progress
python .claude/larsson-metrics-helper.py check-session --session-id "$(date +%Y-%m-%d)"

# End of day: Final report
python .claude/larsson-metrics-helper.py end-session --session-id "$(date +%Y-%m-%d)"
```

### Feature Branch Tracking

```bash
# At branch start
git checkout -b feature/new-rules
python .claude/larsson-metrics-helper.py snapshot \
  --output .claude/metrics-feature-start.json

# Before merging
python .claude/larsson-metrics-helper.py compare \
  --before .claude/metrics-feature-start.json \
  --after <(python .claude/larsson-metrics-helper.py snapshot --output -) \
  --format detailed

# Should show compliance improvement or no regression
```

## Agent Instructions

### When Asked to Measure Compliance Impact

1. **Take baseline snapshot** before starting work
   ```bash
   python .claude/larsson-metrics-helper.py snapshot --output /tmp/baseline.json
   ```

2. **Perform the requested task** (implement feature, fix bug, refactor, etc.)

3. **Take follow-up snapshot** after completing work
   ```bash
   python .claude/larsson-metrics-helper.py snapshot --output /tmp/after.json
   ```

4. **Report delta** with interpretation
   ```bash
   python .claude/larsson-metrics-helper.py compare \
     --before /tmp/baseline.json \
     --after /tmp/after.json \
     --format detailed
   ```

5. **Interpret results** for the user:
   - Highlight improvements (positive deltas)
   - Flag regressions (negative deltas)
   - Explain which component(s) changed and why
   - Recommend next steps if compliance decreased

### When Asked to Track Development Session

Use the session tracking commands:

```bash
# At session start
python .claude/larsson-metrics-helper.py start-session --session-id "$SESSION_ID"

# Periodic checks (after significant changes)
python .claude/larsson-metrics-helper.py check-session --session-id "$SESSION_ID"

# At session end
python .claude/larsson-metrics-helper.py end-session --session-id "$SESSION_ID"
```

### When Asked to Ensure No Regression

Use the `wrap-task` command with `--fail-on-regression`:

```bash
python .claude/larsson-metrics-helper.py wrap-task \
  --command "make test" \
  --description "Run full test suite" \
  --fail-on-regression

# This will exit with code 1 if compliance decreases
```

## Example Usage Scenarios

### Scenario 1: Implementing New Rule

```bash
# Agent receives: "Implement IntegrateAnswer rule"

# 1. Take baseline
python .claude/larsson-metrics-helper.py snapshot --output /tmp/before-rule.json

# 2. Implement rule
# ... create src/ibdm/rules/integrate_answer.py ...
# ... add tests ...
# ... run tests ...

# 3. Compare
python .claude/larsson-metrics-helper.py compare \
  --before /tmp/before-rule.json \
  --after <(python .claude/larsson-metrics-helper.py snapshot --output -) \
  --format detailed

# Expected: Rules Coverage should increase (e.g., 70 → 80)
```

### Scenario 2: Refactoring for Larsson Compliance

```bash
# Agent receives: "Refactor engine to match Algorithm 2.2"

# Use wrap-task for automatic tracking
python .claude/larsson-metrics-helper.py wrap-task \
  --command "pytest tests/unit/test_engine.py" \
  --description "Engine refactoring for Algorithm 2.2 compliance" \
  --fail-on-regression \
  --auto-commit

# Expected: Architectural Compliance should increase (e.g., 85 → 100)
```

### Scenario 3: Sprint/Phase Tracking

```bash
# At phase start (e.g., "Phase 2: Rules Implementation")
python .claude/larsson-metrics-helper.py start-session --session-id "phase-2"

# During phase (after each task)
bd ready --json  # Get next task
# ... do work ...
python .claude/larsson-metrics-helper.py check-session --session-id "phase-2"

# At phase end
python .claude/larsson-metrics-helper.py end-session --session-id "phase-2"

# Shows overall compliance improvement during entire phase
```

## Output Format Details

### Snapshot JSON Structure

```json
{
  "timestamp": "2025-11-14T10:30:00.000Z",
  "overall_score": 87.5,
  "passed": false,
  "components": {
    "architectural_compliance": {
      "name": "Architectural Compliance",
      "score": 95.0,
      "passed": true,
      "details": {
        "four_phase_architecture": true,
        "algorithm_2_2_control_flow": true,
        "single_rule_application": true,
        "explicit_state_passing": false
      },
      "issues": ["Hidden state detected in engine"],
      "recommendations": ["Use Burr state exclusively"]
    },
    "information_state": { ... },
    "semantic_operations": { ... },
    "rules_coverage": { ... },
    "domain_independence": { ... }
  }
}
```

### Comparison Report Formats

#### Summary Format
```
Larsson Compliance: 87.5 → 92.3 (+4.8) ✓ NOW PASSING
```

#### Detailed Format
```
Larsson Compliance Delta Report
================================
Overall: 87.5 → 92.3 (+4.8) ✓ NOW PASSING

Component Changes:
  [+] Architectural Compliance: 95.0 → 100.0 (+5.0)
  [=] Information State: 100.0 → 100.0 (no change)
  [+] Semantic Operations: 75.0 → 85.0 (+10.0)
  [+] Rules Coverage: 70.0 → 80.0 (+10.0)
  [+] Domain Independence: 85.0 → 90.0 (+5.0)

Issues:
  Resolved (3):
    ✓ Hidden state detected in engine
    ✓ Missing resolves() operation
    ✓ Hardcoded domain predicates in SelectRule

  New (0):
    (none)

Recommendations (2 remaining):
  • Implement dominates() operation for IBiS4
  • Add accommodation rules for IBiS3
```

#### JSON Format
```json
{
  "before": {...},
  "after": {...},
  "delta": {
    "overall_score": 4.8,
    "components": {
      "architectural_compliance": 5.0,
      ...
    },
    "issues_resolved": 3,
    "issues_new": 0
  }
}
```

## Best Practices

### For AI Agents

1. **Always measure before major changes** - Baseline is critical for delta reporting
2. **Run compliance check after rule implementation** - Ensures Rules Coverage increases
3. **Use session tracking for multi-task work** - Provides cumulative view
4. **Fail on regression in CI** - Prevents backsliding
5. **Report deltas in commit messages** - E.g., "feat(rules): add IntegrateAsk rule (+8% compliance)"

### For Development Workflow

1. **Set compliance targets per phase**
   - Phase 1: ≥75% (foundation)
   - Phase 2: ≥85% (core rules)
   - Phase 3: ≥90% (complete)

2. **Track compliance in beads tasks**
   ```bash
   bd create "Achieve 90% Larsson compliance" \
     -t feature \
     -p 0 \
     -l "compliance,phase-3" \
     --parent bd-phase3
   ```

3. **Generate visualizations for reviews**
   ```bash
   python .claude/larsson-metrics-helper.py visualize \
     --input compliance-report.json \
     --output compliance-dashboard.png
   ```

4. **Maintain baseline files**
   - `.claude/baseline-metrics.json` - Current main branch
   - `.claude/metrics-*.json` - Feature branch baselines

## Troubleshooting

### Snapshot Fails

```bash
# Check that components are available
python -c "from ibdm.metrics import evaluate_larsson_fidelity; print('OK')"

# Check environment
python -c "import os; assert os.getenv('IBDM_API_KEY'), 'Missing API key'"

# Run with verbose output
python .claude/larsson-metrics-helper.py snapshot --output /tmp/test.json --verbose
```

### Metrics Don't Change

- Ensure you're measuring the right codebase (not stale install)
- Verify changes affect measured components
- Check that tests pass (metrics measure implementation, not just code existence)

### Session Already Exists

```bash
# List active sessions
ls /tmp/ibdm-sessions/

# Remove stale session
rm -rf /tmp/ibdm-sessions/old-session-id

# Or use different session ID
```

## Related Documentation

- `docs/LARSSON_ALGORITHMS.md` - Authoritative algorithmic reference
- `src/ibdm/metrics/larsson_fidelity.py` - Metrics implementation
- `src/ibdm/metrics/visualization.py` - Visual reporting
- `tests/unit/test_larsson_metrics.py` - Metrics test suite
- `LARSSON_PRIORITY_ROADMAP.md` - Compliance-driven development plan

## Integration with Beads

Track compliance improvement as tasks:

```bash
# Create compliance milestone
bd create "Achieve 90% overall Larsson compliance" \
  -t epic \
  -p 0 \
  -l "compliance,milestone"

# Component-specific tasks
bd create "Reach 100% Architectural Compliance" \
  -t task \
  -p 1 \
  --parent bd-compliance-epic

bd create "Implement all IBiS1 rules (80% Rules Coverage)" \
  -t task \
  -p 1 \
  --parent bd-compliance-epic
```

This skill enables AI agents to measure, track, and improve Larsson framework compliance systematically throughout the development lifecycle.
