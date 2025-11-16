"""Tests for IBiS3 accommodation rules (Rules 4.1 and 4.2).

Tests issue accommodation (Rule 4.1) and local question accommodation (Rule 4.2)
per Larsson (2002) Section 4.6.

IBiS3 Enhancement: Questions from task plans are accommodated to private.issues
first, then raised to QUD incrementally when contextually appropriate.
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
