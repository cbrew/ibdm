"""Integration rules for Issue-Based Dialogue Management.

Integration rules update the information state based on dialogue moves.
They manage the QUD stack, commitments, and agenda.

Task plan formation (creating plans for user tasks) happens here in the
integration phase, NOT in interpretation. This is the correct phase per
Larsson (2002).

Based on Larsson (2002) Issue-based Dialogue Management.
"""

from ibdm.core import Answer, DialogueMove, InformationState, Question
from ibdm.rules.update_rules import UpdateRule


def create_integration_rules() -> list[UpdateRule]:
    """Create standard integration rules.

    Returns:
        List of integration rules
    """
    return [
        # Task plan formation - create plans for command/request moves
        # This is THE RIGHT PLACE for task plan formation per Larsson (2002)
        # Renamed from "accommodate_command" to clarify this is task plan formation,
        # not Larsson's presupposition accommodation
        UpdateRule(
            name="form_task_plan",
            preconditions=_is_task_request_move,
            effects=_form_task_plan,
            priority=13,  # Highest - before other integrations
            rule_type="integration",
        ),
        # Command integration - treat commands like requests
        UpdateRule(
            name="integrate_command",
            preconditions=_is_command_move,
            effects=_integrate_command,
            priority=12,
            rule_type="integration",
        ),
        # Request integration - task accommodation (no QUD change needed, plan already created)
        UpdateRule(
            name="integrate_request",
            preconditions=_is_request_move,
            effects=_integrate_request,
            priority=11,
            rule_type="integration",
        ),
        # Question integration - push to QUD
        UpdateRule(
            name="integrate_question",
            preconditions=_is_ask_move,
            effects=_integrate_question,
            priority=10,
            rule_type="integration",
        ),
        # Answer integration - resolve QUD and add commitment
        UpdateRule(
            name="integrate_answer",
            preconditions=_is_answer_move,
            effects=_integrate_answer,
            priority=9,
            rule_type="integration",
        ),
        # Assertion integration - add to commitments
        UpdateRule(
            name="integrate_assertion",
            preconditions=_is_assert_move,
            effects=_integrate_assertion,
            priority=8,
            rule_type="integration",
        ),
        # Greet integration - update control
        UpdateRule(
            name="integrate_greet",
            preconditions=_is_greet_move,
            effects=_integrate_greet,
            priority=7,
            rule_type="integration",
        ),
        # Quit integration - end dialogue
        UpdateRule(
            name="integrate_quit",
            preconditions=_is_quit_move,
            effects=_integrate_quit,
            priority=7,
            rule_type="integration",
        ),
    ]


# Precondition functions


def _is_task_request_move(state: InformationState) -> bool:
    """Check if move is a command/request that requires task plan formation.

    This checks for command or request moves that indicate the user wants
    the system to perform a task (e.g., "I need to draft an NDA").
    """
    move = state.private.beliefs.get("_temp_move")
    if not isinstance(move, DialogueMove):
        return False

    # Check if it's a command or request move
    if move.move_type not in ["command", "request"]:
        return False

    # Check if it looks like a task request (has task metadata or keywords)
    metadata = move.metadata or {}
    task_type = metadata.get("task_type")
    intent = metadata.get("intent", "")

    # Check for explicit task type or draft-related intent
    if task_type or "draft" in intent.lower():
        return True

    # Check content for task keywords
    content_str = str(move.content).lower()
    task_keywords = ["draft", "create", "prepare", "need", "help"]
    return any(keyword in content_str for keyword in task_keywords)


def _is_command_move(state: InformationState) -> bool:
    """Check if the temporary move is a 'command' move."""
    move = state.private.beliefs.get("_temp_move")
    return isinstance(move, DialogueMove) and move.move_type == "command"


def _is_request_move(state: InformationState) -> bool:
    """Check if the temporary move is a 'request' move."""
    move = state.private.beliefs.get("_temp_move")
    return isinstance(move, DialogueMove) and move.move_type == "request"


def _is_ask_move(state: InformationState) -> bool:
    """Check if the temporary move is an 'ask' move."""
    move = state.private.beliefs.get("_temp_move")
    return isinstance(move, DialogueMove) and move.move_type == "ask"


def _is_answer_move(state: InformationState) -> bool:
    """Check if the temporary move is an 'answer' move."""
    move = state.private.beliefs.get("_temp_move")
    return isinstance(move, DialogueMove) and move.move_type == "answer"


