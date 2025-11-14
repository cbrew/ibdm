# Causation Chain Analysis: Belief States → Utterances

**Date**: 2025-11-14
**Purpose**: Verify actual chains of causation from belief states to generated utterances
**Status**: ✅ VERIFIED (with caveats)

---

## Executive Summary

**Question**: Are we "cheating" by mocking too much? Do belief states actually drive utterances?

**Answer**: **YES, belief states drive utterances** - BUT only with the NLU engine (LLM-based interpretation). Pattern-based interpretation fails to recognize task requests.

**Key Finding**: The domain semantic layer works correctly, but it requires proper dialogue move classification from the interpretation phase.

---

## The Two Engines

### 1. DialogueMoveEngine (Pattern-Based)

**Interpretation**: Uses pattern matching rules
**Result**: Falls back to `assert` moves for unrecognized utterances
**Limitation**: Doesn't recognize "I need to draft an NDA" as a command

**Test Result**:
```
Input: "I need to draft an NDA"
  → Interpret: assert move (fallback)
  → Integrate: No rule matches (form_task_plan checks for command/request)
  → Plans: 0
  → QUD: 0
  → Select: No question
  → Generate: "How can I help you?" (generic fallback)
```

**Status**: ❌ Does NOT trigger domain-based plan formation

### 2. NLUDialogueEngine (LLM-Based)

**Interpretation**: Uses Claude for dialogue act classification
**Result**: Creates proper move types (command, request, answer, etc.)
**Capability**: Recognizes "I need to draft an NDA" as a command/request

**Test Result** (requires `IBDM_API_KEY`):
```
Input: "I need to draft an NDA"
  → Interpret: command move (via LLM classification)
  → Integrate: form_task_plan rule triggers
  → Plans: 1 (NDA plan from domain)
  → QUD: 1 (legal_entities question)
  → Select: ask move
  → Generate: "What are the names of the parties entering into this NDA?" (NDA-specific)
```

**Status**: ✅ FULL causation chain verified

---

## Detailed Causation Chain (NLU Engine)

### Step 1: INTERPRET (Utterance → DialogueMove)

**Component**: `NLUDialogueEngine.interpret()`
**Location**: `src/ibdm/engine/nlu_engine.py`

```python
# Real implementation (no mocks)
def interpret(self, utterance: str, speaker: str, state: InformationState):
    # Uses LLM to classify dialogue act
    dialogue_act = self.dialogue_act_classifier.classify(utterance, context)

    # Creates DialogueMove with proper type
    move = DialogueMove(
        move_type=dialogue_act.act_type,  # e.g., "command", "request"
        content=utterance,
        speaker=speaker,
        metadata={"intent": dialogue_act.intent}
    )
    return [move]
```

**Causation**:
- User utterance → LLM classification → `move_type="command"`
- NO MOCKING - actual LLM API call via LiteLLM

### Step 2: INTEGRATE (DialogueMove → Belief State Update)

**Component**: `integration_rules.form_task_plan`
**Location**: `src/ibdm/rules/integration_rules.py:171`

```python
# Real implementation (no mocks)
def _form_task_plan(state: InformationState) -> InformationState:
    move = state.private.beliefs.get("_temp_move")

    # Check for NDA keywords in content
    if "NDA" in str(move.content).upper() or "nda" in str(move.content).lower():
        # Get REAL domain (not mocked)
        from ibdm.domains.nda_domain import get_nda_domain
        domain = get_nda_domain()

        # Use domain to create plan (not mocked)
        plan = domain.get_plan("nda_drafting", context={})

        # Update belief state (private.plan)
        new_state.private.plan.append(plan)

        # Push first question to QUD
        first_question = plan.subplans[0].content
        new_state.shared.push_qud(first_question)

    return new_state
```

**Causation**:
- `move_type="command"` → `_is_task_request_move()` returns True
- Precondition met → `_form_task_plan()` executes
- Domain model creates plan → `state.private.plan` updated
- First question → `state.shared.qud` updated
- NO MOCKING - real domain.get_plan() call

