# Complete Dialogue Loop Implementation Plan

**Date**: 2025-11-14
**Goal**: Achieve fully functional interactive dialogue loop
**Status**: Planning Phase

---

## Executive Summary

**Current Achievement**: Domain semantic layer implemented (95% Larsson fidelity)

**Remaining Gap**: Full end-to-end interactive dialogue loop with NLU engine

**Critical Issue**: Pattern-based interpretation breaks the chain; NLU engine integration needs verification and completion

**Goal**: User utterances → proper dialogue moves → domain-driven plans → natural questions → user answers → validated integration → next questions → completion

---

## Current State Analysis

### ✅ What Works

1. **Domain Semantic Layer** (100% complete)
   - `DomainModel` with predicates, sorts, plan builders
   - NDA domain with 5 predicates, 2 sorts
   - Type-safe answer validation via `domain.resolves()`
   - 76 tests passing, 0 mocks

2. **Integration Rules** (100% complete)
   - `form_task_plan` uses `domain.get_plan()`
   - Plan creation properly updates `state.private.plan`
   - First question pushed to `state.shared.qud`
   - Task plan formation in correct phase (integration, not interpretation)

3. **Selection Rules** (100% complete)
   - Reads from `state.shared.qud`
   - Selects ask moves when questions available
   - Proper turn-taking logic

4. **Generation Rules** (100% complete)
   - Plan-aware question generation
   - `_get_active_plan()` reads from `state.private.plan`
   - NDA-specific templates with domain descriptions
   - Progress indicators: "[Step N of M]"

5. **Burr Integration** (100% complete)
   - State machine orchestrates IBDM loop
   - All actions implemented (interpret, integrate, select, generate)
   - Proper state flow through actions

### ❌ What's Missing/Broken

1. **NLU Engine Dialogue Act Classification**
   - **Status**: Implemented but not fully tested with real API calls
   - **Issue**: Pattern-based fallback creates wrong move types
   - **Need**: Verify LLM-based classification works end-to-end
   - **Test Coverage**: Limited integration tests with actual LLM calls

2. **Answer Processing Pipeline**
   - **Status**: Partially implemented
   - **Issue**: Answer integration may not use domain validation
   - **Need**: Verify `domain.resolves()` is called in answer integration
   - **Need**: Proper QUD popping after valid answers

3. **Multi-Turn Dialogue Flow**
   - **Status**: Individual components tested, full flow untested
   - **Issue**: Haven't verified complete 5-question NDA workflow
   - **Need**: End-to-end test with real LLM calls
   - **Need**: Verify plan progress tracking through all turns

4. **Entity Extraction → Domain Mapping**
   - **Status**: `NLUDomainMapper` created but not integrated
   - **Issue**: NLU extracts entities, but mapping to domain predicates untested
   - **Need**: Verify ORGANIZATION entities → legal_entities predicate
   - **Need**: Test with real NLU extraction

5. **Interactive Demo Completion**
   - **Status**: Demo exists but may not showcase full workflow
   - **Issue**: Need to verify it actually works end-to-end
   - **Need**: Test with real API key
   - **Need**: Document expected vs actual behavior

---

## Desired End State

### User Experience Flow

```
User: "I need to draft an NDA"
System: "What are the names of the parties entering into this NDA?"

User: "Acme Corp and Beta Inc"
System: "[Step 2 of 5] Should this be a mutual or one-way NDA?"

User: "mutual"
System: "[Step 3 of 5] What is the effective date for the NDA?"

User: "January 1, 2025"
System: "[Step 4 of 5] How long should the confidentiality obligations last? (e.g., '2 years', '5 years')"

User: "3 years"
System: "[Step 5 of 5] Which state's law should govern the NDA: California or Delaware?"

User: "California"
System: "Perfect! I have all the information needed to draft your NDA."
```

### Technical Requirements

1. **Interpretation** (Turn N):
   - User utterance → NLU engine (Claude Haiku/Sonnet)
   - LLM classifies dialogue act → proper move type
   - For request: creates `command` move
   - For answer: creates `answer` move with extracted entities
   - **No fallback to pattern matching**

2. **Integration** (Turn N):
   - Command move → `form_task_plan` → domain.get_plan()
   - Answer move → `integrate_answer` → domain.resolves()
   - Valid answer → pop QUD, mark subplan complete, add to commitments
   - Invalid answer → re-ask with clarification
   - Plan progress tracked in subplan.status

