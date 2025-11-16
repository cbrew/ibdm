"""Unit tests for IoT domain mock devices.

Tests SmartHomeDevice, SensorDevice, and AutomationDevice.
"""

import sys
from pathlib import Path

# Add tests directory to path
tests_dir = Path(__file__).parent.parent
sys.path.insert(0, str(tests_dir))

from mocks.devices.iot_devices import (  # noqa: E402
    AutomationDevice,
    SensorDevice,
    SmartHomeDevice,
)

from ibdm.core.actions import Action, ActionType  # noqa: E402
from ibdm.core.information_state import InformationState  # noqa: E402
from ibdm.interfaces.device import ActionStatus  # noqa: E402


class TestSmartHomeDevice:
    """Test SmartHomeDevice."""

    def test_initialization(self) -> None:
        """Test device initialization."""
        device = SmartHomeDevice()

        assert len(device.devices) > 0
        assert device.automations == {}

    def test_control_light_on(self) -> None:
        """Test turning light on."""
        device = SmartHomeDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="control_light",
            parameters={
                "device_id": "light_001",
                "state": "on",
                "brightness": 80,
            },
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert device.devices["light_001"]["state"] == "on"
        assert device.devices["light_001"]["brightness"] == 80

    def test_control_light_color(self) -> None:
        """Test changing light color."""
        device = SmartHomeDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="control_light",
            parameters={
                "device_id": "light_001",
                "state": "on",
                "color": "blue",
            },
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert device.devices["light_001"]["color"] == "blue"

    def test_control_nonexistent_device(self) -> None:
        """Test controlling non-existent device."""
        device = SmartHomeDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="control_light",
            parameters={"device_id": "INVALID", "state": "on"},
        )

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert result.status == ActionStatus.FAILURE

    def test_control_wrong_device_type(self) -> None:
        """Test controlling device with wrong action."""
        device = SmartHomeDevice()
        state = InformationState()

        # Try to control a thermostat as a light
        action = Action(
            action_type=ActionType.EXECUTE,
            name="control_light",
            parameters={"device_id": "therm_001", "state": "on"},
        )

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert "not a light" in result.error_message

    def test_set_thermostat_temperature(self) -> None:
        """Test setting thermostat temperature."""
        device = SmartHomeDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="set_thermostat",
            parameters={
                "device_id": "therm_001",
                "temperature": 75,
                "mode": "heat",
            },
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert device.devices["therm_001"]["temperature"] == 75
        assert device.devices["therm_001"]["mode"] == "heat"

    def test_control_lock_success(self) -> None:
        """Test locking/unlocking door."""
        device = SmartHomeDevice()
        state = InformationState()

        # Unlock
        action = Action(
            action_type=ActionType.EXECUTE,
            name="control_lock",
            parameters={"device_id": "lock_001", "state": "unlocked"},
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert device.devices["lock_001"]["state"] == "unlocked"

    def test_control_lock_invalid_state(self) -> None:
        """Test lock with invalid state."""
        device = SmartHomeDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="control_lock",
            parameters={"device_id": "lock_001", "state": "broken"},
        )

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert "invalid lock state" in result.error_message.lower()

    def test_get_device_status(self) -> None:
        """Test getting device status."""
        device = SmartHomeDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.GET,
            name="get_device_status",
            parameters={"device_id": "light_001"},
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert "device_id" in result.return_value
        assert "type" in result.return_value
        assert "name" in result.return_value

    def test_create_automation_success(self) -> None:
        """Test creating automation rule."""
        device = SmartHomeDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="create_automation",
            parameters={
                "name": "Turn on lights at sunset",
                "trigger": {"type": "time", "at": "sunset"},
                "actions": [{"device_id": "light_001", "state": "on"}],
            },
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert "rule_id" in result.return_value
        assert result.return_value["rule_id"].startswith("AUTO-")


