# NLU + IBDM + NLG Integration Design

**Date**: 2025-11-13
**Status**: Design Document
**Supersedes**: REFACTORING_PLAN_accommodation.md (Phase 1 keyword approach)

---

## The Correct Architecture

### Current Problem

We have three sophisticated systems that aren't properly integrated:

1. **NLU (Natural Language Understanding)**: LLM-based interpretation in `nlu_engine.py`
   - Already interprets utterances → creates DialogueMoves
   - Uses Claude for semantic understanding
   - Creates: command, request, question, answer, assertion moves

2. **IBDM (Issue-Based Dialogue Management)**: Larsson's framework in `rules/`
   - Manages QUD stack, commitments, plans
   - Should handle task accommodation
   - Currently: accommodation is in WRONG phase (interpretation)

3. **NLG (Natural Language Generation)**: Template-based generation in `generation_rules.py`
   - Creates utterances from DialogueMoves
   - Currently: ignores plan context
   - Generic templates only

**The Issue**: Accommodation (plan creation) is in interpretation phase, so NLU-created moves bypass it.

---

## The Correct Design: NLU → IBDM → NLG Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    DIALOGUE TURN PROCESSING                      │
└─────────────────────────────────────────────────────────────────┘

User Utterance: "I need to draft an NDA"
        │
        ▼
┌───────────────────────────────────────────────────────────────────┐
│ PHASE 1: INTERPRET (NLU)                                          │
│                                                                   │
│  NLUDialogueEngine.interpret():                                  │
│    ├─ LLM analyzes utterance semantically                        │
│    ├─ Dialogue act classification → "command"                    │
│    ├─ Intent: "draft_document"                                   │
│    └─ Output: DialogueMove(type="command",                       │
│                             content="I need to draft an NDA",    │
│                             metadata={intent, entities, ...})    │
│                                                                   │
│  NO PLAN CREATION HERE (interpretation is syntactic/semantic)    │
└───────────────────────────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────────────────────────┐
│ PHASE 2: INTEGRATE (Accommodation + State Updates)               │
│                                                                   │
│  Integration Rules (integration_rules.py):                       │
│                                                                   │
│  1. integrate_command rule:                                      │
│     ├─ Detects: DialogueMove.type == "command"                  │
│     ├─ Checks metadata for intent/task info                     │
│     └─ Triggers: accommodate_task()                             │
│                                                                   │
│  2. accommodate_task():                                          │
│     ├─ Reads: move.metadata["intent"] or move.content           │
│     ├─ Task Classification (LLM or metadata):                   │
│     │    "draft_document" + "NDA" → NDA_TASK                    │
│     ├─ Creates Plan:                                             │
│     │    Plan(type="nda_drafting",                              │
│     │         subplans=[                                         │
│     │           findout(parties),                                │
│     │           findout(nda_type),                               │
│     │           findout(effective_date),                         │
│     │           findout(duration),                               │
│     │           findout(governing_law)                           │
│     │         ])                                                 │
│     ├─ Adds to: state.private.plan                              │
│     ├─ Pushes first question to: state.shared.qud               │
│     └─ Sets: state.control.next_speaker = "system"              │
│                                                                   │
│  3. Track move in history                                        │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────────────────────────┐
│ PHASE 3: SELECT (Choose Next Action)                             │
│                                                                   │
│  Selection Rules (selection_rules.py):                           │
│    ├─ Check agenda (empty)                                       │
│    ├─ Execute active plan (select_plan_driven_question):        │
│    │    ├─ Get first active findout subplan                     │
│    │    ├─ Create ask move with question: WhQuestion(parties)   │
│    │    ├─ Add to agenda                                         │
│    │    └─ Mark subplan as executed                             │
│    └─ Output: DialogueMove(type="ask",                           │
│                             content=WhQuestion(variable="parties",│
│                                                predicate="legal_entities"))│
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────────────────────────┐
│ PHASE 4: GENERATE (NLG with Plan Context)                        │
│                                                                   │
│  Generation Rules (generation_rules.py):                         │
│                                                                   │
│  1. _generate_question_text():                                   │
│     ├─ Checks for active plan: _get_active_plan(state)          │
│     ├─ Plan type: "nda_drafting"                                 │
│     ├─ Question type: WhQuestion(parties, legal_entities)       │
│     └─ Uses NDA-specific template:                              │
│                                                                   │
│        "Let's start with the parties. Who are the                │
│         organizations entering into this NDA?"                   │
│                                                                   │
│  Alternative: LLM-based generation                               │
│     ├─ Prompt includes plan context                             │
│     ├─ "Generate question for NDA parties (step 1 of 5)"        │
│     └─ More natural, adaptive responses                          │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
        │
        ▼
