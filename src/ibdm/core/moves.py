"""Dialogue move representations for Issue-Based Dialogue Management.

Dialogue moves are the atomic units of communication in the dialogue.
They represent speaker intentions and actions.

ICM Extensions (IBiS2):
Interactive Communication Management (ICM) moves provide feedback about
grounding at different action levels (perception, understanding, acceptance).
Based on Larsson (2002) Section 3.4.
"""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from ibdm.core.grounding import ActionLevel


class Polarity(Enum):
    """Polarity of ICM feedback moves.

    Based on Larsson (2002) Section 3.4 - ICM Taxonomy.

    ICM moves can provide:
    - Positive feedback (confirmation, understanding)
    - Negative feedback (perception failure, misunderstanding)
    - Interrogative feedback (request for confirmation)
    """

    POSITIVE = "pos"
    """Positive feedback: 'I heard you', 'Okay', 'Paris'"""

    NEGATIVE = "neg"
    """Negative feedback: 'Pardon?', 'I don't understand'"""

    INTERROGATIVE = "int"
    """Interrogative feedback: 'Paris, is that correct?', 'Did you say Paris?'"""


@dataclass
class DialogueMove:
    """Abstract dialogue move.

    Dialogue moves represent communicative acts performed by dialogue participants.
    Common move types include: ask, answer, assert, request, greet, quit, icm.

    ICM Extensions (IBiS2):
    For ICM (Interactive Communication Management) moves, additional fields
    specify the feedback level, polarity, and target of the feedback.
    Based on Larsson (2002) Section 3.4.
    """

    move_type: str
    """Type of move: 'ask', 'answer', 'assert', 'request', 'greet', 'quit', 'icm', etc."""

    content: Any
    """Content of the move (Question, Answer, proposition, etc.)"""

    speaker: str
    """ID of the speaker performing this move"""

    timestamp: float = field(default_factory=lambda: time.time())
    """Timestamp when the move was created"""

    metadata: dict[str, Any] = field(default_factory=lambda: {})
    """Additional metadata about the move (e.g., confidence scores, NLU annotations)"""

    # ICM-specific fields (IBiS2)
    feedback_level: "ActionLevel | None" = None
    """Action level of ICM feedback (PERCEPTION, UNDERSTANDING, ACCEPTANCE) - IBiS2 only"""

    polarity: Polarity | None = None
    """Polarity of ICM feedback (POSITIVE, NEGATIVE, INTERROGATIVE) - IBiS2 only"""

    target_move_index: int | None = None
    """Index in shared.moves of the move being grounded - IBiS2 only"""

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict.

        This ensures proper serialization for Burr's persistence layer.
        Includes ICM-specific fields for IBiS2 grounding support.

        Returns:
            Dictionary representation suitable for JSON serialization
        """
        result = {
            "move_type": self.move_type,
            "content": (
                self.content.to_dict()
                if hasattr(self.content, "to_dict")
                else str(self.content)
                if self.content is not None
                else None
            ),
            "speaker": self.speaker,
            "timestamp": self.timestamp,
            "metadata": self.metadata.copy(),
        }

        # Add ICM-specific fields if present (IBiS2)
        if self.feedback_level is not None:
            result["feedback_level"] = self.feedback_level.value
        if self.polarity is not None:
            result["polarity"] = self.polarity.value
        if self.target_move_index is not None:
            result["target_move_index"] = self.target_move_index

        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DialogueMove":
        """Reconstruct DialogueMove from dict.

        Properly deserializes Question, Answer, and ICM-specific fields.

        Args:
            data: Dictionary representation from to_dict()

        Returns:
            Reconstructed DialogueMove
        """
        content: Any = data.get("content")

        # Deserialize Questions and Answers from dict representations
        if isinstance(content, dict):
            # Import here to avoid circular dependency
            from ibdm.core.answers import Answer
            from ibdm.core.questions import Question

            content_dict = cast(dict[str, Any], content)
            # Check if it's a Question (has 'type' field)
            if "type" in content_dict:
                content = Question.from_dict(content_dict)
            # Check if it's an Answer (has 'question_ref' field)
            elif "question_ref" in content_dict:
                content = Answer.from_dict(content_dict)
            # Otherwise leave as dict

        # Deserialize ICM-specific fields (IBiS2)
        feedback_level = None
        if "feedback_level" in data:
            from ibdm.core.grounding import ActionLevel

            feedback_level = ActionLevel(data["feedback_level"])

        polarity = None
        if "polarity" in data:
            polarity = Polarity(data["polarity"])

        return cls(
            move_type=data.get("move_type", "unknown"),
            content=content,
            speaker=data.get("speaker", "unknown"),
            timestamp=data.get("timestamp", time.time()),
            metadata=data.get("metadata", {}),
            feedback_level=feedback_level,
            polarity=polarity,
            target_move_index=data.get("target_move_index"),
        )

    def __str__(self) -> str:
        """Return string representation.

        For ICM moves, includes feedback level and polarity in format:
        speaker:icm:level*polarity(content)
        e.g., system:icm:per*pos(I heard you)
        """
        if self.move_type == "icm" and self.feedback_level and self.polarity:
            level = self.feedback_level.value
            pol = self.polarity.value
            return f"{self.speaker}:icm:{level}*{pol}({self.content})"
        return f"{self.speaker}:{self.move_type}({self.content})"

    def is_icm(self) -> bool:
        """Check if this is an ICM (Interactive Communication Management) move."""
        return self.move_type == "icm"

    def get_icm_signature(self) -> str | None:
        """Get ICM signature in format 'level*polarity' (e.g., 'per*pos').

        Returns:
            ICM signature string, or None if not an ICM move

        Example:
            >>> move = create_icm_perception_positive("I heard you", "system")
            >>> move.get_icm_signature()
            'per*pos'
        """
        if not self.is_icm() or not self.feedback_level or not self.polarity:
            return None
        return f"{self.feedback_level.value}*{self.polarity.value}"


# ICM Factory Functions (IBiS2)
# Based on Larsson (2002) Section 3.4 - ICM Taxonomy


def create_icm_perception_positive(
    content: str,
    speaker: str,
    target_move_index: int | None = None,
) -> DialogueMove:
    """Create positive perception ICM move (icm:per*pos).

    Indicates that the speaker heard/perceived the utterance.
    Typically realized as verbatim repetition or "I heard you say...".

    Args:
        content: Content of the feedback (e.g., "I heard 'to Paris'")
        speaker: Speaker ID (typically 'system')
        target_move_index: Index of move being grounded in shared.moves

    Returns:
        ICM move with perception positive feedback

    Example:
        >>> move = create_icm_perception_positive("I heard 'to Paris'", "system")
        >>> move.get_icm_signature()
        'per*pos'
    """
    from ibdm.core.grounding import ActionLevel

    return DialogueMove(
        move_type="icm",
        content=content,
        speaker=speaker,
        feedback_level=ActionLevel.PERCEPTION,
        polarity=Polarity.POSITIVE,
        target_move_index=target_move_index,
    )


def create_icm_perception_negative(
    content: str,
    speaker: str,
    target_move_index: int | None = None,
) -> DialogueMove:
    """Create negative perception ICM move (icm:per*neg).

    Indicates perception failure (didn't hear the utterance).
    Typically realized as "Pardon?", "I didn't hear you".

    Args:
        content: Content of the feedback (e.g., "Pardon?")
        speaker: Speaker ID (typically 'system')
        target_move_index: Index of move being grounded in shared.moves

    Returns:
        ICM move with perception negative feedback

    Example:
        >>> move = create_icm_perception_negative("Pardon?", "system")
        >>> move.get_icm_signature()
        'per*neg'
    """
    from ibdm.core.grounding import ActionLevel

    return DialogueMove(
        move_type="icm",
        content=content,
        speaker=speaker,
        feedback_level=ActionLevel.PERCEPTION,
        polarity=Polarity.NEGATIVE,
        target_move_index=target_move_index,
    )


def create_icm_understanding_positive(
    content: Any,
    speaker: str,
    target_move_index: int | None = None,
) -> DialogueMove:
    """Create positive understanding ICM move (icm:und*pos).

    Indicates pragmatic understanding of the utterance.
    Typically realized as reformulation or "To Paris" (acknowledging destination).

    Args:
        content: Content of the feedback (interpreted content, Question, Answer, etc.)
        speaker: Speaker ID (typically 'system')
        target_move_index: Index of move being grounded in shared.moves

    Returns:
        ICM move with understanding positive feedback

    Example:
        >>> q = WhQuestion(variable="x", predicate="destination(x)")
        >>> move = create_icm_understanding_positive(q, "system")
        >>> move.get_icm_signature()
        'und*pos'
    """
    from ibdm.core.grounding import ActionLevel

    return DialogueMove(
        move_type="icm",
        content=content,
        speaker=speaker,
        feedback_level=ActionLevel.UNDERSTANDING,
        polarity=Polarity.POSITIVE,
        target_move_index=target_move_index,
    )


def create_icm_understanding_negative(
    content: str,
    speaker: str,
    target_move_index: int | None = None,
) -> DialogueMove:
    """Create negative understanding ICM move (icm:und*neg).

    Indicates understanding failure (didn't understand the utterance).
    Typically realized as "I don't understand", "I don't quite understand".

    Args:
        content: Content of the feedback (e.g., "I don't understand")
        speaker: Speaker ID (typically 'system')
        target_move_index: Index of move being grounded in shared.moves

    Returns:
        ICM move with understanding negative feedback

    Example:
        >>> move = create_icm_understanding_negative("I don't understand", "system")
        >>> move.get_icm_signature()
        'und*neg'
    """
    from ibdm.core.grounding import ActionLevel

    return DialogueMove(
        move_type="icm",
        content=content,
        speaker=speaker,
        feedback_level=ActionLevel.UNDERSTANDING,
        polarity=Polarity.NEGATIVE,
        target_move_index=target_move_index,
    )


def create_icm_understanding_interrogative(
    content: Any,
    speaker: str,
    target_move_index: int | None = None,
) -> DialogueMove:
    """Create interrogative understanding ICM move (icm:und*int).

    Requests confirmation of understanding.
    Typically realized as "To Paris, is that correct?", "Did you say Paris?".

    Args:
        content: Content needing confirmation (Question, Answer, or string)
        speaker: Speaker ID (typically 'system')
        target_move_index: Index of move being grounded in shared.moves

    Returns:
        ICM move with understanding interrogative feedback

    Example:
        >>> move = create_icm_understanding_interrogative("Paris, correct?", "system")
        >>> move.get_icm_signature()
        'und*int'
    """
    from ibdm.core.grounding import ActionLevel

    return DialogueMove(
        move_type="icm",
        content=content,
        speaker=speaker,
        feedback_level=ActionLevel.UNDERSTANDING,
        polarity=Polarity.INTERROGATIVE,
        target_move_index=target_move_index,
    )


def create_icm_acceptance_positive(
    content: str,
    speaker: str,
    target_move_index: int | None = None,
) -> DialogueMove:
    """Create positive acceptance ICM move (icm:acc*pos).

    Indicates acceptance/acknowledgment of the utterance.
    Typically realized as "Okay", "Good", "I'll do that".

    Args:
        content: Content of the feedback (e.g., "Okay")
        speaker: Speaker ID (typically 'system')
        target_move_index: Index of move being grounded in shared.moves

    Returns:
        ICM move with acceptance positive feedback

    Example:
        >>> move = create_icm_acceptance_positive("Okay", "system")
        >>> move.get_icm_signature()
        'acc*pos'
    """
    from ibdm.core.grounding import ActionLevel

    return DialogueMove(
        move_type="icm",
        content=content,
        speaker=speaker,
        feedback_level=ActionLevel.ACCEPTANCE,
        polarity=Polarity.POSITIVE,
        target_move_index=target_move_index,
    )


def create_icm_acceptance_negative(
    content: str,
    speaker: str,
    target_move_index: int | None = None,
) -> DialogueMove:
    """Create negative acceptance ICM move (icm:acc*neg).

    Indicates rejection of the proposition or request.
    Typically realized as "Sorry, I can't do that", explanation of why not.

    Args:
        content: Content of the rejection (e.g., "Sorry, Paris is not available")
        speaker: Speaker ID (typically 'system')
        target_move_index: Index of move being grounded in shared.moves

    Returns:
        ICM move with acceptance negative feedback

    Example:
        >>> move = create_icm_acceptance_negative("Sorry, not available", "system")
        >>> move.get_icm_signature()
        'acc*neg'
    """
    from ibdm.core.grounding import ActionLevel

    return DialogueMove(
        move_type="icm",
        content=content,
        speaker=speaker,
        feedback_level=ActionLevel.ACCEPTANCE,
        polarity=Polarity.NEGATIVE,
        target_move_index=target_move_index,
    )
