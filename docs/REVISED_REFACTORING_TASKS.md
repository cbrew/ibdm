# REVISED: NLU + IBDM + NLG Integration Tasks

**Supersedes**: Previous refactoring plan that incorrectly suggested keyword matching
**Based on**: ARCHITECTURE_NLU_IBDM_NLG_INTEGRATION.md
**Key Principle**: Use existing NLU, move accommodation to integration, enhance NLG

---

## The Correct Approach

**DO NOT** regress to keyword matching. We already have sophisticated NLU!

**DO** integrate the three systems properly:
1. **NLU** (already working) → interprets utterances semantically
2. **IBDM Integration** (needs fix) → accommodates tasks, manages plans
3. **NLG** (needs enhancement) → generates context-aware responses

---

## Task Breakdown

### Phase 1: Move Accommodation to Integration Phase ⭐ CRITICAL

**Epic**: Move task accommodation from interpretation to integration
**Time**: 3 hours
**Priority**: P0

#### Task 1.1: Add accommodate_command integration rule (P0)
**File**: `src/ibdm/rules/integration_rules.py`

```python
# Add new rule
UpdateRule(
    name="accommodate_command",
    preconditions=_is_command_or_request_move,
    effects=_accommodate_task,
    priority=13,  # Highest - before other integrations
    rule_type="integration"
)

def _is_command_or_request_move(state):
    """Check for command or request moves from NLU or rules."""
    move = state.private.beliefs.get("_temp_move")
    return isinstance(move, DialogueMove) and \
           move.move_type in ["command", "request"]
```

**Test**:
```python
def test_accommodate_command_rule_triggers():
    state = create_test_state()
    move = DialogueMove(type="command", content="I need to draft an NDA")
    state.private.beliefs["_temp_move"] = move

    assert _is_command_or_request_move(state) == True
```

**Time**: 30 min

---

#### Task 1.2: Implement _accommodate_task() with NDA support (P0)
**File**: `src/ibdm/rules/integration_rules.py`

```python
def _accommodate_task(state):
    """Accommodate user task by creating appropriate plan.

    Uses NLU metadata or task classification to infer user's goal.
    This is THE RIGHT PLACE for accommodation per Larsson.
    """
    move = state.private.beliefs.get("_temp_move")
    new_state = state.clone()

    # Option 1: Use NLU metadata (preferred)
    task_type = move.metadata.get("task_type")
    intent = move.metadata.get("intent")

    # Option 2: Fallback to task classifier
    if not task_type:
        classifier = _get_task_classifier()
        result = classifier.classify(str(move.content))
        task_type = result.task_type
        intent = result.parameters.get("document_type", "")

    # Dispatch to task-specific accommodation
    if task_type == "DRAFT_DOCUMENT" or "draft" in intent.lower():
        if "NDA" in intent.upper() or "NDA" in str(move.content).upper():
            plan = _create_nda_plan()
            new_state.private.plan.append(plan)

            # Push first question to QUD
            if plan.subplans:
                first_question = plan.subplans[0].content
                new_state.shared.push_qud(first_question)

    # Track move and set next speaker
    new_state.shared.last_moves.append(move)
    new_state.control.next_speaker = new_state.agent_id

    return new_state

def _create_nda_plan():
    """Create NDA drafting plan (moved from interpretation_rules.py)."""
    subplans = [
        Plan(plan_type="findout",
             content=WhQuestion(variable="parties", predicate="legal_entities"),
             status="active"),
        Plan(plan_type="findout",
             content=AltQuestion(alternatives=["mutual", "one-way"]),
             status="active"),
        Plan(plan_type="findout",
             content=WhQuestion(variable="effective_date", predicate="date"),
             status="active"),
        Plan(plan_type="findout",
             content=WhQuestion(variable="duration", predicate="time_period"),
             status="active"),
        Plan(plan_type="findout",
             content=AltQuestion(alternatives=["California", "Delaware"]),
             status="active"),
    ]

    return Plan(
        plan_type="nda_drafting",
        content="nda_requirements",
        status="active",
        subplans=subplans
    )

# Move task classifier here from interpretation
_task_classifier = None

def _get_task_classifier():
    """Get or create task classifier singleton."""
    global _task_classifier
    if _task_classifier is None:
        from ibdm.nlu.task_classifier import create_task_classifier
        _task_classifier = create_task_classifier(use_fast_model=True)
    return _task_classifier
```

