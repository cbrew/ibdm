"""Tests for terminal renderer."""

import pytest
from rich.console import Console

from ibdm.core import DialogueMove, InformationState, Plan, PrivateIS, SharedIS, WhQuestion
from ibdm.visualization import (
    ChangeType,
    RuleTrace,
    StateSnapshot,
    TerminalRenderer,
    compute_diff,
)
from ibdm.visualization.rule_trace import RuleEvaluation


class TestTerminalRenderer:
    """Test Rich-based terminal renderer."""

    @pytest.fixture
    def renderer(self):
        """Create renderer for testing."""
        # Use record=True to capture output for assertions
        console = Console(record=True, width=120)
        return TerminalRenderer(console=console)

    @pytest.fixture
    def sample_state(self):
        """Create a sample information state."""
        question = WhQuestion(predicate="destination", variable="city")
        return InformationState(
            private=PrivateIS(
                issues=[question],
                beliefs={"destination": "Paris", "date": "2025-01-15"},
                agenda=[DialogueMove(move_type="ask", content=question, speaker="system")],
                plan=[Plan(plan_type="findout", content=question)],
            ),
            shared=SharedIS(
                qud=[question],
                commitments={"destination: Paris"},
                last_moves=[DialogueMove(move_type="answer", content="Paris", speaker="user")],
            ),
            agent_id="system",
        )

    def test_render_state(self, renderer, sample_state):
        """Test rendering information state."""
        panel = renderer.render_state(sample_state, title="Test State")
        assert panel is not None
        assert "Test State" in panel.title

    def test_print_state(self, renderer, sample_state):
        """Test printing state to console."""
        renderer.print_state(sample_state, title="Test State")
        
        # Verify output was generated
        output = renderer.console.export_text()
        assert "Test State" in output
        assert "Shared State" in output
        assert "Private State" in output
        assert "Control" in output

    def test_render_state_shows_qud(self, renderer, sample_state):
        """Test that QUD is rendered."""
        renderer.print_state(sample_state)
        output = renderer.console.export_text()
        assert "QUD" in output
        # Question should be visible
        assert "destination" in output or "city" in output

    def test_render_state_shows_beliefs(self, renderer, sample_state):
        """Test that beliefs are rendered."""
        renderer.print_state(sample_state)
        output = renderer.console.export_text()
        assert "Beliefs" in output
        assert "beliefs" in output  # Count or content

    def test_render_empty_state(self, renderer):
        """Test rendering empty state."""
        empty_state = InformationState()
        panel = renderer.render_state(empty_state)
        assert panel is not None

    def test_render_diff_no_changes(self, renderer):
        """Test rendering diff with no changes."""
        state = InformationState()
        snapshot1 = StateSnapshot.from_state(state, timestamp=0, label="Before")
        snapshot2 = StateSnapshot.from_state(state, timestamp=1, label="After")
        diff = compute_diff(snapshot1, snapshot2)
        
        panel = renderer.render_diff(diff)
        assert panel is not None
        
        renderer.print_diff(diff)
        output = renderer.console.export_text()
        assert "No changes" in output

    def test_render_diff_with_changes(self, renderer):
        """Test rendering diff with changes."""
        # Before state
        state1 = InformationState()
        snapshot1 = StateSnapshot.from_state(state1, timestamp=0, label="Before")
        
        # After state (add question to QUD)
        question = WhQuestion(predicate="destination", variable="city")
        state2 = InformationState(shared=SharedIS(qud=[question]))
        snapshot2 = StateSnapshot.from_state(state2, timestamp=1, label="After")
        
        diff = compute_diff(snapshot1, snapshot2)
        
        renderer.print_diff(diff, title="Test Diff")
        output = renderer.console.export_text()
        
        assert "Test Diff" in output
        assert "qud" in output
        assert "ADDED" in output or "changes" in output

    def test_render_diff_shows_change_types(self, renderer):
        """Test that different change types are displayed."""
        # Create state with question
        question = WhQuestion(predicate="destination", variable="city")
        state1 = InformationState(shared=SharedIS(qud=[question]))
        snapshot1 = StateSnapshot.from_state(state1, timestamp=0, label="Before")
        
        # Remove question
        state2 = InformationState()
        snapshot2 = StateSnapshot.from_state(state2, timestamp=1, label="After")
        
        diff = compute_diff(snapshot1, snapshot2)
        
        renderer.print_diff(diff)
        output = renderer.console.export_text()
        
        # Should show removal
        assert "REMOVED" in output or "-" in output

    def test_render_rule_trace_basic(self, renderer):
        """Test rendering basic rule trace."""
        trace = RuleTrace(
            phase="integrate",
            timestamp=1,
            label="Test Trace",
            selected_rule="integrate_answer",
        )
        
        panel = renderer.render_rule_trace(trace)
        assert panel is not None
        assert "integrate" in panel.title or "Rule" in panel.title

    def test_render_rule_trace_with_evaluations(self, renderer):
        """Test rendering rule trace with evaluations."""
        trace = RuleTrace(
            phase="integrate",
            timestamp=1,
            label="Test Trace",
            selected_rule="integrate_answer",
            evaluations=[
                RuleEvaluation(
                    rule_name="integrate_answer",
                    priority=10,
                    preconditions_met=True,
                    was_selected=True,
                    reason="User provided answer",
                ),
                RuleEvaluation(
                    rule_name="integrate_question",
                    priority=9,
                    preconditions_met=False,
                    was_selected=False,
                    reason="No question in move",
                ),
            ],
        )
        
        renderer.print_rule_trace(trace)
        output = renderer.console.export_text()
        
        assert "integrate_answer" in output
        assert "integrate_question" in output
        # Should show checkmarks or crosses for preconditions
        assert "✓" in output or "✗" in output

    def test_render_rule_trace_with_diff(self, renderer):
        """Test rendering rule trace with state diff."""
        # Create before/after states
        state1 = InformationState()
        snapshot1 = StateSnapshot.from_state(state1, timestamp=0, label="Before")
        
        question = WhQuestion(predicate="destination", variable="city")
        state2 = InformationState(shared=SharedIS(qud=[question]))
        snapshot2 = StateSnapshot.from_state(state2, timestamp=1, label="After")
        
        diff = compute_diff(snapshot1, snapshot2)
        
        trace = RuleTrace(
            phase="integrate",
            timestamp=1,
            label="After rule",
            state_before=snapshot1,
            state_after=snapshot2,
            diff=diff,
            selected_rule="integrate_question",
        )
        
        renderer.print_rule_trace(trace)
        output = renderer.console.export_text()
        
        assert "State Changes" in output or "changes" in output

    def test_console_width_respected(self):
        """Test that console width is respected."""
        console = Console(record=True, width=80)
        renderer = TerminalRenderer(console=console, width=80)
        
        state = InformationState()
        renderer.print_state(state)
        
        # Just verify it doesn't crash with narrower width
        output = renderer.console.export_text()
        assert output is not None

    def test_format_question_list(self, renderer):
        """Test formatting question list."""
        questions = [
            WhQuestion(predicate="destination", variable="city"),
            WhQuestion(predicate="date", variable="when"),
        ]
        
        text = renderer._format_question_list(questions)
        assert text is not None
        assert len(text) > 0

    def test_format_move_list(self, renderer):
        """Test formatting move list."""
        moves = [
            DialogueMove(move_type="ask", content="Where?", speaker="system"),
            DialogueMove(move_type="answer", content="Paris", speaker="user"),
        ]
        
        text = renderer._format_move_list(moves)
        assert text is not None

    def test_format_plan_list(self, renderer):
        """Test formatting plan list."""
        plans = [
            Plan(plan_type="findout", content="destination"),
            Plan(plan_type="inform", content="result"),
        ]
        
        text = renderer._format_plan_list(plans)
        assert text is not None


