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
