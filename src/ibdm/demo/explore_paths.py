"""CLI for best-first beam search path exploration.

Run scenario exploration using beam search to discover high-quality dialogue paths.
"""

import sys
from typing import Any

from ibdm.demo.path_explorer import (
    PathExplorer,
    generate_exploration_report,
    generate_top_paths_report,
    generate_tree_visualization,
)
from ibdm.demo.scenario_distractors import SCENARIO_DISTRACTORS
from ibdm.demo.scenarios import (
    get_ibis2_scenarios,
    get_ibis3_scenarios,
    get_ibis4_scenarios,
)
from ibdm.domains.nda_domain import get_nda_domain
from ibdm.domains.travel_domain import get_travel_domain


def main() -> None:
    """Main entry point for path exploration."""
    print("\n" + "=" * 70)
    print("  IBiS Path Explorer - Best-First Beam Search")
    print("=" * 70)
    print()

    # Get all scenarios
    ibis3_scenarios = get_ibis3_scenarios()
    ibis2_scenarios = get_ibis2_scenarios()
    ibis4_scenarios = get_ibis4_scenarios()
    all_scenarios = ibis3_scenarios + ibis2_scenarios + ibis4_scenarios

    print("Available Scenarios:")
    print("-" * 70)
    print("\nIBiS-3 Scenarios (Question Accommodation):")
    for i, scenario in enumerate(ibis3_scenarios, 1):
        has_distractors = scenario.name in SCENARIO_DISTRACTORS
        marker = "✓" if has_distractors else " "
        has_payoff = any(step.is_payoff for step in scenario.steps)
        payoff_marker = "⭐" if has_payoff else " "
        print(f"  {i}. [{marker}] {scenario.name} {payoff_marker}")

    offset = len(ibis3_scenarios)
    print("\nIBiS-2 Scenarios (Grounding & Feedback):")
    for i, scenario in enumerate(ibis2_scenarios, offset + 1):
        has_distractors = scenario.name in SCENARIO_DISTRACTORS
        marker = "✓" if has_distractors else " "
        has_payoff = any(step.is_payoff for step in scenario.steps)
        payoff_marker = "⭐" if has_payoff else " "
        print(f"  {i}. [{marker}] {scenario.name} {payoff_marker}")

    offset += len(ibis2_scenarios)
    print("\nIBiS-4 Scenarios (Action-Oriented Dialogue):")
    for i, scenario in enumerate(ibis4_scenarios, offset + 1):
        has_distractors = scenario.name in SCENARIO_DISTRACTORS
        marker = "✓" if has_distractors else " "
        has_payoff = any(step.is_payoff for step in scenario.steps)
        payoff_marker = "⭐" if has_payoff else " "
        print(f"  {i}. [{marker}] {scenario.name} {payoff_marker}")

    print("-" * 70)
    print("\nLegend: [✓] = Has distractors  ⭐ = Has payoff state")
    print("-" * 70)

    # Select scenario
    while True:
        choice = input(f"\nSelect scenario (1-{len(all_scenarios)}) or 'q' to quit: ").strip()

        if choice.lower() == "q":
            print("Goodbye!")
            return

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(all_scenarios):
                selected_scenario = all_scenarios[idx]
                break
            print(f"Please enter a number between 1 and {len(all_scenarios)}")
        except ValueError:
            print("Invalid input. Please enter a number or 'q'")

    # Select depth
    while True:
        depth_choice = input("\nMaximum depth (default: 20): ").strip()
        if not depth_choice:
            max_depth = 20
            break

        try:
            max_depth = int(depth_choice)
            if max_depth >= 1:
                if max_depth > 30:
                    confirm = input(
                        f"Warning: Depth {max_depth} may generate many paths "
                        f"and take significant time. Continue? (y/n): "
                    ).strip()
                    if confirm.lower() == "y":
                        break
                else:
                    break
            else:
                print("Please enter a positive number")
        except ValueError:
            print("Invalid input. Please enter a number")

    # Select beam size
    while True:
        beam_choice = input("\nBeam size (default: 200): ").strip()
        if not beam_choice:
            beam_size = 200
            break

        try:
            beam_size = int(beam_choice)
            if beam_size >= 1:
                break
            else:
                print("Please enter a positive number")
        except ValueError:
            print("Invalid input. Please enter a number")

    # Select turn penalty
    while True:
        penalty_choice = input(
            "\nTurn penalty (default: 5.0, higher favors shorter paths): "
        ).strip()
        if not penalty_choice:
            turn_penalty = 5.0
            break

        try:
            turn_penalty = float(penalty_choice)
            if turn_penalty >= 0:
                break
            else:
                print("Please enter a non-negative number")
        except ValueError:
            print("Invalid input. Please enter a number")

    # Select exploration mode
    while True:
        mode_choice = input(
            "\nExploration mode:\n"
            "  1. Full exploration (all choices including distractors)\n"
            "  2. Expected path only (no distractors)\n"
            "Select (1-2, default: 1): "
        ).strip()
        if not mode_choice or mode_choice == "1":
            expected_only = False
            break
        elif mode_choice == "2":
            expected_only = True
            break
        else:
            print("Invalid input. Please enter 1 or 2")

    print(f"\n✓ Selected: {selected_scenario.name}")
    print(f"✓ Max depth: {max_depth}")
    print(f"✓ Beam size: {beam_size}")
    print(f"✓ Turn penalty: {turn_penalty}")
    print(f"✓ Mode: {'Expected path only' if expected_only else 'Full exploration'}")
    print()

    # Determine domain
    domain: Any
    if "nda" in selected_scenario.name.lower():
        domain = get_nda_domain()
        print("✓ Domain: NDA")
    else:
        domain = get_travel_domain()
        print("✓ Domain: Travel")

    # Create explorer
    print(f"\nExploring paths up to depth {max_depth} with beam size {beam_size}...")
    print(f"Turn penalty: {turn_penalty} (favors shorter dialogues)")
    print(
        f"Mode: {'Expected path only' if expected_only else 'Full exploration (with distractors)'}"
    )
    print("Using best-first beam search...")
    print()

    explorer = PathExplorer(
        selected_scenario,
        domain,
        beam_size=beam_size,
        turn_penalty=turn_penalty,
        expected_only=expected_only,
    )
    result = explorer.explore_paths(max_depth=max_depth)

    print("✓ Exploration complete!")
    print(f"  - Total paths: {result.total_paths}")
    print(f"  - Unique states: {len(result.unique_states)}")
    print()

    # Display options
    while True:
        print("Display Options:")
        print("  1. Summary report")
        print("  2. Tree visualization (depth 1)")
        print("  3. Tree visualization (depth 2)")
        print("  4. Tree visualization (full depth)")
        print("  5. Top 5 highest-scoring paths to payoff")
        print("  6. Exit")
        print()

        option = input("Select option: ").strip()

        if option == "1":
            print()
            report = generate_exploration_report(result)
            print(report)
            print()

        elif option == "2":
            print()
            tree = generate_tree_visualization(result, max_depth=1)
            print(tree)
            print()

        elif option == "3":
            print()
            tree = generate_tree_visualization(result, max_depth=2)
            print(tree)
            print()

        elif option == "4":
            print()
            tree = generate_tree_visualization(result, max_depth=max_depth)
            print(tree)
            print()

        elif option == "5":
            print()
            top_paths = generate_top_paths_report(result, selected_scenario, top_n=5)
            print(top_paths)
            print()

        elif option == "6":
            print("\nGoodbye!")
            break

        else:
            print("Invalid option. Please select 1-6.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExploration interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
