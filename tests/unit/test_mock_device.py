"""Unit tests for MockDevice.

Tests the configurable mock device implementation.
"""

import sys  # noqa: E402
from pathlib import Path  # noqa: E402

# Add tests directory to path to allow direct imports
tests_dir = Path(__file__).parent.parent
sys.path.insert(0, str(tests_dir))

from mocks.mock_device import MockDevice  # noqa: E402

from ibdm.core.actions import Action, ActionType  # noqa: E402
from ibdm.core.information_state import InformationState  # noqa: E402
from ibdm.interfaces.device import ActionStatus  # noqa: E402


class TestMockDeviceBasics:
    """Test basic MockDevice functionality."""

    def test_initialization(self) -> None:
        """Test MockDevice initialization."""
        device = MockDevice()

        assert device.execution_count == 0
        assert device.action_history == []
        assert not device.should_fail
        assert not device.should_fail_preconditions

    def test_execute_action_success(self) -> None:
        """Test successful action execution."""
        device = MockDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H123"},
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert result.status == ActionStatus.SUCCESS
        assert device.execution_count == 1
        assert len(device.action_history) == 1

    def test_execute_action_tracks_history(self) -> None:
        """Test that action history is tracked."""
        device = MockDevice()
        state = InformationState()

        action1 = Action(action_type=ActionType.BOOK, name="book_hotel")
        action2 = Action(action_type=ActionType.CANCEL, name="cancel_booking")

        device.execute_action(action1, state)
        device.execute_action(action2, state)

        assert device.execution_count == 2
        assert len(device.action_history) == 2
        assert device.action_history[0][0].name == "book_hotel"
        assert device.action_history[1][0].name == "cancel_booking"

    def test_return_value_includes_confirmation(self) -> None:
        """Test that return value includes confirmation number."""
        device = MockDevice()
        state = InformationState()

        action = Action(action_type=ActionType.BOOK, name="book_hotel")

        result = device.execute_action(action, state)

        assert result.return_value is not None
        assert "confirmation" in result.return_value
        assert result.return_value["confirmation"] == "MOCK_001"

    def test_postconditions_generated(self) -> None:
        """Test that postconditions are generated."""
        device = MockDevice()
        state = InformationState()

        action = Action(action_type=ActionType.BOOK, name="book_hotel")

        result = device.execute_action(action, state)

        assert result.postconditions == ["executed(book_hotel)"]


class TestMockDeviceConfiguration:
    """Test MockDevice configuration options."""

    def test_configure_should_fail(self) -> None:
        """Test configuring device to fail."""
        device = MockDevice()
        device.configure(should_fail=True)

        state = InformationState()
        action = Action(action_type=ActionType.BOOK, name="book_hotel")

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert result.status == ActionStatus.FAILURE
        assert "Simulated device failure" in result.error_message

    def test_configure_custom_failure_message(self) -> None:
        """Test custom failure message."""
        device = MockDevice()
        device.configure(should_fail=True, failure_message="Custom error message")

        state = InformationState()
        action = Action(action_type=ActionType.BOOK, name="book_hotel")

        result = device.execute_action(action, state)

        assert "Custom error message" in result.error_message

    def test_configure_should_fail_preconditions(self) -> None:
        """Test configuring preconditions to fail."""
        device = MockDevice()
        device.configure(should_fail_preconditions=True)

        state = InformationState()
        action = Action(action_type=ActionType.BOOK, name="book_hotel")

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert result.status == ActionStatus.PRECONDITION_FAILED

    def test_reset_clears_state(self) -> None:
        """Test that reset() clears device state."""
        device = MockDevice()
        device.configure(should_fail=True)

        state = InformationState()
        action = Action(action_type=ActionType.BOOK, name="book_hotel")

        device.execute_action(action, state)

        # Reset
        device.reset()

        assert device.execution_count == 0
        assert device.action_history == []
        assert not device.should_fail


