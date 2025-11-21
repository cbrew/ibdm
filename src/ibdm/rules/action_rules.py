"""Action execution rules for IBiS-4 action-oriented dialogue.

Implements action execution mechanisms from Larsson (2002) Chapter 5 Section 5.6:
- Action execution with precondition checking
- Action confirmation before execution
- Result handling (success/failure)
- Action rollback on failure

Based on Larsson (2002) Section 5.6 (Action Execution).
"""

from ibdm.core import Answer, InformationState
from ibdm.core.actions import Action
from ibdm.interfaces.device import ActionResult, DeviceInterface
from ibdm.rules.update_rules import UpdateRule


def create_action_integration_rules() -> list[UpdateRule]:
    """Create IBiS-4 action execution integration rules.

    Returns rules for executing actions and handling results:
    - Execute pending actions
    - Process action results (add postconditions, handle errors)
    - Rollback failed actions

    Based on Larsson Section 5.6.

    Returns:
        List of action integration rules
    """
    return [
        # Execute action - run pending actions via device interface
        UpdateRule(
            name="execute_action",
            preconditions=_has_action_to_execute,
            effects=_execute_action,
            priority=10,  # After integration, before selection
            rule_type="integration",
        ),
        # Process action result - handle success/failure
        UpdateRule(
            name="process_action_result",
            preconditions=_has_action_result_to_process,
            effects=_process_action_result,
            priority=9,  # After execution
            rule_type="integration",
        ),
    ]


def create_action_selection_rules() -> list[UpdateRule]:
    """Create action selection rules.

    Returns selection rules for action confirmation and feedback:
    - Request confirmation before critical actions
    - Generate action feedback messages

    Based on Larsson Section 5.6.4.

    Returns:
        List of action selection rules
    """
    return [
        # Request confirmation before executing action
        UpdateRule(
            name="request_action_confirmation",
            preconditions=_should_confirm_action,
            effects=_request_action_confirmation,
            priority=20,  # High priority - check before execution
            rule_type="selection",
        ),
    ]


# ============================================================================
# Precondition Functions
# ============================================================================


def _has_action_to_execute(state: InformationState) -> bool:
    """Check if there are actions ready for execution.

    Actions are ready when:
    - Action is in private.actions queue
    - Action is confirmed (if confirmation was required)
    - Action has not been executed yet

    Args:
        state: Current information state

    Returns:
        True if actions are ready for execution
    """
    if not state.private.actions:
        return False

    # Check if first action is ready (confirmed or doesn't need confirmation)
    action = state.private.actions[0]

    # Check if action needs confirmation
    if _action_needs_confirmation(action):
        # Check if we received confirmation
        if state.private.last_utterance:
            move = state.private.last_utterance
            if move.move_type == "answer" and isinstance(move.content, Answer):
                answer_text = str(move.content.content).lower()
                if answer_text in ["yes", "ok", "sure", "confirm"]:
                    return True
                elif answer_text in ["no", "cancel"]:
                    # User cancelled - remove action
                    return False
        return False  # Still waiting for confirmation

    # Action doesn't need confirmation - ready to execute
    return True


def _has_action_result_to_process(state: InformationState) -> bool:
    """Check if there are action results to process.

    Results are stored in beliefs["action_result"] after execution.

    Args:
        state: Current information state

    Returns:
        True if action results need processing
    """
    return "action_result" in state.private.beliefs


def _should_confirm_action(state: InformationState) -> bool:
    """Check if we should request confirmation for pending action.

    Confirmation is requested for:
    - Critical actions (booking, payment, deletion)
    - Actions with significant side effects
    - Actions that haven't been confirmed yet

    Args:
        state: Current information state

    Returns:
        True if confirmation should be requested
    """
    if not state.private.actions:
        return False

    action = state.private.actions[0]

    # Check if action needs confirmation
    if not _action_needs_confirmation(action):
        return False

    # Check if we already requested confirmation
    if state.private.agenda:
        last_agenda_item = state.private.agenda[-1]
        if (
            hasattr(last_agenda_item, "metadata")
            and last_agenda_item.metadata
            and last_agenda_item.metadata.get("confirmation_request")
        ):
            return False  # Already requested

    return True


# ============================================================================
# Effect Functions
# ============================================================================


def _execute_action(state: InformationState) -> InformationState:
    """Execute pending action via device interface.

    Executes the first action in private.actions queue:
    1. Get device interface from beliefs (injected by dialogue engine)
    2. Check preconditions
    3. Execute action
    4. Store result in beliefs for processing

    Based on Larsson Section 5.6.2 (ExecuteAction rule).

    Args:
        state: Current information state

    Returns:
        Updated state with action result in beliefs
    """
    if not state.private.actions:
        return state

    new_state = state.clone()
    action = new_state.private.actions[0]

    # Get device interface from beliefs (injected by engine)
    device: DeviceInterface | None = new_state.private.beliefs.get("device_interface")
    domain = new_state.private.beliefs.get("domain_model")

    # Execute action
    try:
        if device is not None:
            result = device.execute_action(action, new_state)
        elif domain is not None:
            # Simulate execution using domain postconditions
            from ibdm.interfaces.device import ActionResult, ActionStatus

            postconds = [str(p) for p in domain.postcond(action)]
            result = ActionResult(
                status=ActionStatus.SUCCESS,
                action=action,
                return_value=None,
                postconditions=postconds,
            )
        else:
            from ibdm.interfaces.device import ActionResult, ActionStatus

            result = ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message="No device interface available",
            )
        new_state.private.beliefs["action_result"] = result
    except Exception as e:
        # Handle execution errors
        from ibdm.interfaces.device import ActionResult, ActionStatus

        result = ActionResult(
            status=ActionStatus.FAILURE,
            action=action,
            error_message=f"Execution error: {e}",
        )
        new_state.private.beliefs["action_result"] = result

    return new_state


