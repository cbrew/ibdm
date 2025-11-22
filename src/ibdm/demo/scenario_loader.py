"""Unified scenario loader for JSON-based scenarios.

This module provides a single, clean interface for loading and managing
all demo scenarios. All scenarios are stored in JSON format in the
demos/scenarios/ directory.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ibdm.core import Answer, DialogueMove, WhQuestion
from ibdm.core.grounding import ActionLevel
from ibdm.core.moves import Polarity


@dataclass
class ScenarioTurn:
    """A single turn in a scenario.

    Attributes:
        turn: Turn number (1-indexed)
        speaker: Who speaks ("user" or "system")
        utterance: What they say
        move_type: Type of dialogue move (request, answer, ask, inform, etc.)
        business_explanation: What this demonstrates
        larsson_rule: Which Larsson rule applies
        state_changes: Expected state changes
        is_payoff: Whether this turn produces high-value output
        move: Optional structured DialogueMove object (overrides text-based recognition)
        confidence: Optional confidence score for grounding strategies (0.0-1.0)
    """

    turn: int
    speaker: str
    utterance: str
    move_type: str
    business_explanation: str
    larsson_rule: str
    state_changes: dict[str, Any]
    is_payoff: bool = False
    move: DialogueMove | None = None
    confidence: float | None = None


@dataclass
class ScenarioMetadata:
    """Scenario metadata and expected outcomes.

    Attributes:
        scenario_id: Unique identifier
        title: Human-readable title
        description: Brief description
        business_narrative: Business value explanation
        larsson_algorithms: List of Larsson rules/algorithms
        expected_outcomes: Expected metrics (turns, QUD depth, etc.)
        confidence_mode: Grounding strategy (optimistic, cautious, etc.)
        metrics: Quality metrics for this scenario
    """

    scenario_id: str
    title: str
    description: str
    business_narrative: str
    larsson_algorithms: list[str]
    expected_outcomes: dict[str, Any]
    confidence_mode: str
    metrics: dict[str, str]


@dataclass
class Scenario:
    """Complete scenario with metadata and turns.

    Attributes:
        metadata: Scenario metadata
        turns: List of dialogue turns
    """

    metadata: ScenarioMetadata
    turns: list[ScenarioTurn]

    @property
    def scenario_id(self) -> str:
        """Get scenario ID."""
        return self.metadata.scenario_id

    @property
    def title(self) -> str:
        """Get scenario title."""
        return self.metadata.title

    @property
    def total_turns(self) -> int:
        """Get total number of turns."""
        return len(self.turns)

    @property
    def user_turns(self) -> list[ScenarioTurn]:
        """Get all user turns."""
        return [t for t in self.turns if t.speaker == "user"]

    @property
    def system_turns(self) -> list[ScenarioTurn]:
        """Get all system turns."""
        return [t for t in self.turns if t.speaker == "system"]

    @property
    def payoff_turns(self) -> list[ScenarioTurn]:
        """Get all payoff turns (high-value outputs)."""
        return [t for t in self.turns if t.is_payoff]

    def get_turn(self, turn_number: int) -> ScenarioTurn | None:
        """Get turn by number (1-indexed).

        Args:
            turn_number: Turn number to retrieve

        Returns:
            ScenarioTurn if found, None otherwise
        """
        for turn in self.turns:
            if turn.turn == turn_number:
                return turn
        return None


def build_dialogue_move_from_json(
    move_spec: dict[str, Any], speaker: str, agent_id: str = "system"
) -> DialogueMove:
    """Build a DialogueMove from JSON specification.

    Args:
        move_spec: JSON specification with move fields
        speaker: Who is making the move ("user" or "system")
        agent_id: Agent ID for the system (default: "system")

    Returns:
        Constructed DialogueMove object

    Example move_spec formats:
        # ICM move
        {
            "move_type": "icm",
            "feedback_level": "perception",
            "polarity": "negative"
        }

        # Answer with polarity
        {
            "move_type": "answer",
            "content": "Yes",
            "polarity": "positive"
        }

        # Regular answer
        {
            "move_type": "answer",
            "content": "mutual"
        }
    """
    move_type = move_spec.get("move_type", "unknown")

    # Determine speaker ID
    speaker_id = agent_id if speaker == "system" else "user"

    # Build content based on move type
    content: Any = None

    if move_type == "answer":
        # Build Answer object
        answer_content = move_spec.get("content", "")
        polarity = None
        if "polarity" in move_spec:
            polarity = Polarity(move_spec["polarity"])
        content = Answer(content=answer_content, polarity=polarity)

    elif move_type == "ask":
        # Build WhQuestion or other question type
        question_predicate = move_spec.get("predicate", "")
        variable = move_spec.get("variable", "x")
        content = WhQuestion(variable=variable, predicate=question_predicate)

    else:
        # Use raw content if provided
        content = move_spec.get("content")

    # Build base move with metadata
    metadata = {}

    # Extract confidence if specified (for grounding strategies)
    if "confidence" in move_spec:
        metadata["confidence"] = move_spec["confidence"]

    # Build move with metadata only if non-empty
    if metadata:
        move = DialogueMove(
            move_type=move_type,
            content=content,
            speaker=speaker_id,
            metadata=metadata,
        )
    else:
        move = DialogueMove(
            move_type=move_type,
            content=content,
            speaker=speaker_id,
        )

    # Add ICM-specific fields if this is an ICM move
    if move_type == "icm":
        if "feedback_level" in move_spec:
            move.feedback_level = ActionLevel(move_spec["feedback_level"])
        if "polarity" in move_spec:
            move.polarity = Polarity(move_spec["polarity"])
        if "target_move_index" in move_spec:
            move.target_move_index = move_spec["target_move_index"]

    return move


class ScenarioLoader:
    """Loads and manages JSON-based demo scenarios.

    This class provides the single, canonical way to load scenarios.
    All scenarios are stored in JSON format.
    """

    def __init__(self, scenarios_dir: Path | None = None):
        """Initialize scenario loader.

        Args:
            scenarios_dir: Directory containing JSON scenarios.
                          Defaults to demos/scenarios/ relative to project root.
        """
        if scenarios_dir is None:
            # Auto-discover scenarios directory
            # Try relative to this file: src/ibdm/demo/scenario_loader.py
            # Project root is 3 levels up: ../../..
            module_file = Path(__file__)
            project_root = module_file.parent.parent.parent.parent
            scenarios_dir = project_root / "demos" / "scenarios"

        self.scenarios_dir = Path(scenarios_dir)

        if not self.scenarios_dir.exists():
            raise ValueError(f"Scenarios directory not found: {self.scenarios_dir}")

    def list_scenarios(self) -> list[str]:
        """List all available scenario IDs.

        Returns:
            Sorted list of scenario IDs
        """
        scenario_files = self.scenarios_dir.glob("*.json")
        scenario_ids = [f.stem for f in scenario_files]
        return sorted(scenario_ids)

    def list_scenarios_by_category(self) -> dict[str, list[str]]:
        """List scenarios grouped by category.

        Returns:
            Dictionary mapping category to list of scenario IDs
        """
        categories: dict[str, list[str]] = {
            "IBiS-3 (Question Accommodation)": [],
            "IBiS-2 (Grounding)": [],
            "Business Demos": [],
            "Other": [],
        }

        for scenario_id in self.list_scenarios():
            if scenario_id.startswith("ibis3_"):
                categories["IBiS-3 (Question Accommodation)"].append(scenario_id)
            elif scenario_id.startswith("ibis2_"):
                categories["IBiS-2 (Grounding)"].append(scenario_id)
            elif scenario_id.startswith("nda_") or scenario_id.startswith("legal_"):
                categories["Business Demos"].append(scenario_id)
            else:
                categories["Other"].append(scenario_id)

        # Remove empty categories
        return {k: v for k, v in categories.items() if v}

    def load_scenario(self, scenario_id: str) -> Scenario:
        """Load a scenario by ID.

        Args:
            scenario_id: Scenario identifier (without .json extension)

        Returns:
            Loaded Scenario object

        Raises:
            FileNotFoundError: If scenario file doesn't exist
            ValueError: If JSON is invalid or missing required fields
        """
        scenario_path = self.scenarios_dir / f"{scenario_id}.json"

        if not scenario_path.exists():
            available = ", ".join(self.list_scenarios())
            raise FileNotFoundError(
                f"Scenario '{scenario_id}' not found.\nAvailable scenarios: {available}"
            )

        try:
            with open(scenario_path) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {scenario_path}: {e}") from e

        # Validate required fields
        required_fields = [
            "scenario_id",
            "title",
            "description",
            "business_narrative",
            "larsson_algorithms",
            "expected_outcomes",
            "turns",
        ]
        missing = [f for f in required_fields if f not in data]
        if missing:
            raise ValueError(f"Missing required fields in {scenario_path}: {missing}")

        # Parse metadata
        metadata = ScenarioMetadata(
            scenario_id=data["scenario_id"],
            title=data["title"],
            description=data["description"],
            business_narrative=data["business_narrative"],
            larsson_algorithms=data["larsson_algorithms"],
            expected_outcomes=data["expected_outcomes"],
            confidence_mode=data.get("confidence_mode", "heuristic"),
            metrics=data.get("metrics", {}),
        )

        # Parse turns
        turns: list[ScenarioTurn] = []
        for turn_data in data["turns"]:
            # Handle different field names across scenarios
            business_explanation = turn_data.get(
                "business_explanation",
                turn_data.get("description", f"{turn_data['speaker']} turn"),
            )
            larsson_rule = turn_data.get(
                "larsson_rule", turn_data.get("rule", "Dialogue update rule")
            )

            # Build structured DialogueMove if "move" spec is provided
            structured_move = None
            if "move" in turn_data:
                try:
                    structured_move = build_dialogue_move_from_json(
                        move_spec=turn_data["move"],
                        speaker=turn_data["speaker"],
                        agent_id="system",  # Could be parameterized if needed
                    )
                except Exception as e:
                    # Log warning but continue - scenarios can still use text-based processing
                    print(f"Warning: Failed to build move for turn {turn_data['turn']}: {e}")

            turn = ScenarioTurn(
                turn=turn_data["turn"],
                speaker=turn_data["speaker"],
                utterance=turn_data["utterance"],
                move_type=turn_data["move_type"],
                business_explanation=business_explanation,
                larsson_rule=larsson_rule,
                state_changes=turn_data.get("state_changes", {}),
                is_payoff=turn_data.get("is_payoff", False),
                move=structured_move,
                confidence=turn_data.get("confidence"),
            )
            turns.append(turn)

        return Scenario(metadata=metadata, turns=turns)

    def search_scenarios(self, query: str) -> list[str]:
        """Search scenarios by keyword.

        Args:
            query: Search term (case-insensitive)

        Returns:
            List of matching scenario IDs
        """
        query_lower = query.lower()
        matches: list[str] = []

        for scenario_id in self.list_scenarios():
            try:
                scenario = self.load_scenario(scenario_id)

                # Search in metadata
                searchable = [
                    scenario_id,
                    scenario.title,
                    scenario.metadata.description,
                    scenario.metadata.business_narrative,
                    " ".join(scenario.metadata.larsson_algorithms),
                ]

                if any(query_lower in text.lower() for text in searchable):
                    matches.append(scenario_id)

            except Exception:
                # Skip scenarios that fail to load
                continue

        return sorted(matches)

    def validate_scenario(self, scenario_id: str) -> tuple[bool, list[str]]:
        """Validate a scenario's structure and content.

        Args:
            scenario_id: Scenario to validate

        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues: list[str] = []

        try:
            scenario = self.load_scenario(scenario_id)
        except Exception as e:
            return (False, [f"Failed to load: {e}"])

        # Check turn numbering
        for idx, turn in enumerate(scenario.turns, start=1):
            if turn.turn != idx:
                issues.append(f"Turn {idx} has wrong number: {turn.turn}")

        # Check speaker alternation (warn only, not always required)
        for i in range(len(scenario.turns) - 1):
            if scenario.turns[i].speaker == scenario.turns[i + 1].speaker:
                issues.append(
                    f"Warning: Turns {i + 1} and {i + 2} both from {scenario.turns[i].speaker}"
                )

        # Check for at least one user turn
        if not scenario.user_turns:
            issues.append("No user turns found")

        # Check for at least one system turn
        if not scenario.system_turns:
            issues.append("No system turns found")

        # Check metadata completeness
        if not scenario.metadata.larsson_algorithms:
            issues.append("No Larsson algorithms specified")

        if not scenario.metadata.expected_outcomes:
            issues.append("No expected outcomes specified")

        return (len(issues) == 0, issues)


# Global loader instance (lazy initialization)
_loader: ScenarioLoader | None = None


def get_loader() -> ScenarioLoader:
    """Get the global scenario loader instance.

    Returns:
        ScenarioLoader instance
    """
    global _loader
    if _loader is None:
        _loader = ScenarioLoader()
    return _loader


def list_scenarios() -> list[str]:
    """List all available scenarios.

    Returns:
        Sorted list of scenario IDs
    """
    return get_loader().list_scenarios()


def list_scenarios_by_category() -> dict[str, list[str]]:
    """List scenarios grouped by category.

    Returns:
        Dictionary mapping category to list of scenario IDs
    """
    return get_loader().list_scenarios_by_category()


def load_scenario(scenario_id: str) -> Scenario:
    """Load a scenario by ID.

    Args:
        scenario_id: Scenario identifier

    Returns:
        Loaded Scenario object
    """
    return get_loader().load_scenario(scenario_id)


def search_scenarios(query: str) -> list[str]:
    """Search scenarios by keyword.

    Args:
        query: Search term

    Returns:
        List of matching scenario IDs
    """
    return get_loader().search_scenarios(query)
