# Next Recommended Task

**Date**: 2025-11-16 (Updated)
**Basis**: Code verification, LARSSON_PRIORITY_ROADMAP.md, test suite analysis

---

## Status Update: TIER 1 Architecture Complete ✅

### Verification Results (2025-11-16)

After comprehensive code and test review, **ALL TIER 1 Core Larsson Architecture tasks are COMPLETE**:

#### ✅ ibdm-loop (Complete Interactive Dialogue Loop)
- **ibdm-loop.2**: Domain validation in answer integration ✅
  - Implemented in `integration_rules.py:476-482`
  - Uses `domain.resolves(answer, question)` for semantic validation
  - Tested in `test_nda_with_domain.py`, `test_domain_model.py`

- **ibdm-loop.3**: Handle invalid answers with clarification ✅
  - Implemented in `integration_rules.py:501-507`
  - Sets `_needs_clarification` flag, keeps question on QUD
  - Tested in `test_clarification_handling.py`

- **ibdm-loop.4**: Mark subplan complete after valid answer ✅
  - Implemented in `integration_rules.py:492-493`
  - Calls `_complete_subplan_for_question()`
  - Tested in `test_qud_and_plan_progression.py`

- **ibdm-loop.5**: Push next question to QUD after answer ✅
  - Implemented in `integration_rules.py:496-500`
  - Gets next question from plan and pushes to QUD
  - Tested in `test_qud_and_plan_progression.py`

- **ibdm-loop.11**: Verify QUD management across turns ✅
  - Comprehensive tests in `test_qud_and_plan_progression.py`
  - Tests LIFO behavior, multi-turn dialogues, invalid answer handling

- **ibdm-loop.12**: Verify plan progress tracking ✅
  - Comprehensive tests in `test_qud_and_plan_progression.py`
  - Tests subplan completion, plan progression, multi-turn scenarios

**Test Results**: 90/90 core tests passing (100%)

#### ✅ ibdm-accom (Accommodation in Integration Phase)
- **Status**: COMPLETE
- Task plan formation is in `integration_rules.py` (`form_task_plan` rule)
- NO accommodation in interpretation phase (verified via grep)
- Architecture properly separates INTERPRET (syntax) from INTEGRATE (pragmatics)

#### ✅ ibdm-bsr (Burr-Centric State Refactoring)
- **Status**: COMPLETE
- Engine is stateless (verified: no `self.state` in engine code)
- All methods accept `InformationState` as parameter
- Methods are pure functions: `interpret()`, `integrate()`, `select_action()`, `generate()`

---

## Updated Recommendation: Larsson Fidelity Metrics

**Priority**: P0 (Foundation for Validation)
**Estimated Duration**: 2-3 days
**Epic**: ibdm-metrics

### Why This Task Now?

With TIER 1 complete, we need **objective validation** before moving to demos:

1. **Verify Larsson Compliance**: Quantitatively measure how well our implementation matches Larsson (2002)
2. **Baseline for Future Work**: Establish metrics before adding complexity
3. **Support Demo Claims**: Back up "Larsson-faithful" claims with measurements
4. **Guide Next Steps**: Metrics will reveal any gaps in implementation

### Current State

**What's Complete**:
- ✅ Core Larsson algorithms (QUD, plans, domain validation, clarification)
- ✅ Four-phase architecture (INTERPRET → INTEGRATE → SELECT → GENERATE)
- ✅ Domain abstraction layer with semantic operations
- ✅ Stateless engine with explicit state passing

**What's Missing**:
- ❌ Quantitative Larsson fidelity measurement
- ❌ Architectural compliance metrics
- ❌ Baseline for tracking improvements/regressions

### Specific Tasks

#### Task 1: Define Architectural Compliance Metrics (ibdm-metrics.1.1)

**Actions**:
1. Create metrics module: `src/ibdm/metrics/architectural_compliance.py`
2. Define metrics for:
   - Four-phase separation (interpretation, integration, selection, generation)
   - Rule organization and priority handling
   - Control loop structure
3. Implement measurement functions
4. Add tests for metric calculation

**Success Criteria**:
- Metrics module with clear API
- Can measure phase separation quantitatively
- Tests verify metric calculations

**Code Location**: Implementation lives in `integration_rules.py:451-522` (answer integration)

#### Task 2: Define Information State Structure Metrics (ibdm-metrics.1.2)

**Actions**:
1. Verify InformationState structure matches Larsson
   - private/shared separation
   - QUD as stack (LIFO)
   - agenda structure
   - plan structure
2. Create structural validation metrics
3. Add tests for structure compliance

**Success Criteria**:
- Can verify QUD is LIFO (not set/list)
- Can validate private/shared separation
- Structural metrics pass for current implementation

#### Task 3: Define Semantic Operations Coverage (ibdm-metrics.1.3)

**Actions**:
1. Verify all Larsson semantic operations implemented:
   - `resolves(answer, question)` ✅ (already verified)
   - `relevant(proposition, question)` (check implementation)
   - `combines(answer1, answer2)` (verify if needed)
   - `depends(question1, question2)` (verify if needed)
2. Create coverage metrics
3. Test operation correctness

**Success Criteria**:
- Metric shows which operations are implemented
- Can verify operation correctness
- Coverage report generated

**Code Location**: `src/ibdm/core/domain.py:151-204` (resolves, relevant methods)

#### Task 4: Define Update Rules Coverage (ibdm-metrics.1.4)

**Actions**:
1. Map implemented rules to Larsson algorithms:
   - Integration rules (8 rules in `integration_rules.py`)
   - Selection rules (check `selection_rules.py`)
   - Generation rules (check `generation_rules.py`)
