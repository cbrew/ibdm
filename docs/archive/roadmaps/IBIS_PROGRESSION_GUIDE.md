# IBiS Progression Guide

**Status**: ✅ CURRENT
**Purpose**: Roadmap for implementing Larsson's IBiS1 → IBiS2 → IBiS3 → IBiS4 progression
**Last Updated**: 2025-11-15
**For**: AI agents and developers implementing IBDM

---

## Executive Summary

This guide tells the story of how IBDM progresses through Larsson's four incremental dialogue systems. It combines:
- **Where we are**: Current implementation status (verified from code)
- **Where we're going**: Task-to-thesis mapping
- **How to get there**: Concrete implementation steps for each IBiS stage

**Current State** (Verified from Code):
- ✅ **IBiS1 COMPLETE** (100%) - Core QUD, Plans, Four-phase control loop
- ⚠️ **IBiS2 PARTIAL** (60%) - Basic grounding, missing advanced ICM
- 🔧 **IBiS3 FOUNDATION** (30%) - Architecture ready, accommodation incomplete
- 📋 **IBiS4 PLANNED** (10%) - Structure defined, not yet implemented

---

## The IBiS Progression Story

Larsson's thesis presents dialogue management as **incremental evolution**, each system building on the previous:

```
IBiS1 → IBiS2 → IBiS3 → IBiS4
 Core   Ground   Accom   Actions
```

**Philosophy**: Build a solid foundation, then add capabilities systematically. Each system maintains backward compatibility while adding new features.

**IBDM Strategy**: We're implementing **IBiS1 + IBiS3 first**, then IBiS2 grounding, finally IBiS4 actions. This prioritizes core dialogue competence over advanced features.

---

## Part 1: IBiS1 - Core Issue-Based Dialogue Management

**Thesis**: Larsson (2002) Chapter 2
**Status**: ✅ **COMPLETE** (100%)
**Completion**: 2025-11-16

### What IBiS1 Is

The foundation of issue-based dialogue management:
- **Questions Under Discussion (QUD)**: LIFO stack tracking active questions
- **Plans**: Task plans guide information-seeking behavior
- **Four Phases**: INTERPRET → INTEGRATE → SELECT → GENERATE
- **Domain Independence**: Rules work across domains

### Current Implementation (Verified)

**Information State Structure** (`src/ibdm/core/information_state.py`):
```python
@dataclass
class PrivateIS:
    plan: list[Plan]           # Task plans
    agenda: list[DialogueMove] # Immediate actions
    beliefs: dict[str, Any]    # Private knowledge
    last_utterance: DialogueMove | None

@dataclass
class SharedIS:
    qud: list[Question]        # Stack (LIFO) - last = top
    commitments: set[str]      # Common ground
    last_moves: list[DialogueMove]

@dataclass
class ControlIS:
    speaker: str
    next_speaker: str
    initiative: str
    dialogue_state: str
```

**Update Rules Implemented** (`src/ibdm/rules/integration_rules.py`):
- ✅ `form_task_plan` - Task plan formation (Section 2.8.6 FindPlan)
- ✅ `integrate_question` - Push to QUD (Section 2.8.2 IntegrateAsk)
- ✅ `integrate_answer` - Resolve QUD, add commitment (Section 2.8.3 IntegrateAnswer)
- ✅ `integrate_assertion` - Add to commitments
- ✅ `integrate_greet` - Initialize dialogue
- ✅ `integrate_quit` - End dialogue

**Selection Rules** (`src/ibdm/rules/selection_rules.py`):
- ✅ Select from plan (Section 2.9.1 SelectFromPlan)
- ✅ Select question from QUD (Section 2.9.2 SelectAsk)
- ✅ Select clarification for invalid answers (Section 3.6, basic ICM)

**Semantic Operations** (`src/ibdm/core/domain.py`):
- ✅ `resolves(answer, question)` - Does answer resolve question?
- ✅ `combines(question, answer)` - Form proposition from Q+A
- ✅ Domain-specific predicates and sorts (NDA, Travel domains)

### What Works

**Example Dialogue** (Tested):
```
System: "What are the parties to the agreement?"
User: "Acme Corp and Smith Inc"
System: [Pops question from QUD, adds commitment, advances plan]
System: "What's the effective date?"
User: "invalid response"
System: "I need a valid date. Please provide the effective date."
User: "January 1, 2025"
System: [Continues with plan]
```

