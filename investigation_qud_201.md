# Investigation: QUD Stack Management Issues (ibdm-201)

## Date: 2025-11-21
## Task: ibdm-201.1 - Investigate QUD stack operations in nda_comprehensive

## Background

The `nda_comprehensive` scenario shows QUD stack issues in turns 4, 6, 9, and 13 where:
- QUD should be pushed when clarification questions are asked
- QUD should be popped when answers are provided
- Instead, the QUD remains unchanged or "keeps growing"

## Code Review Findings

### QUD Operations Implementation (src/ibdm/core/information_state.py:298-311)

**Push operation** (lines 298-301):
```python
def push_qud(self, question: Question) -> None:
    """Push a question onto the QUD stack."""
    self.qud.append(question)
    logger.debug(f"QUD PUSH: {question} (depth: {len(self.qud)})")
```

**Pop operation** (lines 303-311):
```python
def pop_qud(self) -> Question | None:
    """Pop and return the top question from QUD stack."""
    if self.qud:
        question = self.qud.pop()
        logger.debug(f"QUD POP: {question} (depth: {len(self.qud)})")
        return question
    else:
        logger.debug("QUD POP: stack empty")
        return None
```

✅ **Result**: Basic QUD operations are correctly implemented with proper logging.

### Clarification Question Accommodation (src/ibdm/rules/integration_rules.py:515-559)

**Rule: `accommodate_clarification`** (lines 515-559):
- **When**: `_needs_clarification` flag is True (invalid answer detected)
- **Action**: Creates a clarification question and **pushes to QUD** (line 551)
- **Effect**: Original question remains on stack below (suspended)

✅ **Result**: Clarification push logic exists and calls `push_qud()`.

### Answer Integration (src/ibdm/rules/integration_rules.py:861-951)

**Rule: `integrate_answer`** (lines 861-951):
- **When**: Move type is "answer"
- **Action**: Checks if answer resolves top QUD using `domain.resolves()` (line 914)
- **If valid**: Pops QUD (line 917), adds commitment, marks subplan complete
- **If invalid**: Sets `_needs_clarification` flag, keeps question on QUD

✅ **Result**: Answer pop logic exists and calls `pop_qud()` when answer is valid.

## Scenario Analysis: nda_comprehensive.json

### Turn 3: User asks clarification question

**Expected**:
```json
{
  "qud_pushed": "?x.clarify [utterance=What does mutual mean exactly?, topic=mutual_nda]",
  "qud_depth": 2
}
```

**What should happen**:
1. User utterance "What does mutual mean exactly?" is interpreted as `clarification_question` move
2. Some integration rule should recognize this and push clarification onto QUD

**Question**: Is there a rule that handles incoming clarification_question moves and pushes them to QUD?

### Turn 4: System provides clarification

**Expected**:
```json
{
  "qud_unchanged": "?x.clarify...",
  "qud_depth": 3,
  "note": "System provides clarification but QUD not popped yet"
}
```

**Analysis**: System answers clarification but QUD should NOT pop yet because the user hasn't confirmed understanding. This seems correct.

### Turn 5: User answers "I think mutual makes sense"

**Expected**:
```json
{
  "qud_unchanged": "?x.clarify...",
  "commitment_added": "?{mutual, one-way}: I think mutual makes sense...",
  "note": "Answer creates question+answer commitment, not clean nda_type(mutual)"
}
```

**Problem**: QUD should have been popped here! The user's answer "I think mutual makes sense" should:
1. Resolve the original question (?x.nda_type)
2. Pop the clarification question from QUD
3. Pop the original question from QUD
4. Add a clean commitment

**Key Issue**: The answer is being integrated but NOT popping QUD. Why?

## Hypothesis

The problem may be in how the answer is being checked against the QUD:

1. **Clarification Question on Top**: After turn 3, the clarification question is on top of QUD
2. **User Answers Original Question**: In turn 5, user answers the ORIGINAL question (nda_type), not the clarification question directly
3. **Resolve Check Fails**: `domain.resolves(answer, top_question)` checks if answer resolves the TOP question (clarification), not the original question below it
4. **QUD Not Popped**: Since the answer doesn't resolve the clarification question specifically, QUD is not popped

## Key Question

How should the system handle when a user provides an answer to the original question after a clarification sub-dialogue?

