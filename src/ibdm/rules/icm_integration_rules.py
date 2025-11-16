"""ICM Integration rules for Issue-Based Dialogue Management.

ICM (Interactive Communication Management) integration rules handle grounding
feedback moves. They update the information state based on perception,
understanding, and acceptance feedback.

Based on Larsson (2002) Section 3.6 - ICM Update Rules.
"""

from ibdm.core import InformationState
from ibdm.core.grounding import ActionLevel
from ibdm.core.moves import Polarity
from ibdm.rules.update_rules import UpdateRule


def create_icm_integration_rules() -> list[UpdateRule]:
    """Create ICM integration rules for IBiS2 grounding.

    Implements Rules 3.1-3.5 from Larsson (2002) Section 3.6:
    - Rule 3.1: IntegrateICM_PerceptionPositive (icm:per*pos)
    - Rule 3.2: IntegrateICM_UnderstandingPositive (icm:und*pos)
    - Rule 3.3: IntegrateICM_AcceptancePositive (icm:acc*pos)
    - Rule 3.4: IntegrateICM_PerceptionNegative (icm:per*neg)
    - Rule 3.5: IntegrateICM_UnderstandingNegative (icm:und*neg)

    Returns:
        List of ICM integration rules
    """
    return [
        # Rule 3.1: IntegrateICM_PerceptionPositive
        # Pre: last move is icm:per*pos
        # Effect: Mark target move as perceived (update grounding status)
        UpdateRule(
            name="integrate_icm_perception_positive",
            preconditions=_is_perception_positive_icm,
            effects=_integrate_perception_positive,
            priority=15,  # Before general ICM processing
            rule_type="integration",
        ),
        # Rule 3.2: IntegrateICM_UnderstandingPositive
        # Pre: last move is icm:und*pos
        # Effect: Mark target move as understood
        UpdateRule(
            name="integrate_icm_understanding_positive",
            preconditions=_is_understanding_positive_icm,
            effects=_integrate_understanding_positive,
            priority=15,
            rule_type="integration",
        ),
        # Rule 3.3: IntegrateICM_AcceptancePositive
        # Pre: last move is icm:acc*pos
        # Effect: Add content to commitments (full grounding)
        UpdateRule(
            name="integrate_icm_acceptance_positive",
            preconditions=_is_acceptance_positive_icm,
            effects=_integrate_acceptance_positive,
            priority=15,
            rule_type="integration",
        ),
        # Rule 3.4: IntegrateICM_PerceptionNegative
        # Pre: last move is icm:per*neg
        # Effect: Mark for re-utterance (perception failure)
        UpdateRule(
            name="integrate_icm_perception_negative",
            preconditions=_is_perception_negative_icm,
            effects=_integrate_perception_negative,
            priority=15,
            rule_type="integration",
        ),
        # Rule 3.5: IntegrateICM_UnderstandingNegative
        # Pre: last move is icm:und*neg
        # Effect: Mark for clarification (understanding failure)
        UpdateRule(
            name="integrate_icm_understanding_negative",
            preconditions=_is_understanding_negative_icm,
            effects=_integrate_understanding_negative,
            priority=15,
            rule_type="integration",
        ),
        # Generic ICM move tracking
        # Ensures all ICM moves are added to move history
        UpdateRule(
            name="track_icm_move",
            preconditions=_is_any_icm_move,
            effects=_track_icm_move,
            priority=5,  # Lower priority, runs after specific ICM handlers
            rule_type="integration",
        ),
    ]


# Precondition functions


def _is_perception_positive_icm(state: InformationState) -> bool:
    """Check if last move is icm:per*pos.

    Args:
        state: Current information state

    Returns:
        True if last move is positive perception ICM
    """
    if not state.shared.last_moves:
        return False

    last_move = state.shared.last_moves[-1]
    if not last_move.is_icm():
        return False

    return (
        last_move.feedback_level == ActionLevel.PERCEPTION
        and last_move.polarity == Polarity.POSITIVE
    )


def _is_understanding_positive_icm(state: InformationState) -> bool:
    """Check if last move is icm:und*pos.

    Args:
        state: Current information state

    Returns:
        True if last move is positive understanding ICM
    """
    if not state.shared.last_moves:
        return False

    last_move = state.shared.last_moves[-1]
    if not last_move.is_icm():
        return False

    return (
        last_move.feedback_level == ActionLevel.UNDERSTANDING
        and last_move.polarity == Polarity.POSITIVE
    )


def _is_acceptance_positive_icm(state: InformationState) -> bool:
    """Check if last move is icm:acc*pos.

    Args:
        state: Current information state

    Returns:
        True if last move is positive acceptance ICM
    """
    if not state.shared.last_moves:
        return False

    last_move = state.shared.last_moves[-1]
    if not last_move.is_icm():
        return False

    return (
        last_move.feedback_level == ActionLevel.ACCEPTANCE
        and last_move.polarity == Polarity.POSITIVE
    )


def _is_perception_negative_icm(state: InformationState) -> bool:
    """Check if last move is icm:per*neg.

    Args:
        state: Current information state

    Returns:
        True if last move is negative perception ICM
    """
    if not state.shared.last_moves:
        return False

    last_move = state.shared.last_moves[-1]
    if not last_move.is_icm():
        return False

    return (
        last_move.feedback_level == ActionLevel.PERCEPTION
        and last_move.polarity == Polarity.NEGATIVE
    )


