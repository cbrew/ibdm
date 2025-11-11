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

    def __str__(self) -> str:
        """Return string representation."""
        return f"{self.speaker}:{self.move_type}({self.content})"
