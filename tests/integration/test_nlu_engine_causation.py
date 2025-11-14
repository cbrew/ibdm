"""
Test causation chain with NLU engine (uses LLMs).

This demonstrates the REAL chain when using NLUDialogueEngine.

The difference:
- DialogueMoveEngine: Pattern-based interpretation → creates assert moves
- NLUDialogueEngine: LLM-based interpretation → creates proper move types
"""

import os

import pytest

from ibdm.core import InformationState
from ibdm.engine import NLUDialogueEngine, NLUEngineConfig
from ibdm.nlu import ModelType
from ibdm.rules import (
    RuleSet,
    create_generation_rules,
    create_integration_rules,
    create_interpretation_rules,
    create_selection_rules,
)


@pytest.mark.skipif(
    not os.getenv("IBDM_API_KEY"),
    reason="Requires IBDM_API_KEY for LLM-based NLU",
)
class TestNLUEngineCausationChain:
    """Test causation chain with NLU engine (requires API key)."""

    def test_nlu_engine_complete_causation_chain(self):
        """
        Test complete chain with NLUDialogueEngine.

        Unlike DialogueMoveEngine (pattern-based), NLUDialogueEngine uses
        LLMs to properly classify "I need to draft an NDA" as a command/request.

        This test requires IBDM_API_KEY to be set.
        """
        # Setup with NLU engine
        rules = RuleSet()
        for rule in create_interpretation_rules():
            rules.add_rule(rule)
        for rule in create_integration_rules():
            rules.add_rule(rule)
        for rule in create_selection_rules():
            rules.add_rule(rule)
        for rule in create_generation_rules():
            rules.add_rule(rule)

        config = NLUEngineConfig(
            llm_model=ModelType.HAIKU,  # Use Haiku for faster/cheaper classification
            temperature=0.3,
            max_tokens=500,
        )

        engine = NLUDialogueEngine(agent_id="system", rules=rules, config=config)
        state = InformationState(agent_id="system")

        print("\n" + "=" * 70)
        print("TESTING WITH NLU ENGINE (LLM-BASED)")
        print("=" * 70)

        # STEP 1: INTERPRET with LLM
        utterance = "I need to draft an NDA"
        moves = engine.interpret(utterance, "user", state)

        assert len(moves) >= 1, "Should create at least one move"
        move = moves[0]

        print(f"✓ Interpreted move type: {move.move_type}")
        print(f"✓ Interpreted move content: {move.content}")

        # With NLU, should create command or request move (not assert)
        assert move.move_type in [
            "command",
            "request",
        ], f"NLU should create command/request, got: {move.move_type}"

        # STEP 2: INTEGRATE (should trigger form_task_plan)
        integrated_state = engine.integrate(move, state)

        print(f"✓ Plans created: {len(integrated_state.private.plan)}")
        print(f"✓ QUD size: {len(integrated_state.shared.qud)}")

        # NOW it should create plan because move type is correct
        assert len(integrated_state.private.plan) >= 1, "Should create plan"

        plan = integrated_state.private.plan[0]
        assert plan.plan_type == "nda_drafting"

        # Should push question to QUD
        assert len(integrated_state.shared.qud) >= 1, "Should push question to QUD"

        question = integrated_state.shared.qud[-1]
        print(f"✓ QUD top question: {question.predicate if hasattr(question, 'predicate') else question}")

        # STEP 3: SELECT (should choose to ask question)
        response_move, final_state = engine.select_action(integrated_state)

        assert response_move is not None, "Should select response"
        assert response_move.move_type == "ask", "Should ask question"

        print(f"✓ Selected move type: {response_move.move_type}")

        # STEP 4: GENERATE (should use NDA template)
        utterance_text = engine.generate(response_move, final_state)

        print(f"✓ Generated: '{utterance_text}'")

        # Should NOT be generic "How can I help you?"
        assert utterance_text.lower() != "how can I help you?".lower()

        # Should ask about NDA-specific things
        assert (
            "parties" in utterance_text.lower()
            or "organizations" in utterance_text.lower()
            or "NDA" in utterance_text
            or "nda" in utterance_text.lower()
        ), f"Should be NDA-specific, got: {utterance_text}"

        print("=" * 70)
        print("CAUSATION CHAIN VERIFIED WITH NLU ENGINE")
        print("=" * 70)


class TestCausationChainComparison:
    """Compare pattern-based vs LLM-based interpretation."""

    def test_pattern_engine_fails_on_nda_request(self):
        """
        Document that DialogueMoveEngine (pattern-based) fails to recognize NDA requests.

        This is EXPECTED behavior - pattern-based interpretation doesn't
        understand "I need to draft an NDA" as a command.
        """
        from ibdm.engine import DialogueMoveEngine

        rules = RuleSet()
        for rule in create_interpretation_rules():
            rules.add_rule(rule)
        for rule in create_integration_rules():
            rules.add_rule(rule)

        engine = DialogueMoveEngine(agent_id="system", rules=rules)
        state = InformationState(agent_id="system")

        # Interpret with pattern rules
        moves = engine.interpret("I need to draft an NDA", "user", state)
        move = moves[0]

        # Pattern-based creates assert move (fallback)
        assert move.move_type == "assert", "Pattern-based creates assert (fallback)"

        # Integrate - no plan created because move type is wrong
        integrated = engine.integrate(move, state)

        # No plan because form_task_plan precondition checks for command/request
        assert (
            len(integrated.private.plan) == 0
        ), "Pattern-based doesn't trigger plan formation"

        assert len(integrated.shared.qud) == 0, "No question pushed to QUD"

        print("\n" + "=" * 70)
        print("PATTERN-BASED ENGINE (DialogueMoveEngine):")
        print("=" * 70)
        print(f"Move type: {move.move_type} (assert = fallback)")
        print(f"Plans created: {len(integrated.private.plan)} (none)")
        print(f"QUD size: {len(integrated.shared.qud)} (none)")
        print("\nConclusion: Pattern-based interpretation doesn't recognize NDA requests.")
        print("Need NLU engine with LLM for proper classification.")
        print("=" * 70)
