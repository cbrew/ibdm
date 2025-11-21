# NDA Comprehensive Scenario - State Mismatch Analysis

**Date**: 2025-11-21
**Scenario**: nda_comprehensive
**Total Mismatches**: 2 turns with state mismatches

## Executive Summary

The nda_comprehensive scenario shows 2 critical state mismatches where the dialogue engine is not properly tracking volunteered information and structured commitments:

1. **Turn 1**: Volunteered information (date + legal entities) not stored as commitments
2. **Turn 8**: Answer commitments (nda_type + time_period) not properly structured + QUD not popped

Both issues indicate problems with:
- Volunteer information accommodation (Larsson Rule 4.3)
- Answer integration creating structured commitments (Larsson Rule 4.1)
- QUD stack management for clarification dialogues (Larsson Rule 4.2)

## Detailed Mismatch Analysis

### Mismatch 1: Turn 1 - Volunteered Information Not Accommodated

**User Utterance**: "I need an NDA between us and Global Industries, effective February 1st"

**Move Type**: request + volunteer_info

**Expected State Changes**:
- Commitments added:
  - `date(value=2025-02-01)`
  - `legal_entities(value=current_company, Global Industries)`

**Actual State**:
- ❌ Missing commitments for both date and legal_entities

**Larsson Rule**: Rule 4.3 - Belief Accommodation (volunteered information)

**Problem**: When user volunteers information ("effective February 1st", "Global Industries"), the system acknowledges it verbally (Turn 2: "I understand you need an NDA with Global Industries, effective February 1st") but does NOT store these as structured commitments in the information state.

**Root Cause**: The volunteer information accommodation rule is either:
1. Not firing during integration phase
2. Firing but not creating proper commitment structures
3. Creating commitments but in wrong format (not matching expected format)

**Impact**:
- System appears to "forget" volunteered information
- Questions that should be skipped (parties, date) might still be asked
- Violates Rule 4.5 (Question Reaccommodation - skip already-answered questions)

---

### Mismatch 2: Turn 8 - Answer Not Creating Structured Commitments + QUD Not Popped

**User Utterance**: "I think we should go with mutual, and by the way, we need this for 3 years"

**Move Type**: answer + volunteer_info

**Expected State Changes**:
- QUD popped: `?x.clarify [utterance=What does mutual mean exactly?, topic=mutual_nda]`
- QUD depth: 2 (decreased from 3)
- Commitments added:
  - `nda_type(value=mutual)`
  - `time_period(value=3 years)`

**Actual State**:
- ❌ Missing commitments for both nda_type and time_period
- ❌ QUD `?x.clarify` NOT popped (remains on stack)

**Larsson Rules**:
- Rule 4.1 - Answer Integration
- Rule 4.3 - Belief Accommodation (volunteered duration)
- Rule 4.2 - Local Question Accommodation (QUD management for clarifications)

**Problems**:
1. **Answer not creating structured commitment**: User answers "mutual" but this doesn't create a clean `nda_type(value=mutual)` commitment
2. **Volunteered info not accommodated**: User volunteers "3 years" but this doesn't create `time_period(value=3 years)` commitment
3. **QUD not popped**: The clarification question `?x.clarify` should be popped when the underlying question is answered, but it remains on the stack

**Root Causes**:
1. Answer integration rule creating question+answer pairs instead of domain-specific commitments
2. Volunteer information accommodation not working for composite moves
3. QUD pop logic not recognizing when clarification is resolved

**Impact**:
- QUD stack grows unbounded (depth 3→6→8 instead of proper nesting/popping)
- Commitments stored in wrong format (question+answer string instead of structured data)
- Domain reasoning (e.g., "is nda_type question resolved?") cannot work with unstructured commitments

---

## Pattern Analysis

### Common Issues Across Both Mismatches

1. **Commitment Format Problem**:
   - Scenario expects: `nda_type(value=mutual)` (structured, domain-specific)
   - Engine creates: `?{mutual, one-way}: I think mutual makes sense...` (question+answer text pair)

