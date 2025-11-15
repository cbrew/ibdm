"""NLU Result dataclass for serializing NLU processing results in Burr State.

This module provides the NLUResult dataclass that captures all outputs from the
NLU processing stage, enabling visibility and debugging in the Burr pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class NLUResult:
    """Result from NLU processing of an utterance.

    This dataclass captures all NLU outputs in a structured format suitable for
    serialization to Burr State. It includes classification, entities, and
    dialogue-act-specific enrichments.

    Attributes:
        dialogue_act: Classified dialogue act type (e.g., "question", "answer", "command")
        confidence: Classification confidence score (0.0 to 1.0)
        entities: List of extracted entities (as dicts)
        intent: Classified intent for commands/requests (optional)
        question_details: Question analysis details for ask dialogue acts (optional)
        answer_content: Parsed answer content for answer dialogue acts (optional)
        raw_interpretation: Full interpretation result from context interpreter (optional)
        tokens_used: Number of LLM tokens used during NLU processing
        latency: Processing time in seconds
    """

    dialogue_act: str
    confidence: float
    # Entities are serialized as dicts for Burr State storage
    entities: list[dict[str, Any]] = field(default_factory=lambda: [])  # type: ignore[reportUnknownVariableType]
    intent: str | None = None
    question_details: dict[str, Any] | None = None
    answer_content: dict[str, Any] | None = None
    raw_interpretation: dict[str, Any] | None = None
    tokens_used: int = 0
    latency: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict for Burr state storage.

        Returns:
            Dictionary representation suitable for JSON serialization
        """
        return {
            "dialogue_act": self.dialogue_act,
            "confidence": self.confidence,
            "entities": self.entities,
            "intent": self.intent,
            "question_details": self.question_details,
            "answer_content": self.answer_content,
            "raw_interpretation": self.raw_interpretation,
            "tokens_used": self.tokens_used,
            "latency": self.latency,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> NLUResult:
        """Create from dict loaded from Burr state.

        Args:
            data: Dictionary representation

        Returns:
            NLUResult instance
        """
        return cls(
            dialogue_act=data["dialogue_act"],
            confidence=data["confidence"],
            entities=data.get("entities", []),
            intent=data.get("intent"),
            question_details=data.get("question_details"),
            answer_content=data.get("answer_content"),
            raw_interpretation=data.get("raw_interpretation"),
            tokens_used=data.get("tokens_used", 0),
            latency=data.get("latency", 0.0),
        )

    def __str__(self) -> str:
        """Return string representation."""
        parts = [f"{self.dialogue_act} (conf={self.confidence:.2f})"]
        if self.entities:
            parts.append(f"{len(self.entities)} entities")
        if self.intent:
            parts.append(f"intent={self.intent}")
        if self.question_details:
            parts.append("question_details")
        if self.answer_content:
            parts.append("answer_content")
        return f"NLUResult({', '.join(parts)})"
