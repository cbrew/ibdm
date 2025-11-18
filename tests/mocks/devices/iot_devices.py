"""IoT and smart home mock devices.

Simulates smart home devices, sensors, and automation systems.
"""

import random
from datetime import datetime
from typing import Any

from ibdm.core.actions import Action
from ibdm.core.information_state import InformationState
from ibdm.interfaces.device import ActionResult, ActionStatus, DeviceInterface


class SmartHomeDevice(DeviceInterface):
    """Mock smart home control system (e.g., SmartThings, Home Assistant).

    Simulates control of lights, thermostats, locks, and other smart devices.

    Actions:
    - control_light: Turn lights on/off, set brightness/color
    - set_thermostat: Set temperature, mode
    - control_lock: Lock/unlock doors
    - get_device_status: Get current device state
    - create_automation: Create automation rule

    Preconditions:
    - Valid device ID
    - Valid command parameters

    Postconditions:
    - device_controlled(device_id=..., state=...)
    - automation_created(rule_id=...)
    """

    DEVICE_TYPES = {
        "light": ["on", "off", "brightness", "color"],
        "thermostat": ["temperature", "mode", "fan_mode"],
        "lock": ["locked", "unlocked"],
        "sensor": ["temperature", "humidity", "motion", "contact"],
        "switch": ["on", "off"],
    }

    def __init__(self, fail_rate: float = 0.0):
        """Initialize smart home device.

        Args:
            fail_rate: Probability of simulated failures (0.0-1.0)
        """
        # Initialize with sample devices
        self.devices: dict[str, Any] = {
            "light_001": {
                "type": "light",
                "name": "Living Room Light",
                "state": "off",
                "brightness": 100,
                "color": "white",
            },
            "light_002": {
                "type": "light",
                "name": "Bedroom Light",
                "state": "off",
                "brightness": 80,
                "color": "warm_white",
            },
            "therm_001": {
                "type": "thermostat",
                "name": "Main Thermostat",
                "temperature": 72,
                "mode": "auto",
                "fan_mode": "auto",
                "current_temp": 70,
            },
            "lock_001": {
                "type": "lock",
                "name": "Front Door",
                "state": "locked",
            },
            "sensor_001": {
                "type": "sensor",
                "name": "Living Room Sensor",
                "temperature": 72.5,
                "humidity": 45,
                "motion": False,
            },
        }
        self.automations: dict[str, Any] = {}
        self.fail_rate = fail_rate
        self.automation_count = 0

    def execute_action(self, action: Action, state: InformationState) -> ActionResult:
        """Execute smart home action."""
        # Check preconditions
        if not self.check_preconditions(action, state):
            return ActionResult(
                status=ActionStatus.PRECONDITION_FAILED,
                action=action,
                error_message="Required smart home parameters missing",
            )

        # Simulate random failures
        if random.random() < self.fail_rate:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message="Smart home service temporarily unavailable",
            )

        # Route to specific action handler
        if action.name == "control_light":
            return self._control_light(action)
        elif action.name == "set_thermostat":
            return self._set_thermostat(action)
        elif action.name == "control_lock":
            return self._control_lock(action)
        elif action.name == "get_device_status":
            return self._get_device_status(action)
        elif action.name == "create_automation":
            return self._create_automation(action)
        else:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Unknown action: {action.name}",
            )

    def check_preconditions(self, action: Action, state: InformationState) -> bool:
        """Check if smart home preconditions are satisfied."""
        params = action.parameters

        if action.name in ["control_light", "set_thermostat", "control_lock", "get_device_status"]:
            # Require device ID
            return "device_id" in params
        elif action.name == "create_automation":
            # Require trigger and actions
            return "trigger" in params and "actions" in params

        return True

    def get_postconditions(self, action: Action) -> list[str]:
        """Get postconditions for smart home action."""
        if action.name in ["control_light", "set_thermostat", "control_lock"]:
            device_id = action.parameters.get("device_id", "unknown")
            return [f"device_controlled(device_id={device_id})"]
        elif action.name == "get_device_status":
            return ["device_status_retrieved"]
        elif action.name == "create_automation":
            rule_id = f"AUTO-{self.automation_count:06d}"
            return [f"automation_created(rule_id={rule_id})"]

        return []

    def _control_light(self, action: Action) -> ActionResult:
        """Control light device."""
        device_id = action.parameters.get("device_id")

        if device_id not in self.devices:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Device {device_id} not found",
            )

        device = self.devices[device_id]

        if device["type"] != "light":
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Device {device_id} is not a light",
            )

        # Update device state
        params = action.parameters
        if "state" in params:
            device["state"] = params["state"]
        if "brightness" in params:
            device["brightness"] = params["brightness"]
        if "color" in params:
            device["color"] = params["color"]

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "device_id": device_id,
                "name": device["name"],
                "state": device["state"],
                "brightness": device.get("brightness"),
                "color": device.get("color"),
            },
            postconditions=[f"device_controlled(device_id={device_id})"],
        )

    def _set_thermostat(self, action: Action) -> ActionResult:
        """Set thermostat parameters."""
        device_id = action.parameters.get("device_id")

        if device_id not in self.devices:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Device {device_id} not found",
            )

        device = self.devices[device_id]

        if device["type"] != "thermostat":
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Device {device_id} is not a thermostat",
            )

        # Update thermostat settings
        params = action.parameters
        if "temperature" in params:
            device["temperature"] = params["temperature"]
        if "mode" in params:
            device["mode"] = params["mode"]
        if "fan_mode" in params:
            device["fan_mode"] = params["fan_mode"]

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "device_id": device_id,
                "name": device["name"],
                "temperature": device["temperature"],
                "mode": device["mode"],
                "fan_mode": device["fan_mode"],
                "current_temp": device["current_temp"],
            },
            postconditions=[f"device_controlled(device_id={device_id})"],
        )

    def _control_lock(self, action: Action) -> ActionResult:
        """Control door lock."""
        device_id = action.parameters.get("device_id")

        if device_id not in self.devices:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Device {device_id} not found",
            )

        device = self.devices[device_id]

        if device["type"] != "lock":
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Device {device_id} is not a lock",
            )

        # Update lock state
        new_state = action.parameters.get("state")
        if new_state not in ["locked", "unlocked"]:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Invalid lock state: {new_state}",
            )

        device["state"] = new_state
        device["last_changed"] = datetime.now().isoformat()

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "device_id": device_id,
                "name": device["name"],
                "state": device["state"],
                "last_changed": device["last_changed"],
            },
            postconditions=[f"device_controlled(device_id={device_id})"],
        )

    def _get_device_status(self, action: Action) -> ActionResult:
        """Get current device status."""
        device_id = action.parameters.get("device_id")

        if device_id not in self.devices:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Device {device_id} not found",
            )

        device = self.devices[device_id]

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "device_id": device_id,
                "type": device["type"],
                "name": device["name"],
                **{k: v for k, v in device.items() if k not in ["type", "name"]},
            },
            postconditions=["device_status_retrieved"],
        )

    def _create_automation(self, action: Action) -> ActionResult:
        """Create automation rule."""
        self.automation_count += 1
        rule_id = f"AUTO-{self.automation_count:06d}"

        params = action.parameters

        automation = {
            "rule_id": rule_id,
            "name": params.get("name", f"Automation {rule_id}"),
            "trigger": params["trigger"],
            "actions": params["actions"],
            "enabled": params.get("enabled", True),
            "created_at": datetime.now().isoformat(),
        }

        self.automations[rule_id] = automation

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "rule_id": rule_id,
                "name": automation["name"],
                "enabled": automation["enabled"],
            },
            postconditions=[f"automation_created(rule_id={rule_id})"],
        )


