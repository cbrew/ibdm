"""Device interface protocol for action execution.

Defines the abstract interface for connecting dialogue systems to external
devices and systems for executing non-communicative actions.

Based on Larsson (2002) Section 5.3.2 (Device Actions) and Section 5.6.2
(Action Execution).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from ibdm.core.actions import Action
from ibdm.core.information_state import InformationState


class ActionStatus(Enum):
    """Status of an action execution.

    Based on Larsson Section 5.6.2 (Action Execution and Results).
    """

    SUCCESS = "success"
    """Action completed successfully"""

    FAILURE = "failure"
    """Action failed to execute"""

    PRECONDITION_FAILED = "precondition_failed"
    """Action preconditions not satisfied"""

    TIMEOUT = "timeout"
    """Action timed out"""

    CANCELLED = "cancelled"
    """Action was cancelled before completion"""

    PENDING = "pending"
    """Action is still executing (for async operations)"""


@dataclass
class ActionResult:
    """Result of an action execution.

    Encapsulates the outcome of executing an action on a device,
    including status, return values, and error information.

    Based on Larsson Section 5.6.2.

    Attributes:
        status: Execution status (success, failure, etc.)
        action: The action that was executed
        return_value: Value returned by the action (if any)
        error_message: Error description (if failed)
        postconditions: Propositions that became true (if successful)
        metadata: Additional result metadata (timestamps, logs, etc.)

    Example:
        >>> result = ActionResult(
        ...     status=ActionStatus.SUCCESS,
        ...     action=book_hotel_action,
        ...     return_value={"confirmation_number": "ABC123"},
        ...     postconditions=["booked(hotel_id=H123)"]
        ... )
    """

    status: ActionStatus
    """Execution status"""

    action: Action
    """The action that was executed"""

    return_value: Any = None
    """Value returned by the action"""

    error_message: str = ""
    """Error description if status is FAILURE or PRECONDITION_FAILED"""

    postconditions: list[str] = field(default_factory=lambda: [])
    """Propositions that became true after successful execution"""

    metadata: dict[str, Any] = field(default_factory=lambda: {})
    """Additional metadata (execution_time, device_id, logs, etc.)"""

    def is_successful(self) -> bool:
        """Check if action executed successfully."""
        return self.status == ActionStatus.SUCCESS

    def is_failed(self) -> bool:
        """Check if action failed."""
        return self.status in {
            ActionStatus.FAILURE,
            ActionStatus.PRECONDITION_FAILED,
            ActionStatus.TIMEOUT,
        }

    def __str__(self) -> str:
        """Return string representation."""
        if self.is_successful():
            return f"ActionResult(SUCCESS: {self.action.name})"
        else:
            return f"ActionResult({self.status.value}: {self.action.name} - {self.error_message})"


class DeviceInterface(ABC):
    """Abstract interface for device/system integration.

    Devices execute non-communicative actions requested by dialogue
    participants. This interface defines the contract for action execution,
    precondition checking, and postcondition generation.

    Based on Larsson (2002) Section 5.3.2 (Device Actions) and Section 5.6.2
    (Action Execution).

    Implementers should subclass this and provide device-specific logic.

    Example Implementation:
        >>> class HotelBookingDevice(DeviceInterface):
        ...     def execute_action(
        ...         self, action: Action, state: InformationState
        ...     ) -> ActionResult:
        ...         # Check preconditions first
        ...         if not self.check_preconditions(action, state):
        ...             return ActionResult(
        ...                 status=ActionStatus.PRECONDITION_FAILED,
        ...                 action=action,
        ...                 error_message="Missing required fields"
        ...             )
        ...
        ...         # Execute booking API call
        ...         try:
        ...             confirmation = self.api.book_hotel(
        ...                 hotel_id=action.parameters["hotel_id"],
        ...                 check_in=action.parameters["check_in"],
        ...                 check_out=action.parameters["check_out"]
        ...             )
        ...             return ActionResult(
        ...                 status=ActionStatus.SUCCESS,
        ...                 action=action,
        ...                 return_value={"confirmation_number": confirmation},
        ...                 postconditions=self.get_postconditions(action)
        ...             )
        ...         except Exception as e:
        ...             return ActionResult(
        ...                 status=ActionStatus.FAILURE,
        ...                 action=action,
        ...                 error_message=str(e)
        ...             )
        ...
        ...     def check_preconditions(
        ...         self, action: Action, state: InformationState
        ...     ) -> bool:
        ...         # Verify required parameters are present
        ...         return all(
        ...             param in action.parameters
        ...             for param in ["hotel_id", "check_in", "check_out"]
        ...         )
        ...
        ...     def get_postconditions(self, action: Action) -> list[str]:
        ...         # Generate postconditions from action
        ...         hotel_id = action.parameters.get("hotel_id", "unknown")
        ...         return [f"booked(hotel_id={hotel_id})"]
    """

    @abstractmethod
    def execute_action(self, action: Action, state: InformationState) -> ActionResult:
        """Execute an action on the device.

        This is the main entry point for action execution. Implementations
        should:
        1. Validate preconditions (optionally using check_preconditions)
        2. Perform the actual action (API call, database update, etc.)
        3. Return result with status and postconditions

        Based on Larsson Section 5.6.2 (ExecuteAction rule).

        Note: This is a synchronous interface. For long-running operations,
        implementations can return ActionStatus.PENDING and provide a
        separate polling mechanism.

        Args:
            action: The action to execute
            state: Current information state (for context/precondition checking)

        Returns:
            ActionResult with status, return value, and postconditions

        Raises:
            May raise exceptions that should be caught and converted to
            ActionResult with FAILURE status

        Example:
            >>> device = MyDevice()
            >>> action = Action(
            ...     action_type=ActionType.BOOK,
            ...     name="book_hotel",
            ...     parameters={"hotel_id": "H123"}
            ... )
            >>> result = device.execute_action(action, state)
            >>> if result.is_successful():
            ...     print(f"Success! Confirmation: {result.return_value}")
        """
        pass

    @abstractmethod
    def check_preconditions(self, action: Action, state: InformationState) -> bool:
        """Check if action preconditions are satisfied.

        Verifies that the action can be executed in the current state.
        This includes checking:
        - Required parameters are present
        - Required information is in commitments/beliefs
        - External conditions are met (e.g., device is available)

        Based on Larsson Section 5.6.2.

        Args:
            action: The action to check
            state: Current information state

        Returns:
            True if preconditions are satisfied, False otherwise

        Example:
            >>> action = Action(
            ...     action_type=ActionType.BOOK,
            ...     name="book_hotel",
            ...     preconditions=["check_in_date_known", "check_out_date_known"]
            ... )
            >>> can_execute = device.check_preconditions(action, state)
            >>> if not can_execute:
            ...     print("Missing required information")
        """
        pass

    @abstractmethod
    def get_postconditions(self, action: Action) -> list[str]:
        """Get postconditions that will be true after action execution.

        Generates the propositions that become true if the action executes
        successfully. These are added to commitments after execution.

        Based on Larsson Section 5.3.2 (Actions and Postconditions).

        Args:
            action: The action to get postconditions for

        Returns:
            List of postcondition predicates as strings

        Example:
            >>> action = Action(
            ...     action_type=ActionType.BOOK,
            ...     name="book_hotel",
            ...     parameters={"hotel_id": "H123"}
            ... )
            >>> postconds = device.get_postconditions(action)
            >>> # Returns: ["booked(hotel_id=H123)"]
        """
        pass

    def get_name(self) -> str:
        """Get device name for logging and identification.

        Returns:
            Human-readable device name

        Default implementation returns class name.
        """
        return self.__class__.__name__

    def supports_action_type(self, action_type: str) -> bool:
        """Check if this device supports a given action type.

        Args:
            action_type: Action type to check (e.g., "book", "cancel")

        Returns:
            True if this device can execute actions of this type

        Default implementation returns True for all types.
        Override to restrict to specific action types.
        """
        return True
