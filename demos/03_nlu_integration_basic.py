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
from dataclasses import dataclass, field
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
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
from ibdm.nlu import InterpretationStrategy

# =============================================================================
# Metrics Tracking
# =============================================================================


@dataclass
class TurnMetrics:
    """Metrics for a single dialogue turn."""

    turn_number: int
    speaker: str
    utterance: str
    strategy_used: InterpretationStrategy | str
    tokens_input: int = 0
    tokens_output: int = 0
    cost: float = 0.0
    latency: float = 0.0

    @property
    def total_tokens(self) -> int:
        """Total tokens used in this turn."""
        return self.tokens_input + self.tokens_output

    def calculate_cost(self) -> None:
        """Calculate cost based on model and tokens used."""
        # Pricing per million tokens (Claude models via LiteLLM)
        if isinstance(self.strategy_used, InterpretationStrategy):
            strategy_str = self.strategy_used.value
        else:
            strategy_str = str(self.strategy_used).lower()

        if "sonnet" in strategy_str:
            # Claude Sonnet 4.5: $3 input / $15 output per million
            input_cost = (self.tokens_input / 1_000_000) * 3.0
            output_cost = (self.tokens_output / 1_000_000) * 15.0
            self.cost = input_cost + output_cost
        elif "haiku" in strategy_str:
            # Claude Haiku 4.5: $1 input / $5 output per million
            input_cost = (self.tokens_input / 1_000_000) * 1.0
            output_cost = (self.tokens_output / 1_000_000) * 5.0
            self.cost = input_cost + output_cost
        else:
            # Rules/patterns: free
            self.cost = 0.0


@dataclass
class MetricsTracker:
    """Tracks metrics across dialogue turns."""

    turns: list[TurnMetrics] = field(default_factory=list)

    def add_turn(
        self,
        turn_number: int,
        speaker: str,
        utterance: str,
        strategy: InterpretationStrategy | str,
        tokens_input: int = 0,
        tokens_output: int = 0,
        latency: float = 0.0,
    ) -> TurnMetrics:
        """Add a new turn's metrics.

        Args:
            turn_number: Turn number
            speaker: Speaker ID
            utterance: The utterance text
            strategy: Strategy used for interpretation
            tokens_input: Input tokens used
            tokens_output: Output tokens used
            latency: Processing latency in seconds

        Returns:
            The created TurnMetrics object
        """
        metrics = TurnMetrics(
            turn_number=turn_number,
            speaker=speaker,
            utterance=utterance,
            strategy_used=strategy,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            latency=latency,
        )
        metrics.calculate_cost()
        self.turns.append(metrics)
        return metrics

    @property
    def total_tokens(self) -> int:
        """Total tokens across all turns."""
        return sum(t.total_tokens for t in self.turns)

    @property
    def total_cost(self) -> float:
        """Total cost across all turns."""
        return sum(t.cost for t in self.turns)

    @property
    def total_latency(self) -> float:
        """Total latency across all turns."""
        return sum(t.latency for t in self.turns)

    @property
    def avg_latency(self) -> float:
        """Average latency per turn."""
        return self.total_latency / len(self.turns) if self.turns else 0.0

    def strategy_distribution(self) -> dict[str, int]:
        """Get distribution of strategies used."""
        distribution: dict[str, int] = {}
        for turn in self.turns:
            if isinstance(turn.strategy_used, InterpretationStrategy):
                strategy = turn.strategy_used.value
            else:
                strategy = str(turn.strategy_used).lower()

            distribution[strategy] = distribution.get(strategy, 0) + 1
        return distribution


