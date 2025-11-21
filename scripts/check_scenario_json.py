#!/usr/bin/env python3
"""Quick JSON syntax checker for scenario files.

Validates JSON syntax and basic structure without running full scenario validation.
Much faster than validate_scenarios.py for quick syntax checks.

Usage:
    python scripts/check_scenario_json.py                    # Check all scenarios
    python scripts/check_scenario_json.py nda_comprehensive  # Check specific scenario
"""

import json
import sys
from pathlib import Path

# Required fields for valid scenarios
REQUIRED_TOP_LEVEL = {"scenario_id", "title", "turns"}
REQUIRED_TURN_FIELDS = {"turn", "speaker", "utterance", "move_type"}
VALID_SPEAKERS = {"user", "system"}


def validate_json_file(file_path: Path) -> tuple[bool, str]:
    """Validate JSON syntax and structure of a scenario file.

    Args:
        file_path: Path to scenario JSON file

    Returns:
        Tuple of (is_valid, message)
    """
    try:
        # Check JSON syntax
        data = json.loads(file_path.read_text())

        # Check required top-level fields
        missing_top = REQUIRED_TOP_LEVEL - set(data.keys())
        if missing_top:
            return False, f"Missing top-level fields: {', '.join(sorted(missing_top))}"

        # Check turns is a list
        if not isinstance(data["turns"], list):
            return False, "'turns' must be a list"

        if not data["turns"]:
            return False, "No turns defined"

        # Check each turn
        for i, turn in enumerate(data["turns"], 1):
            # Check required turn fields
            missing_turn = REQUIRED_TURN_FIELDS - set(turn.keys())
            if missing_turn:
                return (
                    False,
                    f"Turn {i}: Missing fields: {', '.join(sorted(missing_turn))}",
                )

            # Check turn number is correct
            if turn["turn"] != i:
                return False, f"Turn {i}: Expected turn number {i}, got {turn['turn']}"

            # Check speaker is valid
            if turn["speaker"] not in VALID_SPEAKERS:
                return (
                    False,
                    f"Turn {i}: Invalid speaker '{turn['speaker']}' (must be 'user' or 'system')",
                )

        return True, f"Valid ({len(data['turns'])} turns)"

    except json.JSONDecodeError as e:
        return False, f"JSON syntax error at line {e.lineno}, column {e.colno}: {e.msg}"
    except Exception as e:
        return False, f"Error: {e}"


def main() -> int:
    """Main entry point.

    Returns:
        Exit code (0 = all valid, 1 = some invalid)
    """
    scenarios_dir = Path("demos/scenarios")

    # Determine which files to check
    if len(sys.argv) > 1:
        # Check specific scenario
        scenario_id = sys.argv[1]
        files = [scenarios_dir / f"{scenario_id}.json"]
        if not files[0].exists():
            print(f"✗ Scenario not found: {scenario_id}")
            return 1
    else:
        # Check all scenarios
        files = sorted(scenarios_dir.glob("*.json"))

    if not files:
        print("No scenario files found in demos/scenarios/")
        return 1

    print(f"Checking {len(files)} scenario file(s)...\n")

    all_valid = True
    for file_path in files:
        is_valid, message = validate_json_file(file_path)
        status = "✓" if is_valid else "✗"
        print(f"{status} {file_path.name:30} {message}")
        if not is_valid:
            all_valid = False

    print()
    if all_valid:
        print(f"✓ All {len(files)} scenario(s) have valid JSON syntax and structure")
        return 0
    else:
        print("✗ Some scenarios have errors - see above")
        return 1


if __name__ == "__main__":
    sys.exit(main())
