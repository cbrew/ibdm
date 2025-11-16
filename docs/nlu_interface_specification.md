# NLU Interface Specification for IBiS Dialogue Management

**Status**: ✅ CURRENT
**Purpose**: Specification of NLU requirements for IBiS1-4 dialogue management
**Date**: 2025-11-16

---

## Overview

`src/ibdm/nlu/base_nlu_service.py` defines **BaseNLUService**, an abstract interface capturing all NLU requirements from Larsson's IBiS dialogue management variants.

**Purpose**:
1. **Document** what NLU must provide for each IBiS level
2. **Specify** the contract between NLU and dialogue management
3. **Enable** dialogue manager testing with mock NLU implementations
4. **Guide** future NLU enhancements

---

## Design Principle

> **Dialogue Management Drives NLU Design**

The IBiS variants define **what the dialogue manager needs** from NLU. This interface makes those requirements explicit and testable.

**Strategy**: Build and test IBiS dialogue managers first, using this interface. Then enhance NLU to meet higher IBiS levels.

---

## Interface Structure

### Core Types

**Data Structures** (defined in base_nlu_service.py):
- `NLUConfidence` - Perception and understanding confidence scores (IBiS2)
- `AmbiguityInfo` - Ambiguity detection results (IBiS2)
- `ExtractedFact` - Single fact from utterance (IBiS3)
- `MultiFact` - Multiple facts from single utterance (IBiS3)
- `ActionRequest` - Detected action request (IBiS4)
- `UserPreference` - Extracted preference or constraint (IBiS4)

### Method Organization by IBiS Level

```python
class BaseNLUService(ABC):
    # IBiS1: Basic dialogue (REQUIRED)
    classify_dialogue_act()    # "ask", "answer", "request", etc.
    parse_question()           # → Question object
    parse_answer()             # → Answer object
    extract_entities()         # → ORGANIZATION, DATE, etc.

    # IBiS2: Grounding (OPTIONAL)
    get_confidence()           # → NLUConfidence
    detect_ambiguity()         # → AmbiguityInfo
    recognize_icm()            # → ICM move type

    # IBiS3: Accommodation (OPTIONAL)
    extract_multiple_facts()   # → MultiFact (primary + volunteer)
    match_answer_to_question() # → resolves(answer, question)
    detect_volunteer_information() # → List[ExtractedFact]

    # IBiS4: Actions (OPTIONAL)
    detect_action_request()    # → ActionRequest
    extract_preferences()      # → List[UserPreference]
    parse_comparison()         # → comparison dimension

    # Main entry point
    process()                  # → DialogueMove
```

---

## IBiS Level Requirements

### IBiS1: Foundation (REQUIRED)

**What dialogue manager needs**:
- Classify utterances into dialogue acts
- Parse questions into structured Question objects
- Parse answers into Answer objects with extracted entities
- Extract named entities (ORGANIZATION, DATE, PERSON, etc.)

**Methods**:
```python
# All IBiS1 methods are @abstractmethod - MUST be implemented
classify_dialogue_act(utterance, state) → (act_type, confidence)
parse_question(utterance, state) → (Question | None, confidence)
parse_answer(utterance, state) → (Answer | None, confidence)
extract_entities(utterance, state) → List[entity_dict]
process(utterance, speaker, state) → DialogueMove
```

**Example Usage**:
```python
# User: "What are the parties?"
act, conf = nlu.classify_dialogue_act(utterance, state)
# act = "ask", conf = 0.95

question, conf = nlu.parse_question(utterance, state)
# question = WhQuestion(predicate="parties", variable="?x")
```

### IBiS2: Grounding (OPTIONAL)

**What dialogue manager needs**:
- Confidence scores to select grounding strategy
- Ambiguity detection to generate clarifications
- ICM move recognition for feedback processing

**Methods**:
```python
# All IBiS2 methods have default implementations - override to support IBiS2
get_confidence(utterance, state) → NLUConfidence
detect_ambiguity(utterance, state) → AmbiguityInfo
recognize_icm(utterance, state) → (icm_type | None, confidence)
```

**Example Usage**:
```python
# User: [garbled speech]
conf = nlu.get_confidence(utterance, state)
if conf.overall < 0.6:
    # Generate: "Sorry, I didn't hear that. Could you repeat?"
    pass
```