def _is_assert_move(state: InformationState) -> bool:
    """Check if the temporary move is an 'assert' move."""
    move = state.private.beliefs.get("_temp_move")
    return isinstance(move, DialogueMove) and move.move_type == "assert"


def _is_greet_move(state: InformationState) -> bool:
    """Check if the temporary move is a 'greet' move."""
    move = state.private.beliefs.get("_temp_move")
    return isinstance(move, DialogueMove) and move.move_type == "greet"


def _is_quit_move(state: InformationState) -> bool:
    """Check if the temporary move is a 'quit' move."""
    move = state.private.beliefs.get("_temp_move")
    return isinstance(move, DialogueMove) and move.move_type == "quit"


# Effect functions


def _form_task_plan(state: InformationState) -> InformationState:
    """Form execution plan for user's task.

    RENAMED from _accommodate_task to clarify this is task plan formation,
    not Larsson's presupposition accommodation.

    Uses domain model to get appropriate plan via domain.get_plan().
    This replaces hardcoded plan creation with domain-driven approach.

    Args:
        state: Current information state

    Returns:
        New state with plan added and first question on QUD
    """
    move = state.private.beliefs.get("_temp_move")
    new_state = state.clone()

    if not isinstance(move, DialogueMove):
        return new_state

    # Extract task type from metadata or content
    metadata = move.metadata or {}
    task_type = metadata.get("task_type")
    intent = metadata.get("intent", "")

    # Determine which task this is
    # For now, check for NDA-related requests
    if (
        task_type == "DRAFT_DOCUMENT"
        or "draft" in intent.lower()
        or "NDA" in str(move.content).upper()
        or "nda" in str(move.content).lower()
        or "confidentiality" in str(move.content).lower()
    ):
        # Get NDA domain and create plan using domain model
        from ibdm.domains.nda_domain import get_nda_domain

        domain = get_nda_domain()

        # Use domain to get plan (not hardcoded!)
        context = _extract_context(move, state)
        plan = domain.get_plan("nda_drafting", context)

        # Add plan to state
        new_state.private.plan.append(plan)

        # Push first question to QUD
        if plan.subplans and len(plan.subplans) > 0:
            first_subplan = plan.subplans[0]
            if first_subplan.content and isinstance(first_subplan.content, Question):
                new_state.shared.push_qud(first_subplan.content)

    # Add move to history
    new_state.shared.last_moves.append(move)

    # System should respond
    new_state.control.next_speaker = new_state.agent_id

    return new_state


def _extract_context(move: DialogueMove, state: InformationState) -> dict:
    """Extract context from move for plan building.

    Args:
        move: The dialogue move
        state: Current information state

    Returns:
        Context dictionary for plan builder

    Note:
        Currently returns empty dict. Future enhancements could extract
        entities, intent details, etc. from move metadata.
    """
    # Can extract entities, intent details, etc.
    # For now, return empty context
    return {}


def _integrate_command(state: InformationState) -> InformationState:
    """Integrate a 'command' move by treating it like a request.

    Command moves (like "I need to draft an NDA") trigger task accommodation.
    Commands are similar to requests - they express user goals/intentions.
    """
    new_state = state.clone()
    move = new_state.private.beliefs.get("_temp_move")

    if not isinstance(move, DialogueMove):
        return new_state

    # Add to last_moves for history
    new_state.shared.last_moves.append(move)

    # System should respond to the command
    new_state.control.next_speaker = new_state.agent_id

    return new_state


def _integrate_request(state: InformationState) -> InformationState:
    """Integrate a 'request' move by acknowledging task request.

    Request moves (like "I need to draft an NDA") trigger task accommodation.
    The interpretation rule already created the plan, so this just tracks the move.
    """
    new_state = state.clone()
    move = new_state.private.beliefs.get("_temp_move")

    if not isinstance(move, DialogueMove):
        return new_state

    # Add to last_moves for history
    new_state.shared.last_moves.append(move)

    # System should respond with first question from plan
    new_state.control.next_speaker = new_state.agent_id

    return new_state


