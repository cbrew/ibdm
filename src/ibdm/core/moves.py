"""Dialogue move representations for Issue-Based Dialogue Management.

Dialogue moves are the atomic units of communication in the dialogue.
They represent speaker intentions and actions.
"""

import time
from dataclasses import dataclass, field
from typing import Any, cast


@dataclass
class DialogueMove:
    """Abstract dialogue move.

    Dialogue moves represent communicative acts performed by dialogue participants.
    Common move types include: ask, answer, assert, request, greet, quit, icm.
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

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict.

        This ensures proper serialization for Burr's persistence layer.

        Returns:
            Dictionary representation suitable for JSON serialization
        """
        return {
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

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DialogueMove":
        """Reconstruct DialogueMove from dict.

        Properly deserializes Question and Answer objects from their dict representations.

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

        return cls(
            move_type=data.get("move_type", "unknown"),
            content=content,
            speaker=data.get("speaker", "unknown"),
            timestamp=data.get("timestamp", time.time()),
            metadata=data.get("metadata", {}),
        )

    def __str__(self) -> str:
        """Return string representation."""
        return f"{self.speaker}:{self.move_type}({self.content})"
