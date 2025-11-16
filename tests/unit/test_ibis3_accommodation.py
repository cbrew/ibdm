"""Tests for IBiS3 accommodation rules (Rules 4.1, 4.2, and 4.3).

Tests issue accommodation (Rule 4.1), local question accommodation (Rule 4.2),
and issue clarification (Rule 4.3) per Larsson (2002) Section 4.6.

IBiS3 Enhancement: Questions from task plans are accommodated to private.issues
first, then raised to QUD incrementally when contextually appropriate.
Clarification questions are pushed to QUD to suspend original questions.
"""

from ibdm.core import (
    InformationState,
    Plan,
    WhQuestion,
)


class TestRule41IssueAccommodation:
    """Test Rule 4.1: IssueAccommodation from plans to private.issues."""

    def test_rule_4_1_issue_accommodation(self):
        """Test Rule 4.1: Findout subplans accommodated to private.issues."""
        from ibdm.rules.integration_rules import _accommodate_findout_to_issues

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

    def test_plan_has_findout_subplan_precondition(self):
        """Test precondition: detects plans with findout subplans."""
        from ibdm.rules.integration_rules import _plan_has_findout_subplan

        state = InformationState()

        # No plans - should be False
        assert not _plan_has_findout_subplan(state)

        # Add plan with findout subplan
        q1 = WhQuestion(variable="x", predicate="parties(x)")
        subplan1 = Plan(plan_type="findout", content=q1)
        plan = Plan(plan_type="nda_drafting", content=None, subplans=[subplan1])
        state.private.plan.append(plan)

        # Should be True
        assert _plan_has_findout_subplan(state)

    def test_no_duplicate_accommodation(self):
        """Test that questions already in issues or QUD are not duplicated."""
        from ibdm.rules.integration_rules import _accommodate_findout_to_issues

        state = InformationState()

        # Create question and add to private.issues
        q1 = WhQuestion(variable="x", predicate="parties(x)")
        state.private.issues.append(q1)

        # Create plan with same question
        subplan1 = Plan(plan_type="findout", content=q1)
        plan = Plan(plan_type="nda_drafting", content=None, subplans=[subplan1])
        state.private.plan.append(plan)

        # Apply Rule 4.1
        new_state = _accommodate_findout_to_issues(state)

        # Should not add duplicate
        assert len(new_state.private.issues) == 1
        assert new_state.private.issues[0] == q1

    def test_inactive_subplans_not_accommodated(self):
        """Test that completed/inactive subplans are not accommodated."""
        from ibdm.rules.integration_rules import _accommodate_findout_to_issues

        state = InformationState()

        # Create plan with completed findout subplan
        q1 = WhQuestion(variable="x", predicate="parties(x)")
        subplan1 = Plan(plan_type="findout", content=q1)
        subplan1.complete()  # Mark as completed
        plan = Plan(plan_type="nda_drafting", content=None, subplans=[subplan1])
        state.private.plan.append(plan)

        # Apply Rule 4.1
        new_state = _accommodate_findout_to_issues(state)

        # Should not accommodate completed subplan
        assert len(new_state.private.issues) == 0


