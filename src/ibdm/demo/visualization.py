"""Dialogue visualization and export utilities for IBDM demo.

Provides enhanced visualization of dialogue history, state transitions,
and export capabilities.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any


@dataclass
class TurnRecord:
    """Record of a single dialogue turn.

    Attributes:
        turn_number: Turn number
        timestamp: ISO timestamp
        speaker: Speaker ID
        utterance: What was said
        move_type: Type of dialogue move
        confidence: Confidence score (if applicable)
        grounding_strategy: Grounding strategy used (if applicable)
        state_snapshot: Internal state snapshot
        nlg_comparison: NLG comparison data (if applicable, compare mode only)
    """

    turn_number: int
    timestamp: str
    speaker: str
    utterance: str
    move_type: str | None = None
    confidence: float | None = None
    grounding_strategy: str | None = None
    state_snapshot: dict[str, Any] | None = None
    nlg_comparison: dict[str, Any] | None = None


@dataclass
class DialogueHistory:
    """Complete dialogue history with metadata.

    Attributes:
        session_id: Unique session identifier
        start_time: Session start timestamp
        end_time: Session end timestamp (None if ongoing)
        turns: List of turn records
        metadata: Additional session metadata
    """

    session_id: str
    start_time: str
    end_time: str | None = None
    turns: list[TurnRecord] | None = None
    metadata: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        """Initialize mutable defaults."""
        if self.turns is None:
            self.turns = []
        if self.metadata is None:
            self.metadata = {}

    def add_turn(
        self,
        turn_number: int,
        speaker: str,
        utterance: str,
        move_type: str | None = None,
        confidence: float | None = None,
        grounding_strategy: str | None = None,
        state_snapshot: dict[str, Any] | None = None,
        nlg_comparison: dict[str, Any] | None = None,
    ) -> None:
        """Add a turn to the history.

        Args:
            turn_number: Turn number
            speaker: Speaker ID
            utterance: What was said
            move_type: Type of dialogue move
            confidence: Confidence score
            grounding_strategy: Grounding strategy used
            state_snapshot: Internal state snapshot
            nlg_comparison: NLG comparison data (compare mode only)
        """
        if self.turns is None:
            self.turns = []

        turn = TurnRecord(
            turn_number=turn_number,
            timestamp=datetime.now().isoformat(),
            speaker=speaker,
            utterance=utterance,
            move_type=move_type,
            confidence=confidence,
            grounding_strategy=grounding_strategy,
            state_snapshot=state_snapshot,
            nlg_comparison=nlg_comparison,
        )
        self.turns.append(turn)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary.

        Returns:
            Dictionary representation
        """
        turns_list = [asdict(turn) for turn in self.turns] if self.turns else []
        return {
            "session_id": self.session_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "turns": turns_list,
            "metadata": self.metadata or {},
        }

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string.

        Args:
            indent: JSON indentation level

        Returns:
            JSON string
        """
        return json.dumps(self.to_dict(), indent=indent)

    def save_to_file(self, filepath: str) -> None:
        """Save history to JSON file.

        Args:
            filepath: Path to save file
        """
        with open(filepath, "w") as f:
            f.write(self.to_json())

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DialogueHistory:
        """Create from dictionary.

        Args:
            data: Dictionary data

        Returns:
            DialogueHistory instance
        """
        turns = [TurnRecord(**turn) for turn in data.get("turns", [])]
        return cls(
            session_id=data["session_id"],
            start_time=data["start_time"],
            end_time=data.get("end_time"),
            turns=turns,
            metadata=data.get("metadata", {}),
        )

    @classmethod
    def load_from_file(cls, filepath: str) -> DialogueHistory:
        """Load history from JSON file.

        Args:
            filepath: Path to load file

        Returns:
            DialogueHistory instance
        """
        with open(filepath) as f:
            data = json.load(f)
        return cls.from_dict(data)


class DialogueVisualizer:
    """Visualizer for dialogue history and state transitions.

    This class provides methods to format and export dialogue history and state
    transitions into various human-readable formats. It is designed to be a
    standalone utility for analyzing and presenting dialogue data from IBDM sessions.

    The visualizer supports multiple output formats, including:
    - Detailed, multi-line formatting for each turn
    - Compact, single-line formatting for a quick overview
    - State timeline visualization for tracking specific metrics
    - Export to Markdown and CSV for external analysis

    Example:
        history = DialogueHistory(...)
        visualizer = DialogueVisualizer()
        print(visualizer.format_history(history))
        markdown_export = visualizer.export_to_markdown(history)
    """

    def __init__(self, width: int = 70) -> None:
        """Initialize visualizer.

        Args:
            width: Display width in characters
        """
        self.width = width

    def format_turn(
        self,
        turn: TurnRecord,
        show_metadata: bool = True,
        show_state: bool = False,
    ) -> str:
        """Formats a single dialogue turn into a detailed, multi-line string.

        This method provides a comprehensive view of a single turn, including
        the speaker, utterance, and optional metadata and state information.

        Args:
            turn: The TurnRecord object to format.
            show_metadata: If True, includes dialogue move type, confidence, and
                           grounding strategy.
            show_state: If True, includes a snapshot of the dialogue state.

        Returns:
            A formatted string representing the turn.
        """
        lines: list[str] = []

        # Turn header
        lines.append(f"\n{'=' * self.width}")
        lines.append(f"Turn {turn.turn_number} - {turn.speaker}")
        if show_metadata and turn.timestamp:
            lines.append(f"Time: {turn.timestamp}")
        lines.append(f"{'=' * self.width}")

        # Utterance
        lines.append(f"{turn.speaker}: {turn.utterance}")

        # Metadata
        if show_metadata:
            metadata_items: list[str] = []
            if turn.move_type:
                metadata_items.append(f"Move: {turn.move_type}")
            if turn.confidence is not None:
                metadata_items.append(f"Confidence: {turn.confidence:.2f}")
            if turn.grounding_strategy:
                metadata_items.append(f"Strategy: {turn.grounding_strategy}")

            if metadata_items:
                lines.append(f"[{', '.join(metadata_items)}]")

        # State snapshot
        if show_state and turn.state_snapshot:
            lines.append("\nState:")
            for key, value in turn.state_snapshot.items():
                lines.append(f"  {key}: {value}")

        return "\n".join(lines)

    def format_history(
        self,
        history: DialogueHistory,
        show_metadata: bool = True,
        show_state: bool = False,
    ) -> str:
        """Formats the complete dialogue history into a detailed string.

        This method provides a comprehensive, multi-line representation of the
        entire dialogue session, including a header, all turns, and a summary
        footer.

        Args:
            history: The DialogueHistory object to format.
            show_metadata: If True, shows metadata for each turn.
            show_state: If True, shows the state snapshot for each turn.

        Returns:
            A formatted string of the entire dialogue history.
        """
        lines: list[str] = []

        # Session header
        lines.append(f"\n{'=' * self.width}")
        lines.append(f"Dialogue Session: {history.session_id}")
        lines.append(f"Started: {history.start_time}")
        if history.end_time:
            lines.append(f"Ended: {history.end_time}")
        if history.metadata:
            for key, value in history.metadata.items():
                lines.append(f"{key}: {value}")
        lines.append(f"{'=' * self.width}")

        # Turns
        if history.turns:
            for turn in history.turns:
                lines.append(self.format_turn(turn, show_metadata, show_state))

        # Footer
        lines.append(f"\n{'=' * self.width}")
        turn_count = len(history.turns) if history.turns else 0
        lines.append(f"Total turns: {turn_count}")
        lines.append(f"{'=' * self.width}\n")

        return "\n".join(lines)

    def format_compact_history(self, history: DialogueHistory) -> str:
        """Formats the dialogue history into a compact, single-line-per-turn view.

        This method is useful for getting a quick overview of the dialogue flow
        without the detailed metadata or state information.

        Args:
            history: The DialogueHistory object to format.

        Returns:
            A compact, formatted string of the dialogue history.
        """
        lines: list[str] = []
        lines.append(f"\n{'=' * self.width}")
        lines.append(f"Dialogue History: {history.session_id}")
        lines.append(f"{'=' * self.width}")

        if history.turns:
            for turn in history.turns:
                # Compact format: Turn X [speaker]: utterance
                line = f"{turn.turn_number:3d}. [{turn.speaker:6s}] {turn.utterance}"
                if turn.confidence is not None:
                    line += f" (conf={turn.confidence:.2f})"
                lines.append(line)

        lines.append(f"{'=' * self.width}\n")
        return "\n".join(lines)

    def format_state_timeline(self, history: DialogueHistory, state_key: str) -> str:
        """Generates a timeline showing the value of a specific state variable over turns.

        This method is useful for tracking how a particular aspect of the dialogue
        state, such as QUD depth or the number of commitments, changes over time.

        Args:
            history: The DialogueHistory object containing the state snapshots.
            state_key: The key of the state variable to track (e.g., "qud_depth").

        Returns:
            A formatted string showing the state variable's timeline.
        """
        lines: list[str] = []
        lines.append(f"\n{'=' * self.width}")
        lines.append(f"State Timeline: {state_key}")
        lines.append(f"{'=' * self.width}")

        if history.turns:
            for turn in history.turns:
                if turn.state_snapshot and state_key in turn.state_snapshot:
                    value = turn.state_snapshot[state_key]
                    lines.append(f"Turn {turn.turn_number:3d}: {value}")

        lines.append(f"{'=' * self.width}\n")
        return "\n".join(lines)

    def export_to_markdown(self, history: DialogueHistory) -> str:
        """Exports the dialogue history to a Markdown-formatted string.

        This method generates a structured Markdown document, making it easy to
        share or document the dialogue session.

        Args:
            history: The DialogueHistory object to export.

        Returns:
            A string containing the dialogue history in Markdown format.
        """
        lines: list[str] = []

        # Header
        lines.append(f"# Dialogue Session: {history.session_id}\n")
        lines.append(f"**Started:** {history.start_time}")
        if history.end_time:
            lines.append(f"**Ended:** {history.end_time}")
        lines.append("")

        if history.metadata:
            lines.append("## Session Metadata\n")
            for key, value in history.metadata.items():
                lines.append(f"- **{key}:** {value}")
            lines.append("")

        # Turns
        lines.append("## Dialogue\n")
        if history.turns:
            for turn in history.turns:
                lines.append(f"### Turn {turn.turn_number}\n")
                lines.append(f"**{turn.speaker}:** {turn.utterance}\n")

                if turn.move_type or turn.confidence or turn.grounding_strategy:
                    lines.append("**Metadata:**")
                    if turn.move_type:
                        lines.append(f"- Move Type: `{turn.move_type}`")
                    if turn.confidence is not None:
                        lines.append(f"- Confidence: {turn.confidence:.2f}")
                    if turn.grounding_strategy:
                        lines.append(f"- Grounding: `{turn.grounding_strategy}`")
                    lines.append("")

        # Summary
        lines.append("## Summary\n")
        turn_count = len(history.turns) if history.turns else 0
        lines.append(f"- Total turns: {turn_count}")
        lines.append("")

        return "\n".join(lines)

    def export_to_csv(self, history: DialogueHistory) -> str:
        """Exports the dialogue history to a CSV-formatted string.

        This method converts the dialogue history into a CSV format, suitable for
        data analysis in spreadsheets or other tools. Each turn is represented
        as a single row.

        Args:
            history: The DialogueHistory object to export.

        Returns:
            A string containing the dialogue history in CSV format.
        """
        lines: list[str] = []

        # Header
        lines.append("turn,timestamp,speaker,utterance,move_type,confidence,grounding_strategy")

        # Rows
        if history.turns:
            for turn in history.turns:
                confidence_str = f"{turn.confidence:.2f}" if turn.confidence is not None else ""
                grounding_str = turn.grounding_strategy or ""
                move_type_str = turn.move_type or ""

                # Escape utterance for CSV (quotes)
                utterance = turn.utterance.replace('"', '""')

                lines.append(
                    f"{turn.turn_number},{turn.timestamp},{turn.speaker},"
                    f'"{utterance}",{move_type_str},{confidence_str},{grounding_str}'
                )

        return "\n".join(lines)
