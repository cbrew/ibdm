# IBiS Variants Completion Priority Roadmap

**Status**: ✅ CURRENT
**Goal**: Complete IBiS-2, IBiS-3, and IBiS-4 variants from Larsson (2002)
**Date**: 2025-11-16
**Basis**: IBIS_PROGRESSION_GUIDE.md analysis, Larsson thesis compliance

---

## Executive Summary

**Current State**:
- ✅ IBiS1: 100% complete (core dialogue management)
- ⚠️ IBiS2: 60% complete (basic grounding only)
- 🔧 IBiS3: 30% complete (foundation laid, accommodation missing)
- 📋 IBiS4: 10% complete (planned, not implemented)

**Optimal Completion Order**: IBiS3 → IBiS2 → IBiS4

**Rationale**:
1. **IBiS3 first**: User experience improvement, enables natural dialogue
2. **IBiS2 second**: Robustness features, grounding and error handling
3. **IBiS4 last**: Advanced features, actions and negotiation

---

## PRIORITY 1: Complete IBiS3 - Question Accommodation

**Target**: 30% → 100% (8-10 weeks)
**Why First**: Biggest user experience improvement, enables natural volunteer information
**Larsson**: Chapter 4 - Question Accommodation

### Critical Path Tasks

#### Week 1-2: Core Accommodation Infrastructure

**1. Add private.issues Field**
- **Task**: Update `src/ibdm/core/information_state.py`
- **What**: Add `issues: list[Question]` to PrivateIS
- **Why**: Foundation for two-phase accommodation (issues → qud)
- **Larsson**: Figure 4.1 - Information State Extensions
- **Effort**: 1 day
- **Tests**: Update serialization, state management tests

**2. Implement Rule 4.1 (IssueAccommodation)**
- **Task**: Create update rule `accommodate_issue_from_plan`
- **What**: Plan findout actions → private.issues (not directly to QUD)
- **Why**: Separates accommodation from raising
- **Larsson**: Section 4.6.1 - IssueAccommodation rule
- **Code**: `src/ibdm/rules/integration_rules.py`
- **Priority**: 14 (before form_task_plan)
- **Effort**: 2-3 days
- **Tests**: Plans push to issues, not QUD

**3. Implement Rule 4.2 (LocalQuestionAccommodation)**
- **Task**: Create selection rule `raise_accommodated_question`
- **What**: private.issues → shared.qud (when contextually appropriate)
- **Why**: Incremental questioning, not dumping all questions at once
- **Larsson**: Section 4.6.2 - LocalQuestionAccommodation rule
- **Code**: `src/ibdm/rules/selection_rules.py`
- **Priority**: 20 (high)
- **Effort**: 2-3 days
- **Tests**: Issues raised to QUD at appropriate times

#### Week 3-4: Volunteer Information Handling

**4. Handle Answers to Unasked Questions**
- **Task**: Modify `integrate_answer` rule
- **What**: Check if answer resolves question in private.issues
- **Why**: Users can volunteer information before asked
- **Larsson**: Core IBiS3 capability
- **Logic**:
  ```python
  # Check private.issues first
  if answer resolves question in private.issues:
      remove from issues
      add commitment
      don't push to QUD
  # Then check QUD
  elif answer resolves question on QUD:
      normal QUD processing
  else:
      clarification needed
  ```
- **Effort**: 3-5 days
- **Tests**: User volunteers date before asked, system doesn't re-ask

**5. Implement Rule 4.3 (IssueClarification)**
- **Task**: Create clarification rule for ambiguous answers
- **What**: Detect unclear answers, generate clarification question CQ
- **Why**: Handle ambiguity in volunteer information
- **Larsson**: Section 4.3 - IssueClarification
- **Logic**:
  - Detect unclear/ambiguous answers
  - Generate clarification question CQ
  - Push CQ to shared.qud (above original question)
  - Suspend original question temporarily
- **Effort**: 2 days
- **Tests**: Ambiguous answer → clarification → resolution

#### Week 5-6: Dependent Issues

