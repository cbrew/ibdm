"""Tests for IBiS3 accommodation rules (Rules 4.1, 4.2, 4.3, and 4.4).

Tests issue accommodation (Rule 4.1), local question accommodation (Rule 4.2),
issue clarification (Rule 4.3), and dependent issue accommodation (Rule 4.4)
per Larsson (2002) Section 4.6.

IBiS3 Enhancement: Questions from task plans are accommodated to private.issues
first, then raised to QUD incrementally when contextually appropriate.
Clarification questions are pushed to QUD to suspend original questions.
Dependent questions are suspended until their prerequisites are answered.
"""

from ibdm.core import (
    DomainModel,
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

    def test_answer_resolves_suspended_question(self):
        """Test ibdm-203: Answer to suspended question pops both clarification and original.

        When a clarification question is on top of QUD and the user provides an answer
        to the suspended (original) question beneath it, both questions should be popped.
        This implements proper nested dialogue management per Larsson Section 4.2.
        """
        from ibdm.core import Answer, DialogueMove, DomainModel
        from ibdm.rules.integration_rules import _integrate_answer

        state = InformationState()

        # Setup domain with nda_type validation
        domain = DomainModel("nda")
        domain.add_predicate("nda_type", arity=1)

        # Register domain
        state.private.beliefs["_active_domain"] = domain

        # Setup: Original question on QUD
        original_q = WhQuestion(variable="x", predicate="nda_type")
        state.shared.push_qud(original_q)

        # Clarification question pushed on top (suspends original)
        clarification_q = WhQuestion(
            variable="X",
            predicate="clarification_for_nda_type",
            constraints={"is_clarification": True, "for_question": str(original_q)},
        )
        state.shared.push_qud(clarification_q)

        # QUD depth should be 2
        assert len(state.shared.qud) == 2

        # User provides answer to ORIGINAL question (not clarification)
        answer = Answer(content="mutual")
        move = DialogueMove(speaker="user", move_type="answer", content=answer)
        state.private.beliefs["_temp_move"] = move

        # Apply integration
        new_state = _integrate_answer(state)

        # Assertions
        # Both questions should be popped
        assert len(new_state.shared.qud) == 0
        # Answer should be committed
        assert len(new_state.shared.commitments) > 0
        # Commitment should reference the ORIGINAL question, not clarification
        commitment_str = list(new_state.shared.commitments)[0]
        assert "nda_type" in commitment_str
        assert "mutual" in commitment_str

    def test_answer_does_not_resolve_suspended_keeps_qud(self):
        """Test that invalid answer to neither question keeps QUD intact.

        If answer doesn't resolve top question or suspended question,
        clarification flag should be set but QUD should remain unchanged.
        """
        from ibdm.core import AltQuestion, Answer, DialogueMove, DomainModel
        from ibdm.rules.integration_rules import _integrate_answer

        state = InformationState()

        # Setup domain
        domain = DomainModel("nda")
        domain.add_predicate("nda_type", arity=1)
        state.private.beliefs["_active_domain"] = domain

        # Setup: Original question (ALT question with specific alternatives) + clarification on QUD
        # Using AltQuestion so we can test strict validation
        original_q = AltQuestion(alternatives=["mutual", "one-way"])
        state.shared.push_qud(original_q)
        clarification_q = WhQuestion(
            variable="X",
            predicate="clarification_for_nda_type",
            constraints={"is_clarification": True},
        )
        state.shared.push_qud(clarification_q)

        # User provides invalid answer (not in alternatives)
        answer = Answer(content="invalid_value")
        move = DialogueMove(speaker="user", move_type="answer", content=answer)
        state.private.beliefs["_temp_move"] = move

        # Apply integration
        new_state = _integrate_answer(state)

        # Assertions
        # QUD should remain unchanged
        assert len(new_state.shared.qud) == 2
        # Clarification flag should be set
        assert new_state.private.beliefs.get("_needs_clarification", False)
        # No commitment added
        assert len(new_state.shared.commitments) == 0


class TestRule44DependentIssueAccommodation:
    """Test Rule 4.4: DependentIssueAccommodation for prerequisite questions."""

    def test_rule_4_4_dependent_issue_accommodation(self):
        """Test Rule 4.4: Prerequisite question pushed to QUD when needed."""
        from ibdm.rules.selection_rules import _accommodate_dependency

        state = InformationState()

        # Setup domain with dependencies
        domain = DomainModel("travel")
        domain.add_predicate("price", arity=1)
        domain.add_predicate("departure_city", arity=1)
        domain.add_dependency("price", "departure_city")  # price depends on city

        state.private.beliefs["_domain"] = domain

        # Setup: Question on QUD that has dependency
        price_q = WhQuestion(variable="x", predicate="price")
        state.shared.push_qud(price_q)

        # Apply Rule 4.4
        new_state = _accommodate_dependency(state)

        # Assertions
        assert len(new_state.shared.qud) == 2  # Original + prerequisite
        assert new_state.shared.qud[0] == price_q  # Price at bottom (suspended)
        prereq_q = new_state.shared.qud[-1]  # Prerequisite on top
        assert prereq_q.predicate == "departure_city"
        assert prereq_q.constraints.get("is_prerequisite") is True

    def test_has_unanswered_dependency_precondition(self):
        """Test precondition: detects unanswered dependencies."""
        from ibdm.rules.selection_rules import _has_unanswered_dependency

        state = InformationState()

        # Setup domain with dependencies
        domain = DomainModel("travel")
        domain.add_predicate("price", arity=1)
        domain.add_predicate("departure_city", arity=1)
        domain.add_dependency("price", "departure_city")

        state.private.beliefs["_domain"] = domain

        # No question on QUD - should be False
        assert not _has_unanswered_dependency(state)

        # Add question with dependency
        price_q = WhQuestion(variable="x", predicate="price")
        state.shared.push_qud(price_q)

        # Should be True (dependency not answered)
        assert _has_unanswered_dependency(state)

        # Answer the dependency
        state.private.beliefs["departure_city"] = "London"

        # Should be False (dependency answered)
        assert not _has_unanswered_dependency(state)

    def test_no_dependency_no_accommodation(self):
        """Test that questions without dependencies are not accommodated."""
        from ibdm.rules.selection_rules import _accommodate_dependency

        state = InformationState()

        # Setup domain without dependencies
        domain = DomainModel("simple")
        domain.add_predicate("name", arity=1)

        state.private.beliefs["_domain"] = domain

        # Add question with no dependencies
        name_q = WhQuestion(variable="x", predicate="name")
        state.shared.push_qud(name_q)

        # Apply Rule 4.4
        new_state = _accommodate_dependency(state)

        # Should have no effect
        assert len(new_state.shared.qud) == 1
        assert new_state.shared.qud[0] == name_q

    def test_multiple_dependencies_one_at_a_time(self):
        """Test that multiple dependencies are accommodated one at a time."""
        from ibdm.rules.selection_rules import _accommodate_dependency

        state = InformationState()

        # Setup domain with multiple dependencies
        domain = DomainModel("travel")
        domain.add_predicate("price", arity=1)
        domain.add_predicate("departure_city", arity=1)
        domain.add_predicate("travel_date", arity=1)
        domain.add_dependency("price", ["departure_city", "travel_date"])

        state.private.beliefs["_domain"] = domain

        # Add question with multiple dependencies
        price_q = WhQuestion(variable="x", predicate="price")
        state.shared.push_qud(price_q)

        # Apply Rule 4.4
        new_state = _accommodate_dependency(state)

        # Should only accommodate first dependency
        assert len(new_state.shared.qud) == 2
        assert new_state.shared.qud[0] == price_q
        # First dependency should be on top
        prereq_q = new_state.shared.qud[-1]
        assert prereq_q.predicate in ["departure_city", "travel_date"]

    def test_dependency_contains_context(self):
        """Test that prerequisite question contains context about dependent question."""
        from ibdm.rules.selection_rules import _accommodate_dependency

        state = InformationState()

        # Setup domain
        domain = DomainModel("travel")
        domain.add_predicate("price", arity=1)
        domain.add_predicate("destination", arity=1)
        domain.add_dependency("price", "destination")

        state.private.beliefs["_domain"] = domain

        # Add dependent question
        price_q = WhQuestion(variable="x", predicate="price")
        state.shared.push_qud(price_q)

        # Apply Rule 4.4
        new_state = _accommodate_dependency(state)

        # Check prerequisite contains context
        prereq_q = new_state.shared.top_qud()
        assert prereq_q is not None
        assert "for_question" in prereq_q.constraints
        assert prereq_q.constraints["for_question"] == str(price_q)
