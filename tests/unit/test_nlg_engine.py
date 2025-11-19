"""Unit tests for NLG engine dialogue history functionality."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Add src to path to avoid circular imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from ibdm.core.answers import Answer
from ibdm.core.information_state import InformationState, PrivateIS, SharedIS
from ibdm.core.moves import DialogueMove
from ibdm.core.plans import Plan
from ibdm.core.questions import Question, WhQuestion, YNQuestion

# Import NLG engine directly to avoid circular import through __init__.py
from ibdm.nlg.nlg_engine import NLGEngine, NLGEngineConfig


class TestDialogueHistoryFormatting:
    """Test dialogue history formatting for NLG prompts."""

    @pytest.fixture
    def engine(self):
        """Create NLG engine for testing."""
        config = NLGEngineConfig(default_strategy="template")
        return NLGEngine(config)

    @pytest.fixture
    def empty_state(self):
        """Create empty information state."""
        return InformationState(private=PrivateIS(), shared=SharedIS())

    def test_format_dialogue_history_empty(self, engine):
        """Test formatting empty dialogue history."""
        moves = []
        result = engine._format_dialogue_history(moves)
        assert result == "(no prior dialogue)"

    def test_format_dialogue_history_single_move(self, engine):
        """Test formatting single move."""
        move = DialogueMove(move_type="greet", content="Hello", speaker="user")
        moves = [move]

        result = engine._format_dialogue_history(moves)

        # Should include speaker, move type, and content
        assert "User:" in result
        assert "greet" in result
        assert "Hello" in result
        assert "1." in result  # Should be numbered

    def test_format_dialogue_history_multiple_moves(self, engine):
        """Test formatting multiple moves."""
        moves = [
            DialogueMove(move_type="greet", content="Hello", speaker="user"),
            DialogueMove(move_type="greet", content="Hi there!", speaker="system"),
            DialogueMove(
                move_type="ask",
                content=WhQuestion(variable="x", predicate="name"),
                speaker="system",
            ),
        ]

        result = engine._format_dialogue_history(moves)

        # Should include all moves numbered
        assert "1. User: greet" in result
        assert "2. System: greet" in result
        assert "3. System: ask" in result

    def test_format_dialogue_history_max_moves_limit(self, engine):
        """Test that dialogue history respects max_moves limit."""
        # Create 15 moves
        moves = [
            DialogueMove(move_type="greet", content=f"Message {i}", speaker="user")
            for i in range(15)
        ]

        # Request only last 5
        result = engine._format_dialogue_history(moves, max_moves=5)

        # Should only include last 5 moves (numbered 1-5 in output)
        lines = result.strip().split("\n")
        assert len(lines) == 5
        assert "1. User: greet - Message 10" in result  # 11th move is first shown
        assert "5. User: greet - Message 14" in result  # 15th move is last shown

    def test_format_dialogue_history_with_grounding_status(self, engine):
        """Test that grounding status is included when available."""
        move = DialogueMove(
            move_type="answer",
            content="Paris",
            speaker="user",
            metadata={"grounding_status": "perceived"},
        )
        moves = [move]

        result = engine._format_dialogue_history(moves)

        # Should include grounding status
        assert "[perceived]" in result

    def test_format_dialogue_history_no_grounding_for_grounded(self, engine):
        """Test that 'grounded' status is not shown (noise reduction)."""
        move = DialogueMove(
            move_type="answer",
            content="Paris",
            speaker="user",
            metadata={"grounding_status": "grounded"},
        )
        moves = [move]

        result = engine._format_dialogue_history(moves)

        # Should NOT include grounding status for fully grounded
        assert "[grounded]" not in result

    def test_format_move_content_whquestion(self, engine):
        """Test formatting WhQuestion content."""
        question = WhQuestion(variable="x", predicate="city")
        result = engine._format_move_content_for_history(question)
        assert "city" in result

    def test_format_move_content_ynquestion(self, engine):
        """Test formatting YNQuestion content."""
        question = YNQuestion(proposition="user_confirmed")
        result = engine._format_move_content_for_history(question)
        assert "user_confirmed" in result

    def test_format_move_content_answer(self, engine):
        """Test formatting Answer content."""
        answer = Answer(content="Paris")
        result = engine._format_move_content_for_history(answer)
        assert result == "Paris"

    def test_format_move_content_string(self, engine):
        """Test formatting string content."""
        result = engine._format_move_content_for_history("Hello there")
        assert result == "Hello there"

    def test_format_move_content_long_string_truncation(self, engine):
        """Test that long strings are truncated."""
        long_string = "x" * 100
        result = engine._format_move_content_for_history(long_string)
        assert len(result) <= 80
        assert result.endswith("...")


class TestDialogueHistoryInPrompts:
    """Test dialogue history inclusion in NLG prompts."""

    @pytest.fixture
    def engine(self):
        """Create NLG engine for testing."""
        config = NLGEngineConfig(default_strategy="template")
        return NLGEngine(config)

    def test_system_prompt_includes_dialogue_history(self, engine):
        """Test that system prompt includes dialogue history."""
        # Create state with dialogue history
        moves = [
            DialogueMove(move_type="greet", content="Hello", speaker="user"),
            DialogueMove(move_type="greet", content="Hi!", speaker="system"),
        ]
        state = InformationState(
            private=PrivateIS(),
            shared=SharedIS(moves=moves),
        )

        # Create a move to generate
        move = DialogueMove(
            move_type="ask", content=WhQuestion(variable="x", predicate="name"), speaker="system"
        )

        # Build prompt
        prompt = engine._build_nlg_system_prompt(move, state)

        # Should include dialogue history section
        assert "Dialogue history:" in prompt
        assert "User: greet" in prompt
        assert "System: greet" in prompt

    def test_system_prompt_without_dialogue_history(self, engine):
        """Test system prompt when there's no dialogue history."""
        # Create state without dialogue history
        state = InformationState(
            private=PrivateIS(),
            shared=SharedIS(moves=[]),
        )

        move = DialogueMove(move_type="greet", content="Hello", speaker="system")

        # Build prompt
        prompt = engine._build_nlg_system_prompt(move, state)

        # Should NOT include dialogue history section
        assert "Dialogue history:" not in prompt

    def test_system_prompt_includes_all_context(self, engine):
        """Test that system prompt includes dialogue history + QUD + plans."""
        # Create comprehensive state
        moves = [
            DialogueMove(move_type="greet", content="Hello", speaker="user"),
        ]
        qud_question: Question = WhQuestion(variable="x", predicate="city")
        qud = [qud_question]
        plan = Plan(plan_type="nda_drafting", content="nda_info", status="active")

        state = InformationState(
            private=PrivateIS(plan=[plan]),
            shared=SharedIS(moves=moves, qud=qud),
        )

        move = DialogueMove(
            move_type="ask", content=WhQuestion(variable="y", predicate="date"), speaker="system"
        )

        # Build prompt
        prompt = engine._build_nlg_system_prompt(move, state)

        # Should include all context
        assert "Dialogue history:" in prompt
        assert "Current questions under discussion:" in prompt
        assert "Active plans:" in prompt
        assert "nda_drafting" in prompt