**Test**:
```python
def test_accommodate_task_creates_nda_plan():
    state = create_test_state()
    move = DialogueMove(
        type="command",
        content="I need to draft an NDA",
        metadata={"intent": "draft_document", "task_type": "NDA"}
    )
    state.private.beliefs["_temp_move"] = move

    new_state = _accommodate_task(state)

    assert len(new_state.private.plan) == 1
    assert new_state.private.plan[0].plan_type == "nda_drafting"
    assert len(new_state.private.plan[0].subplans) == 5
    assert len(new_state.shared.qud) == 1  # First question pushed
```

**Time**: 1.5 hours

---

#### Task 1.3: Integration tests for accommodation (P1)
**File**: `tests/unit/test_integration_rules.py`

Add tests:
- `test_accommodate_command_rule_exists()`
- `test_accommodate_task_creates_nda_plan()`
- `test_qud_pushed_after_accommodation()`
- `test_nlu_command_triggers_accommodation()`
- `test_next_speaker_set_after_accommodation()`

**Time**: 1 hour

**Total Phase 1 Time**: 3 hours

---

### Phase 2: Clean Up Interpretation Rules

**Epic**: Remove accommodation from interpretation phase
**Time**: 1 hour
**Priority**: P1

#### Task 2.1: Remove accommodate_nda_task from interpretation (P1)
**File**: `src/ibdm/rules/interpretation_rules.py`

Delete:
- `accommodate_nda_task` rule
- `_is_nda_request()` function
- `_create_nda_plan()` function (moved to integration)
- `_task_classifier` global
- `_get_task_classifier()` function

**Time**: 20 min

---

#### Task 2.2: Update interpretation docstrings (P2)
**File**: `src/ibdm/rules/interpretation_rules.py`

Update module docstring:
```python
"""Interpretation rules for Issue-Based Dialogue Management.

Interpretation rules map utterances to dialogue moves. They are SYNTACTIC ONLY.

Task accommodation (plan creation) happens in the INTEGRATION phase,
not here. See integration_rules.py for accommodation logic.

Based on Larsson (2002) Issue-based Dialogue Management.
"""
```

**Time**: 10 min

---

#### Task 2.3: Verify tests still pass (P1)
**Command**: `pytest tests/unit/test_interpretation_rules.py -v`

Ensure no tests rely on accommodation in interpretation.

**Time**: 30 min

**Total Phase 2 Time**: 1 hour

---

### Phase 3: Enhance NLG with Plan Context

**Epic**: Generate context-aware, natural responses
**Time**: 2 hours
**Priority**: P1

#### Task 3.1: Add plan context helpers (P1)
**File**: `src/ibdm/rules/generation_rules.py`

```python
def _get_active_plan(state):
    """Get currently active plan, if any."""
    for plan in state.private.plan:
        if plan.is_active():
            return plan
    return None

def _get_plan_progress(plan):
    """Get plan progress (completed, total)."""
    if not plan or not plan.subplans:
        return (0, 0)

    completed = sum(1 for sp in plan.subplans if sp.status == "completed")
    total = len(plan.subplans)
    return (completed, total)
```

**Time**: 15 min

---

#### Task 3.2: Update _generate_question_text() for plan awareness (P1)
**File**: `src/ibdm/rules/generation_rules.py`

```python
def _generate_question_text(state):
    """Generate text for a question move with plan awareness."""
    new_state = state.clone()
    move = new_state.private.beliefs.get("_temp_generate_move")
    question = move.content

    # Check for active plan
    active_plan = _get_active_plan(state)

    if active_plan:
        # Plan-driven generation
        if active_plan.plan_type == "nda_drafting":
            text = _generate_nda_question(question, active_plan, state)
        else:
            # Fallback for unknown plan types
            text = _generate_generic_question(question)
    else:
        # No active plan - use generic
        text = _generate_generic_question(question)

    new_state.private.beliefs["_temp_generated_text"] = text
    return new_state

def _generate_generic_question(question):
    """Generic question generation (existing logic)."""
    if isinstance(question, WhQuestion):
        wh_word = question.constraints.get("wh_word", "what")
        predicate = question.predicate.replace("_", " ")
        return f"{wh_word.capitalize()} {predicate}?"
    elif isinstance(question, YNQuestion):
        proposition = question.proposition.replace("_", " ")
        return f"{proposition.capitalize()}?"
    elif isinstance(question, AltQuestion):
        if len(question.alternatives) == 2:
            return f"{question.alternatives[0].capitalize()} or {question.alternatives[1]}?"
        else:
            alt_list = ", ".join(question.alternatives[:-1])
            return f"{alt_list.capitalize()}, or {question.alternatives[-1]}?"
    else:
        return str(question)
```