class SensorDevice(DeviceInterface):
    """Mock IoT sensor system (e.g., environmental sensors, motion detectors).

    Simulates reading from various sensors and monitoring conditions.

    Actions:
    - read_temperature: Read temperature sensor
    - read_humidity: Read humidity sensor
    - check_motion: Check motion detector
    - read_air_quality: Read air quality sensor
    - get_sensor_history: Get historical sensor data

    Preconditions:
    - Valid sensor ID

    Postconditions:
    - sensor_read(sensor_id=..., value=...)
    """

    def __init__(self, fail_rate: float = 0.0):
        """Initialize sensor device.

        Args:
            fail_rate: Probability of simulated failures (0.0-1.0)
        """
        # Initialize with sample sensors
        self.sensors: dict[str, Any] = {
            "temp_001": {
                "type": "temperature",
                "name": "Living Room Temperature",
                "unit": "F",
                "min": 60,
                "max": 80,
            },
            "hum_001": {
                "type": "humidity",
                "name": "Living Room Humidity",
                "unit": "%",
                "min": 30,
                "max": 60,
            },
            "motion_001": {
                "type": "motion",
                "name": "Front Door Motion",
            },
            "air_001": {
                "type": "air_quality",
                "name": "Indoor Air Quality",
                "unit": "AQI",
            },
        }
        self.history: dict[str, list] = {sensor_id: [] for sensor_id in self.sensors}
        self.fail_rate = fail_rate

    def execute_action(self, action: Action, state: InformationState) -> ActionResult:
        """Execute sensor action."""
        # Check preconditions
        if not self.check_preconditions(action, state):
            return ActionResult(
                status=ActionStatus.PRECONDITION_FAILED,
                action=action,
                error_message="Required sensor parameters missing",
            )

        # Simulate random failures
        if random.random() < self.fail_rate:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message="Sensor temporarily unavailable",
            )

        # Route to specific action handler
        if action.name == "read_temperature":
            return self._read_temperature(action)
        elif action.name == "read_humidity":
            return self._read_humidity(action)
        elif action.name == "check_motion":
            return self._check_motion(action)
        elif action.name == "read_air_quality":
            return self._read_air_quality(action)
        elif action.name == "get_sensor_history":
            return self._get_sensor_history(action)
        else:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Unknown action: {action.name}",
            )

    def check_preconditions(self, action: Action, state: InformationState) -> bool:
        """Check if sensor preconditions are satisfied."""
        params = action.parameters

        if action.name in [
            "read_temperature",
            "read_humidity",
            "check_motion",
            "read_air_quality",
            "get_sensor_history",
        ]:
            # Require sensor ID
            return "sensor_id" in params

        return True

    def get_postconditions(self, action: Action) -> list[str]:
        """Get postconditions for sensor action."""
        sensor_id = action.parameters.get("sensor_id", "unknown")

        if action.name in ["read_temperature", "read_humidity", "check_motion", "read_air_quality"]:
            return [f"sensor_read(sensor_id={sensor_id})"]
        elif action.name == "get_sensor_history":
            return ["sensor_history_retrieved"]

        return []

    def _read_temperature(self, action: Action) -> ActionResult:
        """Read temperature sensor."""
        sensor_id = action.parameters.get("sensor_id")

        if sensor_id not in self.sensors:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Sensor {sensor_id} not found",
            )

        sensor = self.sensors[sensor_id]

        if sensor["type"] != "temperature":
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Sensor {sensor_id} is not a temperature sensor",
            )

        # Generate realistic temperature reading
        value = random.uniform(sensor["min"], sensor["max"])
        timestamp = datetime.now().isoformat()

        # Store in history
        self.history[sensor_id].append({"value": value, "timestamp": timestamp})

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "sensor_id": sensor_id,
                "name": sensor["name"],
                "value": round(value, 1),
                "unit": sensor["unit"],
                "timestamp": timestamp,
            },
            postconditions=[f"sensor_read(sensor_id={sensor_id})"],
        )

    def _read_humidity(self, action: Action) -> ActionResult:
        """Read humidity sensor."""
        sensor_id = action.parameters.get("sensor_id")

        if sensor_id not in self.sensors:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Sensor {sensor_id} not found",
            )

        sensor = self.sensors[sensor_id]

        if sensor["type"] != "humidity":
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Sensor {sensor_id} is not a humidity sensor",
            )

        # Generate realistic humidity reading
        value = random.uniform(sensor["min"], sensor["max"])
        timestamp = datetime.now().isoformat()

        # Store in history
        self.history[sensor_id].append({"value": value, "timestamp": timestamp})

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "sensor_id": sensor_id,
                "name": sensor["name"],
                "value": round(value, 1),
                "unit": sensor["unit"],
                "timestamp": timestamp,
            },
            postconditions=[f"sensor_read(sensor_id={sensor_id})"],
        )

    def _check_motion(self, action: Action) -> ActionResult:
        """Check motion detector."""
        sensor_id = action.parameters.get("sensor_id")

        if sensor_id not in self.sensors:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Sensor {sensor_id} not found",
            )

        sensor = self.sensors[sensor_id]

        if sensor["type"] != "motion":
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Sensor {sensor_id} is not a motion sensor",
            )

        # Simulate motion detection (20% chance of motion)
        motion_detected = random.random() < 0.2
        timestamp = datetime.now().isoformat()

        # Store in history
        self.history[sensor_id].append({"value": motion_detected, "timestamp": timestamp})

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "sensor_id": sensor_id,
                "name": sensor["name"],
                "motion_detected": motion_detected,
                "timestamp": timestamp,
            },
            postconditions=[f"sensor_read(sensor_id={sensor_id})"],
        )

    def _read_air_quality(self, action: Action) -> ActionResult:
        """Read air quality sensor."""
        sensor_id = action.parameters.get("sensor_id")

        if sensor_id not in self.sensors:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Sensor {sensor_id} not found",
            )

        sensor = self.sensors[sensor_id]

        if sensor["type"] != "air_quality":
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Sensor {sensor_id} is not an air quality sensor",
            )

        # Generate air quality index (0-500)
        aqi = random.randint(0, 150)
        timestamp = datetime.now().isoformat()

        # Determine quality level
        if aqi <= 50:
            level = "Good"
        elif aqi <= 100:
            level = "Moderate"
        elif aqi <= 150:
            level = "Unhealthy for Sensitive Groups"
        elif aqi <= 200:
            level = "Unhealthy"
        elif aqi <= 300:
            level = "Very Unhealthy"
        else:
            level = "Hazardous"

        # Store in history
        self.history[sensor_id].append({"value": aqi, "timestamp": timestamp})

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "sensor_id": sensor_id,
                "name": sensor["name"],
                "aqi": aqi,
                "level": level,
                "timestamp": timestamp,
            },
            postconditions=[f"sensor_read(sensor_id={sensor_id})"],
        )

    def _get_sensor_history(self, action: Action) -> ActionResult:
        """Get historical sensor data."""
        sensor_id = action.parameters.get("sensor_id")

        if sensor_id not in self.sensors:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Sensor {sensor_id} not found",
            )

        # Get last N readings
        limit = action.parameters.get("limit", 10)
        history = self.history[sensor_id][-limit:]

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "sensor_id": sensor_id,
                "name": self.sensors[sensor_id]["name"],
                "readings_count": len(history),
                "readings": history,
            },
            postconditions=["sensor_history_retrieved"],
        )