class TestRule42LocalQuestionAccommodation:
    """Test Rule 4.2: LocalQuestionAccommodation from private.issues to QUD."""

    def test_rule_4_2_local_question_accommodation(self):
        """Test Rule 4.2: Issues raised to QUD when appropriate."""
        from ibdm.rules.selection_rules import _raise_issue_to_qud

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

    def test_has_raisable_issue_precondition(self):
        """Test precondition: detects raisable issues."""
        from ibdm.rules.selection_rules import _has_raisable_issue

        state = InformationState()

        # No issues - should be False
        assert not _has_raisable_issue(state)

        # Add issue, QUD empty - should be True
        q1 = WhQuestion(variable="x", predicate="parties(x)")
        state.private.issues.append(q1)
        assert _has_raisable_issue(state)

        # Add question to QUD - should be False (QUD not empty)
        state.shared.push_qud(WhQuestion(variable="z", predicate="test(z)"))
        assert not _has_raisable_issue(state)

    def test_raise_multiple_issues_incrementally(self):
        """Test that issues are raised one at a time."""
        from ibdm.rules.selection_rules import _raise_issue_to_qud

        state = InformationState()

        # Setup: Three questions in private.issues
        q1 = WhQuestion(variable="x", predicate="parties(x)")
        q2 = WhQuestion(variable="y", predicate="effective_date(y)")
        q3 = WhQuestion(variable="z", predicate="governing_law(z)")
        state.private.issues = [q1, q2, q3]

        # First raise
        new_state = _raise_issue_to_qud(state)
        assert len(new_state.shared.qud) == 1
        assert new_state.shared.qud[0] == q1
        assert len(new_state.private.issues) == 2

        # Clear QUD and raise again
        new_state.shared.qud.clear()
        new_state2 = _raise_issue_to_qud(new_state)
        assert len(new_state2.shared.qud) == 1
        assert new_state2.shared.qud[0] == q2
        assert len(new_state2.private.issues) == 1

    def test_empty_issues_no_effect(self):
        """Test that rule has no effect when issues list is empty."""
        from ibdm.rules.selection_rules import _raise_issue_to_qud

        state = InformationState()

        # No issues
        new_state = _raise_issue_to_qud(state)

        # Should have no effect
        assert len(new_state.shared.qud) == 0
        assert len(new_state.private.issues) == 0


class TestVolunteerInformationHandling:
    """Test volunteer information handling in integrate_answer."""

    def test_volunteer_information_handling(self):
        """Test IBiS3: User volunteers answer before being asked."""
        from ibdm.core import Answer, DialogueMove
        from ibdm.rules.integration_rules import _integrate_answer

        state = InformationState()

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

    def test_volunteer_answer_not_in_qud(self):
        """Test that volunteer answers don't affect QUD."""
        from ibdm.core import Answer, DialogueMove
        from ibdm.rules.integration_rules import _integrate_answer

        state = InformationState()

        # Setup: Two questions - one in issues, one in QUD
        q_issue = WhQuestion(variable="x", predicate="effective_date(x)")
        q_qud = WhQuestion(variable="y", predicate="parties(y)")
        state.private.issues.append(q_issue)
        state.shared.push_qud(q_qud)

        # User volunteers answer to the issue question (not the QUD question)
        answer = Answer(content="January 1, 2025", question_ref=q_issue)
        move = DialogueMove(move_type="answer", content=answer, speaker="user")
        state.private.beliefs["_temp_move"] = move

        # Apply integration
        new_state = _integrate_answer(state)

        # Assertions
        assert q_issue not in new_state.private.issues  # Removed from issues
        assert len(new_state.shared.qud) == 1  # QUD unchanged
        assert new_state.shared.qud[0] == q_qud  # Same question in QUD

    def test_normal_qud_answer_still_works(self):
        """Test that normal QUD answering still works after modification."""
        from ibdm.core import Answer, DialogueMove
        from ibdm.rules.integration_rules import _integrate_answer

        state = InformationState()

        # Setup: Question in QUD (normal case)
        q = WhQuestion(variable="x", predicate="parties(x)")
        state.shared.push_qud(q)

        # User answers the QUD question
        answer = Answer(content="Acme Corp", question_ref=q)
        move = DialogueMove(move_type="answer", content=answer, speaker="user")
        state.private.beliefs["_temp_move"] = move

        # Apply integration
        new_state = _integrate_answer(state)

        # Assertions
        assert len(new_state.shared.qud) == 0  # QUD popped
        assert len(new_state.shared.commitments) > 0  # Answer committed