**6. Implement Rule 4.4 (DependentIssueAccommodation)**
- **Task**: Handle prerequisite questions
- **What**: If Q1 depends on Q2, accommodate Q2 first
- **Why**: Logical question ordering (e.g., "Which party?" before "Party address?")
- **Larsson**: Section 4.4 - DependentIssueAccommodation
- **Domain Setup**:
  ```python
  # In domain model
  depends(Q_party_address, Q_parties) → True
  # "Can't ask for party address before knowing parties"
  ```
- **Logic**:
  - When raising Q1 from issues
  - Check if depends(Q1, Q2) for any Q2
  - If Q2 not answered, raise Q2 first (push above Q1)
- **Effort**: 3-4 days
- **Tests**: Dependent questions raised in correct order

**7. Implement Rule 4.5 (QuestionReaccommodation)**
- **Task**: Handle persistent non-resolving answers
- **What**: After N failed attempts, reformulate question
- **Why**: Avoid infinite clarification loops
- **Larsson**: Section 4.5 - QuestionReaccommodation
- **Logic**:
  - Track answer attempts per question
  - After 3 failed attempts, reformulate
  - Re-accommodate to private.issues with new wording
- **Effort**: 2 days
- **Tests**: Multiple failed answers → reformulation

#### Week 7-8: Integration & Validation

**8. Integration Testing**
- **Task**: `ibdm-accom.1.3, ibdm-accom.5.1-5.3`
- **What**: End-to-end accommodation tests
- **Scenarios**:
  - User volunteers multiple facts in single utterance
  - System skips already-answered questions
  - Dependent questions raised in order
  - Clarification for ambiguous volunteer information
  - Reformulation after persistent failures
- **Effort**: 1 week

**9. Domain Integration**
- **Task**: Add accommodation to NDA + Travel domains
- **What**:
  - Define `depends()` relations in domain models
  - Add ambiguity detection predicates
  - Test with both domains
- **Effort**: 3-4 days

**10. Documentation & Metrics**
- **Task**: Update documentation, measure compliance
- **What**:
  - Document private.issues field
  - Document all 5 accommodation rules
  - Measure IBiS3 compliance (target: 100%)
  - Update IBIS_PROGRESSION_GUIDE.md
- **Effort**: 2 days

### Success Criteria - IBiS3

- [x] `private.issues` field in InformationState
- [x] Rule 4.1: Plan → private.issues (accommodation)
- [x] Rule 4.2: private.issues → shared.qud (raising)
- [x] Rule 4.3: Clarification questions for ambiguity
- [x] Rule 4.4: Dependent issue accommodation
- [x] Rule 4.5: Question reaccommodation
- [x] Answers to unasked questions handled correctly
- [x] Integration tests: Volunteer information scenarios
- [x] Both domains (NDA, Travel) support accommodation
- [x] IBiS3 fidelity: 100% (up from 30%)

### Example: IBiS3 Impact

**Without IBiS3 (Current)**:
```
System: "What are the parties to the agreement?"
User: "Acme and Smith, effective January 1, 2025"
System: [Only processes parties, ignores date]
System: "What's the effective date?"
User: "I just told you, January 1, 2025"  ← BAD UX
```

**With IBiS3 (Target)**:
```
System: "What are the parties to the agreement?"
User: "Acme and Smith, effective January 1, 2025"
System: [Accommodates date answer to unasked question]
System: [Removes date question from private.issues]
System: "What's the governing law?"  ← SKIPS ALREADY-ANSWERED
```

---

## PRIORITY 2: Complete IBiS2 - Grounding & ICM

**Target**: 60% → 100% (6-8 weeks)
**Why Second**: Robustness and error handling, less critical than UX
**Larsson**: Chapter 3 - Grounding and Interactive Communication Management

### Critical Path Tasks

#### Week 1-2: Information State Extensions

**11. Add Grounding Fields to SharedIS**
- **Task**: Update `src/ibdm/core/information_state.py`
- **What**: Add grounding-specific fields
  ```python
  @dataclass
  class SharedIS:
      qud: list[Question]
      commitments: set[str]
      last_moves: list[DialogueMove]
      # NEW for IBiS2:
      moves: list[Move]           # Complete move history
      next_moves: list[Move]      # Pending system moves
  ```
- **Why**: Track grounding status per utterance
- **Larsson**: Figure 3.1 - IBiS2 Information State
- **Effort**: 1 day

