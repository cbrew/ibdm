"""Demo script for Terminal Visualizer."""

from ibdm.core import DialogueMove, InformationState, Plan, PrivateIS, SharedIS, WhQuestion
from ibdm.visualization.diff_engine import compute_diff
from ibdm.visualization.state_snapshot import StateSnapshot
from ibdm.visualization.terminal import TerminalVisualizer


def create_dummy_state(timestamp: int, label: str) -> StateSnapshot:
    """Create a dummy state snapshot."""
    shared = SharedIS(
        qud=[WhQuestion("x", "name(x)")],
        commitments=["greeted"],
        moves=[],
        next_moves=[],
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
    """Run demo terminal visualization."""
    print("Creating states...")
    state1 = create_dummy_state(0, "Initial State")
    state2 = create_dummy_state(1, "After User Input")

    visualizer = TerminalVisualizer()

    print("\n--- Snapshot Visualization ---")
    visualizer.render_snapshot(state1)

    print("\n--- Diff Visualization ---")
    diff = compute_diff(state1, state2)
    visualizer.render_diff(diff)


if __name__ == "__main__":
    main()
