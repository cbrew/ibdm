#!/usr/bin/env python3
"""CLI script to run IBDM scenarios with rich formatting.

This script provides a simple interface to run JSON-based scenarios
using the unified ScenarioRunner.

Usage:
    python scripts/run_scenario.py                        # List available scenarios
    python scripts/run_scenario.py nda_basic              # Run specific scenario
    python scripts/run_scenario.py nda_basic --step       # Run in step mode
    python scripts/run_scenario.py nda_basic --delay 1.0  # Custom delay
    python scripts/run_scenario.py --list                 # List by category
    python scripts/run_scenario.py --search grounding     # Search scenarios
"""

import argparse
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rich.console import Console

from ibdm.demo import (
    ExecutionMode,
    ScenarioRunner,
    list_json_scenarios,
    list_scenarios_by_category,
    load_scenario,
    search_scenarios,
)
from ibdm.demo.execution_controller import ExecutionController


def list_available_scenarios() -> None:
    """Display all available scenarios grouped by category."""
    console = Console()

    console.print("\n[bold cyan]Available Scenarios[/bold cyan]\n")

    categories = list_scenarios_by_category()

    for category, scenarios in categories.items():
        console.print(f"[bold yellow]{category}[/bold yellow]")
        for scenario_id in scenarios:
            console.print(f"  • {scenario_id}")
        console.print()

    console.print("[dim]Run a scenario: python scripts/run_scenario.py <scenario_id>[/dim]\n")


def search_and_display(query: str) -> None:
    """Search and display matching scenarios.

    Args:
        query: Search query
    """
    console = Console()
    matches = search_scenarios(query)

    if not matches:
        console.print(f"[yellow]No scenarios found matching '{query}'[/yellow]")
        return

    console.print(f"\n[bold cyan]Scenarios matching '{query}':[/bold cyan]\n")
    for scenario_id in matches:
        console.print(f"  • {scenario_id}")
    console.print()


def run_scenario_cli(
    scenario_id: str,
    mode: ExecutionMode = ExecutionMode.AUTO,
    delay: float = 2.0,
    minimal: bool = False,
) -> None:
    """Run a scenario with specified options.

    Args:
        scenario_id: Scenario identifier
        mode: Execution mode
        delay: Auto-advance delay in seconds
        minimal: If True, hide detailed information
    """
    console = Console()

    try:
        scenario = load_scenario(scenario_id)
    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("\n[yellow]Available scenarios:[/yellow]")
        for sid in list_json_scenarios():
            console.print(f"  • {sid}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error loading scenario: {e}[/red]")
        sys.exit(1)

    # Create controller
    controller = ExecutionController(mode=mode, auto_delay=delay)

    # Create runner with display options
    runner = ScenarioRunner(
        scenario=scenario,
        controller=controller,
        console=console,
        show_explanations=not minimal,
        show_state_changes=not minimal,
        show_larsson_rules=not minimal,
        show_metrics=not minimal,
    )

    try:
        runner.run()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]⚠️  Interrupted by user (Ctrl+C)[/yellow]")
        sys.exit(0)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run IBDM scenarios with rich formatting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                        List available scenarios
  %(prog)s nda_basic              Run NDA basic scenario (auto mode)
  %(prog)s nda_basic --step       Run in step mode (press Enter to advance)
  %(prog)s nda_basic --delay 1.0  Run with 1-second delay
  %(prog)s nda_basic --minimal    Run with minimal output
  %(prog)s --list                 List scenarios by category
  %(prog)s --search grounding     Search for scenarios about grounding
        """,
    )

    parser.add_argument(
        "scenario_id",
        nargs="?",
        help="Scenario ID to run (e.g., nda_basic, ibis3_clarification)",
    )

    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        help="List all available scenarios grouped by category",
    )

    parser.add_argument(
        "--search",
        "-s",
        metavar="QUERY",
        help="Search scenarios by keyword",
    )

    # Execution mode options
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--step",
        action="store_true",
        help="Step mode: press Enter to advance each turn",
    )
    mode_group.add_argument(
        "--auto",
        action="store_true",
        help="Auto mode: automatic advancement (default)",
    )
    mode_group.add_argument(
        "--replay",
        action="store_true",
        help="Replay mode: instant playback",
    )

    parser.add_argument(
        "--delay",
        "-d",
        type=float,
        default=2.0,
        metavar="SECONDS",
        help="Delay between turns in auto mode (default: 2.0)",
    )

    parser.add_argument(
        "--minimal",
        "-m",
        action="store_true",
        help="Minimal output: hide explanations, state changes, and rules",
    )

    args = parser.parse_args()

    # Handle list option
    if args.list:
        list_available_scenarios()
        return

    # Handle search option
    if args.search:
        search_and_display(args.search)
        return

    # If no scenario_id provided, list scenarios
    if not args.scenario_id:
        list_available_scenarios()
        return

    # Determine execution mode
    if args.step:
        mode = ExecutionMode.STEP
    elif args.replay:
        mode = ExecutionMode.REPLAY
    else:
        mode = ExecutionMode.AUTO

    # Run the scenario
    run_scenario_cli(
        scenario_id=args.scenario_id,
        mode=mode,
        delay=args.delay,
        minimal=args.minimal,
    )


if __name__ == "__main__":
    main()
