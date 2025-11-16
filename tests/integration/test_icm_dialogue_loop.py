"""End-to-end tests for ICM integration in the dialogue loop.

Tests that ICM integration and selection rules are properly integrated
into the main dialogue processing loop and that grounding feedback is
handled correctly.

Based on Larsson (2002) Section 3.6 - ICM Update Rules.
"""

import pytest

from ibdm.core import DialogueMove, InformationState
from ibdm.core.grounding import ActionLevel
from ibdm.core.moves import Polarity, create_icm_acceptance_positive
from ibdm.engine import DialogueMoveEngine
from ibdm.rules import (
    RuleSet,
    create_generation_rules,
    create_integration_rules,
    create_selection_rules,
)


@pytest.fixture
def engine_with_icm() -> DialogueMoveEngine:
    """Create a dialogue engine with ICM rules enabled."""
    rules = RuleSet()

    # Add all rule types including ICM rules
    for rule in create_integration_rules():
        rules.add_rule(rule)

    for rule in create_selection_rules():
        rules.add_rule(rule)

    for rule in create_generation_rules():
        rules.add_rule(rule)

    return DialogueMoveEngine(agent_id="system", rules=rules)


class TestICMIntegrationInDialogueLoop:
    """Test ICM integration rules in dialogue loop."""

    def test_icm_perception_positive_integration(self, engine_with_icm):
        """Test that icm:per*pos is integrated and updates grounding status."""
        state = InformationState(agent_id="system")

        # Add a user move to the move history
        user_move = DialogueMove(move_type="answer", content="Paris", speaker="user")
        state.shared.moves.append(user_move)

        # Create icm:per*pos move
        icm_move = DialogueMove(
            move_type="icm",
            content="okay",
            speaker="system",
            feedback_level=ActionLevel.PERCEPTION,
            polarity=Polarity.POSITIVE,
            target_move_index=0,
        )

        # Integrate the ICM move
        new_state = engine_with_icm.integrate(icm_move, state)

        # Verify: ICM move added to move history
        assert len(new_state.shared.moves) == 2
        assert new_state.shared.moves[-1].is_icm()

        # Verify: Target move has grounding status updated
        assert new_state.shared.moves[0].metadata.get("grounding_status") == "perceived"

    def test_icm_acceptance_positive_integration(self, engine_with_icm):
        """Test that icm:acc*pos marks moves as fully grounded."""
        state = InformationState(agent_id="system")

        # Add user move
        user_move = DialogueMove(move_type="answer", content="Paris", speaker="user")
        state.shared.moves.append(user_move)

        # Create icm:acc*pos
        icm_move = create_icm_acceptance_positive(
            speaker="system",
            content="okay",
            target_move_index=0,
        )

        # Integrate
        new_state = engine_with_icm.integrate(icm_move, state)

        # Verify: Grounding status is "grounded"
        assert new_state.shared.moves[0].metadata.get("grounding_status") == "grounded"

    def test_icm_perception_negative_integration(self, engine_with_icm):
        """Test that icm:per*neg marks moves for reutterance."""
        state = InformationState(agent_id="system")

        # Add user move
        user_move = DialogueMove(
            move_type="answer", content="[garbled]", speaker="user", metadata={"confidence": 0.2}
        )
        state.shared.moves.append(user_move)

        # Create icm:per*neg
        icm_move = DialogueMove(
            move_type="icm",
            content="pardon?",
            speaker="system",
            feedback_level=ActionLevel.PERCEPTION,
            polarity=Polarity.NEGATIVE,
            target_move_index=0,
        )

        # Integrate
        new_state = engine_with_icm.integrate(icm_move, state)

        # Verify: Grounding status and flags
        assert new_state.shared.moves[0].metadata.get("grounding_status") == "perception_failed"
        assert new_state.shared.moves[0].metadata.get("needs_reutterance") is True


class TestICMSelectionInDialogueLoop:
    """Test ICM selection rules in dialogue loop."""

    def test_select_perception_check_low_confidence(self, engine_with_icm):
        """Test that low confidence triggers perception check selection."""
        state = InformationState(agent_id="system")
        state.control.next_speaker = "system"

        # Add low confidence user move
        user_move = DialogueMove(
            move_type="answer", content="[unclear]", speaker="user", metadata={"confidence": 0.3}
        )
        state.shared.last_moves = [user_move]

        # Select action
        selected_move, new_state = engine_with_icm.select_action(state)

        # Verify: ICM perception check selected
        assert selected_move is not None
        assert selected_move.is_icm()
        assert selected_move.feedback_level == ActionLevel.PERCEPTION
        assert selected_move.polarity == Polarity.NEGATIVE

    def test_select_understanding_confirmation_medium_confidence(self, engine_with_icm):
        """Test that medium confidence triggers understanding confirmation."""
        state = InformationState(agent_id="system")
        state.control.next_speaker = "system"

        # Add medium confidence user move
        user_move = DialogueMove(
            move_type="answer", content="Paris", speaker="user", metadata={"confidence": 0.6}
        )
        state.shared.last_moves = [user_move]

        # Select action
        selected_move, new_state = engine_with_icm.select_action(state)

        # Verify: Understanding confirmation selected
        assert selected_move is not None
        assert selected_move.is_icm()
        assert selected_move.feedback_level == ActionLevel.UNDERSTANDING
        assert selected_move.polarity == Polarity.INTERROGATIVE

    def test_select_acceptance_high_confidence(self, engine_with_icm):
        """Test that high confidence triggers acceptance feedback."""
        state = InformationState(agent_id="system")
        state.control.next_speaker = "system"

        # Add high confidence user move
        user_move = DialogueMove(
            move_type="answer", content="Paris", speaker="user", metadata={"confidence": 0.9}
        )
        state.shared.last_moves = [user_move]

        # Select action
        selected_move, new_state = engine_with_icm.select_action(state)

        # Verify: Acceptance selected
        assert selected_move is not None
        assert selected_move.is_icm()
        assert selected_move.feedback_level == ActionLevel.ACCEPTANCE
        assert selected_move.polarity == Polarity.POSITIVE


