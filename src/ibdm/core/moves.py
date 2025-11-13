"""Dialogue move representations for Issue-Based Dialogue Management.

Dialogue moves are the atomic units of communication in the dialogue.
They represent speaker intentions and actions.
"""

import time
from dataclasses import dataclass, field
from typing import Any


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
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DialogueMove":
        """Reconstruct DialogueMove from dict.

        Note: Content is stored as string if it was a complex object.

        Args:
            data: Dictionary representation from to_dict()

        Returns:
            Reconstructed DialogueMove
        """
        return cls(
            move_type=data.get("move_type", "unknown"),
            content=data.get("content"),  # Keep as-is (may be string or dict)
            speaker=data.get("speaker", "unknown"),
            timestamp=data.get("timestamp", time.time()),
        )

    def __str__(self) -> str:
        """Return string representation."""
        return f"{self.speaker}:{self.move_type}({self.content})"