def format_turn_metrics(metrics: TurnMetrics) -> Table:
    """Format per-turn metrics as a rich Table.

    Args:
        metrics: The turn metrics to format

    Returns:
        A styled Table showing turn metrics
    """
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column("Label", style="dim")
    table.add_column("Value")

    # Strategy color coding
    if isinstance(metrics.strategy_used, InterpretationStrategy):
        strategy_str = metrics.strategy_used.value
    else:
        strategy_str = str(metrics.strategy_used).lower()

    if "rules" in strategy_str or "pattern" in strategy_str:
        strategy_color = "green"
        strategy_badge = "🟢"
    elif "haiku" in strategy_str:
        strategy_color = "yellow"
        strategy_badge = "🟡"
    elif "sonnet" in strategy_str:
        strategy_color = "red"
        strategy_badge = "🔴"
    else:
        strategy_color = "white"
        strategy_badge = "⚪"

    table.add_row(
        "Strategy:", f"{strategy_badge} [{strategy_color}]{strategy_str}[/{strategy_color}]"
    )
    table.add_row(
        "Tokens:",
        f"{metrics.total_tokens} ({metrics.tokens_input} in / {metrics.tokens_output} out)",
    )
    table.add_row("Cost:", f"${metrics.cost:.6f}")
    table.add_row("Latency:", f"{metrics.latency:.3f}s")

    return table


def format_metrics_dashboard(tracker: MetricsTracker) -> Panel:
    """Format complete metrics dashboard.

    Args:
        tracker: The MetricsTracker with accumulated metrics

    Returns:
        A Panel containing the metrics dashboard
    """
    # Create main table
    table = Table(title="Metrics Dashboard", show_header=True, header_style="bold cyan")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="right")

    # Overall stats
    table.add_section()
    table.add_row("Total Turns", str(len(tracker.turns)))
    table.add_row("Total Tokens", f"{tracker.total_tokens:,}")
    table.add_row("Total Cost", f"${tracker.total_cost:.6f}")
    table.add_row("Avg Latency", f"{tracker.avg_latency:.3f}s")
    table.add_row("Total Latency", f"{tracker.total_latency:.3f}s")

    # Strategy distribution
    distribution = tracker.strategy_distribution()
    if distribution:
        table.add_section()
        table.add_row("[bold]Strategy Distribution[/bold]", "")
        for strategy, count in sorted(distribution.items()):
            percentage = (count / len(tracker.turns)) * 100
            if "rules" in strategy or "pattern" in strategy:
                badge = "🟢"
            elif "haiku" in strategy:
                badge = "🟡"
            elif "sonnet" in strategy:
                badge = "🔴"
            else:
                badge = "⚪"
            table.add_row(f"  {badge} {strategy}", f"{count} ({percentage:.1f}%)")

    # Cost breakdown
    costs_by_strategy: dict[str, float] = {}
    tokens_by_strategy: dict[str, int] = {}
    for turn in tracker.turns:
        if isinstance(turn.strategy_used, InterpretationStrategy):
            strategy = turn.strategy_used.value
        else:
            strategy = str(turn.strategy_used).lower()

        costs_by_strategy[strategy] = costs_by_strategy.get(strategy, 0.0) + turn.cost
        tokens_by_strategy[strategy] = tokens_by_strategy.get(strategy, 0) + turn.total_tokens

    if costs_by_strategy:
        table.add_section()
        table.add_row("[bold]Cost by Strategy[/bold]", "")
        for strategy, cost in sorted(costs_by_strategy.items(), key=lambda x: x[1], reverse=True):
            tokens = tokens_by_strategy.get(strategy, 0)
            table.add_row(f"  {strategy}", f"${cost:.6f} ({tokens} tokens)")

    return Panel(table, border_style="cyan", padding=(1, 2))


# =============================================================================
# Dialogue Scenarios
# =============================================================================


@dataclass
class DialogueTurn:
    """A single turn in a pre-scripted dialogue."""

    turn_number: int
    speaker: str  # "attorney" or "system"
    utterance: str
    expected_strategy: InterpretationStrategy | str
    expected_dialogue_act: str
    expected_tokens_input: int = 0
    expected_tokens_output: int = 0
    expected_latency: float = 0.0
    entities: list[dict[str, Any]] = field(default_factory=list)
    notes: str = ""