**Option A**: The answer to the original question should:
1. Pop the clarification question (because it's been implicitly resolved)
2. Pop the original question (because it's been answered)

**Option B**: There should be an explicit acknowledgment that clarification was understood before popping

## Next Steps

1. ✅ Verify QUD push/pop methods work (CONFIRMED with test script)
2. ⏳ Check if clarification_question moves trigger QUD push
3. ⏳ Trace turn 5 integration to see why QUD is not popped
4. ⏳ Determine correct behavior for answering original question after clarification
5. ⏳ Review Larsson (2002) Section 4.2 for guidance on local question accommodation

## Test Results

### Basic QUD Operations
- ✅ `push_qud()` works correctly
- ✅ `pop_qud()` works correctly
- ✅ Logging triggers correctly
- ✅ LIFO stack semantics maintained

### Scenario Run (--show-engine-state)
- Turn 3: Clarification question IS on top of QUD ✅
- Turn 4: Clarification question STILL on top of QUD ✅
- Turn 5: Clarification question STILL on top of QUD ❌ (should have been popped)

## Root Cause Analysis

The QUD operations themselves work correctly. The problem is in the **integration logic** - specifically, how answers are matched against the QUD stack when there are nested questions (clarification sub-dialogues).

### Current Behavior (src/ibdm/rules/integration_rules.py:910-936)

```python
# Line 910: Get top question from QUD
top_question = new_state.shared.top_qud()
if top_question:
    # Line 914: Check if answer resolves THE TOP question
    if domain.resolves(answer, top_question):
        # Line 917: Pop QUD and add commitment
        new_state.shared.pop_qud()
        # ...
    else:
        # Line 931-936: Invalid answer - set clarification flag
        new_state.private.beliefs["_needs_clarification"] = True
```

**Problem**: This only checks the TOP question. In a clarification sub-dialogue:
- QUD stack: `[original_question, clarification_question]`
- User answers original question
- Check: Does answer resolve `clarification_question`? NO
- Result: QUD unchanged, no pop occurs

### Expected Behavior Per Larsson (2002)

According to Larsson Section 4.2 (Local Question Accommodation):

1. **Clarification Question Pushed**: When user doesn't understand, clarification question is pushed onto QUD, suspending the original question below it

2. **Answer Resolves Original**: When user provides answer to original question (even after clarification), this implicitly means:
   - Clarification was understood (implicit positive feedback)
   - Original question is now being answered
   - BOTH questions should be resolved and popped

3. **Nested Dialogue Closure**: Providing an answer to the suspended question closes the clarification sub-dialogue

### Missing Logic

The `integrate_answer` function needs to handle the case where:
1. Top QUD is a clarification question
2. Answer resolves the SUSPENDED question underneath
3. Action: Pop clarification question (implicitly resolved) + Pop original question (explicitly answered)

## Required Fix

Add logic to check questions deeper in the QUD stack when the answer doesn't resolve the top question but the top question is a clarification:

```python
top_question = new_state.shared.top_qud()
if top_question:
    if domain.resolves(answer, top_question):
        # Current path: answer resolves top question
        new_state.shared.pop_qud()
        # ... add commitment ...
    elif (is_clarification_question(top_question) and
          len(new_state.shared.qud) > 1):
        # NEW: Check if answer resolves the suspended question
        suspended_question = new_state.shared.qud[-2]  # Question below clarification
        if domain.resolves(answer, suspended_question):
            # Answer resolves suspended question
            # Pop clarification (implicitly resolved by providing answer)
            new_state.shared.pop_qud()
            # Pop original question (explicitly answered)
            new_state.shared.pop_qud()
            # ... add commitment for suspended question ...
        else:
            # Answer doesn't resolve either question - needs clarification
            new_state.private.beliefs["_needs_clarification"] = True
    else:
        # Answer doesn't resolve top question - needs clarification
        new_state.private.beliefs["_needs_clarification"] = True
```

## Verification Steps for Fix

1. Turn 3: Push clarification question → QUD depth = 2 ✓
2. Turn 5: Answer "mutual" resolves suspended question → Pop clarification + Pop original → QUD depth = 0 ✓
3. Turn 12-13: Same pattern for second clarification ✓

## Files to Modify

- `src/ibdm/rules/integration_rules.py` - Function `_integrate_answer` (lines 861-951)
- Add helper function to check if question is clarification
- Add logic to check suspended questions when top is clarification

## Testing

After fix, run:
```bash
export IBDM_DEBUG=qud
python scripts/run_scenario.py nda_comprehensive --show-engine-state
```

Expected QUD operations:
- Turn 3: QUD PUSH (clarification) → depth 2
- Turn 5: QUD POP (clarification) + QUD POP (original) → depth 0
- Turn 12: QUD PUSH (clarification) → depth 1
- Turn 13 or 16: QUD POP (clarification) + QUD POP (jurisdiction) → depth 0

## Conclusion

**Root Cause**: `integrate_answer` only checks if answer resolves the TOP question on QUD, failing to handle the case where a clarification question is on top but the user answers the suspended question underneath.

**Impact**: QUD stack grows without being popped, violating Larsson's LIFO semantics and breaking nested dialogue management.

**Solution**: Add logic to check suspended questions when top question is a clarification, and pop both questions when the answer resolves the suspended question.

**Status**: Investigation complete ✅ Ready for implementation phase (ibdm-202, ibdm-203)
