#!/usr/bin/env python3
"""
Demo 3: IBDM-NLU Integration - Legal Document Generation

This demo showcases the integration between IBDM theoretical concepts and
practical NLU components through a legal document generation scenario.

Domain: Non-Disclosure Agreement (NDA) Generation
Participants: Attorney (User) ↔ Legal Document System (Agent)

Key Demonstrations:
- Natural language utterances → IBDM structures (Questions, Moves, Answers)
- Question Under Discussion (QUD) stack evolution
- Entity extraction for legal entities (organizations, dates, jurisdictions)
- Task accommodation (system infers document requirements)
- Hybrid fallback strategy (pattern matching → Haiku → Sonnet)
- Cost optimization and performance metrics

Requirements:
- IBDM_API_KEY environment variable must be set
- Uses Claude models via LiteLLM for NLU tasks

Usage:
    python demos/03_nlu_integration_basic.py [--verbose] [--no-color]

Options:
    --verbose, -v    Show detailed NLU processing information
    --no-color       Disable colored output
    --help, -h       Show this help message

Run: python demos/03_nlu_integration_basic.py
"""

import argparse
import os
import sys

from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree

# IBDM Core imports
from ibdm.core import (
    AltQuestion,
    Answer,
    DialogueMove,
    InformationState,
    Question,
    WhQuestion,
    YNQuestion,
)

# IBDM Engine imports

# NLU imports


# =============================================================================
# Visualization Helper Functions
# =============================================================================


def format_question(question: Question) -> Panel:
    """Format a Question object as a rich Panel.

    Args:
        question: The Question object to format

    Returns:
        A styled Panel containing the question representation
    """
    # Determine question type and color
    if isinstance(question, WhQuestion):
        qtype = "Wh-Question"
        color = "cyan"
        details = f"Variable: [bold]{question.variable}[/bold]\n"
        details += f"Predicate: {question.predicate}"
        if question.constraints:
            details += f"\nConstraints: {question.constraints}"
    elif isinstance(question, YNQuestion):
        qtype = "Y/N Question"
        color = "green"
        details = f"Proposition: {question.proposition}"
        if question.parameters:
            details += f"\nParameters: {question.parameters}"
    elif isinstance(question, AltQuestion):
        qtype = "Alternative Question"
        color = "yellow"
        details = f"Alternatives: {', '.join(question.alternatives)}"
    else:
        qtype = "Question"
        color = "white"
        details = str(question)

    # Create the panel content
    content = f"[{color}]{qtype}[/{color}]\n"
    content += f"[dim]Representation:[/dim] [bold]{question}[/bold]\n\n"
    content += details

    return Panel(content, border_style=color, title="Question", padding=(1, 2))


def format_dialogue_move(move: DialogueMove) -> Panel:
    """Format a DialogueMove as a rich Panel.

    Args:
        move: The DialogueMove to format

    Returns:
        A styled Panel containing the move details
    """
    # Color coding for different move types
    move_colors = {
        "ask": "cyan",
        "answer": "green",
        "assert": "blue",
        "request": "magenta",
        "greet": "yellow",
        "quit": "red",
        "acknowledge": "green",
        "clarify": "yellow",
        "inform": "blue",
    }

    color = move_colors.get(move.move_type, "white")

    # Format content based on type
    if isinstance(move.content, Question):
        content_str = str(move.content)
        content_type = "Question"
    elif isinstance(move.content, Answer):
        content_str = str(move.content)
        content_type = "Answer"
    else:
        content_str = str(move.content)
        content_type = "Content"

    # Build panel content
    panel_content = f"[{color}]Move Type:[/{color}] [bold]{move.move_type}[/bold]\n"
    panel_content += f"[dim]Speaker:[/dim] {move.speaker}\n"
    panel_content += f"[dim]{content_type}:[/dim] {content_str}"

    return Panel(panel_content, border_style=color, title="Dialogue Move", padding=(1, 2))


def format_answer(answer: Answer) -> Panel:
    """Format an Answer object as a rich Panel.

    Args:
        answer: The Answer to format

    Returns:
        A styled Panel containing the answer details
    """
    # Determine color based on certainty
    if answer.certainty >= 0.9:
        color = "green"
    elif answer.certainty >= 0.7:
        color = "yellow"
    else:
        color = "red"

    # Build content
    content = f"[bold]Content:[/bold] {answer.content}\n"
    content += f"[dim]Certainty:[/dim] {answer.certainty:.2f}"

    if answer.question_ref:
        content += f"\n[dim]Addresses:[/dim] {answer.question_ref}"

    return Panel(content, border_style=color, title="Answer", padding=(1, 2))


