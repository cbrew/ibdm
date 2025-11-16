"""End-to-end integration tests for IBiS3 accommodation rules.

Tests the complete IBiS3 dialogue flow:
1. Rule 4.1 (IssueAccommodation): Task plan questions → private.issues
2. Rule 4.2 (LocalQuestionAccommodation): private.issues → QUD incrementally
3. Volunteer information: User answers unasked questions
4. Natural dialogue: System skips already-answered questions

Based on Larsson (2002) Sections 4.6.1 and 4.6.2.
"""

from ibdm.core import Answer, DialogueMove, InformationState, WhQuestion
from ibdm.rules import RuleSet, create_integration_rules, create_selection_rules


class TestIBiS3RuleChain:
    """Test complete IBiS3 rule chain working together."""

    def test_rule_chain_task_plan_to_issues_to_qud(self):
        """Test Rule 4.1 → Rule 4.2: Plan questions go to issues, then to QUD.

        Flow:
        1. User: "I need to draft an NDA"
        2. INTEGRATION: form_task_plan creates plan with findout subplans
        3. INTEGRATION: Rule 4.1 accommodates findout questions to private.issues
        4. SELECTION: Rule 4.2 raises first issue to QUD
        5. System asks the question
        """
        # Setup rulesets
        integration_ruleset = RuleSet()
        for rule in create_integration_rules():
            integration_ruleset.add_rule(rule)

        selection_ruleset = RuleSet()
        for rule in create_selection_rules():
            selection_ruleset.add_rule(rule)

        state = InformationState(agent_id="system")

        # Turn 1: User requests NDA drafting
        user_move = DialogueMove(
            move_type="command",
            content="I need to draft an NDA",
            speaker="user"
        )

        # Store move in state for rules to process
        state.private.beliefs["_temp_move"] = user_move

        # INTEGRATION phase - apply integration rules
        state = integration_ruleset.apply_rules("integration", state)

        # Verify: Plan created
        assert len(state.private.plan) == 1, "Plan should be created"
        plan = state.private.plan[0]
        assert plan.plan_type == "nda_drafting"
        assert len(plan.subplans) == 5, "NDA plan should have 5 subplans"

        # Verify: Rule 4.1 - Questions accommodated to private.issues (NOT QUD yet)
        # All 5 questions should be in private.issues
        assert len(state.private.issues) == 5, (
            f"Expected 5 issues, got {len(state.private.issues)}"
        )

        # QUD should be EMPTY at this point (before SELECTION phase)
        assert len(state.shared.qud) == 0, (
            "QUD should be empty after integration - questions go to issues first"
        )

        print("\n✅ After INTEGRATION:")
        print(f"  - Plan created: {plan.plan_type}")
        print(f"  - Issues: {len(state.private.issues)} questions")
        print(f"  - QUD: {len(state.shared.qud)} questions")

        # SELECTION phase - apply selection rules
        state = selection_ruleset.apply_rules("selection", state)

        # Verify: Rule 4.2 - First issue raised to QUD
        assert len(state.shared.qud) == 1, (
            "QUD should have one question after selection"
        )
        assert len(state.private.issues) == 4, (
            "Issues should have 4 questions left (one moved to QUD)"
        )

        # Verify: Question on QUD
        question = state.shared.qud[-1]
        assert isinstance(question, WhQuestion)
        assert question.predicate == "legal_entities", (
            "First question should ask for legal entities (parties)"
        )

        # Verify: System should have selected to ask this question (agenda)
        assert len(state.private.agenda) > 0, "Agenda should have a move"
        agenda_move = state.private.agenda[-1]
        assert agenda_move.move_type == "ask"

        print("\n✅ After SELECTION:")
        print(f"  - QUD: {len(state.shared.qud)} question")
        print(f"  - Issues: {len(state.private.issues)} questions remaining")
        print(f"  - Question on QUD: {question.predicate}")

    def test_volunteer_information_handling(self):
        """Test IBiS3: User volunteers answer to unasked question.

        Flow:
        1. Setup: Questions in private.issues
        2. User volunteers answer to unasked question
        3. INTEGRATION: Answer resolves question from issues
        4. Question removed from issues, commitment added
        """
        # Setup rulesets
        integration_ruleset = RuleSet()
        for rule in create_integration_rules():
            integration_ruleset.add_rule(rule)

        state = InformationState(agent_id="system")

        # Turn 1: Create NDA plan
        user_move = DialogueMove(
            move_type="command",
            content="I need to draft an NDA",
            speaker="user"
        )
        state.private.beliefs["_temp_move"] = user_move
        state = integration_ruleset.apply_rules("integration", state)

        # Verify setup: Questions in issues
        assert len(state.private.issues) == 5
        initial_issues_count = len(state.private.issues)

        # Find the date question in issues
        date_question = None
        for issue in state.private.issues:
            if isinstance(issue, WhQuestion) and issue.predicate == "date":
                date_question = issue
                break
        assert date_question is not None, "Date question should be in issues"

        print(f"\n✅ Setup: {initial_issues_count} questions in issues")
        print(f"  - Date question: {date_question}")

        # Turn 2: User volunteers answer for date (unasked question!)
        volunteer_answer = Answer(
            content="January 1, 2025",
            question_ref=date_question
        )
        volunteer_move = DialogueMove(
            move_type="answer",
            content=volunteer_answer,
            speaker="user"
        )
        state.private.beliefs["_temp_move"] = volunteer_move

        # Apply integration rules
        state = integration_ruleset.apply_rules("integration", state)

        # Verify: Date question removed from issues
        assert date_question not in state.private.issues, (
            "Volunteer question should be removed from issues"
        )
        assert len(state.private.issues) == initial_issues_count - 1, (
            "One question should be removed from issues"
        )

        # Verify: Commitment added
        expected_commitment = f"{date_question}: {volunteer_answer.content}"
        assert expected_commitment in state.shared.commitments, (
            "Volunteer answer should be committed"
        )

        print(f"\n✅ After volunteer answer:")
        print(f"  - Issues: {len(state.private.issues)} questions (one removed)")
        print(f"  - Commitment added: {expected_commitment}")
        print(f"  - QUD: {len(state.shared.qud)} (unchanged - not asked yet)")