3. **Selection** (Turn N+1):
   - Read from `state.shared.qud` (if populated)
   - Read from `state.private.plan` (check next incomplete subplan)
   - Select ask move for next question
   - Or select completion message if plan done

4. **Generation** (Turn N+1):
   - Detect active plan via `_get_active_plan()`
   - Use plan type to select template
   - For NDA: use `_generate_nda_question()`
   - Include progress: "[Step N of M]"
   - Use domain descriptions for natural phrasing

5. **State Consistency**:
   - `state.private.plan` always reflects current plan state
   - `state.shared.qud` always has current question (or empty when done)
   - `state.shared.commitments` accumulates validated answers
   - Plan subplan.status tracks progress

---

## Gap Analysis

### Gap 1: NLU Engine Integration Not Fully Tested

**What's missing**:
- End-to-end tests with real LLM API calls
- Verification that dialogue act classification works reliably
- Tests for both command classification and answer parsing

**Impact**: High - this is the entry point to the whole system

**Effort**: Medium (2-3 hours)

### Gap 2: Answer Integration Doesn't Use Domain Validation

**What's missing**:
- Integration rule for answers doesn't call `domain.resolves()`
- No validation of answer against question predicate
- No re-asking on invalid answers

**Impact**: High - breaks the validation chain

**Effort**: Medium (1-2 hours)

### Gap 3: Multi-Turn Flow Untested

**What's missing**:
- No test that goes through all 5 NDA questions
- No verification of QUD popping after each answer
- No verification of plan progress tracking

**Impact**: High - this is the core use case

**Effort**: High (3-4 hours)

### Gap 4: Entity Extraction → Domain Mapping

**What's missing**:
- NLUDomainMapper created but not integrated into answer processing
- No tests verifying entity extraction → predicate mapping
- Unclear how extracted entities become Answer content

**Impact**: Medium - affects answer quality

**Effort**: Medium (2 hours)

### Gap 5: Demo Doesn't Work End-to-End

**What's missing**:
- Demo may use incorrect engine or configuration
- May not properly display all dialogue features
- Progress indicators may not show
- Domain-aware questions may not appear

**Impact**: Medium - user-facing issue

**Effort**: Low (1 hour)

---

## Implementation Plan

### Phase 1: Fix Answer Integration with Domain Validation

**Goal**: Ensure answers are validated via domain before accepting

**Tasks**:

1. **Task 1.1**: Review current answer integration rule
   - Check `integration_rules.py::_integrate_answer`
   - Identify where domain validation should be called
   - Document current behavior

2. **Task 1.2**: Add domain validation to answer integration
   - Get active plan from state
   - Get domain from plan
   - Call `domain.resolves(answer, question)`
   - Only pop QUD if resolves returns True

3. **Task 1.3**: Handle invalid answers
   - If domain.resolves() returns False, don't pop QUD
   - Re-ask with clarification
   - Log validation failure

4. **Task 1.4**: Mark subplan complete after valid answer
   - After popping QUD, find corresponding subplan
   - Set subplan.status = "completed"
   - Update plan progress

5. **Task 1.5**: Push next question to QUD
   - After completing subplan, find next active subplan
   - Push its question to QUD
   - Or leave QUD empty if plan complete

**Tests**:
- Test valid answer → QUD popped, subplan completed
- Test invalid answer (empty) → QUD remains, re-asked
- Test final answer → QUD empty, plan complete

**Estimated Time**: 2 hours

---

### Phase 2: Verify NLU Engine End-to-End

**Goal**: Ensure NLU engine properly classifies and processes utterances

**Tasks**:

1. **Task 2.1**: Create comprehensive NLU engine test
   - Test command classification: "I need to draft an NDA"
   - Test answer parsing: "Acme Corp and Beta Inc"
   - Test with real API calls (IBDM_API_KEY)
   - Verify move types are correct

2. **Task 2.2**: Verify entity extraction works
   - Test NLU extracts ORGANIZATION entities
   - Test entities are included in move metadata
   - Verify entity types match domain predicates

3. **Task 2.3**: Test NLU + Domain integration
   - Create answer move with entities
   - Verify NLUDomainMapper maps to predicates
   - Verify mapped answer resolves question

4. **Task 2.4**: Test error handling
   - Test LLM API failure handling
   - Test malformed responses
   - Verify graceful degradation

**Tests**:
- Test NLU classifies "I need to draft an NDA" as command
- Test NLU classifies "Acme Corp" as answer with ORGANIZATION
- Test end-to-end: utterance → moves → integration → response

**Estimated Time**: 3 hours

