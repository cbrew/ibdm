"""Tests for visualization data model and diff engine."""

from ibdm.core import (
    InformationState,
    Plan,
    PrivateIS,
    SharedIS,
    WhQuestion,
)
from ibdm.visualization import (
    ChangeType,
    RuleTrace,
    StateSnapshot,
    compute_diff,
)
from ibdm.visualization.rule_trace import RuleEvaluation


class TestStateSnapshot:
    """Test StateSnapshot creation and field access."""

    def test_snapshot_from_state(self):
        """Test creating snapshot from InformationState."""
        # Create a state with some content
        question = WhQuestion(predicate="destination", variable="city")
        state = InformationState(
            private=PrivateIS(issues=[question]),
            shared=SharedIS(qud=[question]),
            agent_id="system",
        )

        # Create snapshot
        snapshot = StateSnapshot.from_state(state, timestamp=0, label="Initial state")

        # Verify snapshot captured state correctly
        assert snapshot.timestamp == 0
        assert snapshot.label == "Initial state"
        assert len(snapshot.qud) == 1
        assert snapshot.qud[0] == question
        assert len(snapshot.issues) == 1
        assert snapshot.issues[0] == question
        assert snapshot.agent_id == "system"

    def test_snapshot_immutability(self):
        """Test that snapshots are immutable (frozen dataclass)."""
        state = InformationState()
        snapshot = StateSnapshot.from_state(state, timestamp=0, label="Test")

        # Should not be able to modify snapshot
        try:
            snapshot.timestamp = 1  # type: ignore
            assert False, "Should not be able to modify frozen snapshot"
        except AttributeError:
            pass  # Expected

    def test_snapshot_field_value(self):
        """Test field_value accessor."""
        question = WhQuestion(predicate="destination", variable="city")
        state = InformationState(shared=SharedIS(qud=[question]))
        snapshot = StateSnapshot.from_state(state, timestamp=0, label="Test")

        # Access field by name
        qud = snapshot.field_value("qud")
        assert len(qud) == 1
        assert qud[0] == question


class TestDiffEngine:
    """Test diff engine for state comparison."""

    def test_diff_no_changes(self):
        """Test diff when states are identical."""
        state = InformationState()
        snapshot1 = StateSnapshot.from_state(state, timestamp=0, label="Before")
        snapshot2 = StateSnapshot.from_state(state, timestamp=1, label="After")

        diff = compute_diff(snapshot1, snapshot2)

        assert not diff.has_changes()
        assert diff.total_change_count() == 0
        assert diff.changed_field_names() == []

    def test_diff_qud_added(self):
        """Test diff when question is added to QUD."""
        state1 = InformationState()
        snapshot1 = StateSnapshot.from_state(state1, timestamp=0, label="Before")

        # Add question to QUD
        question = WhQuestion(predicate="destination", variable="city")
        state2 = InformationState(shared=SharedIS(qud=[question]))
        snapshot2 = StateSnapshot.from_state(state2, timestamp=1, label="After")

        diff = compute_diff(snapshot1, snapshot2)

        assert diff.has_changes()
        assert "qud" in diff.changed_field_names()

        qud_change = diff.get_changed_field("qud")
        assert qud_change is not None
        assert qud_change.change_type == ChangeType.ADDED
        assert len(qud_change.added_items) == 1
        assert len(qud_change.removed_items) == 0

    def test_diff_qud_removed(self):
        """Test diff when question is removed from QUD."""
        question = WhQuestion(predicate="destination", variable="city")
        state1 = InformationState(shared=SharedIS(qud=[question]))
        snapshot1 = StateSnapshot.from_state(state1, timestamp=0, label="Before")

        state2 = InformationState()
        snapshot2 = StateSnapshot.from_state(state2, timestamp=1, label="After")

        diff = compute_diff(snapshot1, snapshot2)

        assert diff.has_changes()
        qud_change = diff.get_changed_field("qud")
        assert qud_change is not None
        assert qud_change.change_type == ChangeType.REMOVED
        assert len(qud_change.added_items) == 0
        assert len(qud_change.removed_items) == 1

    def test_diff_beliefs_modified(self):
        """Test diff when beliefs dict is modified."""
        state1 = InformationState(private=PrivateIS(beliefs={"destination": "Paris"}))
        snapshot1 = StateSnapshot.from_state(state1, timestamp=0, label="Before")

        state2 = InformationState(
            private=PrivateIS(beliefs={"destination": "London", "date": "2024-01-15"})
        )
        snapshot2 = StateSnapshot.from_state(state2, timestamp=1, label="After")

        diff = compute_diff(snapshot1, snapshot2)

        assert diff.has_changes()
        beliefs_change = diff.get_changed_field("beliefs")
        assert beliefs_change is not None
        # Has both added items and modified items, so overall state changes
        assert beliefs_change.has_changes()
        # Modified: destination changed from Paris to London
        # Added: date=2024-01-15
        assert len(beliefs_change.modified_items) == 1
        assert len(beliefs_change.added_items) == 1

    def test_diff_plan_added(self):
        """Test diff when plan is added."""
        state1 = InformationState()
        snapshot1 = StateSnapshot.from_state(state1, timestamp=0, label="Before")

        plan = Plan(plan_type="findout", content="test")
        state2 = InformationState(private=PrivateIS(plan=[plan]))
        snapshot2 = StateSnapshot.from_state(state2, timestamp=1, label="After")

        diff = compute_diff(snapshot1, snapshot2)

        assert diff.has_changes()
        plan_change = diff.get_changed_field("plan")
        assert plan_change is not None
        assert plan_change.change_type == ChangeType.ADDED
        assert len(plan_change.added_items) == 1

    def test_diff_summary(self):
        """Test summary generation for diffs."""
        # Create state with question on QUD
        question = WhQuestion(predicate="destination", variable="city")
        state1 = InformationState()
        snapshot1 = StateSnapshot.from_state(state1, timestamp=0, label="Before")

        state2 = InformationState(shared=SharedIS(qud=[question]))
        snapshot2 = StateSnapshot.from_state(state2, timestamp=1, label="After")

        diff = compute_diff(snapshot1, snapshot2)

        summary = diff.format_summary()
        assert "qud" in summary
        assert "+1" in summary