**12. Add Grounding Status Tracking**
- **Task**: Create `src/ibdm/core/grounding.py`
- **What**:
  - GroundingStatus enum (ungrounded, pending, grounded)
  - Evidence requirements per move type
  - Grounding strategy selection
- **Why**: Foundation for all grounding operations
- **Larsson**: Section 3.5 - Grounding Strategies
- **Effort**: 2 days

#### Week 3-5: ICM Taxonomy Implementation

**13. Implement ICM Move Types**
- **Task**: Extend `src/ibdm/core/moves.py`
- **What**: Add all ICM move types from Larsson
  - `icm:per*pos` - Positive perception ("I heard you")
  - `icm:per*neg` - Negative perception ("Sorry, I didn't hear that")
  - `icm:und*pos` - Positive understanding ("OK, Paris")
  - `icm:und*neg` - Negative understanding ("Paris? Did you say Paris?")
  - `icm:und*int:USR*NUM` - Understanding confirmation ("Paris, is that correct?")
- **Why**: Complete ICM taxonomy
- **Larsson**: Section 3.4 - ICM Taxonomy
- **Effort**: 3-4 days

**14. Implement All 27 ICM Update Rules**
- **Task**: `ibdm-okw.2` - Add Rules 3.1-3.27 to integration rules
- **What**: Each rule handles specific grounding situation
- **Key Rules**:
  - Rule 3.1: IntegratePerPos (positive perception)
  - Rule 3.5: IntegrateUndPos (positive understanding)
  - Rule 3.15: Reraising after grounding failure
  - Rule 3.20: Confirmation after low confidence
- **Why**: Complete grounding behavior
- **Larsson**: Section 3.6 - Update Rules
- **Effort**: 2 weeks
- **Tests**: Each rule has unit test

#### Week 6: Grounding Strategies

**15. Implement Grounding Strategy Selection**
- **Task**: `ibdm-okw.1` - Strategy-based grounding
- **What**:
  - Optimistic: Assume grounded unless negative evidence
  - Cautious: Request confirmation
  - Pessimistic: Request explicit acknowledgment
- **Logic**:
  ```python
  if confidence > 0.9:
      strategy = Optimistic  # Assume grounded
  elif confidence > 0.6:
      strategy = Cautious    # Request confirmation
  else:
      strategy = Pessimistic  # Request explicit ack
  ```
- **Why**: Adaptive grounding based on confidence
- **Larsson**: Section 3.5 - Grounding Strategies
- **Effort**: 1 week

**16. Implement Evidence Requirements**
- **Task**: Define evidence needed per utterance type
- **What**:
  - Questions: Need understanding confirmation
  - Answers: Need acceptance/rejection
  - Commands: Need acknowledgment + execution confirmation
- **Why**: Know when something is grounded
- **Larsson**: Section 3.3 - Evidence and Grounding
- **Effort**: 2-3 days

#### Week 7: Perception Checking

**17. Implement ASR Confidence Integration**
- **Task**: `ibdm-okw.3` - Perception checking
- **What**:
  - Accept ASR confidence scores with utterances
  - Low confidence → perception checking
  - Very low confidence → request repetition
- **Logic**:
  ```python
  if asr_confidence < 0.5:
      generate_icm("per*neg")  # "Sorry, I didn't hear that"
  elif asr_confidence < 0.7:
      generate_icm("und*int")  # "Did you say X?"
  ```
- **Why**: Handle speech recognition errors
- **Larsson**: Section 3.6.7 - Perception Checking
- **Effort**: 3-4 days

**18. Implement Spelling Confirmation**
- **Task**: Low-confidence entity confirmation
- **What**: For entities with low ASR confidence, ask for spelling
- **Example**: "Did you say 'Acme Corp'? Can you spell that?"
- **Why**: Critical entities (names, dates) need high confidence
- **Effort**: 2 days

#### Week 8: Integration & Validation

**19. ICM Integration Testing**
- **Task**: End-to-end grounding tests
- **Scenarios**:
  - High confidence → optimistic grounding
  - Medium confidence → cautious grounding (confirmation)
  - Low confidence → perception checking
  - Very low confidence → request repetition
  - Grounding failure → reraising
