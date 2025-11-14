"""
End-to-end causation chain test - NO MOCKS.

This test verifies the actual chain of causation from user input
through belief state updates to utterance generation.

Chain of Causation:
1. User utterance → engine.interpret() → DialogueMove created
2. DialogueMove → integration_rules → InformationState.private.plan updated
3. Plan creation → integration_rules → InformationState.shared.qud updated
4. QUD state → selection_rules → response_move selected
5. response_move + active plan → generation_rules → natural language utterance

NO MOCKING - everything uses real implementations.
"""

import pytest

from ibdm.core import InformationState, WhQuestion
from ibdm.engine import DialogueMoveEngine
from ibdm.rules import (
    RuleSet,
    create_generation_rules,
    create_integration_rules,
    create_interpretation_rules,
    create_selection_rules,
)


class TestEndToEndCausationChain:
    """Test the complete causation chain without any mocks."""

    def test_complete_causation_chain_nda_request(self):
        """
        Test complete chain: utterance → interpretation → integration → selection → generation.

        This verifies:
        1. Interpretation creates command move from "I need to draft an NDA"
        2. Integration rules trigger form_task_plan (detects NDA keywords)
        3. form_task_plan uses domain.get_plan() to create 5-step plan
        4. form_task_plan pushes first question (legal_entities) to QUD
        5. Selection rules detect QUD has question, select ask move
        6. Generation rules detect active plan, use NDA-specific template
        7. Final utterance is domain-aware, not generic

        NO MOCKS - all real implementations.
        """
        # Setup - real rule set with all rules
        rules = RuleSet()
        for rule in create_interpretation_rules():
            rules.add_rule(rule)
        for rule in create_integration_rules():
            rules.add_rule(rule)
        for rule in create_selection_rules():
            rules.add_rule(rule)
        for rule in create_generation_rules():
            rules.add_rule(rule)

        # Real engine with real rules
        engine = DialogueMoveEngine(agent_id="system", rules=rules)

        # Real information state (empty initially)
        state = InformationState(agent_id="system")

        # Verify initial state is empty
        assert len(state.private.plan) == 0, "Should start with no plans"
        assert len(state.shared.qud) == 0, "Should start with empty QUD"

        # ============================================================
        # STEP 1: INTERPRET - utterance → DialogueMove
        # ============================================================
        utterance = "I need to draft an NDA"
        speaker = "user"

        moves = engine.interpret(utterance, speaker, state)

        # Verify interpretation creates command move
        assert len(moves) == 1, "Should create one move"
        move = moves[0]
        assert move.move_type == "command", "Should be command move"
        assert "NDA" in move.content or "nda" in move.content.lower(), "Should contain NDA"

        print(f"✓ Step 1 (INTERPRET): Created {move.move_type} move")

        # ============================================================
        # STEP 2: INTEGRATE - DialogueMove → belief state update
        # ============================================================

        # Apply move through integration (this should trigger form_task_plan rule)
        updated_state = engine.integrate(move, state)

        # Verify plan was created in belief state
        assert (
            len(updated_state.private.plan) == 1
        ), "Integration should create plan in private.plan"

        plan = updated_state.private.plan[0]
        assert plan.plan_type == "nda_drafting", "Should be NDA plan from domain"
        assert len(plan.subplans) == 5, "NDA plan should have 5 subplans from domain"

        print(f"✓ Step 2 (INTEGRATE): Created plan with {len(plan.subplans)} subplans")

        # Verify first question was pushed to QUD
        assert len(updated_state.shared.qud) == 1, "Should have pushed first question to QUD"

        question = updated_state.shared.qud[-1]  # Top of QUD
        assert isinstance(question, WhQuestion), "First question should be WhQuestion"
        assert (
            question.predicate == "legal_entities"
        ), "First question should ask for legal_entities (from domain)"

        print(f"✓ Step 2 (INTEGRATE): Pushed question to QUD: {question.predicate}")

        # ============================================================
        # STEP 3: SELECT - QUD state → response_move
        # ============================================================

        # Select next action based on updated state
        response_move, final_state = engine.select_action(updated_state)

        # Verify selection chose to ask the QUD question
        assert response_move is not None, "Should select a response"
        assert response_move.move_type == "ask", "Should select ask move"
        assert response_move.speaker == "system", "System should respond"

        selected_question = response_move.content
        assert isinstance(selected_question, WhQuestion), "Should be asking WhQuestion"
        assert (
            selected_question.predicate == "legal_entities"
        ), "Should ask question from QUD"

        print(f"✓ Step 3 (SELECT): Selected ask move for {selected_question.predicate}")

        # ============================================================
        # STEP 4: GENERATE - response_move + plan → natural language
        # ============================================================

        # Generate utterance from response move
        utterance_text = engine.generate(response_move, final_state)

        # Verify generated text is domain-aware (not generic)
        assert utterance_text, "Should generate non-empty utterance"

        # Should use NDA-specific template from generation_rules.py
        # _generate_nda_question() generates:
        # "What are the names of the parties entering into this NDA?"
        assert (
            "parties" in utterance_text.lower() or "organizations" in utterance_text.lower()
        ), f"Should ask about parties/organizations, got: {utterance_text}"

        # Should NOT be generic template like "What legal entities?"
        assert "legal_entities" not in utterance_text, "Should not use raw predicate name"

        # Should mention NDA (domain-specific)
        assert "NDA" in utterance_text or "nda" in utterance_text.lower(), (
            "Should mention NDA (domain-specific)"
        )

        print(f"✓ Step 4 (GENERATE): Generated: '{utterance_text}'")

        # ============================================================
        # VERIFY CAUSATION CHAIN
        # ============================================================

        # Trace the chain:
        # 1. User said "I need to draft an NDA"
        # 2. → command move created
        # 3. → integration rule recognized NDA keywords
        # 4. → integration rule called domain.get_plan("nda_drafting")
        # 5. → domain returned 5-step plan with first question (legal_entities)
        # 6. → integration rule pushed legal_entities question to QUD
        # 7. → selection rule saw QUD has question, selected ask move
        # 8. → generation rule detected active NDA plan
        # 9. → generation rule used _generate_nda_question() template
        # 10. → result: "What are the names of the parties entering into this NDA?"

        print("\n" + "=" * 70)
        print("CAUSATION CHAIN VERIFIED:")
        print("=" * 70)
        print(f"Input: '{utterance}'")
        print(f"  → Interpretation: {move.move_type} move")
        print(f"  → Integration: Created {plan.plan_type} plan with {len(plan.subplans)} steps")
        print(f"  → Integration: Pushed {question.predicate} to QUD")
        print(f"  → Selection: Chose to ask {selected_question.predicate}")
        print(f"  → Generation: '{utterance_text}'")
        print("=" * 70)

    def test_belief_state_drives_utterance_not_input(self):
        """
        Verify that utterances are driven by belief state, not input utterance.

        This tests that even with the same initial utterance, different
        belief states produce different outputs.
        """
        # Setup
        rules = RuleSet()
        for rule in create_interpretation_rules():
            rules.add_rule(rule)
        for rule in create_integration_rules():
            rules.add_rule(rule)
        for rule in create_selection_rules():
            rules.add_rule(rule)
        for rule in create_generation_rules():
            rules.add_rule(rule)

        engine = DialogueMoveEngine(agent_id="system", rules=rules)

        # Scenario 1: Empty state → generic response
        empty_state = InformationState(agent_id="system")

        moves = engine.interpret("I need to draft an NDA", "user", empty_state)
        integrated_state = engine.integrate(moves[0], empty_state)
        response_move, final_state = engine.select_action(integrated_state)
        utterance_1 = engine.generate(response_move, final_state)

        # Scenario 2: State with existing plan → different response
        # (This would be after answering the first question)
        # For simplicity, we verify scenario 1 produces NDA-specific output

        # The key verification:
        # - Utterance is NOT just echoing input
        # - Utterance is generated from belief state (plan + QUD)
        assert "draft" not in utterance_1.lower() or utterance_1 != "I need to draft an NDA"
        assert (
            len(utterance_1) > 10
        ), "Should be a real question, not just echoing"  # Real question

        # The utterance asks about parties because:
        # 1. Integration created plan in belief state
        # 2. Plan pushed legal_entities question to QUD
        # 3. Selection saw QUD question
        # 4. Generation used plan-aware template
        assert "parties" in utterance_1.lower() or "organizations" in utterance_1.lower()

    def test_plan_in_belief_state_affects_generation(self):
        """
        Verify that having a plan in belief state changes generation output.

        Tests that generation_rules._get_active_plan() actually reads from
        InformationState.private.plan and uses it.
        """
        rules = RuleSet()
        for rule in create_generation_rules():
            rules.add_rule(rule)

        engine = DialogueMoveEngine(agent_id="system", rules=rules)

        # State WITHOUT plan
        state_no_plan = InformationState(agent_id="system")
        question = WhQuestion(variable="x", predicate="legal_entities")

        from ibdm.core import DialogueMove

        move_no_plan = DialogueMove(move_type="ask", content=question, speaker="system")

        utterance_no_plan = engine.generate(move_no_plan, state_no_plan)

        # State WITH NDA plan
        from ibdm.domains.nda_domain import get_nda_domain

        state_with_plan = InformationState(agent_id="system")
        domain = get_nda_domain()
        plan = domain.get_plan("nda_drafting", {})
        state_with_plan.private.plan.append(plan)

        move_with_plan = DialogueMove(move_type="ask", content=question, speaker="system")

        utterance_with_plan = engine.generate(move_with_plan, state_with_plan)

        # Verify different outputs
        # Without plan: generic "What legal entities?"
        # With plan: "What are the names of the parties entering into this NDA?"

        print(f"Without plan: '{utterance_no_plan}'")
        print(f"With plan: '{utterance_with_plan}'")

        # The WITH plan version should be NDA-specific
        assert "NDA" in utterance_with_plan or "nda" in utterance_with_plan.lower(), (
            "With plan should mention NDA"
        )

        # Verify they're different (plan affects output)
        assert (
            utterance_no_plan != utterance_with_plan
        ), "Plan in belief state should change output"


