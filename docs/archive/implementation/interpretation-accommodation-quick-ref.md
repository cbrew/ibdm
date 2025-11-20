# IBDM Architecture Issue: Quick Reference

## The Core Problem

**Task accommodation (plan creation) is happening in the INTERPRETATION phase when it should happen in the INTEGRATION phase.**

This violates Larsson's IBDM framework and makes the mechanism unreachable from the NLU engine.

---

## Larsson's Four-Phase Control Loop

```
┌──────────────────────────────────────────────────────────────┐
│ 1. INTERPRET: Utterance → Dialogue Move (syntactic)         │
│    Example: "I need an NDA" → DialogueMove(type="request")  │
├──────────────────────────────────────────────────────────────┤
│ 2. INTEGRATE: Move + State → Updated State (semantic)       │
│    ← TASK ACCOMMODATION HAPPENS HERE                        │
│    Example: request → infer plan → create subplans          │
├──────────────────────────────────────────────────────────────┤
│ 3. SELECT: State → System Action (strategic)                │
│    Example: "What are the parties?" (first question)        │
├──────────────────────────────────────────────────────────────┤
│ 4. GENERATE: Move → Utterance (linguistic)                  │
│    Example: DialogueMove → "What are the parties?"          │
└──────────────────────────────────────────────────────────────┘
```

---

## What Should Happen in Each Phase

### INTERPRETATION (Syntactic - Keep it simple)
- Convert text to structured dialogue moves
- Classify: Is this a question? Answer? Request?
- Extract semantic content (for questions: structure and variables)
- **Should NOT** infer plans or what information is needed

### INTEGRATION (Semantic - Where accommodation belongs)
- Apply moves to update information state
- Manage QUD stack (push questions, pop answers)
- **ACCOMMODATE**: When request move → infer task → create plan
- Push first question to QUD
- Update commitments and history

### SELECTION (Strategic - No changes needed)
- Decide what system should do next
- Already works correctly with accommodated plans

### GENERATION (Linguistic - No changes needed)
- Convert selected move to text
- Already works correctly

---

## Current Problem in Code

### Problem 1: Misplaced Task Accommodation

**File**: `src/ibdm/rules/interpretation_rules.py` (line 43-49)

```python
# WRONG: This is in interpretation rules
UpdateRule(
    name="accommodate_nda_task",  # ← Accommodation in interpretation!
    preconditions=_is_nda_request,
    effects=_create_nda_plan,      # ← Creates plan here
    priority=12,
    rule_type="interpretation",    # ← WRONG phase!
)
```

**Why this is wrong**:
- `_create_nda_plan` uses expensive LLM-based task classification
- It creates both a move AND a plan (mixes two phases)
- It's in the wrong place conceptually

### Problem 2: NLU Engine Bypasses Everything

**File**: `src/ibdm/engine/nlu_engine.py` (line 133-155)

```python
def interpret(self, utterance: str, speaker: str, state: InformationState) -> list[DialogueMove]:
    # Directly interprets using NLU
    # Completely bypasses interpretation rules
    # No task accommodation happens!
    ...
```

**Why this is a problem**:
- When using NLU engine, the interpretation rules never run
- So the `_create_nda_plan` accommodation logic is unreachable
- NLU engine has no accommodation mechanism

---

## The Fix (High Level)

### Step 1: Move Task Accommodation to Integration Rules
```python
# In integration_rules.py

UpdateRule(
    name="accommodate_request",     # ← Now in integration!
    preconditions=_is_request_move, # ← Checks for request move
    effects=_accommodate_request_task,
    priority=11,
    rule_type="integration",        # ← CORRECT phase!
)
```

### Step 2: Simplify Interpretation Rules
```python
# In interpretation_rules.py

UpdateRule(
    name="interpret_request",
    preconditions=_is_request,      # ← Simple keyword matching
    effects=_create_request_move,   # ← Just creates move, no plan
    rule_type="interpretation",
)

def _create_request_move(state):
    # Create simple request move with just the utterance text
    # Don't try to infer the plan
    return DialogueMove(
        move_type="request",
        content=utterance,  # Just store text
        speaker=speaker,
    )
```

### Step 3: Update NLU Engine
```python
# In nlu_engine.py

def interpret(self, utterance, speaker, state):
    # When interpreting a request, just create a basic move
    if dialogue_act == DialogueActType.REQUEST:
        return [DialogueMove(
            move_type="request",
            content=utterance,  # No plan creation here!
            speaker=speaker,
        )]
    # ... handle other acts ...
    
    # The base class's integrate() method will apply 
    # accommodation rules, which now work for both paths!
```

### Step 4: Implement Task Accommodation in Integration Rules
```python
# In integration_rules.py

def _accommodate_request_task(state):
    move = state.private.beliefs.get("_temp_move")
    utterance = str(move.content)
    
    # Now it's safe to use expensive task classification
    # We're in the integration phase, not interpretation
    classifier = _get_task_classifier()
    task_result = classifier.classify(utterance)
    
    # Create appropriate plan based on task type
    if task_result.task_type == TaskType.DRAFT_DOCUMENT:
        plan = _create_accommodation_for_task(task_result)
        state.private.plan.append(plan)
        
        # Push first question to QUD
        if plan.subplans:
            first_q = plan.subplans[0].content
            state.shared.push_qud(first_q)
    
    return state
```

---

## Benefits of This Fix

✅ **Conceptually Sound**: Respects Larsson's phase boundaries  
✅ **Reusable**: Task accommodation works for both rule and NLU interpretation  
✅ **Maintainable**: Plan creation logic is in one place (integration rules)  
✅ **Extensible**: Adding new task types just requires new integration rules  
✅ **Debuggable**: Clear phase boundaries make debugging easier  

---

## Files to Modify

1. **`src/ibdm/rules/interpretation_rules.py`**
   - Remove `accommodate_nda_task` rule
   - Add `interpret_request` rule (simple)
   - Add `_create_request_move` function

2. **`src/ibdm/rules/integration_rules.py`**
   - Add `accommodate_request` rule
   - Add `_accommodate_request_task` function
   - Add `_create_nda_accommodation` function (moved from interpretation_rules.py)

3. **`src/ibdm/engine/nlu_engine.py`**
   - Remove any task-specific logic from `_create_moves_from_act`
   - For request moves, just create basic move without planning

---

## Reading the Full Analysis

For complete details, context, and code examples, see:
`/home/user/ibdm/docs/architecture_interpretation_accommodation.md`

This document includes:
- Full explanation of Larsson's framework
- Detailed analysis of current problems
- Complete before/after code examples
- Phase-by-phase implementation guide
- Benefits and references
