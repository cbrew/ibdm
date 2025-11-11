"""Tests for Phase 4 accommodation implementations.

Tests question accommodation, task accommodation, answer accommodation,
and plan inference.
"""

from ibdm.accommodation import (
    accommodate_question,
    accommodate_task,
    infer_plan,
    resolve_elliptical_answer,
)
from ibdm.core import (
    AltQuestion,
    DialogueMove,
    InformationState,
    WhQuestion,
    YNQuestion,
)


class TestQuestionAccommodation:
    """Test question accommodation mechanisms."""

    def test_bare_wh_question_from_qud(self):
        """Test accommodating bare wh-question using QUD context."""
        state = InformationState(agent_id="system")
        # Set up context: previous question about weather
        previous_q = WhQuestion(variable="x", predicate="weather")
        state.shared.push_qud(previous_q)

        # User asks bare "What?"
        bare_q = WhQuestion(variable="x", predicate="what", constraints={"wh_word": "what"})
        accommodated = accommodate_question(bare_q, state)

        # Should inherit predicate from context
        assert accommodated.predicate == "weather"
        assert accommodated.constraints.get("accommodated") is True

    def test_anaphoric_wh_question(self):
        """Test resolving anaphoric reference in wh-question."""
        state = InformationState(agent_id="system")
        # Context: question about Paris
        context_q = WhQuestion(variable="x", predicate="population of Paris")
        state.shared.push_qud(context_q)

        # User asks "What about it?"
        anaphoric_q = WhQuestion(
            variable="x", predicate="what about it", constraints={"wh_word": "what"}
        )
        accommodated = accommodate_question(anaphoric_q, state)

        # "it" should be resolved to "population of Paris"
        assert "population of Paris" in accommodated.predicate
        assert accommodated.constraints.get("resolved_anaphora") is True

    def test_follow_up_question(self):
        """Test accommodating follow-up question with 'and'."""
        state = InformationState(agent_id="system")
        # Context: question about a meeting
        context_q = WhQuestion(variable="x", predicate="time of the meeting")
        state.shared.push_qud(context_q)

        # User asks "And the location?"
        followup_q = WhQuestion(
            variable="x", predicate="and the location", constraints={"wh_word": "what"}
        )
        accommodated = accommodate_question(followup_q, state)

        # Should include entity from context
        assert "location" in accommodated.predicate.lower()
        assert accommodated.constraints.get("follow_up") is True

    def test_yn_question_anaphora(self):
        """Test resolving anaphora in yes/no questions."""
        state = InformationState(agent_id="system")
        # Context: question about the weather
        context_q = WhQuestion(variable="x", predicate="weather")
        state.shared.push_qud(context_q)

        # User asks "Is it sunny?"
        anaphoric_yn = YNQuestion(proposition="is it sunny")
        accommodated = accommodate_question(anaphoric_yn, state)

        # "it" should be resolved
        assert "weather" in accommodated.proposition
        assert accommodated.parameters.get("resolved_anaphora") is True


class TestTaskAccommodation:
    """Test task accommodation mechanisms."""

    def test_anaphoric_task(self):
        """Test resolving anaphoric reference in task."""
        state = InformationState(agent_id="system")
        # Add recent assertion
        assertion = DialogueMove(move_type="assert", content="book a table", speaker="user")
        state.shared.last_moves.append(assertion)

        # User says "Do that"
        task_move = accommodate_task("Do that", state)

        assert "book a table" in task_move.content

    def test_follow_up_task(self):
        """Test accommodating follow-up task with 'also'."""
        state = InformationState(agent_id="system")

        # User says "Also send confirmation"
        task_move = accommodate_task("Also send confirmation", state)

        # Should remove "also" and create request
        assert task_move.move_type == "request"
        assert "send confirmation" in task_move.content
        assert "also" not in task_move.content.lower()

    def test_abbreviated_cancel(self):
        """Test resolving abbreviated 'cancel' command."""
        state = InformationState(agent_id="system")
        # Add a QUD
        question = WhQuestion(variable="x", predicate="restaurant")
        state.shared.push_qud(question)

        # User says "Cancel"
        task_move = accommodate_task("Cancel", state)

        # Should infer what to cancel
        assert task_move.move_type == "request"
        assert "cancel" in task_move.content.lower()