2. Create rule coverage metrics
3. Verify single-rule application per cycle

**Success Criteria**:
- Coverage report of Larsson algorithms implemented
- Verification that rules fire correctly
- Documentation of any intentional deviations

**Code Location**: `src/ibdm/rules/integration_rules.py:17-91` (8 integration rules)

#### Task 5: Generate Baseline Report (ibdm-metrics.1.5)

**Actions**:
1. Run all metrics on current codebase
2. Generate baseline report: `reports/larsson-fidelity-baseline-2025-11-16.md`
3. Document current compliance level (estimate 85-95%)
4. Identify any gaps for future work

**Success Criteria**:
- Comprehensive baseline report
- Quantitative compliance score
- Clear documentation for stakeholders

### Implementation Plan

```bash
# 1. Create metrics module structure
mkdir -p src/ibdm/metrics tests/unit/metrics

# 2. Implement metrics (red-green-refactor)
# - Write failing test
# - Implement metric
# - Refactor and commit

# 3. Generate baseline report
python -m ibdm.metrics.generate_report > reports/larsson-fidelity-baseline.md

# 4. Review and document
# Update SYSTEM_ACHIEVEMENTS.md with quantitative metrics
```

### Why Not Domain Completeness?

Domain completeness (previous recommendation) is **still important** but:

1. **Metrics First**: Need to establish baseline BEFORE adding complexity
2. **Validation Foundation**: Metrics will help verify domain switching works correctly
3. **Risk Mitigation**: Quantify current state before changing architecture
4. **Better Demos**: Can claim "95% Larsson-compliant" with evidence

**Revised Timeline**:
1. **This Week**: Larsson fidelity metrics (ibdm-metrics) - 2-3 days
2. **Next Week**: Domain completeness & switching (ibdm-84, ibdm-85) - 3-5 days
3. **Following**: End-to-end validation with metrics tracking

### Expected Outcome

After completing metrics:
- **Quantitative Larsson Fidelity Score**: 85-95% (estimated)
- **Baseline Documentation**: For tracking future changes
- **Gap Analysis**: Clear list of remaining work
- **Demo Credibility**: Evidence-based claims
- **Clear Path**: To domain completeness and end-to-end validation

---

## Alternative: Continue with Domain Completeness

If metrics implementation is deferred, the **previous recommendation remains valid**:

### Domain Completeness & Runtime Switching (ibdm-84, ibdm-85)

**Why**: Demonstrates architectural soundness and domain portability
**Priority**: P0 for demo readiness
**Estimated**: 3-5 days

**Tasks**:
1. Verify NDA domain completeness (ibdm-84.1)
2. Complete Travel domain (ibdm-85)
3. Implement runtime domain switching
4. Create side-by-side demo

**Outcome**: Goal 3 (Domain Portability) 90% → 100%

---

## Recommended Path: Metrics → Domains → Validation

```
Week 1 (Current): Larsson Fidelity Metrics
  ├─ Define metrics (architectural, structural, semantic, rules)
  ├─ Implement measurement
  ├─ Generate baseline report
  └─ Document compliance level

Week 2: Domain Completeness
  ├─ Verify NDA domain
  ├─ Complete Travel domain
  ├─ Runtime switching
  └─ Side-by-side demo

Week 3-4: End-to-End Validation
  ├─ Full workflow validation (both domains)
  ├─ Metrics tracking through dialogues
  ├─ Performance benchmarks
  └─ Demo polish
```

---

## How to Start (Metrics Path)

### 1. Review Larsson Compliance Documentation

```bash
# Read Larsson algorithms reference
cat docs/LARSSON_ALGORITHMS.md

# Review implementation
cat LARSSON_PRIORITY_ROADMAP.md
```

### 2. Examine Current Implementation

```bash
# Check integration rules (answer validation logic)
cat src/ibdm/rules/integration_rules.py

# Check domain semantic operations
cat src/ibdm/core/domain.py

# Check test coverage
pytest tests/integration/test_qud_and_plan_progression.py -v
```

### 3. Create Metrics Module

```bash
# Create module structure
mkdir -p src/ibdm/metrics tests/unit/metrics

# Start with architectural metrics
touch src/ibdm/metrics/__init__.py
touch src/ibdm/metrics/architectural_compliance.py
touch tests/unit/metrics/test_architectural_compliance.py
```

### 4. Follow Development Workflow

Per `CLAUDE.md`:
1. Use beads for tracking: `.claude/beads-larsson.sh start ibdm-metrics.1.1`
2. Red-Green-Refactor: Test → Implement → Refactor
3. Quality checks: `ruff format && ruff check --fix && pyright && pytest`
4. Commit: `feat(metrics): add architectural compliance metrics`

---

## Alignment with Project Goals

**Metrics-First Path**:
- ✅ **Larsson Fidelity**: Quantitatively verify compliance
- ✅ **Validation Foundation**: Establish baseline before complexity
- ✅ **Demo Credibility**: Evidence-based claims
- ✅ **Risk Mitigation**: Measure before changing

**Bottom Line**: Metrics provide the **foundation for confident progress**. With TIER 1 complete, we need quantitative validation before adding domain switching complexity or creating demos.

---

## Summary

**Status**: TIER 1 (Core Larsson Architecture) ✅ COMPLETE
**Recommendation**: Implement Larsson Fidelity Metrics (ibdm-metrics)
**Alternative**: Domain Completeness & Runtime Switching (ibdm-84, ibdm-85)
**Rationale**: Establish quantitative baseline before adding complexity

**Key Finding**: The core dialogue loop with domain validation, QUD management, plan progression, and clarification handling is **fully implemented and tested**. Next step is to measure how well it matches Larsson (2002) before proceeding.
