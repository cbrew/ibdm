"""NLG Result dataclass for serializing NLG processing results in Burr State.

This module provides the NLGResult dataclass that captures all outputs from the
NLG processing stage, enabling visibility and debugging in the Burr pipeline.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class NLGResult:
    """Result from NLG processing of a dialogue move.

    This dataclass captures all NLG outputs in a structured format suitable for
    serialization to Burr State. It includes the generated text, strategy used,
    and performance metrics.

    Attributes:
        utterance_text: Generated natural language text
        strategy: Generation strategy used ("template" | "plan_aware" | "llm")
        generation_rule: Name of the generation rule applied (if any)
        tokens_used: Number of LLM tokens used during NLG processing
        latency: Processing time in seconds
        metadata: Additional generation metadata (optional)
    """

    utterance_text: str
    strategy: str
    generation_rule: str | None = None
    tokens_used: int = 0
    latency: float = 0.0
    metadata: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict for Burr state storage.

        Returns:
            Dictionary representation suitable for JSON serialization
        """
        return {
            "utterance_text": self.utterance_text,
            "strategy": self.strategy,
            "generation_rule": self.generation_rule,
            "tokens_used": self.tokens_used,
            "latency": self.latency,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "NLGResult":
        """Create from dict loaded from Burr state.

        Args:
            data: Dictionary representation

        Returns:
            NLGResult instance
        """
        return cls(
            utterance_text=data["utterance_text"],
            strategy=data["strategy"],
            generation_rule=data.get("generation_rule"),
            tokens_used=data.get("tokens_used", 0),
            latency=data.get("latency", 0.0),
            metadata=data.get("metadata"),
        )

    def __str__(self) -> str:
        """Return string representation."""
        parts = [f"strategy={self.strategy}"]
        if self.generation_rule:
            parts.append(f"rule={self.generation_rule}")
        if self.tokens_used > 0:
            parts.append(f"tokens={self.tokens_used}")
        parts.append(f"latency={self.latency:.3f}s")
        return f"NLGResult({', '.join(parts)})"
