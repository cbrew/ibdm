"""Reference resolution for IBDM.

This module provides reference resolution capabilities for resolving pronouns,
definite descriptions, and demonstratives to entities in the discourse context.
"""

import logging
import re
from dataclasses import dataclass
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from ibdm.core.information_state import InformationState
from ibdm.nlu.entity_extractor import Entity, EntityTracker, EntityType
from ibdm.nlu.llm_adapter import LLMAdapter, LLMConfig, ModelType

logger = logging.getLogger(__name__)


class ReferenceType(str, Enum):
    """Types of references that can be resolved."""

    PRONOUN = "pronoun"  # he, she, they, it
    DEMONSTRATIVE = "demonstrative"  # this, that, these, those
    DEFINITE_DESCRIPTION = "definite_description"  # the X
    ONE_ANAPHORA = "one_anaphora"  # one, ones
    POSSESSIVE = "possessive"  # his, her, their
    OTHER = "other"


class Reference(BaseModel):
    """A reference to resolve.

    Attributes:
        text: The reference text
        type: The reference type
        index: Position in utterance
        properties: Additional properties (e.g., number, gender)
    """

    text: str = Field(..., description="Reference text")
    type: str = Field(..., description="Reference type")
    index: int = Field(..., description="Position in utterance")
    properties: dict[str, Any] = Field(default_factory=dict, description="Additional properties")


class ReferenceResolution(BaseModel):
    """Result of reference resolution.

    Attributes:
        reference: The original reference
        resolved_entity: The entity this reference resolves to (if found)
        candidates: List of candidate entities with salience scores
        confidence: Resolution confidence
        ambiguous: Whether resolution is ambiguous
    """

    reference: Reference = Field(..., description="Original reference")
    resolved_entity: Entity | None = Field(default=None, description="Resolved entity")
    candidates: list[dict[str, Any]] = Field(
        default_factory=list, description="Candidate entities with scores"
    )
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    ambiguous: bool = Field(default=False, description="Whether resolution is ambiguous")


@dataclass
class ReferenceResolverConfig:
    """Configuration for reference resolver.

    Attributes:
        llm_config: Configuration for the LLM adapter
        use_llm: Whether to use LLM for complex references
        salience_recency_weight: Weight for recency in salience (0-1)
        salience_syntactic_weight: Weight for syntactic position
        ambiguity_threshold: Threshold for marking resolution as ambiguous
        confidence_threshold: Minimum confidence for resolution
    """

    llm_config: LLMConfig | None = None
    use_llm: bool = True
    salience_recency_weight: float = 0.6
    salience_syntactic_weight: float = 0.4
    ambiguity_threshold: float = 0.2  # Difference between top 2 candidates
    confidence_threshold: float = 0.5


