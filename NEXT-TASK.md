# Next Recommended Task

**Date**: 2025-11-16 (Updated - Beads Synchronized!)
**Basis**: IBIS_VARIANTS_PRIORITY.md, IBiS3 end-to-end verified, beads tasks reprioritized
**Status**: 🎉 Week 3 complete, IBiS3 rule chain verified! Beads tasks created and prioritized!

---

## ✅ Week 1 Complete: IBiS3 Foundation Implemented!

**Completed** (2025-11-16):
- ✅ Phase separation verified (task plan formation in INTEGRATION phase)
- ✅ `private.issues` field added to PrivateIS
- ✅ Serialization updated (to_dict/from_dict with type safety)
- ✅ Tests written and passing (97/97 core tests)
- ✅ Type checks clean (pyright 0 errors)
- ✅ Committed and pushed: `feat(ibis3): add private.issues field to InformationState`

**Progress**: IBiS3 30% → 35% (foundation infrastructure complete)

---

## ✅ Week 2 Complete: IBiS3 Accommodation Rules Implemented!

**Completed** (2025-11-16):
- ✅ Rule 4.1 (IssueAccommodation) - questions from plans → private.issues
- ✅ Rule 4.2 (LocalQuestionAccommodation) - issues → QUD incrementally
- ✅ Volunteer information handling - check private.issues before QUD
- ✅ Modified _form_task_plan to NOT push to QUD directly
- ✅ Modified _integrate_answer to handle volunteer answers
- ✅ 11 new tests passing, 155 total core tests passing
- ✅ Type checks clean (pyright 0 errors)
- ✅ Committed and pushed: 3 commits implementing Rules 4.1, 4.2, and volunteer info

**Commits**:
- `feat(ibis3): implement Rule 4.1 (IssueAccommodation)`
- `feat(ibis3): implement Rule 4.2 (LocalQuestionAccommodation)`
- `feat(ibis3): handle volunteer information in integrate_answer`

**Progress**: IBiS3 35% → 50% (core accommodation rules working)

**Key Achievement**: Natural dialogue with volunteer information now works!
```
System: "What are the parties?"
User: "Acme and Smith, effective January 1, 2025"
System: [Accommodates date to private.issues, processes as volunteer answer]
System: "What's the governing law?" ← SKIPS ALREADY-ANSWERED QUESTION!
```

---

## ✅ Week 3 Complete: IBiS3 End-to-End Testing & Bug Fixes!

**Completed** (2025-11-16):
- ✅ Created comprehensive end-to-end integration tests (`test_ibis3_end_to_end.py`)
- ✅ Discovered and fixed 3 critical bugs in rule chain
- ✅ All IBiS3 tests passing (3/3 end-to-end tests)
- ✅ Removed obsolete IBiS1 tests expecting old behavior
- ✅ Verified complete rule chain: Rule 4.1 → Rule 4.2 → SelectAsk

**Bugs Fixed**:
1. **Rule Priority Bug**: form_task_plan now runs BEFORE accommodate_issue_from_plan
2. **Fallback Selection Bug**: Fallback only fires when agenda is empty
3. **Plan Progression Bug**: Removed direct QUD push, Rule 4.2 handles raising

**Commits**:
- `test(ibis3): add end-to-end integration tests for IBiS3 rule chain`
- `fix(ibis3): fix rule priorities and implement incremental questioning`

**Progress**: IBiS3 50% → 60% (rule chain verified and working)

**Key Achievement**: Incremental questioning verified end-to-end!
```
Turn 1:
  - Plan created with 5 questions
  - All 5 questions → private.issues (Rule 4.1)
  - First question → QUD (Rule 4.2)
  - System asks: "What are the parties?"

Turn 2:
  - User answers: "Acme Corp and Smith Inc"
  - Answer integrated, question popped from QUD
  - Next question raised from issues → QUD (Rule 4.2)
  - System asks next question

✅ ONE QUESTION AT A TIME (incremental questioning working!)
```

---

## 🎯 NEXT PRIORITY: Documentation & Consolidation

**Current Focus**: Week 4 - Document achievements and prepare for next features
**Duration**: 1-2 days
**Blockers**: None - IBiS3 core working!

**✅ Beads Tasks Created**: ibdm-89, ibdm-90, ibdm-91, ibdm-92, ibdm-93, ibdm-94, ibdm-95

---

## Week 4 Tasks: Consolidation & Documentation (P0 Priority)

### ibdm-89: Update SYSTEM_ACHIEVEMENTS.md ⚡ NEXT

**Priority**: P0
**Duration**: 1 hour

**What to Do**:
- Document Week 3 completion (IBiS3 rule chain verified)
- Add section on bugs discovered and fixed
- Note the importance of rule priority ordering
- Document incremental questioning achievement

**Beads Command**: `~/go/bin/bd show ibdm-89`

---

### ibdm-90: Update LARSSON_PRIORITY_ROADMAP.md

**Priority**: P0
**Duration**: 30 min

**What to Do**:
- Mark Rules 4.1 (IssueAccommodation) and 4.2 (LocalQuestionAccommodation) as complete
- Update IBiS3 progress: 60% → 65%
- Document volunteer information handling
- Note test coverage improvements

**Beads Command**: `~/go/bin/bd show ibdm-90`

---

### ibdm-91: Create IBiS3 Implementation Guide

**Priority**: P0
**Duration**: 2 hours

**What to Do**:
- Create `docs/ibis3_implementation.md`
- Overview of Rules 4.1 and 4.2
- How questions flow: plan → issues → QUD
- Volunteer information handling
- Testing approach
- Common pitfalls (rule priorities, fallback behavior)

