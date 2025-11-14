"""NDA drafting domain model.

Defines predicates, sorts, and plan builder for NDA drafting tasks.

This domain model provides semantic grounding for:
- Legal entity identification (parties)
- NDA type selection (mutual vs one-way)
- Temporal information (effective date, duration)
- Jurisdiction selection (governing law)
"""

from ibdm.core.domain import DomainModel
from ibdm.core.plans import Plan
from ibdm.core.questions import AltQuestion, WhQuestion


def create_nda_domain() -> DomainModel:
    """Create NDA drafting domain model.

    Defines:
    • Predicates: parties, nda_type, effective_date, duration, governing_law
    • Sorts: nda_kind, jurisdiction
    • Plan builder: nda_drafting

    Returns:
        Configured DomainModel for NDA drafting

    Example:
        >>> domain = create_nda_domain()
        >>> assert "legal_entities" in domain.predicates
        >>> assert "nda_kind" in domain.sorts
        >>> plan = domain.get_plan("nda_drafting", {})
        >>> assert len(plan.subplans) == 5
    """
    domain = DomainModel(name="nda_drafting")

    # Define predicates
    domain.add_predicate(
        "legal_entities",
        arity=1,
        arg_types=["organization_list"],
        description="Organizations entering into NDA",
    )
    domain.add_predicate(
        "nda_type",
        arity=1,
        arg_types=["nda_kind"],
        description="Type of NDA (mutual or one-way)",
    )
    domain.add_predicate(
        "date",
        arity=1,
        arg_types=["date_string"],
        description="Effective date when NDA takes effect",
    )
    domain.add_predicate(
        "time_period",
        arity=1,
        arg_types=["duration_string"],
        description="Duration of confidentiality obligations",
    )
    domain.add_predicate(
        "jurisdiction",
        arity=1,
        arg_types=["us_state"],
        description="Governing law jurisdiction",
    )

    # Define sorts (semantic types with valid values)
    domain.add_sort("nda_kind", ["mutual", "one-way", "unilateral"])
    domain.add_sort("us_state", ["California", "Delaware", "New York"])

    # Register plan builder
    domain.register_plan_builder("nda_drafting", _build_nda_plan)

    return domain


def _build_nda_plan(context: dict) -> Plan:
    """Build NDA drafting plan.

    Creates a findout plan for gathering NDA requirements.
    The plan consists of 5 subplans to collect all necessary information.

    Args:
        context: Context dict (currently unused, for future extensibility)

    Returns:
        Plan with 5 findout subplans

    Note:
        This plan builder is registered with the domain model and called
        via domain.get_plan("nda_drafting", context).
    """
    subplans = [
        Plan(
            plan_type="findout",
            content=WhQuestion(variable="parties", predicate="legal_entities"),
            status="active",
        ),
        Plan(
            plan_type="findout",
            content=AltQuestion(alternatives=["mutual", "one-way"]),
            status="active",
        ),
        Plan(
            plan_type="findout",
            content=WhQuestion(variable="effective_date", predicate="date"),
            status="active",
        ),
        Plan(
            plan_type="findout",
            content=WhQuestion(variable="duration", predicate="time_period"),
            status="active",
        ),
        Plan(
            plan_type="findout",
            content=AltQuestion(alternatives=["California", "Delaware", "New York"]),
            status="active",
        ),
    ]

    return Plan(
        plan_type="nda_drafting",
        content="nda_requirements",
        status="active",
        subplans=subplans,
    )


# Singleton pattern for domain model
_nda_domain: DomainModel | None = None


def get_nda_domain() -> DomainModel:
    """Get or create NDA domain singleton.

    Returns:
        Singleton DomainModel instance for NDA drafting

    Example:
        >>> domain1 = get_nda_domain()
        >>> domain2 = get_nda_domain()
        >>> assert domain1 is domain2  # Same instance
    """
    global _nda_domain
    if _nda_domain is None:
        _nda_domain = create_nda_domain()
    return _nda_domain
