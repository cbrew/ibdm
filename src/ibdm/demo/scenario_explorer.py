"""Interactive Scenario Explorer with Choice-Based Navigation.

Allows users to explore IBiS scenarios by choosing between:
- Expected dialogue moves (from the scenario)
- Distractors (alternative moves that lead to different trajectories)
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any

from ibdm.core import InformationState
from ibdm.demo.scenarios import DemoScenario, ScenarioStep


class MoveCategory(Enum):
    """Categories of dialogue moves for distractor generation."""

    EXPECTED = "expected"  # The move from the scenario
    INVALID_ANSWER = "invalid_answer"  # Wrong/nonsensical answer
    CLARIFICATION_REQUEST = "clarification_request"  # User asks for clarification
    NESTED_QUESTION = "nested_question"  # User asks a different question
    VOLUNTEER_INFO = "volunteer_info"  # User provides extra information
    CORRECTION = "correction"  # User corrects previous answer
    REJECTION = "rejection"  # User rejects system's move


@dataclass
class ChoiceOption:
    """A dialogue move choice presented to the user."""

    id: int
    category: MoveCategory
    utterance: str
    description: str
    expected_trajectory: str  # What happens next


class DistractorGenerator:
    """Generates plausible distractor moves based on current dialogue context."""

    def __init__(self, domain: Any):
        """Initialize with domain knowledge."""
        self.domain = domain

    def generate_distractors(
        self, expected_step: ScenarioStep, state: InformationState
    ) -> list[ChoiceOption]:
        """Generate distractor options for a given scenario step.

        Args:
            expected_step: The expected scenario step (contains expected utterance)
            state: Current dialogue state

        Returns:
            List of choice options (expected + distractors)
        """
        choices: list[ChoiceOption] = []

        # Option 1: Expected move (from scenario)
        choices.append(
            ChoiceOption(
                id=1,
                category=MoveCategory.EXPECTED,
                utterance=expected_step.utterance,
                description=f"[Expected] {expected_step.description or 'Continue on scenario path'}",
                expected_trajectory="Scenario continues as expected",
            )
        )

        # Generate distractors based on current QUD
        if state.shared.qud:
            top_question = state.shared.qud[-1]
            predicate = getattr(top_question, "predicate", None)

            # Option 2: Invalid answer (triggers clarification)
            if predicate:
                choices.append(self._generate_invalid_answer(predicate, len(choices) + 1))

            # Option 3: Nested question (user asks for clarification)
            choices.append(self._generate_nested_question(predicate, len(choices) + 1))

            # Option 4: Volunteer info (if there are pending issues)
            if state.private.issues:
                choices.append(self._generate_volunteer_info(state, len(choices) + 1))

        # Option 5: Correction (if there are existing commitments)
        if state.shared.commitments:
            choices.append(self._generate_correction(state, len(choices) + 1))

        return choices

    def _generate_invalid_answer(self, predicate: str | None, option_id: int) -> ChoiceOption:
        """Generate an invalid answer option."""
        invalid_answers = {
            "parties": "blue",
            "effective_date": "yesterday",
            "dest_city": "123",
            "price": "elephant",
            "term": "forever",
        }
        invalid = invalid_answers.get(predicate or "", "invalid")

        return ChoiceOption(
            id=option_id,
            category=MoveCategory.INVALID_ANSWER,
            utterance=invalid,
            description="[Distractor] Invalid answer → System asks for clarification",
            expected_trajectory="System detects invalid answer, generates clarification question (Rule 4.3)",
        )

    def _generate_nested_question(self, predicate: str | None, option_id: int) -> ChoiceOption:
        """Generate a nested question option."""
        nested_questions = {
            "parties": "What format should I use for the parties?",
            "effective_date": "Can the effective date be in the past?",
            "dest_city": "What cities do you fly to?",
            "price": "What's included in the price?",
            "term": "What's the minimum term?",
        }
        question = nested_questions.get(predicate or "", "Can you give me more details?")

        return ChoiceOption(
            id=option_id,
            category=MoveCategory.NESTED_QUESTION,
            utterance=question,
            description="[Distractor] User asks clarifying question → Pushed to QUD above current question",
            expected_trajectory="System pushes user's question to QUD (stack), answers it, then returns to original question",
        )

    def _generate_volunteer_info(self, state: InformationState, option_id: int) -> ChoiceOption:
        """Generate a volunteer information option."""
        # Get the current question and next issue
        current_q = state.shared.qud[-1] if state.shared.qud else None
        next_issue = state.private.issues[0] if state.private.issues else None

        if not current_q or not next_issue:
            return ChoiceOption(
                id=option_id,
                category=MoveCategory.VOLUNTEER_INFO,
                utterance="Acme Corp and Smith Inc, effective January 1, 2025",
                description="[Distractor] Volunteer multiple facts → System processes both",
                expected_trajectory="System accepts current answer + volunteers next answer, skips asking for volunteered info",
            )

        # Generate volunteer info based on predicates
        current_pred = getattr(current_q, "predicate", "")
        next_pred = getattr(next_issue, "predicate", "")

        volunteer_combos = {
            ("parties", "effective_date"): "Acme Corp and Smith Inc, effective January 1, 2025",
            (
                "dest_city",
                "depart_date",
            ): "Paris, departing March 15",
            ("effective_date", "term"): "January 1, 2025, for a term of 5 years",
        }

        utterance = volunteer_combos.get((current_pred, next_pred), "Answer 1, and also answer 2")

        return ChoiceOption(
            id=option_id,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance=utterance,
            description=f"[Distractor] Volunteer info for {next_pred} → System removes it from issues, skips asking",
            expected_trajectory=f"System integrates both answers, removes {next_pred} from private.issues, skips that question",
        )

    def _generate_correction(self, state: InformationState, option_id: int) -> ChoiceOption:
        """Generate a correction option."""
        if not state.shared.commitments:
            return ChoiceOption(
                id=option_id,
                category=MoveCategory.CORRECTION,
                utterance="Actually, let me change my previous answer",
                description="[Distractor] User corrects previous answer → Belief revision",
                expected_trajectory="System retracts old commitment, re-accommodates question, integrates new answer",
            )

        # Get first commitment to correct
        first_commitment = list(state.shared.commitments)[0]

        corrections = {
            "parties": "Actually, the parties should be XYZ Corp and ABC Inc",
            "effective_date": "Wait, the effective date should be April 1, 2025",
            "dest_city": "Actually, I want to go to London, not Paris",
            "term": "Let me change the term to 3 years",
        }

        # Try to find matching correction
        utterance = "Actually, let me change my previous answer"
        for key, correction in corrections.items():
            if key in first_commitment:
                utterance = correction
                break

        return ChoiceOption(
            id=option_id,
            category=MoveCategory.CORRECTION,
            utterance=utterance,
            description="[Distractor] Correction → System retracts commitment, re-accommodates question (Rules 4.6-4.8)",
            expected_trajectory="Retract old commitment → Re-accommodate question to issues → Integrate new answer → Check dependent questions",
        )


class TrajectoryTracker:
    """Tracks the path taken through the scenario vs. expected path."""

    def __init__(self, scenario: DemoScenario):
        """Initialize tracker with expected scenario."""
        self.scenario = scenario
        self.expected_step_index = 0
        self.actual_moves: list[tuple[MoveCategory, str]] = []
        self.divergence_points: list[int] = []

    def record_choice(self, choice: ChoiceOption) -> None:
        """Record a user's choice."""
        self.actual_moves.append((choice.category, choice.utterance))

        if choice.category != MoveCategory.EXPECTED:
            self.divergence_points.append(len(self.actual_moves) - 1)

        # Only advance expected step if we're on the expected path
        if choice.category == MoveCategory.EXPECTED:
            self.expected_step_index += 1

    def get_status(self) -> dict[str, Any]:
        """Get current trajectory status."""
        return {
            "total_moves": len(self.actual_moves),
            "expected_moves": self.expected_step_index,
            "divergences": len(self.divergence_points),
            "on_expected_path": len(self.divergence_points) == 0,
            "completion": self.expected_step_index / len(self.scenario.steps)
            if self.scenario.steps
            else 0.0,
        }

    def format_path(self) -> str:
        """Format the trajectory path for display."""
        lines = ["Trajectory Path:"]
        lines.append("=" * 50)

        for i, (category, utterance) in enumerate(self.actual_moves):
            marker = "✓" if category == MoveCategory.EXPECTED else "↻"
            diverged = " [DIVERGED]" if i in self.divergence_points else ""
            lines.append(f"{marker} {i + 1}. [{category.value}] {utterance}{diverged}")

        status = self.get_status()
        lines.append("=" * 50)
        lines.append(f"Divergences: {status['divergences']}")
        lines.append(f"Completion: {status['completion']:.0%} of expected scenario")

        return "\n".join(lines)


