# Scenario Alignment Guide

**Status**: ✅ CURRENT (2025-11-21)
**Audience**: AI Code Assistants

This document explains how to work with scenarios in IBDM. Scenarios are demonstration scripts that show dialogue system behavior. The state changes documented in scenarios reflect what the implementation actually does, not what we initially guessed it would do.

---

## Philosophy: Scenarios Follow Implementation

**KEY PRINCIPLE**: Scenarios document actual behavior, not prescriptive specifications.

### What This Means

1. **Scenarios were created based on guesses** about probable state changes
2. **We are now aligning scenarios** with actual implementation behavior
3. **We want scenarios that work** and demonstrate what they're supposed to demonstrate
4. **We are NOT committed** to the specific state changes initially written in scenarios

### The Relationship

```
Implementation (source of truth)
        ↓
Actual Runtime Behavior
        ↓
Scenarios (documentation of behavior)
```

NOT:

```
Scenarios (specification)
        ↓
Implementation (tries to match)
```

---

## When Working on Scenarios: Step-by-Step

### Step 1: Identify Your Task

**Are you**:
- A) Fixing a bug in the dialogue engine?
- B) Implementing a new Larsson rule?
- C) Updating scenario documentation to match current behavior?
- D) Creating a new scenario for a new feature?

### Step 2: Execute Based on Task Type

#### Task Type A: Fixing Dialogue Engine Bug

```bash
# 1. Identify the bug in implementation
#    Example: "integrate_answer rule not popping QUD correctly"

# 2. Write/run test that exposes bug
pytest tests/unit/test_update_rules.py::test_integrate_answer -v

# 3. Fix the implementation
#    - Edit src/ibdm/rules/update_rules.py
#    - Make the code work correctly

# 4. Verify fix with tests
pytest tests/unit/test_update_rules.py::test_integrate_answer -v

# 5. THEN update scenarios to match new behavior
#    - Run scenario with current implementation
#    - Document what actually happens in state_changes
#    - Update expected_outcomes if needed

# 6. Commit implementation fix and scenario updates separately
git commit -m "fix(rules): correct QUD pop in integrate_answer"
git commit -m "docs(scenarios): update state_changes for integrate_answer fix"
```

**Rule**: Implementation correctness comes first. Scenarios document the fix.

#### Task Type B: Implementing New Larsson Rule

```bash
# 1. Implement the rule per Larsson (2002)
#    Example: Rule 4.3 (Dependent Question Accommodation)

# 2. Write tests for the rule
pytest tests/unit/test_update_rules.py::test_accommodate_dependent_question -v

# 3. Run implementation, observe behavior
export IBDM_DEBUG=all
python scripts/run_scenario.py ibis3_dependent_questions --step

# 4. Document ACTUAL behavior in scenario
#    Look at debug output:
#    - What gets pushed to QUD?
#    - What gets added to private.issues?
#    - What commitments are made?

# 5. Update scenario JSON with observed state_changes
#    Example:
#    "state_changes": {
#      "qud_pushed": "?x.clarification(x)",
#      "depends_on": "?x.nda_type(x)"
#    }

# 6. Verify scenario matches implementation
python scripts/run_scenario.py ibis3_dependent_questions --replay

# 7. Commit
git commit -m "feat(rules): implement Rule 4.3 dependent questions"
git commit -m "docs(scenarios): document Rule 4.3 behavior"
```

**Rule**: Implement correctly first, then document what you implemented.

#### Task Type C: Updating Scenario to Match Current Behavior

```bash
# 1. Run the scenario with debug logging
export IBDM_DEBUG=all
python scripts/run_scenario.py nda_basic --step > /tmp/scenario_trace.txt

# 2. Compare scenario state_changes with actual debug output
#    Scenario says:
#      "state_changes": {"qud_pushed": "?x.legal_entities(x)"}
#    Debug output shows:
#      [DEBUG] QUD PUSH: WhQuestion(variable='x', predicate='legal_entities')

# 3. Check if they match
#    - If YES: Scenario is aligned, no change needed
#    - If NO: Proceed to step 4

# 4. Determine which is correct
#    A. Is implementation following Larsson (2002)? → Update scenario
#    B. Is implementation buggy? → Fix implementation (see Task Type A)

# 5. If updating scenario (case A):
#    - Edit demos/scenarios/nda_basic.json
#    - Update state_changes to match actual behavior
#    - Update expected_outcomes if needed
#    - Add comment if behavior is surprising

# 6. Validate updated scenario
python scripts/run_scenario.py nda_basic --replay

# 7. Commit
git commit -m "docs(scenarios): align nda_basic with current implementation"
```

