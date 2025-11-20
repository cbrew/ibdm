"""Unified scenario runner for executing and displaying dialogue scenarios.

This module provides a clean, reusable interface for running JSON-based scenarios
with professional console output, execution flow control, and rich formatting.
"""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ibdm.demo.execution_controller import ExecutionController, ExecutionMode
from ibdm.demo.scenario_loader import Scenario, ScenarioLoader, ScenarioTurn


class ScenarioRunner:
    """Runs and displays dialogue scenarios with rich formatting.

    This class orchestrates scenario execution by combining:
    - ScenarioLoader: Loads JSON scenarios
    - ExecutionController: Controls timing and flow (step/auto/replay)
    - Rich formatting: Professional console output

    Unlike BusinessDemo, this runner focuses on scenario display
    rather than running the actual Larsson dialogue engine.

    Examples:
        >>> # Load and run a scenario
        >>> loader = ScenarioLoader()
        >>> scenario = loader.load_scenario("nda_basic")
        >>> runner = ScenarioRunner(scenario)
        >>> runner.run()

        >>> # Run in auto mode with custom delay
        >>> controller = ExecutionController(
        ...     mode=ExecutionMode.AUTO,
        ...     auto_delay=1.5
        ... )
        >>> runner = ScenarioRunner(scenario, controller=controller)
        >>> runner.run()

        >>> # Show detailed information
        >>> runner = ScenarioRunner(scenario, show_explanations=True)
        >>> runner.run()
    """

    def __init__(
        self,
        scenario: Scenario,
        controller: ExecutionController | None = None,
        console: Console | None = None,
        show_explanations: bool = True,
        show_state_changes: bool = True,
        show_larsson_rules: bool = True,
        show_metrics: bool = True,
    ):
        """Initialize scenario runner.

        Args:
            scenario: Scenario to run
            controller: Execution controller (default: AUTO mode)
            console: Rich console for output (default: create new)
            show_explanations: Show business explanations for each turn
            show_state_changes: Show state changes for each turn
            show_larsson_rules: Show Larsson rule references
            show_metrics: Show scenario metrics at the end
        """
        self.scenario = scenario
        self.controller = controller or ExecutionController(mode=ExecutionMode.AUTO)
        self.console = console or Console()
        self.show_explanations = show_explanations
        self.show_state_changes = show_state_changes
        self.show_larsson_rules = show_larsson_rules
        self.show_metrics = show_metrics

    def run(self) -> None:
        """Run the complete scenario.

        Displays:
        1. Banner with scenario metadata
        2. Each dialogue turn with formatting
        3. Final summary and metrics
        """
        self._display_banner()
        self.controller.wait_at_banner()

        for turn in self.scenario.turns:
            self._display_turn(turn)
            self.controller.wait_between_turns()

        self._display_summary()
        self.controller.wait_at_end()

    def _display_banner(self) -> None:
        """Display scenario banner with metadata."""
        # Title panel
        title_text = Text(self.scenario.title, style="bold cyan", justify="center")
        self.console.print(Panel(title_text, border_style="cyan"))

        # Metadata
        self.console.print(f"\n[bold]Description:[/bold] {self.scenario.metadata.description}")
        self.console.print(
            f"\n[bold yellow]Business Value:[/bold yellow]\n"
            f"{self.scenario.metadata.business_narrative}"
        )

        # Larsson algorithms
        if self.scenario.metadata.larsson_algorithms:
            self.console.print("\n[bold green]Larsson Algorithms:[/bold green]")
            for algo in self.scenario.metadata.larsson_algorithms:
                self.console.print(f"  • {algo}")

        # Expected outcomes
        if self.scenario.metadata.expected_outcomes:
            self.console.print("\n[bold magenta]Expected Outcomes:[/bold magenta]")
            for key, value in self.scenario.metadata.expected_outcomes.items():
                formatted_key = key.replace("_", " ").title()
                self.console.print(f"  • {formatted_key}: {value}")

        # Execution mode
        mode_text = {
            ExecutionMode.STEP: "⏸️  Manual mode: Press Enter to advance",
            ExecutionMode.AUTO: "▶️  Auto mode: Playing automatically",
            ExecutionMode.REPLAY: "🔄 Replay mode: Playing back scenario",
        }
        self.console.print(f"\n[dim]{mode_text.get(self.controller.mode, '')}[/dim]\n")

    def _display_turn(self, turn: ScenarioTurn) -> None:
        """Display a single dialogue turn.

        Args:
            turn: Turn to display
        """
        # Determine speaker styling
        if turn.speaker == "user":
            speaker_emoji = "👤"
            speaker_label = "USER"
            speaker_style = "bold blue"
            border_style = "blue"
        else:
            speaker_emoji = "🤖"
            speaker_label = "SYSTEM"
            speaker_style = "bold green"
            border_style = "green"

        # Turn header
        header = Text()
        header.append(f"{speaker_emoji} {speaker_label} ", style=speaker_style)
        header.append(f"[Turn {turn.turn}]", style="dim")
        header.append(f" • {turn.move_type}", style="italic")

        # Utterance
        utterance_text = Text(f'"{turn.utterance}"', style="white")

        # Build panel content
        content_parts = [utterance_text]

        # Business explanation
        if self.show_explanations and turn.business_explanation:
            content_parts.append(Text())  # Blank line
            content_parts.append(Text("💡 Business: ", style="bold yellow"))
            content_parts.append(Text(turn.business_explanation, style="yellow"))

        # Larsson rule
        if self.show_larsson_rules and turn.larsson_rule:
            content_parts.append(Text())
            content_parts.append(Text("📚 Larsson: ", style="bold cyan"))
            content_parts.append(Text(turn.larsson_rule, style="cyan"))

        # State changes
        if self.show_state_changes and turn.state_changes:
            content_parts.append(Text())
            content_parts.append(Text("🔄 State Changes:", style="bold magenta"))
            for key, value in turn.state_changes.items():
                formatted_key = key.replace("_", " ").title()
                content_parts.append(Text(f"  • {formatted_key}: {value}", style="magenta"))

        # Payoff indicator
        if turn.is_payoff:
            content_parts.append(Text())
            content_parts.append(Text("⭐ High-Value Output", style="bold yellow on black"))

        # Combine content
        panel_content = Text()
        for i, part in enumerate(content_parts):
            if i > 0 and part.plain == "":
                panel_content.append("\n")
            else:
                panel_content.append(part)
                if i < len(content_parts) - 1:
                    panel_content.append("\n")

        # Display panel
        self.console.print(
            Panel(
                panel_content,
                title=header,
                border_style=border_style,
                padding=(1, 2),
            )
        )

    def _display_summary(self) -> None:
        """Display scenario summary and metrics."""
        self.console.print("\n" + "═" * 80 + "\n")
        self.console.print("[bold green]✓ Scenario Complete[/bold green]\n")

        # Statistics
        stats_table = Table(show_header=False, box=None, padding=(0, 2))
        stats_table.add_column("Metric", style="bold")
        stats_table.add_column("Value", style="cyan")

        stats_table.add_row("Total Turns", str(self.scenario.total_turns))
        stats_table.add_row("User Turns", str(len(self.scenario.user_turns)))
        stats_table.add_row("System Turns", str(len(self.scenario.system_turns)))
        stats_table.add_row("Payoff Turns", str(len(self.scenario.payoff_turns)))

        self.console.print(stats_table)

        # Quality metrics
        if self.show_metrics and self.scenario.metadata.metrics:
            self.console.print("\n[bold yellow]Quality Metrics:[/bold yellow]")
            for key, value in self.scenario.metadata.metrics.items():
                formatted_key = key.replace("_", " ").title()
                self.console.print(f"  • {formatted_key}: {value}")

        self.console.print()


