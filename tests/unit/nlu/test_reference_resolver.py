"""Tests for reference resolution module."""

import pytest

from ibdm.core.information_state import InformationState
from ibdm.core.questions import WhQuestion
from ibdm.nlu.entity_extractor import Entity, EntityTracker, EntityType
from ibdm.nlu.reference_resolver import (
    Reference,
    ReferenceResolution,
    ReferenceResolver,
    ReferenceResolverConfig,
    ReferenceType,
    create_resolver,
)


class TestReferenceType:
    """Tests for ReferenceType enum."""

    def test_reference_types_exist(self):
        """Test that all reference types are defined."""
        assert ReferenceType.PRONOUN.value == "pronoun"
        assert ReferenceType.DEMONSTRATIVE.value == "demonstrative"
        assert ReferenceType.DEFINITE_DESCRIPTION.value == "definite_description"
        assert ReferenceType.ONE_ANAPHORA.value == "one_anaphora"
        assert ReferenceType.POSSESSIVE.value == "possessive"
        assert ReferenceType.OTHER.value == "other"


class TestReference:
    """Tests for Reference Pydantic model."""

    def test_create_basic_reference(self):
        """Test creating a basic reference."""
        ref = Reference(
            text="she",
            type=ReferenceType.PRONOUN.value,
            index=0,
        )

        assert ref.text == "she"
        assert ref.type == "pronoun"
        assert ref.index == 0
        assert ref.properties == {}

    def test_create_reference_with_properties(self):
        """Test creating reference with properties."""
        ref = Reference(
            text="he",
            type=ReferenceType.PRONOUN.value,
            index=2,
            properties={"number": "singular", "gender": "masculine"},
        )

        assert ref.properties["number"] == "singular"
        assert ref.properties["gender"] == "masculine"


class TestReferenceResolution:
    """Tests for ReferenceResolution model."""

    def test_create_empty_resolution(self):
        """Test creating unresolved reference resolution."""
        ref = Reference(text="it", type="pronoun", index=0)
        resolution = ReferenceResolution(
            reference=ref,
            confidence=0.0,
        )

        assert resolution.reference == ref
        assert resolution.resolved_entity is None
        assert resolution.candidates == []
        assert resolution.confidence == 0.0
        assert resolution.ambiguous is False

    def test_create_resolved_reference(self):
        """Test creating resolved reference."""
        ref = Reference(text="she", type="pronoun", index=0)
        entity = Entity(text="Alice", type="person", mention_id="m_1", confidence=0.95)

        resolution = ReferenceResolution(
            reference=ref,
            resolved_entity=entity,
            confidence=0.9,
        )

        assert resolution.resolved_entity == entity
        assert resolution.confidence == 0.9

    def test_create_ambiguous_resolution(self):
        """Test creating ambiguous resolution."""
        ref = Reference(text="she", type="pronoun", index=0)
        candidates = [
            {
                "entity": Entity(text="Alice", type="person", mention_id="m_1", confidence=0.9),
                "score": 0.8,
            },
            {
                "entity": Entity(text="Bob", type="person", mention_id="m_2", confidence=0.9),
                "score": 0.75,
            },
        ]

        resolution = ReferenceResolution(
            reference=ref,
            candidates=candidates,
            confidence=0.8,
            ambiguous=True,
        )

        assert resolution.ambiguous is True
        assert len(resolution.candidates) == 2


class TestReferenceResolverConfig:
    """Tests for ReferenceResolverConfig."""

    def test_default_config(self):
        """Test default configuration."""
        config = ReferenceResolverConfig()

        assert config.use_llm is True
        assert config.salience_recency_weight == 0.6
        assert config.salience_syntactic_weight == 0.4
        assert config.ambiguity_threshold == 0.2
        assert config.confidence_threshold == 0.5

    def test_custom_config(self):
        """Test custom configuration."""
        config = ReferenceResolverConfig(
            use_llm=False,
            salience_recency_weight=0.7,
            ambiguity_threshold=0.3,
        )

        assert config.use_llm is False
        assert config.salience_recency_weight == 0.7
        assert config.ambiguity_threshold == 0.3


