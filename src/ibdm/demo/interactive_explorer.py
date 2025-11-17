"""Interactive Scenario Explorer CLI.

Run scenarios with user-controlled choice-based navigation.
"""

import sys
from typing import Any

from ibdm.core import InformationState
from ibdm.demo.scenario_explorer import ChoiceOption, MoveCategory, ScenarioExplorer
from ibdm.demo.scenarios import (
    DemoScenario,
    get_ibis2_scenarios,
    get_ibis3_scenarios,
)
from ibdm.domains.nda_domain import get_nda_domain
from ibdm.domains.travel_domain import get_travel_domain

# Note: Not using DialogueMoveEngine or RuleSets in this version
# This is a visualization-focused tool for exploring scenarios
# from ibdm.engine.dialogue_engine import DialogueMoveEngine
# from ibdm.rules import create_integration_rules, create_selection_rules, RuleSet


class InteractiveExplorerCLI:
    """CLI for interactive scenario exploration."""

    def __init__(self) -> None:
        """Initialize the interactive explorer CLI."""
        self.scenario: DemoScenario | None = None
        self.explorer: ScenarioExplorer | None = None
        # self.engine: DialogueMoveEngine | None = None  # Not used in visualization mode
        self.domain: Any = None
        self.state: InformationState | None = None

    def run(self) -> None:
        """Run the interactive explorer."""
        self._display_welcome()

        # Step 1: Select scenario
        scenario = self._select_scenario()
        if not scenario:
            return

        self.scenario = scenario

        # Step 2: Initialize domain and engine
        self._initialize_engine(scenario)

        # Step 3: Create explorer
        assert self.state is not None
        assert self.domain is not None
        self.explorer = ScenarioExplorer(scenario, self.state, self.domain)

        # Step 4: Run exploration loop
        self._exploration_loop()

        # Step 5: Display summary
        self._display_summary()

    def _display_welcome(self) -> None:
        """Display welcome message."""
        welcome = """
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║          IBiS Interactive Scenario Explorer                          ║
║                                                                      ║
║  Explore dialogue scenarios with choice-based navigation            ║
║  • Choose the expected move to follow the scenario                  ║
║  • Choose distractors to explore alternative paths                  ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
"""
        print(welcome)

    def _select_scenario(self) -> DemoScenario | None:
        """Let user select a scenario to explore.

        Returns:
            Selected scenario or None if user quits
        """
        ibis3_scenarios = get_ibis3_scenarios()
        ibis2_scenarios = get_ibis2_scenarios()
        all_scenarios = ibis3_scenarios + ibis2_scenarios

        print("\nAvailable Scenarios:")
        print("=" * 70)

        print("\nIBiS-3 Scenarios (Question Accommodation):")
        for i, scenario in enumerate(ibis3_scenarios, 1):
            print(f"  {i}. {scenario.name}")
            print(f"     {scenario.description}")

        offset = len(ibis3_scenarios)
        print("\nIBiS-2 Scenarios (Grounding & Feedback):")
        for i, scenario in enumerate(ibis2_scenarios, offset + 1):
            print(f"  {i}. {scenario.name}")
            print(f"     {scenario.description}")

        print("=" * 70)

        while True:
            choice = input(f"\nSelect scenario (1-{len(all_scenarios)}) or 'q' to quit: ").strip()

            if choice.lower() == "q":
                return None

            try:
                idx = int(choice) - 1
                if 0 <= idx < len(all_scenarios):
                    selected = all_scenarios[idx]
                    print(f"\n✓ Selected: {selected.name}")
                    print(f"  Features: {', '.join(selected.features)}")
                    return selected
                print(f"Please enter a number between 1 and {len(all_scenarios)}")
            except ValueError:
                print("Invalid input. Please enter a number or 'q'")

    def _initialize_engine(self, scenario: DemoScenario) -> None:
        """Initialize the dialogue engine for the scenario.

        Args:
            scenario: Selected scenario
        """
        # Determine domain from scenario
        if "nda" in scenario.name.lower():
            self.domain = get_nda_domain()
        else:
            self.domain = get_travel_domain()

        # Create initial state
        self.state = InformationState(agent_id="system")
        self.state.private.beliefs["domain"] = self.domain

        # Note: Not creating full engine in visualization mode
        # We're focusing on exploring scenarios through choices
        # Full engine integration can be added later

        print(f"\n✓ Domain initialized: {self.domain.__class__.__name__}")

    def _exploration_loop(self) -> None:
        """Main exploration loop."""
        assert self.explorer is not None
        assert self.state is not None

        print("\n" + "=" * 70)
        print("Starting Scenario Exploration")
        print("=" * 70)
        print("Type /help for commands, /quit to exit")

        turn = 0

        while not self.explorer.is_complete():
            # Get current expected step
            if self.explorer.current_step_index >= len(self.explorer.scenario.steps):
                break

            expected_step = self.explorer.scenario.steps[self.explorer.current_step_index]

            # If it's a system turn, execute it
            if expected_step.speaker == "system":
                print(f"\n{'─' * 70}")
                print(f"Turn {turn} [System]")
                print(f"{'─' * 70}")

                # Check if this is a document generation step
                if (
                    "document_generated" in str(expected_step.expected_state)
                    and expected_step.description
                    and "document" in expected_step.description.lower()
                ):
                    # Use actual template injection from collected commitments
                    from ibdm.demo.document_generator import (
                        generate_document_from_state,
                    )

                    print("\n[TEMPLATE INJECTION - Using dialogue commitments]")
                    generated_doc = generate_document_from_state(self.state, document_type="nda")
                    print(f"system: {generated_doc}")
                else:
                    print(f"system: {expected_step.utterance}")

                if expected_step.description:
                    print(f"  ({expected_step.description})")

                self.explorer.advance_step()
                turn += 1
                continue

            # User turn - present choices
            print(f"\n{'─' * 70}")
            print(f"Turn {turn} [User]")
            print(f"{'─' * 70}")

            choices = self.explorer.get_current_choices()
            if not choices:
                print("No choices available. Ending exploration.")
                break

            self.explorer.display_choices(choices)

            # Get user selection
            selected_choice = self._get_user_choice(choices)
            if selected_choice is None:
                # User quit
                break

            # Record choice
            self.explorer.tracker.record_choice(selected_choice)

            # Display what happens next
            print(f"\n✓ You chose: {selected_choice.utterance}")
            print(f"→ {selected_choice.expected_trajectory}")

            # Apply the dialogue move to the engine
            self._apply_user_move(selected_choice)

            # Advance to next step
            self.explorer.advance_step()
            turn += 1

            # Brief pause
            input("\nPress Enter to continue...")

    def _get_user_choice(self, choices: list[ChoiceOption]) -> ChoiceOption | None:
        """Get user's choice from options.

        Args:
            choices: Available choices

        Returns:
            Selected choice or None if user quits
        """
        assert self.explorer is not None

        while True:
            user_input = input("\nYour choice: ").strip()

            # Handle commands
            if user_input.startswith("/"):
                if user_input == "/quit":
                    return None
                elif user_input == "/state":
                    self.explorer.display_state()
                    continue
                elif user_input == "/path":
                    self.explorer.display_trajectory()
                    continue
                elif user_input == "/help":
                    self.explorer.display_help()
                    continue
                else:
                    print(f"Unknown command: {user_input}")
                    continue

            # Try to parse as choice number
            choice = self.explorer.select_choice(user_input, choices)
            if choice:
                return choice

            print(
                f"Invalid choice. Please enter a number 1-{len(choices)} or a command (/help, /quit)"
            )

    def _apply_user_move(self, choice: ChoiceOption) -> None:
        """Apply the user's selected move to the dialogue state.

        Args:
            choice: The selected choice option
        """
        assert self.state is not None

        print(f"\n[Simulating move: {choice.category.value}]")

        # Extract commitment from utterance (simple pattern matching for demo)
        commitment = self._extract_commitment_from_utterance(choice.utterance)
        if commitment:
            self.state.shared.commitments.add(commitment)
            print(f"  → Added commitment: {commitment}")

        if choice.category == MoveCategory.EXPECTED:
            print("  → Following expected path")
        elif choice.category == MoveCategory.INVALID_ANSWER:
            print("  → Triggering clarification mechanism")
        elif choice.category == MoveCategory.NESTED_QUESTION:
            print("  → Pushing nested question to QUD")
        elif choice.category == MoveCategory.VOLUNTEER_INFO:
            print("  → Processing volunteer information")
            # Handle volunteer info - may have multiple commitments
            volunteer_commitments = self._extract_volunteer_commitments(choice.utterance)
            for vc in volunteer_commitments:
                if vc and vc not in self.state.shared.commitments:
                    self.state.shared.commitments.add(vc)
                    print(f"  → Added volunteer commitment: {vc}")
        elif choice.category == MoveCategory.CORRECTION:
            print("  → Initiating belief revision")

    def _extract_commitment_from_utterance(self, utterance: str) -> str | None:
        """Extract commitment from user utterance.

        This is a simple pattern matcher for demo purposes.
        In a real system, this would use NLU.

        Args:
            utterance: User's utterance

        Returns:
            Commitment string or None
        """
        # Simple mapping for common NDA scenario utterances
        if "Acme Corp and Smith Inc" in utterance:
            return "parties(Acme Corp and Smith Inc)"
        elif utterance.lower() == "mutual":
            return "nda_type(mutual)"
        elif utterance.lower() == "one-way":
            return "nda_type(one-way)"
        elif "January 1, 2025" in utterance or "2025" in utterance:
            # Extract the date if present
            if "January 1, 2025" in utterance:
                return "effective_date(January 1, 2025)"
        elif "5 years" in utterance or "5 year" in utterance:
            return "duration(5 years)"
        elif utterance == "Perpetual" or utterance.lower() == "perpetual":
            return "duration(perpetual)"
        elif utterance == "California":
            return "governing_law(California)"
        elif utterance == "Delaware":
            return "governing_law(Delaware)"
        elif utterance == "New York":
            return "governing_law(New York)"

        return None

    def _extract_volunteer_commitments(self, utterance: str) -> list[str]:
        """Extract multiple commitments from volunteer info utterance.

        Args:
            utterance: User's utterance with multiple facts

        Returns:
            List of commitment strings
        """
        commitments: list[str] = []

        # Check for each possible commitment in the utterance
        if "Acme Corp" in utterance or "Smith Inc" in utterance:
            commitments.append("parties(Acme Corp and Smith Inc)")
        if "January 1, 2025" in utterance or "2025" in utterance:
            commitments.append("effective_date(January 1, 2025)")
        if "5 year" in utterance:
            commitments.append("duration(5 years)")
        if "California" in utterance:
            commitments.append("governing_law(California)")

        return commitments

    def _display_summary(self) -> None:
        """Display exploration summary."""
        assert self.explorer is not None

        print("\n" + "=" * 70)
        print("Exploration Complete!")
        print("=" * 70)

        status = self.explorer.get_trajectory_status()

        print(f"\nTotal moves: {status['total_moves']}")
        print(f"Expected moves followed: {status['expected_moves']}")
        print(f"Divergences: {status['divergences']}")
        print(f"Completion: {status['completion']:.0%}")

        print("\nFinal trajectory:")
        self.explorer.display_trajectory()

        print("\nThank you for exploring! 🎉")


def main() -> None:
    """Main entry point for the interactive explorer."""
    try:
        cli = InteractiveExplorerCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\nExploration interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