**Beads Command**: `~/go/bin/bd show ibdm-91`

---

### ibdm-92: NLU Interface Adoption ⚡ RECOMMENDED

**Priority**: P0
**Duration**: 4-6 hours

**What to Do**:
1. Create `src/ibdm/nlu/nlu_service_adapter.py` wrapping current `NLUEngine`
2. Create `tests/mocks/mock_nlu_service.py` for testing
3. Use interface in dialogue manager tests
4. Document IBiS3 NLU requirements

**Benefits**:
- Test dialogue managers independently of NLU complexity
- Clear contract for what NLU must provide
- Easy to compare different NLU approaches
- Progressive enhancement path (IBiS1 → IBiS3 → IBiS2 → IBiS4)

**Beads Command**: `~/go/bin/bd show ibdm-92`

---

## Week 5+ Tasks: Next IBiS3 Features (P1 Priority)

### ibdm-93: Implement Rule 4.3 (IssueClarification)

**Priority**: P1 (after Week 4 documentation)
**Duration**: 3-5 days
**Goal**: Handle ambiguous utterances with clarification questions

**What to Do**:
- Review Larsson Section 4.6.3 (clarification)
- Design precondition and effect functions
- Implement clarification question accommodation
- Add tests for ambiguous utterance handling

**Why Next**: Natural complement to Rules 4.1, 4.2; improves dialogue robustness

**Beads Command**: `~/go/bin/bd show ibdm-93`

---

### ibdm-94: Implement Rule 4.4 (DependentIssueAccommodation)

**Priority**: P1
**Duration**: 3-5 days
**Goal**: Handle questions that depend on other questions being answered first

**What to Do**:
- Review Larsson Section 4.6.4 (dependent issues)
- Design dependency detection and ordering
- Implement dependent issue accommodation
- Add tests for question dependencies

**Beads Command**: `~/go/bin/bd show ibdm-94`

---

### ibdm-95: Implement Rule 4.5 (QuestionReaccommodation)

**Priority**: P1
**Duration**: 3-5 days
**Goal**: Re-prioritize unresolved questions based on dialogue context

**What to Do**:
- Review Larsson Section 4.6.5 (reaccommodation)
- Design reaccommodation triggers and logic
- Implement question re-prioritization
- Add tests for dynamic question ordering

**Beads Command**: `~/go/bin/bd show ibdm-95`

---

## Progress Tracking

**IBiS3 Completion**:
- Week 1: ✅ Foundation (30% → 35%)
- Week 2: ✅ Rules 4.1-4.2 (35% → 50%)
- Week 3: ✅ End-to-end testing (50% → 60%)
- Week 4: 📋 Documentation + NLU interface (60% → 65%)
- Week 5-6: 📋 Rule 4.3 - Clarification (65% → 75%)
- Week 7-8: 📋 Rule 4.4 - Dependent issues (75% → 85%)
- Week 9-10: 📋 Rule 4.5 - Reaccommodation (85% → 95%)
- Week 11: 📋 Integration tests + polish (95% → 100%)

**Current**: 60% complete
**Target**: 65% by end of Week 4

**Beads Status**:
- **P0 Tasks**: 4 (Week 4 documentation + NLU interface)
- **P1 Tasks**: 3 (IBiS3 Rules 4.3-4.5)
- **P2 Tasks**: 108 (demos, refactoring, NLU/NLG separation - deferred)
- **P3 Tasks**: 37 (metrics framework - deferred)

---

## Larsson References

**Implemented**:
- ✅ **Section 4.6.1**: IssueAccommodation rule (Rule 4.1)
- ✅ **Section 4.6.2**: LocalQuestionAccommodation rule (Rule 4.2)

**Next**:
- 📋 **Section 4.6.3**: IssueClarification (Rule 4.3)
- 📋 **Section 4.6.4**: DependentIssueAccommodation (Rule 4.4)
- 📋 **Section 4.6.5**: QuestionReaccommodation (Rule 4.5)

---

## Bottom Line

**Immediate Next Steps** (Week 4 - P0 Priority):
1. ⚡ **ibdm-89**: Update SYSTEM_ACHIEVEMENTS.md - 1 hour
2. ⚡ **ibdm-90**: Update LARSSON_PRIORITY_ROADMAP.md - 30 min
3. 📋 **ibdm-91**: Create IBiS3 implementation guide - 2 hours
4. ⚡ **ibdm-92**: NLU Interface Adoption - 4-6 hours
   - Create NLUServiceAdapter wrapping current NLUEngine
   - Create Mock NLU for testing
   - Use interface in dialogue manager tests
   - Document IBiS3 NLU requirements

**After Week 4** (P1 Priority):
5. 🔮 **ibdm-93**: Implement Rule 4.3 (IssueClarification) - 3-5 days
6. 🔮 **ibdm-94**: Implement Rule 4.4 (DependentIssueAccommodation) - 3-5 days
7. 🔮 **ibdm-95**: Implement Rule 4.5 (QuestionReaccommodation) - 3-5 days

**Total Week 4 Effort**: 2-3 days
**Goal**: IBiS3 60% → 65% + NLU interface adoption
**Outcome**: Documented achievements, NLU interface in use, ready for Rules 4.3-4.5

**Beads Integration**: ✅ All tasks created, old tasks winnowed, priorities aligned with IBiS3 focus

**Key Insight**: NLU interface enables testing IBiS variants independently of NLU complexity!

**Use Beads**: Run `~/go/bin/bd ready --priority 0` to see P0 tasks, or `~/go/bin/bd show ibdm-89` to start!

Ready to consolidate! 📚