- **Effort**: 1 week

**20. Documentation & Metrics**
- **Task**: Measure IBiS2 compliance
- **What**:
  - Document all 27 ICM rules
  - Document grounding strategies
  - Measure IBiS2 fidelity (target: 100%)
  - Update IBIS_PROGRESSION_GUIDE.md
- **Effort**: 2 days

### Success Criteria - IBiS2

- [x] `shared.moves` and `shared.next_moves` fields added
- [x] All 27 ICM rules implemented (Section 3.6)
- [x] Grounding status tracking working
- [x] Grounding strategy selection (optimistic/cautious/pessimistic)
- [x] Evidence requirements defined and enforced
- [x] Perception checking for low ASR confidence
- [x] Spelling confirmation for critical entities
- [x] Reraising after grounding failure
- [x] Integration tests: All grounding scenarios
- [x] IBiS2 fidelity: 100% (up from 60%)

### Example: IBiS2 Impact

**Without IBiS2 (Current)**:
```
User: [garbled speech, ASR confidence: 0.3]
System: [Processes anyway, wrong interpretation]
User: "No, that's not what I said!"
```

**With IBiS2 (Target)**:
```
User: [garbled speech, ASR confidence: 0.3]
System: "Sorry, I didn't hear that clearly. Could you repeat?"
User: "Acme Corp"
System: [Processes with context, correct interpretation]
```

---

## PRIORITY 3: Implement IBiS4 - Actions & Negotiation

**Target**: 10% → 100% (8-10 weeks)
**Why Last**: Advanced features, not essential for basic dialogue
**Larsson**: Chapter 5 - Action-Oriented and Negotiative Dialogue

### Critical Path Tasks

#### Week 1-2: Information State Extensions

**21. Add Action Fields to PrivateIS**
- **Task**: Update `src/ibdm/core/information_state.py`
- **What**: Add action-specific fields
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
- **Why**: Track pending actions and negotiation state
- **Larsson**: Figure 5.1 - IBiS4 Information State
- **Effort**: 1 day

**22. Define Action and Proposition Classes**
- **Task**: Create `src/ibdm/core/actions.py`
- **What**:
  - Action class (action_type, parameters, preconditions, postconditions)
  - Proposition class (predicate, arguments, truth_value)
  - ActionStatus enum (pending, executing, completed, failed)
- **Why**: First-class action representation
- **Larsson**: Section 5.2 - Actions and Propositions
- **Effort**: 2 days

#### Week 3-4: Device Interface & Actions

**23. Define Device Interface**
- **Task**: Create `src/ibdm/interfaces/device.py`
- **What**: Abstract interface for external systems
  ```python
  class DeviceInterface(Protocol):
      def execute_action(self, action: Action) -> ActionResult
      def check_preconditions(self, action: Action) -> bool
      def get_postconditions(self, action: Action) -> set[Proposition]
  ```
- **Why**: Connect IBDM to external systems
- **Larsson**: Section 5.4.1 - Device Interface
- **Effort**: 2-3 days

**24. Implement postcond() Function**
- **Task**: Add to `src/ibdm/core/domain.py`
- **What**: Get postconditions for action
  ```python
  postcond(book_hotel(hotel_id)) → {booked(hotel_id)}
  postcond(cancel_reservation(id)) → {cancelled(id)}
  ```
- **Why**: State updates after action execution
- **Larsson**: Section 5.4.3 - Postconditions
- **Effort**: 2 days

**25. Implement Rule 5.1 (IntegrateRequest)**
- **Task**: Add to integration rules
- **What**: User requests action → add to private.actions
- **Example**: "Book the Paris hotel" → book_hotel(paris_hotel)
- **Why**: Handle action requests
- **Larsson**: Section 5.6.1 - IntegrateRequest
- **Effort**: 2 days

**26. Implement Rule 5.2 (RejectRequest)**
- **Task**: Add to integration rules
- **What**: Action not feasible → generate rejection with explanation
- **Example**: "No hotels available in Paris on that date"
- **Why**: Handle impossible actions
- **Larsson**: Section 5.6.1 - RejectRequest
- **Effort**: 1 day

