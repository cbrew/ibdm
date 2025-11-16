# IBiS Variants as NLU Requirements Specification

**Date**: 2025-11-16
**Author**: Analysis of Larsson (2002) dialogue management variants
**Key Insight**: Each IBiS variant defines **what the NLU must produce** for dialogue management to work

---

## Executive Summary

The progression IBiS1 → IBiS2 → IBiS3 → IBiS4 is **not just** about dialogue management complexity - it's fundamentally about **what information the NLU must extract** from user utterances.

**Core Insight**:
- **Dialogue Manager Needs** → **NLU Requirements**
- More sophisticated dialogue management requires richer NLU output
- Each IBiS variant adds new NLU capabilities

---

## Part 1: IBiS1 - Core NLU Requirements

**Dialogue Manager Capability**: Basic question-answering dialogue
**Status**: ✅ Implemented

### What IBiS1 Needs from NLU

#### 1. Dialogue Act Classification
**Requirement**: Classify utterances into move types

**Move Types** (Section 2.4.1):
- `ask` - User asks question
- `answer` - User provides answer
- `request` - User requests task/service
- `assert` - User makes statement
- `greet` - Conversation opening
- `quit` - Conversation closing

**NLU Output**:
```python
DialogueMove(
    type="answer",  # Dialogue act
    content="Acme Corp and Smith Inc",  # Extracted content
    speaker="user"
)
```

**Challenge**: Distinguish between:
- "What are the parties?" (ask)
- "Acme and Smith" (answer)
- "I need an NDA" (request)
- "The parties are Acme and Smith" (assert)

#### 2. Question Understanding
**Requirement**: Parse questions into structured Question objects

**Question Types** (Section 2.4.2):
- `WhQuestion` - Wh-questions (what, who, when, where, why, how)
- `YNQuestion` - Yes/no questions
- `AltQuestion` - Alternative questions ("A or B?")

**NLU Output**:
```python
WhQuestion(
    predicate="parties",
    variable="?x",
    sort="organization"
)
```

**Challenge**: Extract semantic structure:
- "What are the parties?" → WhQuestion(predicate="parties")
- "When is the effective date?" → WhQuestion(predicate="effective_date", sort="date")
- "Is the term 5 years?" → YNQuestion(proposition="term(?x) = 5 years")

#### 3. Answer Content Extraction
**Requirement**: Extract structured content from answers

**Entity Types**:
- ORGANIZATION - "Acme Corp", "Smith Inc"
- DATE - "January 1, 2025", "2025-01-01"
- PERSON - "John Smith"
- LOCATION - "California", "Delaware"
- DURATION - "5 years", "12 months"

**NLU Output**:
```python
Answer(
    content={
        "entities": [
            {"type": "ORGANIZATION", "value": "Acme Corp"},
            {"type": "ORGANIZATION", "value": "Smith Inc"}
        ]
    }
)
```

**Challenge**: Normalize variants:
- "January 1, 2025" → "2025-01-01"
- "five years" → "5 years"
- "Acme Corporation" → "Acme Corp" (if same entity)

#### 4. Semantic Parsing
**Requirement**: Map natural language to domain predicates

**Example Mappings**:
- "parties to the agreement" → `parties(?x)`
- "effective date" → `effective_date(?x)`
- "governing law" → `governing_law(?x)`
- "confidential information" → `confidential_info(?x)`

**NLU Output**:
```python
# User: "What are the parties?"
WhQuestion(
    predicate="parties",  # Domain predicate
    variable="?x",
    sort="organization"
)
```

**Challenge**: Handle linguistic variations:
- "parties" = "parties to the agreement" = "contracting parties"
- All map to same domain predicate: `parties(?x)`

---

## Part 2: IBiS2 - Grounding & Perception Requirements

**Dialogue Manager Capability**: Detect and repair communication failures
**Status**: ⚠️ 60% implemented (basic only)

### What IBiS2 Adds to NLU

#### 5. Confidence Scores
**Requirement**: NLU must report uncertainty about its interpretations

**Confidence Types** (Section 3.6.7):
- **Perception Confidence**: How well was speech recognized?
- **Understanding Confidence**: How certain is the semantic interpretation?

**NLU Output**:
```python
DialogueMove(
    type="answer",
    content="Acme Corp",
    confidence={
        "perception": 0.45,  # Low - garbled speech
        "understanding": 0.85  # High - if heard correctly, meaning clear
    }
)
```

**Grounding Strategy Selection** (Section 3.5):
- Confidence > 0.9 → **Optimistic** (assume grounded)
- Confidence 0.6-0.9 → **Cautious** (request confirmation)
- Confidence < 0.6 → **Pessimistic** (request repetition)