System Response: "Let's start with the parties. Who are the
                  organizations entering into this NDA?"
```

---

## Key Design Principles

### 1. NLU Does Interpretation (Not Keywords!)

**Current**: NLU engine already does this well
```python
# nlu_engine.py
def interpret(utterance, speaker, state):
    # LLM-based dialogue act classification
    act = self.classifier.classify(utterance)

    # Create move with rich metadata
    move = DialogueMove(
        type=act.dialogue_act,      # "command", "question", "answer"
        content=utterance,           # Full text
        speaker=speaker,
        metadata={
            "intent": act.intent,    # "draft_document", "ask_question"
            "confidence": act.confidence,
            "entities": act.entities,
            "task_type": act.task_type  # Can include "NDA"
        }
    )
    return [move]
```

**Don't Regress**: No keyword matching in interpretation!

### 2. Integration Does Accommodation (Task Understanding)

**New**: Move ALL accommodation logic to integration phase

```python
# integration_rules.py

def create_integration_rules():
    return [
        UpdateRule(
            name="accommodate_command",
            preconditions=_is_command_or_request_move,
            effects=_accommodate_task,
            priority=13,  # Highest - before other integrations
            rule_type="integration"
        ),
        # ... other integration rules
    ]

def _is_command_or_request_move(state):
    """Check for command or request moves (from NLU or rules)."""
    move = state.private.beliefs.get("_temp_move")
    return isinstance(move, DialogueMove) and \
           move.move_type in ["command", "request"]

def _accommodate_task(state):
    """Accommodate user task by creating appropriate plan.

    This is THE RIGHT PLACE for task accommodation per Larsson.
    Uses NLU metadata or task classification to infer user's goal.
    """
    move = state.private.beliefs.get("_temp_move")
    new_state = state.clone()

    # Option 1: Use NLU metadata (if available)
    task_type = move.metadata.get("task_type")
    intent = move.metadata.get("intent")

    # Option 2: Re-classify with task classifier (if needed)
    if not task_type:
        classifier = get_task_classifier()
        result = classifier.classify(move.content)
        task_type = result.task_type

    # Dispatch to task-specific accommodation
    if task_type == "DRAFT_DOCUMENT":
        doc_type = _extract_document_type(move, intent)

        if doc_type == "NDA":
            plan = _create_nda_plan()
            new_state.private.plan.append(plan)

            # Push first question to QUD
            if plan.subplans:
                first_question = plan.subplans[0].content
                new_state.shared.push_qud(first_question)

        elif doc_type == "CONTRACT":
            # Future: other document types
            pass

    # Track move and set next speaker
    new_state.shared.last_moves.append(move)
    new_state.control.next_speaker = new_state.agent_id

    return new_state
```

### 3. NLG Uses Plan Context (Smart Generation)

**Enhanced**: Plan-aware generation

```python
# generation_rules.py

def _generate_question_text(state):
    """Generate question text with plan awareness."""
    move = state.private.beliefs.get("_temp_generate_move")
    question = move.content

    # Get active plan context
    active_plan = _get_active_plan(state)

    if active_plan:
        # Plan-driven generation
        if active_plan.plan_type == "nda_drafting":
            return _generate_nda_question(question, active_plan, state)
        elif active_plan.plan_type == "contract_drafting":
            return _generate_contract_question(question, active_plan, state)

    # Fallback: generic generation
    return _generate_generic_question(question)

