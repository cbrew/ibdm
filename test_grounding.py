#!/usr/bin/env python3
"""Test script to verify grounding strategies work correctly."""

from ibdm.core import DialogueMove, InformationState
from ibdm.core.grounding import select_grounding_strategy, GroundingStrategy
from ibdm.engine.dialogue_engine import DialogueMoveEngine
from ibdm.rules import RuleSet, create_integration_rules, create_selection_rules

def test_grounding_strategies():
    """Test that grounding selection rules fire based on confidence."""

    # Create engine with rules
    rules = RuleSet()
    for rule in create_integration_rules():
        rules.add_rule(rule)
    for rule in create_selection_rules():
        rules.add_rule(rule)

    engine = DialogueMoveEngine(agent_id="system", rules=rules)
    state = InformationState(agent_id="system")

    print("=" * 80)
    print("GROUNDING STRATEGY TESTS")
    print("=" * 80)

    # Test 1: Low confidence (0.4) should trigger PESSIMISTIC grounding
    print("\n### Test 1: Low Confidence (0.4) - Should trigger perception check ###")
    user_move_low = DialogueMove(
        move_type="request",
        content="NDA",
        speaker="user",
        metadata={"confidence": 0.4}
    )

    # Check what strategy is selected
    strategy = select_grounding_strategy("request", 0.4)
    print(f"Strategy selected: {strategy}")
    print(f"Expected: {GroundingStrategy.PESSIMISTIC}")

    # Integrate and select
    state = engine.integrate(user_move_low, state)
    system_move, state = engine.select_action(state)

    if system_move:
        print(f"System move type: {system_move.move_type}")
        print(f"System move content: {system_move.content}")
        print(f"Is ICM: {system_move.is_icm()}")
        if system_move.is_icm():
            print(f"Feedback level: {system_move.feedback_level}")
            print(f"Polarity: {system_move.polarity}")
    else:
        print("❌ NO SYSTEM MOVE GENERATED!")

    # Test 2: High confidence (0.9) should trigger OPTIMISTIC grounding
    print("\n### Test 2: High Confidence (0.9) - Should trigger acceptance ###")
    state2 = InformationState(agent_id="system")
    user_move_high = DialogueMove(
        move_type="request",
        content="I need to draft an NDA",
        speaker="user",
        metadata={"confidence": 0.9}
    )

    strategy2 = select_grounding_strategy("request", 0.9)
    print(f"Strategy selected: {strategy2}")
    print(f"Expected: {GroundingStrategy.OPTIMISTIC}")

    state2 = engine.integrate(user_move_high, state2)
    system_move2, state2 = engine.select_action(state2)

    if system_move2:
        print(f"System move type: {system_move2.move_type}")
        print(f"Is ICM: {system_move2.is_icm()}")
        if system_move2.is_icm():
            print(f"Feedback level: {system_move2.feedback_level}")
            print(f"Polarity: {system_move2.polarity}")
    else:
        print("❌ NO SYSTEM MOVE GENERATED!")

    # Test 3: Medium confidence (0.6) should trigger CAUTIOUS grounding
    print("\n### Test 3: Medium Confidence (0.6) - Should trigger understanding confirmation ###")
    state3 = InformationState(agent_id="system")
    user_move_med = DialogueMove(
        move_type="request",
        content="Need NDA draft",
        speaker="user",
        metadata={"confidence": 0.6}
    )

    strategy3 = select_grounding_strategy("request", 0.6)
    print(f"Strategy selected: {strategy3}")
    print(f"Expected: {GroundingStrategy.CAUTIOUS}")

    state3 = engine.integrate(user_move_med, state3)
    system_move3, state3 = engine.select_action(state3)

    if system_move3:
        print(f"System move type: {system_move3.move_type}")
        print(f"Is ICM: {system_move3.is_icm()}")
        if system_move3.is_icm():
            print(f"Feedback level: {system_move3.feedback_level}")
            print(f"Polarity: {system_move3.polarity}")
    else:
        print("❌ NO SYSTEM MOVE GENERATED!")

    print("\n" + "=" * 80)
    print("TESTS COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    test_grounding_strategies()