**Example**:
```
User: [garbled speech, perception confidence: 0.4]
NLU: DialogueMove(content="...", confidence=0.4)
DM: Perception confidence too low
DM: Generate ICM move: "Sorry, I didn't hear that. Could you repeat?"
```

#### 6. Ambiguity Detection
**Requirement**: Identify when utterances are ambiguous

**Ambiguity Types**:
- **Lexical**: Word has multiple meanings ("bank" = financial institution or river edge)
- **Syntactic**: Parse ambiguity ("I saw the man with the telescope")
- **Semantic**: Unclear referent ("the contract" - which contract?)

**NLU Output**:
```python
DialogueMove(
    type="answer",
    content="the contract",  # Ambiguous reference
    ambiguous=True,
    interpretations=[
        {"content": "NDA between Acme and Smith"},
        {"content": "NDA between Acme and Jones"}
    ]
)
```

**Dialogue Manager Response**: Generate clarification question

#### 7. ICM Move Recognition
**Requirement**: Recognize Interactive Communication Management moves from user

**ICM Types** (Section 3.4):
- `icm:per*pos` - "Yes, I can hear you"
- `icm:per*neg` - "Sorry, I didn't hear you"
- `icm:und*pos` - "Yes, that's correct"
- `icm:und*neg` - "No, I said Paris, not Harris"

**NLU Output**:
```python
# User: "Yes, that's correct"
DialogueMove(
    type="icm:und*pos",  # Positive understanding feedback
    refers_to=previous_move  # What they're confirming
)
```

**Challenge**: Distinguish between:
- "Yes" as confirmation (ICM)
- "Yes" as answer to yes/no question (answer)

---

## Part 3: IBiS3 - Accommodation Requirements

**Dialogue Manager Capability**: Handle volunteer information, multi-part utterances
**Status**: 🔧 30% implemented (foundation only)

### What IBiS3 Adds to NLU

#### 8. Multi-Fact Extraction
**Requirement**: Extract **multiple** pieces of information from single utterance

**Example**:
```
System: "What are the parties?"
User: "Acme and Smith, effective January 1, 2025, governed by California law"
```

**NLU Must Produce**:
```python
[
    Answer(
        content={"parties": ["Acme Corp", "Smith Inc"]},
        resolves=WhQuestion(predicate="parties")
    ),
    Answer(
        content={"effective_date": "2025-01-01"},
        resolves=WhQuestion(predicate="effective_date")  # VOLUNTEER INFO
    ),
    Answer(
        content={"governing_law": "California"},
        resolves=WhQuestion(predicate="governing_law")  # VOLUNTEER INFO
    )
]
```

**Critical Capability**:
- Segment utterance into **multiple semantic facts**
- Associate each fact with potential question it answers
- Even if those questions haven't been asked yet!

#### 9. Answer-Question Matching
**Requirement**: Determine which question(s) an answer resolves

**Semantic Operation** (Section 2.4.3):
```python
def resolves(answer: Answer, question: Question) -> bool:
    """Does this answer resolve this question?"""
    # NLU must provide enough structure to enable this check
```

**NLU Must Enable**:
- Extract answer predicate: "January 1, 2025" → `effective_date(?x) = "2025-01-01"`
- Match to question predicate: `?effective_date` in question
- Check semantic compatibility: Date value for date question

**Example**:
```python
# User volunteers date
answer = Answer(content="January 1, 2025")

# NLU must extract enough info that DM can check:
resolves(answer, WhQuestion(predicate="effective_date")) → True
resolves(answer, WhQuestion(predicate="parties")) → False
```

#### 10. Implicit Question Detection
**Requirement**: Infer questions from context, even if not explicitly asked

**Example**:
```
User: "I need an NDA between Acme and Smith"
```

**NLU Should Extract**:
```python
Request(
    action="create_nda",
    volunteer_info={
        "parties": ["Acme Corp", "Smith Inc"]  # Implicit answer!
    }
)
```

**Challenge**: User provided answer to "What are the parties?" **without being asked**

**NLU Requirements**:
- Recognize embedded entities in requests
- Extract them as if they were answers
- Tag them as volunteer information

#### 11. Clarification Question Understanding
**Requirement**: Handle system-generated clarification questions

**Example Dialogue**:
```
System: "What are the parties?"
User: "Acme and someone else"  [Ambiguous]
System: "Who is the other party?"  [Clarification question - CQ]
User: "Smith Inc"  [Answer to CQ]
```

**NLU Must**:
- Recognize "Smith Inc" answers the **clarification question**
- Not the original question
- Provide enough context for `resolves(answer, CQ)` to work

---

## Part 4: IBiS4 - Action & Negotiation Requirements