class TestTerminalRendererIntegration:
    """Integration tests for terminal renderer."""

    def test_full_workflow_visualization(self):
        """Test complete workflow from state creation to visualization."""
        console = Console(record=True, width=120)
        renderer = TerminalRenderer(console=console)
        
        # Create initial state
        question = WhQuestion(predicate="destination", variable="city")
        state = InformationState(
            shared=SharedIS(qud=[question]),
            private=PrivateIS(beliefs={"user_intent": "travel_planning"}),
        )
        
        # Render state
        renderer.print_state(state, title="Travel Planning State")
        
        # Create snapshots and diff
        snapshot1 = StateSnapshot.from_state(state, timestamp=0, label="Initial")
        
        # Modify state (add commitment)
        state.shared.commitments.add("destination: Paris")
        snapshot2 = StateSnapshot.from_state(state, timestamp=1, label="After answer")
        
        diff = compute_diff(snapshot1, snapshot2)
        
        # Render diff
        renderer.print_diff(diff, title="User Answered")
        
        # Create and render rule trace
        trace = RuleTrace(
            phase="integrate",
            timestamp=1,
            label="After integrate_answer",
            selected_rule="integrate_answer",
            state_before=snapshot1,
            state_after=snapshot2,
            diff=diff,
            evaluations=[
                RuleEvaluation(
                    rule_name="integrate_answer",
                    priority=10,
                    preconditions_met=True,
                    was_selected=True,
                    reason="Answer resolves top QUD",
                )
            ],
        )
        
        renderer.print_rule_trace(trace, title="Integration Phase")
        
        # Verify all outputs were generated
        output = renderer.console.export_text()
        assert "Travel Planning State" in output
        assert "User Answered" in output
        assert "Integration Phase" in output


class TestChangeFormatting:
    """Test change formatting helpers."""

    @pytest.fixture
    def renderer(self):
        """Create renderer for testing."""
        return TerminalRenderer()

    def test_format_change_added(self, renderer):
        """Test formatting ADDED change."""
        from ibdm.visualization.state_diff import ChangedField
        
        changed = ChangedField(
            field_name="test",
            change_type=ChangeType.ADDED,
            added_items=["item1"],
        )
        
        text = renderer._format_change(changed)
        assert "+ ADDED" in str(text) or "ADDED" in str(text)

    def test_format_change_removed(self, renderer):
        """Test formatting REMOVED change."""
        from ibdm.visualization.state_diff import ChangedField
        
        changed = ChangedField(
            field_name="test",
            change_type=ChangeType.REMOVED,
            removed_items=["item1"],
        )
        
        text = renderer._format_change(changed)
        assert "- REMOVED" in str(text) or "REMOVED" in str(text)

    def test_format_change_modified(self, renderer):
        """Test formatting MODIFIED change."""
        from ibdm.visualization.state_diff import ChangedField
        
        changed = ChangedField(
            field_name="test",
            change_type=ChangeType.MODIFIED,
            modified_items=[("old", "new")],
        )
        
        text = renderer._format_change(changed)
        assert "~ MODIFIED" in str(text) or "MODIFIED" in str(text)
