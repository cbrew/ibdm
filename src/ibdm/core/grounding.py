"""Grounding status tracking for Issue-Based Dialogue Management.

This module implements grounding mechanisms for IBiS2, based on
Larsson (2002) Section 3.5 and Section 3.6.

Grounding is the process by which dialogue participants establish
mutual belief that an utterance has been perceived, understood, and
accepted into the common ground (shared commitments).
"""

from dataclasses import dataclass
from enum import Enum


class GroundingStatus(Enum):
    """Status of grounding for a dialogue move.

    Based on Larsson (2002) Section 3.6.4.
    """

    UNGROUNDED = "ungrounded"
    """Move has not been grounded yet"""

    PENDING = "pending"
    """Move is awaiting grounding evidence"""

    GROUNDED = "grounded"
    """Move has been grounded (added to common ground)"""


class GroundingStrategy(Enum):
    """Grounding update strategy.

    Based on Larsson (2002) Section 3.5.

    - Optimistic: Update DGB immediately, no backtracking
    - Cautious: Update DGB immediately, backtracking available
    - Pessimistic: Update DGB only after positive evidence acquired
    """

    OPTIMISTIC = "optimistic"
    """DGB updated immediately after utterance produced; no backtracking"""

    CAUTIOUS = "cautious"
    """DGB updated immediately after utterance produced; backtracking available"""

    PESSIMISTIC = "pessimistic"
    """DGB updated when positive evidence of grounding acquired"""


class ActionLevel(Enum):
    """ICM action levels for feedback.

    Based on Larsson (2002) Section 3.6.5.
    """

    CONTACT = "con"
    """Contact level: 'Are you there?'"""

    PERCEPTION = "per"
    """Perception level: 'I heard you say X'"""

    SEMANTIC = "sem"
    """Semantic understanding: 'I don't understand'"""

    UNDERSTANDING = "und"
    """Pragmatic understanding: 'You want to know about X'"""

    ACCEPTANCE = "acc"
    """Acceptance/reaction: 'Okay', 'Sorry, I can't do that'"""


@dataclass
class EvidenceRequirement:
    """Evidence requirements for grounding a move type.

    Different move types require different levels of evidence
    before they can be considered grounded.

    Based on Larsson (2002) Section 3.6.1.
    """

    move_type: str
    """Type of dialogue move (ask, answer, assert, etc.)"""

    min_confidence: float = 0.7
    """Minimum confidence score for optimistic grounding"""

    requires_confirmation: bool = False
    """Whether this move type requires explicit confirmation"""

    action_level: ActionLevel = ActionLevel.UNDERSTANDING
    """Minimum action level required for grounding"""

    def __str__(self) -> str:
        """Return string representation."""
        return (
            f"EvidenceRequirement({self.move_type}, "
            f"confidence>={self.min_confidence}, "
            f"level={self.action_level.value})"
        )


# Default evidence requirements per move type
# Based on Larsson (2002) Section 3.6.6
DEFAULT_EVIDENCE_REQUIREMENTS = {
    "ask": EvidenceRequirement(
        move_type="ask",
        min_confidence=0.8,
        requires_confirmation=False,
        action_level=ActionLevel.UNDERSTANDING,
    ),
    "answer": EvidenceRequirement(
        move_type="answer",
        min_confidence=0.7,
        requires_confirmation=False,
        action_level=ActionLevel.UNDERSTANDING,
    ),
    "assert": EvidenceRequirement(
        move_type="assert",
        min_confidence=0.75,
        requires_confirmation=False,
        action_level=ActionLevel.UNDERSTANDING,
    ),
    "request": EvidenceRequirement(
        move_type="request",
        min_confidence=0.8,
        requires_confirmation=True,  # Requests should be confirmed
        action_level=ActionLevel.ACCEPTANCE,
    ),
    "greet": EvidenceRequirement(
        move_type="greet",
        min_confidence=0.6,
        requires_confirmation=False,
        action_level=ActionLevel.PERCEPTION,
    ),
    "quit": EvidenceRequirement(
        move_type="quit",
        min_confidence=0.9,
        requires_confirmation=True,  # Always confirm quit
        action_level=ActionLevel.ACCEPTANCE,
    ),
    "icm": EvidenceRequirement(
        move_type="icm",
        min_confidence=0.7,
        requires_confirmation=False,
        action_level=ActionLevel.PERCEPTION,
    ),
}


def select_grounding_strategy(
    move_type: str,
    confidence_score: float,
    evidence_requirements: dict[str, EvidenceRequirement] | None = None,
) -> GroundingStrategy:
    """Select grounding strategy based on move type and confidence.

    Based on Larsson (2002) Section 3.6.6: "For user utterances, IBiS2
    uses optimistic or pessimistic grounding strategies based on the
    recognition score and the dialogue move type."

    Args:
        move_type: Type of dialogue move (ask, answer, etc.)
        confidence_score: Recognition/understanding confidence (0.0-1.0)
        evidence_requirements: Custom evidence requirements (optional)

    Returns:
        GroundingStrategy to use for this move

    Example:
        >>> select_grounding_strategy("answer", 0.9)
        <GroundingStrategy.OPTIMISTIC: 'optimistic'>
        >>> select_grounding_strategy("answer", 0.5)
        <GroundingStrategy.PESSIMISTIC: 'pessimistic'>
    """
    if evidence_requirements is None:
        evidence_requirements = DEFAULT_EVIDENCE_REQUIREMENTS

    # Get evidence requirement for this move type
    requirement = evidence_requirements.get(move_type, EvidenceRequirement(move_type=move_type))

    # High confidence: use optimistic grounding
    if confidence_score >= requirement.min_confidence:
        return GroundingStrategy.OPTIMISTIC

    # Medium confidence: use cautious grounding (with backtracking)
    elif confidence_score >= 0.5:
        return GroundingStrategy.CAUTIOUS

    # Low confidence: use pessimistic grounding (require confirmation)
    else:
        return GroundingStrategy.PESSIMISTIC


def requires_confirmation(
    move_type: str,
    confidence_score: float,
    evidence_requirements: dict[str, EvidenceRequirement] | None = None,
) -> bool:
    """Check if a move requires explicit confirmation.

    Based on Larsson (2002) Section 3.6.6.

    Args:
        move_type: Type of dialogue move
        confidence_score: Recognition/understanding confidence (0.0-1.0)
        evidence_requirements: Custom evidence requirements (optional)

    Returns:
        True if confirmation is required, False otherwise

    Example:
        >>> requires_confirmation("quit", 0.9)
        True
        >>> requires_confirmation("greet", 0.9)
        False
    """
    if evidence_requirements is None:
        evidence_requirements = DEFAULT_EVIDENCE_REQUIREMENTS

    requirement = evidence_requirements.get(move_type, EvidenceRequirement(move_type=move_type))

    # Always confirm if move type requires it
    if requirement.requires_confirmation:
        return True

    # Also confirm if confidence is low
    if confidence_score < requirement.min_confidence:
        return True

    return False


def get_evidence_requirement(
    move_type: str,
    evidence_requirements: dict[str, EvidenceRequirement] | None = None,
) -> EvidenceRequirement:
    """Get evidence requirement for a move type.

    Args:
        move_type: Type of dialogue move
        evidence_requirements: Custom evidence requirements (optional)

    Returns:
        EvidenceRequirement for this move type
    """
    if evidence_requirements is None:
        evidence_requirements = DEFAULT_EVIDENCE_REQUIREMENTS

    return evidence_requirements.get(move_type, EvidenceRequirement(move_type=move_type))
