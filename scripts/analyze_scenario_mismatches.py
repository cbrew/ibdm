#!/usr/bin/env python3
"""Analyze state mismatches in scenario runs.

This script runs a scenario and systematically compares expected vs actual state changes
to identify all mismatches for fixing.
"""

import json
import sys
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.table import Table

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ibdm.core.domain import NDADomain
from ibdm.core.information_state import InformationState
from ibdm.engine.dialogue_engine import DialogueEngine


def load_scenario(scenario_path: Path) -> dict[str, Any]:
    """Load scenario from JSON file."""
    with open(scenario_path) as f:
        return json.load(f)


def analyze_state_changes(
    expected: dict[str, Any],
    actual_state: InformationState,
    turn_num: int,
    console: Console,
) -> list[str]:
    """Analyze differences between expected and actual state.

    Returns list of mismatch descriptions.
    """
    mismatches = []

    # Check commitments
    if "commitments_added" in expected:
        expected_commits = expected["commitments_added"]
        if isinstance(expected_commits, str):
            expected_commits = [expected_commits]

        for expected_commit in expected_commits:
            # Parse expected commitment format (e.g., "nda_type(value=mutual)")
            if "(" in expected_commit and ")" in expected_commit:
                key = expected_commit.split("(")[0]
                value = expected_commit.split("value=")[1].rstrip(")")

                # Check if this commitment exists in actual state
                found = False
                for commit in actual_state.shared.commitments:
                    if hasattr(commit, "content"):
                        # Check if commitment matches expected format
                        content_str = str(commit.content)
                        if key in content_str and value in content_str:
                            found = True
                            break

                if not found:
                    mismatches.append(f"Missing commitment: {expected_commit}")

    # Check commitment_added (singular)
    if "commitment_added" in expected:
        expected_commit = expected["commitment_added"]
        # This is a more complex check - for now just note it
        mismatches.append(f"Expected commitment pattern: {expected_commit}")

    # Check QUD operations
    if "qud_pushed" in expected:
        expected_qud = expected["qud_pushed"]
        # Simplified check - just verify QUD depth increased
        # In reality would need to track previous depth

    if "qud_popped" in expected:
        expected_qud = expected["qud_popped"]
        # Check if QUD was actually popped
        mismatches.append(f"Expected QUD pop: {expected_qud}")

    # Check QUD depth
    if "qud_depth" in expected:
        expected_depth = expected["qud_depth"]
        actual_depth = len(actual_state.shared.qud)
        if actual_depth != expected_depth:
            mismatches.append(
                f"QUD depth mismatch: expected {expected_depth}, got {actual_depth}"
            )

    return mismatches


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: analyze_scenario_mismatches.py <scenario_name>")
        sys.exit(1)

    scenario_name = sys.argv[1]
    scenario_path = Path("demos/scenarios") / f"{scenario_name}.json"

    if not scenario_path.exists():
        print(f"Scenario not found: {scenario_path}")
        sys.exit(1)

    console = Console()
    console.print(f"\n[bold cyan]Analyzing scenario: {scenario_name}[/bold cyan]\n")

    # Load scenario
    scenario = load_scenario(scenario_path)

    # Initialize engine
    domain = NDADomain()
    engine = DialogueEngine(domain=domain)
    state = engine.state

    # Track all mismatches
    all_mismatches = []

    # Run through scenario
    for turn_idx, turn in enumerate(scenario["turns"], start=1):
        if turn["speaker"] == "user":
            # Process user utterance
            utterance = turn["utterance"]

            # Update state
            response = engine.process_input(utterance)

            # Check for expected state changes
            if "state_changes" in turn:
                expected = turn["state_changes"]
                mismatches = analyze_state_changes(expected, state, turn_idx, console)

                if mismatches:
                    all_mismatches.append({
                        "turn": turn_idx,
                        "utterance": utterance,
                        "move_type": turn.get("move_type", "unknown"),
                        "mismatches": mismatches,
                        "expected": expected,
                    })

    # Report mismatches
    if all_mismatches:
        console.print(f"\n[bold red]Found {len(all_mismatches)} turns with mismatches:[/bold red]\n")

        for item in all_mismatches:
            console.print(f"[bold yellow]Turn {item['turn']}[/bold yellow] ({item['move_type']})")
            console.print(f"  Utterance: {item['utterance']}")
            console.print(f"  Mismatches:")
            for mismatch in item["mismatches"]:
                console.print(f"    • {mismatch}")
            console.print()

        # Create summary table
        table = Table(title="Mismatch Summary")
        table.add_column("Turn", justify="right", style="cyan")
        table.add_column("Move Type", style="magenta")
        table.add_column("Count", justify="right", style="yellow")

        for item in all_mismatches:
            table.add_row(
                str(item["turn"]),
                item["move_type"],
                str(len(item["mismatches"])),
            )

        console.print(table)

        # Save detailed report
        report_path = Path("reports") / f"mismatch_analysis_{scenario_name}.json"
        report_path.parent.mkdir(exist_ok=True)
        with open(report_path, "w") as f:
            json.dump(all_mismatches, f, indent=2)

        console.print(f"\n[bold green]Detailed report saved to: {report_path}[/bold green]")
    else:
        console.print("[bold green]No mismatches found! 🎉[/bold green]")


if __name__ == "__main__":
    main()
