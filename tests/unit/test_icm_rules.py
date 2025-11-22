"""Unit tests for ICM (Interactive Communication Management) rules.

Tests IBiS2 grounding functionality:
- ICM integration rules (Rules 3.1-3.5)
- ICM selection rules (Rules 3.6-3.8)

Based on Larsson (2002) Section 3.6.
"""

from ibdm.core import DialogueMove, InformationState
from ibdm.core.grounding import ActionLevel
from ibdm.core.moves import (
    Polarity,
    create_icm_acceptance_positive,
    create_icm_perception_negative,
    create_icm_perception_positive,
    create_icm_understanding_interrogative,
    create_icm_understanding_negative,
    create_icm_understanding_positive,
)
from ibdm.rules.icm_integration_rules import create_icm_integration_rules
from ibdm.rules.selection_rules import create_selection_rules


def create_test_state(agent_id: str = "system") -> InformationState:
    """Create a test information state with agent ID."""
    state = InformationState(agent_id=agent_id)
    return state


class TestICMIntegrationRules:
    """Tests for ICM integration rules (Rules 3.1-3.5)."""

    def test_integrate_perception_positive(self):
        """Test Rule 3.1: IntegrateICM_PerceptionPositive."""
        # Create initial state
        state = create_test_state()

        # Add user move to history (will be referenced by ICM)
        user_move = DialogueMove(move_type="answer", content="Paris", speaker="user")
        state.shared.moves.append(user_move)

        # Add perception positive ICM to last_moves
        icm_move = create_icm_perception_positive("I heard 'Paris'", "system", target_move_index=0)
        state.shared.last_moves = [icm_move]
        # Set _temp_move as expected by updated rules
        state.private.beliefs["_temp_move"] = icm_move

        # Apply integration rules
        rules = create_icm_integration_rules()
        perception_rule = next(r for r in rules if r.name == "integrate_icm_perception_positive")

        # Check precondition
        assert perception_rule.applies(state)

        # Apply effect
        new_state = perception_rule.apply(state)

        # Verify ICM move was added to move history
        assert len(new_state.shared.moves) == 2
        assert new_state.shared.moves[-1].is_icm()

        # Verify grounding status was updated on the cloned move
        assert new_state.shared.moves[0].metadata.get("grounding_status") == "perceived"

    def test_integrate_understanding_positive(self):
        """Test Rule 3.2: IntegrateICM_UnderstandingPositive."""
        state = create_test_state()

        # Add user move
        user_move = DialogueMove(move_type="answer", content="Paris", speaker="user")
        state.shared.moves.append(user_move)

        # Add understanding positive ICM
        icm_move = create_icm_understanding_positive("Paris", "system", target_move_index=0)
        state.shared.last_moves = [icm_move]
        state.private.beliefs["_temp_move"] = icm_move

        # Apply rule
        rules = create_icm_integration_rules()
        understanding_rule = next(
            r for r in rules if r.name == "integrate_icm_understanding_positive"
        )

        assert understanding_rule.applies(state)
        new_state = understanding_rule.apply(state)

        # Verify grounding status on cloned move
        assert new_state.shared.moves[0].metadata.get("grounding_status") == "understood"

    def test_integrate_acceptance_positive(self):
        """Test Rule 3.3: IntegrateICM_AcceptancePositive."""
        state = create_test_state()

        # Add user move
        user_move = DialogueMove(move_type="answer", content="Paris", speaker="user")
        state.shared.moves.append(user_move)

        # Add acceptance positive ICM
        icm_move = create_icm_acceptance_positive("Okay", "system", target_move_index=0)
        state.shared.last_moves = [icm_move]
        state.private.beliefs["_temp_move"] = icm_move

        # Apply rule
        rules = create_icm_integration_rules()
        acceptance_rule = next(r for r in rules if r.name == "integrate_icm_acceptance_positive")

        assert acceptance_rule.applies(state)
        new_state = acceptance_rule.apply(state)

        # Verify full grounding on cloned move
        assert new_state.shared.moves[0].metadata.get("grounding_status") == "grounded"

    def test_integrate_perception_negative(self):
        """Test Rule 3.4: IntegrateICM_PerceptionNegative."""
        state = create_test_state()

        # Add user move
        user_move = DialogueMove(move_type="answer", content="[garbled]", speaker="user")
        state.shared.moves.append(user_move)

        # Add perception negative ICM
        icm_move = create_icm_perception_negative("Pardon?", "system", target_move_index=0)
        state.shared.last_moves = [icm_move]
        state.private.beliefs["_temp_move"] = icm_move

        # Apply rule
        rules = create_icm_integration_rules()
        perception_neg_rule = next(
            r for r in rules if r.name == "integrate_icm_perception_negative"
        )

        assert perception_neg_rule.applies(state)
        new_state = perception_neg_rule.apply(state)

        # Verify perception failure marked on cloned move
        assert new_state.shared.moves[0].metadata.get("grounding_status") == "perception_failed"
        assert new_state.shared.moves[0].metadata.get("needs_reutterance") is True

    def test_integrate_understanding_negative(self):
        """Test Rule 3.5: IntegrateICM_UnderstandingNegative."""
        state = create_test_state()

        # Add user move
        user_move = DialogueMove(move_type="answer", content="Unclear", speaker="user")
        state.shared.moves.append(user_move)

        # Add understanding negative ICM
        icm_move = create_icm_understanding_negative(
            "I don't understand", "system", target_move_index=0
        )
        state.shared.last_moves = [icm_move]
        state.private.beliefs["_temp_move"] = icm_move

        # Apply rule
        rules = create_icm_integration_rules()
        understanding_neg_rule = next(
            r for r in rules if r.name == "integrate_icm_understanding_negative"
        )

        assert understanding_neg_rule.applies(state)
        new_state = understanding_neg_rule.apply(state)

        # Verify understanding failure marked on cloned move
        assert new_state.shared.moves[0].metadata.get("grounding_status") == "understanding_failed"
        assert new_state.shared.moves[0].metadata.get("needs_clarification") is True

    def test_track_icm_move_generic(self):
        """Test generic ICM move tracking."""
        state = create_test_state()

        # Add any ICM move (e.g., interrogative)
        icm_move = create_icm_understanding_interrogative("Paris?", "system")
        state.shared.last_moves = [icm_move]
        state.private.beliefs["_temp_move"] = icm_move

        # Apply generic tracking rule
        rules = create_icm_integration_rules()
        track_rule = next(r for r in rules if r.name == "track_icm_move")

        assert track_rule.applies(state)
        new_state = track_rule.apply(state)

        # Verify ICM move was tracked
        assert len(new_state.shared.moves) == 1
        assert new_state.shared.moves[0] == icm_move

    def test_icm_integration_preconditions(self):
        """Test ICM integration rule preconditions."""
        rules = create_icm_integration_rules()

        # Empty state - no rules should apply
        empty_state = create_test_state()
        # Ensure _temp_move is None
        empty_state.private.beliefs.pop("_temp_move", None)

        for rule in rules:
            assert not rule.applies(empty_state), (
                f"Rule {rule.name} should not apply to empty state"
            )

        # Non-ICM move - no ICM rules should apply
        non_icm_state = create_test_state()
        move = DialogueMove(move_type="greet", content="Hello", speaker="user")
        non_icm_state.shared.last_moves = [move]
        non_icm_state.private.beliefs["_temp_move"] = move

        for rule in rules:
            if rule.name != "track_icm_move":  # Generic tracking doesn't apply to non-ICM
                assert not rule.applies(non_icm_state), (
                    f"Rule {rule.name} should not apply to non-ICM move"
                )


