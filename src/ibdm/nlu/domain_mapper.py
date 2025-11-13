"""NLU entity to domain predicate mapper.

Maps generic NLU entities to domain-specific predicates.

This module bridges the gap between:
• NLU's generic entities (ORGANIZATION, TEMPORAL, etc.)
• Domain's semantic predicates (legal_entities, effective_date, etc.)

Example:
    >>> from ibdm.domains.nda_domain import get_nda_domain
    >>> from ibdm.nlu.entity_extractor import Entity, EntityType
    >>>
    >>> domain = get_nda_domain()
    >>> mapper = NLUDomainMapper(domain)
    >>>
    >>> entities = [
    ...     Entity(text="Acme Corp", entity_type=EntityType.ORGANIZATION),
    ...     Entity(text="Beta Inc", entity_type=EntityType.ORGANIZATION),
    ... ]
    >>>
    >>> result = mapper.map_entities_to_answer(entities, "legal_entities")
    >>> assert result == "Acme Corp, Beta Inc"
"""

from ibdm.core.domain import DomainModel
from ibdm.nlu.entity_extractor import Entity, EntityType


class NLUDomainMapper:
    """Maps NLU entities to domain predicates.

    Provides systematic mapping between NLU's generic entity types
    and domain-specific predicates. This addresses the gap identified
    in py-trindikit analysis where NLU entities weren't semantically
    grounded in the domain model.

    Attributes:
        domain: The domain model providing predicate definitions
        entity_to_predicate: Mapping from EntityType to predicate names

    Example:
        >>> domain = get_nda_domain()
        >>> mapper = NLUDomainMapper(domain)
        >>> # mapper knows ORGANIZATION → "legal_entities"
        >>> # mapper knows TEMPORAL → "date"
    """

    def __init__(self, domain: DomainModel):
        """Initialize NLU-domain mapper.

        Args:
            domain: Domain model with predicate definitions
        """
        self.domain = domain

        # Define mapping rules from NLU entity types to domain predicates
        # This is domain-agnostic mapping - specific domains may override
        self.entity_to_predicate = {
            EntityType.ORGANIZATION: "legal_entities",
            EntityType.TEMPORAL: "date",
            EntityType.LOCATION: "jurisdiction",
            # Note: EntityType.DURATION doesn't exist in entity_extractor.py
            # We'll handle duration via TEMPORAL or NUMERICAL entities
        }

    def map_entities_to_answer(
        self, entities: list[Entity], question_predicate: str
    ) -> str | None:
        """Map extracted entities to answer content.

        Filters entities by predicate type and formats them appropriately
        for the question being answered.

        Args:
            entities: List of entities extracted from user utterance
            question_predicate: Predicate from the question being answered

        Returns:
            Formatted answer content, or None if no relevant entities found

        Example:
            >>> entities = [
            ...     Entity(text="Acme Corp", entity_type=EntityType.ORGANIZATION),
            ...     Entity(text="Beta Inc", entity_type=EntityType.ORGANIZATION),
            ... ]
            >>> mapper.map_entities_to_answer(entities, "legal_entities")
            'Acme Corp, Beta Inc'

            >>> entities = [
            ...     Entity(text="2025-01-15", entity_type=EntityType.TEMPORAL),
            ... ]
            >>> mapper.map_entities_to_answer(entities, "date")
            '2025-01-15'
        """
        # Filter entities by predicate type
        relevant_entities = []

        # Find entity type(s) that map to this predicate
        for entity_type, predicate in self.entity_to_predicate.items():
            if predicate == question_predicate:
                relevant_entities = [
                    e for e in entities if e.entity_type == entity_type
                ]
                break

        if not relevant_entities:
            # No mapped entities found - could be direct answer text
            return None

        # Format based on predicate
        if question_predicate == "legal_entities":
            # Multiple organizations - comma-separated list
            return ", ".join([e.text for e in relevant_entities])
        else:
            # Single value predicates - first entity
            return relevant_entities[0].text

    def get_predicate_for_entity_type(
        self, entity_type: EntityType
    ) -> str | None:
        """Get domain predicate for NLU entity type.

        Args:
            entity_type: NLU entity type

        Returns:
            Predicate name, or None if no mapping

        Example:
            >>> mapper.get_predicate_for_entity_type(EntityType.ORGANIZATION)
            'legal_entities'
        """
        return self.entity_to_predicate.get(entity_type)

    def get_entity_type_for_predicate(self, predicate: str) -> EntityType | None:
        """Get NLU entity type for domain predicate.

        Reverse mapping from predicate to entity type.

        Args:
            predicate: Domain predicate name

        Returns:
            EntityType, or None if no mapping

        Example:
            >>> mapper.get_entity_type_for_predicate("legal_entities")
            EntityType.ORGANIZATION
        """
        for entity_type, pred in self.entity_to_predicate.items():
            if pred == predicate:
                return entity_type
        return None


def create_nda_domain_mapper() -> NLUDomainMapper:
    """Create NLU-domain mapper for NDA domain.

    Convenience function that creates mapper with NDA domain.

    Returns:
        Configured NLUDomainMapper for NDA domain

    Example:
        >>> mapper = create_nda_domain_mapper()
        >>> assert mapper.domain.name == "nda_drafting"
    """
    from ibdm.domains.nda_domain import get_nda_domain

    return NLUDomainMapper(get_nda_domain())
