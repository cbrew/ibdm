"""Selection rules for Issue-Based Dialogue Management.

Selection rules choose the next system action based on the information state.
They implement strategies for answering, raising questions, etc.

Based on Larsson (2002) Issue-based Dialogue Management, Chapter 2, Section 2.9.
Implements IBiS1 selection rules.
"""

from ibdm.core import Answer, DialogueMove, InformationState, WhQuestion
from ibdm.rules.update_rules import UpdateRule


def create_selection_rules() -> list[UpdateRule]:
    """Create IBiS1 selection rules.

    Implements the selection rules from Larsson (2002) Section 2.9:
    1. SelectFromPlan (Section 2.9.1) - Select action from plan
    2. SelectAnswer (Section 2.9.4) - Answer top QUD question
    3. SelectAsk (Section 2.9.2) - Ask top QUD question
    4. SelectGreet (Section 2.9) - Greet at dialogue start
    5. Fallback - Generic response

    Returns:
        List of IBiS1 selection rules
    """
    return [
        # Rule: SelectFromPlan (Section 2.9.1)
        # Pre: head(private.plan) is a communicative action
        # Effect: add(shared.next_moves, head(private.plan))
        UpdateRule(
            name="select_from_plan",
            preconditions=_has_communicative_plan,
            effects=_select_plan_action,
            priority=20,
            rule_type="selection",
        ),
        # Rule: SelectAnswer (Section 2.9.4)
        # Pre: top(shared.qud) == Q AND system can answer Q
        # Effect: add(shared.next_moves, answer(answer))
        UpdateRule(
            name="select_answer",
            preconditions=_can_answer_qud,
            effects=_select_answer_to_qud,
            priority=15,
            rule_type="selection",
        ),
        # Rule: SelectAsk (Section 2.9.2)
        # Pre: top(shared.qud) == Q AND system needs to ask Q
        # Effect: add(shared.next_moves, ask(Q))
        UpdateRule(
            name="select_ask",
            preconditions=_should_ask_qud,
            effects=_select_ask_qud,
            priority=10,
            rule_type="selection",
        ),
        # Rule: SelectGreet (Section 2.9)
        # Pre: Dialogue start, no greeting yet
        # Effect: add(shared.next_moves, greet())
        UpdateRule(
            name="select_greet",
            preconditions=_should_greet,
            effects=_select_greeting,
            priority=5,
            rule_type="selection",
        ),
        # Fallback: Generic response if nothing else applies
        UpdateRule(
            name="select_fallback",
            preconditions=lambda state: True,  # Always applicable
            effects=_select_fallback_response,
            priority=1,
            rule_type="selection",
        ),
    ]


# Precondition functions (IBiS1)


def _has_communicative_plan(state: InformationState) -> bool:
    """Check if head of private.plan is a communicative action.

    IBiS1 Rule: SelectFromPlan (Section 2.9.1)
    Pre: head(private.plan) is a communicative action
    """
    # Don't trigger if there's already something on the agenda
    if state.private.agenda:
        return False

    # Check if there's a plan at the head
    if not state.private.plan:
        return False

    # Get the head (first) plan
    head_plan = state.private.plan[0]

    # Check if it's active and is a communicative action
    # Communicative actions include: findout, raise, inform, greet
    if not head_plan.is_active():
        return False

    communicative_types = ["findout", "raise", "inform", "greet", "ask", "answer"]
    return head_plan.plan_type in communicative_types


def _can_answer_qud(state: InformationState) -> bool:
    """Check if system can answer the top QUD from beliefs.

    IBiS1 Rule: SelectAnswer (Section 2.9.4)
    Pre: top(shared.qud) == Q AND system can answer Q
    """
    # Don't trigger if there's already something on the agenda
    if state.private.agenda:
        return False

    if not state.shared.qud:
        return False

    top_question = state.shared.top_qud()

    # Check if we have an answer in our beliefs
    if isinstance(top_question, WhQuestion):
        # Look for a belief that matches the predicate
        predicate_key = top_question.predicate.lower()
        # Check if any belief key contains relevant words
        for key in state.private.beliefs:
            if predicate_key in key.lower() or key.lower() in predicate_key:
                return True

    # For other question types, check for direct answer
    # (This is where domain knowledge would be integrated)
    return False