**Time**: 30 min

---

#### Task 3.3: Implement NDA-specific question templates (P1)
**File**: `src/ibdm/rules/generation_rules.py`

```python
def _generate_nda_question(question, plan, state):
    """Generate NDA-specific question with context and progress."""
    completed, total = _get_plan_progress(plan)

    # WhQuestions
    if isinstance(question, WhQuestion):
        if question.predicate == "legal_entities":
            prefix = "Let's start with the basics." if completed == 0 else ""
            return f"{prefix} Who are the organizations entering into this NDA?".strip()

        elif question.predicate == "date":
            return f"What effective date should we use for this agreement? (Step {completed+1} of {total})"

        elif question.predicate == "time_period":
            return f"How long should the confidentiality obligations last? Common periods are 2-5 years. (Step {completed+1} of {total})"

    # AltQuestions
    elif isinstance(question, AltQuestion):
        if "mutual" in [a.lower() for a in question.alternatives]:
            return f"Will this be a mutual NDA (both parties share confidential info) or one-way? (Step {completed+1} of {total})"

        elif "california" in [a.lower() for a in question.alternatives]:
            return f"Which state's laws should govern this agreement - California or Delaware? (Step {completed+1} of {total})"

    # Fallback
    return _generate_generic_question(question)
```

**Time**: 45 min

---

#### Task 3.4: Add progress feedback (P2)
**File**: `src/ibdm/rules/generation_rules.py`

Add acknowledgment templates that show progress:
```python
def _generate_answer_acknowledgment(state, active_plan):
    """Generate acknowledgment with progress."""
    if not active_plan:
        return "Thank you."

    completed, total = _get_plan_progress(active_plan)

    if completed < total:
        return f"Great! That's {completed} of {total} requirements."
    else:
        return "Perfect! I have all the information needed to draft your NDA."
```

**Time**: 30 min

**Total Phase 3 Time**: 2 hours

---

### Phase 4: Integration Testing

**Epic**: Verify complete NLU → IBDM → NLG pipeline
**Time**: 2 hours
**Priority**: P1

#### Task 4.1: Create comprehensive NDA workflow test (P1)
**File**: `tests/integration/test_complete_nda_workflow.py`

```python
def test_complete_nda_workflow_with_nlu():
    """Test complete NDA workflow using NLU engine."""
    # Setup
    engine = NLUDialogueEngine(agent_id="system", rules=create_all_rules())
    state = InformationState(agent_id="system")

    # Turn 1: User requests NDA
    utterance = "I need to draft an NDA"
    moves = engine.interpret(utterance, "user", state)

    assert len(moves) == 1
    assert moves[0].move_type == "command"

    # Integrate (should trigger accommodation)
    for move in moves:
        state = engine.integrate(move, state)

    # Check plan was created
    assert len(state.private.plan) == 1
    assert state.private.plan[0].plan_type == "nda_drafting"

    # Check first question on QUD
    assert len(state.shared.qud) == 1

    # Select and generate
    response_move, state = engine.select_action(state)
    assert response_move.move_type == "ask"

    response_text = engine.generate(response_move, state)
    assert "parties" in response_text.lower() or "organizations" in response_text.lower()

    # Continue through all 5 questions...
    # (Full test would go through entire workflow)
```

**Time**: 1 hour

---

#### Task 4.2: Manual testing with interactive demo (P1)
**File**: `demos/03_nlu_integration_interactive.py`

Test scenarios:
1. "I need to draft an NDA" → should ask about parties
2. "Help me create an NDA" → same behavior
3. "Draft a confidentiality agreement" → same behavior
4. Answer all 5 questions → get final confirmation

