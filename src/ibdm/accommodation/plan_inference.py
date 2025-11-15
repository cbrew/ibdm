"""Plan inference for dialogue management.

Plan inference attempts to identify the speaker's goals and plans
based on their questions and requests, enabling proactive assistance.

ARCHITECTURAL NOTE (Policy #10, #11):
- Plan formation should happen in INTEGRATION phase, not interpretation
- Domain-specific plans should use DomainModel.get_plan() not hardcoded logic
- This module provides generic plan inference when domain is not available
- For domain-specific plan building, register plan builders with the domain
"""

from ibdm.core import DialogueMove, InformationState, Plan, Question, WhQuestion, YNQuestion
from ibdm.core.domain import DomainModel


def infer_plan(
    move: DialogueMove, state: InformationState, domain: DomainModel | None = None
) -> Plan | None:
    """Infer a dialogue plan from a user's move.

    This function analyzes questions and requests to infer higher-level
    goals and create corresponding plans.

    For domain-specific plan building, use domain.get_plan() with registered
    plan builders instead of this generic inference.

    Args:
        move: The dialogue move to analyze
        state: Current information state
        domain: Optional domain model for domain-specific plan building

    Returns:
        Inferred Plan or None if no plan can be inferred
    """
    if move.move_type == "ask":
        return _infer_plan_from_question(move.content, state, domain)
    elif move.move_type == "request":
        return _infer_plan_from_request(move.content, state, domain)
    else:
        return None


def _infer_plan_from_question(
    question: Question, state: InformationState, domain: DomainModel | None = None
) -> Plan | None:
    """Infer a plan from a question.

    Creates generic information-seeking plans from questions.
    Domain-specific plan building should use domain.get_plan() instead.

    Questions often reveal user goals. For example:
    - "When is the meeting?" → FINDOUT(meeting_time)
    - "Can you book a table?" → PERFORM(book_table)

    Args:
        question: Question object
        state: Information state
        domain: Optional domain model (currently unused, for future extension)

    Returns:
        Generic plan or None
    """
    if not isinstance(question, (WhQuestion, YNQuestion)):
        return None

    if isinstance(question, WhQuestion):
        return _infer_from_wh_question(question, state)
    else:  # YNQuestion
        return _infer_from_yn_question(question, state)


def _infer_from_wh_question(question: WhQuestion, state: InformationState) -> Plan | None:
    """Infer plan from wh-question.

    Creates a generic information-seeking plan based on the question's predicate.
    Domain-independent implementation - no hardcoded domain logic.

    Wh-questions typically indicate information-seeking goals.

    Args:
        question: WhQuestion object
        state: Information state

    Returns:
        Generic FINDOUT plan
    """
    # Create generic information-seeking plan using the predicate
    # No domain-specific logic - just use the predicate directly
    return Plan(
        plan_type="findout",
        content=question,  # Store the question itself as content
        status="active",
    )


def _infer_from_yn_question(question: YNQuestion, state: InformationState) -> Plan | None:
    """Infer plan from yes/no question.

    Creates a generic verification plan.
    Domain-independent implementation - no hardcoded domain logic.

    Y/N questions typically indicate verification goals.

    Args:
        question: YNQuestion object
        state: Information state

    Returns:
        Generic FINDOUT plan for verification
    """
    # Create generic verification plan using the question itself
    # No domain-specific logic - just store the question as content
    return Plan(
        plan_type="findout",
        content=question,  # Store the question itself as content
        status="active",
    )


def _infer_plan_from_request(
    request: str, state: InformationState, domain: DomainModel | None = None
) -> Plan | None:
    """Infer a plan from a request/command.

    Creates a generic action plan.
    Domain-independent implementation - no hardcoded domain logic.

    Direct requests clearly indicate performance goals.

    Args:
        request: Request string
        state: Information state
        domain: Optional domain model (currently unused, for future extension)

    Returns:
        Generic PERFORM plan
    """
    # Create generic action plan
    # No domain-specific logic - just store the request as content
    return Plan(
        plan_type="perform",
        content=request,
        status="active",
    )


def decompose_plan(
    plan: Plan, state: InformationState, domain: DomainModel | None = None
) -> list[Plan]:
    """Decompose a high-level plan into subplans.

    DEPRECATED: Domain-specific plan decomposition should use domain.get_plan()
    with registered plan builders instead of this generic function.

    This function is kept for backward compatibility but returns empty list,
    indicating no generic decomposition is available. Use domain-specific
    plan builders registered with DomainModel instead.

    Args:
        plan: The plan to decompose
        state: Current information state
        domain: Optional domain model for domain-specific decomposition

    Returns:
        Empty list (domain-specific decomposition should use domain.get_plan())

    Example:
        # DEPRECATED - Don't do this:
        subplans = decompose_plan(plan, state)

        # CORRECT - Use domain-specific plan builders:
        domain = get_travel_domain()
        plan = domain.get_plan("travel_booking", context)
    """
    # Domain-specific plan decomposition should be done via domain.get_plan()
    # with registered plan builders, not hardcoded logic here.
    # See travel_domain.py and nda_domain.py for examples.
    return []