**Tests Passing**:
- 156/156 core tests
- Multi-turn QUD management
- Plan progression across turns
- Domain validation (NDA + Travel)
- Clarification handling

### Related Tasks

**Metrics & Validation**:
- `ibdm-metrics.1` (P0): Define Larsson Fidelity Metrics Framework
- `ibdm-metrics.1.1-1.7` (P0): Architectural compliance, state structure, semantic operations, update/selection rules coverage
- `ibdm-82` (P0): Demo Goal 1: Larsson-Faithful IBDM

**Domain Portability**:
- `ibdm-84-88` (P0): Domain portability demonstration (NDA + Travel)
- `ibdm-66-72` (P0-P2): Separate domain-independent from domain-specific code

**Testing**:
- `ibdm-loop.1-3, 10-12` (P0): Answer integration, QUD, plan tests

### Success Criteria ✅

- [x] QUD operates as LIFO stack
- [x] Four-phase control loop working
- [x] Task plan formation in INTEGRATION phase
- [x] Domain-independent rules
- [x] Multi-domain deployment (NDA, Travel)
- [x] 100% core tests passing

---

## Part 2: IBiS2 - Grounding & Interactive Communication Management

**Thesis**: Larsson (2002) Chapter 3
**Status**: ⚠️ **PARTIAL** (60%)
**Current**: Basic clarification, missing advanced grounding

### What IBiS2 Adds

Extensions for robust communication:
- **Grounding**: Ensure mutual understanding of utterances
- **Interactive Communication Management (ICM)**: Explicit feedback moves
- **Evidence Requirements**: What evidence confirms understanding?
- **Grounding Strategies**: Optimistic, cautious, pessimistic

### Information State Extensions

**New Fields** (Figure 3.1):
```python
@dataclass
class SharedIS:
    qud: list[Question]
    commitments: set[str]
    last_moves: list[DialogueMove]
    # NEW for IBiS2:
    moves: list[Move]           # Complete move history for grounding
    next_moves: list[Move]      # Pending system moves
```

### What's Implemented

**Basic ICM** (Verified):
- ✅ Clarification for invalid answers
- ✅ Selection rule for clarification (priority 25)
- ✅ Generation of clarification prompts

**Example**:
```
User: "invalid date"
System: "I need a valid date. Please provide the effective date."
```

### What's Missing

**Advanced ICM Taxonomy** (Section 3.4):
- ❌ `icm:per*pos` - Positive perception ("I heard you")
- ❌ `icm:per*neg` - Negative perception ("Sorry, I didn't hear that")
- ❌ `icm:und*pos` - Positive understanding ("OK, Paris")
- ❌ `icm:und*neg` - Negative understanding ("Paris? Did you say Paris?")
- ❌ `icm:und*int:USR*NUM` - Understanding confirmation ("Paris, is that correct?")

**Grounding Strategies** (Section 3.5):
- ❌ Optimistic (assume grounded unless negative evidence)
- ❌ Cautious (request confirmation)
- ❌ Pessimistic (request explicit acknowledgment)

**Perception Checking** (Section 3.6.7):
- ❌ ASR confidence thresholding
- ❌ Request for repetition when confidence low
- ❌ Spelling confirmation for low-confidence entities

### Related Tasks (P1 - Post-IBiS1-Demo)

**Full ICM Support**:
- `ibdm-okw` (P1): Phase 6: Grounding and ICM
- `ibdm-okw.1` (P1): Implement grounding mechanisms (Section 3.6.3)
- `ibdm-okw.2` (P1): Interactive communication management (Section 3.2.3)
- `ibdm-okw.3` (P1): Feedback and clarification (Section 3.4)
- `ibdm-okw.4` (P1): Error handling and repair (Section 3.6.9)

**Metrics**:
- `ibdm-metrics.2.1` (P0): Define turn management metrics
- `ibdm-metrics.2.4` (P1): Define conversation coherence metrics

**Multi-Party Extensions**:
- `ibdm-metrics.2` (P0): Q2: Define Multi-Party Conversation Metrics
- `ibdm-tty.*` (P1): Multi-agent system (extends grounding for multiple participants)

### Implementation Path