class TestMockDevicePreconditions:
    """Test MockDevice precondition checking."""

    def test_check_preconditions_satisfied(self) -> None:
        """Test precondition checking when satisfied."""
        device = MockDevice()
        state = InformationState()
        state.shared.commitments.add("check_in_date: 2025-01-05")
        state.shared.commitments.add("check_out_date: 2025-01-10")

        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            preconditions=["check_in_date", "check_out_date"],
        )

        result = device.execute_action(action, state)

        assert result.is_successful()

    def test_check_preconditions_missing(self) -> None:
        """Test precondition checking when missing."""
        device = MockDevice()
        state = InformationState()
        state.shared.commitments.add("check_in_date: 2025-01-05")
        # Missing check_out_date

        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            preconditions=["check_in_date", "check_out_date"],
        )

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert result.status == ActionStatus.PRECONDITION_FAILED

    def test_check_preconditions_exact_match(self) -> None:
        """Test precondition checking with exact match."""
        device = MockDevice()
        state = InformationState()
        state.shared.commitments.add("task_ready")

        action = Action(
            action_type=ActionType.EXECUTE,
            name="complete_task",
            preconditions=["task_ready"],
        )

        assert device.check_preconditions(action, state)

    def test_check_preconditions_prefix_match(self) -> None:
        """Test precondition checking with prefix match."""
        device = MockDevice()
        state = InformationState()
        state.shared.commitments.add("check_in_date: 2025-01-05")

        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            preconditions=["check_in_date"],
        )

        assert device.check_preconditions(action, state)

    def test_custom_precondition_function(self) -> None:
        """Test custom precondition function."""
        device = MockDevice()

        # Custom function that always requires "special_requirement"
        def custom_precond(action: Action, state: InformationState) -> bool:
            return "special_requirement" in state.shared.commitments

        device.set_custom_precond_function(custom_precond)

        state = InformationState()
        action = Action(action_type=ActionType.BOOK, name="book_hotel")

        # Should fail without special requirement
        result = device.execute_action(action, state)
        assert not result.is_successful()

        # Should succeed with special requirement
        state.shared.commitments.add("special_requirement")
        result = device.execute_action(action, state)
        assert result.is_successful()


class TestMockDevicePostconditions:
    """Test MockDevice postcondition generation."""

    def test_default_postconditions(self) -> None:
        """Test default postcondition generation."""
        device = MockDevice()

        action = Action(action_type=ActionType.BOOK, name="book_hotel")

        postconds = device.get_postconditions(action)

        assert postconds == ["executed(book_hotel)"]

    def test_custom_postcondition_function(self) -> None:
        """Test custom postcondition function."""
        device = MockDevice()

        # Custom function that generates specific postconditions
        def custom_postcond(action: Action) -> list[str]:
            hotel_id = action.parameters.get("hotel_id", "unknown")
            return [f"booked(hotel_id={hotel_id})", "payment_processed"]

        device.set_custom_postcond_function(custom_postcond)

        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H123"},
        )

        result = device.execute_action(action, InformationState())

        assert "booked(hotel_id=H123)" in result.postconditions
        assert "payment_processed" in result.postconditions


class TestMockDeviceUtilities:
    """Test MockDevice utility methods."""

    def test_get_last_action(self) -> None:
        """Test getting last executed action."""
        device = MockDevice()
        state = InformationState()

        # No actions yet
        assert device.get_last_action() is None

        # Execute actions
        action1 = Action(action_type=ActionType.BOOK, name="book_hotel")
        action2 = Action(action_type=ActionType.CANCEL, name="cancel_booking")

        device.execute_action(action1, state)
        device.execute_action(action2, state)

        # Should return last action
        last_result = device.get_last_action()
        assert last_result is not None
        last_action, _ = last_result
        assert last_action.name == "cancel_booking"

    def test_get_action_count(self) -> None:
        """Test counting action executions."""
        device = MockDevice()
        state = InformationState()

        action1 = Action(action_type=ActionType.BOOK, name="book_hotel")
        action2 = Action(action_type=ActionType.BOOK, name="book_hotel")
        action3 = Action(action_type=ActionType.CANCEL, name="cancel_booking")

        device.execute_action(action1, state)
        device.execute_action(action2, state)
        device.execute_action(action3, state)

        assert device.get_action_count("book_hotel") == 2
        assert device.get_action_count("cancel_booking") == 1
        assert device.get_action_count("nonexistent_action") == 0
