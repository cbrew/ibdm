"""Unit tests for device interface protocol.

Tests the abstract DeviceInterface, ActionResult, and ActionStatus.
"""

from ibdm.core.actions import Action, ActionType
from ibdm.core.information_state import InformationState
from ibdm.interfaces.device import (
    ActionResult,
    ActionStatus,
    DeviceInterface,
)


# Concrete implementation for testing
class MockDevice(DeviceInterface):
    """Mock device implementation for testing."""

    def __init__(self) -> None:
        """Initialize mock device."""
        self.execution_count = 0
        self.should_fail = False
        self.should_fail_preconditions = False

    def execute_action(self, action: Action, state: InformationState) -> ActionResult:
        """Execute action (mock)."""
        self.execution_count += 1

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
                error_message="Simulated device failure",
            )

        # Success
        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={"confirmation": "MOCK123"},
            postconditions=self.get_postconditions(action),
        )

    def check_preconditions(self, action: Action, state: InformationState) -> bool:
        """Check if action preconditions are satisfied."""
        if self.should_fail_preconditions:
            return False

        # Check that all declared preconditions are in commitments
        for precond in action.preconditions:
            if precond not in state.shared.commitments:
                return False

        return True

    def get_postconditions(self, action: Action) -> list[str]:
        """Get postconditions for action."""
        # Simple postcondition generation
        return [f"executed({action.name})"]


class TestActionStatus:
    """Test ActionStatus enum."""

    def test_action_status_values(self) -> None:
        """Test that ActionStatus has expected values."""
        assert ActionStatus.SUCCESS.value == "success"
        assert ActionStatus.FAILURE.value == "failure"
        assert ActionStatus.PRECONDITION_FAILED.value == "precondition_failed"
        assert ActionStatus.TIMEOUT.value == "timeout"
        assert ActionStatus.CANCELLED.value == "cancelled"
        assert ActionStatus.PENDING.value == "pending"


class TestActionResult:
    """Test ActionResult dataclass."""

    def test_action_result_success(self) -> None:
        """Test successful ActionResult."""
        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H123"},
        )

        result = ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={"confirmation_number": "ABC123"},
            postconditions=["booked(hotel_id=H123)"],
        )

        assert result.is_successful()
        assert not result.is_failed()
        assert result.status == ActionStatus.SUCCESS
        assert result.return_value == {"confirmation_number": "ABC123"}
        assert "booked(hotel_id=H123)" in result.postconditions

    def test_action_result_failure(self) -> None:
        """Test failed ActionResult."""
        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
        )

        result = ActionResult(
            status=ActionStatus.FAILURE,
            action=action,
            error_message="Network error",
        )

        assert not result.is_successful()
        assert result.is_failed()
        assert result.error_message == "Network error"

    def test_action_result_precondition_failed(self) -> None:
        """Test ActionResult with precondition failure."""
        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            preconditions=["check_in_date_known"],
        )

        result = ActionResult(
            status=ActionStatus.PRECONDITION_FAILED,
            action=action,
            error_message="Missing check_in_date",
        )

        assert not result.is_successful()
        assert result.is_failed()
        assert result.status == ActionStatus.PRECONDITION_FAILED

    def test_action_result_timeout(self) -> None:
        """Test ActionResult with timeout."""
        action = Action(action_type=ActionType.GET, name="fetch_data")

        result = ActionResult(
            status=ActionStatus.TIMEOUT,
            action=action,
            error_message="Request timed out after 30s",
        )

        assert not result.is_successful()
        assert result.is_failed()

    def test_action_result_pending(self) -> None:
        """Test ActionResult with pending status."""
        action = Action(action_type=ActionType.EXECUTE, name="long_running_task")

        result = ActionResult(
            status=ActionStatus.PENDING,
            action=action,
        )

        assert not result.is_successful()
        assert not result.is_failed()  # Pending is not failed

    def test_action_result_str(self) -> None:
        """Test ActionResult string representation."""
        action = Action(action_type=ActionType.BOOK, name="book_hotel")

        # Success
        result = ActionResult(status=ActionStatus.SUCCESS, action=action)
        assert "SUCCESS" in str(result)
        assert "book_hotel" in str(result)

        # Failure
        result = ActionResult(
            status=ActionStatus.FAILURE, action=action, error_message="Test error"
        )
        assert "failure" in str(result)
        assert "Test error" in str(result)