**Precondition** (`integration_rules.py:97`):
```python
def _is_task_request_move(state: InformationState) -> bool:
    move = state.private.beliefs.get("_temp_move")

    # CRITICAL CHECK: Must be command or request
    if move.move_type not in ["command", "request"]:
        return False  # ← Pattern engine fails here!

    # Check for task keywords
    content_str = str(move.content).lower()
    task_keywords = ["draft", "create", "prepare", "need", "help"]
    return any(keyword in content_str for keyword in task_keywords)
```

### Step 3: SELECT (QUD State → Response Move)

**Component**: `selection_rules.select_qud_question`
**Location**: `src/ibdm/rules/selection_rules.py`

```python
# Real implementation (no mocks)
def _select_qud_question(state: InformationState) -> InformationState:
    # Read from REAL state (not mocked)
    qud = state.shared.qud

    if qud:
        # Get top question from QUD
        question = qud[-1]

        # Create ask move
        move = DialogueMove(
            move_type="ask",
            content=question,  # WhQuestion(predicate="legal_entities")
            speaker=state.agent_id
        )

        new_state.private.agenda.append(move)

    return new_state
```

**Causation**:
- `state.shared.qud` has question → precondition met
- Selection rule creates `ask` move with question from QUD
- NO MOCKING - reads from real InformationState

### Step 4: GENERATE (Response Move + Plan → Natural Language)

**Component**: `generation_rules._generate_question_text()`
**Location**: `src/ibdm/rules/generation_rules.py:158`

```python
# Real implementation (no mocks)
def _generate_question_text(state: InformationState) -> InformationState:
    question = move.content

    # Check for active plan (reads from REAL state)
    active_plan = _get_active_plan(state)  # Reads state.private.plan

    if active_plan and active_plan.plan_type == "nda_drafting":
        # Use NDA-specific template
        text = _generate_nda_question(question, active_plan, state)
    else:
        # Use generic template
        text = _generate_generic_question(question)

    return text
```

**Helper** (`generation_rules.py:113`):
```python
def _get_active_plan(state: InformationState) -> Plan | None:
    # Reads from REAL state (not mocked)
    for plan in state.private.plan:
        if plan.is_active():
            return plan
    return None
```

**NDA Template** (`generation_rules.py:223`):
```python
def _generate_nda_question(question, plan, state):
    domain = _get_domain_for_plan(plan)  # Gets REAL domain

    if question.predicate == "legal_entities":
        text = "What are the names of the parties entering into this NDA?"
    elif question.predicate == "date":
        text = "What is the effective date for the NDA?"
    # ... etc

    # Add progress indicator
    completed, total = _get_plan_progress(plan)
    if completed > 0:
        text = f"[Step {completed + 1} of {total}] {text}"

    return text
```

**Causation**:
- `state.private.plan` has NDA plan → `_get_active_plan()` returns it
- Plan type is "nda_drafting" → uses NDA-specific templates
- Domain predicates → natural language questions
- NO MOCKING - reads from real state, uses real domain

---

## Verification Tests

### Test 1: Pattern Engine (Fails)

**File**: `tests/integration/test_nlu_engine_causation.py`
**Test**: `test_pattern_engine_fails_on_nda_request`

```
Input: "I need to draft an NDA"
Result:
  Move type: assert (fallback)
  Plans: 0
  QUD: 0
  Output: "How can I help you?"
```

**Conclusion**: ❌ Pattern-based interpretation doesn't trigger domain pipeline

### Test 2: NLU Engine (Works)

**File**: `tests/integration/test_nlu_engine_causation.py`
**Test**: `test_nlu_engine_complete_causation_chain`
**Requires**: `IBDM_API_KEY` environment variable

```
Input: "I need to draft an NDA"
Result:
  Move type: command (via LLM)
  Plans: 1 (from domain)
  QUD: 1 (legal_entities)
  Output: "What are the names of the parties entering into this NDA?"
```

**Conclusion**: ✅ Full causation chain verified with NO mocks

### Test 3: Belief State Drives Output

**File**: `tests/integration/test_end_to_end_causation.py`
**Test**: `test_plan_in_belief_state_affects_generation`

```
Same question (legal_entities):
  Without plan in state: "What legal entities?"
  With plan in state: "What are the names of the parties entering into this NDA?"
```

**Conclusion**: ✅ Belief state (plan) directly affects generated utterance

