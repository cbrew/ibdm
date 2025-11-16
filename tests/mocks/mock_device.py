"""Mock device implementation for testing action execution.

Provides a configurable mock device that can simulate various action
execution scenarios without requiring real external systems.
"""

from collections.abc import Callable

from ibdm.core.actions import Action
from ibdm.core.information_state import InformationState
from ibdm.interfaces.device import ActionResult, ActionStatus, DeviceInterface


class MockDevice(DeviceInterface):
    """Configurable mock device for testing.

    Features:
    - Tracks all executed actions
    - Simulates success, failure, and precondition failures
    - Configurable postconditions
    - Parameter validation
    - Commitment checking

    Example:
        >>> device = MockDevice()
        >>> device.configure(should_fail=False)
        >>> action = Action(action_type=ActionType.BOOK, name="book_hotel")
        >>> result = device.execute_action(action, state)
        >>> assert result.is_successful()
        >>> assert len(device.action_history) == 1
    """

    def __init__(self) -> None:
        """Initialize mock device with default configuration."""
        # Execution tracking
        self.execution_count = 0
        self.action_history: list[tuple[Action, InformationState]] = []

        # Configuration flags
        self.should_fail = False
        self.should_fail_preconditions = False
        self.failure_message = "Simulated device failure"

        # Custom precondition and postcondition functions
        self._custom_precond_fn: Callable[[Action, InformationState], bool] | None = None
        self._custom_postcond_fn: Callable[[Action], list[str]] | None = None

    def configure(
        self,
        should_fail: bool = False,
        should_fail_preconditions: bool = False,
        failure_message: str = "Simulated device failure",
    ) -> None:
        """Configure mock device behavior.

        Args:
            should_fail: If True, execute_action() returns FAILURE status
            should_fail_preconditions: If True, preconditions always fail
            failure_message: Error message when should_fail is True
        """
        self.should_fail = should_fail
        self.should_fail_preconditions = should_fail_preconditions
        self.failure_message = failure_message

    def set_custom_precond_function(
        self, fn: Callable[[Action, InformationState], bool]
    ) -> None:
        """Set custom precondition checker.

        Args:
            fn: Function that takes (Action, InformationState) and returns bool
        """
        self._custom_precond_fn = fn

    def set_custom_postcond_function(self, fn: Callable[[Action], list[str]]) -> None:
        """Set custom postcondition generator.

        Args:
            fn: Function that takes Action and returns list of postcondition strings
        """
        self._custom_postcond_fn = fn

    def reset(self) -> None:
        """Reset device state and history."""
        self.execution_count = 0
        self.action_history = []
        self.should_fail = False
        self.should_fail_preconditions = False
        self.failure_message = "Simulated device failure"
        self._custom_precond_fn = None
        self._custom_postcond_fn = None

    def execute_action(
        self, action: Action, state: InformationState
    ) -> ActionResult:
        """Execute action (mock implementation).

        Records the action and returns configured result.

        Args:
            action: Action to execute
            state: Current information state

        Returns:
            ActionResult with configured status
        """
        self.execution_count += 1
        self.action_history.append((action, state))

        # Check preconditions
        if not self.check_preconditions(action, state):
            return ActionResult(
                status=ActionStatus.PRECONDITION_FAILED,
                action=action,
                error_message="Preconditions not satisfied",
            )

        # Simulate failure
        if self.should_fail:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=self.failure_message,
            )

        # Success
        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={"confirmation": f"MOCK_{self.execution_count:03d}"},
            postconditions=self.get_postconditions(action),
        )

    def check_preconditions(self, action: Action, state: InformationState) -> bool:
        """Check if action preconditions are satisfied.

        Args:
            action: Action to check
            state: Current information state

        Returns:
            True if preconditions are satisfied
        """
        # Use custom precondition function if provided
        if self._custom_precond_fn is not None:
            return self._custom_precond_fn(action, state)

        # Configuration override
        if self.should_fail_preconditions:
            return False

        # Check action's declared preconditions against commitments
        for precond in action.preconditions:
            if precond not in state.shared.commitments:
                # Also check for prefix match
                # e.g., "check_in_date" matches "check_in_date: 2025-01-05"
                if not any(c.startswith(precond) for c in state.shared.commitments):
                    return False

        return True

    def get_postconditions(self, action: Action) -> list[str]:
        """Get postconditions for action.

        Args:
            action: Action to get postconditions for

        Returns:
            List of postcondition strings
        """
        # Use custom postcondition function if provided
        if self._custom_postcond_fn is not None:
            return self._custom_postcond_fn(action)

        # Default: generate simple postcondition
        return [f"executed({action.name})"]

    def get_last_action(self) -> tuple[Action, InformationState] | None:
        """Get the last executed action and state.

        Returns:
            Tuple of (Action, InformationState), or None if no actions executed
        """
        if self.action_history:
            return self.action_history[-1]
        return None

    def get_action_count(self, action_name: str) -> int:
        """Count how many times an action was executed.

        Args:
            action_name: Name of action to count

        Returns:
            Number of times action was executed
        """
        return sum(1 for action, _ in self.action_history if action.name == action_name)
