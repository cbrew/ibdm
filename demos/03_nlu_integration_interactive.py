#!/usr/bin/env python3
"""
Demo 3 (Interactive): IBDM-NLU Integration - Legal Document Generation

This interactive demo showcases the integration between IBDM theoretical concepts
and practical NLU components through a conversational legal document generation scenario.

Domain: Non-Disclosure Agreement (NDA) Generation
Participants: You (Attorney) ↔ Legal Document System (Agent)

Key Demonstrations:
- Natural language utterances → IBDM structures (Questions, Moves, Answers)
- Question Under Discussion (QUD) stack evolution
- Entity extraction for legal entities (organizations, dates, jurisdictions)
- Task accommodation (system infers document requirements)
- LLM-based natural language understanding with Claude Sonnet
- Performance metrics and token tracking

Requirements:
- IBDM_API_KEY environment variable must be set
- Uses Claude models via LiteLLM for NLU tasks

Usage:
    python demos/03_nlu_integration_interactive.py [--verbose] [--no-color]

Options:
    --verbose, -v    Show detailed NLU processing information
    --no-color       Disable colored output
    --help, -h       Show this help message

Run: python demos/03_nlu_integration_interactive.py
"""

import argparse
import os
import sys
import time
from dataclasses import dataclass, field

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.tree import Tree

# IBDM Core imports
from ibdm.core import (
    AltQuestion,
    Answer,
    DialogueMove,
    Question,
    WhQuestion,
    YNQuestion,
)

# =============================================================================
# Metrics Tracking
# =============================================================================


@dataclass
class TurnMetrics:
    """Metrics for a single dialogue turn."""

    turn_number: int
    speaker: str
    utterance: str
    strategy_used: str
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
        strategy: str,
        tokens_input: int = 0,
        tokens_output: int = 0,
        latency: float = 0.0,
    ) -> TurnMetrics:
        """Add a new turn's metrics."""
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
            strategy = str(turn.strategy_used).lower()
            distribution[strategy] = distribution.get(strategy, 0) + 1
        return distribution


# =============================================================================
# Visualization Helper Functions
# =============================================================================


def format_turn_metrics(metrics: TurnMetrics) -> Table:
    """Format per-turn metrics as a rich Table."""
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column("Label", style="dim")
    table.add_column("Value")

    # Strategy color coding
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
    """Format complete metrics dashboard."""
    # Create main table
    table = Table(title="Session Metrics", show_header=True, header_style="bold cyan")
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

    return Panel(table, border_style="cyan", padding=(1, 2))


def format_dialogue_move(move: DialogueMove) -> Panel:
    """Format a DialogueMove as a rich Panel."""
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
        "command": "magenta",
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


def format_qud_stack(qud: list[Question]) -> Panel:
    """Format the QUD stack as a Tree visualization."""
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


def check_api_key() -> bool:
    """Verify that IBDM_API_KEY is available."""
    api_key = os.getenv("IBDM_API_KEY")
    if not api_key:
        return False
    return True


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="IBDM-NLU Interactive Demo: Legal Document Generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show detailed NLU processing information"
    )

    parser.add_argument("--no-color", action="store_true", help="Disable colored output")

    return parser.parse_args()