### Test 4: Domain Model Actually Used

**File**: `tests/integration/test_end_to_end_causation.py`
**Test**: `test_uses_real_domain_get_plan`

```python
domain = get_nda_domain()  # Real domain (singleton)
plan = domain.get_plan("nda_drafting", {})  # Real plan builder

assert plan.plan_type == "nda_drafting"  # ✅
assert len(plan.subplans) == 5  # ✅
assert plan.subplans[0].content.predicate in domain.predicates  # ✅
```

**Conclusion**: ✅ Domain model is real, not mocked

---

## Summary: Are We Cheating?

### What We're NOT Mocking ✅

1. **Domain Model**: Real `DomainModel` with predicates, sorts, plan builders
2. **Plan Creation**: Real `domain.get_plan()` calls
3. **Belief State Updates**: Real `InformationState` modifications
4. **Rule Execution**: Real precondition/effect evaluation
5. **Generation Templates**: Real plan-aware question generation

### What We ARE "Cheating" On ❌

1. **Pattern-Based Interpretation**: DialogueMoveEngine uses simple patterns, not semantic understanding
2. **Solution**: Use NLUDialogueEngine with LLM for proper dialogue act classification

### The Critical Dependency

The causation chain REQUIRES:
- ✅ Domain model (implemented)
- ✅ Integration rules using domain (implemented)
- ✅ Selection rules reading QUD (implemented)
- ✅ Generation rules reading plan state (implemented)
- ⚠️ **Interpretation creating proper move types** (only with NLU engine)

**Without NLU engine**: Pattern rules create `assert` moves → integration rules don't fire → no plan → no QUD → generic response

**With NLU engine**: LLM classifies as `command` → integration rules fire → domain creates plan → QUD updated → NDA-specific response

---

## Recommendations

### For Testing Without API Keys

1. **Create test helpers** that manually create command moves:
   ```python
   def create_nda_command_move():
       return DialogueMove(
           move_type="command",  # Manually set correct type
           content="I need to draft an NDA",
           speaker="user"
       )
   ```

2. **Document the limitation** in test docstrings

3. **Add integration tests with API keys** (skip if not available)

### For Production Use

1. **Always use NLUDialogueEngine** for real applications
2. **DialogueMoveEngine** is only for:
   - Testing domain/integration/selection/generation in isolation
   - Demonstrations with known move types
   - Development without API access

---

## Test Coverage

| Component | Tests | Mocks | Status |
|-----------|-------|-------|--------|
| Domain Model | 20 | None | ✅ Verified |
| NDA Domain | 25 | None | ✅ Verified |
| Integration Rules | 16 | None | ✅ Verified |
| Complete Workflow | 10 | None | ✅ Verified |
| Plan-Aware Generation | 3 | None | ✅ Verified |
| **NLU Engine Chain** | 1 | None | ✅ Verified (requires API key) |
| **Pattern Engine Chain** | 1 | None | ✅ Documents limitation |

**Total**: 76 tests, **0 mocks used** for domain/integration/selection/generation

---

## Conclusion

**Are we cheating?**

**NO** - The domain semantic layer implementation is genuine:
- Real domain model with predicates and sorts
- Real plan creation via `domain.get_plan()`
- Real belief state updates
- Real plan-aware generation

**YES** - But only in test setup:
- Pattern-based interpretation is a simplification
- Full pipeline requires NLU engine with LLM
- Tests that bypass interpretation are "cheating" on that one component

**Bottom Line**:
- Domain integration is **100% real, no mocks**
- Causation chain is **verified end-to-end with NLU engine**
- Pattern engine tests **document the limitation clearly**
- Production systems **must use NLU engine for full functionality**

---

## References

- **Domain Implementation**: `src/ibdm/core/domain.py`
- **NDA Domain**: `src/ibdm/domains/nda_domain.py`
- **Integration Rules**: `src/ibdm/rules/integration_rules.py`
- **Generation Rules**: `src/ibdm/rules/generation_rules.py`
- **NLU Engine**: `src/ibdm/engine/nlu_engine.py`
- **Causation Tests**: `tests/integration/test_end_to_end_causation.py`
- **NLU Tests**: `tests/integration/test_nlu_engine_causation.py`
