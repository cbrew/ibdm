"""Unit tests for IBiS3 Question Reaccommodation (Rules 4.6, 4.7, 4.8).

Tests the implementation of Larsson (2002) Section 4.6.6:
- Rule 4.6: QuestionReaccommodation (accommodate Com 2Issues)
- Rule 4.7: Retract incompatible commitments
- Rule 4.8: DependentQuestionReaccommodation

Based on Larsson, S. (2002), Section 4.6.6 - Question Reaccommodation.
"""

import pytest

from ibdm.core import Answer, DialogueMove, InformationState, WhQuestion
from ibdm.domains.travel_domain import get_travel_domain
from ibdm.rules.integration_rules import create_integration_rules


@pytest.fixture
def travel_domain():
    """Get travel domain with dependencies configured."""
    return get_travel_domain()


@pytest.fixture
def state_with_commitment():
    """Create state with an existing commitment about departure day."""
    state = InformationState()

    # Add a question to private.issues (as if it was accommodated)
    date_question = WhQuestion(predicate="depart_day", variable="X")
    state.private.issues.append(date_question)

    # Add commitment (as if user already answered "april 5th")
    state.shared.commitments.add("depart_day: april 5th")

    return state


@pytest.fixture
def state_with_dependent_commitments():
    """Create state with commitments that have dependencies.

    In travel domain:
    - price_quote depends on travel_class
    - If travel_class changes, price_quote must be reaccommodated
    """
    from ibdm.core import Plan

    state = InformationState()

    # Add a travel plan so _get_active_domain() returns travel domain
    travel_plan = Plan(plan_type="travel_booking", content="booking", status="active")
    state.private.plan.append(travel_plan)

    # Add commitments for both class and price (using correct predicate names)
    state.shared.commitments.add("travel_class: economy")
    state.shared.commitments.add("price_quote: 100 dollars")

    return state


class TestRule46QuestionReaccommodation:
    """Test Rule 4.6 - QuestionReaccommodation (accommodate Com 2Issues)."""

    def test_conflicting_answer_triggers_reaccommodation(self, state_with_commitment):
        """Test that providing conflicting answer triggers reaccommodation.

        Dialogue 4.6 from Larsson:
        User says "april 5th"
        [commitment added: "depart_day: april 5th"]
        Later: User says "actually, april 4th"
        → System should detect conflict and reaccommodate question
        """
        # Arrange: User provides conflicting answer
        # Set question_ref so Answer knows what question it's answering
        date_question = WhQuestion(predicate="depart_day", variable="X")
        new_answer = Answer(content="april 4th", question_ref=date_question)
        answer_move = DialogueMove(move_type="answer", content=new_answer, speaker="user")
        state_with_commitment.private.beliefs["_temp_move"] = answer_move

        # Act: Run integration rules
        rules = create_integration_rules()
        reaccommodate_rule = next(
            r for r in rules if r.name == "reaccommodate_question_from_commitment"
        )

        # Check precondition
        assert reaccommodate_rule.preconditions(state_with_commitment) is True

        # Apply effect
        new_state = reaccommodate_rule.effects(state_with_commitment)

        # Assert: Question should be re-raised to issues
        assert date_question in new_state.private.issues

    def test_same_answer_does_not_trigger_reaccommodation(self, state_with_commitment):
        """Test that providing same answer doesn't trigger reaccommodation."""
        # Arrange: User provides same answer
        same_answer = Answer(content="april 5th")
        answer_move = DialogueMove(move_type="answer", content=same_answer, speaker="user")
        state_with_commitment.private.beliefs["_temp_move"] = answer_move

        # Act: Check precondition
        rules = create_integration_rules()
        reaccommodate_rule = next(
            r for r in rules if r.name == "reaccommodate_question_from_commitment"
        )

        # Assert: Should NOT trigger reaccommodation
        assert reaccommodate_rule.preconditions(state_with_commitment) is False

    def test_answer_to_different_question_does_not_trigger_reaccommodation(self):
        """Test that answer to different question doesn't trigger reaccommodation."""
        # Arrange: Fresh state with commitment about departure day
        state = InformationState()
        state.shared.commitments.add("depart_day: april 5th")

        # User answers dest_city (different question)
        destination_answer = Answer(content="London")
        answer_move = DialogueMove(move_type="answer", content=destination_answer, speaker="user")
        state.private.beliefs["_temp_move"] = answer_move

        # Act: Check precondition
        rules = create_integration_rules()
        reaccommodate_rule = next(
            r for r in rules if r.name == "reaccommodate_question_from_commitment"
        )

        # Assert: Should NOT trigger reaccommodation
        assert reaccommodate_rule.preconditions(state) is False


