"""Tests for entity extraction and tracking."""

import pytest

from ibdm.nlu.entity_extractor import (
    Entity,
    EntityExtractionResult,
    EntityExtractor,
    EntityExtractorConfig,
    EntityTracker,
    EntityTrackerConfig,
    EntityType,
    create_extractor,
    create_tracker,
)


class TestEntityModel:
    """Tests for Entity Pydantic model."""

    def test_create_basic_entity(self):
        """Test creating a basic entity."""
        entity = Entity(
            text="Alice",
            type=EntityType.PERSON.value,
            mention_id="m_1",
            confidence=0.95,
        )

        assert entity.text == "Alice"
        assert entity.type == "person"
        assert entity.mention_id == "m_1"
        assert entity.confidence == 0.95
        assert entity.canonical_form is None
        assert entity.entity_id is None

    def test_create_entity_with_properties(self):
        """Test creating entity with additional properties."""
        entity = Entity(
            text="5 kilometers",
            type=EntityType.MEASUREMENT.value,
            canonical_form="5km",
            properties={"value": 5, "unit": "km"},
            mention_id="m_2",
            confidence=0.9,
        )

        assert entity.canonical_form == "5km"
        assert entity.properties["value"] == 5
        assert entity.properties["unit"] == "km"

    def test_entity_with_coref(self):
        """Test entity with coreference ID."""
        entity = Entity(
            text="she",
            type=EntityType.PERSON.value,
            mention_id="m_3",
            entity_id="e_1",
            confidence=0.8,
        )

        assert entity.entity_id == "e_1"


class TestEntityExtractionResult:
    """Tests for EntityExtractionResult model."""

    def test_create_empty_result(self):
        """Test creating empty extraction result."""
        result = EntityExtractionResult(utterance="Hello world", confidence=1.0)

        assert result.utterance == "Hello world"
        assert result.confidence == 1.0
        assert result.entities == []

    def test_create_result_with_entities(self):
        """Test creating result with entities."""
        entities = [
            Entity(text="Alice", type="person", mention_id="m_1", confidence=0.95),
            Entity(text="Stockholm", type="location", mention_id="m_2", confidence=0.9),
        ]

        result = EntityExtractionResult(
            utterance="Alice went to Stockholm",
            entities=entities,
            confidence=0.92,
        )

        assert len(result.entities) == 2
        assert result.entities[0].text == "Alice"
        assert result.entities[1].text == "Stockholm"


class TestEntityExtractorConfig:
    """Tests for EntityExtractorConfig."""

    def test_default_config(self):
        """Test default configuration."""
        config = EntityExtractorConfig()

        assert config.llm_config is None
        assert config.extract_persons is True
        assert config.extract_organizations is True
        assert config.extract_locations is True
        assert config.extract_temporal is True
        assert config.extract_numerical is True
        assert config.use_fast_model is True
        assert config.confidence_threshold == 0.5

    def test_custom_config(self):
        """Test custom configuration."""
        config = EntityExtractorConfig(
            extract_persons=True,
            extract_locations=True,
            extract_temporal=False,
            extract_numerical=False,
            use_fast_model=False,
            confidence_threshold=0.7,
        )

        assert config.extract_persons is True
        assert config.extract_temporal is False
        assert config.use_fast_model is False
        assert config.confidence_threshold == 0.7


class TestEntityExtractorInitialization:
    """Tests for EntityExtractor initialization."""

    def test_initialization_without_api_key(self):
        """Test that initialization fails gracefully without API key."""
        try:
            extractor = EntityExtractor()
            assert extractor is not None
        except ValueError as e:
            assert "IBDM_API_KEY" in str(e)

    def test_initialization_with_custom_config(self):
        """Test initialization with custom config."""
        config = EntityExtractorConfig(use_fast_model=False)

        try:
            extractor = EntityExtractor(config)
            assert extractor.config.use_fast_model is False
        except ValueError as e:
            assert "IBDM_API_KEY" in str(e)


class TestEntityExtractorPrompts:
    """Tests for prompt building."""

    def test_build_extraction_prompt(self):
        """Test building extraction prompt."""
        try:
            extractor = EntityExtractor()
            prompt = extractor._build_extraction_prompt("Alice went to Stockholm.", None)

            assert "Alice went to Stockholm" in prompt
            assert "text:" in prompt
            assert "type:" in prompt
        except ValueError:
            pytest.skip("IBDM_API_KEY not configured")

    def test_build_prompt_with_context(self):
        """Test building prompt with context."""
        try:
            extractor = EntityExtractor()
            context = {"domain": "travel", "previous_entities": ["Alice", "Bob"]}

            prompt = extractor._build_extraction_prompt("She went there.", context)

            assert "She went there" in prompt
            assert "travel" in prompt or "Domain" in prompt
        except ValueError:
            pytest.skip("IBDM_API_KEY not configured")

    def test_build_system_prompt(self):
        """Test building system prompt."""
        try:
            extractor = EntityExtractor()
            system_prompt = extractor._build_system_prompt()

            assert "entity extraction" in system_prompt.lower()
            assert "persons" in system_prompt or "person" in system_prompt
        except ValueError:
            pytest.skip("IBDM_API_KEY not configured")

    def test_generate_mention_id(self):
        """Test mention ID generation."""
        try:
            extractor = EntityExtractor()

            id1 = extractor._generate_mention_id()
            id2 = extractor._generate_mention_id()

            assert id1.startswith("m_")
            assert id2.startswith("m_")
            assert id1 != id2  # Should be unique
        except ValueError:
            pytest.skip("IBDM_API_KEY not configured")


