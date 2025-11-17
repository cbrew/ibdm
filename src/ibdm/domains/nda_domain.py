"""NDA drafting domain model.

Defines predicates, sorts, and plan builder for NDA drafting tasks.

This domain model provides semantic grounding for:
- Legal entity identification (parties)
- NDA type selection (mutual vs one-way)
- Temporal information (effective date, duration)
- Jurisdiction selection (governing law)
"""

from typing import Any

from ibdm.core.actions import Action, Proposition
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

    # Register action precondition functions (IBiS4)
    domain.register_precond_function("generate_draft", _check_generate_draft_precond)
    domain.register_precond_function("send_for_review", _check_send_for_review_precond)
    domain.register_precond_function("execute_agreement", _check_execute_agreement_precond)

    # Register action postcondition functions (IBiS4)
    domain.register_postcond_function("generate_draft", _generate_draft_postcond)
    domain.register_postcond_function("send_for_review", _send_for_review_postcond)
    domain.register_postcond_function("execute_agreement", _execute_agreement_postcond)

    return domain


def _build_nda_plan(context: dict[str, Any]) -> Plan:
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


# ============================================================================
# IBiS4 Action Precondition Functions
# ============================================================================


def _check_generate_draft_precond(action: Action, commitments: set[str]) -> tuple[bool, str]:
    """Check preconditions for generating NDA draft.

    Requires all required fields to be collected:
    - Parties (legal entities)
    - NDA type (mutual/one-way)
    - Effective date
    - Duration
    - Governing jurisdiction

    Args:
        action: generate_draft action
        commitments: Current commitments from dialogue

    Returns:
        Tuple of (satisfied, error_message)
    """
    required_fields = [
        "legal_entities",
        "nda_type",
        "date",
        "time_period",
        "jurisdiction",
    ]

    missing_fields = []
    for field in required_fields:
        # Check if any commitment contains this field
        if not any(field in commit for commit in commitments):
            missing_fields.append(field)

    if missing_fields:
        return (
            False,
            f"Missing required information: {', '.join(missing_fields)}",
        )

    return (True, "")


def _check_send_for_review_precond(action: Action, commitments: set[str]) -> tuple[bool, str]:
    """Check preconditions for sending NDA for review.

    Requires:
    - Draft document generated

    Args:
        action: send_for_review action
        commitments: Current commitments

    Returns:
        Tuple of (satisfied, error_message)
    """
    # Check if draft was generated
    if not any("draft_generated" in commit for commit in commitments):
        return (False, "NDA draft must be generated first")

    return (True, "")


def _check_execute_agreement_precond(action: Action, commitments: set[str]) -> tuple[bool, str]:
    """Check preconditions for executing NDA agreement.

    Requires:
    - Draft sent for review
    - All parties approved

    Args:
        action: execute_agreement action
        commitments: Current commitments

    Returns:
        Tuple of (satisfied, error_message)
    """
    # Check if sent for review
    if not any("sent_for_review" in commit for commit in commitments):
        return (False, "NDA must be sent for review first")

    # Check if approved (in a real system, we'd check each party)
    if not any("review_approved" in commit for commit in commitments):
        return (False, "NDA must be approved by all parties first")

    return (True, "")


# ============================================================================
# IBiS4 Action Postcondition Functions
# ============================================================================


def _generate_draft_postcond(action: Action) -> list[Proposition]:
    """Generate postconditions for draft generation.

    Creates propositions indicating:
    - Draft document has been generated
    - Document ID assigned

    Args:
        action: generate_draft action

    Returns:
        List of postcondition propositions
    """
    document_id = action.parameters.get("document_id", "NDA_DRAFT_001")

    return [
        Proposition(
            predicate="draft_generated",
            arguments={"document_id": document_id, "status": "ready_for_review"},
        ),
    ]


def _send_for_review_postcond(action: Action) -> list[Proposition]:
    """Generate postconditions for sending document for review.

    Creates propositions indicating:
    - Document sent to parties
    - Review requested

    Args:
        action: send_for_review action

    Returns:
        List of postcondition propositions
    """
    document_id = action.parameters.get("document_id", "NDA_DRAFT_001")
    recipients = action.parameters.get("recipients", "all_parties")

    return [
        Proposition(
            predicate="sent_for_review",
            arguments={"document_id": document_id, "recipients": recipients},
        ),
    ]


def _execute_agreement_postcond(action: Action) -> list[Proposition]:
    """Generate postconditions for executing agreement.

    Creates propositions indicating:
    - Agreement executed
    - Agreement is now in effect

    Args:
        action: execute_agreement action

    Returns:
        List of postcondition propositions
    """
    document_id = action.parameters.get("document_id", "NDA_DRAFT_001")
    execution_date = action.parameters.get("execution_date", "2025-01-01")

    return [
        Proposition(
            predicate="agreement_executed",
            arguments={
                "document_id": document_id,
                "execution_date": execution_date,
                "status": "in_effect",
            },
        ),
    ]


# ============================================================================
# Domain Singleton
# ============================================================================


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