**27. Implement Rule 5.3 (ExecuteAction)**
- **Task**: Add to selection rules
- **What**: Execute action on device, add postcond to commitments
- **Logic**:
  ```python
  action = private.actions.pop(0)
  result = device.execute_action(action)
  if result.success:
      for prop in postcond(action):
          shared.commitments.add(prop)
  ```
- **Why**: Actual action execution
- **Larsson**: Section 5.6.2 - ExecuteAction
- **Effort**: 3-4 days

#### Week 5-6: Action Accommodation

**28. Implement Rule 5.4 (ActionAccommodation)**
- **Task**: Add to integration rules
- **What**: User mentions action implicitly → accommodate to private.actions
- **Example**: "I want to go to Paris" → implicitly requests flight/hotel booking
- **Why**: Natural action requests
- **Larsson**: Section 5.6.5 - ActionAccommodation
- **Logic**:
  - Detect implicit action mentions
  - Infer required actions
  - Add to private.actions (like question accommodation)
- **Effort**: 1 week

#### Week 7-8: Negotiation

**29. Implement dominates() Relation**
- **Task**: Add to `src/ibdm/core/domain.py`
- **What**: Compare alternatives
  ```python
  dominates(hotel_price_150, hotel_price_180) → True  # Cheaper
  dominates(hotel_rating_4star, hotel_rating_3star) → True  # Better
  ```
- **Why**: Alternative comparison for negotiation
- **Larsson**: Section 5.7.3 - Dominance
- **Effort**: 2-3 days

**30. Implement Rule 5.5 (IntroduceAlternative)**
- **Task**: Add to integration rules
- **What**: Alternative P' available for P → add to private.iun
- **Example**: User wants hotel under $200, system found two options
- **Why**: Multi-alternative negotiation
- **Larsson**: Section 5.7.3 - IntroduceAlternative
- **Logic**:
  - User specifies constraint (price < 200)
  - System finds multiple satisfying options
  - Add alternatives to private.iun
  - Engage in negotiation dialogue
- **Effort**: 1 week

**31. Implement Preference Elicitation**
- **Task**: Create negotiation dialogue rules
- **What**: Ask user to compare alternatives
- **Example**: "Which is more important: price or location?"
- **Why**: Resolve between multiple valid options
- **Larsson**: Section 5.7 - Negotiative Dialogue
- **Effort**: 3-4 days

#### Week 9-10: Integration & Validation

**32. End-to-End Action Tests**
- **Task**: Action-oriented dialogue scenarios
- **Scenarios**:
  - User requests action → confirmation → execution
  - Action fails → rejection with explanation
  - Implicit action accommodation
  - Precondition checking
  - Postcondition updates to commitments
- **Effort**: 1 week

**33. Negotiation Integration Tests**
- **Task**: Multi-alternative scenarios
- **Scenarios**:
  - Two valid options → preference elicitation
  - Alternative comparison using dominates()
  - User selects option → action execution
- **Effort**: 3-4 days

**34. Domain Integration**
- **Task**: Add actions to Travel domain
- **What**:
  - book_hotel(hotel_id) action
  - book_flight(flight_id) action
  - Define preconditions/postconditions
  - Mock device interface for testing
- **Effort**: 1 week

**35. Documentation & Metrics**
- **Task**: Measure IBiS4 compliance
- **What**:
  - Document action interface
  - Document negotiation rules
  - Measure IBiS4 fidelity (target: 100%)
  - Update IBIS_PROGRESSION_GUIDE.md
- **Effort**: 2 days

### Success Criteria - IBiS4

- [x] `private.actions` and `private.iun` fields added
- [x] Action class and device interface defined
- [x] postcond() function implemented
- [x] Rule 5.1: IntegrateRequest
- [x] Rule 5.2: RejectRequest
- [x] Rule 5.3: ExecuteAction
- [x] Rule 5.4: ActionAccommodation
- [x] Rule 5.5: IntroduceAlternative
- [x] dominates() relation implemented
- [x] Preference elicitation working
- [x] Integration tests: Action execution scenarios
- [x] Integration tests: Negotiation scenarios
- [x] Travel domain has working actions
- [x] IBiS4 fidelity: 100% (up from 10%)

### Example: IBiS4 Impact

