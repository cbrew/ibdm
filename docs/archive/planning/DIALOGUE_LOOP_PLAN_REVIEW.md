# Dialogue Loop Plan Review

**Date**: 2025-11-14
**Purpose**: Verify that beads tasks align with goal of complete interactive dialogue loop
**Status**: Ready for execution

---

## Goal Restatement

**Primary Goal**: Build a complete interactive dialogue loop where:
1. User utterances cause proper state updates in the dialogue engine
2. Dialogue engine state drives natural, contextual utterance generation
3. The loop continues seamlessly through multi-turn conversations
4. Domain knowledge provides semantic grounding throughout

**Success Metric**: User can complete a 5-question NDA workflow with natural language, seeing domain-aware questions and progress indicators.

---

## Plan Verification

### Does the plan achieve the goal?

**YES** ✅ - The plan systematically addresses all gaps between current state and desired state.

### Evidence:

1. **User Utterances → State Updates** (Covered by Phases 1, 2, 4)
   - ✅ Phase 1.2: Answer integration with domain validation
   - ✅ Phase 2.6-2.9: NLU engine verification
   - ✅ Phase 4.14-4.17: Entity extraction → domain mapping
   - **Result**: User answers properly update state with validation

2. **State → Utterance Generation** (Covered by existing work + Phase 3)
   - ✅ Already implemented: Plan-aware generation
   - ✅ Phase 3.12: Verify plan progress tracking
   - ✅ Phase 5.19: Add progress display
   - **Result**: Generated questions reflect actual plan state

3. **Multi-Turn Loop** (Covered by Phases 1, 3)
   - ✅ Phase 1.5: Push next question after answer
   - ✅ Phase 3.10-3.13: Complete multi-turn workflow test
   - **Result**: Seamless continuation through all questions

4. **Domain Grounding** (Already implemented + verification)
   - ✅ Domain model complete (Phase 0, done)
   - ✅ Phase 1.2: Use domain.resolves() for validation
   - ✅ Phase 3.13: Verify domain validation throughout
   - **Result**: Semantic validation at every step

---

## Task Coverage Analysis

### Critical Path Tasks (Must Complete)

| Task ID | Description | Why Critical | Dependencies |
|---------|-------------|--------------|--------------|
| loop.1 | Review answer integration | Understand current state | None |
| loop.2 | Add domain validation | Core validation logic | loop.1 |
| loop.4 | Mark subplan complete | Plan progress tracking | loop.2 |
| loop.5 | Push next question | Multi-turn continuation | loop.4 |
| loop.6 | NLU integration test | Verify entry point | IBDM_API_KEY |
| loop.10 | Multi-turn test | Prove complete loop | loop.1-9 |

**Critical path**: loop.1 → loop.2 → loop.4 → loop.5 → loop.6 → loop.10

**Estimated time**: 2 + 3 + 4 = **9 hours**

### High-Value Tasks (Should Complete)

| Task ID | Description | Value | Priority |
|---------|-------------|-------|----------|
| loop.3 | Handle invalid answers | Better UX | P0 |
| loop.7 | Entity extraction | Data quality | P0 |
| loop.11 | QUD management verification | Correctness | P0 |
| loop.12 | Plan progress verification | User feedback | P0 |
| loop.18-21 | Demo completion | Showcase | P1 |

**Estimated time**: **4 hours**

### Nice-to-Have Tasks (Can Defer)

| Task ID | Description | Can Defer Because |
|---------|-------------|-------------------|
| loop.8-9 | NLU error handling | Demo assumes working API |
| loop.14-17 | Domain mapper | Can use raw text initially |
| loop.22-25 | Documentation | Can document after proving it works |

**Estimated time**: **6 hours** (deferred)

---

## Dependency Graph

