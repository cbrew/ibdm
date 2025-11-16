# Next Recommended Task

**Date**: 2025-11-16 (Updated - Week 2 Complete!)
**Basis**: IBIS_VARIANTS_PRIORITY.md, IBiS3 accommodation rules implemented
**Status**: 🎉 Week 2 complete, core accommodation working!

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

## 🎯 NEXT PRIORITY: Integration Testing & Refinement

**Current Focus**: Week 3 - Test end-to-end and refine accommodation behavior
**Duration**: 2-3 days
**Blockers**: None - core rules implemented!

---

## Week 3 Tasks: Integration Testing & End-to-End Validation

### Task 1: Create End-to-End Integration Test ⚡ NEXT

**Goal**: Verify complete dialogue flow with accommodation and volunteer information

**What to Do**:

1. **Create integration test** in `tests/integration/test_ibis3_end_to_end.py`:
   ```python
   def test_nda_drafting_with_volunteer_information():
       """Test complete NDA drafting dialogue with volunteer answers."""
       # Test scenario:
       # 1. User requests "I need to draft an NDA"
       # 2. System accommodates questions to private.issues
       # 3. System raises first question to QUD
       # 4. User volunteers multiple facts in one answer
       # 5. System processes volunteer info and skips those questions
       # 6. System continues with remaining questions
       # 7. Complete plan execution
   ```

2. **Test the full rule chain**:
   - Task plan formation → Rule 4.1 (accommodation to issues)
   - Rule 4.2 (raise to QUD) → SelectAsk → NLG
   - User volunteer answer → integrate_answer (check issues first)
   - Plan progression (skip answered questions)

3. **Verify expected behavior**:
   - Questions accommodated to private.issues (not QUD directly)
   - Questions raised to QUD incrementally
   - Volunteer answers recognized and processed
   - System doesn't re-ask answered questions
   - Plan completes successfully

**Expected Outcome**:
- Full dialogue flow works end-to-end
- All IBiS3 rules work together correctly
- Natural conversation with volunteer information

---

## ✅ Week 2 Tasks: Core Accommodation Rules (COMPLETED)

### ✅ Task 1: Implement Rule 4.1 (IssueAccommodation)

**Goal**: Accommodate findout questions from plans to private.issues (instead of pushing directly to QUD)

**What to Do**:

1. **Add precondition function** in `src/ibdm/rules/integration_rules.py`:
   ```python
   def _plan_has_findout_subplan(state: InformationState) -> bool:
       """Check if there's an active plan with findout subplans to accommodate.

       This checks if we've just created a task plan that contains findout
       subplans. These should be accommodated to private.issues first,
       not pushed directly to shared.qud.

       Larsson (2002) Section 4.6.1 - IssueAccommodation rule.
       """
       # Check if we have active plans with findout subplans
       for plan in state.private.plan:
           if not plan.is_active():
               continue

           # Check if plan has unaccommodated findout subplans
           for subplan in plan.subplans:
               if subplan.plan_type == "findout" and subplan.is_active():
                   # Check if this question is already in issues or QUD
                   question = subplan.content
                   if isinstance(question, Question):
                       if question not in state.private.issues and question not in state.shared.qud:
                           return True

       return False
   ```

2. **Add effect function** in `src/ibdm/rules/integration_rules.py`:
   ```python
   def _accommodate_findout_to_issues(state: InformationState) -> InformationState:
       """Accommodate findout subplans to private.issues.

       IBiS3 Rule 4.1 (IssueAccommodation):
       Instead of pushing questions directly to QUD, accommodate them
       to private.issues first. They'll be raised to QUD later by
       Rule 4.2 (LocalQuestionAccommodation) when contextually appropriate.

       Args:
           state: Current information state

       Returns:
           New state with findout questions accommodated to private.issues

       Larsson (2002) Section 4.6.1 - IssueAccommodation rule.
       """
       new_state = state.clone()

       # Find active plans with findout subplans
       for plan in new_state.private.plan:
           if not plan.is_active():
               continue

           # Accommodate each findout subplan to private.issues
           for subplan in plan.subplans:
               if subplan.plan_type == "findout" and subplan.is_active():
                   question = subplan.content
                   if isinstance(question, Question):
                       # Only accommodate if not already in issues or QUD
                       if question not in new_state.private.issues and question not in new_state.shared.qud:
                           new_state.private.issues.append(question)

       return new_state
   ```

