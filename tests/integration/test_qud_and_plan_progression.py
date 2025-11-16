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
    create_selection_rules,
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

    def test_next_question_pushed_to_qud_after_answer(self):
        """Verify next question from plan is pushed to QUD after answering current question."""
        state = InformationState(agent_id="system")

        # Create a plan with two findout subplans
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

        # Verify: Second question should now be on QUD
        assert len(new_state.shared.qud) == 1
        assert new_state.shared.top_qud() == q2

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


class TestMultiTurnDialogue:
    """Test complete multi-turn dialogue scenarios."""

    def test_three_turn_dialogue_with_plan_progression(self):
        """Verify complete 3-turn dialogue with plan progression."""
        state = InformationState(agent_id="system")

        # Create a plan with three findout subplans
        q1 = WhQuestion(variable="x", predicate="legal_entities")
        q2 = WhQuestion(variable="y", predicate="date")
        q3 = WhQuestion(variable="z", predicate="time_period")

        plan = Plan(
            plan_type="nda_drafting",
            content="Draft NDA",
            subplans=[
                Plan(plan_type="findout", content=q1),
                Plan(plan_type="findout", content=q2),
                Plan(plan_type="findout", content=q3),
            ],
        )
        state.private.plan.append(plan)
        state.shared.push_qud(q1)

        integration_rules = create_integration_rules()
        ruleset = RuleSet()
        for rule in integration_rules:
            ruleset.add_rule(rule)

        # Turn 1: Answer first question
        answer1 = Answer(content="Acme Corp, Beta Inc", question_ref=q1)
        move1 = DialogueMove(move_type="answer", content=answer1, speaker="user")
        state.private.beliefs["_temp_move"] = move1
        state = ruleset.apply_rules("integration", state)

        # Verify turn 1 results
        assert state.private.plan[0].subplans[0].status == "completed"
        assert state.shared.top_qud() == q2

        # Turn 2: Answer second question
        answer2 = Answer(content="2024-01-15", question_ref=q2)
        move2 = DialogueMove(move_type="answer", content=answer2, speaker="user")
        state.private.beliefs["_temp_move"] = move2
        state = ruleset.apply_rules("integration", state)

        # Verify turn 2 results
        assert state.private.plan[0].subplans[1].status == "completed"
        assert state.shared.top_qud() == q3

        # Turn 3: Answer third question
        answer3 = Answer(content="2 years", question_ref=q3)
        move3 = DialogueMove(move_type="answer", content=answer3, speaker="user")
        state.private.beliefs["_temp_move"] = move3
        state = ruleset.apply_rules("integration", state)

        # Verify turn 3 results - all subplans complete
        assert state.private.plan[0].subplans[2].status == "completed"
        assert len(state.shared.qud) == 0

        # Verify all commitments were added
        assert len(state.shared.commitments) == 3

    def test_dialogue_with_one_invalid_answer(self):
        """Verify dialogue handles invalid answer then continues."""
        state = InformationState(agent_id="system")

        # Create a plan with two questions
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

        integration_rules = create_integration_rules()
        selection_rules = create_selection_rules()
        ruleset_int = RuleSet()
        ruleset_sel = RuleSet()
        for rule in integration_rules:
            ruleset_int.add_rule(rule)
        for rule in selection_rules:
            ruleset_sel.add_rule(rule)

        # Turn 1: Invalid answer (empty)
        invalid_answer = Answer(content="", question_ref=q1)
        move1 = DialogueMove(move_type="answer", content=invalid_answer, speaker="user")
        state.private.beliefs["_temp_move"] = move1
        state = ruleset_int.apply_rules("integration", state)

        # Verify: Question still on QUD, clarification needed
        assert state.shared.top_qud() == q1
        assert state.private.beliefs.get("_needs_clarification") is True

        # Selection phase should create clarification move
        state = ruleset_sel.apply_rules("selection", state)
        icm_moves = [m for m in state.private.agenda if m.move_type == "icm"]
        assert len(icm_moves) == 1

        # Clear agenda for next turn
        state.private.agenda = []

        # Turn 2: Valid answer (retry)
        valid_answer = Answer(content="Acme Corp, Beta Inc", question_ref=q1)
        move2 = DialogueMove(move_type="answer", content=valid_answer, speaker="user")
        state.private.beliefs["_temp_move"] = move2
        state = ruleset_int.apply_rules("integration", state)

        # Verify: Question popped, second question now on QUD
        assert state.shared.top_qud() == q2
        assert state.private.plan[0].subplans[0].status == "completed"