class TestSensorDevice:
    """Test SensorDevice."""

    def test_initialization(self) -> None:
        """Test device initialization."""
        device = SensorDevice()

        assert len(device.sensors) > 0
        assert len(device.history) > 0

    def test_read_temperature_success(self) -> None:
        """Test reading temperature sensor."""
        device = SensorDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.GET,
            name="read_temperature",
            parameters={"sensor_id": "temp_001"},
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert "value" in result.return_value
        assert "unit" in result.return_value
        assert result.return_value["unit"] == "F"
        assert "timestamp" in result.return_value

    def test_read_wrong_sensor_type(self) -> None:
        """Test reading sensor with wrong action."""
        device = SensorDevice()
        state = InformationState()

        # Try to read humidity sensor as temperature
        action = Action(
            action_type=ActionType.GET,
            name="read_temperature",
            parameters={"sensor_id": "hum_001"},
        )

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert "not a temperature sensor" in result.error_message

    def test_read_humidity_success(self) -> None:
        """Test reading humidity sensor."""
        device = SensorDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.GET,
            name="read_humidity",
            parameters={"sensor_id": "hum_001"},
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert "value" in result.return_value
        assert result.return_value["unit"] == "%"

    def test_check_motion_sensor(self) -> None:
        """Test checking motion detector."""
        device = SensorDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.GET,
            name="check_motion",
            parameters={"sensor_id": "motion_001"},
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert "motion_detected" in result.return_value
        assert isinstance(result.return_value["motion_detected"], bool)

    def test_read_air_quality_success(self) -> None:
        """Test reading air quality sensor."""
        device = SensorDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.GET,
            name="read_air_quality",
            parameters={"sensor_id": "air_001"},
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert "aqi" in result.return_value
        assert "level" in result.return_value
        assert 0 <= result.return_value["aqi"] <= 500

    def test_sensor_history_tracking(self) -> None:
        """Test that sensor readings are stored in history."""
        device = SensorDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.GET,
            name="read_temperature",
            parameters={"sensor_id": "temp_001"},
        )

        # Read multiple times
        device.execute_action(action, state)
        device.execute_action(action, state)
        device.execute_action(action, state)

        # Check history
        assert len(device.history["temp_001"]) == 3

    def test_get_sensor_history(self) -> None:
        """Test retrieving sensor history."""
        device = SensorDevice()
        state = InformationState()

        # Generate some readings
        read_action = Action(
            action_type=ActionType.GET,
            name="read_temperature",
            parameters={"sensor_id": "temp_001"},
        )

        for _ in range(5):
            device.execute_action(read_action, state)

        # Get history
        history_action = Action(
            action_type=ActionType.GET,
            name="get_sensor_history",
            parameters={"sensor_id": "temp_001", "limit": 3},
        )

        result = device.execute_action(history_action, state)

        assert result.is_successful()
        assert "readings" in result.return_value
        assert len(result.return_value["readings"]) == 3

    def test_read_nonexistent_sensor(self) -> None:
        """Test reading non-existent sensor."""
        device = SensorDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.GET,
            name="read_temperature",
            parameters={"sensor_id": "INVALID"},
        )

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert result.status == ActionStatus.FAILURE