def _should_ask_qud(state: InformationState) -> bool:
    """Check if system should ask the top QUD question.

    IBiS1 Rule: SelectAsk (Section 2.9.2)
    Pre: top(shared.qud) == Q AND system needs to ask Q

    System asks a question when:
    - There's a question on QUD
    - System doesn't have the answer
    - Question hasn't been asked yet
    """
    # Don't trigger if there's already something on the agenda
    if state.private.agenda:
        return False

    if not state.shared.qud:
        return False

    # If we can answer, SelectAnswer should fire instead
    if _can_answer_qud(state):
        return False

    # System should ask the question
    return True


def _should_greet(state: InformationState) -> bool:
    """Check if system should greet at dialogue start.

    IBiS1 Rule: SelectGreet (Section 2.9)
    Pre: Dialogue start, no greeting yet
    """
    # Don't trigger if there's already something on the agenda
    if state.private.agenda:
        return False

    # Check if dialogue is just starting
    if state.control.dialogue_state != "active":
        return False

    # Check if no moves have been made yet or only user greeting
    if not state.shared.last_moves:
        return True

    # Check if last move was a user greeting and system hasn't responded
    if state.shared.last_moves:
        last_move = state.shared.last_moves[-1]
        if last_move.move_type == "greet" and last_move.speaker != state.agent_id:
            # Check if system has already greeted back
            for move in state.shared.last_moves:
                if move.speaker == state.agent_id and move.move_type == "greet":
                    return False
            return True

    return False


# Effect functions (IBiS1)


def _select_plan_action(state: InformationState) -> InformationState:
    """Select action from head of plan.

    IBiS1 Rule: SelectFromPlan (Section 2.9.1)
    Effect: add(shared.next_moves, head(private.plan))

    Converts the head plan into a dialogue move and adds to agenda.
    """
    new_state = state.clone()

    if not new_state.private.plan:
        return new_state

    # Get the head (first) plan
    head_plan = new_state.private.plan[0]

    # Convert plan to dialogue move based on plan type
    if head_plan.plan_type == "findout":
        # Findout plan: create ask move with question
        move = DialogueMove(
            move_type="ask",
            content=head_plan.content,
            speaker=new_state.agent_id,
        )
    elif head_plan.plan_type == "inform":
        # Inform plan: create assert move
        move = DialogueMove(
            move_type="assert",
            content=head_plan.content,
            speaker=new_state.agent_id,
        )
    elif head_plan.plan_type == "greet":
        # Greet plan: create greet move
        move = DialogueMove(
            move_type="greet",
            content="greeting",
            speaker=new_state.agent_id,
        )
    else:
        # Default: treat as assertion
        move = DialogueMove(
            move_type="assert",
            content=head_plan.content,
            speaker=new_state.agent_id,
        )

    # Add to agenda
    new_state.private.agenda.append(move)

    # Mark head plan as completed
    head_plan.complete()

    return new_state


def _select_answer_to_qud(state: InformationState) -> InformationState:
    """Select answer to top QUD question.

    IBiS1 Rule: SelectAnswer (Section 2.9.4)
    Effect: add(shared.next_moves, answer(answer))
    """
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


def _select_ask_qud(state: InformationState) -> InformationState:
    """Select ask move for top QUD question.

    IBiS1 Rule: SelectAsk (Section 2.9.2)
    Effect: add(shared.next_moves, ask(Q))
    """
    new_state = state.clone()

    top_question = new_state.shared.top_qud()
    if not top_question:
        return new_state

    # Create ask move with the question
    move = DialogueMove(
        move_type="ask",
        content=top_question,
        speaker=new_state.agent_id,
    )
    new_state.private.agenda.append(move)

    return new_state


def _select_greeting(state: InformationState) -> InformationState:
    """Select greeting move.

    IBiS1 Rule: SelectGreet (Section 2.9)
    Effect: add(shared.next_moves, greet())
    """
    new_state = state.clone()

    # Create greeting move
    move = DialogueMove(
        move_type="greet",
        content="greeting_response",
        speaker=new_state.agent_id,
    )
    new_state.private.agenda.append(move)

    return new_state


def _select_fallback_response(state: InformationState) -> InformationState:
    """Select fallback response when no other rule applies.

    This is not part of IBiS1 but provides a safety net.
    """
    new_state = state.clone()

    # Create a simple acknowledgment
    move = DialogueMove(
        move_type="assert",
        content="I understand.",
        speaker=new_state.agent_id,
    )
    new_state.private.agenda.append(move)

    return new_state