def _integrate_question(state: InformationState) -> InformationState:
    """Integrate an 'ask' move by pushing question to QUD.

    When a question is asked, it becomes the new top issue under discussion.
    """
    new_state = state.clone()
    move = new_state.private.beliefs.get("_temp_move")

    if not isinstance(move, DialogueMove):
        return new_state

    if isinstance(move.content, Question):
        # Push question to QUD stack
        new_state.shared.push_qud(move.content)

        # Add to last_moves for history
        new_state.shared.last_moves.append(move)

        # Set next speaker to the system (if user asked)
        if move.speaker != new_state.agent_id:
            new_state.control.next_speaker = new_state.agent_id
        else:
            # If system asked, wait for user response
            new_state.control.next_speaker = "user"

    return new_state


def _integrate_answer(state: InformationState) -> InformationState:
    """Integrate an 'answer' move by resolving QUD and updating commitments.

    When an answer is provided:
    1. Check if it resolves the top QUD
    2. If so, pop the question from QUD
    3. Add the answer as a shared commitment
    """
    new_state = state.clone()
    move = new_state.private.beliefs.get("_temp_move")

    if not isinstance(move, DialogueMove):
        return new_state

    if isinstance(move.content, Answer):
        answer = move.content

        # Check if this answer resolves the top QUD
        top_question = new_state.shared.top_qud()
        if top_question and top_question.resolves_with(answer):
            # Pop the resolved question
            new_state.shared.pop_qud()

            # Add answer as a commitment (convert to string for simplicity)
            commitment = f"{top_question}: {answer.content}"
            new_state.shared.commitments.add(commitment)

        # Add to last_moves
        new_state.shared.last_moves.append(move)

        # Switch turn (if user answered, system's turn next)
        if move.speaker != new_state.agent_id:
            new_state.control.next_speaker = new_state.agent_id
        else:
            # If system answered, check if there are more QUDs
            if new_state.shared.qud:
                new_state.control.next_speaker = new_state.agent_id
            else:
                new_state.control.next_speaker = "user"

    return new_state


def _integrate_assertion(state: InformationState) -> InformationState:
    """Integrate an 'assert' move by adding to commitments.

    Assertions are added to the shared commitment store.
    """
    new_state = state.clone()
    move = new_state.private.beliefs.get("_temp_move")

    if not isinstance(move, DialogueMove):
        return new_state

    # Add assertion to commitments
    if move.content:
        new_state.shared.commitments.add(str(move.content))

    # Add to last_moves
    new_state.shared.last_moves.append(move)

    # Switch turn
    if move.speaker != new_state.agent_id:
        new_state.control.next_speaker = new_state.agent_id
    else:
        new_state.control.next_speaker = "user"

    return new_state


def _integrate_greet(state: InformationState) -> InformationState:
    """Integrate a 'greet' move by updating control state.

    Greetings typically prompt a greeting response.
    """
    new_state = state.clone()
    move = new_state.private.beliefs.get("_temp_move")

    if not isinstance(move, DialogueMove):
        return new_state

    # Add to last_moves
    new_state.shared.last_moves.append(move)

    # Set dialogue to active
    new_state.control.dialogue_state = "active"

    # Switch turn
    if move.speaker != new_state.agent_id:
        # User greeted, system should respond
        new_state.control.next_speaker = new_state.agent_id
        # Add a greeting to agenda
        greeting_move = DialogueMove(
            move_type="greet",
            content="greeting_response",
            speaker=new_state.agent_id,
        )
        new_state.private.agenda.append(greeting_move)
    else:
        new_state.control.next_speaker = "user"

    return new_state


def _integrate_quit(state: InformationState) -> InformationState:
    """Integrate a 'quit' move by ending the dialogue.

    Quit moves set the dialogue state to 'ended'.
    """
    new_state = state.clone()
    move = new_state.private.beliefs.get("_temp_move")

    if not isinstance(move, DialogueMove):
        return new_state

    # Add to last_moves
    new_state.shared.last_moves.append(move)

    # End the dialogue
    new_state.control.dialogue_state = "ended"

    # If user quit, system should acknowledge
    if move.speaker != new_state.agent_id:
        new_state.control.next_speaker = new_state.agent_id
        # Add a quit response to agenda
        quit_move = DialogueMove(
            move_type="quit",
            content="quit_response",
            speaker=new_state.agent_id,
        )
        new_state.private.agenda.append(quit_move)
    else:
        new_state.control.next_speaker = "user"

    return new_state