Document results.

**Time**: 30 min

---

#### Task 4.3: Compare with rule-based interpretation (P2)
Verify accommodation works for both:
- NLU-created command moves
- Rule-created request moves (if we add a simple rule)

**Time**: 30 min

**Total Phase 4 Time**: 2 hours

---

### Phase 5: Documentation

**Epic**: Update all documentation
**Time**: 1 hour
**Priority**: P2

#### Task 5.1: Mark architecture issue as resolved (P2)
**File**: `ARCHITECTURE_ISSUE_SUMMARY.md`

Add banner:
```markdown
# ✅ RESOLVED: 2025-11-13

Task accommodation has been moved to the integration phase.
See: docs/ARCHITECTURE_NLU_IBDM_NLG_INTEGRATION.md
```

**Time**: 5 min

---

#### Task 5.2: Update CLAUDE.md policy (P2)
**File**: `CLAUDE.md`

Add architectural principle:
```markdown
### Policy #10: Accommodation in Integration Phase

**Policy**: Task accommodation (plan creation) belongs in the INTEGRATION phase, not interpretation.

**Rationale**: Per Larsson (2002), interpretation is syntactic/semantic analysis. Integration is where pragmatic understanding and accommodation happen.

**Implementation**:
- NLU engine interprets utterances → creates DialogueMoves
- Integration rules accommodate tasks → create plans
- Selection rules execute plans → choose next action
- Generation rules realize moves → produce natural language

**Example**: NDA request
1. INTERPRET: "I need an NDA" → DialogueMove(type="command")
2. INTEGRATE: Command move → create NDA plan → push first question to QUD
3. SELECT: Execute plan → ask first question
4. GENERATE: Use NDA template → "Who are the organizations..."
```

**Time**: 15 min

---

#### Task 5.3: Update burr_state_refactoring.md (P2)
**File**: `docs/burr_state_refactoring.md`

Update to reflect accommodation in integration.

**Time**: 20 min

---

#### Task 5.4: Update demo documentation (P2)
**File**: `demos/README.md`

Update description of 03_nlu_integration_interactive.py to explain:
- NLU interprets utterances
- Integration accommodates tasks
- System asks context-aware questions
- Natural conversation flow

**Time**: 20 min

**Total Phase 5 Time**: 1 hour

---

## Summary

### Total Effort: 9 hours (down from 12!)

| Phase | Tasks | Time | Priority |
|-------|-------|------|----------|
| 1. Move Accommodation | 3 | 3 hours | P0 |
| 2. Clean Up | 3 | 1 hour | P1 |
| 3. Enhance NLG | 4 | 2 hours | P1 |
| 4. Integration Testing | 3 | 2 hours | P1 |
| 5. Documentation | 4 | 1 hour | P2 |

### Key Differences from Original Plan

**REMOVED** (wrong approach):
- ❌ Keyword-based request detection
- ❌ Hybrid rule + NLU approach
- ❌ Multiple phases of NLU testing

**KEPT** (correct approach):
- ✅ Use existing NLU for interpretation
- ✅ Move accommodation to integration
- ✅ Plan-aware NLG
- ✅ Clean separation of concerns

### Success Criteria

- ✅ No keyword matching (NLU does interpretation)
- ✅ Accommodation in integration phase
- ✅ Works with NLU-created moves
- ✅ Plan-aware NLG generates natural responses
- ✅ Demo shows: "Let's start with the parties..." not "How can I help?"
- ✅ All tests pass

---

## Next Steps

1. Review this revised plan
2. Start with Phase 1, Task 1.1 (add accommodate_command rule)
3. Work through phases sequentially
4. Test after each task
5. Small commits following CLAUDE.md policy

---

## References

- **Correct Design**: docs/ARCHITECTURE_NLU_IBDM_NLG_INTEGRATION.md
- **Superseded Plan**: docs/REFACTORING_PLAN_accommodation.md (Phase 1 was wrong)
- **NLU Implementation**: src/ibdm/engine/nlu_engine.py (already correct!)
- **Integration Rules**: src/ibdm/rules/integration_rules.py (needs accommodation)
- **Generation Rules**: src/ibdm/rules/generation_rules.py (needs plan awareness)
