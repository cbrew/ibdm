"""Tests for demo visualization module."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from ibdm.demo.visualization import DialogueHistory, DialogueVisualizer, TurnRecord


class TestTurnRecord:
    """Test TurnRecord dataclass."""

    def test_creation(self) -> None:
        """Test basic TurnRecord creation."""
        turn = TurnRecord(
            turn_number=1,
            timestamp="2025-11-16T10:00:00",
            speaker="user",
            utterance="Hello",
            move_type="greet",
            confidence=0.9,
            grounding_strategy="optimistic",
            state_snapshot={"qud_depth": 0},
        )

        assert turn.turn_number == 1
        assert turn.speaker == "user"
        assert turn.utterance == "Hello"
        assert turn.move_type == "greet"
        assert turn.confidence == 0.9
        assert turn.grounding_strategy == "optimistic"
        assert turn.state_snapshot == {"qud_depth": 0}

    def test_creation_minimal(self) -> None:
        """Test TurnRecord with minimal fields."""
        turn = TurnRecord(
            turn_number=1,
            timestamp="2025-11-16T10:00:00",
            speaker="user",
            utterance="Hello",
        )

        assert turn.turn_number == 1
        assert turn.speaker == "user"
        assert turn.utterance == "Hello"
        assert turn.move_type is None
        assert turn.confidence is None
        assert turn.grounding_strategy is None
        assert turn.state_snapshot is None


class TestDialogueHistory:
    """Test DialogueHistory class."""

    def test_creation(self) -> None:
        """Test basic DialogueHistory creation."""
        history = DialogueHistory(
            session_id="test-123",
            start_time="2025-11-16T10:00:00",
        )

        assert history.session_id == "test-123"
        assert history.start_time == "2025-11-16T10:00:00"
        assert history.end_time is None
        assert history.turns == []
        assert history.metadata == {}

    def test_creation_with_metadata(self) -> None:
        """Test DialogueHistory with metadata."""
        history = DialogueHistory(
            session_id="test-123",
            start_time="2025-11-16T10:00:00",
            metadata={"agent_id": "system", "user_id": "user"},
        )

        assert history.metadata == {"agent_id": "system", "user_id": "user"}

    def test_add_turn(self) -> None:
        """Test adding turns to history."""
        history = DialogueHistory(
            session_id="test-123",
            start_time="2025-11-16T10:00:00",
        )

        history.add_turn(
            turn_number=1,
            speaker="user",
            utterance="Hello",
            move_type="greet",
            confidence=0.9,
        )

        assert len(history.turns) == 1
        assert history.turns[0].turn_number == 1
        assert history.turns[0].speaker == "user"
        assert history.turns[0].utterance == "Hello"
        assert history.turns[0].move_type == "greet"
        assert history.turns[0].confidence == 0.9

    def test_add_multiple_turns(self) -> None:
        """Test adding multiple turns."""
        history = DialogueHistory(
            session_id="test-123",
            start_time="2025-11-16T10:00:00",
        )

        history.add_turn(1, "user", "Hello")
        history.add_turn(2, "system", "Hi there")
        history.add_turn(3, "user", "How are you?")

        assert len(history.turns) == 3
        assert history.turns[0].speaker == "user"
        assert history.turns[1].speaker == "system"
        assert history.turns[2].speaker == "user"

    def test_to_dict(self) -> None:
        """Test conversion to dictionary."""
        history = DialogueHistory(
            session_id="test-123",
            start_time="2025-11-16T10:00:00",
            metadata={"agent_id": "system"},
        )

        history.add_turn(1, "user", "Hello", move_type="greet", confidence=0.9)

        data = history.to_dict()

        assert data["session_id"] == "test-123"
        assert data["start_time"] == "2025-11-16T10:00:00"
        assert data["end_time"] is None
        assert len(data["turns"]) == 1
        assert data["turns"][0]["speaker"] == "user"
        assert data["turns"][0]["utterance"] == "Hello"
        assert data["metadata"] == {"agent_id": "system"}

    def test_to_json(self) -> None:
        """Test conversion to JSON string."""
        history = DialogueHistory(
            session_id="test-123",
            start_time="2025-11-16T10:00:00",
        )

        history.add_turn(1, "user", "Hello")

        json_str = history.to_json()
        data = json.loads(json_str)

        assert data["session_id"] == "test-123"
        assert len(data["turns"]) == 1

    def test_save_and_load_file(self) -> None:
        """Test saving and loading from file."""
        history = DialogueHistory(
            session_id="test-123",
            start_time="2025-11-16T10:00:00",
            metadata={"agent_id": "system"},
        )

        history.add_turn(1, "user", "Hello", move_type="greet", confidence=0.9)
        history.add_turn(2, "system", "Hi there", move_type="greet")

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            filename = f.name

        try:
            # Save
            history.save_to_file(filename)

            # Load
            loaded = DialogueHistory.load_from_file(filename)

            assert loaded.session_id == "test-123"
            assert loaded.start_time == "2025-11-16T10:00:00"
            assert len(loaded.turns) == 2
            assert loaded.turns[0].speaker == "user"
            assert loaded.turns[0].utterance == "Hello"
            assert loaded.turns[0].confidence == 0.9
            assert loaded.turns[1].speaker == "system"
            assert loaded.metadata == {"agent_id": "system"}

        finally:
            Path(filename).unlink(missing_ok=True)

    def test_from_dict(self) -> None:
        """Test creation from dictionary."""
        data = {
            "session_id": "test-123",
            "start_time": "2025-11-16T10:00:00",
            "end_time": "2025-11-16T10:05:00",
            "turns": [
                {
                    "turn_number": 1,
                    "timestamp": "2025-11-16T10:00:01",
                    "speaker": "user",
                    "utterance": "Hello",
                    "move_type": "greet",
                    "confidence": 0.9,
                    "grounding_strategy": "optimistic",
                    "state_snapshot": {"qud_depth": 0},
                }
            ],
            "metadata": {"agent_id": "system"},
        }

        history = DialogueHistory.from_dict(data)

        assert history.session_id == "test-123"
        assert history.start_time == "2025-11-16T10:00:00"
        assert history.end_time == "2025-11-16T10:05:00"
        assert len(history.turns) == 1
        assert history.turns[0].speaker == "user"
        assert history.metadata == {"agent_id": "system"}


class TestDialogueVisualizer:
    """Test DialogueVisualizer class."""

    def test_creation(self) -> None:
        """Test visualizer creation."""
        viz = DialogueVisualizer(width=70)
        assert viz.width == 70

    def test_format_turn_basic(self) -> None:
        """Test formatting a basic turn."""
        viz = DialogueVisualizer(width=70)
        turn = TurnRecord(
            turn_number=1,
            timestamp="2025-11-16T10:00:00",
            speaker="user",
            utterance="Hello",
        )

        output = viz.format_turn(turn, show_metadata=False)

        assert "Turn 1 - user" in output
        assert "user: Hello" in output

    def test_format_turn_with_metadata(self) -> None:
        """Test formatting turn with metadata."""
        viz = DialogueVisualizer(width=70)
        turn = TurnRecord(
            turn_number=1,
            timestamp="2025-11-16T10:00:00",
            speaker="user",
            utterance="Hello",
            move_type="greet",
            confidence=0.9,
            grounding_strategy="optimistic",
        )

        output = viz.format_turn(turn, show_metadata=True)

        assert "Turn 1 - user" in output
        assert "user: Hello" in output
        assert "Move: greet" in output
        assert "Confidence: 0.90" in output
        assert "Strategy: optimistic" in output

    def test_format_turn_with_state(self) -> None:
        """Test formatting turn with state snapshot."""
        viz = DialogueVisualizer(width=70)
        turn = TurnRecord(
            turn_number=1,
            timestamp="2025-11-16T10:00:00",
            speaker="user",
            utterance="Hello",
            state_snapshot={"qud_depth": 2, "issues_count": 3},
        )

        output = viz.format_turn(turn, show_metadata=True, show_state=True)

        assert "qud_depth: 2" in output
        assert "issues_count: 3" in output

    def test_format_compact_history(self) -> None:
        """Test compact history formatting."""
        viz = DialogueVisualizer(width=70)
        history = DialogueHistory(
            session_id="test-123",
            start_time="2025-11-16T10:00:00",
        )

        history.add_turn(1, "user", "Hello", confidence=0.9)
        history.add_turn(2, "system", "Hi there")

        output = viz.format_compact_history(history)

        assert "Dialogue History: test-123" in output
        assert "1. [user  ] Hello (conf=0.90)" in output
        assert "2. [system] Hi there" in output

    def test_format_history_detailed(self) -> None:
        """Test detailed history formatting."""
        viz = DialogueVisualizer(width=70)
        history = DialogueHistory(
            session_id="test-123",
            start_time="2025-11-16T10:00:00",
        )

        history.add_turn(1, "user", "Hello")
        history.add_turn(2, "system", "Hi there")

        output = viz.format_history(history, show_metadata=True)

        assert "Dialogue Session: test-123" in output
        assert "Started: 2025-11-16T10:00:00" in output
        assert "Total turns: 2" in output

    def test_format_history_empty(self) -> None:
        """Test formatting empty history."""
        viz = DialogueVisualizer(width=70)
        history = DialogueHistory(
            session_id="test-123",
            start_time="2025-11-16T10:00:00",
        )

        output = viz.format_history(history)

        assert "Dialogue Session: test-123" in output
        assert "Total turns: 0" in output

    def test_format_state_timeline(self) -> None:
        """Test state timeline formatting."""
        viz = DialogueVisualizer(width=70)
        history = DialogueHistory(
            session_id="test-123",
            start_time="2025-11-16T10:00:00",
        )

        history.add_turn(1, "user", "Hello", state_snapshot={"qud_depth": 0})
        history.add_turn(2, "system", "Hi", state_snapshot={"qud_depth": 1})
        history.add_turn(3, "user", "Bye", state_snapshot={"qud_depth": 0})

        output = viz.format_state_timeline(history, "qud_depth")

        assert "State Timeline: qud_depth" in output
        assert "Turn   1: 0" in output
        assert "Turn   2: 1" in output
        assert "Turn   3: 0" in output

    def test_export_to_markdown(self) -> None:
        """Test Markdown export."""
        viz = DialogueVisualizer(width=70)
        history = DialogueHistory(
            session_id="test-123",
            start_time="2025-11-16T10:00:00",
            metadata={"agent_id": "system"},
        )

        history.add_turn(
            1, "user", "Hello", move_type="greet", confidence=0.9, grounding_strategy="optimistic"
        )
        history.add_turn(2, "system", "Hi there", move_type="greet")

        markdown = viz.export_to_markdown(history)

        assert "# Dialogue Session: test-123" in markdown
        assert "**Started:** 2025-11-16T10:00:00" in markdown
        assert "## Session Metadata" in markdown
        assert "**agent_id:** system" in markdown
        assert "## Dialogue" in markdown
        assert "### Turn 1" in markdown
        assert "**user:** Hello" in markdown
        assert "Move Type: `greet`" in markdown
        assert "Confidence: 0.90" in markdown
        assert "Grounding: `optimistic`" in markdown
        assert "### Turn 2" in markdown
        assert "**system:** Hi there" in markdown
        assert "## Summary" in markdown
        assert "Total turns: 2" in markdown

    def test_export_to_csv(self) -> None:
        """Test CSV export."""
        viz = DialogueVisualizer(width=70)
        history = DialogueHistory(
            session_id="test-123",
            start_time="2025-11-16T10:00:00",
        )

        history.add_turn(
            1,
            "user",
            "Hello",
            move_type="greet",
            confidence=0.9,
            grounding_strategy="optimistic",
        )
        history.add_turn(2, "system", "Hi there", move_type="greet")

        csv = viz.export_to_csv(history)

        lines = csv.split("\n")
        assert (
            lines[0] == "turn,timestamp,speaker,utterance,move_type,confidence,grounding_strategy"
        )
        assert "1," in lines[1]
        assert "user" in lines[1]
        assert '"Hello"' in lines[1]
        assert "greet" in lines[1]
        assert "0.90" in lines[1]
        assert "optimistic" in lines[1]

    def test_export_csv_with_quotes(self) -> None:
        """Test CSV export with quotes in utterance."""
        viz = DialogueVisualizer(width=70)
        history = DialogueHistory(
            session_id="test-123",
            start_time="2025-11-16T10:00:00",
        )

        history.add_turn(1, "user", 'He said "hello"')

        csv = viz.export_to_csv(history)

        # Should escape quotes as double quotes
        assert '"He said ""hello"""' in csv

    def test_export_to_markdown_empty(self) -> None:
        """Test Markdown export with empty history."""
        viz = DialogueVisualizer(width=70)
        history = DialogueHistory(
            session_id="test-123",
            start_time="2025-11-16T10:00:00",
        )

        markdown = viz.export_to_markdown(history)

        assert "# Dialogue Session: test-123" in markdown
        assert "Total turns: 0" in markdown

    def test_export_to_csv_empty(self) -> None:
        """Test CSV export with empty history."""
        viz = DialogueVisualizer(width=70)
        history = DialogueHistory(
            session_id="test-123",
            start_time="2025-11-16T10:00:00",
        )

        csv = viz.export_to_csv(history)

        lines = csv.split("\n")
        assert len(lines) == 1  # Only header
        assert (
            lines[0] == "turn,timestamp,speaker,utterance,move_type,confidence,grounding_strategy"
        )