class ReferenceResolver:
    """Resolver for pronouns and definite references.

    Uses discourse context, entity tracking, and salience heuristics to resolve
    references to their antecedents.

    Example:
        >>> tracker = EntityTracker()
        >>> resolver = ReferenceResolver(tracker)
        >>>
        >>> # First utterance
        >>> entities = [Entity(text="Alice", type="person", mention_id="m_1", confidence=0.95)]
        >>> tracker.update(entities)
        >>>
        >>> # Resolve pronoun in second utterance
        >>> ref = Reference(text="she", type="pronoun", index=0)
        >>> resolution = resolver.resolve(ref, InformationState())
        >>> print(resolution.resolved_entity.text)
        Alice
    """

    def __init__(
        self,
        entity_tracker: EntityTracker,
        config: ReferenceResolverConfig | None = None,
    ):
        """Initialize the reference resolver.

        Args:
            entity_tracker: Entity tracker with discourse entities
            config: Resolver configuration. Uses defaults if not provided.
        """
        self.entity_tracker = entity_tracker
        self.config = config or ReferenceResolverConfig()

        # Initialize LLM if enabled
        self.llm: LLMAdapter | None = None
        if self.config.use_llm:
            try:
                llm_config = self.config.llm_config or LLMConfig(
                    model=ModelType.HAIKU,  # Use Haiku for fast resolution
                    temperature=0.3,
                    max_tokens=500,
                )
                self.llm = LLMAdapter(llm_config)
            except ValueError as e:
                logger.warning(f"LLM initialization failed, using rule-based only: {e}")
                self.llm = None

        logger.info("Reference resolver initialized")

    def resolve(
        self,
        reference: Reference,
        state: InformationState,
        utterance: str | None = None,
    ) -> ReferenceResolution:
        """Resolve a reference to an entity.

        Args:
            reference: The reference to resolve
            state: Current information state providing discourse context
            utterance: Optional full utterance for context

        Returns:
            ReferenceResolution with resolved entity and candidates
        """
        logger.info(f"Resolving reference: {reference.text} ({reference.type})")

        # Get candidate entities based on reference type
        candidates = self._get_candidates(reference, state)

        if not candidates:
            logger.info("No candidates found for reference")
            return ReferenceResolution(
                reference=reference,
                confidence=0.0,
            )

        # Score candidates by salience
        scored_candidates = self._score_candidates(reference, candidates, state)

        # Sort by score
        scored_candidates.sort(key=lambda x: x["score"], reverse=True)

        # Check for ambiguity
        ambiguous = False
        if len(scored_candidates) >= 2:
            top_score = scored_candidates[0]["score"]
            second_score = scored_candidates[1]["score"]
            if (top_score - second_score) < self.config.ambiguity_threshold:
                ambiguous = True

        # Get best candidate
        best = scored_candidates[0]
        confidence = best["score"]

        # Use LLM for complex/ambiguous cases
        if ambiguous and self.llm and utterance:
            llm_resolution = self._resolve_with_llm(reference, scored_candidates[:3], utterance)
            if llm_resolution:
                best = llm_resolution
                confidence = llm_resolution["score"]
                ambiguous = False

        # Check confidence threshold
        if confidence < self.config.confidence_threshold:
            logger.info(f"Confidence {confidence:.2f} below threshold, marking as unresolved")
            return ReferenceResolution(
                reference=reference,
                candidates=scored_candidates,
                confidence=confidence,
                ambiguous=True,
            )

        return ReferenceResolution(
            reference=reference,
            resolved_entity=best["entity"],
            candidates=scored_candidates,
            confidence=confidence,
            ambiguous=ambiguous,
        )

    def resolve_all(
        self,
        utterance: str,
        state: InformationState,
    ) -> list[ReferenceResolution]:
        """Detect and resolve all references in an utterance.

        Args:
            utterance: The utterance to process
            state: Current information state

        Returns:
            List of ReferenceResolution objects
        """
        # Detect references in utterance
        references = self._detect_references(utterance)

        # Resolve each reference
        resolutions = []
        for ref in references:
            resolution = self.resolve(ref, state, utterance)
            resolutions.append(resolution)

        return resolutions

    def _get_candidates(
        self,
        reference: Reference,
        state: InformationState,
    ) -> list[Entity]:
        """Get candidate entities for a reference.

        Args:
            reference: The reference
            state: Information state

        Returns:
            List of candidate entities
        """
        # Get recent entities from tracker
        recent_entities = self.entity_tracker.get_recent_entities(n=10)

        # Filter based on reference type and properties
        candidates = []

        for entity in recent_entities:
            if self._is_compatible(reference, entity):
                candidates.append(entity)

        return candidates

    def _is_compatible(self, reference: Reference, entity: Entity) -> bool:
        """Check if entity is compatible with reference.

        Args:
            reference: The reference
            entity: The entity

        Returns:
            True if compatible
        """
        ref_type = reference.type

        # Pronoun compatibility
        if ref_type == ReferenceType.PRONOUN.value:
            return self._pronoun_compatible(reference.text, entity)

        # Demonstrative compatibility (this, that, etc.)
        if ref_type == ReferenceType.DEMONSTRATIVE.value:
            return True  # Most demonstratives can refer to any entity

        # Definite description compatibility
        if ref_type == ReferenceType.DEFINITE_DESCRIPTION.value:
            return self._description_compatible(reference.text, entity)

        return True

    def _pronoun_compatible(self, pronoun: str, entity: Entity) -> bool:
        """Check if pronoun is compatible with entity.

        Args:
            pronoun: The pronoun text
            entity: The entity

        Returns:
            True if compatible
        """
        pronoun_lower = pronoun.lower()

        # Person pronouns
        if pronoun_lower in ["he", "him", "his", "himself"]:
            return entity.type == EntityType.PERSON.value
        if pronoun_lower in ["she", "her", "hers", "herself"]:
            return entity.type == EntityType.PERSON.value
        if pronoun_lower in ["they", "them", "their", "theirs", "themselves"]:
            return True  # Can refer to persons or organizations
        if pronoun_lower in ["it", "its", "itself"]:
            return entity.type not in [EntityType.PERSON.value]

        return True

    def _description_compatible(self, description: str, entity: Entity) -> bool:
        """Check if definite description is compatible with entity.

        Args:
            description: The description text
            entity: The entity

        Returns:
            True if compatible
        """
        desc_lower = description.lower()
        entity_text_lower = entity.text.lower()

        # Check if description contains entity text
        if entity_text_lower in desc_lower:
            return True

        # Check if entity has canonical form that matches
        if entity.canonical_form and entity.canonical_form.lower() in desc_lower:
            return True

        # Check for type-based descriptions
        if entity.type == EntityType.PERSON.value and any(
            word in desc_lower for word in ["person", "man", "woman", "guy", "girl"]
        ):
            return True

        if entity.type == EntityType.LOCATION.value and any(
            word in desc_lower for word in ["place", "location", "city", "country"]
        ):
            return True

        return False

    def _score_candidates(
        self,
        reference: Reference,
        candidates: list[Entity],
        state: InformationState,
    ) -> list[dict[str, Any]]:
        """Score candidate entities by salience.

        Args:
            reference: The reference
            candidates: Candidate entities
            state: Information state

        Returns:
            List of dicts with entity and score
        """
        scored = []

        for idx, entity in enumerate(candidates):
            # Recency score (more recent = higher score)
            recency_score = 1.0 - (idx / max(len(candidates), 1))

            # Syntactic prominence (simplified - first mention has higher prominence)
            syntactic_score = 1.0 if idx == 0 else 0.5

            # QUD relevance (is entity related to current question?)
            qud_score = self._compute_qud_relevance(entity, state)

            # Combined salience score
            salience = (
                self.config.salience_recency_weight * recency_score
                + self.config.salience_syntactic_weight * syntactic_score
                + (1 - self.config.salience_recency_weight - self.config.salience_syntactic_weight)
                * qud_score
            )

            scored.append({"entity": entity, "score": salience})

        return scored

    def _compute_qud_relevance(self, entity: Entity, state: InformationState) -> float:
        """Compute relevance to current QUD.

        Args:
            entity: The entity
            state: Information state

        Returns:
            Relevance score (0-1)
        """
        # Check if entity is mentioned in top QUD
        top_qud = state.shared.top_qud()
        if not top_qud:
            return 0.5  # Neutral if no QUD

        qud_str = str(top_qud).lower()
        entity_text = entity.text.lower()

        # Simple check: is entity text in QUD string?
        if entity_text in qud_str:
            return 1.0

        if entity.canonical_form and entity.canonical_form.lower() in qud_str:
            return 1.0

        return 0.3  # Low relevance by default

    def _resolve_with_llm(
        self,
        reference: Reference,
        candidates: list[dict[str, Any]],
        utterance: str,
    ) -> dict[str, Any] | None:
        """Use LLM to resolve ambiguous reference.

        Args:
            reference: The reference
            candidates: Top candidate entities with scores
            utterance: The full utterance

        Returns:
            Selected candidate dict or None
        """
        if not self.llm:
            return None

        try:
            # Build prompt
            prompt = self._build_llm_resolution_prompt(reference, candidates, utterance)

            response = self.llm.call(
                prompt=prompt,
                system_prompt="You are an expert at resolving references in natural language. "
                "Select the most likely entity that a reference refers to based on context.",
            )

            # Parse response to get selected candidate index
            content = response.content.strip().lower()
            for i, candidate in enumerate(candidates):
                if str(i) in content or candidate["entity"].text.lower() in content:
                    return candidate

        except Exception as e:
            logger.warning(f"LLM resolution failed: {e}")

        return None

    def _build_llm_resolution_prompt(
        self,
        reference: Reference,
        candidates: list[dict[str, Any]],
        utterance: str,
    ) -> str:
        """Build prompt for LLM resolution.

        Args:
            reference: The reference
            candidates: Candidate entities
            utterance: The utterance

        Returns:
            Prompt string
        """
        prompt_parts = [
            f'In the utterance: "{utterance}"\n',
            f'\nThe reference "{reference.text}" (type: {reference.type}) needs to be resolved.\n',
            "\nCandidate entities:",
        ]

        for i, cand in enumerate(candidates):
            entity = cand["entity"]
            prompt_parts.append(
                f"\n{i}. {entity.text} (type: {entity.type}, score: {cand['score']:.2f})"
            )

        prompt_parts.append(
            "\n\nWhich entity does this reference most likely refer to? "
            "Respond with the number (0, 1, or 2) and the entity text."
        )

        return "\n".join(prompt_parts)

    def _detect_references(self, utterance: str) -> list[Reference]:
        """Detect references in an utterance.

        Args:
            utterance: The utterance

        Returns:
            List of detected references
        """
        references = []
        words = utterance.split()

        # Pronouns
        pronouns = {
            "he",
            "him",
            "his",
            "himself",
            "she",
            "her",
            "hers",
            "herself",
            "they",
            "them",
            "their",
            "theirs",
            "themselves",
            "it",
            "its",
            "itself",
        }

        # Demonstratives
        demonstratives = {"this", "that", "these", "those"}

        for idx, word in enumerate(words):
            word_lower = word.lower().strip(".,!?;:")

            if word_lower in pronouns:
                references.append(
                    Reference(
                        text=word_lower,
                        type=ReferenceType.PRONOUN.value,
                        index=idx,
                    )
                )

            elif word_lower in demonstratives:
                references.append(
                    Reference(
                        text=word_lower,
                        type=ReferenceType.DEMONSTRATIVE.value,
                        index=idx,
                    )
                )

        # Detect definite descriptions (simple pattern: "the X")
        the_pattern = r"\bthe\s+(\w+(?:\s+\w+)?)"
        for match in re.finditer(the_pattern, utterance, re.IGNORECASE):
            references.append(
                Reference(
                    text=match.group(0),
                    type=ReferenceType.DEFINITE_DESCRIPTION.value,
                    index=match.start(),
                )
            )

        return references


def create_resolver(
    entity_tracker: EntityTracker,
    use_llm: bool = True,
) -> ReferenceResolver:
    """Convenience function to create a reference resolver.

    Args:
        entity_tracker: Entity tracker with discourse entities
        use_llm: Whether to use LLM for complex references

    Returns:
        Configured ReferenceResolver instance

    Example:
        >>> tracker = EntityTracker()
        >>> resolver = create_resolver(tracker, use_llm=True)
    """
    config = ReferenceResolverConfig(use_llm=use_llm)
    return ReferenceResolver(entity_tracker, config)