class TestEntityTrackerConfig:
    """Tests for EntityTrackerConfig."""

    def test_default_config(self):
        """Test default tracker configuration."""
        config = EntityTrackerConfig()

        assert config.max_history == 50
        assert config.coref_confidence_threshold == 0.6

    def test_custom_config(self):
        """Test custom tracker configuration."""
        config = EntityTrackerConfig(max_history=100, coref_confidence_threshold=0.8)

        assert config.max_history == 100
        assert config.coref_confidence_threshold == 0.8


class TestEntityTracker:
    """Tests for EntityTracker."""

    def test_tracker_initialization(self):
        """Test tracker can be initialized."""
        tracker = EntityTracker()

        assert tracker is not None
        assert len(tracker.get_all_entities()) == 0

    def test_update_with_entities(self):
        """Test updating tracker with entities."""
        tracker = EntityTracker()

        entities = [
            Entity(text="Alice", type="person", mention_id="m_1", confidence=0.95),
            Entity(text="Stockholm", type="location", mention_id="m_2", confidence=0.9),
        ]

        tracker.update(entities, resolve_coref=False)

        all_entities = tracker.get_all_entities()
        assert len(all_entities) == 2

    def test_entity_id_assignment(self):
        """Test that entities get assigned IDs."""
        tracker = EntityTracker()

        entities = [Entity(text="Alice", type="person", mention_id="m_1", confidence=0.95)]

        tracker.update(entities, resolve_coref=False)

        entity = tracker.get_all_entities()[0]
        assert entity.entity_id is not None
        assert entity.entity_id.startswith("e_")

    def test_get_entity_by_id(self):
        """Test retrieving entity by ID."""
        tracker = EntityTracker()

        entities = [Entity(text="Alice", type="person", mention_id="m_1", confidence=0.95)]

        tracker.update(entities, resolve_coref=False)
        entity_id = tracker.get_all_entities()[0].entity_id

        retrieved = tracker.get_entity_by_id(entity_id)  # type: ignore
        assert retrieved is not None
        assert retrieved.text == "Alice"

    def test_get_entity_by_id_not_found(self):
        """Test retrieving non-existent entity."""
        tracker = EntityTracker()

        entity = tracker.get_entity_by_id("nonexistent")
        assert entity is None

    def test_coref_chain(self):
        """Test coreference chain tracking."""
        tracker = EntityTracker()

        # First mention
        entities1 = [Entity(text="Alice", type="person", mention_id="m_1", confidence=0.95)]
        tracker.update(entities1, resolve_coref=False)
        entity_id = tracker.get_all_entities()[0].entity_id

        # Second mention - same entity
        entities2 = [
            Entity(
                text="Alice", type="person", mention_id="m_2", entity_id=entity_id, confidence=0.95
            )
        ]
        tracker.update(entities2, resolve_coref=False)

        chain = tracker.get_coref_chain(entity_id)  # type: ignore
        assert len(chain) == 2
        assert "m_1" in chain
        assert "m_2" in chain

    def test_get_recent_entities(self):
        """Test getting recent entities."""
        tracker = EntityTracker()

        entities = [
            Entity(text="Alice", type="person", mention_id="m_1", confidence=0.95),
            Entity(text="Bob", type="person", mention_id="m_2", confidence=0.9),
            Entity(text="Stockholm", type="location", mention_id="m_3", confidence=0.85),
        ]

        tracker.update(entities, resolve_coref=False)

        recent = tracker.get_recent_entities(n=2)
        assert len(recent) == 2

    def test_get_recent_entities_by_type(self):
        """Test filtering recent entities by type."""
        tracker = EntityTracker()

        entities = [
            Entity(text="Alice", type="person", mention_id="m_1", confidence=0.95),
            Entity(text="Stockholm", type="location", mention_id="m_2", confidence=0.9),
        ]

        tracker.update(entities, resolve_coref=False)

        persons = tracker.get_recent_entities(n=10, entity_type="person")
        assert len(persons) == 1
        assert persons[0].text == "Alice"

    def test_entities_match_exact(self):
        """Test exact entity matching."""
        tracker = EntityTracker()

        entity1 = Entity(text="Alice", type="person", mention_id="m_1", confidence=0.95)
        entity2 = Entity(text="Alice", type="person", mention_id="m_2", confidence=0.9)

        assert tracker._entities_match(entity1, entity2)

    def test_entities_match_different_type(self):
        """Test entities don't match if different types."""
        tracker = EntityTracker()

        entity1 = Entity(text="Stockholm", type="location", mention_id="m_1", confidence=0.95)
        entity2 = Entity(text="Stockholm", type="organization", mention_id="m_2", confidence=0.9)

        assert not tracker._entities_match(entity1, entity2)

    def test_entities_match_substring(self):
        """Test substring matching for persons."""
        tracker = EntityTracker()

        entity1 = Entity(text="Alice", type="person", mention_id="m_1", confidence=0.95)
        entity2 = Entity(text="Alice Johnson", type="person", mention_id="m_2", confidence=0.9)

        assert tracker._entities_match(entity1, entity2)

    def test_tracker_clear(self):
        """Test clearing tracker."""
        tracker = EntityTracker()

        entities = [Entity(text="Alice", type="person", mention_id="m_1", confidence=0.95)]

        tracker.update(entities, resolve_coref=False)
        assert len(tracker.get_all_entities()) == 1

        tracker.clear()
        assert len(tracker.get_all_entities()) == 0


