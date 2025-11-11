"""Task accommodation for resolving underspecified requests.

Task accommodation resolves requests and commands that may be incomplete
or reference previous context.
"""

from ibdm.core import DialogueMove, InformationState


def accommodate_task(task: str, state: InformationState) -> DialogueMove:
    """Accommodate an underspecified task/request using dialogue context.

    This function resolves:
    - Underspecified requests (e.g., "Do that" → resolve "that")
    - Follow-up requests (e.g., "Also show..." → add to current task)
    - Abbreviated commands (e.g., "Cancel" → resolve what to cancel)

    Args:
        task: The task description to accommodate
        state: Current information state with context

    Returns:
        Dialogue move representing the accommodated task
    """
    task_lower = task.lower().strip()

    # Handle anaphoric references in tasks
    if any(pron in task_lower for pron in ["that", "it", "this", "them"]):
        resolved_task = _resolve_task_anaphora(task, state)
        return DialogueMove(
            move_type="request",
            content=resolved_task,
            speaker=state.control.speaker,
        )

    # Handle follow-up tasks (starting with "also", "and", etc.)
    if task_lower.startswith(("also ", "and ", "then ")):
        # Remove the connector
        for connector in ["also ", "and ", "then "]:
            if task_lower.startswith(connector):
                task = task[len(connector) :]
                break

        # Check if there's an active plan
        if state.private.plan:
            # This is a subtask of the current plan
            current_plan = state.private.plan[-1]
            return DialogueMove(
                move_type="request",
                content=task,
                speaker=state.control.speaker,
            )

    # Handle abbreviated cancellations
    if task_lower in ["cancel", "stop", "abort"]:
        # Infer what to cancel from context
        if state.private.plan:
            current_plan = state.private.plan[-1]
            return DialogueMove(
                move_type="request",
                content=f"cancel {current_plan.goal}",
                speaker=state.control.speaker,
            )
        elif state.shared.qud:
            # Cancel the current QUD
            return DialogueMove(
                move_type="request",
                content="cancel current question",
                speaker=state.control.speaker,
            )

    # Default: treat as-is
    return DialogueMove(
        move_type="request",
        content=task,
        speaker=state.control.speaker,
    )


def _resolve_task_anaphora(task: str, state: InformationState) -> str:
    """Resolve anaphoric references in a task description.

    Replaces pronouns like "that", "it", "this" with their referents.
    """
    task_lower = task.lower()

    # Try to resolve from recent assertions or answers
    if state.shared.last_moves:
        for move in reversed(state.shared.last_moves):
            if move.move_type == "assert":
                # Replace anaphora with the assertion content
                for pron in ["that", "it", "this"]:
                    if pron in task_lower:
                        return task.replace(pron, str(move.content))
            elif move.move_type == "answer":
                # Replace with answer content
                for pron in ["that", "it", "this"]:
                    if pron in task_lower:
                        answer_content = str(move.content)
                        return task.replace(pron, answer_content)

    # Try to resolve from current plan
    if state.private.plan:
        current_plan = state.private.plan[-1]
        for pron in ["that", "it", "this"]:
            if pron in task_lower:
                return task.replace(pron, current_plan.goal)

    # Couldn't resolve - return original
    return task