**Phase 1: Complete ICM Taxonomy** (2-3 weeks)
1. Add `shared.moves` and `shared.next_moves` to InformationState
2. Implement ICM move types in `src/ibdm/core/moves.py`
3. Add grounding status tracking to SharedIS
4. Create update rules for ICM moves (Rules 3.1-3.27)
5. Add selection rules for ICM generation

**Phase 2: Grounding Strategies** (2 weeks)
1. Define evidence requirements per utterance type
2. Implement strategy selection based on confidence
3. Add grounding status to move history
4. Implement reraising after grounding failure (Rule 3.15)

**Phase 3: Perception Checking** (1 week)
1. Integrate ASR confidence scores
2. Add low-confidence detection
3. Implement repetition requests
4. Add spelling confirmation for entities

### Success Criteria

- [ ] All 27 ICM rules from Section 3.6 implemented
- [ ] Grounding strategy selection working
- [ ] Evidence requirements defined and enforced
- [ ] Perception checking for ASR errors
- [ ] Feedback moves generated appropriately

---

## Part 3: IBiS3 - Question Accommodation

**Thesis**: Larsson (2002) Chapter 4
**Status**: 🔧 **FOUNDATION** (30%)
**Priority**: CRITICAL - Core accommodation refactoring in progress

### What IBiS3 Adds

Flexible, natural dialogue handling:
- **Question Accommodation**: Handle answers to unasked questions
- **Private Issues**: Questions accommodated but not yet explicitly raised
- **Dependent Issues**: Accommodate prerequisite questions
- **Clarification**: Handle unclear or ambiguous answers

### The Key Insight

**Two-Phase Accommodation**:
1. **Accommodation** (Rule 4.1): Plan → `private.issues` (not yet raised)
2. **Raising** (Rule 4.2): `private.issues` → `shared.qud` (explicit)

