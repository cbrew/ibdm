"""Entity extraction and tracking for IBDM.

This module provides LLM-based entity extraction and tracking capabilities including:
- Named entity recognition (persons, organizations, locations)
- Temporal expression extraction
- Numerical values and measurements
- Entity tracking across dialogue turns
- Coreference chain management
"""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from ibdm.nlu.llm_adapter import LLMAdapter, LLMConfig, ModelType

logger = logging.getLogger(__name__)


class EntityType(str, Enum):
    """Types of entities that can be extracted."""

    PERSON = "person"
    ORGANIZATION = "organization"
    LOCATION = "location"
    TEMPORAL = "temporal"
    NUMERICAL = "numerical"
    MEASUREMENT = "measurement"
    OBJECT = "object"
    EVENT = "event"
    OTHER = "other"


class Entity(BaseModel):
    """An extracted entity.

    Attributes:
        text: The entity text as it appears in the utterance
        type: The entity type
        canonical_form: Normalized/canonical form of the entity
        properties: Additional properties (e.g., value for numerical entities)
        mention_id: Unique ID for this mention
        entity_id: ID of the underlying entity (for coreference)
        confidence: Extraction confidence
    """

    text: str = Field(..., description="Entity text from utterance")
    type: str = Field(..., description="Entity type")
    canonical_form: str | None = Field(default=None, description="Canonical form")
    properties: dict[str, Any] = Field(default_factory=dict, description="Additional properties")
    mention_id: str = Field(..., description="Unique mention ID")
    entity_id: str | None = Field(default=None, description="Entity ID for coreference")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")


class EntityExtractionResult(BaseModel):
    """Result of entity extraction.

    Attributes:
        entities: List of extracted entities
        utterance: Original utterance
        confidence: Overall extraction confidence
    """

    entities: list[Entity] = Field(default_factory=list, description="Extracted entities")
    utterance: str = Field(..., description="Original utterance")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Overall confidence")


@dataclass
class EntityExtractorConfig:
    """Configuration for entity extractor.

    Attributes:
        llm_config: Configuration for the LLM adapter
        extract_persons: Enable person extraction
        extract_organizations: Enable organization extraction
        extract_locations: Enable location extraction
        extract_temporal: Enable temporal expression extraction
        extract_numerical: Enable numerical value extraction
        use_fast_model: Whether to use Haiku instead of Sonnet
        confidence_threshold: Minimum confidence for extraction
    """

    llm_config: LLMConfig | None = None
    extract_persons: bool = True
    extract_organizations: bool = True
    extract_locations: bool = True
    extract_temporal: bool = True
    extract_numerical: bool = True
    use_fast_model: bool = True  # Entity extraction is fast, use Haiku
    confidence_threshold: float = 0.5