**Action-Oriented Dialogue**:
```
User: "Book the Paris hotel"
System: "Booking Hotel du Louvre in Paris for $180/night, is that correct?"
User: "Yes"
System: [Executes book_hotel(paris_hotel)]
System: [Adds booked(paris_hotel) to commitments]
System: "Hotel booked. Confirmation number: ABC123"
```

**Negotiative Dialogue**:
```
User: "I want a hotel in Paris under $200"
System: "I found Hotel A at $180 and Hotel B at $150"
User: "Which is closer to the Eiffel Tower?"
System: "Hotel B is 5 minutes away, Hotel A is 15 minutes"
User: "Book Hotel B"
System: [Executes book_hotel(hotel_b)]
System: "Hotel B booked. Confirmation number: XYZ789"
```

---

## Overall Timeline

**Total Effort**: 22-28 weeks (5.5-7 months)

### Phase 1: IBiS3 Completion (Weeks 1-10)
- Weeks 1-2: Core accommodation infrastructure
- Weeks 3-4: Volunteer information handling
- Weeks 5-6: Dependent issues
- Weeks 7-8: Integration & validation
- Weeks 9-10: Buffer & polish

### Phase 2: IBiS2 Completion (Weeks 11-18)
- Weeks 11-12: Information state extensions
- Weeks 13-15: ICM taxonomy implementation
- Week 16: Grounding strategies
- Week 17: Perception checking
- Week 18: Integration & validation

### Phase 3: IBiS4 Implementation (Weeks 19-28)
- Weeks 19-20: Information state extensions
- Weeks 21-22: Device interface & actions
- Weeks 23-24: Action accommodation
- Weeks 25-26: Negotiation
- Weeks 27-28: Integration & validation

---

## Dependencies & Blocking Issues

### IBiS3 Dependencies
- ✅ IBiS1 complete (DONE)
- ✅ InformationState structure in place (DONE)
- ✅ Domain model with predicates/sorts (DONE)
- ✅ Integration and selection rules framework (DONE)
- ⚠️ **BLOCKER**: Task plan formation must be in INTEGRATION phase
  - **Status**: Currently in INTERPRET phase (architectural violation)
  - **Fix**: `ibdm-accom` epic - move to integration
  - **Impact**: Blocks all accommodation work
  - **Effort**: 1 week

### IBiS2 Dependencies
- ✅ IBiS1 complete (DONE)
- ✅ DialogueMove types defined (DONE)
- ⚠️ IBiS3 partial (not blocking, but recommended)
- 🔧 ASR confidence scores (needed for perception checking)
  - **Status**: NLU doesn't currently provide confidence
  - **Fix**: Add confidence to NLU output
  - **Impact**: Perception checking can't work without it
  - **Effort**: 2-3 days

### IBiS4 Dependencies
- ✅ IBiS1 complete (DONE)
- ✅ IBiS3 accommodation (NEEDED for action accommodation)
- ⚠️ Device interface design
  - **Status**: Not yet defined
  - **Fix**: Design abstract interface
  - **Impact**: Can't execute real actions without it
  - **Effort**: 1 week
- ⚠️ Domain action definitions
  - **Status**: No actions in current domains
  - **Fix**: Add actions to Travel domain
  - **Impact**: Can't test without domain actions
  - **Effort**: 3-4 days

---

## Immediate Next Steps

### Week 1: Unblock IBiS3

**Must Do First** (1 week):
1. ✅ Fix architectural violation: `ibdm-accom` epic
   - Move task plan formation to INTEGRATION phase
   - Remove from INTERPRET phase
   - Update all tests
2. ✅ Add `private.issues` field to InformationState
3. ✅ Update serialization/deserialization
4. ✅ Commit and push

### Week 2: Start IBiS3 Core (Tasks 2-3)
1. Implement Rule 4.1 (IssueAccommodation)
2. Implement Rule 4.2 (LocalQuestionAccommodation)
3. Write tests for two-phase accommodation
4. Commit and push

### Week 3: Continue IBiS3 (Task 4)
1. Modify integrate_answer to check private.issues
2. Test volunteer information scenarios
3. Commit and push

---

## Metrics & Validation

### Success Metrics