**Rule**: Scenarios document reality, not wishes.

#### Task Type D: Creating New Scenario

```bash
# 1. Identify what you want to demonstrate
#    Example: "Clarification questions with grounding"

# 2. Create minimal scenario JSON
#    Start with just turns, no state_changes yet

# 3. Run the scenario with debug logging
export IBDM_DEBUG=all
python scripts/run_scenario.py my_new_scenario --step > /tmp/trace.txt

# 4. Observe what actually happens
#    - Watch QUD stack operations
#    - Watch rule evaluations
#    - Watch state modifications

# 5. Document observed behavior in state_changes
#    Add state_changes to each turn based on debug output

# 6. Add metadata
#    - business_explanation: Why this matters
#    - larsson_rule: Which rule fired
#    - expected_outcomes: What we measure

# 7. Validate
python scripts/run_scenario.py my_new_scenario --replay

# 8. Commit
git commit -m "docs(scenarios): add clarification with grounding scenario"
```

**Rule**: Create scenario by observing actual behavior, not guessing.

---

## Scenario State Changes: What to Document

### Always Document

**QUD Operations**:
```json
"state_changes": {
  "qud_pushed": "?x.predicate(x)",
  "qud_popped": "?x.other_predicate(x)",
  "qud_depth": 2
}
```

**Commitment Changes**:
```json
"state_changes": {
  "commitment_added": "legal_entities(acme, smith)",
  "commitments_total": 3
}
```

**Plan Operations**:
```json
"state_changes": {
  "plan_created": "nda_drafting",
  "issues_added": ["legal_entities", "nda_type", "date"],
  "issues_count": 3
}
```

### Sometimes Document

**Rule Activations** (if noteworthy):
```json
"state_changes": {
  "rules_fired": ["accommodate_issue", "integrate_answer"],
  "rules_blocked": ["form_plan"]
}
```

**Grounding State** (for IBiS2 scenarios):
```json
"state_changes": {
  "grounding_status": "cautious",
  "confidence": 0.7,
  "needs_confirmation": true
}
```

### Never Guess

**DON'T DO THIS**:
```json
// ❌ WRONG - Guessing what should happen
"state_changes": {
  "qud_pushed": "probably a WhQuestion",
  "might_add_commitment": "not sure"
}
```

**DO THIS INSTEAD**:
```json
// ✅ RIGHT - Document actual behavior or omit if unknown
"state_changes": {
  "qud_pushed": "?x.legal_entities(x)"  // Observed in debug log
}
// Or omit state_changes entirely until you can observe
```

---

## Debugging Scenarios

### Step 1: Enable Full Debug Logging

```bash
export IBDM_DEBUG=all
```

### Step 2: Run Scenario in Step Mode

```bash
python scripts/run_scenario.py nda_basic --step
```

### Step 3: Compare Expected vs Actual

For each turn:

1. **Read scenario expectation**:
   ```json
   "state_changes": {
     "qud_pushed": "?x.legal_entities(x)"
   }
   ```

2. **Check debug output**:
   ```
   [DEBUG] ibdm.core.information_state: QUD PUSH: WhQuestion(variable='x', predicate='legal_entities')
   ```

3. **Verify match**:
   - Expected: `?x.legal_entities(x)`
   - Actual: `WhQuestion(variable='x', predicate='legal_entities')`
   - Match: ✓ YES

### Step 4: Fix Mismatches

**If scenario is wrong**:
```bash
# Edit scenario JSON
vim demos/scenarios/nda_basic.json
# Update state_changes to match actual behavior
# Commit
git commit -m "docs(scenarios): fix state_changes in nda_basic"
```