---

### Phase 3: Complete Multi-Turn Dialogue Test

**Goal**: Verify complete 5-question NDA workflow

**Tasks**:

1. **Task 3.1**: Create multi-turn integration test
   - Simulates complete NDA dialogue
   - Goes through all 5 questions
   - Uses real NLU engine with API calls
   - Verifies each turn's output

2. **Task 3.2**: Verify QUD management
   - Check QUD has 1 question after each turn
   - Check QUD is popped after valid answer
   - Check next question is pushed
   - Check QUD empty after last answer

3. **Task 3.3**: Verify plan progress
   - Check plan.subplans[0].status after first answer
   - Check progress through all subplans
   - Check all subplans completed at end
   - Check progress indicators in output

4. **Task 3.4**: Verify domain validation throughout
   - Test valid answer is accepted
   - Test empty answer is rejected
   - Test invalid type is rejected
   - Check commitments accumulate correctly

**Tests**:
- Test full NDA workflow (5 questions)
- Test plan progress 0→1→2→3→4→5
- Test QUD push/pop for each turn
- Test domain validation for each answer

**Estimated Time**: 4 hours

---

### Phase 4: Integrate NLU Domain Mapper

**Goal**: Map NLU entities to domain predicates properly

**Tasks**:

1. **Task 4.1**: Review NLUDomainMapper implementation
   - Check entity_to_predicate mapping
   - Verify it handles all entity types
   - Document current behavior

2. **Task 4.2**: Integrate mapper into answer processing
   - Call mapper in answer integration rule
   - Map extracted entities to predicate answers
   - Create proper Answer objects with mapped content

3. **Task 4.3**: Test entity mapping
   - Test ORGANIZATION → legal_entities
   - Test TEMPORAL → date
   - Test DURATION → time_period
   - Verify mapped answers resolve questions

4. **Task 4.4**: Handle unmapped entities
   - Define fallback for unknown entity types
   - Log unmapped entities for debugging
   - Use raw answer text if no mapping

**Tests**:
- Test entity extraction → mapping → answer creation
- Test all NDA entity types are mapped
- Test mapped answers are validated

**Estimated Time**: 2 hours

---

### Phase 5: Complete Interactive Demo

**Goal**: Demonstrate full functionality with working demo

**Tasks**:

1. **Task 5.1**: Update demo configuration
   - Ensure uses NLUDialogueEngine
   - Verify API key is loaded
   - Configure proper model (Haiku for fast responses)
   - Add error handling for API failures

2. **Task 5.2**: Add progress display
   - Show plan progress in demo UI
   - Display "[Step N of M]" in output
   - Show QUD state (optional, for debugging)
   - Show plan completion message

3. **Task 5.3**: Test demo end-to-end
   - Run through complete NDA workflow
   - Verify all questions are asked
   - Verify answers are validated
   - Verify final completion message

4. **Task 5.4**: Document demo usage
   - Update demo docstring
   - Add example dialogue transcript
   - Document expected behavior
   - Add troubleshooting guide

**Tests**:
- Manual test: complete NDA workflow
- Verify all domain features visible
- Verify natural language quality
- Test error scenarios

**Estimated Time**: 2 hours

---

### Phase 6: Documentation and Finalization

**Goal**: Document complete system and create final tests

**Tasks**:

1. **Task 6.1**: Update architecture documentation
   - Document complete dialogue loop
   - Update causation chain analysis
   - Add multi-turn flow diagrams
   - Document domain integration

2. **Task 6.2**: Create user guide
   - How to run the demo
   - How to add new domains
   - How to extend with new question types
   - Troubleshooting guide

3. **Task 6.3**: Final integration test suite
   - Comprehensive test covering all components
   - Tests with and without API keys
   - Performance benchmarks
   - Test coverage report

4. **Task 6.4**: Update CLAUDE.md policies
   - Add policy for multi-turn dialogue testing
   - Add policy for NLU engine usage
   - Update workflow integration examples

**Deliverables**:
- Updated architecture docs
- User guide
- Complete test suite
- Updated policies

**Estimated Time**: 2 hours

---

## Testing Strategy

### Unit Tests (No API calls)

1. Domain model validation
2. Integration rules logic
3. Selection rules logic
4. Generation templates
5. Plan progress calculation

**Status**: ✅ Complete (76 tests)

### Integration Tests (Requires API)

1. NLU engine dialogue act classification
2. Entity extraction and mapping
3. Multi-turn dialogue flow
4. Domain validation in answers
5. Complete NDA workflow