**Overall Larsson Fidelity Target**: 95%+ (from current ~70%)

**Per-Variant Targets**:
- IBiS1: 100% (maintain)
- IBiS2: 100% (from 60%)
- IBiS3: 100% (from 30%)
- IBiS4: 100% (from 10%)

**Test Coverage Target**: 90%+
- Unit tests for all rules
- Integration tests for all scenarios
- Domain tests for NDA + Travel

**Performance Targets**:
- Accommodation decision: <100ms
- Grounding check: <50ms
- Action execution: <1s (excluding device latency)

### Validation Strategy

**Per Variant**:
1. **Implementation Review**: Code matches Larsson algorithms
2. **Unit Tests**: All rules have passing tests
3. **Integration Tests**: Multi-turn scenarios work
4. **Domain Tests**: Both NDA and Travel domains work
5. **Manual Testing**: Natural dialogue feels right
6. **Metrics Report**: Fidelity score calculated

**Reports**:
- Generate fidelity report after each variant completion
- Compare with baseline (IBiS1-only)
- Document improvements

---

## Risk Management

### High Risks

**Risk 1: Accommodation Complexity**
- **Impact**: IBiS3 takes longer than estimated
- **Mitigation**: Implement incrementally, test each rule separately
- **Contingency**: Defer Rules 4.4-4.5 if needed, focus on 4.1-4.3

**Risk 2: ICM Rule Explosion**
- **Impact**: 27 rules is a lot, may have bugs
- **Mitigation**: Template-based rule generation, thorough tests
- **Contingency**: Implement most critical 10 rules first, defer rest

**Risk 3: Device Interface Complexity**
- **Impact**: Real device integration is hard
- **Mitigation**: Start with mock devices, simple actions
- **Contingency**: Keep device interface simple, focus on dialogue management

### Medium Risks

**Risk 4: NLU Confidence Unavailable**
- **Impact**: Can't do perception checking
- **Mitigation**: Mock confidence scores for testing
- **Contingency**: Implement grounding without perception initially

**Risk 5: Domain Action Definition**
- **Impact**: Domains may not have natural actions
- **Mitigation**: Start with Travel domain (booking actions are natural)
- **Contingency**: Create simple test domain with toy actions

---

## Communication & Reporting

### Weekly Progress Reports

**Template**:
```
## Week N Progress Report

**Variant**: IBiS-X
**Tasks Completed**:
- Task A: Description
- Task B: Description

**Tests Added**: N unit tests, M integration tests
**Fidelity Score**: X% (was Y%)
**Blockers**:
- Blocker 1: Description + mitigation
**Next Week**:
- Task C
- Task D
```

### Milestone Reports

**After Each Variant Completion**:
1. Comprehensive fidelity report
2. Test coverage report
3. Performance benchmarks
4. User experience evaluation
5. Next variant planning

---

## References

### Documentation
- `IBIS_PROGRESSION_GUIDE.md` - Detailed guide for each IBiS variant
- `docs/LARSSON_ALGORITHMS.md` - Extracted algorithms and rules
- `docs/Larsson_Tesis_nopages.md` - Complete Larsson thesis
- `CLAUDE.md` - Development policies

### Code
- `src/ibdm/core/information_state.py` - State structure
- `src/ibdm/rules/integration_rules.py` - Integration (update) rules
- `src/ibdm/rules/selection_rules.py` - Selection rules
- `src/ibdm/core/domain.py` - Domain semantic layer

### Tests
- `tests/unit/` - Rule-level tests
- `tests/integration/` - Multi-turn dialogue tests
- `tests/domain/` - Domain-specific tests

---

## Summary

**Goal**: Complete IBiS-2, 3, 4 variants
**Order**: IBiS3 → IBiS2 → IBiS4
**Timeline**: 22-28 weeks
**Current Blocker**: Move accommodation to INTEGRATION phase
**First Milestone**: IBiS3 Rule 4.1-4.2 complete (Week 2)

**Key Insight**: IBiS3 provides the biggest user experience improvement (natural volunteer information), so it comes first even though IBiS2 is further along (60% vs 30%). User experience > robustness > advanced features.

**Next Action**: Fix `ibdm-accom` architectural violation, then implement Rule 4.1.
