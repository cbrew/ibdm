# IBDM Architecture Refactoring Plan: Moving Accommodation to Integration Phase

**Date**: 2025-11-13
**Issue**: Task accommodation (plan creation) is in INTERPRETATION phase, should be in INTEGRATION phase
**Goal**: Align implementation with Larsson's IBDM theoretical framework
**Branch**: `claude/refactor-accommodation-integration-[session-id]`

---

## Executive Summary

This refactoring moves task accommodation logic from the interpretation phase to the integration phase, where it belongs according to Larsson (2002). This enables:

1. NLU engine to work with task accommodation
2. Separation of syntactic (interpret) from semantic (integrate) processing
3. Reusable accommodation logic for any interpretation method
4. Better conversational behavior in demos

---

## Architecture: Before vs After

### Before (Current - INCORRECT)

```
INTERPRET (interpretation_rules.py):
  ├─ accommodate_nda_task ← Creates plan (WRONG PHASE)
  ├─ Uses expensive LLM classification
  └─ Rule never executes when using NLU engine

INTEGRATE (integration_rules.py):
  └─ integrate_request ← Just tracks move, no accommodation

Result: NLU engine can't create plans → System can't ask NDA questions
```

### After (Target - CORRECT)

```
INTERPRET (interpretation_rules.py):
  ├─ interpret_request ← Simple keyword detection
  └─ Creates basic request move (no plan)

INTEGRATE (integration_rules.py):
  ├─ accommodate_request ← Infer task, create plan (RIGHT PHASE)
  ├─ Push first question to QUD
  └─ Works with both rule-based AND NLU interpretation

Result: Both rule-based and NLU engines can trigger accommodation
```

---

## Implementation Phases

### Phase 1: Refactor Interpretation Rules (Remove Accommodation)

**Goal**: Make interpretation lightweight and syntactic-only

**Files**:
- `src/ibdm/rules/interpretation_rules.py`

**Steps**:

1.1. **Add simple request detection rule**
   - Add `interpret_request` rule with keyword matching
   - Precondition: `_is_request()` checks for keywords: "need", "want", "draft", "create", "require"
   - Effect: `_create_request_move()` creates basic request move with utterance text
   - Priority: 11 (high, but below greetings)
   - No LLM calls, no plan creation