**Grounding Strategy Selection**:
- `confidence > 0.9` → Optimistic (assume grounded)
- `0.6 ≤ confidence ≤ 0.9` → Cautious (request confirmation)
- `confidence < 0.6` → Pessimistic (request repetition)

### IBiS3: Accommodation (OPTIONAL)

**What dialogue manager needs**:
- Extract multiple facts from single utterance
- Match answers to questions (including unasked questions)
- Detect volunteer information

**Methods**:
```python
# All IBiS3 methods have default implementations - override to support IBiS3
extract_multiple_facts(utterance, state) → MultiFact
match_answer_to_question(answer, question, state) → confidence_score
detect_volunteer_information(utterance, state) → List[ExtractedFact]
```

**Example Usage**:
```python
# System: "What are the parties?"
# User: "Acme and Smith, effective January 1, 2025"

mf = nlu.extract_multiple_facts(utterance, state)
# mf.primary_fact = ExtractedFact(predicate="parties", ...)
# mf.volunteer_facts = [ExtractedFact(predicate="effective_date", ...)]

# Dialogue manager can now:
# 1. Answer current question (parties)
# 2. Remove effective_date from private.issues (already answered)
# 3. Skip asking about effective_date later
```

**Critical Capability**: This is what enables natural dialogue where users don't have to wait for each question.

### IBiS4: Actions (OPTIONAL)

**What dialogue manager needs**:
- Detect action requests vs. information requests
- Extract preferences and constraints
- Parse comparative questions for negotiation

**Methods**:
```python
# All IBiS4 methods have default implementations - override to support IBiS4
detect_action_request(utterance, state) → (ActionRequest | None, confidence)
extract_preferences(utterance, state) → List[UserPreference]
parse_comparison(utterance, alternatives, state) → (dimension, alts)
```

**Example Usage**:
```python
# User: "Book the Paris hotel"
req, conf = nlu.detect_action_request(utterance, state)
# req = ActionRequest(action="book_hotel", parameters={"location": "Paris"})

# User: "I want a hotel under $200, close to Eiffel Tower"
prefs = nlu.extract_preferences(utterance, state)
# [UserPreference(dimension="max_price", value=200, is_hard_constraint=True),
#  UserPreference(dimension="proximity", value="Eiffel Tower", is_hard_constraint=False)]
```

---

## Implementation Strategy

### Phase 1: Current State (IBiS1 Complete)

**Status**: ✅ Current `NLUEngine` implements IBiS1 requirements

**Capabilities**:
- Dialogue act classification ✅
- Question parsing ✅
- Answer parsing ✅
- Entity extraction ✅

**Adapter Approach**: Create adapter that wraps current `NLUEngine` and implements `BaseNLUService`:

```python
class NLUEngineAdapter(BaseNLUService):
    def __init__(self, nlu_engine: NLUEngine):
        self.engine = nlu_engine

    def classify_dialogue_act(self, utterance, state):
        result, _ = self.engine.process(utterance, "user", state, context)
        return result.dialogue_act, result.confidence

    # ... implement other IBiS1 methods using NLUEngine

    def get_supported_ibis_level(self):
        return "IBiS1"
```

### Phase 2: Add IBiS3 Capabilities (Next Priority)

**Goal**: Enable accommodation (Rules 4.1-4.2)

**Enhancements Needed**:
1. Enhance prompts to extract multiple facts from single utterance
2. Implement semantic matching for `match_answer_to_question()`
3. Detect volunteer information by comparing to `private.issues`

**Why IBiS3 before IBiS2?**:
- Bigger UX improvement (natural dialogue)
- LLMs naturally good at multi-fact extraction
- Needed for Week 4+ accommodation tasks

### Phase 3: Add IBiS2 Capabilities (Future)

**Goal**: Robust grounding and error handling

**Enhancements Needed**:
1. Report confidence scores from LLM
2. Implement ambiguity detection
3. Recognize ICM moves in user utterances

### Phase 4: Add IBiS4 Capabilities (Future)

**Goal**: Action-oriented and negotiative dialogue

**Enhancements Needed**:
1. Distinguish action requests from information requests
2. Extract user preferences and constraints
3. Parse comparative questions

---

## Testing Strategy

### Unit Testing with Mocks