**If implementation is wrong**:
```bash
# Fix implementation
vim src/ibdm/rules/update_rules.py
# Run tests
pytest
# Update scenario to match fixed implementation
vim demos/scenarios/nda_basic.json
# Commit separately
git commit -m "fix(rules): correct QUD operation"
git commit -m "docs(scenarios): update for fixed QUD behavior"
```

---

## Common Patterns

### Pattern 1: State Changes Unknown

**Situation**: Creating scenario, don't know what state changes occur.

**Solution**:
```json
{
  "turn": 1,
  "speaker": "user",
  "utterance": "I need an NDA",
  "move_type": "request",
  "business_explanation": "User initiates task",
  "larsson_rule": "Task Accommodation"
  // NO state_changes field - will add after observing
}
```

**Next steps**:
1. Run with debug logging
2. Observe actual state changes
3. Add state_changes field with observed values
4. Commit update

### Pattern 2: Behavior Changed After Refactoring

**Situation**: Refactored code, scenarios now misaligned.

**Solution**:
```bash
# 1. Run all scenarios, collect traces
for scenario in $(python scripts/run_scenario.py --list | grep '•' | awk '{print $2}'); do
  python scripts/run_scenario.py "$scenario" --replay > "/tmp/${scenario}_trace.txt" 2>&1
done

# 2. Review traces, identify mismatches
grep -r "ERROR\|MISMATCH" /tmp/*_trace.txt

# 3. For each mismatch:
#    A. Is new behavior correct per Larsson? → Update scenario
#    B. Is new behavior broken? → Fix implementation

# 4. Batch update scenarios
git commit -m "docs(scenarios): realign after refactoring"
```

### Pattern 3: New Rule Implementation

**Situation**: Implementing Rule 4.5, need to create scenario.

**Solution**:
```bash
# 1. Implement rule with tests
vim src/ibdm/rules/update_rules.py
pytest tests/unit/test_update_rules.py::test_rule_4_5 -v

# 2. Create scenario skeleton
cat > demos/scenarios/ibis3_rule_4_5.json <<EOF
{
  "scenario_id": "ibis3_rule_4_5",
  "title": "Rule 4.5 - [Description]",
  "turns": [
    {"turn": 1, "speaker": "user", "utterance": "...", "move_type": "request"}
  ]
}
EOF

# 3. Run with debug to observe behavior
export IBDM_DEBUG=all
python scripts/run_scenario.py ibis3_rule_4_5 --step

# 4. Fill in state_changes based on observation
vim demos/scenarios/ibis3_rule_4_5.json

# 5. Commit
git commit -m "feat(rules): implement Rule 4.5"
git commit -m "docs(scenarios): add Rule 4.5 demonstration"
```

---

## Validation Checklist

Before committing scenario updates:

### ✅ Mechanical Validation

```bash
# 1. JSON is valid
python -m json.tool < demos/scenarios/my_scenario.json > /dev/null

# 2. Schema is valid
python -c "from ibdm.demo import ScenarioLoader; print(ScenarioLoader().validate_scenario('my_scenario'))"

# 3. Scenario runs without errors
python scripts/run_scenario.py my_scenario --replay
```

### ✅ Content Validation

- [ ] Every state_changes field is based on observed behavior, not guesses
- [ ] Business explanations describe actual system behavior
- [ ] Larsson rules reference correct thesis sections
- [ ] Expected outcomes are measurable
- [ ] Payoff turns are marked (is_payoff: true)

### ✅ Alignment Validation

```bash
# Run with debug and manually verify
export IBDM_DEBUG=all
python scripts/run_scenario.py my_scenario --step

# Check each turn:
# - Does scenario state_changes match debug output?
# - Does scenario larsson_rule match rules log?
# - Does scenario move_type match move log?
```

---

## Anti-Patterns: What NOT to Do

### ❌ Anti-Pattern 1: Prescriptive Scenarios

**WRONG**:
> "The scenario says QUD should push, so let's change the implementation to push."

**RIGHT**:
> "The implementation correctly implements Larsson Rule 4.1, which doesn't push to QUD in this case. Let's update the scenario to document actual behavior."

### ❌ Anti-Pattern 2: Speculative State Changes

**WRONG**:
```json
"state_changes": {
  "qud_pushed": "probably something about entities",
  "might_create_plan": "if the code does that"
}
```