class TestRule47RetractIncompatibleCommitment:
    """Test Rule 4.7 - Retract incompatible commitment."""

    def test_retract_old_commitment(self, state_with_commitment):
        """Test that old incompatible commitment is retracted."""
        # Arrange: Mark old commitment for retraction
        state_with_commitment.private.beliefs["_reaccommodate_old_commitment"] = (
            "travel_date: april 5th"
        )

        # Act: Run retract rule
        rules = create_integration_rules()
        retract_rule = next(r for r in rules if r.name == "retract_incompatible_commitment")

        # Check precondition
        assert retract_rule.preconditions(state_with_commitment) is True

        # Apply effect
        new_state = retract_rule.effects(state_with_commitment)

        # Assert: Old commitment should be removed
        assert "travel_date: april 5th" not in new_state.shared.commitments
        assert new_state.private.beliefs["_reaccommodate_old_commitment"] is None

    def test_retract_only_when_marked(self):
        """Test that retract only happens when reaccommodation has marked it."""
        # Arrange: State with commitment but no retract marker
        state = InformationState()
        state.shared.commitments.add("travel_date: april 5th")

        # Act: Check precondition
        rules = create_integration_rules()
        retract_rule = next(r for r in rules if r.name == "retract_incompatible_commitment")

        # Assert: Should NOT trigger
        assert retract_rule.preconditions(state) is False


class TestRule48DependentQuestionReaccommodation:
    """Test Rule 4.8 - DependentQuestionReaccommodation."""

    def test_dependent_question_reaccommodated_when_base_changes(
        self, state_with_dependent_commitments
    ):
        """Test that changing base question reaccommodates dependent questions.

        Example from Larsson Section 4.6.6:
        User changes travel_class from "economy" to "business"
        → price_quote depends on travel_class
        → Both class and price questions should be reaccommodated
        """
        # Arrange: Mark travel_class question for reaccommodation
        class_question = WhQuestion(predicate="travel_class", variable="X")
        state_with_dependent_commitments.private.beliefs["_reaccommodate_question"] = class_question

        # Update commitments to use correct predicates (price_quote not price)
        state_with_dependent_commitments.shared.commitments.clear()
        state_with_dependent_commitments.shared.commitments.add("travel_class: economy")
        state_with_dependent_commitments.shared.commitments.add("price_quote: 100 dollars")

        # Act: Run dependent reaccommodation rule
        rules = create_integration_rules()
        dependent_rule = next(r for r in rules if r.name == "reaccommodate_dependent_questions")

        # Check precondition
        assert dependent_rule.preconditions(state_with_dependent_commitments) is True

        # Apply effect
        new_state = dependent_rule.effects(state_with_dependent_commitments)

        # Assert: Price commitment should be retracted
        assert "price_quote: 100 dollars" not in new_state.shared.commitments

        # Assert: Price question should be re-raised to issues
        price_question = WhQuestion(predicate="price_quote", variable="X")
        assert price_question in new_state.private.issues

    def test_no_dependent_reaccommodation_without_dependencies(self, state_with_commitment):
        """Test that questions without dependencies don't trigger dependent reaccommodation."""
        # Arrange: Mark date question for reaccommodation (has no dependents)
        date_question = WhQuestion(predicate="depart_day", variable="X")
        state_with_commitment.private.beliefs["_reaccommodate_question"] = date_question

        # Act: Check precondition
        rules = create_integration_rules()
        dependent_rule = next(r for r in rules if r.name == "reaccommodate_dependent_questions")

        # Assert: Should NOT trigger (depart_day has no dependent questions)
        assert dependent_rule.preconditions(state_with_commitment) is False


class TestDomainHelpers:
    """Test domain helper methods for reaccommodation."""

    def test_incompatible_same_question_different_answers(self, travel_domain):
        """Test incompatibility detection for same question, different answers."""
        prop1 = "depart_day: april 5th"
        prop2 = "depart_day: april 4th"

        assert travel_domain.incompatible(prop1, prop2) is True

    def test_not_incompatible_same_question_same_answer(self, travel_domain):
        """Test that same answer is not incompatible."""
        prop1 = "depart_day: april 5th"
        prop2 = "depart_day: april 5th"

        assert travel_domain.incompatible(prop1, prop2) is False

    def test_not_incompatible_different_questions(self, travel_domain):
        """Test that different questions are not incompatible."""
        prop1 = "depart_day: april 5th"
        prop2 = "dest_city: London"

        assert travel_domain.incompatible(prop1, prop2) is False

    def test_get_question_from_commitment(self, travel_domain):
        """Test extracting question from commitment string."""
        commitment = "depart_day: april 5th"
        question = travel_domain.get_question_from_commitment(commitment)

        assert question is not None
        assert question.predicate == "depart_day"

    def test_get_question_from_invalid_commitment(self, travel_domain):
        """Test extracting question from invalid commitment returns None."""
        invalid_commitment = "not a valid commitment"
        question = travel_domain.get_question_from_commitment(invalid_commitment)

        assert question is None  # Returns None for invalid format