class TestDeviceInterface:
    """Test DeviceInterface abstract class."""

    def test_execute_action_success(self) -> None:
        """Test successful action execution."""
        device = MockDevice()
        state = InformationState()
        state.shared.commitments.add("check_in_date_known")

        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H123"},
            preconditions=["check_in_date_known"],
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert device.execution_count == 1
        assert result.return_value == {"confirmation": "MOCK123"}
        assert "executed(book_hotel)" in result.postconditions

    def test_execute_action_precondition_failure(self) -> None:
        """Test action execution with precondition failure."""
        device = MockDevice()
        state = InformationState()  # Empty commitments

        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            preconditions=["check_in_date_known"],  # Not in commitments
        )

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert result.status == ActionStatus.PRECONDITION_FAILED
        assert "Preconditions not satisfied" in result.error_message

    def test_execute_action_device_failure(self) -> None:
        """Test action execution with device failure."""
        device = MockDevice()
        device.should_fail = True
        state = InformationState()

        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
        )

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert result.status == ActionStatus.FAILURE
        assert "Simulated device failure" in result.error_message

    def test_check_preconditions_satisfied(self) -> None:
        """Test precondition checking when satisfied."""
        device = MockDevice()
        state = InformationState()
        state.shared.commitments.add("check_in_date_known")
        state.shared.commitments.add("check_out_date_known")

        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            preconditions=["check_in_date_known", "check_out_date_known"],
        )

        assert device.check_preconditions(action, state)

    def test_check_preconditions_not_satisfied(self) -> None:
        """Test precondition checking when not satisfied."""
        device = MockDevice()
        state = InformationState()
        state.shared.commitments.add("check_in_date_known")
        # Missing check_out_date_known

        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            preconditions=["check_in_date_known", "check_out_date_known"],
        )

        assert not device.check_preconditions(action, state)

    def test_check_preconditions_empty(self) -> None:
        """Test precondition checking with no preconditions."""
        device = MockDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            preconditions=[],  # No preconditions
        )

        assert device.check_preconditions(action, state)

    def test_get_postconditions(self) -> None:
        """Test postcondition generation."""
        device = MockDevice()

        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H123"},
        )

        postconds = device.get_postconditions(action)

        assert len(postconds) > 0
        assert "executed(book_hotel)" in postconds

    def test_get_name(self) -> None:
        """Test device name retrieval."""
        device = MockDevice()
        assert device.get_name() == "MockDevice"

    def test_supports_action_type_default(self) -> None:
        """Test that device supports all action types by default."""
        device = MockDevice()

        assert device.supports_action_type("book")
        assert device.supports_action_type("cancel")
        assert device.supports_action_type("set")
        assert device.supports_action_type("custom_action")


class TestDeviceIntegration:
    """Integration tests for device interface with actions."""

    def test_full_action_execution_flow(self) -> None:
        """Test complete action execution flow."""
        # Setup
        device = MockDevice()
        state = InformationState()
        state.shared.commitments.add("check_in_date_known")
        state.shared.commitments.add("check_out_date_known")
        state.shared.commitments.add("hotel_selected")

        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H123", "check_in": "2025-01-05"},
            preconditions=["check_in_date_known", "check_out_date_known", "hotel_selected"],
            requires_confirmation=True,
        )

        # Execute
        result = device.execute_action(action, state)

        # Verify
        assert result.is_successful()
        assert result.postconditions == ["executed(book_hotel)"]
        assert result.return_value is not None
        assert device.execution_count == 1

    def test_action_execution_with_metadata(self) -> None:
        """Test action execution with metadata tracking."""
        device = MockDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.GET,
            name="get_price",
            parameters={"destination": "Paris"},
            metadata={"user_id": "user123", "session_id": "sess456"},
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        # Action metadata should be preserved
        assert action.metadata["user_id"] == "user123"