def format_qud_stack(qud: list[Question]) -> Panel:
    """Format the QUD stack as a Tree visualization.

    Args:
        qud: List of Questions representing the QUD stack

    Returns:
        A Panel containing a tree visualization of the QUD stack
    """
    if not qud:
        return Panel(
            "[dim]QUD stack is empty[/dim]",
            border_style="white",
            title="Question Under Discussion (QUD) Stack",
            padding=(1, 2),
        )

    # Create a tree for the QUD stack
    tree = Tree("[bold cyan]QUD Stack[/bold cyan] (bottom → top)")

    # Add questions from bottom to top
    for i, question in enumerate(qud):
        # Determine question type for icon
        if isinstance(question, WhQuestion):
            icon = "❓"
            color = "cyan"
        elif isinstance(question, YNQuestion):
            icon = "✓"
            color = "green"
        elif isinstance(question, AltQuestion):
            icon = "⚡"
            color = "yellow"
        else:
            icon = "•"
            color = "white"

        # Add to tree with position indicator
        position = "TOP" if i == len(qud) - 1 else f"{i}"
        label = f"{icon} [{color}]{question}[/{color}] [dim]({position})[/dim]"
        tree.add(label)

    return Panel(tree, border_style="cyan", title="QUD Stack", padding=(1, 2))


def format_information_state(state: InformationState) -> Panel:
    """Format an InformationState as a multi-section Panel.

    Args:
        state: The InformationState to format

    Returns:
        A Panel containing all sections of the Information State
    """
    # Private IS section
    private_content = "[bold blue]Private IS:[/bold blue]\n"
    private_content += f"  Plans: {len(state.private.plan)}\n"
    private_content += f"  Agenda: {len(state.private.agenda)} items\n"
    private_content += f"  Beliefs: {len(state.private.beliefs)} entries"

    # Shared IS section
    shared_content = "\n\n[bold green]Shared IS:[/bold green]\n"
    shared_content += f"  QUD Stack: {len(state.shared.qud)} questions\n"
    if state.shared.qud:
        shared_content += f"    Top: {state.shared.qud[-1]}\n"
    shared_content += f"  Commitments: {len(state.shared.commitments)}\n"
    shared_content += f"  Recent Moves: {len(state.shared.last_moves)}"

    # Control IS section
    control_content = "\n\n[bold yellow]Control IS:[/bold yellow]\n"
    control_content += f"  Speaker: {state.control.speaker}\n"
    control_content += f"  Next Speaker: {state.control.next_speaker}\n"
    control_content += f"  Initiative: {state.control.initiative}\n"
    control_content += f"  Dialogue State: {state.control.dialogue_state}"

    # Combine all sections
    full_content = private_content + shared_content + control_content

    return Panel(
        full_content,
        border_style="magenta",
        title=f"Information State ({state.agent_id})",
        padding=(1, 2),
    )


def check_api_key() -> bool:
    """Verify that IBDM_API_KEY is available.

    Returns:
        True if API key is found, False otherwise
    """
    api_key = os.getenv("IBDM_API_KEY")
    if not api_key:
        return False
    return True


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="IBDM-NLU Integration Demo: Legal Document Generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show detailed NLU processing information"
    )

    parser.add_argument("--no-color", action="store_true", help="Disable colored output")

    return parser.parse_args()


def main():
    """Main entry point for the demo."""
    # Parse arguments
    args = parse_arguments()

    # Initialize console
    console = Console(
        force_terminal=not args.no_color, color_system="auto" if not args.no_color else None
    )

    # Display header
    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]IBDM-NLU Integration Demo[/bold cyan]\n"
            "[white]Legal Document Generation: Non-Disclosure Agreement[/white]",
            border_style="cyan",
            padding=(1, 2),
        )
    )
    console.print()

    # Check API key
    if not check_api_key():
        console.print(
            "[bold red]Error:[/bold red] IBDM_API_KEY environment variable not found.", style="red"
        )
        console.print()
        console.print("Please set your API key:")
        console.print("  export IBDM_API_KEY='your-key-here'")
        console.print()
        console.print("The API key should be available in the .env file.")
        return 1

    # Display setup info
    if args.verbose:
        console.print("[dim]✓ API key found[/dim]")
        console.print("[dim]✓ Initializing NLU components...[/dim]")
        console.print()

    # Demo: Test visualization helpers
    if args.verbose:
        console.print("[bold]Testing Visualization Helpers:[/bold]")
        console.print()

        # Test format_question
        wh_q = WhQuestion(
            variable="parties", predicate="legal_entities", constraints={"role": "NDA"}
        )
        console.print(format_question(wh_q))
        console.print()

        yn_q = YNQuestion(proposition="generate_document")
        console.print(format_question(yn_q))
        console.print()

        alt_q = AltQuestion(alternatives=["mutual", "one-way"])
        console.print(format_question(alt_q))
        console.print()

        # Test format_dialogue_move
        move = DialogueMove(move_type="ask", content=wh_q, speaker="system")
        console.print(format_dialogue_move(move))
        console.print()

        # Test format_answer
        answer = Answer(content="Acme Corp and TechStart Inc", certainty=0.95)
        console.print(format_answer(answer))
        console.print()

        # Test format_qud_stack
        qud_stack = [wh_q, yn_q, alt_q]
        console.print(format_qud_stack(qud_stack))
        console.print()

        # Test format_information_state
        from ibdm.core import InformationState

        state = InformationState(agent_id="legal_system")
        state.shared.push_qud(wh_q)
        state.shared.push_qud(alt_q)
        console.print(format_information_state(state))
        console.print()

    console.print("[green]✓ Visualization helpers ready[/green]")
    console.print("[yellow]Main demo implementation in progress...[/yellow]")
    console.print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