class TestRuleTrace:
    """Test rule execution trace."""

    def test_rule_trace_creation(self):
        """Test creating a rule trace."""
        trace = RuleTrace(
            phase="integrate",
            timestamp=1,
            label="After integration",
        )

        assert trace.phase == "integrate"
        assert trace.timestamp == 1
        assert trace.rules_evaluated() == 0

    def test_rule_evaluation_tracking(self):
        """Test tracking rule evaluations."""
        trace = RuleTrace(
            phase="integrate",
            timestamp=1,
            label="Test",
            selected_rule="accommodate_skip_question",
        )

        # Add rule evaluations
        trace.evaluations.append(
            RuleEvaluation(
                rule_name="accommodate_skip_question",
                priority=9,
                preconditions_met=True,
                was_selected=True,
                reason="User requested skip",
            )
        )
        trace.evaluations.append(
            RuleEvaluation(
                rule_name="integrate_answer",
                priority=8,
                preconditions_met=False,
                was_selected=False,
                reason="No answer move",
            )
        )

        assert trace.rules_evaluated() == 2
        assert trace.rules_with_met_preconditions() == 1
        assert trace.selected_rule == "accommodate_skip_question"

        selected = trace.get_selected_evaluation()
        assert selected is not None
        assert selected.rule_name == "accommodate_skip_question"

    def test_rule_trace_with_diff(self):
        """Test rule trace with before/after states and diff."""
        state1 = InformationState()
        snapshot1 = StateSnapshot.from_state(state1, timestamp=0, label="Before")

        question = WhQuestion(predicate="destination", variable="city")
        state2 = InformationState(shared=SharedIS(qud=[question]))
        snapshot2 = StateSnapshot.from_state(state2, timestamp=1, label="After")

        diff = compute_diff(snapshot1, snapshot2)

        trace = RuleTrace(
            phase="integrate",
            timestamp=1,
            label="After rule execution",
            state_before=snapshot1,
            state_after=snapshot2,
            diff=diff,
        )

        assert trace.diff is not None
        assert trace.diff.has_changes()
        assert "qud" in trace.diff.changed_field_names()


class TestVisualizationIntegration:
    """Test integration of visualization components."""

    def test_full_workflow(self):
        """Test complete workflow: state → snapshot → diff → trace."""
        # 1. Create initial state
        state1 = InformationState()
        snapshot1 = StateSnapshot.from_state(state1, timestamp=0, label="Turn 1: Start")

        # 2. Modify state (add question to QUD)
        question = WhQuestion(predicate="destination", variable="city")
        state2 = InformationState(shared=SharedIS(qud=[question]))
        snapshot2 = StateSnapshot.from_state(state2, timestamp=1, label="Turn 1: After integrate")

        # 3. Compute diff
        diff = compute_diff(snapshot1, snapshot2)
        assert diff.has_changes()

        # 4. Create rule trace
        trace = RuleTrace(
            phase="integrate",
            timestamp=1,
            label="Integration complete",
            evaluations=[
                RuleEvaluation(
                    rule_name="integrate_question",
                    priority=7,
                    preconditions_met=True,
                    was_selected=True,
                )
            ],
            selected_rule="integrate_question",
            state_before=snapshot1,
            state_after=snapshot2,
            diff=diff,
        )

        # 5. Verify trace has complete information
        assert trace.diff is not None
        assert trace.diff.total_change_count() == 1
        assert trace.rules_evaluated() == 1
        assert trace.selected_rule == "integrate_question"

        summary = trace.format_summary()
        assert "integrate" in summary
        assert "integrate_question" in summary