def main():
    """Main entry point for the interactive demo."""
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
            "[bold cyan]IBDM-NLU Interactive Demo[/bold cyan]\n"
            "[white]Legal Document Generation: Non-Disclosure Agreement[/white]\n\n"
            "[dim]Type your messages to interact with the legal document system\n"
            "Type 'quit' or 'exit' to end the session[/dim]",
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
    console.print()

    # Validate configuration before initializing
    console.print("[dim]Validating configuration...[/dim]")

    try:
        from ibdm.burr_integration import DialogueStateMachine
        from ibdm.engine import NLUDialogueEngine, NLUEngineConfig
        from ibdm.nlu import ModelType
        from ibdm.rules import (
            RuleSet,
            create_generation_rules,
            create_integration_rules,
            create_selection_rules,
        )

        # Check that we can import required components
        console.print("[dim]  ✓ All modules available[/dim]")

        # Create rule set with IBDM rules for proper QUD management
        rules = RuleSet()
        for rule in create_integration_rules():
            rules.add_rule(rule)
        for rule in create_selection_rules():
            rules.add_rule(rule)
        for rule in create_generation_rules():
            rules.add_rule(rule)

        console.print(f"[dim]  ✓ Loaded {rules.rule_count()} IBDM rules[/dim]")

        # Simple, explicit configuration - use Sonnet for NLU
        engine_config = NLUEngineConfig(
            llm_model=ModelType.SONNET,  # Use Sonnet model (Policy #9)
            temperature=0.3,
            max_tokens=2000,
        )

        console.print("[dim]  ✓ Configuration validated[/dim]")
        console.print()
        console.print("[cyan]Configuration:[/cyan]")
        console.print(f"  • Model: {ModelType.SONNET.value}")
        console.print(f"  • Rules: {rules.rule_count()} IBDM rules loaded")
        console.print(f"  • API Key: IBDM_API_KEY ({'✓ set' if check_api_key() else '✗ missing'})")
        console.print()

        # Initialize Burr state machine with NLU engine
        state_machine = DialogueStateMachine(
            agent_id="legal_system",
            rules=rules,
            engine_class=NLUDialogueEngine,
            engine_config=engine_config,
        )
        state_machine.initialize()

        console.print("[green]✓ Burr state machine initialized with NLU engine[/green]")
        console.print()

    except ImportError as e:
        console.print(f"[bold red]Import Error:[/bold red] {e}")
        console.print("Required modules are not available.")
        console.print()
        return 1
    except Exception as e:
        console.print(f"[bold red]Configuration Error:[/bold red] {e}")
        console.print()
        return 1

    # Initialize metrics tracker
    tracker = MetricsTracker()

    # Conversation loop
    console.print("[bold cyan]Starting Interactive Session[/bold cyan]")
    console.print()
    console.print(
        Panel(
            "[bold]System:[/bold] Hello! I'm here to help you draft a Non-Disclosure Agreement.\n"
            "What would you like to do?",
            title="Legal System",
            border_style="green",
            padding=(1, 2),
        )
    )
    console.print()

    turn_number = 0

    while True:
        # Get user input
        console.print()
        try:
            user_input = Prompt.ask("[bold blue]You[/bold blue]")
        except (KeyboardInterrupt, EOFError):
            console.print()
            console.print("[yellow]Session interrupted by user[/yellow]")
            break

        # Check for quit command
        if user_input.strip().lower() in ["quit", "exit", "bye", "goodbye"]:
            console.print()
            console.print("[yellow]Ending session...[/yellow]")
            break

        # Skip empty input
        if not user_input.strip():
            continue

        turn_number += 1

        # Display turn header
        console.print()
        console.print(f"[bold]{'=' * 80}[/bold]")
        console.print(f"[bold cyan]Turn {turn_number}[/bold cyan]")
        console.print(f"[bold]{'=' * 80}[/bold]")
        console.print()

        # Display user utterance
        console.print(
            Panel(
                f"[bold]{user_input}[/bold]",
                title=f"You (Turn {turn_number})",
                border_style="blue",
                padding=(1, 2),
            )
        )
        console.print()

        # Process utterance through Burr state machine
        if args.verbose:
            console.print("[dim]Processing utterance through IBDM loop...[/dim]")

        try:
            # Time the full IBDM loop
            start_time = time.time()
            # Run full IBDM loop: interpret → integrate → select → generate
            response_data = state_machine.process_utterance(user_input, "user")
            latency = time.time() - start_time

            # Get moves from Burr state
            burr_state = state_machine.get_state()
            moves_data = burr_state.get("moves", [])

            # Deserialize moves from dictionaries to DialogueMove objects
            moves = []
            for move_dict in moves_data:
                if isinstance(move_dict, dict):
                    moves.append(DialogueMove.from_dict(move_dict))
                else:
                    moves.append(move_dict)

            # Get token counts from engine if available
            tokens_in = 0
            tokens_out = 0
            info_state = state_machine.get_information_state()
            if info_state and hasattr(info_state, "_last_interpretation_tokens"):
                total_tokens = info_state._last_interpretation_tokens
                tokens_in = total_tokens // 2  # Approximate input/output split
                tokens_out = total_tokens - tokens_in

            # Track metrics
            metrics = tracker.add_turn(
                turn_number=turn_number,
                speaker="user",
                utterance=user_input,
                strategy="sonnet",  # We configured Sonnet model
                tokens_input=tokens_in,
                tokens_output=tokens_out,
                latency=latency,
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
            else:
                console.print("[yellow]⚠ No moves interpreted[/yellow]")
                console.print()

            # Display QUD stack state (managed automatically by integration rules)
            current_state = state_machine.get_information_state()
            if current_state and current_state.shared.qud:
                console.print(format_qud_stack(current_state.shared.qud))
                console.print()

            # Display system response
            if response_data.get("has_response"):
                system_response = response_data.get("utterance_text", "")
                if system_response:
                    console.print(
                        Panel(
                            f"[bold]{system_response}[/bold]",
                            title="Legal System",
                            border_style="green",
                            padding=(1, 2),
                        )
                    )
                    console.print()

        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            if args.verbose:
                import traceback

                console.print(traceback.format_exc())
            console.print()

    # Display final metrics
    console.print()
    console.print(f"[bold]{'=' * 80}[/bold]")
    console.print("[bold cyan]Session Summary[/bold cyan]")
    console.print(f"[bold]{'=' * 80}[/bold]")
    console.print()

    console.print(format_metrics_dashboard(tracker))
    console.print()

    console.print("[green]✓ Interactive session completed![/green]")
    console.print(f"[dim]Processed {len(tracker.turns)} turns using {ModelType.SONNET.value}[/dim]")
    console.print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