def _process_action_result(state: InformationState) -> InformationState:
    """Process action execution result.

    Handles both successful and failed action execution:
    - Success: Add postconditions to commitments, remove action from queue
    - Failure: Store error, prepare error message for user
    - Rollback: Undo changes if needed (for critical failures)

    Based on Larsson Section 5.6.2.

    Args:
        state: Current information state

    Returns:
        Updated state with result processed
    """
    if "action_result" not in state.private.beliefs:
        return state

    new_state = state.clone()
    result: ActionResult = new_state.private.beliefs["action_result"]

    # Remove the executed action from queue
    if new_state.private.actions and new_state.private.actions[0] == result.action:
        new_state.private.actions.pop(0)

    if result.is_successful():
        # Add postconditions to commitments
        for postcond in result.postconditions:
            new_state.shared.commitments.add(postcond)

        # Store success feedback in beliefs for generation
        new_state.private.beliefs["action_feedback"] = {
            "status": "success",
            "action": result.action.name,
            "message": f"Successfully executed {result.action.name}",
        }

    elif result.is_failed():
        # Handle failure
        new_state.private.beliefs["action_feedback"] = {
            "status": "failure",
            "action": result.action.name,
            "error": result.error_message,
            "message": f"Failed to execute {result.action.name}: {result.error_message}",
        }

        # Check if we should rollback
        if _should_rollback(result, new_state):
            new_state = _rollback_action(result.action, new_state)

    # Clear action result
    del new_state.private.beliefs["action_result"]

    return new_state


def _request_action_confirmation(state: InformationState) -> InformationState:
    """Request user confirmation before executing action.

    Generates a confirmation question and adds it to agenda:
    "Execute [action] with [parameters], is that correct?"

    Based on Larsson Section 5.6.4 (Confirmation before Action).

    Args:
        state: Current information state

    Returns:
        Updated state with confirmation request in agenda
    """
    if not state.private.actions:
        return state

    new_state = state.clone()
    action = new_state.private.actions[0]

    # Create confirmation question
    from ibdm.core.moves import DialogueMove
    from ibdm.core.questions import YNQuestion

    # Format action parameters for confirmation
    param_str = ", ".join(f"{k}={v}" for k, v in action.parameters.items())
    confirmation_text = f"Execute {action.name} with {param_str}, is that correct?"

    confirmation_question = YNQuestion(proposition=confirmation_text)

    confirmation_move = DialogueMove(
        speaker="system",
        move_type="ask",
        content=confirmation_question,
        metadata={
            "confirmation_request": True,
            "action": action.to_dict(),
        },
    )

    # Add to agenda
    new_state.private.agenda.append(confirmation_move)

    return new_state


# ============================================================================
# Rollback Functions
# ============================================================================


def _should_rollback(result: ActionResult, state: InformationState) -> bool:
    """Check if action should be rolled back.

    Rollback is needed when:
    - Action failed and has side effects that were committed
    - Action was part of a multi-step transaction
    - Failure affects dependent actions

    Args:
        result: Action execution result
        state: Current information state

    Returns:
        True if rollback is needed
    """
    # Get domain to check what postconditions this action would have created
    from ibdm.core.domain import DomainModel

    domain: DomainModel | None = state.private.beliefs.get("domain")

    if domain:
        # Get postconditions for this action
        postconds = domain.postcond(result.action)

        # Check if any of these postconditions exist in commitments
        for postcond in postconds:
            postcond_str = (
                f"{postcond.predicate}("
                f"{', '.join(f'{k}={v}' for k, v in postcond.arguments.items())})"
            )
            if postcond_str in state.shared.commitments:
                return True  # Need to rollback - postcondition was committed

    return False


def _rollback_action(action: Action, state: InformationState) -> InformationState:
    """Rollback failed action by removing its effects.

    Removes postconditions that were added to commitments.
    Notifies user of rollback.

    Based on Larsson Section 5.6.3 (Error Recovery).

    Args:
        action: Action to rollback
        state: Current information state

    Returns:
        Updated state with rollback applied
    """
    new_state = state.clone()

    # Get domain to compute postconditions
    from ibdm.core.domain import DomainModel

    domain: DomainModel | None = new_state.private.beliefs.get("domain")

    if domain:
        # Get postconditions that should be removed
        postconds = domain.postcond(action)
        postcond_strs = [
            f"{p.predicate}({', '.join(f'{k}={v}' for k, v in p.arguments.items())})"
            for p in postconds
        ]

        # Remove from commitments
        for postcond_str in postcond_strs:
            new_state.shared.commitments.discard(postcond_str)

    # Add rollback notification to beliefs
    new_state.private.beliefs["rollback_performed"] = {
        "action": action.name,
        "reason": "Action failed after partial execution",
    }

    return new_state


# ============================================================================
# Helper Functions
# ============================================================================


def _action_needs_confirmation(action: Action) -> bool:
    """Check if action requires user confirmation.

    Critical actions that need confirmation:
    - Booking/reservation actions
    - Payment/financial actions
    - Deletion/destructive actions
    - Actions with irreversible side effects

    Args:
        action: Action to check

    Returns:
        True if confirmation is required
    """
    critical_action_types = {
        "book",
        "reserve",
        "purchase",
        "pay",
        "delete",
        "cancel",
        "modify",
    }

    # Check if action type is critical
    action_type = (
        action.action_type.value
        if hasattr(action.action_type, "value")
        else str(action.action_type)
    )
    if action_type.lower() in critical_action_types:
        return True

    # Check action name
    action_name_lower = action.name.lower()
    for critical_type in critical_action_types:
        if critical_type in action_name_lower:
            return True

    return False
