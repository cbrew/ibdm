"""Demo script for HTML export."""

from ibdm.core import (
    DialogueMove,
    InformationState,
    Plan,
    PrivateIS,
    SharedIS,
    WhQuestion,
)
from ibdm.visualization.diff_engine import DiffEngine
from ibdm.visualization.html_export import HtmlExporter
from ibdm.visualization.state_snapshot import StateSnapshot
from ibdm.visualization.svg_export import SvgExporter


def create_dummy_state(timestamp: int, label: str) -> StateSnapshot:
    """Create a dummy state snapshot."""
    shared = SharedIS(
        qud=[WhQuestion("x", "name(x)")], commitments=["greeted"], moves=[], next_moves=[]
    )
    private = PrivateIS(
        plan=[Plan("findout", WhQuestion("x", "name(x)"), subplans=[])],
        agenda=[DialogueMove("ask", "What is your name?", "system")],
        beliefs={"name": None},
        issues=[],
        overridden_questions=[],
        actions=[],
        last_utterance=DialogueMove("greet", "Hello", "system"),
    )
    state = InformationState(private=private, shared=shared)

    # Modify state based on timestamp to create diffs
    if timestamp > 0:
        state.shared.qud.append(WhQuestion("x", "age(x)"))
        state.private.beliefs["name"] = "Alice"
        state.private.agenda = []
        # Add a subplan to show hierarchy
        plan = Plan(
            "findout",
            WhQuestion("x", "age(x)"),
            subplans=[Plan("raise", WhQuestion("x", "age(x)"))],
        )
        state.private.plan.insert(0, plan)

    return StateSnapshot.from_state(state, timestamp, label)


def main():
    """Run demo export."""
    print("Creating states...")
    state1 = create_dummy_state(0, "Initial State")
    state2 = create_dummy_state(1, "After User Input")

    exporter = HtmlExporter()
    svg_exporter = SvgExporter()

    # Export Snapshot with SVG
    print("Exporting snapshot...")
    html_content = exporter._render_snapshot(state2)

    # Generate SVGs
    plan_svg = svg_exporter.export_plan_tree(state2)
    qud_svg = svg_exporter.export_qud_stack(state2)

    # Inject SVGs (hacky but demonstrates integration)
    html_with_svg = f"""
    {html_content}
    <div class="section">
        <h3>Visualizations</h3>
        <h4>Plan Tree</h4>
        {plan_svg}
        <h4>QUD Stack</h4>
        {qud_svg}
    </div>
    """

    final_html = exporter._wrap_page(html_with_svg, "State Snapshot with Visualization")

    with open("report_snapshot.html", "w") as f:
        f.write(final_html)
    print("Written report_snapshot.html")

    # Export Diff
    print("Exporting diff...")
    engine = DiffEngine()
    diff = engine.compute_diff(state1, state2)
    html_diff = exporter.export_diff(diff)
    with open("report_diff.html", "w") as f:
        f.write(html_diff)
    print("Written report_diff.html")

    # Export Timeline
    print("Exporting timeline...")
    html_timeline = exporter.export_timeline([state1, state2])
    with open("report_timeline.html", "w") as f:
        f.write(html_timeline)
    print("Written report_timeline.html")


if __name__ == "__main__":
    main()
