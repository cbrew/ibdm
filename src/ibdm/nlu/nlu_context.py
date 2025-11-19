"""NLU context for tracking state across dialogue turns in Burr.

This module provides the NLUContext dataclass that holds NLU component state
that needs to be tracked across dialogue turns, enabling stateless NLU engine design.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class NLUContext:
    """NLU state tracked across dialogue turns.

    This context captures the state of NLU components (entity tracking,
    reference resolution, etc.) that needs to persist across turns but
    is managed by Burr State rather than the engine.

    Attributes:
        entities: List of extracted entities (serialized as dicts)
        entity_mentions: Mapping of entity IDs to their mentions
        reference_chains: List of reference resolution chains
        last_interpretation_tokens: Token count from last LLM call
        last_interpretation_latency: Latency in seconds from last interpretation
    """

    entities: list[dict[str, Any]] = field(default_factory=list)
    entity_mentions: dict[str, list[str]] = field(default_factory=dict)
    reference_chains: list[list[str]] = field(default_factory=list)
    last_interpretation_tokens: int = 0
    last_interpretation_latency: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict for Burr state storage.

        Returns:
            Dictionary representation suitable for JSON serialization
        """
        return {
            "entities": self.entities,
            "entity_mentions": self.entity_mentions,
            "reference_chains": self.reference_chains,
            "last_interpretation_tokens": self.last_interpretation_tokens,
            "last_interpretation_latency": self.last_interpretation_latency,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "NLUContext":
        """Create from dict loaded from Burr state.

        Args:
            data: Dictionary representation

        Returns:
            NLUContext instance
        """
        return cls(
            entities=data.get("entities", []),
            entity_mentions=data.get("entity_mentions", {}),
            reference_chains=data.get("reference_chains", []),
            last_interpretation_tokens=data.get("last_interpretation_tokens", 0),
            last_interpretation_latency=data.get("last_interpretation_latency", 0.0),
        )

    @classmethod
    def create_empty(cls) -> "NLUContext":
        """Create an empty NLU context for initialization.

        Returns:
            Empty NLUContext instance
        """
        return cls()
