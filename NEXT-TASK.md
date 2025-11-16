# Next Recommended Task

**Date**: 2025-11-16
**Basis**: IBIS_PROGRESSION_GUIDE.md, LARSSON_TASK_MAPPING.md, project-status-2025-11-16.md

---

## Recommendation: Domain Completeness & Runtime Switching

**Priority**: P0 (Essential for Demo Polish)
**Estimated Duration**: 3-5 days
**Epic**: ibdm-84, ibdm-85

### Why This Task?

Following the completion of:
- ✅ Documentation reorganization (just completed)
- ✅ IBD-1 (ibdm-loop epic) - Complete interactive dialogue loop
- ✅ Phase 3.5 (ibdm-64) - LLM-enhanced NLU with 11 components

The system is **90% demo-ready** but needs polish to impressively demonstrate the three goals:
1. ✅ Larsson-Faithful IBDM (85% - sufficient)
2. ✅ LLM-Powered Natural Language (95% - excellent)
3. ⚠️ **Domain Portability (90% - needs runtime switching)**

### Current State

**What Works**:
- ✅ Domain abstraction layer (`src/ibdm/core/domain.py`)
- ✅ NDA domain complete with 16 passing tests
- ✅ Travel domain implemented
- ✅ Domain validation with `domain.resolves()`

**What's Missing**:
- ❌ Runtime domain switching capability
- ⚠️ End-to-end validation for both domains
- ⚠️ Side-by-side domain comparison demo

### Specific Tasks

#### Task 1: Verify NDA Domain Completeness (ibdm-84.1)

**Actions**:
1. Review NDA domain implementation (`src/ibdm/domains/nda/`)
2. Verify all predicates are properly registered
3. Ensure all plan builders work correctly
4. Run full NDA workflow end-to-end with LLM NLU
5. Document any gaps

**Success Criteria**:
- All 16 NDA domain tests pass
- Full NDA dialogue (user request → all questions → completion) works
- No errors in domain validation

#### Task 2: Complete Travel Domain (ibdm-85)

**Actions**:
1. Review Travel domain implementation (`src/ibdm/domains/travel/`)
2. Add missing predicates/plan builders if needed
3. Create comprehensive Travel domain tests (target: 15+ tests)
4. Run full Travel workflow end-to-end
5. Ensure parity with NDA domain completeness

**Success Criteria**:
- 15+ Travel domain tests passing
- Full Travel booking dialogue works
- Domain validation operational

#### Task 3: Implement Runtime Domain Switching

**Actions**:
1. Add domain configuration to NLUEngineConfig
2. Implement domain loading/switching in DialogueMoveEngine
3. Create domain registry/factory pattern
4. Update Burr integration to support domain switching
5. Add tests for switching between NDA and Travel mid-session

**Success Criteria**:
- Can initialize engine with different domains
- Domain-specific plan builders work correctly
- All tests pass with both domains

#### Task 4: Create Side-by-Side Demo

**Actions**:
1. Create demo script showing both domains
2. Add visualization of domain-specific plan structures
3. Document domain portability in demo materials
4. Update SYSTEM_ACHIEVEMENTS.md with domain switching capability

**Success Criteria**:
- Demo script runs both NDA and Travel dialogues
- Clear demonstration of domain abstraction working
- Documentation updated

### Why Not NLG Enhancement or End-to-End Validation?

**NLG Enhancement** (ibdm-66, ibdm-67):
- Template-based NLG currently "works adequately"
- Can be improved post-demo
- Not blocking demo readiness

**End-to-End Validation** (ibdm-87, ibdm-88):
- Should come after domain completeness
- Validates complete feature set
- Better to do after all demo features are in place

### Expected Outcome

After completing domain completeness:
- **Goal 3 (Domain Portability)**: 90% → 100% ✅
- **Demo Readiness**: 90% → 95%
- **Clear Path** to end-to-end validation
- **Strong Evidence** of architectural soundness

### Next Steps After This

Once domain completeness is done:
1. **End-to-End Validation** (ibdm-87, ibdm-88) - Verify both workflows
2. **NLG Enhancement** (ibdm-66, ibdm-67) - Polish response quality
3. **Demo Infrastructure** - Visualization, metrics display
4. **IBiS2 Grounding** (Post-demo) - Advanced ICM, confirmation protocols

---

## How to Start

### 1. Review Current Domain Implementation

```bash
# Check NDA domain
tree src/ibdm/domains/nda/
pytest tests/unit/domains/test_nda_domain.py -v

# Check Travel domain
tree src/ibdm/domains/travel/
pytest tests/unit/domains/test_travel_domain.py -v 2>/dev/null || echo "Need Travel tests!"
```

### 2. Consult Primary Documentation

- **Architecture**: `docs/architecture_principles.md` (Policy #0)
- **Domain Model**: `src/ibdm/core/domain.py` docstrings
- **Progression Guide**: `IBIS_PROGRESSION_GUIDE.md` (IBiS1 → IBiS3)
- **Task Mapping**: `LARSSON_TASK_MAPPING.md` (Chapter 2 - Predicates/Sorts)

### 3. Follow Development Workflow

Per `CLAUDE.md`:
1. Use `.claude/beads-larsson.sh start <task-id>` for Larsson tracking
2. Red-Green-Refactor: Test → Implement → Refactor
3. Run quality checks before each commit:
   ```bash
   ruff format src/ tests/ && ruff check --fix src/ tests/ && pyright src/ && pytest
   ```
4. Commit with conventional format: `feat(domains): description`

---

## Alignment with Project Goals

This task directly supports:
- **Demonstration Goal 3**: Domain Portability (90% → 100%)
- **IBiS1 Completion**: Validates domain abstraction layer
- **Demo Readiness**: Critical for impressive demonstration
- **Architectural Soundness**: Proves separation of domain/dialogue management

**Bottom Line**: Domain completeness is the most direct path to 100% demo-ready status while demonstrating a key architectural achievement (domain abstraction working across multiple domains).