**Dialogue Manager Capability**: Execute actions, negotiate alternatives
**Status**: 📋 10% (planned only)

### What IBiS4 Adds to NLU

#### 12. Action/Request Detection
**Requirement**: Recognize when user requests an action (not just information)

**Request Types** (Section 5.2):
- **Explicit**: "Book the Paris hotel"
- **Implicit**: "I want to go to Paris" (implies booking)

**NLU Output**:
```python
Request(
    action="book_hotel",
    parameters={
        "location": "Paris",
        "hotel_id": "paris_hotel"
    }
)
```

**vs. Information-Seeking**:
```python
# "Tell me about the Paris hotel" → WhQuestion, not Request
WhQuestion(predicate="hotel_info", parameters={"hotel": "paris_hotel"})
```

**Challenge**: Distinguish between:
- "Book hotel" (action request)
- "What hotels are available?" (information request)
- "I need a hotel" (implicit action request)

#### 13. Preference Expression Understanding
**Requirement**: Extract user preferences and constraints

**Example**:
```
User: "I want a hotel in Paris under $200, close to the Eiffel Tower"
```

**NLU Output**:
```python
Request(
    action="book_hotel",
    constraints={
        "location": "Paris",
        "max_price": 200,
        "proximity": {"landmark": "Eiffel Tower"}
    },
    preferences={
        "price": "minimize",
        "proximity_to_landmark": "maximize"
    }
)
```

**Preference Types**:
- **Hard Constraints**: "under $200" (must satisfy)
- **Soft Preferences**: "close to Eiffel Tower" (nice to have)
- **Priorities**: "price more important than location"

#### 14. Alternative Comparison Understanding
**Requirement**: Parse comparative statements about alternatives

**Example Dialogue**:
```
System: "Hotel A is $180, Hotel B is $150"
User: "Which is closer to the Eiffel Tower?"
```

**NLU Output**:
```python
WhQuestion(
    predicate="proximity",
    variable="?hotel",
    context="comparison",
    alternatives=["Hotel A", "Hotel B"],
    comparison_dimension="distance_to_landmark"
)
```

**Negotiation Moves**:
- "I prefer A" → Preference(alternative="Hotel A")
- "Is there anything cheaper?" → Request(constraint="price < current_min")
- "What about B?" → InformationRequest(subject="Hotel B")

#### 15. Implicit Action Accommodation
**Requirement**: Infer actions from conversational context

**Example**:
```
System: "Where would you like to go?"
User: "Paris"  [Implicit: book_flight(destination="Paris")]
```

**NLU Must**:
- Recognize "Paris" is answer to question
- ALSO recognize it implies action request (booking)
- Extract both meanings:

```python
[
    Answer(content="Paris"),  # Information-seeking
    Request(action="book_flight", parameters={"destination": "Paris"})  # Action
]
```

**Challenge**: Same utterance serves **dual purposes**

---

## Summary: NLU Requirements by IBiS Variant

| IBiS Variant | Core NLU Capability | Key Output |
|--------------|---------------------|------------|
| **IBiS1** | Dialogue act classification, question/answer parsing | `DialogueMove`, `Question`, `Answer` with entities |
| **IBiS2** | Confidence scores, ambiguity detection, ICM recognition | `confidence` field, `ambiguous` flag, ICM moves |
| **IBiS3** | Multi-fact extraction, answer-question matching, volunteer info | Multiple `Answer` objects per utterance, semantic matching |
| **IBiS4** | Action detection, preference extraction, alternative comparison | `Request` with constraints/preferences, comparison questions |

---

## Cascading Complexity

**Key Observation**: Requirements **accumulate**:

```
IBiS1: Baseline NLU
  ↓
IBiS2: + Confidence + Ambiguity Detection
  ↓
IBiS3: + Multi-Fact + Volunteer Info + Matching
  ↓
IBiS4: + Actions + Preferences + Negotiation
```

**Each level requires ALL previous capabilities plus new ones.**

---

## Implementation Implications

### 1. NLU Must Be Structured Output, Not Text

**Wrong**:
```python
# NLU returns string
nlu_output = "The user wants to know about parties"
```

**Right**:
```python
# NLU returns structured DialogueMove
nlu_output = DialogueMove(
    type="ask",
    content=WhQuestion(predicate="parties", variable="?x")
)
```

**Why**: Dialogue manager needs to:
- Match answers to questions (`resolves()`)
- Determine what to ask next (`domain.get_plan()`)
- Validate answers (`domain.validates()`)
- All require **structured data**, not text

### 2. NLU Must Support Semantic Operations