def _generate_nda_question(question, plan, state):
    """Generate NDA-specific question with context."""

    # Calculate progress
    completed = sum(1 for sp in plan.subplans if sp.status == "completed")
    total = len(plan.subplans)

    # Question-specific templates
    if isinstance(question, WhQuestion):
        if question.predicate == "legal_entities":
            prefix = "Let's start with the basics." if completed == 0 else ""
            return f"{prefix} Who are the organizations entering into this NDA?".strip()

        elif question.predicate == "date":
            return f"What effective date should we use for this agreement? (Step {completed+1} of {total})"

        elif question.predicate == "time_period":
            return f"How long should the confidentiality obligations last? Common periods are 2-5 years."

    elif isinstance(question, AltQuestion):
        if "mutual" in question.alternatives:
            return "Will this be a mutual NDA (both parties share confidential info) or one-way?"

        elif "California" in question.alternatives:
            return "Which state's laws should govern this agreement - California or Delaware?"

    # Fallback
    return f"Question: {question}"

def _get_active_plan(state):
    """Get currently active plan, if any."""
    for plan in state.private.plan:
        if plan.is_active():
            return plan
    return None
```

---

## Implementation Plan (REVISED)

### Phase 1: Move Accommodation to Integration ⭐

**Goal**: Fix the core architectural issue

**Tasks**:

1. **Keep NLU as-is** (it's already good!)
   - No changes to `nlu_engine.py` interpretation
   - Already creates command/request moves with metadata

2. **Add accommodation to integration_rules.py**:
   ```python
   # Add new rule
   UpdateRule(
       name="accommodate_command",
       preconditions=_is_command_or_request_move,
       effects=_accommodate_task,
       priority=13
   )
   ```

3. **Implement _accommodate_task()**:
   - Read move.metadata for task info (from NLU)
   - Or use task classifier as fallback
   - Create plans based on task type
   - Push first question to QUD

4. **Move existing accommodation logic**:
   - Copy `_create_nda_plan()` from interpretation_rules.py
   - Adapt to work in integration context
   - Keep task classifier usage

5. **Update integrate_request/integrate_command**:
   - Check if accommodation already created plan
   - Coordinate with accommodate_command rule

**Test**: NLU interpretation → command move → accommodation → plan creation

---

### Phase 2: Enhance NLG with Plan Context

**Goal**: Generate natural, context-aware responses

**Tasks**:

1. **Add plan context helpers**:
   - `_get_active_plan(state)` → returns active plan or None
   - `_get_plan_progress(plan)` → (completed, total)

2. **Update _generate_question_text()**:
   - Check for active plan
   - Dispatch to plan-specific generators
   - Fallback to generic if no plan

3. **Implement NDA-specific templates**:
   - Template for each question type
   - Include progress indicators
   - Natural, conversational tone

4. **Optional: LLM-based NLG**:
   - Use Claude for generation (not just templates)
   - Prompt includes plan context
   - More adaptive, natural responses

**Test**: Plan-driven questions generate appropriate templates

---

### Phase 3: Clean Up and Document

**Goal**: Remove old code, update docs

**Tasks**:

1. **Remove accommodation from interpretation_rules.py**:
   - Delete `accommodate_nda_task` rule
   - Delete `_is_nda_request()` function
   - Delete `_create_nda_plan()` (moved to integration)
   - Remove task classifier from interpretation

2. **Update documentation**:
   - Mark ARCHITECTURE_ISSUE_SUMMARY.md as resolved
   - Update CLAUDE.md with principle: "Accommodation in Integration"
   - Document NLU → IBDM → NLG pipeline

3. **Add architectural tests**:
   - Test that accommodation happens in integration
   - Test that NLU → accommodation → plan creation works
   - Test that NLG uses plan context

**Test**: Full pipeline test passes

---

### Phase 4: Integration Testing

**Goal**: Verify complete workflow

**Tasks**:

1. **Complete NDA workflow test**:
   - User: "I need to draft an NDA"
   - System asks 5 questions with context
   - User provides answers
   - System generates final confirmation

2. **Test with NLU engine**:
   - Real LLM interpretation
   - Verify metadata propagation
   - Verify accommodation triggers

3. **Manual demo testing**:
   - Run interactive demo
   - Test various phrasings
   - Verify natural conversation flow

**Test**: Demo shows professional, context-aware dialogue

---

## Expected Behavior (After Implementation)

### Example Conversation

```
User: I need to draft an NDA

