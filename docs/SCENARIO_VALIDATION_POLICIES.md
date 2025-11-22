# Scenario Validation Policies

**Status**: ✅ CURRENT
**Last Updated**: 2025-11-22
**Audience**: AI Code Assistants

## Core Principles

### 1. Demonstrate Larsson System Behavior (PRIMARY GOAL)

**The goal is to demonstrate the behavior of a Larsson style system.**

Scenarios exist to:
- Show how Larsson (2002) algorithms work in practice
- Demonstrate Issue-Based Dialogue Management principles
- Provide working examples for understanding IBDM
- Validate that our implementation follows Larsson's thesis

Scenarios are NOT:
- Prescriptive specifications that drive implementation
- Aspirational examples of desired behavior
- Test cases that define requirements

**Key Insight**: Scenarios document what the Larsson-based system *actually does*, not what we wish it would do.

### 2. Expected State Changes Must Match Reality (VERIFICATION REQUIREMENT)

**The expected state changes in the scenario should match the real state changes that the dialogue engine shows.**

This means:
- Run the scenario with `IBDM_DEBUG=all` to observe actual state changes
- Document QUD operations exactly as logged (push/pop operations)
- Document commitment additions as they occur
- Document plan progression as it happens
- NEVER guess or assume what state changes will occur

**Verification Method**:
```bash
export IBDM_DEBUG=all
python scripts/run_scenario.py <scenario> --step > /tmp/trace.txt
# Compare scenario state_changes with actual debug output line by line
```

**Example of Correct Alignment**:
```json
// Scenario documents:
"state_changes": {
  "qud": "2 questions (clarification pushed onto stack)",
  "qud_top": "clarification question [is_clarification=True]"
}

// Debug log shows:
[DEBUG] QUD PUSH: WhQuestion(variable='X', predicate='clarification_for_legal_entities',
                             constraints={'is_clarification': True})
[DEBUG] QUD depth: 2

// ✓ These match - scenario is accurate
```

### 3. Notes Must Reflect Current Version (ACCURACY REQUIREMENT)

**When there are notes in the scenario, they should be accurate and reflect the behavior of the current version.**

This applies to:
- `business_explanation` - Must describe current behavior
- `larsson_rule` - Must reference correct Larsson rule/section
- Analysis reports in payoff turns - Must match current implementation
- State change descriptions - Must match current state structure
- Comments in scenario JSON - Must be current

**When Implementation Changes**:
1. Update scenario notes to match new behavior
2. Update analysis reports to reflect changes
3. Update business explanations if behavior changed
4. Don't leave outdated notes that confuse users

**Example**:
```json
// ❌ WRONG - outdated note from previous implementation
"business_explanation": "System uses fallback response"
// Current implementation actually does sophisticated clarification

// ✅ RIGHT - reflects current behavior
"business_explanation": "System acknowledges off-topic answer and guides user back to valid input"
```

---

## Policy #17: Zero Tolerance for Unverified Claims (MANDATORY)

**Rule**: NEVER claim scenarios are fixed without actually running them and verifying they work.

### Forbidden Actions ❌
- Claiming "I've fixed the issues" without verification
- Saying "the scenario should now work" without testing
- Making edits and assuming they're correct
- Skipping verification because "it's just a small change"

### Required Actions ✅
- Run `python scripts/run_scenario.py <scenario>` BEFORE claiming success
- Check for JSON syntax errors with the scenario runner
- Verify compliance passes (or report actual failures)
- Report actual test results, not assumptions

### Communication Rules
- ❌ NEVER: "I've fixed the issues" (without verification)
- ✅ ALWAYS: "Let me verify the fix" → run scenario → report actual results
- ❌ NEVER: "This should work now" (assumption)
- ✅ ALWAYS: "I've verified it works: [paste actual results]"

### Special Case - JSON Syntax Errors
JSON syntax errors (trailing commas, missing brackets, etc.) are caught IMMEDIATELY by the scenario runner. There is NO EXCUSE for not catching these before claiming a fix. Always run the scenario after editing JSON files.

**Zero Tolerance**: If you claim a fix without verification, you have failed the task regardless of whether the fix was correct.

---

## Policy #16: Scenario Alignment Workflow

**Core Principle**: Implementation demonstrates Larsson, scenarios document implementation.

### Priority Order
1. Ensure implementation correctly demonstrates Larsson algorithms
2. If implementation is incomplete/incorrect, fix it FIRST
3. Run implementation with `IBDM_DEBUG=all` to observe behavior
4. Document observed behavior in scenario state_changes
5. Verify notes and explanations match current behavior
6. Scenarios now accurately demonstrate the Larsson algorithm

### The Relationship

```
Larsson (2002) Thesis
        ↓ (authoritative specification)
Implementation (source of truth for behavior)
        ↓ (observable via debug logging)
Actual Runtime Behavior
        ↓ (documented in)
Scenarios (demonstration of behavior)
```