class EntityExtractor:
    """LLM-based entity extractor.

    Extracts named entities, temporal expressions, and numerical values from
    utterances using LLM-based understanding.

    Example:
        >>> extractor = EntityExtractor()
        >>> result = extractor.extract("Alice went to Stockholm yesterday.")
        >>> for entity in result.entities:
        ...     print(f"{entity.text} ({entity.type})")
        Alice (person)
        Stockholm (location)
        yesterday (temporal)
    """

    def __init__(self, config: EntityExtractorConfig | None = None):
        """Initialize the entity extractor.

        Args:
            config: Extractor configuration. Uses defaults if not provided.
        """
        self.config = config or EntityExtractorConfig()

        # Configure LLM - use Haiku by default for fast extraction
        llm_config = self.config.llm_config or LLMConfig(
            model=ModelType.HAIKU if self.config.use_fast_model else ModelType.SONNET,
            temperature=0.2,  # Low temperature for consistent extraction
            max_tokens=1000,
        )
        self.llm = LLMAdapter(llm_config)

        # Mention counter for unique IDs
        self._mention_counter = 0

        logger.info("Entity extractor initialized")

    def extract(
        self, utterance: str, context: dict[str, Any] | None = None
    ) -> EntityExtractionResult:
        """Extract entities from an utterance.

        Args:
            utterance: The utterance to extract entities from
            context: Optional context (previous entities, domain info)

        Returns:
            EntityExtractionResult with extracted entities

        Raises:
            ValueError: If utterance is empty
        """
        if not utterance or not utterance.strip():
            raise ValueError("Utterance cannot be empty")

        logger.info(f"Extracting entities from: '{utterance}'")

        # Build extraction prompt
        prompt = self._build_extraction_prompt(utterance, context)
        system_prompt = self._build_system_prompt()

        try:
            # Call LLM for structured extraction
            result = self.llm.call_structured(
                prompt=prompt,
                response_model=EntityExtractionResult,
                system_prompt=system_prompt,
            )

            # Assign unique mention IDs
            for entity in result.entities:
                if not entity.mention_id or entity.mention_id == "":
                    entity.mention_id = self._generate_mention_id()

            # Filter by confidence threshold
            result.entities = [
                e for e in result.entities if e.confidence >= self.config.confidence_threshold
            ]

            logger.info(f"Extracted {len(result.entities)} entities")
            return result

        except Exception as e:
            logger.warning(f"Entity extraction failed: {e}")
            # Return empty result on failure
            return EntityExtractionResult(utterance=utterance, confidence=0.0)

    async def aextract(
        self, utterance: str, context: dict[str, Any] | None = None
    ) -> EntityExtractionResult:
        """Extract entities asynchronously.

        Args:
            utterance: The utterance to extract entities from
            context: Optional context

        Returns:
            EntityExtractionResult with extracted entities
        """
        if not utterance or not utterance.strip():
            raise ValueError("Utterance cannot be empty")

        prompt = self._build_extraction_prompt(utterance, context)
        system_prompt = self._build_system_prompt()

        try:
            result = await self.llm.acall_structured(
                prompt=prompt,
                response_model=EntityExtractionResult,
                system_prompt=system_prompt,
            )

            # Assign unique mention IDs
            for entity in result.entities:
                if not entity.mention_id or entity.mention_id == "":
                    entity.mention_id = self._generate_mention_id()

            # Filter by confidence
            result.entities = [
                e for e in result.entities if e.confidence >= self.config.confidence_threshold
            ]

            return result

        except Exception as e:
            logger.warning(f"Async entity extraction failed: {e}")
            return EntityExtractionResult(utterance=utterance, confidence=0.0)

    async def batch_extract(
        self, utterances: list[str], context: dict[str, Any] | None = None
    ) -> list[EntityExtractionResult]:
        """Extract entities from multiple utterances in parallel.

        Args:
            utterances: List of utterances
            context: Optional context

        Returns:
            List of EntityExtractionResult objects
        """
        import asyncio

        tasks = [self.aextract(utt, context) for utt in utterances]
        return await asyncio.gather(*tasks)

    def _build_extraction_prompt(self, utterance: str, context: dict[str, Any] | None) -> str:
        """Build extraction prompt.

        Args:
            utterance: The utterance
            context: Optional context

        Returns:
            Prompt string
        """
        prompt_parts = [f"Extract entities from the following utterance:\n\n{utterance}\n"]

        if context:
            if "domain" in context:
                prompt_parts.append(f"\nDomain: {context['domain']}")
            if "previous_entities" in context:
                prompt_parts.append("\nPrevious entities mentioned:")
                for ent in context["previous_entities"][:5]:  # Last 5
                    prompt_parts.append(f"- {ent}")

        prompt_parts.append(
            "\nFor each entity, provide:\n"
            "- text: The exact text from the utterance\n"
            "- type: Entity type (person, organization, location, temporal, numerical, etc.)\n"
            "- canonical_form: Normalized form (optional)\n"
            "- properties: Additional properties (optional)\n"
            "- mention_id: Unique ID for this mention (generate as 'm_N')\n"
            "- confidence: Your confidence (0.0-1.0)\n"
        )

        return "\n".join(prompt_parts)

    def _build_system_prompt(self) -> str:
        """Build system prompt for entity extraction.

        Returns:
            System prompt string
        """
        entity_types = []
        if self.config.extract_persons:
            entity_types.append("persons")
        if self.config.extract_organizations:
            entity_types.append("organizations")
        if self.config.extract_locations:
            entity_types.append("locations")
        if self.config.extract_temporal:
            entity_types.append("temporal expressions")
        if self.config.extract_numerical:
            entity_types.append("numerical values and measurements")

        types_str = ", ".join(entity_types)

        return (
            f"You are an expert entity extraction system. Extract {types_str} "
            "from utterances. Provide accurate entity types and high confidence scores "
            "for clear entities, lower scores for ambiguous ones. "
            "For temporal expressions, extract relative times (yesterday, tomorrow) "
            "and absolute dates. For numerical values, include the value in properties."
        )

    def _generate_mention_id(self) -> str:
        """Generate unique mention ID.

        Returns:
            Mention ID
        """
        self._mention_counter += 1
        return f"m_{self._mention_counter}"