class TestICMSelectionRules:
    """Tests for ICM selection rules (Rules 3.6-3.8)."""

    def test_select_perception_check_low_confidence(self):
        """Test Rule 3.6: SelectPerceptionCheck for low confidence."""
        state = create_test_state()

        # Add user move with very low confidence
        user_move = DialogueMove(
            move_type="answer", content="[garbled]", speaker="user", metadata={"confidence": 0.3}
        )
        state.shared.last_moves = [user_move]

        # Get selection rules
        rules = create_selection_rules()
        perception_rule = next(r for r in rules if r.name == "select_perception_check")

        # Check precondition
        assert perception_rule.applies(state)

        # Apply effect
        new_state = perception_rule.apply(state)

        # Verify perception check ICM was added to agenda
        assert len(new_state.private.agenda) == 1
        selected_move = new_state.private.agenda[0]
        assert selected_move.is_icm()
        assert selected_move.feedback_level == ActionLevel.PERCEPTION
        assert selected_move.polarity == Polarity.NEGATIVE

    def test_select_understanding_confirmation_medium_confidence(self):
        """Test Rule 3.7: SelectUnderstandingConfirmation for medium confidence."""
        state = create_test_state()

        # Add user move with medium confidence
        user_move = DialogueMove(
            move_type="answer", content="Paris", speaker="user", metadata={"confidence": 0.6}
        )
        state.shared.last_moves = [user_move]

        # Get selection rules
        rules = create_selection_rules()
        confirmation_rule = next(r for r in rules if r.name == "select_understanding_confirmation")

        # Check precondition
        assert confirmation_rule.applies(state)

        # Apply effect
        new_state = confirmation_rule.apply(state)

        # Verify understanding confirmation ICM was added to agenda
        assert len(new_state.private.agenda) == 1
        selected_move = new_state.private.agenda[0]
        assert selected_move.is_icm()
        assert selected_move.feedback_level == ActionLevel.UNDERSTANDING
        assert selected_move.polarity == Polarity.INTERROGATIVE

    def test_select_understanding_confirmation_requires_confirmation(self):
        """Test Rule 3.7: SelectUnderstandingConfirmation for moves requiring confirmation."""
        state = create_test_state()

        # Add quit move (always requires confirmation)
        user_move = DialogueMove(
            move_type="quit", content="bye", speaker="user", metadata={"confidence": 0.95}
        )
        state.shared.last_moves = [user_move]

        # Get selection rules
        rules = create_selection_rules()
        confirmation_rule = next(r for r in rules if r.name == "select_understanding_confirmation")

        # Check precondition - should apply even with high confidence
        assert confirmation_rule.applies(state)

    def test_select_acceptance_high_confidence(self):
        """Test Rule 3.8: SelectAcceptance for high confidence."""
        state = create_test_state()

        # Add user move with high confidence
        user_move = DialogueMove(
            move_type="answer", content="Paris", speaker="user", metadata={"confidence": 0.9}
        )
        state.shared.last_moves = [user_move]

        # Get selection rules
        rules = create_selection_rules()
        acceptance_rule = next(r for r in rules if r.name == "select_acceptance")

        # Check precondition
        assert acceptance_rule.applies(state)

        # Apply effect
        new_state = acceptance_rule.apply(state)

        # Verify acceptance ICM was added to agenda
        assert len(new_state.private.agenda) == 1
        selected_move = new_state.private.agenda[0]
        assert selected_move.is_icm()
        assert selected_move.feedback_level == ActionLevel.ACCEPTANCE
        assert selected_move.polarity == Polarity.POSITIVE

    def test_selection_rules_dont_apply_with_existing_agenda(self):
        """Test that ICM selection rules don't apply when agenda already has moves."""
        state = create_test_state()

        # Add low confidence user move
        state.shared.last_moves = [
            DialogueMove(
                move_type="answer", content="test", speaker="user", metadata={"confidence": 0.3}
            )
        ]

        # Add existing move to agenda
        state.private.agenda.append(
            DialogueMove(move_type="ask", content="What?", speaker="system")
        )

        # Get selection rules
        rules = create_selection_rules()
        icm_rules = [
            r
            for r in rules
            if r.name.startswith("select_")
            and "icm" in r.name
            or r.name
            in ["select_perception_check", "select_understanding_confirmation", "select_acceptance"]
        ]

        # None of the ICM selection rules should apply
        for rule in icm_rules:
            assert not rule.applies(state), f"Rule {rule.name} should not apply when agenda exists"

    def test_selection_rules_dont_apply_to_system_moves(self):
        """Test that ICM selection rules don't apply to system's own moves."""
        state = create_test_state()

        # Add system move (not user)
        state.shared.last_moves = [
            DialogueMove(
                move_type="ask",
                content="What city?",
                speaker="system",
                metadata={"confidence": 0.3},
            )
        ]

        # Get selection rules
        rules = create_selection_rules()
        perception_rule = next(r for r in rules if r.name == "select_perception_check")
        confirmation_rule = next(r for r in rules if r.name == "select_understanding_confirmation")
        acceptance_rule = next(r for r in rules if r.name == "select_acceptance")

        # None should apply to system's own moves
        assert not perception_rule.applies(state)
        assert not confirmation_rule.applies(state)
        assert not acceptance_rule.applies(state)

    def test_grounding_strategy_integration(self):
        """Test integration between confidence levels and grounding strategies."""
        state = create_test_state()
        rules = create_selection_rules()

        # Very low confidence (< 0.5) → PESSIMISTIC → perception check
        state.shared.last_moves = [
            DialogueMove(
                move_type="answer", content="test", speaker="user", metadata={"confidence": 0.2}
            )
        ]
        perception_rule = next(r for r in rules if r.name == "select_perception_check")
        assert perception_rule.applies(state)

        # Medium confidence (0.5-0.7) → CAUTIOUS → understanding confirmation
        state2 = create_test_state()
        state2.shared.last_moves = [
            DialogueMove(
                move_type="answer", content="test", speaker="user", metadata={"confidence": 0.6}
            )
        ]
        confirmation_rule = next(r for r in rules if r.name == "select_understanding_confirmation")
        assert confirmation_rule.applies(state2)

        # High confidence (>= 0.7) → OPTIMISTIC → acceptance
        state3 = create_test_state()
        state3.shared.last_moves = [
            DialogueMove(
                move_type="answer", content="test", speaker="user", metadata={"confidence": 0.9}
            )
        ]
        acceptance_rule = next(r for r in rules if r.name == "select_acceptance")
        assert acceptance_rule.applies(state3)