class TestAutomationDevice:
    """Test AutomationDevice."""

    def test_initialization(self) -> None:
        """Test device initialization."""
        device = AutomationDevice()

        assert device.recipes == {}
        assert device.executions == {}
        assert device.recipe_count == 0

    def test_create_recipe_success(self) -> None:
        """Test creating automation recipe."""
        device = AutomationDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="create_recipe",
            parameters={
                "name": "Temperature Alert",
                "trigger": {"type": "sensor", "sensor_id": "temp_001", "condition": ">80"},
                "action": {"type": "notification", "message": "High temperature!"},
            },
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert "recipe_id" in result.return_value
        assert result.return_value["recipe_id"].startswith("RCP-")
        assert result.return_value["enabled"] is True

    def test_create_recipe_missing_parameters(self) -> None:
        """Test creating recipe with missing parameters."""
        device = AutomationDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="create_recipe",
            parameters={"name": "Test Recipe"},  # Missing trigger and action
        )

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert result.status == ActionStatus.PRECONDITION_FAILED

    def test_trigger_workflow_success(self) -> None:
        """Test manually triggering workflow."""
        device = AutomationDevice()
        state = InformationState()

        # Create recipe first
        create_action = Action(
            action_type=ActionType.EXECUTE,
            name="create_recipe",
            parameters={
                "name": "Test Recipe",
                "trigger": {"type": "manual"},
                "action": {"type": "test"},
            },
        )

        create_result = device.execute_action(create_action, state)
        recipe_id = create_result.return_value["recipe_id"]

        # Trigger workflow
        trigger_action = Action(
            action_type=ActionType.EXECUTE,
            name="trigger_workflow",
            parameters={"recipe_id": recipe_id},
        )

        trigger_result = device.execute_action(trigger_action, state)

        assert trigger_result.is_successful()
        assert "execution_id" in trigger_result.return_value
        assert trigger_result.return_value["execution_id"].startswith("EXEC-")

    def test_trigger_disabled_recipe(self) -> None:
        """Test triggering disabled recipe."""
        device = AutomationDevice()
        state = InformationState()

        # Create disabled recipe
        create_action = Action(
            action_type=ActionType.EXECUTE,
            name="create_recipe",
            parameters={
                "name": "Disabled Recipe",
                "trigger": {"type": "manual"},
                "action": {"type": "test"},
                "enabled": False,
            },
        )

        create_result = device.execute_action(create_action, state)
        recipe_id = create_result.return_value["recipe_id"]

        # Try to trigger
        trigger_action = Action(
            action_type=ActionType.EXECUTE,
            name="trigger_workflow",
            parameters={"recipe_id": recipe_id},
        )

        trigger_result = device.execute_action(trigger_action, state)

        assert not trigger_result.is_successful()
        assert "disabled" in trigger_result.error_message.lower()

    def test_get_recipe_status(self) -> None:
        """Test getting recipe status."""
        device = AutomationDevice()
        state = InformationState()

        # Create recipe
        create_action = Action(
            action_type=ActionType.EXECUTE,
            name="create_recipe",
            parameters={
                "name": "Test Recipe",
                "trigger": {"type": "manual"},
                "action": {"type": "test"},
            },
        )

        create_result = device.execute_action(create_action, state)
        recipe_id = create_result.return_value["recipe_id"]

        # Trigger it a few times
        trigger_action = Action(
            action_type=ActionType.EXECUTE,
            name="trigger_workflow",
            parameters={"recipe_id": recipe_id},
        )

        device.execute_action(trigger_action, state)
        device.execute_action(trigger_action, state)

        # Get status
        status_action = Action(
            action_type=ActionType.GET,
            name="get_recipe_status",
            parameters={"recipe_id": recipe_id},
        )

        status_result = device.execute_action(status_action, state)

        assert status_result.is_successful()
        assert "execution_count" in status_result.return_value
        assert status_result.return_value["execution_count"] == 2

    def test_delete_recipe_success(self) -> None:
        """Test deleting automation recipe."""
        device = AutomationDevice()
        state = InformationState()

        # Create recipe
        create_action = Action(
            action_type=ActionType.EXECUTE,
            name="create_recipe",
            parameters={
                "name": "Test Recipe",
                "trigger": {"type": "manual"},
                "action": {"type": "test"},
            },
        )

        create_result = device.execute_action(create_action, state)
        recipe_id = create_result.return_value["recipe_id"]

        # Delete it
        delete_action = Action(
            action_type=ActionType.EXECUTE,
            name="delete_recipe",
            parameters={"recipe_id": recipe_id},
        )

        delete_result = device.execute_action(delete_action, state)

        assert delete_result.is_successful()
        assert recipe_id not in device.recipes

    def test_delete_nonexistent_recipe(self) -> None:
        """Test deleting non-existent recipe."""
        device = AutomationDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="delete_recipe",
            parameters={"recipe_id": "INVALID-123"},
        )

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert result.status == ActionStatus.FAILURE

    def test_trigger_nonexistent_recipe(self) -> None:
        """Test triggering non-existent recipe."""
        device = AutomationDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="trigger_workflow",
            parameters={"recipe_id": "INVALID-123"},
        )

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert result.status == ActionStatus.FAILURE
