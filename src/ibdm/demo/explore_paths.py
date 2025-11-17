"""CLI for exhaustive path exploration.

Run scenario exploration to discover all possible dialogue paths.
"""

import sys
from typing import Any

from ibdm.demo.path_explorer import (
    PathExplorer,
    generate_exploration_report,
    generate_tree_visualization,
)
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
    print("  IBiS Path Explorer - Exhaustive Dialogue Path Analysis")
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
        print(f"  {i}. {scenario.name}")

    offset = len(ibis3_scenarios)
    print("\nIBiS-2 Scenarios (Grounding & Feedback):")
    for i, scenario in enumerate(ibis2_scenarios, offset + 1):
        print(f"  {i}. {scenario.name}")

    offset += len(ibis2_scenarios)
    print("\nIBiS-4 Scenarios (Action-Oriented Dialogue):")
    for i, scenario in enumerate(ibis4_scenarios, offset + 1):
        print(f"  {i}. {scenario.name}")

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
        depth_choice = input("\nMaximum depth (1-3, default: 3): ").strip()
        if not depth_choice:
            max_depth = 3
            break

        try:
            max_depth = int(depth_choice)
            if 1 <= max_depth <= 3:
                break
            print("Please enter a number between 1 and 3")
        except ValueError:
            print("Invalid input. Please enter a number")

    print(f"\n✓ Selected: {selected_scenario.name}")
    print(f"✓ Max depth: {max_depth}")
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
    print(f"\nExploring all paths up to depth {max_depth}...")
    print("This may take a few seconds for depth 3...")
    print()

    explorer = PathExplorer(selected_scenario, domain)
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
        print("  5. Exit")
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
            print("\nGoodbye!")
            break

        else:
            print("Invalid option. Please select 1-5.\n")


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