class TestIBiS3MultiTurnDialogue:
    """Test multi-turn dialogue with IBiS3."""

    def test_nda_dialogue_natural_flow(self):
        """Test natural NDA dialogue with incremental questioning.

        This verifies the "Week 2 achievement" from NEXT-TASK.md:
        - Questions accommodated to private.issues
        - Questions raised to QUD incrementally
        - Natural dialogue flow
        """
        # Setup rulesets
        integration_ruleset = RuleSet()
        for rule in create_integration_rules():
            integration_ruleset.add_rule(rule)

        selection_ruleset = RuleSet()
        for rule in create_selection_rules():
            selection_ruleset.add_rule(rule)

        state = InformationState(agent_id="system")

        print("\n" + "=" * 60)
        print("IBiS3 Multi-Turn Dialogue Test")
        print("=" * 60)

        # Turn 1: User requests NDA
        print("\n📥 Turn 1: User requests NDA")
        user_move = DialogueMove(
            move_type="command",
            content="I need to draft an NDA",
            speaker="user"
        )
        state.private.beliefs["_temp_move"] = user_move

        # Process: INTEGRATION → SELECTION
        state = integration_ruleset.apply_rules("integration", state)
        state = selection_ruleset.apply_rules("selection", state)

        # Verify IBiS3 behavior after turn 1
        assert len(state.private.plan) == 1, "Plan created"
        assert state.private.plan[0].plan_type == "nda_drafting"

        # Rule 4.1 + 4.2 working together
        assert len(state.shared.qud) == 1, "One question on QUD (incremental!)"
        assert len(state.private.issues) == 4, "Remaining questions in issues"

        # System asks first question
        assert len(state.private.agenda) > 0
        ask_move = state.private.agenda[-1]
        assert ask_move.move_type == "ask"

        print(f"  ✅ Plan created: {state.private.plan[0].plan_type}")
        print(f"  ✅ QUD length: {len(state.shared.qud)} (incremental questioning!)")
        print(f"  ✅ Issues length: {len(state.private.issues)}")
        print(f"  ✅ System asks: {state.shared.qud[-1].predicate}")

        # Turn 2: User answers first question
        print("\n📥 Turn 2: User answers parties question")
        qud_q = state.shared.qud[-1]
        answer = Answer(content="Acme Corp and Smith Inc", question_ref=qud_q)
        answer_move = DialogueMove(move_type="answer", content=answer, speaker="user")
        state.private.beliefs["_temp_move"] = answer_move

        # Clear agenda from previous turn
        state.private.agenda = []

        # Process: INTEGRATION → SELECTION
        state = integration_ruleset.apply_rules("integration", state)
        state = selection_ruleset.apply_rules("selection", state)

        # Verify: Question popped, next question raised
        assert len(state.shared.qud) == 1, "Next question on QUD"
        assert len(state.private.issues) == 3, "One issue raised to QUD"
        assert len(state.private.agenda) > 0, "System selected next move"
        assert state.private.agenda[-1].move_type == "ask"

        print(f"  ✅ QUD length: {len(state.shared.qud)} (still incremental!)")
        print(f"  ✅ Issues length: {len(state.private.issues)}")
        print(f"  ✅ System asks: {state.shared.qud[-1].predicate}")
        print(f"  ✅ Commitments: {len(state.shared.commitments)}")

        # Verify: IBiS3 incremental questioning working
        # Questions asked ONE AT A TIME, not all at once
        assert len(state.shared.qud) == 1, "Incremental questioning!"

        print("\n" + "=" * 60)
        print("🎉 IBiS3 working: Incremental questioning achieved!")
        print("=" * 60)
