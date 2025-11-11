"""Answer representations for Issue-Based Dialogue Management.

Answers resolve questions and can be integrated into the information state
as shared commitments.
"""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Answer:
    """Answer to a question.

    Answers provide values that resolve questions. They can have varying
    degrees of certainty and may reference the question they answer.
    """

    content: Any
    """The actual answer value (can be any type: str, bool, int, object, etc.)"""

    question_ref: Optional["Question"] = None
    """Reference to the question this answer addresses"""

    certainty: float = 1.0
    """Confidence level (0.0 to 1.0)"""

    def __str__(self) -> str:
        """Return string representation."""
        certainty_str = f" (certainty: {self.certainty:.2f})" if self.certainty < 1.0 else ""
        return f"Answer({self.content}){certainty_str}"


# Import here to avoid circular dependency
from ibdm.core.questions import Question  # noqa: E402, F401