def _is_understanding_negative_icm(state: InformationState) -> bool:
    """Check if last move is icm:und*neg.

    Args:
        state: Current information state

    Returns:
        True if last move is negative understanding ICM
    """
    if not state.shared.last_moves:
        return False

    last_move = state.shared.last_moves[-1]
    if not last_move.is_icm():
        return False

    return (
        last_move.feedback_level == ActionLevel.UNDERSTANDING
        and last_move.polarity == Polarity.NEGATIVE
    )


def _is_any_icm_move(state: InformationState) -> bool:
    """Check if last move is any ICM move.

    Args:
        state: Current information state

    Returns:
        True if last move is an ICM move
    """
    if not state.shared.last_moves:
        return False

    return state.shared.last_moves[-1].is_icm()


# Effect functions


def _integrate_perception_positive(state: InformationState) -> InformationState:
    """Integrate positive perception feedback (icm:per*pos).

    Marks the target utterance as perceived. This is the first level of grounding.

    Based on Larsson (2002) Section 3.6, Rule 3.1.

    Args:
        state: Current information state

    Returns:
        Updated information state with perception marked
    """
    new_state = state.clone()
    last_move = new_state.shared.last_moves[-1]

    # Add ICM move to move history
    new_state.shared.moves.append(last_move)

    # Update grounding status in metadata if target_move_index is specified
    if last_move.target_move_index is not None and last_move.target_move_index < len(
        new_state.shared.moves
    ):
        target_move = new_state.shared.moves[last_move.target_move_index]
        if "grounding_status" not in target_move.metadata:
            target_move.metadata["grounding_status"] = "perceived"

    return new_state


def _integrate_understanding_positive(state: InformationState) -> InformationState:
    """Integrate positive understanding feedback (icm:und*pos).

    Marks the target utterance as understood. This is the second level of grounding.

    Based on Larsson (2002) Section 3.6, Rule 3.2.

    Args:
        state: Current information state

    Returns:
        Updated information state with understanding marked
    """
    new_state = state.clone()
    last_move = new_state.shared.last_moves[-1]

    # Add ICM move to move history
    new_state.shared.moves.append(last_move)

    # Update grounding status in metadata
    if last_move.target_move_index is not None and last_move.target_move_index < len(
        new_state.shared.moves
    ):
        target_move = new_state.shared.moves[last_move.target_move_index]
        target_move.metadata["grounding_status"] = "understood"

    return new_state


def _integrate_acceptance_positive(state: InformationState) -> InformationState:
    """Integrate positive acceptance feedback (icm:acc*pos).

    Marks the target utterance as fully grounded and accepted. This is the
    final level of grounding.

    Based on Larsson (2002) Section 3.6, Rule 3.3.

    Args:
        state: Current information state

    Returns:
        Updated information state with acceptance marked
    """
    new_state = state.clone()
    last_move = new_state.shared.last_moves[-1]

    # Add ICM move to move history
    new_state.shared.moves.append(last_move)

    # Update grounding status to fully grounded
    if last_move.target_move_index is not None and last_move.target_move_index < len(
        new_state.shared.moves
    ):
        target_move = new_state.shared.moves[last_move.target_move_index]
        target_move.metadata["grounding_status"] = "grounded"

    # Mark content as accepted (could add to commitments if content is a proposition)
    if isinstance(last_move.content, str) and last_move.content.lower() in [
        "okay",
        "ok",
        "yes",
        "sure",
        "alright",
    ]:
        # Generic acceptance - full grounding achieved
        pass

    return new_state


def _integrate_perception_negative(state: InformationState) -> InformationState:
    """Integrate negative perception feedback (icm:per*neg).

    Indicates perception failure. The system should prepare to re-utter or
    request clarification.

    Based on Larsson (2002) Section 3.6, Rule 3.4.

    Args:
        state: Current information state

    Returns:
        Updated information state with perception failure marked
    """
    new_state = state.clone()
    last_move = new_state.shared.last_moves[-1]

    # Add ICM move to move history
    new_state.shared.moves.append(last_move)

    # Mark target move as not perceived
    if last_move.target_move_index is not None and last_move.target_move_index < len(
        new_state.shared.moves
    ):
        target_move = new_state.shared.moves[last_move.target_move_index]
        target_move.metadata["grounding_status"] = "perception_failed"
        target_move.metadata["needs_reutterance"] = True

    return new_state


def _integrate_understanding_negative(state: InformationState) -> InformationState:
    """Integrate negative understanding feedback (icm:und*neg).

    Indicates understanding failure. The system should prepare clarification.

    Based on Larsson (2002) Section 3.6, Rule 3.5.

    Args:
        state: Current information state

    Returns:
        Updated information state with understanding failure marked
    """
    new_state = state.clone()
    last_move = new_state.shared.last_moves[-1]

    # Add ICM move to move history
    new_state.shared.moves.append(last_move)

    # Mark target move as not understood
    if last_move.target_move_index is not None and last_move.target_move_index < len(
        new_state.shared.moves
    ):
        target_move = new_state.shared.moves[last_move.target_move_index]
        target_move.metadata["grounding_status"] = "understanding_failed"
        target_move.metadata["needs_clarification"] = True

    return new_state


def _track_icm_move(state: InformationState) -> InformationState:
    """Track any ICM move in move history.

    This is a catch-all for ICM moves that aren't handled by specific rules.
    Ensures all ICM feedback is recorded in the move history.

    Args:
        state: Current information state

    Returns:
        Updated information state with ICM move tracked
    """
    new_state = state.clone()
    last_move = new_state.shared.last_moves[-1]

    # Add to move history if not already added by specific handler
    if not new_state.shared.moves or new_state.shared.moves[-1] != last_move:
        new_state.shared.moves.append(last_move)

    return new_state