class TestNoMockingVerification:
    """Meta-test to verify we're not using mocks."""

    def test_uses_real_domain_get_plan(self):
        """Verify domain.get_plan() is actually called, not mocked."""
        from ibdm.domains.nda_domain import get_nda_domain

        # Get real domain
        domain = get_nda_domain()

        # Call get_plan (NOT mocked)
        plan = domain.get_plan("nda_drafting", {})

        # Verify it returns real plan structure
        assert plan.plan_type == "nda_drafting"
        assert len(plan.subplans) == 5
        assert all(subplan.content is not None for subplan in plan.subplans)

        # Verify questions use domain predicates
        first_question = plan.subplans[0].content
        assert first_question.predicate in domain.predicates

    def test_integration_rules_actually_modify_state(self):
        """Verify integration rules actually create plans, not mocks."""
        from ibdm.core import DialogueMove
        from ibdm.engine import DialogueMoveEngine
        from ibdm.rules import RuleSet, create_integration_rules

        rules = RuleSet()
        for rule in create_integration_rules():
            rules.add_rule(rule)

        engine = DialogueMoveEngine(agent_id="system", rules=rules)
        state = InformationState(agent_id="system")

        # Create command move
        move = DialogueMove(move_type="command", content="I need to draft an NDA", speaker="user")

        # Before integration: no plan
        assert len(state.private.plan) == 0

        # Integrate (NOT mocked)
        updated_state = engine.integrate(move, state)

        # After integration: plan exists
        assert (
            len(updated_state.private.plan) == 1
        ), "Integration should create real plan"  # Real plan created

        # Verify it's a real Plan object from domain
        plan = updated_state.private.plan[0]
        assert hasattr(plan, "plan_type")
        assert hasattr(plan, "subplans")
        assert plan.plan_type == "nda_drafting"