NOT:
```
Scenarios (specification)
        ↓
Implementation (tries to match)
```

### Task Types

**Type A - Creating new scenarios:**
1. Implement Larsson rule correctly
2. Run with `IBDM_DEBUG=all`
3. Observe actual behavior
4. Document what happens (state_changes)
5. Write accurate notes (business_explanation, larsson_rule)

**Type B - Updating scenarios:**
1. Verify implementation is correct per Larsson
2. Run scenario to observe current behavior
3. Update scenario state_changes to match
4. Update notes to reflect current behavior

**Type C - Fixing bugs:**
1. Fix implementation first
2. Verify fix with tests
3. Run scenario to observe new behavior
4. Update scenarios to reflect fix
5. Update notes if behavior changed

**Type D - Finding mismatches:**
1. Check if implementation or scenario is wrong
2. Check against Larsson (2002) to determine correctness
3. Fix implementation if needed
4. Update scenario to match corrected implementation
5. Update notes to accurately describe behavior

---

## Validation Workflow (Step-by-Step)

### Step 1: Identify the Problem
- Read scenario and identify issues
- Verify against Larsson (2002) requirements
- Determine if implementation or scenario is incorrect

### Step 2: Fix Implementation (if needed)
- Modify code to correctly implement Larsson algorithm
- Run `ruff format` and `ruff check` for code quality
- Run `pyright` for type checking (zero tolerance for type errors)
- Run relevant unit tests

### Step 3: Observe Actual Behavior
```bash
export IBDM_DEBUG=all
python scripts/run_scenario.py <scenario> --step > /tmp/trace.txt
```
- Watch QUD stack operations in debug log
- Watch rule evaluations and which rules fire
- Watch state modifications (commitments, beliefs, etc.)
- Note the exact sequence of operations

### Step 4: Update Scenario Documentation
- Update turn utterances to match actual output
- Update `state_changes` to match debug log
- Update `business_explanation` to describe current behavior
- Update `larsson_rule` to reference correct rule/section
- Update analysis reports with current behavior
- Ensure all notes are accurate and current

### Step 5: Verify JSON Validity
```bash
python -m json.tool < demos/scenarios/<scenario>.json > /dev/null
```
- Fix any syntax errors (trailing commas, missing brackets)
- Verify valid JSON before running scenario

### Step 6: Run Scenario to Verify Behavior
```bash
python scripts/run_scenario.py <scenario>
```
- **Actually run the scenario** (not assumed it would work)
- Verify each turn shows expected output
- Verify all state changes occur as documented
- Confirm scenario completes successfully
- Check for any error messages or warnings

### Step 7: Commit Only After Verification
- First commit: Implementation fix (if applicable)
- Second commit: Scenario updates
- Both commits made AFTER verifying changes work
- Use clear commit messages explaining what changed

---

## Tools for Validation

### Code Quality (Before Committing)
```bash
ruff format src/ tests/        # Format code
ruff check --fix src/ tests/   # Lint and fix
pyright src/                   # Type check (strict mode)
```

### Scenario Validation (Mandatory)
```bash
# JSON syntax validation
python -m json.tool < demos/scenarios/<scenario>.json

# Scenario execution validation
python scripts/run_scenario.py <scenario>

# Debug mode for observing behavior
export IBDM_DEBUG=all
python scripts/run_scenario.py <scenario> --step
```

### Before Every Commit
```bash
pytest                         # All tests must pass
```

---

## State Change Documentation Requirements

### Always Document

**QUD Operations**:
```json
"state_changes": {
  "qud": "2 questions (clarification pushed onto stack)",
  "qud_top": "clarification question [is_clarification=True]"
}
```
- Document exact QUD depth
- Note what type of question is on top
- Document push/pop operations

**Commitment Changes**:
```json
"state_changes": {
  "commitments": "+1 (legal_entities(Acme Corp and Smith Inc))",
  "qud": "0 questions (both clarification and original popped)"
}
```
- Document exact number of commitments added/removed
- Include the proposition format
- Note when questions are resolved

