#!/usr/bin/env python3
"""CLI script to run IBDM scenarios with the real Larsson dialogue engine.

This script runs scenarios through the actual Larsson dialogue manager,
executing integrate→select→generate phases with optional NLG support.

Usage:
    python scripts/run_scenario.py                              # List available scenarios
    python scripts/run_scenario.py nda_basic                    # Run with scripted text
    python scripts/run_scenario.py nda_basic --step             # Run in step mode
    python scripts/run_scenario.py nda_basic --nlg-mode compare # Compare scripted vs NLG
    python scripts/run_scenario.py nda_basic --nlg-mode replace # NLG only (no scripted)
    python scripts/run_scenario.py nda_basic --show-engine-state # Show engine internals
    python scripts/run_scenario.py --list                       # List by category
    python scripts/run_scenario.py --search grounding           # Search scenarios
"""

import argparse
import sys

from rich.console import Console

from ibdm.demo import (
    ExecutionMode,
    list_json_scenarios,
    list_scenarios_by_category,
    run_scenario,
    search_scenarios,
)


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
    nlg_mode: str = "off",
    show_engine_state: bool = False,
) -> None:
    """Run a scenario with specified options.

    Args:
        scenario_id: Scenario identifier
        mode: Execution mode
        delay: Auto-advance delay in seconds
        minimal: If True, hide detailed information
        nlg_mode: NLG mode - "off" (scripted), "compare" (both), "replace" (NLG only)
        show_engine_state: If True, show actual engine state after each turn
    """
    console = Console()

    # Delegate to shared runner helper to keep CLI behavior in sync.
    try:
        run_scenario(
            scenario_id=scenario_id,
            mode=mode,
            auto_delay=delay,
            nlg_mode=nlg_mode,
            show_explanations=not minimal,
            show_state_changes=not minimal,
            show_larsson_rules=not minimal,
            show_metrics=not minimal,
            show_engine_state=show_engine_state,
        )
    except KeyboardInterrupt:
        console.print("\n\n[yellow]⚠️  Interrupted by user (Ctrl+C)[/yellow]")
        sys.exit(0)
    except FileNotFoundError as error:
        console.print(f"[red]Error: {error}[/red]")
        console.print("\n[yellow]Available scenarios:[/yellow]")
        for sid in list_json_scenarios():
            console.print(f"  • {sid}")
        sys.exit(1)
    except Exception as error:  # pragma: no cover - defensive CLI surface
        console.print(f"[red]Error loading scenario: {error}[/red]")
        sys.exit(1)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run IBDM scenarios with rich formatting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                  List available scenarios
  %(prog)s nda_basic                        Run with scripted text (auto mode)
  %(prog)s nda_basic --step                 Run in step mode (press Enter)
  %(prog)s nda_basic --nlg-mode compare     Compare scripted vs NLG output
  %(prog)s nda_basic --nlg-mode replace     NLG only (no scripted text)
  %(prog)s nda_basic --show-engine-state    Show QUD, commitments, plans
  %(prog)s nda_basic --delay 1.0            Run with 1-second delay
  %(prog)s nda_basic --minimal              Run with minimal output
  %(prog)s --list                           List scenarios by category
  %(prog)s --search grounding               Search for scenarios
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

    parser.add_argument(
        "--nlg-mode",
        choices=["off", "compare", "replace"],
        default="off",
        metavar="MODE",
        help="NLG mode: 'off' (scripted text), 'compare' (show both), 'replace' (NLG only)",
    )

    parser.add_argument(
        "--show-engine-state",
        action="store_true",
        help="Show actual dialogue engine state after each turn (QUD, commitments, plans)",
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
        nlg_mode=args.nlg_mode,
        show_engine_state=args.show_engine_state,
    )


if __name__ == "__main__":
    main()
