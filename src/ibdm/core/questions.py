"""Question representations for Issue-Based Dialogue Management.

Questions represent issues under discussion in the dialogue. They are semantic
representations that can be raised, addressed, and resolved through dialogue moves.

Based on Larsson (2002) Issue-based Dialogue Management.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Question(ABC):
    """Base class for semantic question representations.

    Questions are the core of Issue-Based Dialogue Management. They represent
    issues that participants collaboratively address through dialogue.
    """

    @abstractmethod
    def resolves_with(self, answer: "Answer") -> bool:
        """Check if an answer resolves this question.

        Args:
            answer: The answer to check

        Returns:
            True if the answer resolves this question
        """
        pass

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict.

        Returns:
            Dictionary representation suitable for JSON serialization
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Return a human-readable string representation."""
        pass


@dataclass
class WhQuestion(Question):
    """Wh-question: ?x.P(x) - What is x such that P(x)?

    Examples:
        - "What's the weather?" → WhQuestion(variable="x", predicate="weather(x)")
        - "Where is Stockholm?" → WhQuestion(variable="x", predicate="location(stockholm, x)")
    """

    variable: str
    predicate: str
    constraints: dict[str, Any] = field(default_factory=lambda: {})

    def resolves_with(self, answer: "Answer") -> bool:
        """Check if answer provides a value for the variable."""
        if not hasattr(answer, "content") or answer.content is None:
            return False
        # An answer resolves a Wh-question if it provides a value
        return answer.question_ref is None or answer.question_ref == self

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return {
            "type": "wh",
            "variable": self.variable,
            "predicate": self.predicate,
            "constraints": self.constraints.copy(),
        }

    def __str__(self) -> str:
        """Return string representation."""
        constraints_str = ""
        if self.constraints:
            constraints_str = f" [{', '.join(f'{k}={v}' for k, v in self.constraints.items())}]"
        return f"?{self.variable}.{self.predicate}{constraints_str}"


@dataclass
class YNQuestion(Question):
    """Yes/No question: ?P - Is P true?

    Examples:
        - "Is it raining?" → YNQuestion(proposition="raining")
        - "Do you like coffee?" → YNQuestion(proposition="likes(you, coffee)")
    """

    proposition: str
    parameters: dict[str, Any] = field(default_factory=lambda: {})

    def resolves_with(self, answer: "Answer") -> bool:
        """Check if answer provides a yes/no value."""
        if not hasattr(answer, "content"):
            return False
        # An answer resolves a Y/N question if it's a boolean or yes/no
        content = answer.content
        if isinstance(content, bool):
            return True
        if isinstance(content, str):
            return content.lower() in ["yes", "no", "true", "false"]
        return False

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return {
            "type": "yn",
            "proposition": self.proposition,
            "parameters": self.parameters.copy(),
        }

    def __str__(self) -> str:
        """Return string representation."""
        params_str = ""
        if self.parameters:
            params_str = f" [{', '.join(f'{k}={v}' for k, v in self.parameters.items())}]"
        return f"?{self.proposition}{params_str}"


@dataclass
class AltQuestion(Question):
    """Alternative question: ?{P1, P2, ...} - Which of these is true?

    Examples:
        - "Tea or coffee?" → AltQuestion(alternatives=["tea", "coffee"])
        - "Red, green, or blue?" → AltQuestion(alternatives=["red", "green", "blue"])
    """

    alternatives: list[str] = field(default_factory=lambda: [])

    def resolves_with(self, answer: "Answer") -> bool:
        """Check if answer selects one of the alternatives."""
        if not hasattr(answer, "content") or answer.content is None:
            return False
        # An answer resolves an alternative question if it selects one alternative
        content = str(answer.content).lower()
        return any(alt.lower() in content or content in alt.lower() for alt in self.alternatives)

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return {
            "type": "alt",
            "alternatives": self.alternatives.copy(),
        }

    def __str__(self) -> str:
        """Return string representation."""
        return f"?{{{', '.join(self.alternatives)}}}"


# Import here to avoid circular dependency
from ibdm.core.answers import Answer  # noqa: E402
