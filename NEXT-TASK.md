# Next Recommended Task

**Date**: 2025-11-16 (Updated for IBiS Variants Priority)
**Basis**: IBIS_VARIANTS_PRIORITY.md, code verification, Larsson thesis compliance

---

## Status Update: New Priority - Complete IBiS-2, 3, 4 Variants 🎯

### Current IBiS Status

**Current State** (Verified from IBIS_PROGRESSION_GUIDE.md):
- ✅ **IBiS1**: 100% complete (Core QUD, Plans, Four-phase control loop)
- ⚠️ **IBiS2**: 60% complete (Basic grounding, missing advanced ICM)
- 🔧 **IBiS3**: 30% complete (Architecture ready, accommodation incomplete)
- 📋 **IBiS4**: 10% complete (Structure defined, not yet implemented)

**New Goal**: Complete all IBiS variants to achieve full Larsson (2002) compliance

---

## HIGHEST PRIORITY: Unblock IBiS3 Accommodation

**Task**: Fix architectural violation blocking IBiS3 implementation
**Duration**: 1 week
**Blockers**: None (this IS the blocker removal)

### Critical Blocker

**Current Issue**: Task plan formation is in INTERPRET phase (architectural violation)
- **What's Wrong**: Accommodation happens in wrong phase
- **Larsson Violation**: Interpretation = syntactic, Integration = pragmatic
- **Impact**: Blocks all IBiS3 accommodation work
- **Fix**: `ibdm-accom` epic - move to integration phase

### Week 1: Unblock IBiS3 (IMMEDIATE)

**1. Fix Phase Separation Violation**
- **Task**: `ibdm-accom` - Move accommodation to integration
- **What**:
  - Verify task plan formation is in `integration_rules.py`
  - Ensure NO accommodation in interpretation phase
  - Update all tests
- **Why**: BLOCKS all IBiS3 work
- **Effort**: 1 week
- **Code**: `src/ibdm/rules/integration_rules.py`

**2. Add private.issues Field**
- **Task**: Update `src/ibdm/core/information_state.py`
- **What**: Add `issues: list[Question]` to PrivateIS
- **Why**: Foundation for two-phase accommodation (issues → qud)
- **Larsson**: Figure 4.1 - Information State Extensions
- **Effort**: 1 day
- **Tests**: Update serialization, state management tests

**3. Update Serialization**
- **Task**: Update `to_dict()` and `from_dict()` methods
- **What**: Handle new `issues` field in serialization
- **Why**: State persistence must work
- **Effort**: Half day

### Week 2-3: Implement IBiS3 Core Rules

**4. Implement Rule 4.1 (IssueAccommodation)**
- **Task**: Create `accommodate_issue_from_plan` update rule
- **What**: Plan findout actions → private.issues (not directly to QUD)
- **Why**: Separates accommodation from raising
- **Larsson**: Section 4.6.1 - IssueAccommodation rule
- **Code**: `src/ibdm/rules/integration_rules.py`
- **Priority**: 14 (before form_task_plan)
- **Effort**: 2-3 days

**5. Implement Rule 4.2 (LocalQuestionAccommodation)**
- **Task**: Create `raise_accommodated_question` selection rule
- **What**: private.issues → shared.qud (when contextually appropriate)
- **Why**: Incremental questioning, not dumping all questions at once
- **Larsson**: Section 4.6.2 - LocalQuestionAccommodation rule
- **Code**: `src/ibdm/rules/selection_rules.py`
- **Priority**: 20 (high)
- **Effort**: 2-3 days

**6. Handle Answers to Unasked Questions**
- **Task**: Modify `integrate_answer` rule
- **What**: Check if answer resolves question in private.issues
- **Why**: Users can volunteer information before asked
- **Larsson**: Core IBiS3 capability
- **Effort**: 3-5 days

---

## Complete Roadmap: IBIS_VARIANTS_PRIORITY.md

**See**: [IBIS_VARIANTS_PRIORITY.md](IBIS_VARIANTS_PRIORITY.md) for full 22-28 week plan

**Optimal Completion Order**: IBiS3 → IBiS2 → IBiS4

**Rationale**:
1. **IBiS3 first**: Biggest user experience improvement (natural dialogue, volunteer information)
2. **IBiS2 second**: Robustness features (grounding, error handling)
3. **IBiS4 last**: Advanced features (actions, negotiation)

---

## Timeline Overview

### Phase 1: IBiS3 Completion (Weeks 1-10)
- **Target**: 30% → 100%
- **Key Features**:
  - private.issues field
  - Rules 4.1-4.5 (accommodation, raising, clarification, dependencies, reaccommodation)
  - Volunteer information handling
  - Dependent issue accommodation

### Phase 2: IBiS2 Completion (Weeks 11-18)
- **Target**: 60% → 100%
- **Key Features**:
  - Complete ICM taxonomy (27 rules)
  - Grounding strategies (optimistic/cautious/pessimistic)
  - Perception checking (ASR confidence)
  - Evidence requirements