class TestReferenceResolver:
    """Tests for ReferenceResolver."""

    @pytest.fixture
    def tracker(self):
        """Create an entity tracker with some entities."""
        tracker = EntityTracker()

        # Add some entities in order
        entities1 = [
            Entity(text="Alice", type=EntityType.PERSON.value, mention_id="m_1", confidence=0.95),
        ]
        tracker.update(entities1)

        entities2 = [
            Entity(text="Bob", type=EntityType.PERSON.value, mention_id="m_2", confidence=0.9),
        ]
        tracker.update(entities2)

        return tracker

    @pytest.fixture
    def state(self):
        """Create a basic information state."""
        return InformationState()

    @pytest.fixture
    def resolver(self, tracker):
        """Create a reference resolver without LLM."""
        config = ReferenceResolverConfig(use_llm=False)
        return ReferenceResolver(tracker, config)

    def test_create_resolver(self, tracker):
        """Test creating a reference resolver."""
        config = ReferenceResolverConfig(use_llm=False)
        resolver = ReferenceResolver(tracker, config)

        assert resolver.entity_tracker == tracker
        assert resolver.config == config
        assert resolver.llm is None

    def test_create_resolver_factory(self, tracker):
        """Test creating resolver with factory function."""
        resolver = create_resolver(tracker, use_llm=False)

        assert isinstance(resolver, ReferenceResolver)
        assert resolver.entity_tracker == tracker

    def test_resolve_pronoun_to_person(self, resolver, tracker, state):
        """Test resolving pronoun to person entity."""
        # Add a person entity
        entities = [
            Entity(text="Alice", type=EntityType.PERSON.value, mention_id="m_3", confidence=0.95),
        ]
        tracker.update(entities)

        # Resolve "she"
        ref = Reference(text="she", type=ReferenceType.PRONOUN.value, index=0)
        resolution = resolver.resolve(ref, state)

        assert resolution.resolved_entity is not None
        assert resolution.resolved_entity.text == "Alice"
        assert resolution.confidence >= 0.5

    def test_resolve_pronoun_no_candidates(self, resolver, state):
        """Test resolving pronoun with no candidate entities."""
        # Clear tracker by creating new one
        empty_tracker = EntityTracker()
        resolver_empty = ReferenceResolver(
            empty_tracker,
            ReferenceResolverConfig(use_llm=False),
        )

        ref = Reference(text="she", type=ReferenceType.PRONOUN.value, index=0)
        resolution = resolver_empty.resolve(ref, state)

        assert resolution.resolved_entity is None
        assert resolution.confidence == 0.0

    def test_resolve_it_pronoun(self, resolver, tracker, state):
        """Test resolving 'it' pronoun to non-person entity."""
        # Add a location entity
        entities = [
            Entity(text="Paris", type=EntityType.LOCATION.value, mention_id="m_4", confidence=0.9),
        ]
        tracker.update(entities)

        ref = Reference(text="it", type=ReferenceType.PRONOUN.value, index=0)
        resolution = resolver.resolve(ref, state)

        assert resolution.resolved_entity is not None
        assert resolution.resolved_entity.text == "Paris"

    def test_resolve_demonstrative(self):
        """Test resolving demonstrative reference."""
        # Create fresh tracker and resolver
        tracker = EntityTracker()
        config = ReferenceResolverConfig(use_llm=False)
        resolver = ReferenceResolver(tracker, config)
        state = InformationState()

        # Add an entity
        entities = [
            Entity(text="laptop", type=EntityType.OTHER.value, mention_id="m_5", confidence=0.9),
        ]
        tracker.update(entities)

        ref = Reference(text="this", type=ReferenceType.DEMONSTRATIVE.value, index=0)
        resolution = resolver.resolve(ref, state)

        assert resolution.resolved_entity is not None
        assert resolution.resolved_entity.text == "laptop"

    def test_resolve_definite_description(self, resolver, tracker, state):
        """Test resolving definite description."""
        # Add an entity
        entities = [
            Entity(text="Alice", type=EntityType.PERSON.value, mention_id="m_6", confidence=0.95),
        ]
        tracker.update(entities)

        ref = Reference(
            text="the person",
            type=ReferenceType.DEFINITE_DESCRIPTION.value,
            index=0,
        )
        resolution = resolver.resolve(ref, state)

        assert resolution.resolved_entity is not None
        assert resolution.resolved_entity.text == "Alice"

    def test_resolve_with_recency_preference(self):
        """Test resolution with multiple candidates."""
        # Create fresh tracker and resolver
        tracker = EntityTracker()
        config = ReferenceResolverConfig(use_llm=False)
        resolver = ReferenceResolver(tracker, config)
        state = InformationState()

        # Add two person entities at different times (use different entity_ids)
        entities1 = [
            Entity(
                text="Alice",
                type=EntityType.PERSON.value,
                mention_id="m_7",
                entity_id="person_1",
                confidence=0.9,
            ),
        ]
        tracker.update(entities1, resolve_coref=False)

        entities2 = [
            Entity(
                text="Carol",
                type=EntityType.PERSON.value,
                mention_id="m_8",
                entity_id="person_2",
                confidence=0.9,
            ),
        ]
        tracker.update(entities2, resolve_coref=False)

        # Resolve "she"
        ref = Reference(text="she", type=ReferenceType.PRONOUN.value, index=0)
        resolution = resolver.resolve(ref, state)

        assert resolution.resolved_entity is not None
        # Should resolve to one of the person entities
        assert resolution.resolved_entity.text in ["Alice", "Carol"]
        # Should have multiple candidates
        assert len(resolution.candidates) == 2

    def test_resolve_low_confidence_threshold(self):
        """Test that low confidence resolution works with threshold."""
        # Create fresh tracker with just one entity
        tracker = EntityTracker()
        state = InformationState()

        # Create resolver with moderate confidence threshold
        config = ReferenceResolverConfig(
            use_llm=False,
            confidence_threshold=0.5,
            salience_recency_weight=0.3,  # Lower weights to reduce overall confidence
            salience_syntactic_weight=0.3,
        )
        resolver = ReferenceResolver(tracker, config)

        # Add entity
        entities = [
            Entity(text="Alice", type=EntityType.PERSON.value, mention_id="m_9", confidence=0.9),
        ]
        tracker.update(entities)

        ref = Reference(text="she", type=ReferenceType.PRONOUN.value, index=0)
        resolution = resolver.resolve(ref, state)

        # Should be resolved since there's only one candidate
        assert resolution.confidence >= config.confidence_threshold
        assert resolution.resolved_entity is not None

    def test_detect_references_pronouns(self, resolver):
        """Test detecting pronouns in utterance."""
        utterance = "She gave him the book"
        references = resolver._detect_references(utterance)

        assert len(references) >= 2
        texts = [ref.text for ref in references]
        assert "she" in texts
        assert "him" in texts

    def test_detect_references_demonstratives(self, resolver):
        """Test detecting demonstratives in utterance."""
        utterance = "This is better than that"
        references = resolver._detect_references(utterance)

        texts = [ref.text for ref in references]
        assert "this" in texts
        assert "that" in texts

    def test_detect_references_definite_descriptions(self, resolver):
        """Test detecting definite descriptions in utterance."""
        utterance = "The person walked to the store"
        references = resolver._detect_references(utterance)

        # Should detect "the person" and "the store"
        definite_refs = [
            ref for ref in references if ref.type == ReferenceType.DEFINITE_DESCRIPTION.value
        ]
        assert len(definite_refs) >= 2

    def test_resolve_all_in_utterance(self, resolver, tracker, state):
        """Test resolving all references in an utterance."""
        # Add entities
        entities = [
            Entity(text="Alice", type=EntityType.PERSON.value, mention_id="m_10", confidence=0.95),
            Entity(text="book", type=EntityType.OTHER.value, mention_id="m_11", confidence=0.9),
        ]
        tracker.update(entities)

        utterance = "She read it yesterday"
        resolutions = resolver.resolve_all(utterance, state)

        assert len(resolutions) >= 2
        # Should have resolved "she" and "it"
        resolved_texts = [res.reference.text for res in resolutions]
        assert "she" in resolved_texts
        assert "it" in resolved_texts

    def test_pronoun_compatibility_he(self, resolver):
        """Test pronoun compatibility for 'he'."""
        person = Entity(text="Bob", type=EntityType.PERSON.value, mention_id="m_12", confidence=0.9)
        location = Entity(
            text="Paris", type=EntityType.LOCATION.value, mention_id="m_13", confidence=0.9
        )

        assert resolver._pronoun_compatible("he", person) is True
        assert resolver._pronoun_compatible("he", location) is False

    def test_pronoun_compatibility_it(self, resolver):
        """Test pronoun compatibility for 'it'."""
        person = Entity(text="Bob", type=EntityType.PERSON.value, mention_id="m_14", confidence=0.9)
        location = Entity(
            text="Paris", type=EntityType.LOCATION.value, mention_id="m_15", confidence=0.9
        )

        assert resolver._pronoun_compatible("it", person) is False
        assert resolver._pronoun_compatible("it", location) is True

    def test_pronoun_compatibility_they(self, resolver):
        """Test pronoun compatibility for 'they'."""
        person = Entity(
            text="Alice", type=EntityType.PERSON.value, mention_id="m_16", confidence=0.9
        )
        org = Entity(
            text="Google", type=EntityType.ORGANIZATION.value, mention_id="m_17", confidence=0.9
        )

        # 'they' can refer to persons or organizations
        assert resolver._pronoun_compatible("they", person) is True
        assert resolver._pronoun_compatible("they", org) is True

    def test_description_compatibility_exact_match(self, resolver):
        """Test definite description compatibility with exact match."""
        entity = Entity(
            text="Alice", type=EntityType.PERSON.value, mention_id="m_18", confidence=0.9
        )

        assert resolver._description_compatible("the Alice", entity) is True
        assert resolver._description_compatible("the person", entity) is True
        assert resolver._description_compatible("the Bob", entity) is False

    def test_description_compatibility_canonical_form(self, resolver):
        """Test definite description compatibility with canonical form."""
        entity = Entity(
            text="NYC",
            type=EntityType.LOCATION.value,
            canonical_form="New York City",
            mention_id="m_19",
            confidence=0.9,
        )

        assert resolver._description_compatible("the New York City", entity) is True
        assert resolver._description_compatible("the city", entity) is True

    def test_qud_relevance_with_matching_entity(self):
        """Test QUD relevance scoring with matching entity."""
        # Create fresh tracker and resolver for this test
        tracker = EntityTracker()
        config = ReferenceResolverConfig(use_llm=False)
        resolver = ReferenceResolver(tracker, config)

        # Create state with a QUD mentioning an entity
        state = InformationState()
        question = WhQuestion(variable="x", predicate="weather(x)")
        state.shared.push_qud(question)

        entity = Entity(
            text="weather", type=EntityType.OTHER.value, mention_id="m_20", confidence=0.9
        )
        relevance = resolver._compute_qud_relevance(entity, state)

        assert relevance > 0.5  # Should have higher relevance

    def test_qud_relevance_no_qud(self, resolver):
        """Test QUD relevance with empty QUD stack."""
        state = InformationState()
        entity = Entity(
            text="Alice", type=EntityType.PERSON.value, mention_id="m_21", confidence=0.9
        )

        relevance = resolver._compute_qud_relevance(entity, state)
        assert relevance == 0.5  # Neutral when no QUD

    def test_is_compatible_pronoun(self, resolver):
        """Test compatibility check for pronouns."""
        ref = Reference(text="she", type=ReferenceType.PRONOUN.value, index=0)
        person = Entity(
            text="Alice", type=EntityType.PERSON.value, mention_id="m_22", confidence=0.9
        )
        location = Entity(
            text="Paris", type=EntityType.LOCATION.value, mention_id="m_23", confidence=0.9
        )

        assert resolver._is_compatible(ref, person) is True
        assert resolver._is_compatible(ref, location) is False

    def test_is_compatible_demonstrative(self, resolver):
        """Test compatibility check for demonstratives."""
        ref = Reference(text="this", type=ReferenceType.DEMONSTRATIVE.value, index=0)
        entity = Entity(text="book", type=EntityType.OTHER.value, mention_id="m_24", confidence=0.9)

        # Demonstratives compatible with any entity
        assert resolver._is_compatible(ref, entity) is True

    def test_score_candidates_recency(self, resolver, state):
        """Test candidate scoring based on recency."""
        candidates = [
            Entity(text="Alice", type=EntityType.PERSON.value, mention_id="m_25", confidence=0.9),
            Entity(text="Bob", type=EntityType.PERSON.value, mention_id="m_26", confidence=0.9),
        ]

        ref = Reference(text="she", type=ReferenceType.PRONOUN.value, index=0)
        scored = resolver._score_candidates(ref, candidates, state)

        assert len(scored) == 2
        # First candidate (most recent) should have higher score
        assert scored[0]["score"] > scored[1]["score"]

    def test_get_candidates_filters_by_compatibility(self):
        """Test that get_candidates filters incompatible entities."""
        # Create fresh tracker and resolver
        tracker = EntityTracker()
        config = ReferenceResolverConfig(use_llm=False)
        resolver = ReferenceResolver(tracker, config)
        state = InformationState()

        # Add both person and location
        entities = [
            Entity(text="Alice", type=EntityType.PERSON.value, mention_id="m_27", confidence=0.9),
            Entity(text="Paris", type=EntityType.LOCATION.value, mention_id="m_28", confidence=0.9),
        ]
        tracker.update(entities)

        # Get candidates for "she" - should only return person
        ref = Reference(text="she", type=ReferenceType.PRONOUN.value, index=0)
        candidates = resolver._get_candidates(ref, state)

        assert len(candidates) == 1
        assert candidates[0].text == "Alice"


