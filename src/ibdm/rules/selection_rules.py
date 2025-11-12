"""Selection rules for Issue-Based Dialogue Management.

Selection rules choose the next system action based on the information state.
They implement strategies for answering, raising questions, clarifying, etc.

Based on Larsson (2002) Issue-based Dialogue Management.
"""

from ibdm.core import Answer, DialogueMove, InformationState, WhQuestion
from ibdm.rules.update_rules import UpdateRule


def create_selection_rules() -> list[UpdateRule]:
    """Create standard selection rules.

    Returns:
        List of selection rules
    """
    return [
        # Execute active Plans by converting findout subplans to ask moves
        UpdateRule(
            name="select_plan_driven_question",
            preconditions=_has_active_plan_subplan,
            effects=_execute_plan_subplan,
            priority=15,
            rule_type="selection",
        ),
        # If there's already something on the agenda, don't add more
        # (this is checked in the engine, but we can have rules too)
        # Answer the top QUD if we have knowledge
        UpdateRule(
            name="select_answer_qud",
            preconditions=_can_answer_qud,
            effects=_add_answer_to_agenda,
            priority=10,
            rule_type="selection",
        ),
        # Raise a clarification question if QUD is unclear
        UpdateRule(
            name="select_clarification",
            preconditions=_needs_clarification,
            effects=_add_clarification_to_agenda,
            priority=9,
            rule_type="selection",
        ),
        # Ask a question to gather information
        UpdateRule(
            name="select_ask_question",
            preconditions=_should_ask_question,
            effects=_add_question_to_agenda,
            priority=5,
            rule_type="selection",
        ),
        # Provide a generic response if nothing else applies
        UpdateRule(
            name="select_generic_response",
            preconditions=lambda state: True,  # Always applicable
            effects=_add_generic_response,
            priority=1,
            rule_type="selection",
        ),
    ]


# Precondition functions


def _has_active_plan_subplan(state: InformationState) -> bool:
    """Check if there's an active plan with findout subplans to execute.

    Only triggers when agenda is empty (don't interrupt ongoing actions).
    """
    # Don't trigger if there's already something on the agenda
    if state.private.agenda:
        return False

    # Check if there's an active plan with active subplans
    for plan in state.private.plan:
        if plan.is_active() and plan.subplans:
            # Look for first active findout subplan
            for subplan in plan.subplans:
                if subplan.is_active() and subplan.plan_type == "findout":
                    return True

    return False


def _can_answer_qud(state: InformationState) -> bool:
    """Check if we can answer the top QUD from our beliefs."""
    if not state.shared.qud:
        return False

    top_question = state.shared.top_qud()

    # Check if we have an answer in our beliefs
    # For simplicity, we look for specific belief keys
    if isinstance(top_question, WhQuestion):
        # Look for a belief that matches the predicate
        predicate_key = top_question.predicate.lower()
        # Simple heuristic: check if any belief key contains relevant words
        for key in state.private.beliefs:
            if predicate_key in key.lower() or key.lower() in predicate_key:
                return True

    # For now, don't claim we can answer other types
    # (This is where domain knowledge would be integrated)
    return False


def _needs_clarification(state: InformationState) -> bool:
    """Check if the top QUD needs clarification."""
    if not state.shared.qud:
        return False

    # Check if the last move was unclear or ambiguous
    # For now, we use a simple heuristic: very short questions might need clarification
    if state.shared.last_moves:
        last_move = state.shared.last_moves[-1]
        if last_move.move_type == "ask":
            # Check if the question is very short (might be unclear)
            if isinstance(last_move.content, str) and len(last_move.content.split()) <= 2:
                return True

    return False


def _should_ask_question(state: InformationState) -> bool:
    """Check if we should ask a question to gather information."""
    # Ask a question if:
    # 1. There's no QUD (we can initiate)
    # 2. We're in active dialogue
    # 3. The last move wasn't a question from us

    if state.control.dialogue_state != "active":
        return False

    if state.shared.qud:
        # Don't ask if there's already a QUD
        return False

    # Check if we recently asked
    if state.shared.last_moves:
        last_move = state.shared.last_moves[-1]
        if last_move.speaker == state.agent_id and last_move.move_type == "ask":
            return False

    return True


# Effect functions


def _execute_plan_subplan(state: InformationState) -> InformationState:
    """Execute the first active findout subplan by creating an ask move.

    Takes the first active findout subplan, creates an ask DialogueMove
    with the question from the subplan, adds it to the agenda, and marks
    the subplan as completed.
    """
    new_state = state.clone()

    # Find the first active plan with active findout subplans
    for plan in new_state.private.plan:
        if plan.is_active() and plan.subplans:
            # Find first active findout subplan
            for subplan in plan.subplans:
                if subplan.is_active() and subplan.plan_type == "findout":
                    # Create ask move with the question from the subplan
                    move = DialogueMove(
                        move_type="ask",
                        content=subplan.content,
                        speaker=new_state.agent_id,
                    )
                    new_state.private.agenda.append(move)

                    # Mark subplan as completed (will be executed)
                    subplan.complete()

                    # Only execute one subplan at a time
                    return new_state

    return new_state


def _add_answer_to_agenda(state: InformationState) -> InformationState:
    """Add an answer move to the agenda."""
    new_state = state.clone()

    top_question = new_state.shared.top_qud()
    if not top_question:
        return new_state

    # Retrieve answer from beliefs
    answer_content = None
    if isinstance(top_question, WhQuestion):
        predicate_key = top_question.predicate.lower()
        for key, value in new_state.private.beliefs.items():
            if predicate_key in key.lower() or key.lower() in predicate_key:
                answer_content = value
                break

    if answer_content is not None:
        answer = Answer(content=answer_content, question_ref=top_question)
        move = DialogueMove(
            move_type="answer",
            content=answer,
            speaker=new_state.agent_id,
        )
        new_state.private.agenda.append(move)

    return new_state


def _add_clarification_to_agenda(state: InformationState) -> InformationState:
    """Add a clarification question to the agenda."""
    new_state = state.clone()

    # Create a clarification question
    clarification = WhQuestion(
        variable="x", predicate="clarification_needed", constraints={"type": "icm"}
    )

    move = DialogueMove(
        move_type="ask",
        content=clarification,
        speaker=new_state.agent_id,
    )
    new_state.private.agenda.append(move)

    return new_state


def _add_question_to_agenda(state: InformationState) -> InformationState:
    """Add a question to the agenda."""
    new_state = state.clone()

    # Create a simple question to engage the user
    question = WhQuestion(
        variable="x",
        predicate="how_can_i_help",
    )

    move = DialogueMove(
        move_type="ask",
        content=question,
        speaker=new_state.agent_id,
    )
    new_state.private.agenda.append(move)

    return new_state


def _add_generic_response(state: InformationState) -> InformationState:
    """Add a generic acknowledgment to the agenda."""
    new_state = state.clone()

    # Create a simple acknowledgment
    move = DialogueMove(
        move_type="assert",
        content="I understand.",
        speaker=new_state.agent_id,
    )
    new_state.private.agenda.append(move)

    return new_state
