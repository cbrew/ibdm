# IBDM Architectural Analysis: Interpretation, Accommodation, Selection, Generation

## Executive Summary

The IBDM implementation has a **critical separation-of-concerns violation** in how task accommodation is handled relative to Larsson's theoretical framework. Task accommodation (plan creation) is currently happening during the **Interpretation phase** when it should happen during the **Integration phase**, creating two problems:

1. **Conceptual violation**: Mixing interpretation (utterance → move) with accommodation (inferring dialogue plans)
2. **Implementation issue**: The NLU engine bypasses interpretation rules entirely, making task accommodation unreachable when using LLM-based understanding

## Larsson's IBDM Framework

Based on Larsson's 2002 thesis and the GETTING_STARTED.md documentation, the IBDM control loop has four distinct phases:

### Phase 1: INTERPRETATION
**Input**: Utterance (text)  
**Output**: Dialogue Move (structured)  
**Goal**: Map natural language to structured dialogue moves

**Move Types**:
- `ask(Q)`: User raises question
- `answer(A)`: User provides answer
- `assert(P)`: User commits to proposition
- `request(T)`: User requests task/action
- Social moves: `greet()`, `quit()`

**Key Principle**: Interpretation is *syntactic*—it converts text to structured form. It should NOT infer plans or intentions beyond what's linguistically explicit.

### Phase 2: INTEGRATION
**Input**: Dialogue Move + Information State  
**Output**: Updated Information State  
**Goal**: Update shared beliefs, QUD stack, commitments, and plans based on the move

**Standard Integration Rules**:
- `ask(Q)` → push Q to QUD stack
- `answer(A)` → pop resolved question, add commitment
- `assert(P)` → add to commitments
- `request(T)` → **[task accommodation happens here]**