# NDA Generation Dialogue Scenario
# Based on SCENARIO_PLAN_NDA.md
NDA_DIALOGUE_TURNS = [
    DialogueTurn(
        turn_number=1,
        speaker="attorney",
        utterance="I need to draft an NDA",
        expected_strategy="rules",
        expected_dialogue_act="request",
        expected_tokens_input=0,
        expected_tokens_output=0,
        expected_latency=0.01,
        entities=[],
        notes="Task accommodation: system infers NDA document requirements",
    ),
    DialogueTurn(
        turn_number=2,
        speaker="attorney",
        utterance="Between Acme Corporation as disclosing party and TechStart Incorporated",
        expected_strategy=InterpretationStrategy.HAIKU,
        expected_dialogue_act="answer",
        expected_tokens_input=60,
        expected_tokens_output=120,
        expected_latency=0.5,
        entities=[
            {
                "text": "Acme Corporation",
                "type": "ORG",
                "role": "disclosing_party",
            },
            {
                "text": "TechStart Incorporated",
                "type": "ORG",
                "role": "receiving_party",
            },
        ],
        notes="Entity extraction for legal parties with roles",
    ),
    DialogueTurn(
        turn_number=3,
        speaker="attorney",
        utterance="Mutual NDA",
        expected_strategy="rules",
        expected_dialogue_act="answer",
        expected_tokens_input=0,
        expected_tokens_output=0,
        expected_latency=0.01,
        entities=[],
        notes="Pattern matching: keyword 'mutual' selects alternative",
    ),
    DialogueTurn(
        turn_number=4,
        speaker="attorney",
        utterance="January 1st, 2025",
        expected_strategy=InterpretationStrategy.HAIKU,
        expected_dialogue_act="answer",
        expected_tokens_input=50,
        expected_tokens_output=100,
        expected_latency=0.4,
        entities=[
            {
                "text": "January 1st, 2025",
                "type": "DATE",
                "normalized": "2025-01-01",
            },
        ],
        notes="Temporal entity extraction and normalization",
    ),
    DialogueTurn(
        turn_number=5,
        speaker="attorney",
        utterance="Three years",
        expected_strategy=InterpretationStrategy.HAIKU,
        expected_dialogue_act="answer",
        expected_tokens_input=45,
        expected_tokens_output=90,
        expected_latency=0.4,
        entities=[
            {
                "text": "Three years",
                "type": "DURATION",
                "normalized": {"value": 3, "unit": "years"},
            },
        ],
        notes="Duration parsing from natural language",
    ),
    DialogueTurn(
        turn_number=6,
        speaker="attorney",
        utterance="California law",
        expected_strategy="rules",
        expected_dialogue_act="answer",
        expected_tokens_input=0,
        expected_tokens_output=0,
        expected_latency=0.01,
        entities=[
            {
                "text": "California",
                "type": "LOCATION",
                "context": "governing_law",
            },
        ],
        notes="Jurisdiction selection from common legal jurisdictions",
    ),
    DialogueTurn(
        turn_number=7,
        speaker="attorney",
        utterance="Yes, generate it",
        expected_strategy="rules",
        expected_dialogue_act="answer",
        expected_tokens_input=0,
        expected_tokens_output=0,
        expected_latency=0.01,
        entities=[],
        notes="Affirmative response to Y/N question",
    ),
]

# System prompts for each turn (what system says to elicit the attorney response)
NDA_SYSTEM_PROMPTS = [
    "I'll help you draft an NDA. What are the names of the parties entering into this agreement?",
    "Should this be a mutual NDA or one-way?",
    "What should the effective date be?",
    "What should the confidentiality period be?",
    "Which state law should govern this agreement - California or Delaware?",
    "I have all the information needed. Should I generate the NDA now?",
]