class ScenarioExplorer:
    """Interactive scenario explorer with choice-based navigation."""

    def __init__(self, scenario: DemoScenario, state: InformationState, domain: Any) -> None:
        """Initialize explorer with scenario and initial state.

        Args:
            scenario: The scenario to explore
            state: Initial information state
            domain: Domain for validation and distractor generation
        """
        self.scenario = scenario
        self.state = state
        self.domain = domain
        self.distractor_gen = DistractorGenerator(domain)
        self.tracker = TrajectoryTracker(scenario)
        self.current_step_index = 0

    def get_current_choices(self) -> list[ChoiceOption]:
        """Get available choices for the current dialogue state.

        Returns:
            List of choice options (expected + distractors)
        """
        if self.current_step_index >= len(self.scenario.steps):
            return []

        expected_step = self.scenario.steps[self.current_step_index]

        # Only generate choices for user turns
        if expected_step.speaker != "user":
            return []

        # Try to get scenario-specific distractors first
        from ibdm.demo.scenario_distractors import get_distractors_for_turn

        specific_distractors = get_distractors_for_turn(self.scenario.name, self.current_step_index)

        if specific_distractors:
            return specific_distractors

        # Fall back to generic distractor generation
        return self.distractor_gen.generate_distractors(expected_step, self.state)

    def display_choices(self, choices: list[ChoiceOption]) -> None:
        """Display choices to the user."""
        print("\n" + "=" * 70)
        print("Your dialogue options:")
        print("=" * 70)

        for choice in choices:
            print(f"\n{choice.id}. {choice.description}")
            print(f'   Say: "{choice.utterance}"')
            print(f"   → {choice.expected_trajectory}")

        print("\n" + "=" * 70)
        print(f"Choose option (1-{len(choices)}) or type 'custom' for your own response")
        print("Commands: /state, /path, /help, /quit")
        print("=" * 70)

    def select_choice(self, user_input: str, choices: list[ChoiceOption]) -> ChoiceOption | None:
        """Process user's choice selection.

        Args:
            user_input: User's input (number or 'custom')
            choices: Available choices

        Returns:
            Selected choice option, or None if invalid
        """
        try:
            choice_num = int(user_input)
            if 1 <= choice_num <= len(choices):
                return choices[choice_num - 1]
        except ValueError:
            pass

        return None

    def advance_step(self) -> None:
        """Advance to next step in scenario."""
        self.current_step_index += 1

    def is_complete(self) -> bool:
        """Check if scenario exploration is complete."""
        return self.current_step_index >= len(self.scenario.steps)

    def get_trajectory_status(self) -> dict[str, Any]:
        """Get current trajectory tracking status."""
        return self.tracker.get_status()

    def display_trajectory(self) -> None:
        """Display the current trajectory path."""
        print("\n" + self.tracker.format_path())

    def display_state(self) -> None:
        """Display current dialogue state."""
        print("\n" + "=" * 70)
        print("Current Dialogue State:")
        print("=" * 70)
        print(f"QUD: {len(self.state.shared.qud)} questions")
        if self.state.shared.qud:
            for i, q in enumerate(self.state.shared.qud):
                print(f"  {i + 1}. {getattr(q, 'predicate', str(q))} = ?")

        print(f"Private Issues: {len(self.state.private.issues)} pending")
        if self.state.private.issues:
            for i, q in enumerate(self.state.private.issues[:3]):
                print(f"  {i + 1}. {getattr(q, 'predicate', str(q))} = ?")
            if len(self.state.private.issues) > 3:
                print(f"  ... and {len(self.state.private.issues) - 3} more")

        print(f"Commitments: {len(self.state.shared.commitments)} facts")
        for i, c in enumerate(list(self.state.shared.commitments)[:5]):
            print(f"  - {c}")
        if len(self.state.shared.commitments) > 5:
            print(f"  ... and {len(self.state.shared.commitments) - 5} more")

        print("=" * 70)

    def display_help(self) -> None:
        """Display help information."""
        help_text = """
Interactive Scenario Explorer - Help
====================================

How it works:
1. At each dialogue turn, you'll see multiple options
2. Option 1 is always the expected move from the scenario
3. Options 2+ are distractors that explore alternative paths

Choice Options:
  [Expected]        - Follows the original scenario path
  [Distractor]      - Explores alternative dialogue behavior

Commands:
  /state            - Show current dialogue state (QUD, issues, commitments)
  /path             - Show trajectory path (expected vs. actual)
  /help             - Show this help message
  /quit             - Exit explorer

Making Choices:
  - Type a number (1, 2, 3...) to select an option
  - Type 'custom' to enter your own response (advanced)

Trajectory Tracking:
  ✓ = On expected path
  ↻ = Diverged from expected path
  [DIVERGED] = Divergence point marker

Enjoy exploring! 🚀
"""
        print(help_text)