@dataclass
class EntityTrackerConfig:
    """Configuration for entity tracker.

    Attributes:
        max_history: Maximum number of utterances to track
        coref_confidence_threshold: Minimum confidence for coreference
    """

    max_history: int = 50
    coref_confidence_threshold: float = 0.6


class EntityTracker:
    """Tracks entities across dialogue turns.

    Maintains a database of entities mentioned in the dialogue and manages
    coreference chains to track which mentions refer to the same entity.

    Example:
        >>> tracker = EntityTracker()
        >>> extractor = EntityExtractor()
        >>>
        >>> # First utterance
        >>> result1 = extractor.extract("Alice went to Stockholm.")
        >>> tracker.update(result1.entities)
        >>>
        >>> # Second utterance
        >>> result2 = extractor.extract("She arrived yesterday.")
        >>> tracker.update(result2.entities)
        >>>
        >>> # Get entity database
        >>> entities = tracker.get_all_entities()
    """

    def __init__(self, config: EntityTrackerConfig | None = None):
        """Initialize the entity tracker.

        Args:
            config: Tracker configuration. Uses defaults if not provided.
        """
        self.config = config or EntityTrackerConfig()

        # Entity database: entity_id -> Entity
        self._entities: dict[str, Entity] = {}

        # Coreference chains: entity_id -> list[mention_id]
        self._coref_chains: dict[str, list[str]] = {}

        # Mention history: list of (utterance_index, entity)
        self._mention_history: list[tuple[int, Entity]] = []

        # Utterance counter
        self._utterance_counter = 0

        # Entity ID counter
        self._entity_counter = 0

        logger.info("Entity tracker initialized")

    def update(self, entities: list[Entity], resolve_coref: bool = True) -> None:
        """Update tracker with new entities.

        Args:
            entities: List of entities from current utterance
            resolve_coref: Whether to attempt coreference resolution
        """
        self._utterance_counter += 1

        for entity in entities:
            # Assign entity ID if not already assigned
            if not entity.entity_id:
                if resolve_coref:
                    # Try to resolve to existing entity
                    entity_id = self._resolve_coreference(entity)
                    entity.entity_id = entity_id
                else:
                    # Create new entity
                    entity.entity_id = self._generate_entity_id()

            # Add to entity database
            self._entities[entity.entity_id] = entity

            # Update coreference chain
            if entity.entity_id not in self._coref_chains:
                self._coref_chains[entity.entity_id] = []
            self._coref_chains[entity.entity_id].append(entity.mention_id)

            # Add to mention history
            self._mention_history.append((self._utterance_counter, entity))

            # Trim history if needed
            if len(self._mention_history) > self.config.max_history:
                self._mention_history = self._mention_history[-self.config.max_history :]

        logger.info(
            f"Updated tracker with {len(entities)} entities. "
            f"Total entities: {len(self._entities)}, "
            f"Total mentions: {len(self._mention_history)}"
        )

    def get_all_entities(self) -> list[Entity]:
        """Get all tracked entities.

        Returns:
            List of all entities
        """
        return list(self._entities.values())

    def get_entity_by_id(self, entity_id: str) -> Entity | None:
        """Get entity by ID.

        Args:
            entity_id: The entity ID

        Returns:
            Entity or None if not found
        """
        return self._entities.get(entity_id)

    def get_coref_chain(self, entity_id: str) -> list[str]:
        """Get coreference chain for an entity.

        Args:
            entity_id: The entity ID

        Returns:
            List of mention IDs in the coreference chain
        """
        return self._coref_chains.get(entity_id, [])

    def get_recent_entities(self, n: int = 10, entity_type: str | None = None) -> list[Entity]:
        """Get recently mentioned entities.

        Args:
            n: Number of recent entities to return
            entity_type: Optional filter by entity type

        Returns:
            List of recent entities
        """
        # Get recent mentions
        recent_mentions = self._mention_history[-n:]

        # Extract entities
        entities = [ent for _, ent in recent_mentions]

        # Filter by type if specified
        if entity_type:
            entities = [e for e in entities if e.type == entity_type]

        return entities

    def _resolve_coreference(self, entity: Entity) -> str:
        """Resolve coreference for an entity.

        Simple rule-based coreference using text matching and recency.
        In a more sophisticated system, this would use LLM-based coreference.

        Args:
            entity: The entity to resolve

        Returns:
            Entity ID (existing or new)
        """
        # Get recent entities of the same type
        recent = self.get_recent_entities(n=5, entity_type=entity.type)

        # Try to match based on text similarity
        for recent_entity in reversed(recent):  # Most recent first
            if self._entities_match(entity, recent_entity):
                logger.debug(f"Resolved coreference: {entity.text} -> {recent_entity.entity_id}")
                return recent_entity.entity_id  # type: ignore[return-value]

        # No match found, create new entity
        return self._generate_entity_id()

    def _entities_match(self, entity1: Entity, entity2: Entity) -> bool:
        """Check if two entities refer to the same thing.

        Simple heuristic based on text matching.

        Args:
            entity1: First entity
            entity2: Second entity

        Returns:
            True if entities match
        """
        # Must be same type
        if entity1.type != entity2.type:
            return False

        # Exact text match
        if entity1.text.lower() == entity2.text.lower():
            return True

        # Canonical form match
        if (
            entity1.canonical_form
            and entity2.canonical_form
            and entity1.canonical_form.lower() == entity2.canonical_form.lower()
        ):
            return True

        # Substring match for names (e.g., "Alice" matches "Alice Johnson")
        text1 = entity1.text.lower()
        text2 = entity2.text.lower()
        if entity1.type == EntityType.PERSON:
            if text1 in text2 or text2 in text1:
                return True

        return False

    def _generate_entity_id(self) -> str:
        """Generate unique entity ID.

        Returns:
            Entity ID
        """
        self._entity_counter += 1
        return f"e_{self._entity_counter}"

    def clear(self) -> None:
        """Clear all tracked entities."""
        self._entities.clear()
        self._coref_chains.clear()
        self._mention_history.clear()
        self._utterance_counter = 0
        self._entity_counter = 0
        logger.info("Entity tracker cleared")