**Required Operations** (Section 2.4.3):
- `resolves(answer, question)` - Does answer resolve question?
- `combines(question, answer)` - Form proposition from Q+A
- `relevant(answer, question)` - Is answer relevant?
- `depends(q1, q2)` - Does q1 depend on q2?

**NLU Requirement**:
- Extract predicates from questions
- Extract predicates from answers
- Provide enough structure for semantic matching

### 3. LLMs Are Ideal for IBiS3 NLU

**Why LLMs Excel at IBiS3**:

**Multi-Fact Extraction**:
```
Prompt: "Extract all facts from: 'Acme and Smith, effective Jan 1, governed by CA law'"
LLM: [
  {"fact": "parties", "value": ["Acme", "Smith"]},
  {"fact": "effective_date", "value": "2025-01-01"},
  {"fact": "governing_law", "value": "California"}
]
```

**Answer-Question Matching**:
```
Prompt: "Does 'January 1, 2025' answer 'What is the effective date?'"
LLM: "Yes, it provides a date value for the effective_date predicate"
```

**Volunteer Information Detection**:
```
Prompt: "User said 'Acme and Smith' when asked about parties.
         Did they provide any extra information?"
LLM: "No extra information beyond party names"

vs.

Prompt: "User said 'Acme and Smith, effective Jan 1' when asked about parties.
         Did they provide any extra information?"
LLM: "Yes, they volunteered the effective date"
```

**LLMs are essentially pre-trained for IBiS3 capabilities!**

### 4. Current IBDM Status vs. Requirements

| Requirement | IBiS Level | Implementation Status |
|-------------|------------|----------------------|
| Dialogue act classification | IBiS1 | ✅ Implemented (LLM-based) |
| Question parsing | IBiS1 | ✅ Implemented |
| Answer extraction | IBiS1 | ✅ Implemented (entity extraction) |
| Semantic parsing | IBiS1 | ✅ Implemented (domain predicates) |
| Confidence scores | IBiS2 | ❌ Missing |
| Ambiguity detection | IBiS2 | ⚠️ Basic only |
| ICM move recognition | IBiS2 | ⚠️ Clarification only |
| Multi-fact extraction | IBiS3 | ❌ Missing |
| Answer-question matching | IBiS3 | ✅ `resolves()` implemented |
| Volunteer info detection | IBiS3 | ❌ Missing |
| Action detection | IBiS4 | ❌ Not started |
| Preference extraction | IBiS4 | ❌ Not started |

---

## Key Architectural Insight

**Traditional View**:
```
NLU → [black box] → Text interpretation
```

**Larsson's View**:
```
NLU → Structured DialogueMoves → Semantic Operations → Dialogue Management
        ↑                           ↑
     IBiS defines              IBiS defines
    what to extract           what to support
```

**The Dialogue Manager Drives NLU Design**:
- IBiS1: "Extract dialogue acts and entities"
- IBiS2: "Also report confidence and ambiguity"
- IBiS3: "Also segment multi-fact utterances and match to questions"
- IBiS4: "Also detect actions and extract preferences"

---

## Recommendation: Incremental NLU Development

**Phase 1: IBiS1 NLU** (✅ Complete)
- Dialogue act classification
- Question/answer parsing
- Entity extraction
- Domain predicate mapping

**Phase 2: IBiS3 NLU** (🎯 Next Priority)
- Multi-fact extraction from single utterance
- Volunteer information detection
- Enhanced answer-question matching
- **Why**: Biggest UX improvement, LLMs are naturally good at this

**Phase 3: IBiS2 NLU** (Future)
- Add confidence scores to all outputs
- Implement ambiguity detection
- Enhance ICM move recognition
- **Why**: Robustness improvement, requires ASR integration

**Phase 4: IBiS4 NLU** (Future)
- Action/request detection
- Preference extraction
- Alternative comparison
- **Why**: Advanced features, requires domain action definitions

---

## Bottom Line

**The IBiS variants are a requirements specification for NLU**, not just dialogue management:

1. **IBiS1** says: "NLU must produce structured DialogueMoves with dialogue acts, questions, and answers"

2. **IBiS2** says: "NLU must also report confidence and detect ambiguity"

3. **IBiS3** says: "NLU must extract multiple facts per utterance and support semantic matching"

4. **IBiS4** says: "NLU must recognize actions and extract preferences"

**Current IBDM**: Has IBiS1 NLU complete, needs IBiS3 NLU next (multi-fact extraction + volunteer info)

**Perfect for LLMs**: Modern LLMs (Claude 4.5) naturally excel at IBiS3 requirements (multi-fact extraction, semantic matching)

**Next Steps**: Enhance NLU prompts to extract multiple facts from single utterance, implement volunteer information detection