**Accommodation** (in Larsson's framework):
- **Question Accommodation**: When a question lacks reference (e.g., "When does it close?"), resolve using context
- **Answer Accommodation**: Handle elliptical answers
- **Task Accommodation**: When user makes a request, infer what information is needed to fulfill it

### Phase 3: SELECTION
**Input**: Information State  
**Output**: Dialogue Move (system action)  
**Goal**: Choose what the system should do next

**Selection Logic**:
- Can I answer top QUD? → answer move
- Can I help user's plan? → ask next question
- Can I provide information? → inform move

### Phase 4: GENERATION
**Input**: Dialogue Move  
**Output**: Utterance (text)  
**Goal**: Convert structured move to natural language

---

## Current IBDM Implementation

### Where Interpretation Rules Are (Correct Location)
**File**: `src/ibdm/rules/interpretation_rules.py`

**Rule Examples** (Correct):
- `_is_greeting()` → `_create_greeting_move()`: "hello" → `DialogueMove(type="greet")`
- `_is_wh_question()` → `_create_wh_question_move()`: "What is X?" → `DialogueMove(type="ask", content=WhQuestion(...))`
- `_is_answer()` → `_create_answer_move()`: Answer utterance → `DialogueMove(type="answer", content=Answer(...))`

These are **syntactic transformations**: text → structured move.

### Where Integration Rules Are (Correct Location)
**File**: `src/ibdm/rules/integration_rules.py`

**Rule Examples** (Correct):
- `integrate_question()`: Move of type "ask" → push to QUD
- `integrate_answer()`: Move of type "answer" → pop QUD, add commitment
- `integrate_request()`: Move of type "request" → **should do task accommodation**

---

## THE PROBLEM: Misplaced Task Accommodation

### Current Implementation (INCORRECT)

**File**: `src/ibdm/rules/interpretation_rules.py`, lines 434-505

```python
def create_interpretation_rules() -> list[UpdateRule]:
    return [
        # WRONG LOCATION: Task accommodation in interpretation rules!
        UpdateRule(
            name="accommodate_nda_task",
            preconditions=_is_nda_request,
            effects=_create_nda_plan,           # ← Creates plan here
            priority=12,
            rule_type="interpretation",         # ← Wrong: should be integration
        ),
        ...
    ]

def _is_nda_request(state: InformationState) -> bool:
    """Check if utterance is requesting NDA document generation."""
    utterance = state.private.beliefs.get("_temp_utterance", "")
    classifier = _get_task_classifier()
    result = classifier.classify(utterance)
    return is_nda_document and is_high_confidence

def _create_nda_plan(state: InformationState) -> InformationState:
    """Create a hierarchical plan for NDA document generation."""
    new_state = state.clone()
    
    # Create subplans for each NDA requirement
    subplans = [
        Plan(plan_type="findout", content=WhQuestion(variable="parties", ...)),
        Plan(plan_type="findout", content=AltQuestion(alternatives=["mutual", "one-way"])),
        ...
    ]
    
    nda_plan = Plan(
        plan_type="findout",
        content="nda_requirements",
        status="active",
        subplans=subplans,
    )
    
    # Store plan
    new_state.private.plan.append(nda_plan)
    
    # Also create a request move ← This is interpretation
    move = DialogueMove(
        move_type="request",
        content=utterance,
        speaker=speaker,
    )
    new_state.private.agenda.append(move)
    
    return new_state
```

**Problems with this approach**:

1. **Violates Interpretation Purity**: Interpretation rules should map utterances to moves, not create plans
2. **Uses LLM-based Task Classification**: Heavy semantic analysis during interpretation (should be lighter)
3. **Creates Both Move AND Plan**: Conflates two different phases
4. **Unreachable by NLU Engine**: The NLUDialogueEngine in `src/ibdm/engine/nlu_engine.py` overrides interpretation rules entirely with LLM-based interpretation, so this accommodation logic never executes

---

## The NLU Engine Bypass Issue

### Current NLU Engine Implementation
**File**: `src/ibdm/engine/nlu_engine.py`, lines 133-155

```python
def interpret(
    self, utterance: str, speaker: str, state: InformationState
) -> list[DialogueMove]:
    """Interpret utterance using NLU.
    
    This overrides the base interpret() to use LLM-based NLU interpretation.
    """
    nlu_context = NLUContext.create_empty()
    moves, _ = self.interpret_with_nlu_context(utterance, speaker, state, nlu_context)
    return moves

def _interpret_with_nlu(
    self,
    utterance: str,
    speaker: str,
    state: InformationState,
    nlu_context: NLUContext,
) -> tuple[list[DialogueMove], NLUContext]:
    """Interpret utterance using NLU components."""
    
    moves: list[DialogueMove] = []
    
    # Use context interpreter for comprehensive analysis
    if self.context_interpreter:
        interpretation = self.context_interpreter.interpret(utterance, state)
        
        # Create moves based on dialogue act
        if interpretation.dialogue_act:
            act_moves = self._create_moves_from_act(
                interpretation.dialogue_act,
                utterance,
                speaker,
                state,
                interpretation,
            )
            moves.extend(act_moves)
    
    return moves, nlu_context
```

**Problem**: 
- The NLU engine's `interpret()` method completely bypasses the rule-based interpretation rules in `interpretation_rules.py`
- Therefore, the `_create_nda_plan` accommodation rule is **never executed**
- The NLU engine has no mechanism to perform task accommodation

### Evidence from NDA Demo
**File**: `demos/SCENARIO_PLAN_NDA.md`, Turn 1 analysis:

The demo shows:
```
Turn 1: Task Initiation & Accommodation
Attorney: "I need to draft an NDA"

NLU Processing:
- Dialogue Act: `request`
- Intent: `draft_document`
- Document Type: `NDA`

IBDM Processing:
- Task Accommodation triggered
- System infers plan: `findout(parties, nda_type, effective_date, ...)`
```

But this accommodation is **described** not **implemented** in code. Looking at the NLUDialogueEngine, there's no code that:
1. Detects when a move is type "request"
2. Classifies the task type
3. Infers required information
4. Creates subplans
5. Pushes first question to QUD

---

## Correct Architecture (Per Larsson)

### Phase 1: INTERPRETATION (in `interpretation_rules.py`)

**ONLY syntactic transformation**: Utterance → DialogueMove

```python
def create_interpretation_rules() -> list[UpdateRule]:
    return [
        # Greetings
        UpdateRule(
            name="interpret_greeting",
            preconditions=_is_greeting,
            effects=_create_greeting_move,
            rule_type="interpretation",
        ),
        # Wh-questions
        UpdateRule(
            name="interpret_wh_question",
            preconditions=_is_wh_question,
            effects=_create_wh_question_move,
            rule_type="interpretation",
        ),
        # Yes/No questions
        UpdateRule(
            name="interpret_yn_question",
            preconditions=_is_yn_question,
            effects=_create_yn_question_move,
            rule_type="interpretation",
        ),
        # Answers
        UpdateRule(
            name="interpret_answer",
            preconditions=_is_answer,
            effects=_create_answer_move,
            rule_type="interpretation",
        ),
        # Assertions
        UpdateRule(
            name="interpret_assertion",
            preconditions=_is_assertion,
            effects=_create_assertion_move,
            rule_type="interpretation",
        ),
        # REQUESTS (no accommodation yet!)
        UpdateRule(
            name="interpret_request",
            preconditions=_is_request,
            effects=_create_request_move,
            rule_type="interpretation",
        ),
    ]

def _is_request(state: InformationState) -> bool:
    """Check if utterance is a request/command.
    
    Examples:
    - "I need an NDA"
    - "Draft a contract"
    - "Create a document"
    """
    utterance = state.private.beliefs.get("_temp_utterance", "")
    # SIMPLE heuristics: keywords, patterns
    # Do NOT use expensive LLM classification here
    request_keywords = ["need", "want", "require", "draft", "create", "generate"]
    return any(kw in utterance.lower() for kw in request_keywords)

def _create_request_move(state: InformationState) -> InformationState:
    """Create a request move.
    
    At this point, we don't know what task the user is requesting.
    That determination happens in ACCOMMODATION (integration phase).
    """
    new_state = state.clone()
    speaker = new_state.private.beliefs.get("_temp_speaker", "user")
    utterance = new_state.private.beliefs.get("_temp_utterance", "")
    
    # Create simple request move
    move = DialogueMove(
        move_type="request",
        content=utterance,  # Just store the text
        speaker=speaker,
    )
    new_state.private.agenda.append(move)
    return new_state
```

### Phase 2: INTEGRATION (in `integration_rules.py`)

**Task Accommodation happens here**: DialogueMove + Context → Updated IS + Inferred Plan

```python
def create_integration_rules() -> list[UpdateRule]:
    return [
        # ... existing rules ...
        
        # TASK ACCOMMODATION: When user makes a request
        UpdateRule(
            name="accommodate_request",
            preconditions=_is_request_move,
            effects=_accommodate_request_task,
            priority=11,  # Higher than other integration rules
            rule_type="integration",
        ),
    ]

def _is_request_move(state: InformationState) -> bool:
    """Check if the current move is a request."""
    move = state.private.beliefs.get("_temp_move")
    return isinstance(move, DialogueMove) and move.move_type == "request"

def _accommodate_request_task(state: InformationState) -> InformationState:
    """Accommodate a request by inferring task and creating plan.
    
    This is WHERE ACCOMMODATION HAPPENS.
    
    Process:
    1. Classify the task type using NLU/LLM
    2. Infer what information is needed
    3. Create hierarchical subplans
    4. Push first question to QUD
    """
    new_state = state.clone()
    move = new_state.private.beliefs.get("_temp_move")
    
    if not isinstance(move, DialogueMove) or move.move_type != "request":
        return new_state
    
    utterance = str(move.content)
    
    # STEP 1: Classify the task
    # (This IS expensive and semantic, appropriate for integration)
    task_classifier = _get_task_classifier()
    task_result = task_classifier.classify(utterance)
    
    # STEP 2: Determine domain and requirements
    if task_result.task_type == TaskType.DRAFT_DOCUMENT:
        if task_result.parameters.get("document_type") == "NDA":
            plan = _create_nda_accommodation(task_result)
            new_state.private.plan.append(plan)
            
            # STEP 3: Push first subplan's question to QUD
            if plan.subplans:
                first_question = plan.subplans[0].content
                if isinstance(first_question, Question):
                    new_state.shared.push_qud(first_question)
    
    # Track that we've accommodated
    new_state.private.beliefs["_accommodation_attempted"] = True
    new_state.private.beliefs["_task_type"] = task_result.task_type
    
    # Add to history
    new_state.shared.last_moves.append(move)
    
    # System should respond with first question
    new_state.control.next_speaker = new_state.agent_id
    
    return new_state

def _create_nda_accommodation(task_result) -> Plan:
    """Create NDA document plan from task classification."""
    subplans = [
        Plan(
            plan_type="findout",
            content=WhQuestion(variable="parties", predicate="legal_entities"),
            status="active",
        ),
        Plan(
            plan_type="findout",
            content=AltQuestion(alternatives=["mutual", "one-way"]),
            status="active",
        ),
        Plan(
            plan_type="findout",
            content=WhQuestion(variable="effective_date", predicate="date"),
            status="active",
        ),
        Plan(
            plan_type="findout",
            content=WhQuestion(variable="duration", predicate="time_period"),
            status="active",
        ),
        Plan(
            plan_type="findout",
            content=AltQuestion(alternatives=["California", "Delaware"]),
            status="active",
        ),
        Plan(
            plan_type="findout",
            content=YNQuestion(proposition="generate_document"),
            status="active",
        ),
    ]
    
    return Plan(
        plan_type="findout",
        content="nda_requirements",
        status="active",
        subplans=subplans,
    )
```

### Phase 3: SELECTION (unchanged)

Operates on the Information State that now has the plan. No changes needed.

### Phase 4: GENERATION (unchanged)

Converts moves to text. No changes needed.

---

## How NLU Engine Should Work

The NLU engine should respect the IBDM phases:

```python
class NLUDialogueEngine(DialogueMoveEngine):
    """NLU-enhanced engine that still respects IBDM phases."""
    
    def interpret(
        self, utterance: str, speaker: str, state: InformationState
    ) -> list[DialogueMove]:
        """Interpret using NLU, but only for INTERPRETATION phase.
        
        NLU should determine:
        - What dialogue act is this? (ask, answer, assert, request)
        - What is the semantic content? (question structure, assertion content)
        
        NLU should NOT determine:
        - What plan should be created? (that's accommodation)
        - What information is needed? (that's accommodation)
        """
        
        # Use NLU for dialogue act classification and semantic parsing
        dialogue_act = self.dialogue_act_classifier.classify(utterance)
        
        # Create basic move (interpretation only)
        if dialogue_act == DialogueActType.REQUEST:
            # Just create a request move with the utterance
            # Don't try to infer the plan here
            return [DialogueMove(
                move_type="request",
                content=utterance,
                speaker=speaker,
            )]
        
        # For other acts, proceed normally
        # ... handle questions, answers, etc.
    
    # integrate() is inherited and uses integration rules
    # Those rules can now do task accommodation
```

---

## Summary of Required Fixes

### Problem 1: Move Task Accommodation Rule
**From**: `interpretation_rules.py` (WRONG)  
**To**: `integration_rules.py` (CORRECT)

**Action**:
1. Remove `accommodate_nda_task` rule from `create_interpretation_rules()`
2. Create new `accommodate_request` rule in `create_integration_rules()`
3. Rename `_create_nda_plan` to `_create_nda_accommodation` to clarify it's accommodation
4. Update precondition to check for "request" move type (not utterance text)

### Problem 2: Simplify Interpretation Rules
**Goal**: Keep interpretation rules lightweight and syntactic

**Action**:
1. Add simple `_is_request()` precondition using keyword matching
2. Add `_create_request_move()` effect that just creates a basic request move
3. Remove LLM-based classification from interpretation phase

### Problem 3: Add Accommodation to Integration Rules
**Goal**: Make task accommodation explicit and reachable

**Action**:
1. Add `_accommodate_request_task()` integration rule
2. Use task classification here (it's now appropriate)
3. Create plans for different task types
4. Push first question to QUD
5. Make logic reachable from both rule-based and NLU interpretation

### Problem 4: Update NLU Engine
**Goal**: Have NLU engine create moves, let rules do accommodation

**Action**:
1. When NLU interprets a "request" utterance, create a basic request move
2. Don't try to infer plans in NLU engine
3. Let integration rules (which apply to both paths) do accommodation
4. Delete any task-specific logic from NLU engine's interpretation

---

## Benefits of This Architecture

1. **Clear Separation of Concerns**: Interpretation ≠ Accommodation
2. **Reusability**: Accommodation works for both rule-based and NLU interpretation
3. **Theoretical Soundness**: Aligns with Larsson's framework
4. **Maintainability**: Task accommodation logic is in one place (integration rules)
5. **Extensibility**: Adding new task types only requires adding accommodation rules
6. **Debuggability**: Clear phase boundaries make it easier to debug

---

## Larsson Citation

Per *Larsson, S. (2002). Issue-based Dialogue Management* and the GETTING_STARTED.md documentation:

> The control loop processes each user turn through four phases:
> 1. INTERPRET: utterance → dialogue moves (syntactic)
> 2. INTEGRATE: moves + context → updated information state (semantic)
> 3. SELECT: information state → system action (strategic)
> 4. GENERATE: move → utterance (linguistic)

Accommodation (including task accommodation) is explicitly part of the Integration phase, where the system updates its understanding of the user's goals and plans based on their moves.

