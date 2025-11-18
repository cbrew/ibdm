"""Tests for question override functionality.

Tests that users can skip optional questions (required=False) when they
don't have the information, and that plans can execute with overridden questions.
"""

from ibdm.core import (
    DialogueMove,
    InformationState,
    Plan,
    PrivateIS,
    SharedIS,
    WhQuestion,
)
from ibdm.rules.integration_rules import (
    _accommodate_skip_question,
    _is_skip_request_move,
)
from ibdm.rules.selection_rules import _has_communicative_plan
from ibdm.utils.skip_detection import is_skip_request


class TestSkipDetection:
    """Test the skip request pattern matching."""

    def test_skip_patterns(self):
        """Test various skip request patterns are recognized."""
        skip_requests = [
            "skip that",
            "skip this question",
            "pass",
            "I don't have that information",
            "I don't know",
            "not available",
            "no available",
            "move on",
            "proceed anyway",
            "proceed without it",
            "can't provide",
            "no info",
            "no information",
            "idk",
            "dunno",
        ]

        for request in skip_requests:
            assert is_skip_request(request), f"Should recognize skip request: {request}"

    def test_non_skip_patterns(self):
        """Test that normal answers are not mistaken for skip requests."""
        normal_answers = [
            "Paris",
            "John Smith",
            "Yes",
            "No",
            "I think it should be blue",
            "Let me check that",
            "42",
        ]

        for answer in normal_answers:
            assert not is_skip_request(answer), f"Should NOT recognize as skip: {answer}"


class TestQuestionOverride:
    """Test question override functionality in dialogue management."""

    def test_optional_question_can_be_skipped(self):
        """Test that optional questions (required=False) can be skipped."""
        # Create a state with an optional question on QUD
        optional_question = WhQuestion(
            predicate="favorite_color",
            variable="color",
            required=False,  # Optional question
        )

        state = InformationState(
            private=PrivateIS(),
            shared=SharedIS(qud=[optional_question]),
            agent_id="system",
        )

        # User says "I don't know"
        skip_move = DialogueMove(
            move_type="answer",  # NLU would classify as answer
            content="I don't know",
            speaker="user",
        )

        # Store move in temp for integration rules
        state.private.beliefs["_temp_move"] = skip_move

        # Check precondition
        assert _is_skip_request_move(state), "Should recognize skip request"

        # Apply accommodation rule
        new_state = _accommodate_skip_question(state)

        # Question should be removed from QUD
        assert len(new_state.shared.qud) == 0, "Optional question should be removed from QUD"

        # Question should be in overridden_questions
        assert optional_question in new_state.private.overridden_questions, (
            "Question should be tracked as overridden"
        )

    def test_required_question_cannot_be_skipped(self):
        """Test that required questions (required=True) cannot be skipped."""
        # Create a state with a required question on QUD
        required_question = WhQuestion(
            predicate="destination",
            variable="city",
            required=True,  # Required question
        )

        state = InformationState(
            private=PrivateIS(),
            shared=SharedIS(qud=[required_question]),
            agent_id="system",
        )

        # User says "skip that"
        skip_move = DialogueMove(
            move_type="answer",
            content="skip that",
            speaker="user",
        )

        state.private.beliefs["_temp_move"] = skip_move

        # Check precondition - should NOT trigger for required question
        assert not _is_skip_request_move(state), "Should not trigger for required question"

        # Apply accommodation rule (should have no effect)
        new_state = _accommodate_skip_question(state)

        # Question should still be on QUD (cannot be skipped)
        assert required_question in new_state.shared.qud, "Required question should remain on QUD"

        # Question should NOT be in overridden_questions
        assert required_question not in new_state.private.overridden_questions, (
            "Required question should not be overridden"
        )

    def test_plan_executes_with_overridden_questions(self):
        """Test that a plan can execute if all findout subplans are complete or overridden."""
        # Create a plan with two findout subplans: one required, one optional
        required_question = WhQuestion(
            predicate="destination",
            variable="city",
            required=True,
        )

        optional_question = WhQuestion(
            predicate="seat_preference",
            variable="seat",
            required=False,
        )

        # Create findout subplans
        required_findout = Plan(
            plan_type="findout",
            content=required_question,
            status="completed",  # User answered this one
        )

        optional_findout = Plan(
            plan_type="findout",
            content=optional_question,
            status="active",  # Still active, but will be overridden
        )

        # Create main plan with these subplans
        main_plan = Plan(
            plan_type="inform",
            content="Booking confirmed",
            subplans=[required_findout, optional_findout],
        )

        # Create state with this plan and the optional question overridden
        state = InformationState(
            private=PrivateIS(
                plan=[main_plan],
                overridden_questions=[optional_question],
            ),
            shared=SharedIS(),
            agent_id="system",
        )

        # Check precondition - plan should be ready to execute
        assert _has_communicative_plan(state), (
            "Plan should be executable with overridden optional question"
        )

    def test_plan_blocked_with_unanswered_required_question(self):
        """Test that a plan is blocked if required questions are unanswered."""
        # Create a plan with an unanswered required question
        required_question = WhQuestion(
            predicate="destination",
            variable="city",
            required=True,
        )

        required_findout = Plan(
            plan_type="findout",
            content=required_question,
            status="active",  # Still needs an answer
        )

        main_plan = Plan(
            plan_type="inform",
            content="Booking confirmed",
            subplans=[required_findout],
        )

        state = InformationState(
            private=PrivateIS(plan=[main_plan]),
            shared=SharedIS(),
            agent_id="system",
        )

        # Check precondition - plan should NOT be ready to execute
        assert not _has_communicative_plan(state), (
            "Plan should be blocked with unanswered required question"
        )

    def test_serialization_of_overridden_questions(self):
        """Test that overridden_questions can be serialized and deserialized."""
        question = WhQuestion(
            predicate="favorite_color",
            variable="color",
            required=False,
        )

        state = InformationState(
            private=PrivateIS(overridden_questions=[question]),
            shared=SharedIS(),
            agent_id="system",
        )

        # Serialize
        state_dict = state.to_dict()

        # Deserialize
        restored_state = InformationState.from_dict(state_dict)

        # Check overridden_questions is preserved
        assert len(restored_state.private.overridden_questions) == 1
        restored_question = restored_state.private.overridden_questions[0]
        assert isinstance(restored_question, WhQuestion)
        assert restored_question.predicate == "favorite_color"
        assert restored_question.required is False