1.2. **Deprecate (but don't remove) NDA accommodation rule**
   - Rename `accommodate_nda_task` → `accommodate_nda_task_DEPRECATED`
   - Lower priority to 0 (effectively disabled)
   - Add deprecation comment explaining it will be removed in Phase 2
   - Keep code for reference during migration

1.3. **Update tests**
   - Add test for `interpret_request` rule
   - Verify it creates request moves without plans
   - Update existing tests that expect plan creation in interpretation

**Deliverable**: Request detection works, creates moves, no plans yet (plan creation disabled)

**Tests**:
```bash
pytest tests/unit/test_interpretation_rules.py::test_interpret_request -v
pytest tests/unit/test_interpretation_rules.py -v  # All should pass
```

---

### Phase 2: Add Accommodation to Integration Rules

**Goal**: Implement task accommodation in the correct phase

**Files**:
- `src/ibdm/rules/integration_rules.py`

**Steps**:

2.1. **Add accommodation infrastructure**
   - Add `accommodate_request` integration rule
   - Precondition: `_is_request_move()` or `_is_command_move()`
   - Effect: `_accommodate_request_task()`
   - Priority: 13 (highest - run before other integrations)

2.2. **Implement task classification in integration**
   - Move task classifier import to integration_rules.py
   - Implement `_accommodate_request_task()`:
     - Get task classifier
     - Classify utterance content
     - Dispatch to task-specific handlers
   - Add caching to avoid re-classification

2.3. **Move NDA accommodation logic**
   - Copy `_create_nda_plan()` from interpretation_rules.py
   - Rename to `_accommodate_nda_task()`
   - Update to work with request move instead of utterance
   - Add plan to `state.private.plan`
   - Push first question to `state.shared.qud`

2.4. **Handle both request and command move types**
   - Ensure both move types trigger accommodation
   - Unified logic path for NLU (command) and rules (request)

2.5. **Update integration for request moves**
   - Modify existing `_integrate_request()`:
     - Check if plan already created by accommodation
     - Set `next_speaker` appropriately
     - Track move in history

**Deliverable**: Request moves trigger plan creation in integration phase

**Tests**:
```bash
pytest tests/unit/test_integration_rules.py::test_accommodate_request -v
pytest tests/unit/test_integration_rules.py::test_accommodate_nda -v
pytest tests/integration/test_nda_workflow.py -v
```

---

### Phase 3: Clean Up and Remove Deprecated Code

**Goal**: Remove old accommodation code from interpretation phase

**Files**:
- `src/ibdm/rules/interpretation_rules.py`

**Steps**:

3.1. **Remove deprecated NDA accommodation rule**
   - Delete `accommodate_nda_task_DEPRECATED` rule
   - Delete `_is_nda_request()` function
   - Delete `_create_nda_plan()` function (now in integration_rules.py)

3.2. **Remove task classifier from interpretation**
   - Remove `_task_classifier` global
   - Remove `_get_task_classifier()` function
   - Remove task classifier imports

3.3. **Update documentation**
   - Update docstrings to reflect interpretation is syntactic only
   - Add references to integration rules for accommodation

**Deliverable**: Clean codebase with clear separation of concerns

**Tests**:
```bash
pytest tests/unit/test_interpretation_rules.py -v
pytest tests/unit/test_integration_rules.py -v
```

---

### Phase 4: Enhance NLG with Plan Context

**Goal**: Generate context-aware responses based on active plans

**Files**:
- `src/ibdm/rules/generation_rules.py`

**Steps**:

4.1. **Add plan-aware question generation**
   - Update `_generate_question_text()` to check for active plans
   - Add helper: `_get_active_plan(state)` → returns current plan or None
   - Add NDA-specific templates for each question type

4.2. **Implement NDA question templates**
   - Parties question: "Let's start with the parties. Who are the organizations entering into this NDA?"
   - NDA type question: "Will this be a mutual NDA or a one-way NDA?"
   - Effective date: "What effective date should we use for this agreement?"
   - Duration: "How long should the confidentiality obligations last?"
   - Governing law: "Which state's laws should govern this agreement - California or Delaware?"

4.3. **Add plan progress feedback**
   - Show progress in acknowledgments: "Great! That's 2 of 5 requirements."
   - Final confirmation: "I have all the information needed. Would you like me to generate the NDA?"

4.4. **Fallback to generic generation**
   - If no active plan context, use existing generic templates
   - Maintain backward compatibility

**Deliverable**: Natural, context-aware dialogue for NDA workflow

**Tests**:
```bash
pytest tests/unit/test_generation_rules.py::test_plan_aware_generation -v
pytest tests/integration/test_nda_conversation.py -v
```

---

### Phase 5: Update NLU Engine Integration

**Goal**: Ensure NLU engine works seamlessly with new accommodation

**Files**:
- `src/ibdm/engine/nlu_engine.py`

**Steps**:

5.1. **Verify NLU engine creates appropriate move types**
   - Check that NLU creates "command" or "request" moves for task requests
   - Ensure move content includes full utterance text
   - Verify metadata is populated with NLU confidence scores

5.2. **Test integration path**
   - NLU interpret → creates move
   - Base class integrate → applies accommodation rules
   - Verify plan is created correctly

5.3. **Add logging for debugging**
   - Log when NLU creates request/command moves
   - Log when accommodation is triggered
   - Log plan creation and QUD updates

**Deliverable**: NLU engine triggers accommodation correctly

**Tests**:
```bash
pytest tests/integration/test_nlu_accommodation.py -v
python demos/03_nlu_integration_interactive.py  # Manual test
```

---

### Phase 6: Integration Testing and Demo Verification

**Goal**: Verify complete workflow end-to-end

**Files**:
- `tests/integration/test_complete_nda_workflow.py` (new)
- `demos/03_nlu_integration_interactive.py`

**Steps**:

6.1. **Create comprehensive integration test**
   - Test complete NDA workflow:
     - User: "I need to draft an NDA"
     - System asks about parties
     - User provides parties
     - System asks about NDA type
     - ... continue through all 5 questions
     - Verify final confirmation

6.2. **Test with both interpretation methods**
   - Test with rule-based interpretation
   - Test with NLU interpretation
   - Verify identical behavior (plan creation, QUD management)

6.3. **Manual testing with interactive demo**
   - Run demo with real LLM
   - Verify natural conversation flow
   - Test various phrasings: "need NDA", "draft NDA", "create confidentiality agreement"
   - Verify plan execution and question sequencing

6.4. **Performance testing**
   - Measure latency with accommodation in integration
   - Compare to baseline (current implementation)
   - Ensure no significant performance regression

**Deliverable**: Fully working NDA workflow with natural conversation

**Tests**:
```bash
pytest tests/integration/test_complete_nda_workflow.py -v
# Manual: python demos/03_nlu_integration_interactive.py
```

---

### Phase 7: Documentation and Cleanup

**Goal**: Update all documentation to reflect new architecture

**Files**:
- `docs/burr_state_refactoring.md`
- `docs/architecture_interpretation_accommodation.md`
- `CLAUDE.md`
- `README.md`

**Steps**:

7.1. **Update architecture documentation**
   - Update burr_state_refactoring.md with accommodation in integration
   - Mark ARCHITECTURE_ISSUE_SUMMARY.md as resolved
   - Add "Resolved: YYYY-MM-DD" banner

7.2. **Update code comments**
   - Add comments explaining accommodation in integration rules
   - Reference Larsson (2002) in relevant docstrings
   - Add examples in docstrings

7.3. **Update CLAUDE.md policy**
   - Document that accommodation belongs in integration phase
   - Add architectural principle: "Interpretation is syntactic, Integration is semantic"
   - Reference this refactoring as example

7.4. **Update demo documentation**
   - Update demos/README.md with new behavior description
   - Add example conversation showing plan-driven dialogue
   - Document the architectural improvement

**Deliverable**: Complete, accurate documentation

---

## Risk Mitigation

### Risk 1: Breaking Existing Functionality
- **Mitigation**: Run full test suite after each phase
- **Rollback**: Small commits allow easy git revert

### Risk 2: Performance Regression
- **Mitigation**: Benchmark before/after in Phase 6
- **Contingency**: Add caching for task classification

### Risk 3: NLU Engine Incompatibility
- **Mitigation**: Test both rule-based and NLU paths in Phase 5
- **Contingency**: Add compatibility shim if needed

### Risk 4: Test Failures
- **Mitigation**: Update tests incrementally with each phase
- **Contingency**: Fix tests before moving to next phase

---

## Success Criteria

### Functional
- ✅ NDA demo workflow executes plan-driven dialogue
- ✅ System asks specific NDA questions in sequence
- ✅ Both rule-based and NLU interpretation trigger accommodation
- ✅ All existing tests pass
- ✅ New integration tests pass

### Architectural
- ✅ Accommodation logic is in integration phase (not interpretation)
- ✅ Interpretation phase is lightweight and syntactic
- ✅ Code follows Larsson's IBDM framework
- ✅ Clear separation of concerns

### User Experience
- ✅ Natural conversation flow in demo
- ✅ Context-aware questions from system
- ✅ Progress feedback during NDA collection
- ✅ No performance regression

---

## Timeline Estimate

| Phase | Estimated Time | Dependencies |
|-------|---------------|--------------|
| Phase 1 | 2 hours | None |
| Phase 2 | 3 hours | Phase 1 |
| Phase 3 | 1 hour | Phase 2 |
| Phase 4 | 2 hours | Phase 3 |
| Phase 5 | 1 hour | Phase 4 |
| Phase 6 | 2 hours | Phase 5 |
| Phase 7 | 1 hour | Phase 6 |
| **Total** | **12 hours** | Sequential |

---

## Post-Implementation

### Follow-up Tasks
1. Add more task types (beyond NDA)
2. Implement multi-turn clarification dialogues
3. Add confidence-based confirmation requests
4. Enhance error recovery for plan failures

### Lessons Learned
- Document architectural decisions early
- Align implementation with theoretical framework
- Test both interpretation methods (rules + NLU)
- Keep accommodation logic reusable

---

## References

1. Larsson, S. (2002). *Issue-based Dialogue Management*. PhD Thesis, Göteborg University.
2. `docs/architecture_interpretation_accommodation.md` - Detailed architectural analysis
3. `ARCHITECTURE_ISSUE_SUMMARY.md` - Quick reference
4. `docs/burr_state_refactoring.md` - Burr integration design

---

## Approval

- [ ] Plan reviewed
- [ ] Beads tasks created
- [ ] Branch created
- [ ] Ready to implement

**Approved by**: _______________
**Date**: _______________