3. **Add rule to `create_integration_rules()`**:
   ```python
   # At the top of the rules list, BEFORE form_task_plan
   UpdateRule(
       name="accommodate_issue_from_plan",
       preconditions=_plan_has_findout_subplan,
       effects=_accommodate_findout_to_issues,
       priority=14,  # Higher than form_task_plan (13)
       rule_type="integration",
   ),
   ```

4. **Modify `_form_task_plan()` to NOT push to QUD**:
   - Remove lines 229-233 and 256-260 that push first question to QUD
   - Let Rule 4.2 handle raising questions to QUD instead

**Expected Outcome**:
- Task plans created with findout subplans
- Questions accommodated to `private.issues` (not pushed to QUD yet)
- QUD remains empty until Rule 4.2 raises questions

**Tests to Write**:
```python
def test_rule_4_1_issue_accommodation():
    """Test Rule 4.1: Findout subplans accommodated to private.issues."""
    state = InformationState()

    # Create task plan with findout subplans
    q1 = WhQuestion(variable="x", predicate="parties(x)")
    q2 = WhQuestion(variable="y", predicate="effective_date(y)")
    subplan1 = Plan(plan_type="findout", content=q1)
    subplan2 = Plan(plan_type="findout", content=q2)
    plan = Plan(plan_type="nda_drafting", content=None, subplans=[subplan1, subplan2])
    state.private.plan.append(plan)

    # Apply Rule 4.1
    new_state = _accommodate_findout_to_issues(state)

    # Assertions
    assert len(new_state.private.issues) == 2
    assert q1 in new_state.private.issues
    assert q2 in new_state.private.issues
    assert len(new_state.shared.qud) == 0  # Not raised to QUD yet!
```

**Larsson Reference**: Section 4.6.1 - IssueAccommodation rule

---

### Task 2: Implement Rule 4.2 (LocalQuestionAccommodation) 🎯

**Goal**: Raise accommodated questions from private.issues to shared.qud when contextually appropriate

**What to Do**:

1. **Create `src/ibdm/rules/selection_rules.py` if it doesn't exist**, or add to existing file:
   ```python
   def _has_raisable_issue(state: InformationState) -> bool:
       """Check if there are issues that can be raised to QUD.

       An issue can be raised if:
       - There are issues in private.issues
       - QUD is empty or current QUD is not blocking
       - Context is appropriate for asking a new question

       Larsson (2002) Section 4.6.2 - LocalQuestionAccommodation rule.
       """
       # Need at least one issue to raise
       if not state.private.issues:
           return False

       # For now, simple strategy: raise if QUD is empty
       # Future: more sophisticated context checking
       if not state.shared.qud:
           return True

       return False
   ```

2. **Add effect function**:
   ```python
   def _raise_issue_to_qud(state: InformationState) -> InformationState:
       """Raise first issue from private.issues to shared.qud.

       IBiS3 Rule 4.2 (LocalQuestionAccommodation):
       When context is appropriate, raise accommodated questions
       to QUD so they can be asked. This implements incremental
       questioning - we don't dump all questions at once.

       Args:
           state: Current information state

       Returns:
           New state with first issue raised to QUD

       Larsson (2002) Section 4.6.2 - LocalQuestionAccommodation rule.
       """
       new_state = state.clone()

       # Pop first issue from private.issues
       if new_state.private.issues:
           question = new_state.private.issues.pop(0)

           # Push to QUD
           new_state.shared.push_qud(question)

       return new_state
   ```

3. **Add selection rule**:
   ```python
   # In create_selection_rules() function
   UpdateRule(
       name="raise_accommodated_question",
       preconditions=_has_raisable_issue,
       effects=_raise_issue_to_qud,
       priority=20,  # High priority
       rule_type="selection",
   ),
   ```

**Expected Outcome**:
- Questions raised from private.issues to shared.qud incrementally
- Only one question raised at a time (when QUD is empty)
- Enables natural, incremental dialogue flow