class TestRule43IssueClarification:
    """Test Rule 4.3: IssueClarification for ambiguous/invalid utterances."""

    def test_rule_4_3_issue_clarification(self):
        """Test Rule 4.3: Clarification question pushed to QUD when needed."""
        from ibdm.rules.integration_rules import _accommodate_clarification

        state = InformationState()

        # Setup: Original question on QUD, invalid answer detected
        original_q = WhQuestion(variable="x", predicate="parties(x)")
        state.shared.push_qud(original_q)
        state.private.beliefs["_needs_clarification"] = True
        state.private.beliefs["_clarification_question"] = original_q
        state.private.beliefs["_invalid_answer"] = "some invalid value"

        # Apply Rule 4.3
        new_state = _accommodate_clarification(state)

        # Assertions
        assert len(new_state.shared.qud) == 2  # Original + clarification
        # Stack: index 0 is bottom (first pushed), index -1 is top (last pushed)
        assert new_state.shared.qud[0] == original_q  # Original at bottom (suspended)
        clarification_q = new_state.shared.qud[-1]  # Clarification on top
        assert clarification_q.constraints.get("is_clarification") is True
        assert not new_state.private.beliefs.get("_needs_clarification", False)

    def test_needs_clarification_question_precondition(self):
        """Test precondition: detects when clarification is needed."""
        from ibdm.rules.integration_rules import _needs_clarification_question

        state = InformationState()

        # No clarification marker - should be False
        assert not _needs_clarification_question(state)

        # Add clarification marker but no question - should be False
        state.private.beliefs["_needs_clarification"] = True
        assert not _needs_clarification_question(state)

        # Add question needing clarification - should be True
        q = WhQuestion(variable="x", predicate="parties(x)")
        state.private.beliefs["_clarification_question"] = q
        assert _needs_clarification_question(state)

    def test_clarification_question_suspends_original(self):
        """Test that clarification question suspends (doesn't remove) original question."""
        from ibdm.rules.integration_rules import _accommodate_clarification

        state = InformationState()

        # Setup: Original question on QUD
        original_q = WhQuestion(variable="x", predicate="effective_date(x)")
        state.shared.push_qud(original_q)
        state.private.beliefs["_needs_clarification"] = True
        state.private.beliefs["_clarification_question"] = original_q
        state.private.beliefs["_invalid_answer"] = "invalid date"

        # Apply Rule 4.3
        new_state = _accommodate_clarification(state)

        # Assertions
        assert len(new_state.shared.qud) == 2
        # Original question should still be on stack (suspended, not removed)
        assert original_q in new_state.shared.qud
        # Clarification question should be on top
        clarification_q = new_state.shared.top_qud()
        assert clarification_q is not None
        assert clarification_q.constraints.get("is_clarification") is True

    def test_no_duplicate_clarification_questions(self):
        """Test that clarification questions are not re-raised if already on QUD."""
        from ibdm.rules.integration_rules import _needs_clarification_question

        state = InformationState()

        # Setup: Clarification question already on QUD
        clarification_q = WhQuestion(
            variable="X",
            predicate="clarification",
            constraints={"is_clarification": True},
        )
        state.shared.push_qud(clarification_q)
        state.private.beliefs["_needs_clarification"] = True
        state.private.beliefs["_clarification_question"] = clarification_q

        # Precondition should be False (already have clarification on QUD)
        assert not _needs_clarification_question(state)

    def test_clarification_question_contains_context(self):
        """Test that clarification question contains context about the error."""
        from ibdm.rules.integration_rules import _accommodate_clarification

        state = InformationState()

        # Setup with specific original question and invalid answer
        original_q = WhQuestion(variable="x", predicate="governing_law(x)")
        invalid_answer = "blue"  # Invalid for governing law
        state.shared.push_qud(original_q)
        state.private.beliefs["_needs_clarification"] = True
        state.private.beliefs["_clarification_question"] = original_q
        state.private.beliefs["_invalid_answer"] = invalid_answer

        # Apply Rule 4.3
        new_state = _accommodate_clarification(state)

        # Check that clarification question contains context
        clarification_q = new_state.shared.top_qud()
        assert clarification_q is not None
        assert "for_question" in clarification_q.constraints
        assert "invalid_answer" in clarification_q.constraints
        assert clarification_q.constraints["invalid_answer"] == invalid_answer

    def test_clarification_clears_flag(self):
        """Test that accommodation clears the clarification flag."""
        from ibdm.rules.integration_rules import _accommodate_clarification

        state = InformationState()

        # Setup
        original_q = WhQuestion(variable="x", predicate="parties(x)")
        state.shared.push_qud(original_q)
        state.private.beliefs["_needs_clarification"] = True
        state.private.beliefs["_clarification_question"] = original_q
        state.private.beliefs["_invalid_answer"] = "invalid"

        # Apply Rule 4.3
        new_state = _accommodate_clarification(state)

        # Flag should be cleared
        assert not new_state.private.beliefs.get("_needs_clarification", False)
