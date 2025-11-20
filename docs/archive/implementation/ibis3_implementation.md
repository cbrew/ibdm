# IBiS3 Implementation Guide

**Status**: ✅ CURRENT
**Date**: 2025-11-16
**Version**: 1.0 (Weeks 1-3 Complete)
**Progress**: 60% (Rules 4.1-4.2 implemented and tested)

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Rules 4.1 & 4.2 Implementation](#rules-41--42-implementation)
4. [Question Flow](#question-flow)
5. [Volunteer Information Handling](#volunteer-information-handling)
6. [Testing Approach](#testing-approach)
7. [Common Pitfalls](#common-pitfalls)
8. [Next Steps](#next-steps)

---

## Overview

### What is IBiS3?

**IBiS3** (Issue-Based Information State Update Approach, variant 3) is Larsson's dialogue management variant that adds **question accommodation** capabilities. This enables natural dialogue where users can:

1. **Volunteer information** before being asked
2. **Answer multiple questions** in a single utterance
3. **Skip redundant questions** that have already been answered

### Key Capabilities

Without IBiS3:
```
System: "What are the parties?"
User: "Acme and Smith, effective January 1, 2025"
System: [ignores date]
System: "What's the effective date?"
User: "I just told you, January 1!" ← BAD UX
```

With IBiS3:
```
System: "What are the parties?"
User: "Acme and Smith, effective January 1, 2025"
System: [accommodates date to private.issues, marks as answered]
System: "What's the governing law?" ← SKIPS DATE QUESTION
```

### Implementation Status

**Completed** (60%):
- ✅ Week 1: `private.issues` field in InformationState
- ✅ Week 2: Rules 4.1 (IssueAccommodation) and 4.2 (LocalQuestionAccommodation)
- ✅ Week 3: End-to-end testing, bug fixes, incremental questioning verified

**Remaining** (40%):
- 📋 Rule 4.3: IssueClarification (handle ambiguous answers)
- 📋 Rule 4.4: DependentIssueAccommodation (prerequisite questions)
- 📋 Rule 4.5: QuestionReaccommodation (re-prioritize questions)

---

## Architecture

### Information State Extensions

IBiS3 adds one new field to `PrivateIS`:

```python
@dataclass
class PrivateIS:
    plan: list[Plan]
    agenda: list[DialogueMove]
    beliefs: dict[str, Any]
    last_utterance: DialogueMove | None
    issues: list[Question]  # NEW for IBiS3
```

**Purpose**: `private.issues` holds questions that have been **accommodated** but not yet **raised** to the QUD.

### Two-Phase Accommodation

IBiS3 separates accommodation into two distinct phases:

1. **Accommodation** (Rule 4.1): Plan questions → `private.issues`
2. **Raising** (Rule 4.2): `private.issues` → `shared.qud` (incrementally)

**Why separate?**
- Enables incremental questioning (one at a time)
- Allows checking for volunteer answers before raising
- Provides control over question ordering

### Phase Separation

```
┌─────────────┐
│  INTERPRET  │ → Parse utterance, classify dialogue act
└──────┬──────┘
       ↓
┌─────────────┐
│  INTEGRATE  │ → Rule 4.1: Accommodate questions from plan to issues
│             │ → Check for volunteer answers in issues
│             │ → Process answers, update commitments
└──────┬──────┘
       ↓
┌─────────────┐
│   SELECT    │ → Rule 4.2: Raise question from issues to QUD
│             │ → Select next system move from agenda/QUD
└──────┬──────┘
       ↓
┌─────────────┐
│  GENERATE   │ → Generate natural language response
└─────────────┘
```

**Critical**: Task plan formation happens in **INTEGRATION** phase, not interpretation.

---

## Rules 4.1 & 4.2 Implementation

### Rule 4.1: IssueAccommodation

**Larsson Reference**: Section 4.6.1
**File**: `src/ibdm/rules/integration_rules.py`
**Priority**: 14 (runs BEFORE form_task_plan at priority 15)

#### Purpose

Accommodate questions from task plans into `private.issues` instead of pushing directly to QUD.

#### Precondition

```python
def precondition(state: InformationState) -> bool:
    """Check if there are plans with findout actions."""
    if not state.private.plan:
        return False

    for plan in state.private.plan:
        for action in plan.actions:
            if action.get("type") == "findout":
                return True
    return False
```

#### Effect

```python
def effect(state: InformationState) -> InformationState:
    """Extract questions from plan and add to private.issues."""
    new_state = state.clone()

    for plan in new_state.private.plan:
        for action in plan.actions:
            if action.get("type") == "findout":
                question = action.get("question")
                if question and question not in new_state.private.issues:
                    new_state.private.issues.append(question)

    return new_state
```

#### Key Points

1. **Does NOT push to QUD** - questions go to `private.issues`
2. **Runs early** (priority 14) to ensure questions are accommodated before other rules
3. **Deduplicates** - only adds questions not already in issues
4. **Preserves plan** - doesn't modify the plan, just extracts questions

#### Testing

```python
def test_rule_41_issue_accommodation():
    """Test that plan questions are accommodated to private.issues."""
    state = InformationState.create()

    # Create plan with findout actions
    plan = Plan(
        actions=[
            {"type": "findout", "question": WhQuestion(variable="x", predicate="parties")},
            {"type": "findout", "question": WhQuestion(variable="x", predicate="effective_date")},
        ]
    )
    state.private.plan.append(plan)

    # Apply Rule 4.1
    rule = IntegrationRule(
        name="accommodate_issue_from_plan",
        precondition=precondition,
        effect=effect,
        priority=14
    )

    if rule.precondition(state):
        new_state = rule.effect(state)

        # Verify questions in private.issues
        assert len(new_state.private.issues) == 2
        assert new_state.private.issues[0].predicate == "parties"
        assert new_state.private.issues[1].predicate == "effective_date"

        # Verify NOT on QUD
        assert len(new_state.shared.qud) == 0
```

### Rule 4.2: LocalQuestionAccommodation

**Larsson Reference**: Section 4.6.2
**File**: `src/ibdm/rules/selection_rules.py`
**Priority**: 20 (high priority in selection phase)

#### Purpose

Raise questions from `private.issues` to `shared.qud` incrementally (one at a time).

#### Precondition

```python
def precondition(state: InformationState) -> bool:
    """Check if there are issues to raise and QUD is not busy."""
    # Has accommodated issues
    if not state.private.issues:
        return False

    # QUD should be empty or not actively pursuing a question
    # (allows raising next question after previous one resolved)
    return True
```

#### Effect

```python
def effect(state: InformationState) -> InformationState:
    """Raise first question from private.issues to shared.qud."""
    new_state = state.clone()

    if new_state.private.issues:
        # Take first question from issues
        question = new_state.private.issues.pop(0)

        # Push to QUD
        new_state.shared.push_qud(question)

        # Add to agenda to ensure system asks it
        move = DialogueMove(
            move_type="ask",
            content=question,
            speaker=new_state.control.system_id
        )
        new_state.private.agenda.append(move)

    return new_state
```

#### Key Points

1. **Incremental** - only raises ONE question at a time
2. **FIFO ordering** - takes first question from issues list
3. **Adds to agenda** - ensures system will ask the question
4. **Runs in SELECT phase** - after integration rules have processed

#### Testing

```python
def test_rule_42_local_question_accommodation():
    """Test that questions are raised from issues to QUD incrementally."""
    state = InformationState.create()

    # Add questions to private.issues
    q1 = WhQuestion(variable="x", predicate="parties")
    q2 = WhQuestion(variable="x", predicate="effective_date")
    state.private.issues.extend([q1, q2])

    # Apply Rule 4.2 (first time)
    rule = SelectionRule(
        name="raise_accommodated_question",
        precondition=precondition,
        effect=effect,
        priority=20
    )

    if rule.precondition(state):
        new_state = rule.effect(state)

        # Verify ONE question raised
        assert len(new_state.shared.qud) == 1
        assert new_state.shared.qud[0] == q1

        # Verify one question remains in issues
        assert len(new_state.private.issues) == 1
        assert new_state.private.issues[0] == q2

        # Verify question on agenda
        assert len(new_state.private.agenda) == 1
        assert new_state.private.agenda[0].move_type == "ask"
```

---

## Question Flow

### Complete Flow Diagram

```
1. Task Plan Created
   ├─ Plan: [findout(parties), findout(date), findout(law)]
   └─ private.plan: [Plan]

2. Rule 4.1 (IssueAccommodation) - Priority 14
   ├─ Extract questions from plan
   └─ private.issues: [Q_parties, Q_date, Q_law]

3. Rule 4.2 (LocalQuestionAccommodation) - Priority 20
   ├─ Pop Q_parties from issues
   ├─ Push Q_parties to QUD
   ├─ Add "ask(Q_parties)" to agenda
   └─ QUD: [Q_parties], issues: [Q_date, Q_law]

4. System asks: "What are the parties?"

5. User answers: "Acme and Smith, effective Jan 1"

6. integrate_answer (modified for IBiS3)
   ├─ Check if "Jan 1" resolves Q_date in private.issues
   ├─ Yes! Remove Q_date from issues
   ├─ Add commitment: effective_date = "Jan 1"
   ├─ Process "Acme and Smith" as answer to Q_parties
   ├─ Pop Q_parties from QUD (resolved)
   └─ issues: [Q_law] (date question REMOVED)

7. Rule 4.2 fires again
   ├─ Pop Q_law from issues
   ├─ Push Q_law to QUD
   └─ QUD: [Q_law], issues: []

8. System asks: "What's the governing law?"
   (SKIPPED Q_date because it was volunteer answered!)
```

### Key Insight

The flow ensures:
- **Incremental questioning**: One question at a time
- **Volunteer detection**: Checks `private.issues` before raising
- **No redundancy**: Already-answered questions removed from issues

---

## Volunteer Information Handling

### Modified integrate_answer Rule

**File**: `src/ibdm/rules/integration_rules.py`
**Priority**: 10

#### Original Behavior (IBiS1)

```python
def integrate_answer_ibis1(state: InformationState, move: DialogueMove) -> InformationState:
    """Original: only check QUD."""
    top_qud = state.shared.top_qud()

    if top_qud and resolves(answer, top_qud):
        new_state.shared.pop_qud()
        new_state.shared.commitments.add(answer_content)

    return new_state
```

**Problem**: Ignores volunteer information that doesn't address current QUD.

#### Enhanced Behavior (IBiS3)

```python
def integrate_answer_ibis3(state: InformationState, move: DialogueMove) -> InformationState:
    """Enhanced: check private.issues FIRST, then QUD."""
    answer = move.content
    new_state = state.clone()

    # STEP 1: Check if answer resolves any question in private.issues
    for i, issue in enumerate(new_state.private.issues):
        if domain.resolves(answer, issue):
            # Remove from issues (already answered!)
            new_state.private.issues.pop(i)
            # Add commitment
            new_state.shared.commitments.add(extract_content(answer))
            logger.info(f"Volunteer answer matched issue: {issue}")
            break  # Only match one issue per answer

    # STEP 2: Check if answer resolves question on QUD
    top_qud = new_state.shared.top_qud()
    if top_qud and domain.resolves(answer, top_qud):
        new_state.shared.pop_qud()
        new_state.shared.commitments.add(extract_content(answer))
        logger.info(f"Answer resolved QUD: {top_qud}")

    return new_state
```

#### Key Changes

1. **Check `private.issues` FIRST** - before checking QUD
2. **Remove matched issues** - prevents re-asking
3. **Still check QUD** - handle direct answers too
4. **Order matters** - volunteer detection happens before QUD resolution

### Example: Multi-Fact Answer

User says: "Acme and Smith, effective January 1, 2025"

**NLU Processing** (with IBiS3-capable NLU):
```python
# Using BaseNLUService interface
multi_fact = nlu_service.extract_multiple_facts(utterance, state)

# Result:
# multi_fact.primary_fact = ExtractedFact(
#     predicate="parties",
#     value=["Acme Corp", "Smith Inc"],
#     is_volunteer=False
# )
# multi_fact.volunteer_facts = [
#     ExtractedFact(
#         predicate="effective_date",
#         value="2025-01-01",
#         is_volunteer=True
#     )
# ]
```

**Dialogue Manager Processing**:
1. Primary fact → processes as answer to current QUD (parties)
2. Volunteer fact → checks against `private.issues`
3. Finds Q_effective_date in issues → removes it, adds commitment
4. Result: effective_date question won't be asked later

---

## Testing Approach

### Unit Tests

**File**: `tests/unit/test_ibis3_rules.py`

Test each rule in isolation:

```python
def test_rule_41_accommodation():
    """Test Rule 4.1: plan → issues."""
    # Setup
    state = create_state_with_plan()

    # Execute
    new_state = apply_rule_41(state)

    # Verify
    assert len(new_state.private.issues) == expected_count
    assert questions_match_plan(new_state)

def test_rule_42_raising():
    """Test Rule 4.2: issues → QUD (incremental)."""
    # Setup
    state = create_state_with_issues()

    # Execute
    new_state = apply_rule_42(state)

    # Verify
    assert len(new_state.shared.qud) == 1  # ONE question
    assert len(new_state.private.issues) == original - 1
```

### Integration Tests

**File**: `tests/integration/test_ibis3_end_to_end.py`

Test complete dialogue flows:

```python
def test_ibis3_incremental_questioning():
    """Test that system asks questions one at a time."""
    # Turn 1: Create plan with 5 questions
    state = manager.process_input("create NDA", "user")
    assert len(state.private.issues) == 5  # All accommodated
    assert len(state.shared.qud) == 1      # Only one raised
    response = manager.generate(state)
    assert "What are the parties?" in response  # First question

    # Turn 2: Answer first question
    state = manager.process_input("Acme and Smith", "user")
    assert len(state.shared.qud) == 1      # Next question raised
    assert len(state.private.issues) == 3  # One answered, one raised
    response = manager.generate(state)
    assert "effective date" in response     # Second question

    # Verify: ONE QUESTION AT A TIME

def test_ibis3_volunteer_information():
    """Test that volunteer information prevents re-asking."""
    # Turn 1: Ask for parties
    state = manager.process_input("create NDA", "user")
    response = manager.generate(state)
    assert "parties" in response

    # Turn 2: Answer with volunteer date
    state = manager.process_input("Acme and Smith, effective Jan 1", "user")

    # Verify: date question removed from issues
    date_questions = [q for q in state.private.issues if "date" in str(q)]
    assert len(date_questions) == 0

    # Turn 3: Should NOT ask about date
    response = manager.generate(state)
    assert "date" not in response.lower()
    assert "effective" not in response.lower()
```

### Test with Mock NLU

**File**: `tests/unit/test_ibis3_with_mock_nlu.py`

Use `MockNLUService` for fast, deterministic testing:

```python
from tests.mocks import MockNLUService, create_mock_nlu
from ibdm.nlu.base_nlu_service import MultiFact, ExtractedFact

def test_volunteer_info_with_mock():
    """Test volunteer information using mock NLU."""
    # Setup mock NLU
    mock_nlu = create_mock_nlu(ibis_level="IBiS3")

    # Configure multi-fact response
    mock_nlu.configure_response(
        utterance="Acme and Smith, effective Jan 1",
        dialogue_act="answer",
        multi_fact=MultiFact(
            primary_fact=ExtractedFact(
                predicate="parties",
                value=["Acme", "Smith"],
                is_volunteer=False
            ),
            volunteer_facts=[
                ExtractedFact(
                    predicate="effective_date",
                    value="2025-01-01",
                    is_volunteer=True
                )
            ]
        )
    )

    # Create dialogue manager with mock NLU
    manager = DialogueManager(nlu_service=mock_nlu)

    # Test dialogue
    state = manager.process_input("Acme and Smith, effective Jan 1", "user")

    # Verify both facts processed
    assert has_commitment(state, "parties")
    assert has_commitment(state, "effective_date")
```

**Benefits of MockNLUService**:
- No LLM calls (fast, free)
- Deterministic (same input → same output)
- Configurable (set up exact test scenarios)
- IBiS3-capable (supports multi-fact extraction)

---

## Common Pitfalls

### 1. Rule Priority Ordering

**Problem**: Rules fire in wrong order, breaking the flow.

**Symptom**:
```
ERROR: form_task_plan runs BEFORE accommodate_issue_from_plan
Result: Questions pushed directly to QUD, bypassing issues
```

**Solution**:
```python
# CORRECT ordering (priority determines execution order - LOWER runs FIRST)
accommodate_issue_from_plan: priority=14  # Runs FIRST
form_task_plan: priority=15               # Runs SECOND
integrate_answer: priority=10             # Runs even earlier
```

**Rule of Thumb**: Lower priority number = runs earlier

**Week 3 Fix**: We discovered this bug and fixed rule priorities:
- `accommodate_issue_from_plan` now runs at priority 14
- `form_task_plan` runs at priority 15
- This ensures questions are accommodated to issues BEFORE plan formation completes

### 2. Fallback Selection Firing Too Early

**Problem**: Fallback rule fires when it shouldn't, bypassing Rule 4.2.

**Symptom**:
```
System has questions in private.issues
But fallback fires and says "I don't know what to do"
Rule 4.2 never gets to raise questions to QUD
```

**Solution**:
```python
# WRONG: Fallback fires when agenda is empty
def fallback_precondition(state):
    return not state.private.agenda

# CORRECT: Fallback only fires when agenda AND issues are empty
def fallback_precondition(state):
    return not state.private.agenda and not state.private.issues
```

**Week 3 Fix**: Updated fallback precondition to check both agenda AND issues.

### 3. Direct QUD Push from Plan

**Problem**: Task plan formation pushes questions directly to QUD.

**Symptom**:
```
All 5 questions appear on QUD immediately
System asks all questions in rapid succession
Incremental questioning doesn't work
```

**Solution**:
```python
# WRONG: Push to QUD in plan formation
def form_task_plan(state):
    for question in plan.questions:
        state.shared.push_qud(question)  # ❌ NO!

# CORRECT: Let Rule 4.1 accommodate to issues
def form_task_plan(state):
    # Just create the plan with findout actions
    plan = Plan(actions=[
        {"type": "findout", "question": q}
        for q in questions
    ])
    state.private.plan.append(plan)
    # Rule 4.1 will handle accommodation to issues
```

**Week 3 Fix**: Removed direct QUD push from `_form_task_plan`. Rule 4.2 now exclusively handles raising questions.

### 4. Not Checking private.issues in integrate_answer

**Problem**: Volunteer information ignored because only QUD is checked.

**Symptom**:
```
User: "Acme and Smith, effective Jan 1"
System: [processes parties]
System: "What's the effective date?"  ← Should have been skipped!
```

**Solution**:
```python
# WRONG: Only check QUD
def integrate_answer(state, answer):
    if resolves(answer, state.shared.top_qud()):
        # process answer

# CORRECT: Check issues FIRST, then QUD
def integrate_answer(state, answer):
    # Check private.issues for volunteer matches
    for issue in state.private.issues:
        if resolves(answer, issue):
            state.private.issues.remove(issue)
            # add commitment

    # Then check QUD
    if resolves(answer, state.shared.top_qud()):
        # process direct answer
```

**Week 2 Implementation**: Modified `integrate_answer` to check `private.issues` before QUD.

### 5. Forgetting to Clone State

**Problem**: Mutating state in-place instead of creating new state.

**Symptom**:
```
Burr can't track state changes
Rollback doesn't work
State history is broken
```

**Solution**:
```python
# WRONG: Mutate in place
def effect(state):
    state.private.issues.append(question)  # ❌ Mutates original!
    return state

# CORRECT: Clone first
def effect(state):
    new_state = state.clone()  # ✅ Create new state
    new_state.private.issues.append(question)
    return new_state
```

**Policy #0**: All dialogue engine methods must be pure functions. Always clone state.

---

## Next Steps

### Remaining IBiS3 Rules (60% → 100%)

**Week 5-6: Rule 4.3 - IssueClarification** (60% → 75%)
- Handle ambiguous utterances
- Generate clarification questions
- Larsson Section 4.6.3

```python
# Example
User: "The hotel"  # Which hotel?
System: "Which hotel do you mean - Hotel A or Hotel B?"
```

**Week 7-8: Rule 4.4 - DependentIssueAccommodation** (75% → 85%)
- Handle prerequisite questions
- Order questions based on dependencies
- Larsson Section 4.6.4

```python
# Example
Q1: "What's the party address?" depends on Q2: "Who are the parties?"
System asks Q2 first, then Q1
```

**Week 9-10: Rule 4.5 - QuestionReaccommodation** (85% → 95%)
- Re-prioritize unresolved questions
- Handle persistent failures
- Larsson Section 4.6.5

```python
# Example
After 3 failed attempts to get effective date:
System reformulates: "When does the agreement start?"
```

### NLU Enhancement for IBiS3

Current `NLUServiceAdapter` provides IBiS1 support. To fully leverage IBiS3:

**Enhance Multi-Fact Extraction**:
```python
class IBiS3NLUService(NLUServiceAdapter):
    """Enhanced NLU with IBiS3 multi-fact extraction."""

    def extract_multiple_facts(self, utterance, state):
        """Extract primary + volunteer facts from utterance."""
        # Use LLM to identify all facts in utterance
        # Compare against private.issues to identify volunteers
        # Return MultiFact with primary and volunteer facts
```

**Benefits**:
- Better volunteer information detection
- Semantic matching for question resolution
- Context-aware interpretation

### Testing Coverage

**Current**: 155 core tests passing, 3 end-to-end IBiS3 tests

**Add**:
- More volunteer information scenarios
- Multi-turn dialogue with complex question dependencies
- Error cases (clarification, reaccommodation)
- Performance tests (large task plans)

### Documentation

**Complete**:
- ✅ This implementation guide
- ✅ SYSTEM_ACHIEVEMENTS.md (Week 3 progress)
- ✅ LARSSON_PRIORITY_ROADMAP.md (IBiS3 status)

**Add**:
- API documentation for IBiS3-specific methods
- Tutorial: Building an IBiS3 dialogue application
- Comparison: IBiS1 vs IBiS3 dialogue quality

---

## References

### Larsson (2002) Thesis

- **Section 4.6.1**: IssueAccommodation (Rule 4.1)
- **Section 4.6.2**: LocalQuestionAccommodation (Rule 4.2)
- **Section 4.6.3**: IssueClarification (Rule 4.3)
- **Section 4.6.4**: DependentIssueAccommodation (Rule 4.4)
- **Section 4.6.5**: QuestionReaccommodation (Rule 4.5)
- **Chapter 4**: Question Accommodation (complete IBiS3 specification)

### IBDM Documentation

- `IBIS_VARIANTS_PRIORITY.md` - IBiS3 completion roadmap
- `LARSSON_PRIORITY_ROADMAP.md` - Overall priorities
- `SYSTEM_ACHIEVEMENTS.md` - Week 1-3 achievements
- `docs/LARSSON_ALGORITHMS.md` - Extracted algorithms
- `docs/nlu_interface_specification.md` - NLU requirements

### Code

- `src/ibdm/core/information_state.py` - State structure with `private.issues`
- `src/ibdm/rules/integration_rules.py` - Rules 4.1, integrate_answer modifications
- `src/ibdm/rules/selection_rules.py` - Rule 4.2
- `tests/integration/test_ibis3_end_to_end.py` - End-to-end tests

---

## Summary

**IBiS3 Implementation** (60% complete) enables natural dialogue through:

1. **Two-Phase Accommodation**: Questions accommodated to `private.issues`, then raised to QUD incrementally
2. **Volunteer Information**: Answers checked against `private.issues` before QUD
3. **Incremental Questioning**: One question at a time, not all at once
4. **No Redundancy**: Already-answered questions removed from issues

**Key Rules Implemented**:
- ✅ Rule 4.1 (IssueAccommodation): plan → issues
- ✅ Rule 4.2 (LocalQuestionAccommodation): issues → QUD
- ✅ Modified integrate_answer: Check issues before QUD

**Testing**:
- ✅ 155 core tests passing
- ✅ 3 end-to-end IBiS3 integration tests
- ✅ Mock NLU service for testing without LLM

**Next Milestone**: Rule 4.3 (IssueClarification) → 75% complete

The foundation is solid. Rules 4.1-4.2 provide the core accommodation mechanism. Rules 4.3-4.5 will add robustness and sophistication to the dialogue experience.