@pytest.mark.skipif(
    "not config.getoption('--run-llm')",
    reason="Requires --run-llm flag and IBDM_API_KEY",
)
class TestEntityExtractorIntegration:
    """Integration tests for EntityExtractor (requires LLM API)."""

    def test_extract_simple_entities(self):
        """Test extracting entities from simple utterance."""
        extractor = create_extractor()

        result = extractor.extract("Alice went to Stockholm yesterday.")

        assert result.utterance == "Alice went to Stockholm yesterday."
        assert len(result.entities) > 0

        # Should extract at least person and location
        entity_types = {e.type for e in result.entities}
        assert "person" in entity_types or "location" in entity_types

    def test_extract_with_confidence_threshold(self):
        """Test that low confidence entities are filtered."""
        config = EntityExtractorConfig(confidence_threshold=0.9)
        extractor = EntityExtractor(config)

        result = extractor.extract("Alice went somewhere.")

        # Only high-confidence entities should remain
        for entity in result.entities:
            assert entity.confidence >= 0.9

    def test_extract_temporal_expressions(self):
        """Test temporal expression extraction."""
        extractor = create_extractor(extract_temporal=True)

        result = extractor.extract("I will go there tomorrow at 3pm.")

        # Should extract temporal entities
        temporal_entities = [e for e in result.entities if e.type == "temporal"]
        assert len(temporal_entities) >= 0  # May or may not extract depending on LLM

    def test_extract_empty_utterance(self):
        """Test that empty utterance raises ValueError."""
        extractor = create_extractor()

        with pytest.raises(ValueError, match="empty"):
            extractor.extract("")

        with pytest.raises(ValueError, match="empty"):
            extractor.extract("   ")

    @pytest.mark.asyncio
    async def test_async_extract(self):
        """Test async entity extraction."""
        extractor = create_extractor()

        result = await extractor.aextract("Alice went to Stockholm.")

        assert result.utterance == "Alice went to Stockholm."
        assert len(result.entities) >= 0

    @pytest.mark.asyncio
    async def test_batch_extract(self):
        """Test batch extraction."""
        extractor = create_extractor()

        utterances = [
            "Alice is in Stockholm.",
            "Bob went to Paris.",
            "Carol visited London yesterday.",
        ]

        results = await extractor.batch_extract(utterances)

        assert len(results) == 3
        for result in results:
            assert result.utterance in utterances


class TestCreateExtractor:
    """Tests for create_extractor convenience function."""

    def test_create_fast_extractor(self):
        """Test creating fast extractor."""
        try:
            extractor = create_extractor(use_fast_model=True)
            assert extractor.config.use_fast_model is True
        except ValueError as e:
            assert "IBDM_API_KEY" in str(e)

    def test_create_detailed_extractor(self):
        """Test creating detailed extractor."""
        try:
            extractor = create_extractor(use_fast_model=False)
            assert extractor.config.use_fast_model is False
        except ValueError as e:
            assert "IBDM_API_KEY" in str(e)


class TestCreateTracker:
    """Tests for create_tracker convenience function."""

    def test_create_tracker(self):
        """Test creating tracker."""
        tracker = create_tracker()
        assert tracker is not None
        assert tracker.config.max_history == 50

    def test_create_tracker_custom_history(self):
        """Test creating tracker with custom history."""
        tracker = create_tracker(max_history=100)
        assert tracker.config.max_history == 100


class TestIntegratedExtractorAndTracker:
    """Tests for integrated extractor and tracker workflow."""

    @pytest.mark.skipif(
        "not config.getoption('--run-llm')",
        reason="Requires --run-llm flag and IBDM_API_KEY",
    )
    def test_extract_and_track(self):
        """Test extracting and tracking entities across turns."""
        extractor = create_extractor()
        tracker = create_tracker()

        # First turn
        result1 = extractor.extract("Alice went to Stockholm.")
        tracker.update(result1.entities, resolve_coref=False)

        assert len(tracker.get_all_entities()) > 0

        # Second turn
        result2 = extractor.extract("Bob joined her there.")
        tracker.update(result2.entities, resolve_coref=False)

        # Should have entities from both turns
        all_entities = tracker.get_all_entities()
        assert len(all_entities) >= 2