class AutomationDevice(DeviceInterface):
    """Mock IoT automation platform (e.g., IFTTT, Zapier for IoT).

    Simulates trigger-based automation and workflow execution.

    Actions:
    - create_recipe: Create automation recipe
    - trigger_workflow: Manually trigger workflow
    - get_recipe_status: Check recipe execution status
    - delete_recipe: Delete automation recipe

    Preconditions:
    - Valid trigger and action definitions

    Postconditions:
    - recipe_created(recipe_id=...)
    - workflow_triggered(execution_id=...)
    """

    def __init__(self, fail_rate: float = 0.0):
        """Initialize automation device.

        Args:
            fail_rate: Probability of simulated failures (0.0-1.0)
        """
        self.recipes: dict[str, Any] = {}
        self.executions: dict[str, Any] = {}
        self.fail_rate = fail_rate
        self.recipe_count = 0
        self.execution_count = 0

    def execute_action(self, action: Action, state: InformationState) -> ActionResult:
        """Execute automation action."""
        # Check preconditions
        if not self.check_preconditions(action, state):
            return ActionResult(
                status=ActionStatus.PRECONDITION_FAILED,
                action=action,
                error_message="Required automation parameters missing",
            )

        # Simulate random failures
        if random.random() < self.fail_rate:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message="Automation service temporarily unavailable",
            )

        # Route to specific action handler
        if action.name == "create_recipe":
            return self._create_recipe(action)
        elif action.name == "trigger_workflow":
            return self._trigger_workflow(action)
        elif action.name == "get_recipe_status":
            return self._get_recipe_status(action)
        elif action.name == "delete_recipe":
            return self._delete_recipe(action)
        else:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Unknown action: {action.name}",
            )

    def check_preconditions(self, action: Action, state: InformationState) -> bool:
        """Check if automation preconditions are satisfied."""
        params = action.parameters

        if action.name == "create_recipe":
            # Require trigger and action
            return "trigger" in params and "action" in params
        elif action.name == "trigger_workflow":
            # Require recipe ID
            return "recipe_id" in params
        elif action.name in ["get_recipe_status", "delete_recipe"]:
            # Require recipe ID
            return "recipe_id" in params

        return True

    def get_postconditions(self, action: Action) -> list[str]:
        """Get postconditions for automation action."""
        if action.name == "create_recipe":
            recipe_id = f"RCP-{self.recipe_count:06d}"
            return [f"recipe_created(recipe_id={recipe_id})"]
        elif action.name == "trigger_workflow":
            exec_id = f"EXEC-{self.execution_count:08d}"
            return [f"workflow_triggered(execution_id={exec_id})"]
        elif action.name == "get_recipe_status":
            return ["recipe_status_retrieved"]
        elif action.name == "delete_recipe":
            return ["recipe_deleted"]

        return []

    def _create_recipe(self, action: Action) -> ActionResult:
        """Create automation recipe."""
        self.recipe_count += 1
        recipe_id = f"RCP-{self.recipe_count:06d}"

        params = action.parameters

        recipe = {
            "recipe_id": recipe_id,
            "name": params.get("name", f"Recipe {recipe_id}"),
            "trigger": params["trigger"],
            "action": params["action"],
            "enabled": params.get("enabled", True),
            "created_at": datetime.now().isoformat(),
            "execution_count": 0,
        }

        self.recipes[recipe_id] = recipe

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "recipe_id": recipe_id,
                "name": recipe["name"],
                "enabled": recipe["enabled"],
            },
            postconditions=[f"recipe_created(recipe_id={recipe_id})"],
        )

    def _trigger_workflow(self, action: Action) -> ActionResult:
        """Manually trigger workflow."""
        recipe_id = action.parameters.get("recipe_id")

        if recipe_id not in self.recipes:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Recipe {recipe_id} not found",
            )

        recipe = self.recipes[recipe_id]

        if not recipe["enabled"]:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Recipe {recipe_id} is disabled",
            )

        self.execution_count += 1
        exec_id = f"EXEC-{self.execution_count:08d}"

        execution = {
            "execution_id": exec_id,
            "recipe_id": recipe_id,
            "status": "success",
            "started_at": datetime.now().isoformat(),
            "completed_at": datetime.now().isoformat(),
        }

        self.executions[exec_id] = execution
        recipe["execution_count"] += 1

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "execution_id": exec_id,
                "recipe_id": recipe_id,
                "status": "success",
            },
            postconditions=[f"workflow_triggered(execution_id={exec_id})"],
        )

    def _get_recipe_status(self, action: Action) -> ActionResult:
        """Get recipe execution status."""
        recipe_id = action.parameters.get("recipe_id")

        if recipe_id not in self.recipes:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Recipe {recipe_id} not found",
            )

        recipe = self.recipes[recipe_id]

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "recipe_id": recipe_id,
                "name": recipe["name"],
                "enabled": recipe["enabled"],
                "execution_count": recipe["execution_count"],
                "created_at": recipe["created_at"],
            },
            postconditions=["recipe_status_retrieved"],
        )

    def _delete_recipe(self, action: Action) -> ActionResult:
        """Delete automation recipe."""
        recipe_id = action.parameters.get("recipe_id")

        if recipe_id not in self.recipes:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Recipe {recipe_id} not found",
            )

        del self.recipes[recipe_id]

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "recipe_id": recipe_id,
                "deleted": True,
            },
            postconditions=["recipe_deleted"],
        )
