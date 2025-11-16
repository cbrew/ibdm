"""Action and Proposition types for Action-Oriented Dialogue (IBiS-4).

Based on Larsson (2002) Chapter 5: Action-oriented and Negotiative Dialogue.

Actions represent non-communicative operations that can be performed by
dialogue participants (e.g., booking a hotel, adding a VCR program).

Propositions represent statements that can be negotiated (e.g., hotel
alternatives, preferences).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ActionType(Enum):
    """Types of actions that can be executed.

    Based on Larsson Section 5.3.2 (Actions and Postconditions).
    """

    BOOK = "book"
    """Book a reservation or resource"""

    CANCEL = "cancel"
    """Cancel an existing reservation or action"""

    SET = "set"
    """Set a parameter or configuration"""

    GET = "get"
    """Retrieve information from a device/system"""

    EXECUTE = "execute"
    """Execute a general action"""

    CONFIRM = "confirm"
    """Confirm an action before execution"""

    GENERATE = "generate"
    """Generate a document or artifact"""

    SEND = "send"
    """Send or transmit something"""


@dataclass
class Action:
    """Represents a non-communicative action.

    Actions are operations performed by dialogue participants, such as
    booking tickets, controlling devices, or generating documents.

    Based on Larsson (2002) Section 5.2 (Issues and Actions in AOD).

    Attributes:
        action_type: Type of action (book, cancel, set, etc.)
        name: Human-readable action name
        parameters: Action parameters/arguments
        preconditions: Predicates that must be true before execution
        postconditions: Predicates that become true after execution
        requires_confirmation: Whether this action needs user confirmation
        metadata: Additional action metadata

    Example:
        >>> action = Action(
        ...     action_type=ActionType.BOOK,
        ...     name="book_hotel",
        ...     parameters={"hotel_id": "H123", "check_in": "2025-01-05"},
        ...     preconditions=["check_in_date_known", "check_out_date_known"],
        ...     postconditions=["booked(hotel_id=H123)"],
        ...     requires_confirmation=True
        ... )
    """

    action_type: ActionType
    """Type of action"""

    name: str
    """Human-readable action name"""

    parameters: dict[str, Any] = field(default_factory=lambda: {})
    """Action parameters/arguments"""

    preconditions: list[str] = field(default_factory=lambda: [])
    """Predicates that must be satisfied before execution"""

    postconditions: list[str] = field(default_factory=lambda: [])
    """Predicates that become true after successful execution"""

    requires_confirmation: bool = True
    """Whether this action requires user confirmation before execution"""

    metadata: dict[str, Any] = field(default_factory=lambda: {})
    """Additional metadata (confidence, timestamps, etc.)"""

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict.

        Returns:
            Dictionary representation suitable for serialization
        """
        # Type annotations to satisfy pyright - these are safe copies of typed fields
        parameters: dict[str, Any] = self.parameters.copy()
        preconditions: list[str] = self.preconditions.copy()
        postconditions: list[str] = self.postconditions.copy()
        metadata: dict[str, Any] = self.metadata.copy()

        return {
            "action_type": self.action_type.value,
            "name": self.name,
            "parameters": parameters,
            "preconditions": preconditions,
            "postconditions": postconditions,
            "requires_confirmation": self.requires_confirmation,
            "metadata": metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Action":
        """Reconstruct from dict.

        Args:
            data: Dictionary representation from to_dict()

        Returns:
            Reconstructed Action object
        """
        parameters: dict[str, Any] = data.get("parameters", {}).copy()
        preconditions: list[str] = [str(p) for p in data.get("preconditions", [])]
        postconditions: list[str] = [str(p) for p in data.get("postconditions", [])]
        metadata: dict[str, Any] = data.get("metadata", {}).copy()

        return cls(
            action_type=ActionType(data["action_type"]),
            name=data["name"],
            parameters=parameters,
            preconditions=preconditions,
            postconditions=postconditions,
            requires_confirmation=data.get("requires_confirmation", True),
            metadata=metadata,
        )

    def __str__(self) -> str:
        """Return string representation."""
        params_str = ", ".join(f"{k}={v}" for k, v in self.parameters.items())
        confirm = " [needs confirmation]" if self.requires_confirmation else ""
        return f"{self.action_type.value}:{self.name}({params_str}){confirm}"

    def __hash__(self) -> int:
        """Make Action hashable for use in sets/dicts."""
        # Use name and frozen parameters for hash
        param_tuple = tuple(sorted(self.parameters.items()))
        return hash((self.action_type, self.name, param_tuple))

    def __eq__(self, other: object) -> bool:
        """Check equality based on type, name, and parameters."""
        if not isinstance(other, Action):
            return False
        return (
            self.action_type == other.action_type
            and self.name == other.name
            and self.parameters == other.parameters
        )


@dataclass
class Proposition:
    """Represents a statement that can be negotiated.

    Propositions are used in negotiative dialogue to represent alternatives,
    preferences, and statements under discussion.

    Based on Larsson (2002) Section 5.7 (Negotiative Dialogue).

    Attributes:
        predicate: The proposition predicate (e.g., "hotel", "price")
        arguments: Arguments to the predicate
        polarity: Whether the proposition is positive or negative
        confidence: Confidence score (0.0-1.0)
        metadata: Additional proposition metadata

    Example:
        >>> prop1 = Proposition(
        ...     predicate="hotel",
        ...     arguments={"name": "Hotel A", "price": 180, "location": "Paris"}
        ... )
        >>> prop2 = Proposition(
        ...     predicate="hotel",
        ...     arguments={"name": "Hotel B", "price": 150, "location": "Paris"}
        ... )
    """

    predicate: str
    """Proposition predicate"""

    arguments: dict[str, Any] = field(default_factory=lambda: {})
    """Predicate arguments"""

    polarity: bool = True
    """True for positive, False for negative"""

    confidence: float = 1.0
    """Confidence score (0.0-1.0)"""

    metadata: dict[str, Any] = field(default_factory=lambda: {})
    """Additional metadata"""

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict.

        Returns:
            Dictionary representation suitable for serialization
        """
        # Type annotations to satisfy pyright - these are safe copies of typed fields
        arguments: dict[str, Any] = self.arguments.copy()
        metadata: dict[str, Any] = self.metadata.copy()

        return {
            "predicate": self.predicate,
            "arguments": arguments,
            "polarity": self.polarity,
            "confidence": self.confidence,
            "metadata": metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Proposition":
        """Reconstruct from dict.

        Args:
            data: Dictionary representation from to_dict()

        Returns:
            Reconstructed Proposition object
        """
        arguments: dict[str, Any] = data.get("arguments", {}).copy()
        metadata: dict[str, Any] = data.get("metadata", {}).copy()

        return cls(
            predicate=data["predicate"],
            arguments=arguments,
            polarity=data.get("polarity", True),
            confidence=data.get("confidence", 1.0),
            metadata=metadata,
        )

    def __str__(self) -> str:
        """Return string representation."""
        args_str = ", ".join(f"{k}={v}" for k, v in self.arguments.items())
        polarity_str = "" if self.polarity else "¬"
        return f"{polarity_str}{self.predicate}({args_str})"

    def __hash__(self) -> int:
        """Make Proposition hashable for use in sets/dicts."""
        arg_tuple = tuple(sorted(self.arguments.items()))
        return hash((self.predicate, arg_tuple, self.polarity))

    def __eq__(self, other: object) -> bool:
        """Check equality based on predicate, arguments, and polarity."""
        if not isinstance(other, Proposition):
            return False
        return (
            self.predicate == other.predicate
            and self.arguments == other.arguments
            and self.polarity == other.polarity
        )


def dominates(prop1: Proposition, prop2: Proposition) -> bool:
    """Check if prop1 dominates prop2 (is strictly better).

    Based on Larsson Section 5.7.3 (Dominance and Alternatives).

    This is a placeholder implementation. Domain-specific dominance
    relations should be defined in domain models.

    Args:
        prop1: First proposition
        prop2: Second proposition

    Returns:
        True if prop1 dominates prop2, False otherwise

    Example:
        >>> p1 = Proposition("hotel", {"price": 150})
        >>> p2 = Proposition("hotel", {"price": 180})
        >>> dominates(p1, p2)  # Cheaper is better
        True
    """
    # Basic dominance: lower price is better (if both have price)
    if "price" in prop1.arguments and "price" in prop2.arguments:
        try:
            price1 = float(prop1.arguments["price"])
            price2 = float(prop2.arguments["price"])
            return price1 < price2
        except (ValueError, TypeError):
            pass

    # Basic dominance: higher rating is better (if both have rating)
    if "rating" in prop1.arguments and "rating" in prop2.arguments:
        try:
            rating1 = float(prop1.arguments["rating"])
            rating2 = float(prop2.arguments["rating"])
            return rating1 > rating2
        except (ValueError, TypeError):
            pass

    # No dominance relation found
    return False