**Plan Operations**:
```json
"state_changes": {
  "plan": "active",
  "plan_type": "nda_drafting"
}
```
- Document plan creation
- Document plan completion
- Note which issues are accommodated

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
  "qud": "2 questions (clarification pushed onto stack)",
  "qud_top": "clarification question [is_clarification=True]"
}
// Or omit state_changes entirely until you can observe with IBDM_DEBUG=all
```

---

## Notes and Explanations Requirements

### business_explanation

Must describe what actually happens in current implementation:
- Why this turn occurs
- What the system is doing
- What the user is providing
- Any special handling that occurs

**Example - Current Version**:
```json
"business_explanation": "System acknowledges off-topic answer and guides user back to valid input"
```

**Not**:
```json
// ❌ Outdated - doesn't reflect current clarification behavior
"business_explanation": "System requests clarification"
```

### larsson_rule

Must reference the actual Larsson rule that fires:
- Include rule number if applicable (e.g., "Rule 4.3")
- Include thesis section reference (e.g., "Section 4.6.3")
- Describe what the rule does
- Match actual rule implementation in code

**Example**:
```json
"larsson_rule": "Rule 4.3 (IssueClarification) - pushes clarification above original question, generates recovery guidance"
```

### Analysis Reports (Payoff Turns)

Must accurately reflect current system behavior:
- Update metrics to match actual behavior
- Update comparisons to reflect current implementation
- Update recommendations based on current performance
- Include accurate examples from the dialogue

**Example - Updated for current version**:
```
System Behavior - Error Recovery:
  ⚠ User provided nonsensical answer: "blue"
  ✓ System did NOT accept invalid input
  ✓ System did NOT proceed with bad data
  ✓ System acknowledged off-topic answer explicitly  ← Current behavior
  ✓ System provided clear guidance for recovery      ← Current behavior
  ✓ System handled corrected input properly
  ✓ Dialogue recovered gracefully
```

---

## Special Considerations

### JSON Syntax Errors
- JSON errors are caught IMMEDIATELY by the scenario runner
- There is NO EXCUSE for not catching these before claiming a fix
- Always validate JSON syntax after editing .json files
- Common issues: trailing commas, unescaped quotes, missing brackets

### Type Errors (Policy #3)
- Zero tolerance for type errors in code I write or modify
- Type errors indicate design problems
- Never suppress with `# type: ignore` without documentation
- Run `pyright` before committing

### Implementation vs. Scenario Mismatches

When you find a mismatch:

1. **Check Larsson (2002)** - Which is correct per the thesis?
2. **If implementation is wrong** - Fix implementation first
3. **If scenario is wrong** - Update scenario to match implementation
4. **Update notes** - Ensure all explanations are accurate

---

## Critical Requirement: Scenario Alignment Skill

For scenario-related tasks, I MUST:
1. USE the Scenario Alignment Skill (`.claude/skills/scenario-alignment.md`) for incremental work
2. READ `docs/SCENARIO_ALIGNMENT.md` in full for philosophy and procedures
3. FOLLOW step-by-step procedures for task type (A, B, C, or D)
4. NEVER guess state changes - always observe with `IBDM_DEBUG=all`
5. VERIFY implementation correctness per Larsson (2002) before updating scenarios
6. COMMIT implementation fixes and scenario updates separately
7. ENSURE all notes and explanations match current behavior

---

## Example: Today's Clarification Fix

### What I Did Right

✅ **Identified implementation needed improvement**
- Clarification message was generic, not helpful
- Violated Larsson's requirement for helpful feedback

✅ **Fixed implementation first**
- Enhanced `generation_rules.py` with context-aware messages
- Acknowledged off-topic answer explicitly
- Provided clear guidance for recovery

✅ **Observed actual behavior**
```bash
export IBDM_DEBUG=all
python scripts/run_scenario.py ibis3_clarification
```

✅ **Updated scenario to match**
- Turn 4 utterance: New clarification message
- Turn 4 state_changes: Documented QUD operations
- Turn 4 notes: Updated business_explanation to reflect acknowledgment
- Turn 8 analysis: Updated to document new behavior

✅ **Verified before claiming success**
- Validated JSON syntax
- Ran scenario successfully
- Reported actual results

### What I Would Have Done Wrong Without These Policies

❌ Updated scenario without fixing implementation
❌ Assumed JSON was valid without checking
❌ Claimed "it's fixed" without running scenario
❌ Left outdated notes about "generic clarification"
❌ Guessed at state changes instead of observing them

**Result**: User would discover errors I should have caught, eroding trust.

---

## Summary Checklist

Before claiming a scenario is fixed:

- [ ] Implementation correctly demonstrates Larsson algorithm
- [ ] Ran scenario with `IBDM_DEBUG=all` to observe behavior
- [ ] State_changes match actual debug log output
- [ ] business_explanation reflects current behavior
- [ ] larsson_rule references correct rule and section
- [ ] Analysis reports document current implementation
- [ ] All notes are accurate for current version
- [ ] JSON syntax is valid
- [ ] Scenario runs successfully without errors
- [ ] Actually verified - not assumed

**Remember**: The goal is to demonstrate the behavior of a Larsson style system. Everything in the scenario must accurately reflect what the system actually does.

---

## References

- **CLAUDE.md**: Policy #16 (Scenario Alignment), Policy #17 (Verification)
- **SCENARIO_ALIGNMENT.md**: Philosophy and step-by-step procedures
- **Larsson (2002)**: Authoritative specification for algorithms
- **LARSSON_ALGORITHMS.md**: Implementation reference