2. **Volunteer Information Rule Not Firing**:
   - Both turns involve volunteered information
   - Neither turn properly accommodates the volunteered facts
   - Suggests Rule 4.3 (BeliefAccommodation) is not implemented or not working

3. **QUD Stack Management**:
   - Clarification questions pushed but never popped
   - Depth grows monotonically (never decreases)
   - Suggests missing logic for "when to pop clarification from QUD"

---

## Categories of Fixes Needed

### Category A: Commitment Creation Format

**Problem**: Answers create question+answer text pairs instead of structured domain commitments

**Files to Fix**:
- `src/ibdm/rules/update_rules.py` - `integrate_answer` rule
- Possibly `src/ibdm/core/domain.py` - domain-specific commitment creation

**What to implement**:
- Parse answer content to extract semantic value
- Use domain knowledge to create properly structured commitment
- Example: For AltQuestion "mutual or one-way", extract "mutual" from answer and create `nda_type(value=mutual)`

---

### Category B: Volunteer Information Accommodation

**Problem**: Rule 4.3 (BeliefAccommodation) not accommodating volunteered information

**Files to Fix**:
- `src/ibdm/rules/update_rules.py` - need to add/fix volunteer info accommodation rule
- `src/ibdm/nlu/` - might need to detect volunteered information in NLU phase

**What to implement**:
- Detect when user provides information not requested
- Extract semantic content (dates, entities, durations)
- Create domain-specific commitments for each volunteered fact
- Example: "effective February 1st" → `date(value=2025-02-01)`

---

### Category C: QUD Stack Management for Clarifications

**Problem**: Clarification questions pushed but never popped

**Files to Fix**:
- `src/ibdm/rules/update_rules.py` - QUD pop logic in answer integration
- Logic for determining "is clarification resolved?"

**What to implement**:
- When user answers underlying question after clarification, pop both:
  1. The clarification question
  2. The original question (if fully resolved)
- Example: User asks "What does mutual mean?", system explains, user says "I'll go with mutual" → pop clarification question

---

### Category D: Scenario Expectation Alignment

**Problem**: Scenario might have incorrect expectations (less likely but possible)

**Files to Fix**:
- `demos/scenarios/nda_comprehensive.json` - update state_changes if needed

**What to verify**:
- Run scenario with `IBDM_DEBUG=all` after fixes
- Compare expected vs actual state at each turn
- Update scenario if implementation is correct but expectations are wrong (per Policy #16)

---

## Recommended Fix Order

### Phase 1: Core Commitment Creation (High Priority)
1. ✅ Fix answer integration to create structured commitments (Category A)
2. ✅ Implement volunteer information accommodation (Category B)

### Phase 2: QUD Management (Medium Priority)
3. ✅ Fix QUD popping for clarifications (Category C)

### Phase 3: Verification (Low Priority)
4. ✅ Run scenario, verify all mismatches resolved
5. ✅ Update scenario expectations if needed (Category D)

---

## Success Criteria

When fixed, running `python scripts/run_scenario.py nda_comprehensive` should show:
- ✅ No state mismatch warnings
- ✅ Turn 1: Both date and legal_entities commitments created
- ✅ Turn 8: Both nda_type and time_period commitments created + QUD popped
- ✅ QUD depth properly managed (increases/decreases as expected)
- ✅ All commitments in structured format matching domain model

---

## References

- **Scenario File**: `demos/scenarios/nda_comprehensive.json`
- **Update Rules**: `src/ibdm/rules/update_rules.py`
- **State Verification**: `src/ibdm/demo/scenario_runner.py:521` (`_verify_state_changes`)
- **Larsson Algorithms**: `docs/LARSSON_ALGORITHMS.md`
- **Scenario Alignment**: `docs/SCENARIO_ALIGNMENT.md` (Policy #16)
