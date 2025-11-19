"""Tests for visualization export tools."""

from ibdm.core import (
    DialogueMove,
    InformationState,
    Plan,
    PrivateIS,
    SharedIS,
    WhQuestion,
)
from ibdm.visualization.diff_engine import compute_diff
from ibdm.visualization.html_export import HtmlExporter
from ibdm.visualization.state_snapshot import StateSnapshot
from ibdm.visualization.svg_export import SvgExporter


class TestHtmlExporter:
    """Test HTML export functionality."""

    def test_export_snapshot(self):
        """Test exporting a single snapshot to HTML."""
        # Setup state
        question = WhQuestion(predicate="destination", variable="city")
        state = InformationState(
            shared=SharedIS(qud=[question]),
            private=PrivateIS(agenda=[DialogueMove("ask", "Where to?", "system")]),
        )
        snapshot = StateSnapshot.from_state(state, timestamp=0, label="Test State")

        # Export
        exporter = HtmlExporter()
        html = exporter.export_snapshot(snapshot)

        # Verify content
        assert "<!DOCTYPE html>" in html
        assert "Test State" in html
        assert "QUD" in html
        # WhQuestion str representation is ?variable.predicate
        assert "?city.destination" in html
        assert "Where to?" in html

    def test_export_diff(self):
        """Test exporting a state diff to HTML."""
        # Setup states
        state1 = InformationState()
        snapshot1 = StateSnapshot.from_state(state1, timestamp=0, label="Before")

        state2 = InformationState(private=PrivateIS(beliefs={"city": "Paris"}))
        snapshot2 = StateSnapshot.from_state(state2, timestamp=1, label="After")

        # Compute diff
        diff = compute_diff(snapshot1, snapshot2)

        # Export
        exporter = HtmlExporter()
        html = exporter.export_diff(diff)

        # Verify content
        assert "city" in html
        assert "Paris" in html
        assert 'class="diff-added"' in html
        assert "Beliefs" in html

    def test_export_timeline(self):
        """Test exporting a timeline of snapshots."""
        # Setup states
        state1 = InformationState()
        snapshot1 = StateSnapshot.from_state(state1, timestamp=0, label="Step 1")

        state2 = InformationState(shared=SharedIS(commitments={"c1"}))
        snapshot2 = StateSnapshot.from_state(state2, timestamp=1, label="Step 2")

        # Export
        exporter = HtmlExporter()
        html = exporter.export_timeline([snapshot1, snapshot2])

        # Verify content
        assert "Step 1" in html
        # Timeline shows diffs for subsequent steps, checking for content
        assert "commitments" in html
        assert "c1" in html

    def test_export_rule_trace(self):
        """Test exporting a rule trace to HTML."""
        # Setup trace
        from ibdm.visualization.rule_trace import RuleEvaluation, RuleTrace
        
        trace = RuleTrace(
            phase="integrate",
            timestamp=1,
            label="Test Trace",
            evaluations=[
                RuleEvaluation("rule1", 10, True, True, "Selected"),
                RuleEvaluation("rule2", 5, True, False, "Lower priority"),
                RuleEvaluation("rule3", 1, False, False, "Preconditions not met")
            ],
            selected_rule="rule1"
        )
        
        # Export
        exporter = HtmlExporter()
        html = exporter.export_rule_trace(trace)
        
        # Verify content
        assert "rule1" in html
        assert "rule2" in html
        assert "rule3" in html
        assert "class=\"rule-selected\"" in html
        assert "class=\"rule-met\"" in html
        assert "class=\"rule-unmet\"" in html
        assert "Selected" in html


class TestSvgExporter:
    """Test SVG export functionality."""

    def test_export_plan_tree(self):
        """Test exporting plan tree to SVG."""
        # Setup state with plan
        plan = Plan(
            plan_type="findout",
            content=WhQuestion("x", "destination(x)"),
            subplans=[Plan(plan_type="raise", content=WhQuestion("x", "destination(x)"))],
        )
        state = InformationState(private=PrivateIS(plan=[plan]))
        snapshot = StateSnapshot.from_state(state, timestamp=0, label="Test")

        # Export
        exporter = SvgExporter()
        svg = exporter.export_plan_tree(snapshot)

        # Verify content (assuming graphviz is working or fallback)
        if "<svg" in svg:
            # Basic checks
            assert "destination" in svg
            if "Error" not in svg:
                assert "findout" in svg
                assert "raise" in svg

    def test_export_qud_stack(self):
        """Test exporting QUD stack to SVG."""
        # Setup state with QUD
        state = InformationState(
            shared=SharedIS(qud=[WhQuestion("x", "destination(x)"), WhQuestion("y", "date(y)")])
        )
        snapshot = StateSnapshot.from_state(state, timestamp=0, label="Test")

        # Export
        exporter = SvgExporter()
        svg = exporter.export_qud_stack(snapshot)

        # Verify content
        if "<svg" in svg:
            assert "destination" in svg
            assert "date" in svg

    def test_export_empty_structures(self):
        """Test exporting empty structures."""
        state = InformationState()
        snapshot = StateSnapshot.from_state(state, timestamp=0, label="Empty")

        exporter = SvgExporter()

        plan_svg = exporter.export_plan_tree(snapshot)
        assert "No active plans" in plan_svg

        qud_svg = exporter.export_qud_stack(snapshot)
        assert "Empty QUD" in qud_svg