class TestICMEndToEndFlow:
    """Test complete ICM flows through the dialogue loop."""

    def test_pessimistic_grounding_complete_flow(self, engine_with_icm):
        """Test complete pessimistic grounding flow (low confidence)."""
        state = InformationState(agent_id="system")
        state.control.next_speaker = "system"

        # Step 1: User provides low confidence answer
        user_move = DialogueMove(
            move_type="answer", content="[garbled]", speaker="user", metadata={"confidence": 0.2}
        )
        state.shared.last_moves = [user_move]
        state.shared.moves.append(user_move)

        # Step 2: System selects perception check (icm:per*neg)
        selected_move, new_state = engine_with_icm.select_action(state)

        assert selected_move is not None
        assert selected_move.is_icm()
        assert selected_move.feedback_level == ActionLevel.PERCEPTION
        assert selected_move.polarity == Polarity.NEGATIVE

        # Step 3: Integrate the perception check
        selected_move.target_move_index = 0
        final_state = engine_with_icm.integrate(selected_move, new_state)

        # Verify: User move marked as perception_failed
        assert final_state.shared.moves[0].metadata.get("grounding_status") == "perception_failed"
        assert final_state.shared.moves[0].metadata.get("needs_reutterance") is True

    def test_cautious_grounding_complete_flow(self, engine_with_icm):
        """Test complete cautious grounding flow (medium confidence)."""
        state = InformationState(agent_id="system")
        state.control.next_speaker = "system"

        # Step 1: User provides medium confidence answer
        user_move = DialogueMove(
            move_type="answer", content="Paris", speaker="user", metadata={"confidence": 0.6}
        )
        state.shared.last_moves = [user_move]
        state.shared.moves.append(user_move)

        # Step 2: System selects understanding confirmation (icm:und*int)
        selected_move, new_state = engine_with_icm.select_action(state)

        assert selected_move is not None
        assert selected_move.is_icm()
        assert selected_move.feedback_level == ActionLevel.UNDERSTANDING
        assert selected_move.polarity == Polarity.INTERROGATIVE

        # Step 3: User confirms with positive understanding ICM
        confirm_move = DialogueMove(
            move_type="icm",
            content="yes",
            speaker="user",
            feedback_level=ActionLevel.UNDERSTANDING,
            polarity=Polarity.POSITIVE,
            target_move_index=0,
        )

        # Integrate confirmation
        final_state = engine_with_icm.integrate(confirm_move, new_state)

        # Verify: Original move marked as understood
        assert final_state.shared.moves[0].metadata.get("grounding_status") == "understood"

    def test_optimistic_grounding_complete_flow(self, engine_with_icm):
        """Test complete optimistic grounding flow (high confidence)."""
        state = InformationState(agent_id="system")
        state.control.next_speaker = "system"

        # Step 1: User provides high confidence answer
        user_move = DialogueMove(
            move_type="answer", content="Paris", speaker="user", metadata={"confidence": 0.95}
        )
        state.shared.last_moves = [user_move]
        state.shared.moves.append(user_move)

        # Step 2: System selects acceptance (icm:acc*pos)
        selected_move, new_state = engine_with_icm.select_action(state)

        assert selected_move is not None
        assert selected_move.is_icm()
        assert selected_move.feedback_level == ActionLevel.ACCEPTANCE
        assert selected_move.polarity == Polarity.POSITIVE

        # Step 3: Integrate acceptance
        selected_move.target_move_index = 0
        final_state = engine_with_icm.integrate(selected_move, new_state)

        # Verify: User move marked as fully grounded
        assert final_state.shared.moves[0].metadata.get("grounding_status") == "grounded"

    def test_grounding_status_progression(self, engine_with_icm):
        """Test progression through grounding statuses."""
        state = InformationState(agent_id="system")

        # Add user move
        user_move = DialogueMove(move_type="answer", content="Paris", speaker="user")
        state.shared.moves.append(user_move)

        # Perception positive
        per_pos = DialogueMove(
            move_type="icm",
            content="uh-huh",
            speaker="system",
            feedback_level=ActionLevel.PERCEPTION,
            polarity=Polarity.POSITIVE,
            target_move_index=0,
        )
        state = engine_with_icm.integrate(per_pos, state)
        assert state.shared.moves[0].metadata.get("grounding_status") == "perceived"

        # Understanding positive
        und_pos = DialogueMove(
            move_type="icm",
            content="okay",
            speaker="system",
            feedback_level=ActionLevel.UNDERSTANDING,
            polarity=Polarity.POSITIVE,
            target_move_index=0,
        )
        state = engine_with_icm.integrate(und_pos, state)
        assert state.shared.moves[0].metadata.get("grounding_status") == "understood"

        # Acceptance positive
        acc_pos = create_icm_acceptance_positive(
            speaker="system",
            content="great",
            target_move_index=0,
        )
        state = engine_with_icm.integrate(acc_pos, state)
        assert state.shared.moves[0].metadata.get("grounding_status") == "grounded"