# Document requirements checklist
NDA_REQUIREMENTS = [
    {"field": "document_type", "label": "Document Type", "required": True},
    {"field": "parties", "label": "Parties", "required": True},
    {"field": "nda_type", "label": "NDA Type", "required": True},
    {"field": "effective_date", "label": "Effective Date", "required": True},
    {"field": "duration", "label": "Duration", "required": True},
    {"field": "governing_law", "label": "Governing Law", "required": True},
]


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
    console.print("[dim]✓ API key found[/dim]")
    console.print("[dim]✓ Initializing NLU components...[/dim]")
    console.print()

    # Initialize NLU engine with hybrid fallback
    try:
        from ibdm.engine import NLUDialogueEngine, NLUEngineConfig
        from ibdm.nlu import FallbackConfig

        # Configure hybrid fallback for cost optimization
        fallback_config = FallbackConfig(
            enable_fast_path=True,
            enable_cascading=True,
            complexity_threshold=0.7,  # Try Haiku first for medium complexity
        )

        engine_config = NLUEngineConfig(
            use_nlu=True,
            use_llm=True,
            enable_hybrid_fallback=True,
            fallback_config=fallback_config,
        )

        engine = NLUDialogueEngine(agent_id="legal_system", config=engine_config)

        console.print("[green]✓ NLU engine initialized with hybrid fallback[/green]")
        console.print()

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] Failed to initialize NLU engine: {e}")
        console.print()
        return 1

    # Initialize information state
    state = InformationState(agent_id="legal_system")

    # Initialize metrics tracker
    tracker = MetricsTracker()

    # Document information being gathered
    gathered_info: dict[str, Any] = {
        "document_type": "NDA",  # Known from turn 1
    }

    # Run through the dialogue scenario
    console.print("[bold cyan]Starting NDA Generation Dialogue[/bold cyan]")
    console.print()

    for i, turn in enumerate(NDA_DIALOGUE_TURNS):
        # Display turn header
        console.print(f"[bold]{'=' * 80}[/bold]")
        console.print(f"[bold cyan]Turn {turn.turn_number}[/bold cyan]")
        console.print(f"[bold]{'=' * 80}[/bold]")
        console.print()

        # Display attorney utterance
        console.print(
            Panel(
                f"[bold]{turn.utterance}[/bold]",
                title=f"Attorney (Turn {turn.turn_number})",
                border_style="blue",
                padding=(1, 2),
            )
        )
        console.print()

        # Interpret the utterance
        if args.verbose:
            console.print("[dim]Interpreting with NLU...[/dim]")

        try:
            moves = engine.interpret(turn.utterance, "attorney")

            # Get strategy used and tokens
            strategy_used = "rules"  # Default
            tokens_in = 0
            tokens_out = 0

            if engine.fallback_strategy:
                # Get the most recent strategy from stats
                stats = engine.fallback_strategy.get_stats()
                if stats.strategy_usage:
                    # Find the strategy with the highest usage count (most recent)
                    strategy_used = max(
                        stats.strategy_usage.items(),
                        key=lambda x: x[1],
                    )[0].value

                # Get token counts from the last interpretation
                tokens_in = engine.last_interpretation_tokens // 2  # Approximate split
                tokens_out = engine.last_interpretation_tokens - tokens_in

            # Track metrics
            metrics = tracker.add_turn(
                turn_number=turn.turn_number,
                speaker="attorney",
                utterance=turn.utterance,
                strategy=strategy_used,
                tokens_input=tokens_in,
                tokens_output=tokens_out,
                latency=engine.last_interpretation_latency,
            )

            # Display strategy used
            console.print(format_turn_metrics(metrics))
            console.print()

            # Display dialogue moves
            if moves:
                console.print(f"[green]✓ Interpreted {len(moves)} dialogue move(s)[/green]")
                for move in moves:
                    console.print(format_dialogue_move(move))
                    console.print()

                    # Extract structured information based on move type
                    if move.move_type == "request":
                        console.print(
                            "[dim]Task accommodation: System infers NDA requirements[/dim]"
                        )
                        console.print()

                    elif move.move_type == "answer" and isinstance(move.content, Answer):
                        # Update gathered info based on turn
                        if turn.turn_number == 2:
                            gathered_info["parties"] = move.content.content
                            gathered_info["entities"] = turn.entities
                        elif turn.turn_number == 3:
                            gathered_info["nda_type"] = "Mutual"
                        elif turn.turn_number == 4:
                            gathered_info["effective_date"] = "2025-01-01"
                        elif turn.turn_number == 5:
                            gathered_info["duration"] = "3 years"
                        elif turn.turn_number == 6:
                            gathered_info["governing_law"] = "California"

            else:
                console.print("[yellow]⚠ No moves interpreted[/yellow]")
                console.print()

            # Display QUD stack state
            if state.shared.qud:
                console.print(format_qud_stack(state.shared.qud))
                console.print()

            # Display system response (from pre-scripted prompts)
            if i < len(NDA_SYSTEM_PROMPTS):
                system_prompt = NDA_SYSTEM_PROMPTS[i]
                console.print(
                    Panel(
                        f"[bold]{system_prompt}[/bold]",
                        title="Legal System",
                        border_style="green",
                        padding=(1, 2),
                    )
                )
                console.print()

                # Update QUD stack to reflect system question
                # (In a real system, this would be done by the selection/generation rules)
                if i == 0:  # After turn 1
                    q = WhQuestion(variable="parties", predicate="legal_entities")
                    state.shared.push_qud(q)
                elif i == 1:  # After turn 2
                    if state.shared.qud:
                        state.shared.pop_qud()  # Resolve parties question
                    q = AltQuestion(alternatives=["mutual", "one-way"])
                    state.shared.push_qud(q)
                elif i == 2:  # After turn 3
                    if state.shared.qud:
                        state.shared.pop_qud()  # Resolve NDA type
                    q = WhQuestion(variable="effective_date", predicate="date")
                    state.shared.push_qud(q)
                elif i == 3:  # After turn 4
                    if state.shared.qud:
                        state.shared.pop_qud()  # Resolve effective date
                    q = WhQuestion(variable="duration", predicate="time_period")
                    state.shared.push_qud(q)
                elif i == 4:  # After turn 5
                    if state.shared.qud:
                        state.shared.pop_qud()  # Resolve duration
                    q = AltQuestion(alternatives=["California", "Delaware"])
                    state.shared.push_qud(q)
                elif i == 5:  # After turn 6
                    if state.shared.qud:
                        state.shared.pop_qud()  # Resolve governing law
                    q = YNQuestion(proposition="generate_document")
                    state.shared.push_qud(q)

        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            if args.verbose:
                import traceback

                console.print(traceback.format_exc())
            console.print()

        # Separator between turns
        console.print()

    # Display final gathered information
    console.print(f"[bold]{'=' * 80}[/bold]")
    console.print("[bold green]Document Information Gathered[/bold green]")
    console.print(f"[bold]{'=' * 80}[/bold]")
    console.print()

    # Create checklist table
    checklist = Table(title="NDA Requirements", show_header=True, header_style="bold cyan")
    checklist.add_column("Field", style="cyan")
    checklist.add_column("Value", style="green")
    checklist.add_column("Status", justify="center")

    for req in NDA_REQUIREMENTS:
        field_name = req["field"]
        value = gathered_info.get(field_name, "—")
        status = "✓" if field_name in gathered_info else "✗"
        status_color = "green" if field_name in gathered_info else "red"

        checklist.add_row(req["label"], str(value), f"[{status_color}]{status}[/{status_color}]")

    console.print(checklist)
    console.print()

    # Display final metrics dashboard
    console.print(f"[bold]{'=' * 80}[/bold]")
    console.print("[bold cyan]Performance Metrics[/bold cyan]")
    console.print(f"[bold]{'=' * 80}[/bold]")
    console.print()

    console.print(format_metrics_dashboard(tracker))
    console.print()

    # Display strategy effectiveness
    if engine.fallback_strategy:
        stats = engine.fallback_strategy.get_stats()
        console.print("[bold]Strategy Distribution:[/bold]")
        console.print(f"  Total interpretations: {stats.total_calls}")
        console.print()

        if stats.strategy_usage:
            usage_table = Table(show_header=True, header_style="bold")
            usage_table.add_column("Strategy", style="cyan")
            usage_table.add_column("Usage Count", justify="right")
            usage_table.add_column("Percentage", justify="right")

            for strategy, count in stats.strategy_usage.items():
                pct = (count / stats.total_calls * 100) if stats.total_calls > 0 else 0
                usage_table.add_row(strategy.value, str(count), f"{pct:.1f}%")

            console.print(usage_table)
            console.print()

    console.print("[green]✓ Demo completed successfully![/green]")
    console.print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