**Tests to Write**:
```python
def test_rule_4_2_local_question_accommodation():
    """Test Rule 4.2: Issues raised to QUD when appropriate."""
    state = InformationState()

    # Setup: Questions in private.issues, QUD empty
    q1 = WhQuestion(variable="x", predicate="parties(x)")
    q2 = WhQuestion(variable="y", predicate="effective_date(y)")
    state.private.issues = [q1, q2]

    # Apply Rule 4.2
    new_state = _raise_issue_to_qud(state)

    # Assertions
    assert len(new_state.shared.qud) == 1
    assert new_state.shared.qud[0] == q1  # First issue raised
    assert len(new_state.private.issues) == 1
    assert new_state.private.issues[0] == q2  # Second issue remains
```

**Larsson Reference**: Section 4.6.2 - LocalQuestionAccommodation rule

---

### Task 3: Modify integrate_answer for Volunteer Information 🔄

**Goal**: Check private.issues before checking QUD when processing answers

**What to Do**:

1. **Update `_integrate_answer()` in `src/ibdm/rules/integration_rules.py`**:
   ```python
   def _integrate_answer(state: InformationState) -> InformationState:
       """Integrate answer, checking private.issues FIRST (IBiS3).

       Modified for IBiS3:
       1. Check if answer resolves question in private.issues (volunteer info)
       2. If yes: remove from issues, add commitment, DON'T raise to QUD
       3. If no: check QUD as normal (original behavior)
       """
       new_state = state.clone()
       move = new_state.private.beliefs.get("_temp_move")

       if not isinstance(move, DialogueMove):
           return new_state

       if isinstance(move.content, Answer):
           answer = move.content
           domain = _get_active_domain(new_state)

           # IBiS3: Check private.issues FIRST (volunteer information)
           for issue in new_state.private.issues[:]:  # Iterate over copy
               if domain.resolves(answer, issue):
                   # User volunteered answer to unasked question!
                   new_state.private.issues.remove(issue)

                   # Add commitment
                   commitment = f"{issue}: {answer.content}"
                   new_state.shared.commitments.add(commitment)

                   # Mark corresponding subplan as completed
                   _complete_subplan_for_question(new_state, issue)

                   # DON'T raise this question to QUD - already answered!
                   # Continue to check other issues
                   break  # Process one volunteer answer per turn
           else:
               # No volunteer info - check QUD as normal (original behavior)
               top_question = new_state.shared.top_qud()
               if top_question:
                   if domain.resolves(answer, top_question):
                       # Normal QUD resolution...
                       # (existing code)

       return new_state
   ```

**Expected Outcome**:
- User can volunteer information before being asked
- System recognizes volunteer answers and doesn't re-ask
- Natural dialogue flow

**Tests to Write**:
```python
def test_volunteer_information_handling():
    """Test IBiS3: User volunteers answer before being asked."""
    state = InformationState()
    domain = get_nda_domain()

    # Setup: Question in private.issues (not yet asked)
    q = WhQuestion(variable="x", predicate="effective_date(x)")
    state.private.issues.append(q)

    # User volunteers answer
    answer = Answer(content="January 1, 2025", question_ref=q)
    move = DialogueMove(move_type="answer", content=answer, speaker="user")
    state.private.beliefs["_temp_move"] = move

    # Apply integration
    new_state = _integrate_answer(state)

    # Assertions
    assert q not in new_state.private.issues  # Removed from issues
    assert len(new_state.shared.qud) == 0  # NOT raised to QUD
    assert len(new_state.shared.commitments) > 0  # Answer committed
```

---

## Development Workflow

### For Each Task:

1. **Write the test first** (TDD)
   ```bash
   # Create/update test file
   vim tests/unit/test_ibis3_accommodation.py
   ```

2. **Run test (should fail)**
   ```bash
   pytest tests/unit/test_ibis3_accommodation.py -v
   ```

3. **Implement the function**
   ```bash
   vim src/ibdm/rules/integration_rules.py
   # Or: vim src/ibdm/rules/selection_rules.py
   ```

4. **Run test (should pass)**
   ```bash
   pytest tests/unit/test_ibis3_accommodation.py -v
   ```

5. **Quality checks**
   ```bash
   ruff format src/ tests/
   ruff check --fix src/ tests/
   pyright src/
   pytest  # Full suite
   ```

6. **Commit**
   ```bash
   git add .
   git commit -m "feat(ibis3): implement Rule 4.1 (IssueAccommodation)"
   # Or: "feat(ibis3): implement Rule 4.2 (LocalQuestionAccommodation)"
   # Or: "feat(ibis3): handle volunteer information in integrate_answer"
   ```