**Benefit**: Test dialogue managers WITHOUT implementing full NLU

```python
class MockNLUService(BaseNLUService):
    """Mock NLU for testing dialogue management."""

    def classify_dialogue_act(self, utterance, state):
        # Return predetermined dialogue acts for test scenarios
        if "what" in utterance.lower():
            return "ask", 1.0
        if "acme" in utterance.lower():
            return "answer", 1.0
        return "other", 0.5

    # ... implement other methods with test-friendly logic
```

**Usage**:
```python
def test_ibis3_volunteer_information():
    mock_nlu = MockNLUService()

    # Configure mock to return multi-fact result
    mock_nlu.set_response(
        utterance="Acme and Smith, effective Jan 1",
        multi_fact=MultiFact(
            primary_fact=ExtractedFact(predicate="parties", ...),
            volunteer_facts=[ExtractedFact(predicate="effective_date", ...)]
        )
    )

    # Test dialogue manager with mock NLU
    # Verify Rule 4.1 (IssueAccommodation) works correctly
```

### Integration Testing Levels

**Level 1: IBiS1 Only**
- Test basic dialogue flow
- QUD management
- Plan progression

**Level 2: IBiS1 + IBiS3**
- Test volunteer information handling
- Multi-fact extraction
- Answer-question matching

**Level 3: Full IBiS1-4**
- Test all capabilities
- Complex scenarios

---

## Migration Path

### Step 1: Create Adapter (Immediate)

Wrap current `NLUEngine` in `BaseNLUService` adapter:

```python
# src/ibdm/nlu/nlu_service_adapter.py
class NLUServiceAdapter(BaseNLUService):
    """Adapter wrapping current NLUEngine as BaseNLUService."""
    # Implements IBiS1 methods using existing NLUEngine
```

### Step 2: Use in Dialogue Manager (Week 4)

Update dialogue manager to use `BaseNLUService` interface:

```python
# Before
engine = NLUEngine(config)
result, context = engine.process(utterance, speaker, state, context)

# After
nlu_service = NLUServiceAdapter(NLUEngine(config))
move = nlu_service.process(utterance, speaker, state)
```

### Step 3: Enhance for IBiS3 (Week 5+)

Add IBiS3 methods to adapter:

```python
class IBiS3NLUService(NLUServiceAdapter):
    """NLU service with IBiS3 accommodation support."""

    def extract_multiple_facts(self, utterance, state):
        # Use enhanced prompts to extract multiple facts
        # LLM naturally good at this!
        pass

    def get_supported_ibis_level(self):
        return "IBiS3"
```

---

## Benefits

### 1. Clear Specification
- Documents exactly what NLU must provide
- Makes IBiS requirements explicit
- Enables dialogue manager development without full NLU

### 2. Testability
- Mock implementations for unit testing
- Progressive integration testing (IBiS1 → IBiS2 → IBiS3 → IBiS4)
- Validate dialogue managers independently

### 3. Flexibility
- Multiple NLU implementations can satisfy same interface
- Easy to compare different NLU approaches
- Can mix levels (e.g., IBiS1 + IBiS3 without IBiS2)

### 4. Documentation
- Type hints clarify data structures
- Docstrings explain requirements
- Examples show usage patterns

---

## Related Documents

- **Analysis**: `reports/ibis-nlu-requirements-analysis.md` - Detailed requirements breakdown
- **Implementation**: `src/ibdm/nlu/base_nlu_service.py` - Abstract interface
- **Current NLU**: `src/ibdm/nlu/nlu_engine.py` - Existing IBiS1 implementation
- **Roadmap**: `IBIS_VARIANTS_PRIORITY.md` - IBiS implementation priorities

---

## Summary

**BaseNLUService** provides:
- ✅ Complete specification of IBiS NLU requirements
- ✅ Abstract interface for multiple implementations
- ✅ Clear upgrade path (IBiS1 → IBiS2 → IBiS3 → IBiS4)
- ✅ Testing support via mock implementations
- ✅ Documentation of dialogue manager needs

**Next Steps**:
1. Create adapter for current `NLUEngine` (IBiS1)
2. Use interface in dialogue manager
3. Enhance to IBiS3 when implementing accommodation (Week 5+)
4. Add IBiS2 for grounding (later)
5. Add IBiS4 for actions (future)