**Status**: ⚠️ Partial (need more API tests)

### End-to-End Tests

1. Interactive demo test
2. Full 5-question workflow
3. Error handling scenarios
4. Edge cases (invalid answers, retries)

**Status**: ❌ Missing

---

## Success Criteria

### Functional Requirements

- [ ] User can initiate NDA request with natural language
- [ ] System asks all 5 questions in order
- [ ] System uses natural, domain-specific phrasing
- [ ] System shows progress indicators
- [ ] System validates answers via domain
- [ ] System rejects invalid answers
- [ ] System completes successfully after all answers
- [ ] Complete dialogue takes < 30 seconds

### Technical Requirements

- [ ] NLU engine classifies moves correctly (>90% accuracy)
- [ ] Domain validation used for all answers
- [ ] QUD management works correctly (push/pop)
- [ ] Plan progress tracked accurately
- [ ] No mocking in integration tests
- [ ] All causation chains verified
- [ ] Code passes ruff, pyright
- [ ] Test coverage >80% for new code

### Quality Requirements

- [ ] Natural language questions (not raw predicates)
- [ ] Helpful error messages
- [ ] Graceful API failure handling
- [ ] Clear progress feedback
- [ ] Reasonable response times (<5s per turn)

---

## Timeline

| Phase | Tasks | Estimated Time | Dependencies |
|-------|-------|----------------|--------------|
| Phase 1 | Answer validation (5 tasks) | 2 hours | None |
| Phase 2 | NLU verification (4 tasks) | 3 hours | IBDM_API_KEY |
| Phase 3 | Multi-turn test (4 tasks) | 4 hours | Phase 1, 2 |
| Phase 4 | Domain mapper (4 tasks) | 2 hours | Phase 2 |
| Phase 5 | Demo completion (4 tasks) | 2 hours | Phase 3, 4 |
| Phase 6 | Documentation (4 tasks) | 2 hours | All |
| **TOTAL** | **25 tasks** | **15 hours** | |

---

## Risk Assessment

### High Risk

1. **NLU API Reliability**
   - **Risk**: LLM API may be unreliable or slow
   - **Mitigation**: Add retries, timeouts, caching
   - **Fallback**: Pattern-based for demos (documented limitation)

2. **Domain Validation Edge Cases**
   - **Risk**: Unclear what constitutes "valid" answer for some predicates
   - **Mitigation**: Start with simple validation (non-empty)
   - **Future**: Add sophisticated validation (regex, ranges, etc.)

### Medium Risk

1. **Multi-Turn State Management**
   - **Risk**: State may become inconsistent across turns
   - **Mitigation**: Extensive logging, state snapshots for debugging
   - **Testing**: Comprehensive multi-turn tests

2. **Entity Extraction Accuracy**
   - **Risk**: NLU may miss entities or extract wrong types
   - **Mitigation**: Use examples in prompts, retry on failure
   - **Fallback**: Use raw text if no entities found

### Low Risk

1. **Performance**
   - **Risk**: LLM calls may be slow
   - **Mitigation**: Use Haiku for fast responses, cache where possible
   - **Acceptable**: <5s per turn is acceptable for demo

---

## Next Steps

1. **Create beads tasks** for all 25 tasks across 6 phases
2. **Start with Phase 1** (answer validation) - highest impact, no API dependency
3. **Verify Phase 2** (NLU engine) with real API calls
4. **Complete Phase 3** (multi-turn) to prove full loop
5. **Polish Phases 4-6** for production readiness

---

## Appendix: Key Files

### Core Implementation
- `src/ibdm/core/domain.py` - Domain model
- `src/ibdm/domains/nda_domain.py` - NDA domain
- `src/ibdm/rules/integration_rules.py` - Integration rules (needs Phase 1 updates)
- `src/ibdm/rules/generation_rules.py` - Generation rules (complete)
- `src/ibdm/engine/nlu_engine.py` - NLU engine (needs Phase 2 verification)

### Tests
- `tests/integration/test_complete_nda_workflow.py` - Workflow tests (needs expansion)
- `tests/integration/test_nlu_engine_causation.py` - NLU tests (needs API tests)

### Documentation
- `docs/CAUSATION_CHAIN_ANALYSIS.md` - Current causation analysis
- `docs/COMPLETE_DIALOGUE_LOOP_PLAN.md` - This document
- `CLAUDE.md` - Development policies

### Demo
- `demos/03_nlu_integration_interactive.py` - Interactive demo (needs Phase 5 updates)