class TestICMIntegrationFlow:
    """Integration tests for complete ICM grounding flows."""

    def test_pessimistic_grounding_flow(self):
        """Test complete pessimistic grounding flow (low confidence)."""
        # Step 1: User utterance with low confidence
        state = create_test_state()
        user_move = DialogueMove(
            move_type="answer", content="[garbled]", speaker="user", metadata={"confidence": 0.3}
        )
        state.shared.last_moves = [user_move]

        # Step 2: System selects perception check
        selection_rules = create_selection_rules()
        perception_rule = next(r for r in selection_rules if r.name == "select_perception_check")
        state = perception_rule.apply(state)

        # Verify perception check was selected
        assert len(state.private.agenda) == 1
        icm_move = state.private.agenda[0]
        assert icm_move.get_icm_signature() == "per*neg"

    def test_cautious_grounding_flow(self):
        """Test complete cautious grounding flow (medium confidence)."""
        # Step 1: User utterance with medium confidence
        state = create_test_state()
        user_move = DialogueMove(
            move_type="answer", content="Paris", speaker="user", metadata={"confidence": 0.6}
        )
        state.shared.last_moves = [user_move]

        # Step 2: System selects understanding confirmation
        selection_rules = create_selection_rules()
        confirmation_rule = next(
            r for r in selection_rules if r.name == "select_understanding_confirmation"
        )
        state = confirmation_rule.apply(state)

        # Verify understanding confirmation was selected
        assert len(state.private.agenda) == 1
        icm_move = state.private.agenda[0]
        assert icm_move.get_icm_signature() == "und*int"

    def test_optimistic_grounding_flow(self):
        """Test complete optimistic grounding flow (high confidence)."""
        # Step 1: User utterance with high confidence
        state = create_test_state()
        user_move = DialogueMove(
            move_type="answer", content="Paris", speaker="user", metadata={"confidence": 0.9}
        )
        state.shared.last_moves = [user_move]

        # Step 2: System selects acceptance
        selection_rules = create_selection_rules()
        acceptance_rule = next(r for r in selection_rules if r.name == "select_acceptance")
        state = acceptance_rule.apply(state)

        # Verify acceptance was selected
        assert len(state.private.agenda) == 1
        icm_move = state.private.agenda[0]
        assert icm_move.get_icm_signature() == "acc*pos"

    def test_grounding_status_progression(self):
        """Test progression of grounding statuses through ICM feedback."""
        state = create_test_state()
        integration_rules = create_icm_integration_rules()

        # Initial user move
        user_move = DialogueMove(move_type="answer", content="Paris", speaker="user")
        state.shared.moves.append(user_move)

        # Step 1: Perception positive → perceived
        icm_per = create_icm_perception_positive("I heard 'Paris'", "system", target_move_index=0)
        state.shared.last_moves = [icm_per]
        state.private.beliefs["_temp_move"] = icm_per

        per_rule = next(
            r for r in integration_rules if r.name == "integrate_icm_perception_positive"
        )
        state = per_rule.apply(state)
        assert state.shared.moves[0].metadata.get("grounding_status") == "perceived"

        # Step 2: Understanding positive → understood
        icm_und = create_icm_understanding_positive("Paris", "system", target_move_index=0)
        state.shared.last_moves = [icm_und]
        state.private.beliefs["_temp_move"] = icm_und

        und_rule = next(
            r for r in integration_rules if r.name == "integrate_icm_understanding_positive"
        )
        state = und_rule.apply(state)
        assert state.shared.moves[0].metadata.get("grounding_status") == "understood"

        # Step 3: Acceptance positive → grounded
        icm_acc = create_icm_acceptance_positive("Okay", "system", target_move_index=0)
        state.shared.last_moves = [icm_acc]
        state.private.beliefs["_temp_move"] = icm_acc

        acc_rule = next(
            r for r in integration_rules if r.name == "integrate_icm_acceptance_positive"
        )
        state = acc_rule.apply(state)
        assert state.shared.moves[0].metadata.get("grounding_status") == "grounded"


class TestICMRulePriorities:
    """Tests for ICM rule priorities and ordering."""

    def test_icm_integration_rules_priority(self):
        """Test that ICM integration rules have appropriate priorities."""
        rules = create_icm_integration_rules()

        # All specific ICM handlers should have higher priority than generic tracking
        specific_rules = [r for r in rules if r.name != "track_icm_move"]
        generic_rule = next(r for r in rules if r.name == "track_icm_move")

        for rule in specific_rules:
            assert rule.priority > generic_rule.priority, (
                f"{rule.name} should have higher priority than tracking"
            )

    def test_icm_selection_rules_priority(self):
        """Test that ICM selection rules have appropriate priorities."""
        rules = create_selection_rules()

        perception_rule = next(r for r in rules if r.name == "select_perception_check")
        confirmation_rule = next(r for r in rules if r.name == "select_understanding_confirmation")
        acceptance_rule = next(r for r in rules if r.name == "select_acceptance")

        # Perception check should have highest priority (most critical)
        assert perception_rule.priority > confirmation_rule.priority
        assert perception_rule.priority > acceptance_rule.priority

        # Confirmation should have higher priority than acceptance
        assert confirmation_rule.priority > acceptance_rule.priority