[INTERPRET (NLU)]
→ DialogueMove(type="command", content="...",
               metadata={intent: "draft_document", task_type: "NDA"})

[INTEGRATE (Accommodation)]
→ Creates NDA plan with 5 findout subplans
→ Pushes WhQuestion(parties, legal_entities) to QUD
→ Sets next_speaker = system

[SELECT]
→ Executes first plan step
→ DialogueMove(type="ask", content=WhQuestion(parties, ...))

[GENERATE (NLG with context)]
→ Uses NDA template + plan context
→ "Let's start with the basics. Who are the organizations
    entering into this NDA?"

System: Let's start with the basics. Who are the organizations
        entering into this NDA?

User: Acme Corp and Beta Industries

[INTERPRET (NLU)]
→ DialogueMove(type="answer", content=Answer(...))

[INTEGRATE]
→ Pops question from QUD
→ Adds commitment: parties = "Acme Corp and Beta Industries"
→ Marks plan step 1 as completed

[SELECT]
→ Executes next plan step
→ DialogueMove(type="ask", content=AltQuestion([mutual, one-way]))

[GENERATE (NLG with context)]
→ "Will this be a mutual NDA (both parties share confidential
    info) or one-way? (Step 2 of 5)"

System: Will this be a mutual NDA (both parties share confidential
        info) or one-way? (Step 2 of 5)

... continues through all 5 questions ...

System: Perfect! I have all the information needed to draft your
        NDA between Acme Corp and Beta Industries. Should I generate
        the document now?
```

---

## Why This Design is Correct

### 1. Follows Larsson's Framework
- **Interpretation**: Syntactic/semantic analysis (NLU does this)
- **Integration**: Pragmatic understanding, accommodation (plan creation HERE)
- **Selection**: Strategic choice (what to do next)
- **Generation**: Linguistic realization (context-aware)

### 2. Uses NLU Properly
- Leverages LLM for semantic understanding
- Creates rich moves with metadata
- No regression to keyword matching

### 3. Enables Both Approaches
- NLU-based interpretation (production)
- Rule-based interpretation (development/testing)
- Both trigger same accommodation logic

### 4. Scalable
- Easy to add new task types (contracts, emails, reports)
- Easy to add new document types (NDAs, SOWs, MSAs)
- Accommodation logic centralized in integration

### 5. Natural Conversation
- Plan-aware NLG
- Progress indicators
- Context-sensitive templates
- Optional LLM-based generation

---

## Files to Modify

### Core Changes

1. **`src/ibdm/rules/integration_rules.py`** (MAIN WORK)
   - Add `accommodate_command` rule
   - Add `_accommodate_task()` function
   - Add `_create_nda_plan()` (moved from interpretation)
   - Add `_extract_document_type()` helper

2. **`src/ibdm/rules/generation_rules.py`** (ENHANCE)
   - Add `_get_active_plan()` helper
   - Update `_generate_question_text()` for plan awareness
   - Add `_generate_nda_question()` templates
   - Add progress indicators

3. **`src/ibdm/rules/interpretation_rules.py`** (CLEAN UP)
   - Remove `accommodate_nda_task` rule
   - Remove task classifier usage
   - Remove plan creation logic

### No Changes Needed

- **`src/ibdm/engine/nlu_engine.py`** - Already perfect!
- **`src/ibdm/burr_integration/`** - Already supports this flow
- **`src/ibdm/nlu/`** - NLU components are good

---

## Success Criteria

- ✅ NLU interprets utterances (no keyword matching)
- ✅ Integration creates plans for commands/requests
- ✅ Plans work with NLU-created moves
- ✅ NLG generates context-aware responses
- ✅ Demo shows natural NDA conversation
- ✅ All tests pass
- ✅ No architectural regressions

---

## References

- Larsson, S. (2002). *Issue-based Dialogue Management*
- Current NLU implementation: `src/ibdm/engine/nlu_engine.py`
- Current IBDM rules: `src/ibdm/rules/*.py`
- Demo: `demos/03_nlu_integration_interactive.py`