This separation enables:
- Incremental questioning (don't dump all questions at once)
- Context-sensitive raising (raise when appropriate)
- User initiative (user can volunteer information)

### Information State Extensions

**New Field** (Figure 4.1):
```python
@dataclass
class PrivateIS:
    plan: list[Plan]
    agenda: list[DialogueMove]
    beliefs: dict[str, Any]
    last_utterance: DialogueMove | None
    # NEW for IBiS3:
    issues: list[Question]      # Accommodated but not yet raised
```

### Current Implementation (Verified)

**Foundation in Place**:
- ✅ Task plan formation in INTEGRATION phase (not INTERPRET)
  - Code: `src/ibdm/rules/integration_rules.py:29` - `form_task_plan` rule
  - Comment: "Task plan formation - create plans for command/request moves"
  - Comment: "This is THE RIGHT PLACE for task plan formation per Larsson (2002)"
- ✅ Accommodation module exists (`src/ibdm/accommodation/`)
- ✅ Domain-based dependency checking structure

**What's Missing**:
- ❌ `private.issues` field in InformationState
- ❌ Rule 4.1 (IssueAccommodation): Plan → private.issues
- ❌ Rule 4.2 (LocalQuestionAccommodation): private.issues → shared.qud
- ❌ Rule 4.3 (IssueClarification)
- ❌ Rule 4.4 (DependentIssueAccommodation)
- ❌ Rule 4.5 (QuestionReaccommodation)

### The Critical Refactoring

**Task**: `ibdm-accom` (P0) - **Refactor: Move Task Accommodation from Interpretation to Integration Phase**

**Current Architecture** (Verified from code):
```
INTERPRET → DialogueMove (move_type="request", content="I need an NDA")
INTEGRATE → form_task_plan → Create Plan, execute FindPlan rule
            Questions go DIRECTLY to QUD
```

**Target Architecture** (Larsson Section 4.6.1-4.6.2):
```
INTERPRET → DialogueMove (move_type="request")
INTEGRATE → form_task_plan → Create Plan
            → Rule 4.1 (IssueAccommodation) → Questions to private.issues
SELECT    → Rule 4.2 (LocalQuestionAccommodation) → private.issues to shared.qud
            (based on context, only raise when appropriate)
```

**Why This Matters**:
- **Architectural Fidelity**: Accommodation is pragmatic processing (INTEGRATE/SELECT), not syntactic (INTERPRET)
- **User Initiative**: User can answer questions before they're explicitly asked
- **Incremental Questioning**: System doesn't overwhelm user with all questions at once
- **Context Sensitivity**: System raises questions based on dialogue flow

### Example: The Difference

**Without IBiS3 (Current)**:
```
System: "What are the parties to the agreement?"
User: "Acme and Smith, effective January 1, 2025"
System: [Only processes parties, ignores date]
System: "What's the effective date?"
User: "I just told you, January 1, 2025"
```

**With IBiS3 (Target)**:
```
System: "What are the parties to the agreement?"
User: "Acme and Smith, effective January 1, 2025"
System: [Accommodates date answer to unasked question]
System: [Removes date question from private.issues]
System: "What's the governing law?"  [Skips to next question]
```

### Related Tasks (P0 - CRITICAL)

**Core Refactoring**:
- `ibdm-accom` (P0): **Main epic - Move accommodation to integration**
  - Maps to: Rule 4.1 (IssueAccommodation) + Rule 4.2 (LocalQuestionAccommodation)
  - Why: Architectural fidelity to Larsson (2002) Chapter 4

**Integration Testing**:
- `ibdm-accom.1.3` (P0): Update integration tests for accommodation
  - Validates: Two-phase accommodation flow (issues → qud)

**Path Validation**:
- `ibdm-accom.4.1` (P1): Verify NLU engine creates correct move types
- `ibdm-accom.4.2` (P1): Test NLU → integration → accommodation path
- `ibdm-accom.4.3` (P2): Add logging for accommodation debugging
- `ibdm-accom.4.4` (P2): Add fallback to generic generation

**End-to-End Validation**:
- `ibdm-accom.5.1` (P1): Create comprehensive NDA workflow integration test
- `ibdm-accom.5.2` (P1): Test with both rule-based and NLU interpretation
- `ibdm-accom.5.3` (P1): Manual testing with interactive demo
- `ibdm-accom.5.4` (P2): Performance testing and benchmarking

**Plan-Aware NLG**:
- `ibdm-accom.3` (P1): Phase 3: Enhance NLG with plan context
- `ibdm-accom.3.1` (P1): Add plan-aware question generation helper
- `ibdm-accom.3.2` (P1): Implement NDA-specific question templates
- `ibdm-accom.3.3` (P2): Add plan progress feedback

### Implementation Path

**Phase 1: Add private.issues Field** (1 day)
1. Update `src/ibdm/core/information_state.py`:
   ```python
   @dataclass
   class PrivateIS:
       plan: list[Plan]
       agenda: list[DialogueMove]
       beliefs: dict[str, Any]
       last_utterance: DialogueMove | None
       issues: list[Question] = field(default_factory=list)  # NEW
   ```
2. Update serialization in `to_dict()` and `from_dict()`
3. Update tests for new field

**Phase 2: Implement Rule 4.1 (IssueAccommodation)** (2-3 days)
1. Create update rule in `src/ibdm/rules/integration_rules.py`:
   ```python
   UpdateRule(
       name="accommodate_issue_from_plan",
       preconditions=_plan_has_findout_action,
       effects=_move_findout_to_issues,
       priority=14,  # Before form_task_plan
       rule_type="integration",
   )
   ```
2. Implementation:
   - Check if `head(private.plan).type == "findout"`
   - Extract question Q
   - Push Q to `private.issues`
   - Pop from `private.plan`

**Phase 3: Implement Rule 4.2 (LocalQuestionAccommodation)** (2-3 days)
1. Create selection rule in `src/ibdm/rules/selection_rules.py`:
   ```python
   UpdateRule(
       name="raise_accommodated_question",
       preconditions=_has_raisable_issue,
       effects=_raise_issue_to_qud,
       priority=20,  # High priority
       rule_type="selection",
   )
   ```
2. Implementation:
   - Check if `private.issues` has questions
   - Check if context appropriate for raising (not interrupting)
   - Pop Q from `private.issues`
   - Push Q to `shared.qud`

**Phase 4: Handle Answers to Unasked Questions** (3-5 days)
1. Modify `integrate_answer` rule:
   - Check if answer resolves a question in `private.issues`
   - If yes: remove from issues, add commitment, don't push to QUD
   - If no: normal QUD-based processing
2. Add tests for volunteer information scenarios

**Phase 5: Implement Rule 4.3 (IssueClarification)** (2 days)
1. Detect unclear/ambiguous answers
2. Generate clarification question CQ
3. Push CQ to `shared.qud`
4. Suspend original question

**Phase 6: Implement Rule 4.4 (DependentIssueAccommodation)** (Future)
1. Define `depends(Q1, Q2)` in domain models
2. When Q1 on QUD, check if Q2 is prerequisite
3. If Q2 not answered, push Q2 to QUD (above Q1)

**Phase 7: Implement Rule 4.5 (QuestionReaccommodation)** (Future)
1. Detect persistent non-resolving answers
2. Reformulate question
3. Re-accommodate to `private.issues`

### Success Criteria

- [ ] `private.issues` field in InformationState
- [ ] Rule 4.1: Plan → private.issues (accommodation)
- [ ] Rule 4.2: private.issues → shared.qud (raising)
- [ ] Rule 4.3: Clarification questions generated
- [ ] Answers to unasked questions handled correctly
- [ ] Tests: User volunteers information, system doesn't re-ask
- [ ] Integration tests pass for two-phase accommodation

---

## Part 4: IBiS4 - Action-Oriented & Negotiative Dialogue

**Thesis**: Larsson (2002) Chapter 5
**Status**: 📋 **PLANNED** (10%)
**Priority**: P1 (Future work, post-IBiS3)

### What IBiS4 Adds

Extensions for task execution and negotiation:
- **Device Actions**: Execute actions on external systems
- **Action Accommodation**: Handle implicit action requests
- **Negotiation**: Discuss alternatives, preferences
- **Issues Under Negotiation (IUN)**: Propositions being debated

### Information State Extensions

**New Fields** (Figure 5.1):
```python
@dataclass
class PrivateIS:
    plan: list[Plan]
    agenda: list[DialogueMove]
    beliefs: dict[str, Any]
    last_utterance: DialogueMove | None
    issues: list[Question]        # IBiS3
    # NEW for IBiS4:
    actions: list[Action]         # Pending device actions
    iun: set[Proposition]         # Issues Under Negotiation
```

### What IBiS4 Would Enable

**Action-Oriented Dialogue** (Section 5.4):
```
User: "Book the Paris hotel"
System: [Confirms: "Booking Hotel du Louvre in Paris, is that correct?"]
User: "Yes"
System: [Executes action, updates state with postcondition]
System: "Hotel booked. Confirmation number: ABC123"
```

**Negotiative Dialogue** (Section 5.7):
```
User: "I want a hotel in Paris under $200"
System: "I found Hotel A at $180 and Hotel B at $150"
User: "Which is closer to the Eiffel Tower?"
System: "Hotel B is 5 minutes away, Hotel A is 15 minutes"
User: "Book Hotel B"
System: [Executes booking action]
```

### New Semantic Operations

**postcond(Action)** (Section 5.4.3):
```python
postcond(book_hotel(hotel_id)) → booked(hotel_id)
postcond(cancel_reservation(id)) → cancelled(id)
```

**dominates(P1, P2)** (Section 5.7.3):
```python
dominates(hotel_price_150, hotel_price_180) → True  # Cheaper
dominates(hotel_rating_4star, hotel_rating_3star) → True  # Better
```

### New Update Rules

**Rule 5.1: IntegrateRequest** (Section 5.6.1):
- User requests action A
- Add A to `private.actions`

**Rule 5.2: RejectRequest** (Section 5.6.1):
- Action A not feasible
- Generate rejection, explain why

**Rule 5.3: ExecuteAction** (Section 5.6.2):
- Execute action A on device
- Add `postcond(A)` to `shared.com`

**Rule 5.4: ActionAccommodation** (Section 5.6.5):
- User mentions action A implicitly
- Accommodate A to `private.actions`

**Rule 5.5: IntroduceAlternative** (Section 5.7.3):
- Alternative P' available for P
- Add P' to `private.iun`

### Related Tasks (P1+ - Future)

**Infrastructure**:
- Device interface definition
- Menu structure to plan conversion (Section 5.4.2)
- `postcond()` function implementation
- `dominates()` relation definition

**Not Yet Prioritized**: IBiS4 features deferred until IBiS1-3 complete

### Implementation Path (When Ready)

**Phase 1: Device Actions** (3-4 weeks)
1. Add `private.actions` to PrivateIS
2. Implement Rules 5.1-5.4 (request, reject, execute, accommodate)
3. Define device interface
4. Implement `postcond()` function
5. Connect to external systems (APIs, databases)

**Phase 2: Negotiation** (3-4 weeks)
1. Add `private.iun` to PrivateIS
2. Implement Rule 5.5 (IntroduceAlternative)
3. Define `dominates()` relation
4. Implement alternative comparison
5. Implement preference elicitation

**Phase 3: Integration** (2 weeks)
1. End-to-end action-oriented dialogue tests
2. Multi-alternative negotiation tests
3. Integration with IBiS1-3 features

### Success Criteria

- [ ] `private.actions` and `private.iun` fields in InformationState
- [ ] Action execution with postconditions
- [ ] Device interface defined and working
- [ ] Multi-alternative comparison
- [ ] Negotiative dialogue support
- [ ] Integration tests pass

---

## Implementation Priority & Timeline

### Current Focus: IBiS1 Polish + IBiS3 Foundation

**Phase 1: IBiS1 Demo Polish** (2-3 weeks, P0)
- NLG enhancement (make responses natural)
- Domain completeness (NDA + Travel validated)
- Runtime domain switching
- Demo visualization (QUD, plan state)
- End-to-end validation

**Tasks**:
- `ibdm-66.1`, `ibdm-67.1`: NLG module infrastructure
- `ibdm-84.1`, `ibdm-85`: Verify domain completeness
- `ibdm-86-88`: Domain switching, end-to-end validation
- `ibdm-dem.*`: Demo implementation

### Phase 2: IBiS3 Critical Refactoring (2-3 weeks, P0)

**ARCHITECTURAL CHANGE** - Highest Priority After Demo

1. Add `private.issues` field
2. Implement Rule 4.1 (IssueAccommodation)
3. Implement Rule 4.2 (LocalQuestionAccommodation)
4. Handle answers to unasked questions
5. Integration testing

**Tasks**:
- `ibdm-accom` (P0): Main accommodation refactoring
- `ibdm-accom.1.3, 4.*, 5.*`: Testing and validation

**Rationale**: Accommodation is the key differentiator between template-based and truly intelligent dialogue. This enables natural, flexible conversation.

### Phase 3: IBiS2 Complete Grounding (4-6 weeks, P1)

**Post-Demo Priority**

1. Implement full ICM taxonomy (27 rules)
2. Grounding strategies (optimistic/cautious/pessimistic)
3. Perception checking (ASR confidence)
4. Evidence requirements
5. Multi-party extensions

**Tasks**:
- `ibdm-okw.*`: Grounding and ICM implementation
- `ibdm-tty.*`: Multi-agent system (extends grounding)

### Phase 4: IBiS4 Actions & Negotiation (Future, P1+)

**Long-term Enhancement**

- Device action integration
- Negotiative dialogue
- Multi-alternative handling

---

## Verification & Metrics

### How to Verify Each IBiS Stage

**IBiS1 Verification** ✅:
- Run: `pytest tests/unit/test_clarification_handling.py tests/integration/test_qud_and_plan_progression.py`
- Check: QUD operates as stack, plans progress, clarification works
- Metrics: `ibdm-metrics.1.*` (Larsson fidelity framework)

**IBiS2 Verification** (When Complete):
- Run: `pytest tests/unit/test_grounding.py tests/integration/test_icm.py`
- Check: All ICM moves generated correctly, grounding strategies work
- Metrics: `ibdm-metrics.2.*` (Turn management, conversation coherence)

**IBiS3 Verification** (When Complete):
- Run: `pytest tests/integration/test_accommodation.py`
- Check: Answers to unasked questions handled, issues → qud flow works
- Example: User volunteers information, system doesn't re-ask
- Metrics: Accommodation coverage, volunteer information handling

**IBiS4 Verification** (When Complete):
- Run: `pytest tests/integration/test_actions.py tests/integration/test_negotiation.py`
- Check: Actions execute, postconditions added, alternatives compared
- Metrics: Action success rate, negotiation completion

### Larsson Fidelity Scoring

**Overall Target**: 100% compliance with implemented systems

**Current Status** (Verified):
- IBiS1: 100% (complete)
- IBiS2: 60% (basic grounding only)
- IBiS3: 30% (foundation only)
- IBiS4: 10% (planning only)

**Calculation**:
- **Full Thesis Compliance**: ~50% (weighted average)
- **Demo-Relevant Features**: 90% (IBiS1 + partial IBiS2)

---

## Key Architectural Principles

### 1. Incremental Development

**Build systematically**:
- IBiS1 first (foundation)
- IBiS3 next (user experience)
- IBiS2 then (robustness)
- IBiS4 last (advanced features)

**Why this order?**
- IBiS1: Can't do anything without core dialogue loop
- IBiS3: User experience >> robustness for demos
- IBiS2: Grounding important but not demo-critical
- IBiS4: Actions nice-to-have, not essential

### 2. Phase Separation is Sacred

**INTERPRET** (Syntactic/Semantic):
- Utterance → DialogueMove
- NO state updates
- NO task plan formation
- NO accommodation

**INTEGRATE** (Pragmatic):
- DialogueMove → State updates
- Task plan formation HERE (Rule 2.8.6 FindPlan)
- Issue accommodation HERE (Rule 4.1)
- QUD updates

**SELECT** (Decision):
- Choose next system move
- Issue raising HERE (Rule 4.2)
- Plan-based + reactive selection

**GENERATE** (Surface Realization):
- DialogueMove → Natural language
- Template-based or LLM-enhanced

**Critical**: Don't mix phases! Accommodation is INTEGRATE/SELECT, not INTERPRET.

### 3. QUD as Stack (LIFO)

**Always**:
- Push new questions to end: `qud.append(question)`
- Pop from end: `qud.pop()`
- Top is last element: `qud[-1]`

**Never**:
- Treat as set (no ordering)
- Treat as queue (FIFO)
- Access middle elements

### 4. Domain Independence

**Rules are domain-independent**:
- `integrate_answer` works for ANY domain
- `select_question` works for ANY domain

**Domain knowledge in resources**:
- Predicates, sorts, semantic operations
- Task plans, question templates
- Database queries, validation logic

**Benefit**: Add new domain without changing rules

### 5. Explicit State, No Hidden Mutations

**All state in InformationState**:
- Visible in Burr state machine
- No hidden engine state
- Pure functional engines (future: ibdm-bsr)

**Benefits**:
- Transparent behavior
- Easier testing
- Reproducible dialogues

---

## Common Pitfalls & How to Avoid

### Pitfall 1: Accommodation in INTERPRET

**Wrong**:
```python
def interpret(utterance):
    moves = parse_utterance(utterance)
    # DON'T DO THIS:
    if move.type == "request":
        plan = create_task_plan(move)  # WRONG PHASE!
    return moves
```

**Right**:
```python
def interpret(utterance):
    moves = parse_utterance(utterance)
    return moves  # Just return moves, no state changes

def integrate(move, state):
    if move.type == "request":
        plan = create_task_plan(move)  # RIGHT PHASE!
        state.private.plan.append(plan)
    return state
```

### Pitfall 2: QUD as Set or List

**Wrong**:
```python
# Don't treat QUD as unordered set
if question in state.shared.qud:
    state.shared.qud.remove(question)

# Don't pop from beginning (FIFO)
question = state.shared.qud.pop(0)
```

**Right**:
```python
# QUD is LIFO stack
state.shared.qud.append(question)  # Push
question = state.shared.qud.pop()   # Pop from end
top = state.shared.qud[-1]          # Peek at top
```

### Pitfall 3: Skipping IBiS Stages

**Wrong**:
- Implement IBiS4 actions before IBiS1 is solid
- Add IBiS2 grounding before basic dialogue works
- Mix features from multiple IBiS stages haphazardly

**Right**:
- Complete IBiS1 fully before moving on
- Add IBiS3 accommodation next (user experience)
- Then IBiS2 grounding (robustness)
- Finally IBiS4 actions (advanced features)

**Why**: Each stage builds on previous. Solid foundation >> fancy features.

### Pitfall 4: Hidden Engine State

**Wrong**:
```python
class DialogueEngine:
    def __init__(self):
        self.qud = []  # DON'T: hidden state
        self.plan = []  # DON'T: hidden state

    def integrate(self, move):
        self.qud.append(...)  # Mutates hidden state
```

**Right**:
```python
def integrate(move, state):
    new_state = copy.deepcopy(state)
    new_state.shared.qud.append(...)
    return new_state  # Pure function, explicit state
```

---

## Resources & References

### Essential Reading

**Thesis**:
- `docs/Larsson_Tesis_nopages.md` - Complete thesis
- `docs/LARSSON_ALGORITHMS.md` - Extracted algorithms and rules

**Current Project Status**:
- `PROJECT_STATUS.md` - What's implemented (verified from code)
- `LARSSON_TASK_MAPPING.md` - Task-to-thesis mapping
- `SYSTEM_ACHIEVEMENTS.md` - Detailed accomplishments

**Development**:
- `CLAUDE.md` - Development policies
- `LARSSON_PRIORITY_ROADMAP.md` - Task priorities
- `docs/architecture_principles.md` - Policy #0

### Code Verification

**Check Current Implementation**:
```bash
# Information State structure
cat src/ibdm/core/information_state.py

# Integration rules (where accommodation belongs)
cat src/ibdm/rules/integration_rules.py

# Selection rules (where issue raising belongs)
cat src/ibdm/rules/selection_rules.py

# Domain definitions
cat src/ibdm/core/domain.py
cat src/ibdm/domains/nda.py
cat src/ibdm/domains/travel.py

# Tests
pytest tests/unit/test_clarification_handling.py -v
pytest tests/integration/test_qud_and_plan_progression.py -v
```

### Task Tracking

```bash
# View ready tasks
.claude/beads-helpers.sh ready

# View current work
.claude/beads-helpers.sh current

# Project summary
.claude/beads-helpers.sh summary
```

---

## Quick Decision Tree

**"Which IBiS feature should I implement next?"**

```
Are IBiS1 core tests passing (156/156)?
├─ NO → Fix IBiS1 first
└─ YES → Is demo-ready (NLG polish, domain switching)?
    ├─ NO → Polish IBiS1 demo (Phase 1)
    └─ YES → Is private.issues implemented?
        ├─ NO → Implement IBiS3 accommodation (Phase 2) ← CRITICAL
        └─ YES → Are all ICM rules implemented?
            ├─ NO → Implement IBiS2 grounding (Phase 3)
            └─ YES → Ready for IBiS4 actions (Phase 4)
```

**"Where does this feature go?"**

```
Does it involve understanding language?
├─ YES → INTERPRET phase
└─ NO → Does it update dialogue state?
    ├─ YES → INTEGRATE phase
    └─ NO → Does it decide what to say?
        ├─ YES → SELECT phase
        └─ NO → Must be GENERATE phase
```

**"Is this IBiS1, 2, 3, or 4?"**

```
Feature involves:
- QUD, Plans, Basic dialogue loop → IBiS1
- ICM, Grounding, Feedback → IBiS2
- private.issues, Accommodation, Volunteer answers → IBiS3
- Device actions, Negotiation, IUN → IBiS4
```

---

## Updates

**Maintenance**: Update this guide when:
1. IBiS stage transitions occur (e.g., IBiS3 complete)
2. Major architectural decisions made
3. Implementation status changes significantly
4. New verification methods added

**Last Major Update**: 2025-11-15 (Initial creation, comprehensive progression guide)

---

**The Journey**: IBiS1 (foundation) → IBiS3 (user experience) → IBiS2 (robustness) → IBiS4 (advanced)

**Current Position**: ✅ IBiS1 complete, 🔧 IBiS3 foundation laid, ⚠️ IBiS2 partial

**Next Steps**: Polish demo → Implement IBiS3 accommodation → Complete IBiS2 grounding → Add IBiS4 actions

---

## Historical Documentation

### Archived Planning Documents
- **Development Plan**: `docs/archive/planning/DEVELOPMENT_PLAN.md` (📋 Original 8-phase plan)
- **Demo Plan**: `docs/archive/planning/DEMO_PLAN.md` (✅ Completed demo strategy)
- **NLU Enhancement Plan**: `docs/archive/planning/NLU_ENHANCEMENT_PLAN.md` (✅ Phase 3.5 completed)
- **Project Structure**: `docs/archive/planning/PROJECT_STRUCTURE.md` (📋 Ideal structure from design phase)

### Analysis & Status Reports
- **IBD-1 Completion Analysis**: `reports/ibd-1-completion-analysis.md` (Detailed assessment vs. Larsson thesis)
- **Project Status Snapshot**: `reports/project-status-2025-11-16.md` (Comprehensive status at IBD-1 completion)

### Reference Documents
- **Interpretation/Accommodation Issue**: `docs/interpretation-accommodation-quick-ref.md` (Quick reference for phase boundaries)