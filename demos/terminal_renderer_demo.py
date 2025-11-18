"""Demo script for terminal state renderer.

Shows the terminal renderer in action with sample dialogue states,
diffs, and rule traces.
"""

from rich.console import Console

from ibdm.core import DialogueMove, InformationState, Plan, PrivateIS, SharedIS, WhQuestion
from ibdm.visualization import RuleTrace, StateSnapshot, TerminalRenderer, compute_diff
from ibdm.visualization.rule_trace import RuleEvaluation


def main():
    """Run terminal renderer demo."""
    console = Console()
    renderer = TerminalRenderer(console=console)
    
    console.print("\n[bold cyan]═══ IBDM Terminal State Renderer Demo ═══[/bold cyan]\n")
    
    # Demo 1: Simple information state
    console.print("\n[bold]Demo 1: Information State Visualization[/bold]\n")
    
    question = WhQuestion(predicate="destination", variable="city")
    state = InformationState(
        shared=SharedIS(
            qud=[question],
            commitments={"travel_intent: booking"},
            last_moves=[
                DialogueMove(move_type="greet", content="Hello", speaker="user"),
                DialogueMove(move_type="greet", content="Hi! How can I help?", speaker="system"),
            ],
        ),
        private=PrivateIS(
            beliefs={"destination": "Paris", "user_intent": "travel_planning"},
            agenda=[DialogueMove(move_type="ask", content=question, speaker="system")],
            plan=[
                Plan(plan_type="findout", content=question),
                Plan(plan_type="inform", content="travel_options"),
            ],
            issues=[WhQuestion(predicate="date", variable="when")],
        ),
    )
    
    renderer.print_state(state, title="Travel Planning Dialogue")
    
    # Demo 2: State diff visualization
    console.print("\n\n[bold]Demo 2: State Diff Visualization[/bold]\n")
    
    # Before state
    snapshot1 = StateSnapshot.from_state(state, timestamp=0, label="Before answer")
    
    # After state - user answers destination question
    state.shared.commitments.add("destination: Paris")
    state.shared.qud.pop()  # Remove answered question
    state.private.beliefs["destination_confirmed"] = True
    
    snapshot2 = StateSnapshot.from_state(state, timestamp=1, label="After answer")
    
    diff = compute_diff(snapshot1, snapshot2)
    renderer.print_diff(diff, title="User Answered Destination Question")
    
    # Demo 3: Rule trace visualization
    console.print("\n\n[bold]Demo 3: Rule Execution Trace[/bold]\n")
    
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
                rule_name="accommodate_skip_question",
                priority=25,
                preconditions_met=False,
                was_selected=False,
                reason="No skip request in user move",
            ),
            RuleEvaluation(
                rule_name="integrate_answer",
                priority=20,
                preconditions_met=True,
                was_selected=True,
                reason="Answer resolves top QUD question",
            ),
            RuleEvaluation(
                rule_name="integrate_question",
                priority=18,
                preconditions_met=False,
                was_selected=False,
                reason="User move is not a question",
            ),
            RuleEvaluation(
                rule_name="update_commitments",
                priority=10,
                preconditions_met=True,
                was_selected=False,
                reason="Lower priority than selected rule",
            ),
        ],
    )
    
    renderer.print_rule_trace(trace, title="Integration Phase - Answer Processing")
    
    # Demo 4: ICM grounding visualization
    console.print("\n\n[bold]Demo 4: ICM Grounding Flow[/bold]\n")
    
    # Low confidence scenario
    state_low_conf = InformationState(
        shared=SharedIS(
            last_moves=[
                DialogueMove(
                    move_type="answer",
                    content="[garbled]",
                    speaker="user",
                    metadata={"confidence": 0.3},
                )
            ]
        ),
        private=PrivateIS(
            beliefs={"grounding_strategy": "pessimistic"},
        ),
    )
    
    renderer.print_state(state_low_conf, title="Low Confidence Input (Pessimistic Grounding)")
    
    icm_trace = RuleTrace(
        phase="select",
        timestamp=2,
        label="Select perception check",
        selected_rule="select_perception_check",
        evaluations=[
            RuleEvaluation(
                rule_name="select_perception_check",
                priority=18,
                preconditions_met=True,
                was_selected=True,
                reason="Very low confidence (0.3) → pessimistic strategy",
            ),
            RuleEvaluation(
                rule_name="select_understanding_confirmation",
                priority=17,
                preconditions_met=False,
                was_selected=False,
                reason="Confidence too low for cautious strategy",
            ),
            RuleEvaluation(
                rule_name="select_answer",
                priority=15,
                preconditions_met=False,
                was_selected=False,
                reason="Cannot answer unclear input",
            ),
        ],
    )
    
    renderer.print_rule_trace(icm_trace, title="ICM Selection - Perception Check")
    
    console.print("\n[bold cyan]═══ End of Demo ═══[/bold cyan]\n")


if __name__ == "__main__":
    main()