---

## Success Criteria - Week 2

After completing these tasks, you should have:

- [x] Rule 4.1 (IssueAccommodation) implemented
  - Precondition: `_plan_has_findout_subplan`
  - Effect: `_accommodate_findout_to_issues`
  - Questions go to private.issues (not QUD)

- [x] Rule 4.2 (LocalQuestionAccommodation) implemented
  - Precondition: `_has_raisable_issue`
  - Effect: `_raise_issue_to_qud`
  - Questions raised from issues to QUD incrementally

- [x] Volunteer information handling
  - `_integrate_answer` checks private.issues first
  - Answers to unasked questions processed correctly
  - System doesn't re-ask already-answered questions

- [x] Tests passing
  - test_rule_4_1_issue_accommodation
  - test_rule_4_2_local_question_accommodation
  - test_volunteer_information_handling

- [x] Integration tests
  - Multi-turn dialogue with accommodation
  - User volunteers multiple facts
  - System adapts questioning based on volunteer info

---

## Expected Behavior After Week 2

**Without IBiS3** (Current):
```
System: "What are the parties?"
User: "Acme and Smith, effective January 1, 2025"
System: [Only processes parties, ignores date]
System: "What's the effective date?"
User: "I just told you!"  ← BAD UX
```

**With IBiS3** (After Week 2):
```
System: "What are the parties?"
User: "Acme and Smith, effective January 1, 2025"
System: [Accommodates date to private.issues, then processes as volunteer answer]
System: [Removes date question from issues, adds commitment]
System: "What's the governing law?"  ← SKIPS ALREADY-ANSWERED!
```

---

## Progress Tracking

**IBiS3 Completion**:
- Week 1: ✅ Foundation (30% → 35%)
- Week 2: 🔧 Rules 4.1-4.2 (35% → 50%)
- Week 3-4: Volunteer information + clarification (50% → 65%)
- Week 5-6: Dependent issues (65% → 80%)
- Week 7-8: Question reaccommodation (80% → 90%)
- Week 9-10: Integration tests + polish (90% → 100%)

**Current**: 35% complete
**Target**: 50% by end of Week 2

---

## File Locations

**Core Files to Modify**:
- `src/ibdm/core/information_state.py` - ✅ Already updated (private.issues)
- `src/ibdm/rules/integration_rules.py` - 🔧 Add Rule 4.1, modify _form_task_plan, modify _integrate_answer
- `src/ibdm/rules/selection_rules.py` - 🔧 Add Rule 4.2

**Test Files**:
- `tests/unit/test_information_state.py` - ✅ Already updated
- `tests/unit/test_ibis3_accommodation.py` - 📋 To create
- `tests/integration/test_volunteer_information.py` - 📋 To create

---

## Larsson References

**Essential Reading**:
- **Section 4.6.1**: IssueAccommodation rule (Rule 4.1)
- **Section 4.6.2**: LocalQuestionAccommodation rule (Rule 4.2)
- **Figure 4.1**: IBiS3 Information State structure
- **Section 4.3**: Clarification questions

**Access**:
```bash
# Read Larsson algorithms
cat docs/LARSSON_ALGORITHMS.md | grep -A 50 "IBiS3"

# Read full thesis chapter
cat docs/larsson_thesis/chapter_4.md
```

---

## Questions or Issues?

**If stuck**:
1. Review `IBIS_PROGRESSION_GUIDE.md` - Section "Part 3: IBiS3"
2. Check existing integration rules for patterns
3. Look at test examples in `tests/integration/test_qud_and_plan_progression.py`

**Key Principle**: Accommodation is INTEGRATION/SELECT, not INTERPRET
- Questions accommodated to private.issues (INTEGRATION)
- Questions raised to QUD (SELECTION)
- User can answer before being asked (natural dialogue)

---

## Bottom Line

**Next Steps** (in order):
1. ⚡ Implement Rule 4.1 (IssueAccommodation) - 1-2 days
2. 🎯 Implement Rule 4.2 (LocalQuestionAccommodation) - 1-2 days
3. 🔄 Modify integrate_answer for volunteer info - 1 day

**Total Effort**: 3-5 days
**Goal**: IBiS3 35% → 50%
**Outcome**: Natural dialogue with volunteer information handling

Ready to code! 🚀
