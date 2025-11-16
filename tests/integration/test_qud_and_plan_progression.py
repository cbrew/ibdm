"""Integration tests for QUD management and plan progression.

These tests verify that:
1. QUD is managed as a stack (LIFO) across multiple turns
2. Plans progress correctly through subgoals
3. Invalid answers keep questions on QUD and trigger clarification
4. Valid answers pop questions and advance to next subplan

Based on Larsson (2002) Section 2.6 (Plan Execution) and Section 2.4 (QUD).
"""

from ibdm.core import Answer, DialogueMove, InformationState, Plan, WhQuestion
from ibdm.rules import (
    RuleSet,
    create_integration_rules,
)


class TestQUDManagement:
    """Test QUD stack management across multiple dialogue turns."""

    def test_qud_lifo_behavior(self):
        """Verify QUD operates as a stack (LIFO - Last In, First Out)."""
        state = InformationState(agent_id="system")

        # Push three questions onto QUD stack
        q1 = WhQuestion(variable="x", predicate="task")
        q2 = WhQuestion(variable="y", predicate="deadline")
        q3 = WhQuestion(variable="z", predicate="priority")

        state.shared.push_qud(q1)
        state.shared.push_qud(q2)
        state.shared.push_qud(q3)

        # Verify stack order (top should be last pushed)
        assert len(state.shared.qud) == 3
        assert state.shared.top_qud() == q3

        # Pop questions - should come off in LIFO order
        state.shared.pop_qud()
        assert state.shared.top_qud() == q2

        state.shared.pop_qud()
        assert state.shared.top_qud() == q1

        state.shared.pop_qud()
        assert state.shared.qud == []

    def test_question_stays_on_qud_after_invalid_answer(self):
        """Verify question remains on QUD when answer is invalid."""
        state = InformationState(agent_id="system")

        # Setup question on QUD
        question = WhQuestion(variable="x", predicate="legal_entities")
        state.shared.push_qud(question)
        initial_qud_len = len(state.shared.qud)

        # Provide invalid answer (empty value)
        invalid_answer = Answer(content="", question_ref=question)
        move = DialogueMove(move_type="answer", content=invalid_answer, speaker="user")
        state.private.beliefs["_temp_move"] = move

        # Apply integration rules
        rules = create_integration_rules()
        ruleset = RuleSet()
        for rule in rules:
            ruleset.add_rule(rule)

        new_state = ruleset.apply_rules("integration", state)

        # Verify: Question should still be on QUD (not popped)
        assert len(new_state.shared.qud) == initial_qud_len
        assert new_state.shared.top_qud() == question

        # Verify: Clarification needed
        assert new_state.private.beliefs.get("_needs_clarification") is True

    def test_question_removed_from_qud_after_valid_answer(self):
        """Verify question is popped from QUD when answer is valid."""
        state = InformationState(agent_id="system")

        # Setup question on QUD
        question = WhQuestion(variable="x", predicate="legal_entities")
        state.shared.push_qud(question)
        initial_qud_len = len(state.shared.qud)

        # Provide valid answer
        valid_answer = Answer(content="Acme Corp, Beta Inc", question_ref=question)
        move = DialogueMove(move_type="answer", content=valid_answer, speaker="user")
        state.private.beliefs["_temp_move"] = move

        # Apply integration rules
        rules = create_integration_rules()
        ruleset = RuleSet()
        for rule in rules:
            ruleset.add_rule(rule)

        new_state = ruleset.apply_rules("integration", state)

        # Verify: Question should be popped from QUD
        assert len(new_state.shared.qud) == initial_qud_len - 1

        # Verify: No clarification needed
        assert new_state.private.beliefs.get("_needs_clarification") is not True


class TestPlanProgression:
    """Test plan progression through subgoals."""

    def test_subplan_marked_complete_after_answer(self):
        """Verify subplan is marked complete when its question is answered."""
        state = InformationState(agent_id="system")

        # Create a plan with findout subplans
        q1 = WhQuestion(variable="x", predicate="legal_entities")
        q2 = WhQuestion(variable="y", predicate="date")

        plan = Plan(
            plan_type="nda_drafting",
            content="Draft NDA",
            subplans=[
                Plan(plan_type="findout", content=q1),
                Plan(plan_type="findout", content=q2),
            ],
        )
        state.private.plan.append(plan)
        state.shared.push_qud(q1)

        # Verify initial state - both subplans active
        assert plan.subplans[0].is_active()
        assert plan.subplans[1].is_active()

        # Answer first question
        answer = Answer(content="Acme Corp, Beta Inc", question_ref=q1)
        move = DialogueMove(move_type="answer", content=answer, speaker="user")
        state.private.beliefs["_temp_move"] = move

        # Apply integration rules
        rules = create_integration_rules()
        ruleset = RuleSet()
        for rule in rules:
            ruleset.add_rule(rule)

        new_state = ruleset.apply_rules("integration", state)

        # Verify: First subplan should be completed
        assert new_state.private.plan[0].subplans[0].status == "completed"
        assert new_state.private.plan[0].subplans[1].is_active()

    def test_qud_empty_when_plan_complete(self):
        """Verify QUD is empty when all subplans are completed."""
        state = InformationState(agent_id="system")

        # Create a plan with one findout subplan
        q1 = WhQuestion(variable="x", predicate="legal_entities")

        plan = Plan(
            plan_type="nda_drafting",
            content="Draft NDA",
            subplans=[
                Plan(plan_type="findout", content=q1),
            ],
        )
        state.private.plan.append(plan)
        state.shared.push_qud(q1)

        # Answer the question
        answer = Answer(content="Acme Corp, Beta Inc", question_ref=q1)
        move = DialogueMove(move_type="answer", content=answer, speaker="user")
        state.private.beliefs["_temp_move"] = move

        # Apply integration rules
        rules = create_integration_rules()
        ruleset = RuleSet()
        for rule in rules:
            ruleset.add_rule(rule)

        new_state = ruleset.apply_rules("integration", state)

        # Verify: QUD should be empty (no more questions)
        assert len(new_state.shared.qud) == 0


# NOTE: TestMultiTurnDialogue class removed - tests expected IBiS1 behavior
# (questions pushed directly to QUD during integration). IBiS3 tests in
# test_ibis3_end_to_end.py now verify the correct behavior (questions go to
# private.issues first, then raised to QUD during selection).