class TestReferenceResolverWithLLM:
    """Tests for ReferenceResolver with LLM enabled."""

    @pytest.fixture
    def tracker(self):
        """Create an entity tracker."""
        return EntityTracker()

    @pytest.fixture
    def state(self):
        """Create a basic information state."""
        return InformationState()

    @pytest.mark.run_llm
    def test_create_resolver_with_llm(self, tracker):
        """Test creating resolver with LLM enabled."""
        config = ReferenceResolverConfig(use_llm=True)
        resolver = ReferenceResolver(tracker, config)

        # LLM may or may not initialize depending on API key availability
        assert resolver.config.use_llm is True

    @pytest.mark.run_llm
    def test_resolve_ambiguous_with_llm(self, tracker, state):
        """Test resolving ambiguous reference with LLM."""
        config = ReferenceResolverConfig(
            use_llm=True,
            ambiguity_threshold=0.9,  # High threshold to trigger ambiguity
        )
        resolver = ReferenceResolver(tracker, config)

        # Add multiple similar entities
        entities = [
            Entity(text="Alice", type=EntityType.PERSON.value, mention_id="m_29", confidence=0.9),
            Entity(text="Carol", type=EntityType.PERSON.value, mention_id="m_30", confidence=0.9),
        ]
        tracker.update(entities)

        ref = Reference(text="she", type=ReferenceType.PRONOUN.value, index=0)
        utterance = "She went to the store"

        # This should attempt LLM resolution if available
        resolution = resolver.resolve(ref, state, utterance=utterance)

        # Should still return a result (even if LLM unavailable)
        assert resolution is not None