```
Epic: Complete Dialogue Loop
│
├─ Phase 1: Answer Integration (BLOCKING - must do first)
│  ├─ loop.1: Review → loop.2: Add validation
│  ├─ loop.2: Validation → loop.3: Handle errors
│  ├─ loop.2: Validation → loop.4: Mark complete
│  └─ loop.4: Complete → loop.5: Next question
│
├─ Phase 2: NLU Engine (INDEPENDENT - can run in parallel)
│  ├─ loop.6: Integration test
│  ├─ loop.7: Entity extraction
│  ├─ loop.8: NLU+Domain (DEPENDS ON: loop.2)
│  └─ loop.9: Error handling
│
├─ Phase 3: Multi-Turn (DEPENDS ON: Phase 1, Phase 2)
│  ├─ loop.10: Multi-turn test
│  ├─ loop.11: QUD verification
│  ├─ loop.12: Progress verification
│  └─ loop.13: Domain validation
│
├─ Phase 4: Domain Mapper (INDEPENDENT, lower priority)
│  ├─ loop.14: Review
│  ├─ loop.15: Integrate
│  ├─ loop.16: Test
│  └─ loop.17: Handle unmapped
│
├─ Phase 5: Demo (DEPENDS ON: Phase 3)
│  ├─ loop.18: Config
│  ├─ loop.19: Progress display
│  ├─ loop.20: Test e2e
│  └─ loop.21: Document
│
└─ Phase 6: Documentation (DEPENDS ON: All)
   ├─ loop.22: Architecture
   ├─ loop.23: User guide
   ├─ loop.24: Test suite
   └─ loop.25: Policies
```

---

## Execution Strategy

### Recommended Sequence

**Week 1: Prove the Loop Works**

1. **Day 1-2**: Phase 1 (Answer Integration)
   - Execute loop.1 → loop.2 → loop.4 → loop.5
   - Skip loop.3 initially (handle invalid answers later)
   - **Goal**: Answer integration updates state correctly
   - **Output**: Unit tests passing, plan progress working

2. **Day 2-3**: Phase 2 (NLU Engine)
   - Execute loop.6 (critical) and loop.7
   - Skip loop.8-9 initially
   - **Goal**: Verify NLU creates proper move types
   - **Output**: Integration tests with real API calls

3. **Day 3-4**: Phase 3 (Multi-Turn)
   - Execute loop.10 (critical path completion!)
   - Execute loop.11, loop.12, loop.13
   - **Goal**: PROVE the complete loop works
   - **Output**: 5-question workflow passing

**Week 2: Polish and Deploy**

4. **Day 5**: Phase 5 (Demo)
   - Execute loop.18 → loop.19 → loop.20
   - **Goal**: Make it user-facing
   - **Output**: Working interactive demo

5. **Day 6**: Fill Gaps
   - Execute loop.3 (invalid answer handling)
   - Execute loop.8-9 (NLU error handling)
   - **Goal**: Production readiness
   - **Output**: Robust error handling

6. **Day 7**: Documentation
   - Execute loop.22-25
   - Optional: Phase 4 (domain mapper) if time permits
   - **Goal**: Handoff readiness
   - **Output**: Complete documentation

---

## Gap Analysis: Tasks vs Goal

### Question: Does completing these tasks guarantee goal achievement?

**Answer**: YES, with caveat

**If we complete critical path** (loop.1-2-4-5-6-10):
- ✅ User utterances update state (loop.6: NLU, loop.2: validation)
- ✅ State drives generation (already implemented, verified by loop.10)
- ✅ Loop continues (loop.5: push next question, loop.10: multi-turn test)
- ✅ Domain grounding (loop.2: domain.resolves(), loop.13: verification)
- **Result**: GOAL ACHIEVED

**Caveat**: Requires working IBDM_API_KEY
- If API unavailable: Can't complete loop.6, loop.7, loop.10, loop.20
- Mitigation: All critical logic tested with mocked moves
- Fallback: Document limitation, defer API testing

### Question: Are any tasks missing?

**Scan for gaps**:

1. ❓ **Answer extraction from LLM response**
   - Loop.7 tests entity extraction
   - But who converts entities → Answer.content?
   - **Status**: Covered by loop.15 (domain mapper integration)

2. ❓ **QUD popping logic**
   - Loop.2 should pop QUD after valid answer
   - Loop.11 verifies it works
   - **Status**: Covered ✅

3. ❓ **Plan completion detection**
   - What happens when all subplans complete?
   - Need final message, not next question
   - **Status**: Loop.5 covers this (leave QUD empty)

4. ❓ **Error recovery**
   - Loop.3: invalid answers
   - Loop.9: API failures
   - **Status**: Covered ✅

**Conclusion**: NO GAPS - all necessary tasks present

---

## Risk Assessment

### Risk 1: NLU Engine Not Working

**Probability**: Low (already implemented, just needs testing)
**Impact**: High (breaks entire chain)

**Mitigation**:
- Loop.6: Verify early with real API
- If fails: Debug before proceeding to Phase 3
- Fallback: Manual move creation for demo