**RIGHT**:
```json
"state_changes": {
  "qud_pushed": "?x.legal_entities(x)"  // From debug log line 47
}
```

### ❌ Anti-Pattern 3: Ignoring Mismatches

**WRONG**:
> "The scenario says X but implementation does Y. I'll ignore it."

**RIGHT**:
> "Mismatch found. Is Y correct per Larsson? Yes → update scenario. No → fix implementation."

### ❌ Anti-Pattern 4: Batch Updates Without Verification

**WRONG**:
```bash
# Update all scenarios to say "qud_pushed"
sed -i 's/"qud_added"/"qud_pushed"/g' demos/scenarios/*.json
git commit -m "fix scenarios"
```

**RIGHT**:
```bash
# Update each scenario after verifying behavior
for scenario in nda_basic nda_distractor; do
  python scripts/run_scenario.py "$scenario" --replay
  # Manually verify, then edit if needed
  vim "demos/scenarios/${scenario}.json"
  git commit -m "docs(scenarios): verify and update ${scenario}"
done
```

---

## When to Update Scenarios vs Implementation

### Update Scenario When

1. **Implementation is correct per Larsson (2002)**
   - Rule evaluation follows thesis algorithms
   - State changes are theoretically sound
   - Tests pass
   - → Scenario just documents wrong behavior

2. **Implementation was intentionally changed**
   - Refactoring improved code
   - New feature added correctly
   - Optimization didn't change semantics
   - → Scenario needs to reflect new reality

3. **Scenario was based on speculation**
   - State changes were guesses
   - Never verified against actual behavior
   - → Scenario needs to be grounded in observation

### Update Implementation When

1. **Violates Larsson (2002)**
   - Rule doesn't follow thesis algorithm
   - QUD operations wrong (not LIFO)
   - Accommodation order wrong
   - → Fix implementation to match Larsson

2. **Tests fail**
   - Unit tests expose bug
   - Integration tests fail
   - → Fix implementation

3. **Behavior is clearly wrong**
   - System asks same question twice
   - Plan doesn't progress
   - Commitments not stored
   - → Fix implementation bug

### Update Both When

1. **Implementing new feature**
   - Write implementation + tests
   - Create scenario showing feature
   - → Both are new

2. **Fixing bug with scenario impact**
   - Fix implementation bug
   - Update scenario to show correct behavior
   - → Implementation fix, then scenario update

---

## Quick Reference

### I need to...

**...create a new scenario**
```bash
# 1. Write skeleton JSON (no state_changes)
# 2. Run with IBDM_DEBUG=all
# 3. Observe behavior
# 4. Document in state_changes
# 5. Validate and commit
```

**...update an outdated scenario**
```bash
# 1. Run scenario with debug
# 2. Compare expected vs actual
# 3. If implementation correct: update scenario
# 4. If implementation wrong: fix implementation, then update scenario
# 5. Commit
```

**...verify scenario alignment**
```bash
export IBDM_DEBUG=all
python scripts/run_scenario.py <scenario_id> --step
# Manually compare each turn's state_changes with debug output
```

**...fix a mismatch**
```bash
# 1. Determine: Is implementation or scenario wrong?
# 2. If scenario: edit JSON, commit "docs(scenarios): ..."
# 3. If implementation: fix code, run tests, update scenario, commit separately
```

---

## Summary for AI Assistants

**When you see a scenario**:
1. Treat it as documentation, not specification
2. If mismatched, check implementation correctness FIRST
3. Update scenario to match correct implementation
4. Never guess state_changes - observe actual behavior
5. Use debug logging to verify alignment

**When you write code**:
1. Implement correctly per Larsson (2002)
2. Write tests
3. Run scenarios to see behavior
4. Update scenario documentation to match
5. Commit implementation and docs separately

**Golden Rule**: Implementation follows Larsson. Scenarios follow implementation.

---

## References

- **Larsson (2002)**: `docs/reference/larsson-godis-thesis-2002.pdf`
- **Unified Scenario System**: `docs/UNIFIED_SCENARIO_SYSTEM.md`
- **Debug Configuration**: `docs/configuration/debug_config.md`
- **Scenario Runner**: `scripts/run_scenario.py`
- **Scenarios Directory**: `demos/scenarios/`