def run_scenario(
    scenario_id: str,
    mode: ExecutionMode = ExecutionMode.AUTO,
    auto_delay: float = 2.0,
    show_explanations: bool = True,
    show_state_changes: bool = True,
    show_larsson_rules: bool = True,
    show_metrics: bool = True,
) -> None:
    """Convenience function to run a scenario by ID.

    Args:
        scenario_id: Scenario identifier
        mode: Execution mode (STEP, AUTO, or REPLAY)
        auto_delay: Delay between turns in AUTO mode (seconds)
        show_explanations: Show business explanations
        show_state_changes: Show state changes
        show_larsson_rules: Show Larsson rule references
        show_metrics: Show scenario metrics

    Examples:
        >>> # Run with defaults
        >>> run_scenario("nda_basic")

        >>> # Run in step mode
        >>> run_scenario("nda_basic", mode=ExecutionMode.STEP)

        >>> # Run with minimal output
        >>> run_scenario("nda_basic", show_explanations=False, show_state_changes=False)
    """
    loader = ScenarioLoader()
    scenario = loader.load_scenario(scenario_id)

    controller = ExecutionController(
        mode=mode,
        auto_delay=auto_delay,
    )

    runner = ScenarioRunner(
        scenario=scenario,
        controller=controller,
        show_explanations=show_explanations,
        show_state_changes=show_state_changes,
        show_larsson_rules=show_larsson_rules,
        show_metrics=show_metrics,
    )

    runner.run()