class TestAnswerAccommodation:
    """Test answer accommodation for ellipsis."""

    def test_fragment_wh_answer(self):
        """Test resolving fragment answer to wh-question."""
        state = InformationState(agent_id="system")
        # Question: "When is the meeting?"
        question = WhQuestion(
            variable="x", predicate="when is the meeting", constraints={"wh_word": "when"}
        )
        state.shared.push_qud(question)

        # Answer: "Tomorrow"
        answer = resolve_elliptical_answer("Tomorrow", state)

        assert answer.content == "Tomorrow"
        assert answer.question_ref == question

    def test_yn_answer_yes(self):
        """Test resolving yes answer to yn-question."""
        state = InformationState(agent_id="system")
        # Question: "Is it raining?"
        question = YNQuestion(proposition="is it raining")
        state.shared.push_qud(question)

        # Answer: "Yes"
        answer = resolve_elliptical_answer("Yes", state)

        assert answer.content is True
        assert answer.question_ref == question

    def test_yn_answer_no(self):
        """Test resolving no answer to yn-question."""
        state = InformationState(agent_id="system")
        question = YNQuestion(proposition="is it sunny")
        state.shared.push_qud(question)

        answer = resolve_elliptical_answer("No", state)

        assert answer.content is False
        assert answer.question_ref == question

    def test_alt_answer(self):
        """Test resolving alternative answer."""
        state = InformationState(agent_id="system")
        # Question: "Tea or coffee?"
        question = AltQuestion(alternatives=["tea", "coffee"])
        state.shared.push_qud(question)

        # Answer: "Coffee"
        answer = resolve_elliptical_answer("Coffee", state)

        assert answer.content == "coffee"
        assert answer.question_ref == question

    def test_no_qud_context(self):
        """Test answer resolution without QUD context."""
        state = InformationState(agent_id="system")
        # No question on QUD

        answer = resolve_elliptical_answer("Some answer", state)

        # Should return literal answer
        assert answer.content == "Some answer"
        assert answer.question_ref is None


class TestPlanInference:
    """Test plan inference mechanisms."""

    def test_infer_from_wh_question(self):
        """Test inferring plan from wh-question."""
        state = InformationState(agent_id="system")
        question = WhQuestion(variable="x", predicate="weather", constraints={"wh_word": "what"})
        move = DialogueMove(move_type="ask", content=question, speaker="user")

        plan = infer_plan(move, state)

        assert plan is not None
        assert "weather" in str(plan.content).lower()
        assert plan.plan_type == "findout"
        assert plan.status == "active"

    def test_infer_from_yn_request(self):
        """Test inferring plan from polite request (yn-question)."""
        state = InformationState(agent_id="system")
        # "Can you book a table?"
        question = YNQuestion(proposition="can you book a table")
        move = DialogueMove(move_type="ask", content=question, speaker="user")

        plan = infer_plan(move, state)

        assert plan is not None
        assert "book a table" in str(plan.content).lower()
        assert plan.plan_type == "perform"

    def test_infer_from_request(self):
        """Test inferring plan from direct request."""
        state = InformationState(agent_id="system")
        move = DialogueMove(move_type="request", content="Book a flight", speaker="user")

        plan = infer_plan(move, state)

        assert plan is not None
        assert "book" in str(plan.content).lower()
        assert plan.plan_type == "perform"

    def test_time_question_plan(self):
        """Test inferring plan for time-related question."""
        state = InformationState(agent_id="system")
        question = WhQuestion(
            variable="x", predicate="time of the meeting", constraints={"wh_word": "when"}
        )
        move = DialogueMove(move_type="ask", content=question, speaker="user")

        plan = infer_plan(move, state)

        assert plan is not None
        assert "time" in str(plan.content).lower()
        assert plan.plan_type == "findout"

    def test_no_plan_inference(self):
        """Test that no plan is inferred from non-question, non-request moves."""
        state = InformationState(agent_id="system")
        move = DialogueMove(move_type="greet", content="Hello", speaker="user")

        plan = infer_plan(move, state)

        assert plan is None


class TestAccommodationIntegration:
    """Test integration of accommodation mechanisms."""

    def test_question_answer_accommodation_flow(self):
        """Test complete flow with question accommodation and answer resolution."""
        state = InformationState(agent_id="system")

        # Step 1: User asks "What is the weather?"
        q1 = WhQuestion(
            variable="x", predicate="what is the weather", constraints={"wh_word": "what"}
        )
        state.shared.push_qud(q1)

        # Step 2: User asks a bare question like "What?"
        # (Note: "And tomorrow?" would be follow-up, but "What?" triggers bare wh accommodation)
        q2 = WhQuestion(variable="x", predicate="what", constraints={"wh_word": "what"})
        accommodated_q = accommodate_question(q2, state)

        # Should be accommodated with context from QUD
        assert accommodated_q.constraints.get("accommodated") is True
        assert accommodated_q.predicate == q1.predicate  # Should inherit predicate

        # Step 3: System answers, user says "Yes"
        # (imagining the question became "Is it sunny?")
        state.shared.pop_qud()  # Remove first question
        yn_q = YNQuestion(proposition="is it sunny tomorrow")
        state.shared.push_qud(yn_q)

        answer = resolve_elliptical_answer("Yes", state)
        assert answer.content is True

    def test_plan_inference_with_accommodation(self):
        """Test plan inference after question accommodation."""
        state = InformationState(agent_id="system")

        # Previous question about meetings
        prev_q = WhQuestion(variable="x", predicate="meeting time")
        state.shared.push_qud(prev_q)

        # User asks "And the location?"
        follow_up = WhQuestion(
            variable="x", predicate="and the location", constraints={"wh_word": "what"}
        )
        accommodated = accommodate_question(follow_up, state)

        # Create move and infer plan
        move = DialogueMove(move_type="ask", content=accommodated, speaker="user")
        plan = infer_plan(move, state)

        # Should infer information-seeking plan
        assert plan is not None
        assert plan.plan_type == "findout"