def create_extractor(
    use_fast_model: bool = True,
    extract_persons: bool = True,
    extract_locations: bool = True,
    extract_temporal: bool = True,
) -> EntityExtractor:
    """Convenience function to create an entity extractor.

    Args:
        use_fast_model: Use Haiku (True) or Sonnet (False)
        extract_persons: Enable person extraction
        extract_locations: Enable location extraction
        extract_temporal: Enable temporal expression extraction

    Returns:
        Configured EntityExtractor instance

    Example:
        >>> # Fast extractor for persons and locations
        >>> extractor = create_extractor(use_fast_model=True)
        >>>
        >>> # Detailed extractor with all entity types
        >>> extractor = create_extractor(use_fast_model=False)
    """
    config = EntityExtractorConfig(
        use_fast_model=use_fast_model,
        extract_persons=extract_persons,
        extract_locations=extract_locations,
        extract_temporal=extract_temporal,
    )

    return EntityExtractor(config)


def create_tracker(max_history: int = 50) -> EntityTracker:
    """Convenience function to create an entity tracker.

    Args:
        max_history: Maximum number of utterances to track

    Returns:
        Configured EntityTracker instance

    Example:
        >>> tracker = create_tracker(max_history=100)
    """
    config = EntityTrackerConfig(max_history=max_history)
    return EntityTracker(config)
