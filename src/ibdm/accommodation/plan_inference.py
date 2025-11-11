"""Plan inference for dialogue management.

Plan inference attempts to identify the speaker's goals and plans
based on their questions and requests, enabling proactive assistance.
"""

from ibdm.core import DialogueMove, InformationState, Plan, Question, WhQuestion, YNQuestion


def infer_plan(move: DialogueMove, state: InformationState) -> Plan | None:
    """Infer a dialogue plan from a user's move.

    This function analyzes questions and requests to infer higher-level
    goals and create corresponding plans.

    Args:
        move: The dialogue move to analyze
        state: Current information state

    Returns:
        Inferred Plan or None if no plan can be inferred
    """
    if move.move_type == "ask":
        return _infer_plan_from_question(move.content, state)
    elif move.move_type == "request":
        return _infer_plan_from_request(move.content, state)
    else:
        return None


def _infer_plan_from_question(question: Question, state: InformationState) -> Plan | None:
    """Infer a plan from a question.

    Questions often reveal user goals. For example:
    - "When is the meeting?" → FINDOUT(meeting_time)
    - "Can you book a table?" → PERFORM(book_table)
    """
    if not isinstance(question, (WhQuestion, YNQuestion)):
        return None

    if isinstance(question, WhQuestion):
        return _infer_from_wh_question(question, state)
    else:  # YNQuestion
        return _infer_from_yn_question(question, state)


def _infer_from_wh_question(question: WhQuestion, state: InformationState) -> Plan | None:
    """Infer plan from wh-question.

    Wh-questions typically indicate information-seeking goals.
    """
    predicate = question.predicate.lower()
    wh_word = question.constraints.get("wh_word", "").lower()

    # Extract key terms from predicate
    if "weather" in predicate:
        return Plan(
            plan_type="findout",
            content="findout_weather",
            status="active",
        )
    elif "time" in predicate or "when" in wh_word:
        return Plan(
            plan_type="findout",
            content=f"findout_time({predicate})",
            status="active",
        )
    elif "location" in predicate or "where" in wh_word:
        return Plan(
            plan_type="findout",
            content=f"findout_location({predicate})",
            status="active",
        )
    elif "price" in predicate or "cost" in predicate:
        return Plan(
            plan_type="findout",
            content=f"findout_cost({predicate})",
            status="active",
        )
    else:
        # Generic information seeking
        return Plan(
            plan_type="findout",
            content=f"findout({predicate})",
            status="active",
        )


def _infer_from_yn_question(question: YNQuestion, state: InformationState) -> Plan | None:
    """Infer plan from yes/no question.

    Y/N questions starting with "can you" or "could you" often indicate
    requests for action rather than pure information seeking.
    """
    proposition = question.proposition.lower()

    # Check for polite requests
    if proposition.startswith(("can you", "could you", "would you")):
        # This is really a request
        # Extract the action
        for prefix in ["can you", "could you", "would you"]:
            if proposition.startswith(prefix):
                action = proposition[len(prefix) :].strip()
                return Plan(
                    plan_type="perform",
                    content=f"perform({action})",
                    status="active",
                )

    # Check for capability questions ("can I...", "am I able to...")
    if proposition.startswith(("can i", "may i", "am i")):
        return Plan(
            plan_type="findout",
            content=f"check_capability({proposition})",
            status="active",
        )

    # Generic yes/no question - checking a fact
    return Plan(
        plan_type="findout",
        content=f"verify({proposition})",
        status="active",
    )


def _infer_plan_from_request(request: str, state: InformationState) -> Plan | None:
    """Infer a plan from a request/command.

    Direct requests clearly indicate performance goals.
    """
    request_lower = request.lower().strip()

    # Identify action verbs
    action_verbs = {
        "book": "book",
        "reserve": "reserve",
        "cancel": "cancel",
        "change": "modify",
        "show": "display",
        "tell": "inform",
        "find": "search",
        "search": "search",
        "get": "retrieve",
    }

    for verb, action_type in action_verbs.items():
        if request_lower.startswith(verb):
            return Plan(
                plan_type="perform",
                content=f"{action_type}({request})",
                status="active",
            )

    # Generic action request
    return Plan(
        plan_type="perform",
        content=f"perform({request})",
        status="active",
    )


def decompose_plan(plan: Plan, state: InformationState) -> list[Plan]:
    """Decompose a high-level plan into subplans.

    This creates a plan hierarchy for complex goals.

    Args:
        plan: The plan to decompose
        state: Current information state

    Returns:
        List of subplans (may be empty if plan is atomic)
    """
    content_lower = str(plan.content).lower()

    # Example decompositions
    if "book" in content_lower and "restaurant" in content_lower:
        # Booking a restaurant requires: time, party size, location
        return [
            Plan(
                plan_type="findout",
                content="findout(restaurant_time)",
                status="active",
            ),
            Plan(
                plan_type="findout",
                content="findout(party_size)",
                status="active",
            ),
            Plan(
                plan_type="findout",
                content="findout(location_preference)",
                status="active",
            ),
            Plan(
                plan_type="perform",
                content="perform(make_reservation)",
                status="pending",
            ),
        ]
    elif "book" in content_lower and "flight" in content_lower:
        # Flight booking requires: origin, destination, dates
        return [
            Plan(
                plan_type="findout",
                content="findout(origin)",
                status="active",
            ),
            Plan(
                plan_type="findout",
                content="findout(destination)",
                status="active",
            ),
            Plan(
                plan_type="findout",
                content="findout(travel_dates)",
                status="active",
            ),
            Plan(
                plan_type="perform",
                content="perform(book_flight)",
                status="pending",
            ),
        ]

    # No decomposition needed
    return []