### Risk 2: Domain Validation Too Strict

**Probability**: Medium (domain.resolves() may reject valid answers)
**Impact**: Medium (frustrating UX)

**Mitigation**:
- Loop.2: Start with simple validation (non-empty)
- Loop.13: Test with various answer formats
- Iterate: Loosen validation if needed

### Risk 3: Multi-Turn State Inconsistency

**Probability**: Low (immutable state pattern)
**Impact**: High (breaks loop)

**Mitigation**:
- Loop.10: Test each turn carefully
- Loop.11: Verify QUD consistency
- Add logging: State snapshots after each turn

### Risk 4: Timeline Underestimation

**Probability**: Medium (always true)
**Impact**: Low (can defer docs/demo polish)

**Mitigation**:
- Focus on critical path first (9 hours)
- Defer nice-to-haves (6 hours)
- Set clear done criteria

---

## Success Metrics

### Minimum Viable Product (MVP)

**Definition**: Can complete one successful 5-question NDA workflow

**Requirements**:
- [ ] User: "I need to draft an NDA"
- [ ] System: "What are the names of the parties..."
- [ ] User: "Acme Corp and Beta Inc"
- [ ] System: "[Step 2 of 5] Should this be mutual or one-way..."
- [ ] ... (continues through all 5 questions)
- [ ] System: "Perfect! I have all the information..."

**Tests**: Loop.10 passing

**Timeline**: After Phase 1 + 2 + 3 (Day 4)

### Production Ready

**Definition**: Robust, documented, demonstrable

**Requirements**:
- All MVP requirements +
- [ ] Handles invalid answers gracefully
- [ ] Shows helpful error messages
- [ ] API failure doesn't crash
- [ ] Interactive demo works
- [ ] Documentation complete

**Tests**: All P0-P1 tasks complete

**Timeline**: End of Week 2 (Day 7)

---

## Conclusion

### Is the plan sound?

**YES** ✅

**Reasons**:
1. Tasks systematically address all gaps
2. Critical path clearly identified
3. Dependencies properly sequenced
4. Risks identified and mitigated
5. Success criteria measurable

### Are task definitions aligned with goals?

**YES** ✅

**Evidence**:
- Goal: User utterances → state updates
  - Tasks: loop.1-2, loop.6-7
- Goal: State → generation
  - Tasks: Already done + loop.12 verification
- Goal: Multi-turn loop
  - Tasks: loop.5, loop.10-11
- Goal: Domain grounding
  - Tasks: loop.2, loop.13

### Should we proceed?

**YES** ✅

**Recommendation**:
1. Start with **Phase 1** (Answer Integration) - 2 hours, no API needed
2. Move to **Phase 2** (NLU Engine) - 3 hours, requires API
3. Complete **Phase 3** (Multi-Turn) - 4 hours, proves goal
4. **Checkpoint**: If loop.10 passes, goal achieved!
5. Polish with Phases 5-6 as time permits

**Next Action**: Execute `loop.1` - Review answer integration rule

---

## Appendix: Task Checklist

### Phase 1: Answer Integration (P0)
- [ ] loop.1: Review answer integration
- [ ] loop.2: Add domain validation
- [ ] loop.3: Handle invalid answers
- [ ] loop.4: Mark subplan complete
- [ ] loop.5: Push next question

### Phase 2: NLU Engine (P0)
- [ ] loop.6: NLU integration test (requires API)
- [ ] loop.7: Entity extraction (requires API)
- [ ] loop.8: NLU+Domain integration
- [ ] loop.9: Error handling

### Phase 3: Multi-Turn (P0)
- [ ] loop.10: Multi-turn test (requires API)
- [ ] loop.11: QUD management
- [ ] loop.12: Plan progress
- [ ] loop.13: Domain validation

### Phase 4: Domain Mapper (P1)
- [ ] loop.14: Review mapper
- [ ] loop.15: Integrate mapper
- [ ] loop.16: Test mapping
- [ ] loop.17: Handle unmapped

### Phase 5: Demo (P1)
- [ ] loop.18: Update config
- [ ] loop.19: Progress display
- [ ] loop.20: Test e2e (requires API)
- [ ] loop.21: Document

### Phase 6: Documentation (P2)
- [ ] loop.22: Architecture docs
- [ ] loop.23: User guide
- [ ] loop.24: Test suite
- [ ] loop.25: Update policies