### Phase 3: IBiS4 Implementation (Weeks 19-28)
- **Target**: 10% → 100%
- **Key Features**:
  - Device actions and interface
  - Action accommodation
  - Negotiation and dominates() relation
  - Multi-alternative handling

---

## Success Criteria

### IBiS3 Complete (Week 10)
- [x] `private.issues` field in InformationState
- [x] Rule 4.1: Plan → private.issues (accommodation)
- [x] Rule 4.2: private.issues → shared.qud (raising)
- [x] Rule 4.3: Clarification questions
- [x] Rule 4.4: Dependent issue accommodation
- [x] Rule 4.5: Question reaccommodation
- [x] Answers to unasked questions handled
- [x] Integration tests passing
- [x] IBiS3 fidelity: 100% (up from 30%)

### IBiS2 Complete (Week 18)
- [x] All 27 ICM rules implemented
- [x] Grounding status tracking
- [x] Strategy selection working
- [x] Perception checking integrated
- [x] IBiS2 fidelity: 100% (up from 60%)

### IBiS4 Complete (Week 28)
- [x] Device actions working
- [x] Action accommodation implemented
- [x] Negotiation dialogue working
- [x] IBiS4 fidelity: 100% (up from 10%)

### Overall Target
- **Larsson Fidelity**: 95%+ (from current ~70%)
- **Test Coverage**: 90%+
- **All Tests**: Passing

---

## How to Start

### 1. Review IBiS Variants Documentation

```bash
# Read comprehensive IBiS progression guide
cat IBIS_PROGRESSION_GUIDE.md

# Read new priority roadmap
cat IBIS_VARIANTS_PRIORITY.md

# Review Larsson algorithms
cat docs/LARSSON_ALGORITHMS.md
```

### 2. Verify Current Implementation

```bash
# Check if accommodation is in correct phase
grep -r "accommodate" src/ibdm/rules/integration_rules.py
grep -r "accommodate" src/ibdm/rules/interpretation_rules.py

# Check InformationState structure
cat src/ibdm/core/information_state.py
```

### 3. Start Week 1 Tasks

```bash
# 1. Fix phase separation (if needed)
# Review ibdm-accom epic

# 2. Add private.issues field
# Edit src/ibdm/core/information_state.py

# 3. Follow development workflow
ruff format src/ tests/
ruff check --fix src/ tests/
pyright src/
pytest
```

### 4. Development Workflow

Per `CLAUDE.md`:
1. Red-Green-Refactor: Test → Implement → Refactor
2. Quality checks before each commit
3. Commit: `feat(ibis3): add private.issues field`
4. Push regularly

---

## Why IBiS3 First?

**User Experience Impact**:

**Without IBiS3** (Current):
```
System: "What are the parties to the agreement?"
User: "Acme and Smith, effective January 1, 2025"
System: [Only processes parties, ignores date]
System: "What's the effective date?"
User: "I just told you, January 1, 2025"  ← BAD UX
```

**With IBiS3** (Target):
```
System: "What are the parties to the agreement?"
User: "Acme and Smith, effective January 1, 2025"
System: [Accommodates date answer to unasked question]
System: [Removes date question from private.issues]
System: "What's the governing law?"  ← NATURAL DIALOGUE
```

**Bottom Line**: IBiS3 makes dialogue feel intelligent and natural. This is more important than robustness (IBiS2) or advanced features (IBiS4).

---

## Alternative Path: Metrics First

If you prefer to establish baseline metrics before IBiS variants:

**Task**: Larsson Fidelity Metrics (ibdm-metrics)
**Duration**: 2-3 days
**Why**: Quantitative validation before adding complexity

**Then**: Proceed to IBiS3 with baseline established

---

## Alignment with Project Goals

**IBiS Variants Completion**:
- ✅ **Larsson Fidelity**: Full compliance with thesis (95%+)
- ✅ **User Experience**: Natural, intelligent dialogue (IBiS3)
- ✅ **Robustness**: Error handling, grounding (IBiS2)
- ✅ **Advanced Features**: Actions, negotiation (IBiS4)
- ✅ **Research Contribution**: Complete Larsson implementation

**Bottom Line**: Completing all IBiS variants achieves the full vision of Larsson (2002) thesis, demonstrating a complete, production-ready issue-based dialogue management system.

---

## Summary

**Status**: IBiS1 ✅ COMPLETE, Need to complete IBiS-2, 3, 4
**Immediate Task**: Fix phase separation blocker, add private.issues field
**Week 1 Goal**: Unblock IBiS3, implement Rules 4.1-4.2
**Overall Goal**: Complete all IBiS variants (22-28 weeks)
**Target Fidelity**: 95%+ Larsson compliance

**Key Action**: Start with Week 1 tasks in IBIS_VARIANTS_PRIORITY.md
