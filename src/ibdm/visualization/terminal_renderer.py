"""Beautiful terminal rendering of dialogue state using Rich library.

Provides rich, colorful terminal visualization of:
- InformationState (QUD, commitments, plans, agenda, etc.)
- StateDiff (changes between states with highlighting)
- RuleTrace (rule execution with precondition/effect visualization)

Based on Rich library for panels, tables, syntax highlighting, and colors.
"""

from typing import Any

from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from ibdm.core import DialogueMove, InformationState, Question
from ibdm.visualization import ChangedField, ChangeType, RuleTrace, StateDiff, StateSnapshot


class TerminalRenderer:
    """Rich-based terminal renderer for dialogue state visualization.
    
    Renders InformationState, StateDiff, and RuleTrace objects with beautiful
    formatting, colors, and structure for terminal display.
    """

    def __init__(self, console: Console | None = None, width: int = 120):
        """Initialize renderer.
        
        Args:
            console: Rich console to use (creates new one if None)
            width: Maximum rendering width
        """
        self.console = console or Console(width=width)
        self.width = width

    def render_state(self, state: InformationState, title: str = "Information State") -> Panel:
        """Render complete information state as a Rich panel.
        
        Args:
            state: Information state to render
            title: Panel title
            
        Returns:
            Rich Panel containing formatted state
        """
        sections = []
        
        # Shared state section
        shared_table = self._render_shared_state(state.shared)
        sections.append(Panel(shared_table, title="[bold cyan]Shared State", border_style="cyan"))
        
        # Private state section
        private_table = self._render_private_state(state.private)
        sections.append(Panel(private_table, title="[bold yellow]Private State", border_style="yellow"))
        
        # Control section
        control_text = self._render_control_state(state.control)
        sections.append(Panel(control_text, title="[bold green]Control", border_style="green"))
        
        group = Group(*sections)
        return Panel(group, title=f"[bold white]{title}", border_style="white")

    def _render_shared_state(self, shared: Any) -> Table:
        """Render shared information state fields."""
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="bold")
        table.add_column("Value")
        
        # QUD
        qud_text = self._format_question_list(shared.qud) if shared.qud else Text("[]", style="dim")
        table.add_row("QUD", qud_text)
        
        # Commitments
        commitments_text = Text(f"{list(shared.commitments)}" if shared.commitments else "[]")
        table.add_row("Commitments", commitments_text)
        
        # Last moves
        last_moves_text = self._format_move_list(shared.last_moves) if shared.last_moves else Text("[]", style="dim")
        table.add_row("Last Moves", last_moves_text)
        
        # Move history count
        move_count = Text(str(len(shared.moves)))
        table.add_row("Moves", move_count)
        
        # Next moves
        next_moves_text = self._format_move_list(shared.next_moves) if shared.next_moves else Text("[]", style="dim")
        table.add_row("Next Moves", next_moves_text)
        
        # Actions
        action_count = Text(str(len(shared.actions)))
        table.add_row("Actions", action_count)
        
        return table

    def _render_private_state(self, private: Any) -> Table:
        """Render private information state fields."""
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="bold")
        table.add_column("Value")
        
        # Plan
        plan_text = self._format_plan_list(private.plan) if private.plan else Text("[]", style="dim")
        table.add_row("Plan", plan_text)
        
        # Agenda
        agenda_text = self._format_move_list(private.agenda) if private.agenda else Text("[]", style="dim")
        table.add_row("Agenda", agenda_text)
        
        # Issues
        issues_text = self._format_question_list(private.issues) if private.issues else Text("[]", style="dim")
        table.add_row("Issues", issues_text)
        
        # Beliefs (show count and sample)
        if private.beliefs:
            beliefs_text = Text(f"{len(private.beliefs)} beliefs")
            # Show first few beliefs
            sample = list(private.beliefs.items())[:3]
            for k, v in sample:
                beliefs_text.append(f"\n  • {k}: {v}", style="dim")
            if len(private.beliefs) > 3:
                beliefs_text.append(f"\n  ... ({len(private.beliefs) - 3} more)", style="dim italic")
        else:
            beliefs_text = Text("{}", style="dim")
        table.add_row("Beliefs", beliefs_text)
        
        # Overridden questions
        overridden_count = Text(str(len(private.overridden_questions)))
        table.add_row("Overridden", overridden_count)
        
        # Actions
        action_count = Text(str(len(private.actions)))
        table.add_row("Actions", action_count)
        
        return table

    def _render_control_state(self, control: Any) -> Text:
        """Render control state fields."""
        text = Text()
        text.append(f"Speaker: ", style="bold")
        text.append(f"{control.speaker}\n")
        text.append(f"Next: ", style="bold")
        text.append(f"{control.next_speaker}\n")
        text.append(f"Initiative: ", style="bold")
        text.append(f"{control.initiative}\n")
        text.append(f"State: ", style="bold")
        text.append(control.dialogue_state, style="green" if control.dialogue_state == "active" else "yellow")
        return text

    def _format_question_list(self, questions: list[Question]) -> Text:
        """Format list of questions."""
        text = Text()
        for i, q in enumerate(questions):
            if i > 0:
                text.append("\n")
            text.append(f"  {i+1}. ", style="dim")
            text.append(str(q), style="cyan")
        return text

    def _format_move_list(self, moves: list[DialogueMove]) -> Text:
        """Format list of dialogue moves."""
        text = Text()
        for i, move in enumerate(moves):
            if i > 0:
                text.append("\n")
            text.append(f"  {i+1}. ", style="dim")
            
            # Color by speaker
            speaker_style = "yellow" if move.speaker == "system" else "blue"
            text.append(f"{move.speaker}:", style=speaker_style)
            text.append(f"{move.move_type} ", style="bold")
            
            # Show content summary
            content_str = str(move.content)[:50]
            if len(str(move.content)) > 50:
                content_str += "..."
            text.append(content_str, style="dim")
        return text

    def _format_plan_list(self, plans: list[Any]) -> Text:
        """Format list of plans."""
        text = Text()
        for i, plan in enumerate(plans):
            if i > 0:
                text.append("\n")
            text.append(f"  {i+1}. ", style="dim")
            text.append(f"{plan.plan_type}", style="magenta")
            status = "✓" if not plan.is_active() else "○"
            text.append(f" {status}", style="green" if not plan.is_active() else "yellow")
        return text

    def render_diff(self, diff: StateDiff, title: str = "State Changes") -> Panel:
        """Render state diff with change highlighting.
        
        Args:
            diff: State diff to render
            title: Panel title
            
        Returns:
            Rich Panel containing formatted diff
        """
        if not diff.has_changes():
            return Panel(
                Text("No changes", style="dim italic"),
                title=f"[bold white]{title}",
                border_style="dim"
            )
        
        # Create table for changes
        table = Table(show_header=True, box=None)
        table.add_column("Field", style="bold cyan")
        table.add_column("Change", style="yellow")
        table.add_column("Details")
        
        for field_name in sorted(diff.changed_field_names()):
            changed = diff.get_changed_field(field_name)
            if changed and changed.has_changes():
                change_text = self._format_change(changed)
                details_text = self._format_change_details(changed)
                table.add_row(field_name, change_text, details_text)
        
        summary = Text(diff.format_summary(), style="bold")
        group = Group(summary, "", table)
        
        return Panel(
            group,
            title=f"[bold white]{title}",
            subtitle=f"t{diff.before.timestamp} → t{diff.after.timestamp}",
            border_style="yellow"
        )

    def _format_change(self, changed: ChangedField) -> Text:
        """Format change type indicator."""
        change_map = {
            ChangeType.ADDED: ("+ ADDED", "green"),
            ChangeType.REMOVED: ("- REMOVED", "red"),
            ChangeType.MODIFIED: ("~ MODIFIED", "yellow"),
            ChangeType.UNCHANGED: ("= UNCHANGED", "dim"),
        }
        label, style = change_map.get(changed.change_type, ("?", "white"))
        return Text(label, style=style)

    def _format_change_details(self, changed: ChangedField) -> Text:
        """Format detailed change information."""
        text = Text()
        
        # Added items
        if changed.added_items:
            text.append(f"+{len(changed.added_items)} ", style="green")
        
        # Removed items
        if changed.removed_items:
            text.append(f"-{len(changed.removed_items)} ", style="red")
        
        # Modified items
        if changed.modified_items:
            text.append(f"~{len(changed.modified_items)} ", style="yellow")
        
        # Summary
        if changed.summary:
            text.append(f"({changed.summary})", style="dim")
        
        return text

    def render_rule_trace(self, trace: RuleTrace, title: str = "Rule Execution") -> Panel:
        """Render rule execution trace.
        
        Args:
            trace: Rule trace to render
            title: Panel title
            
        Returns:
            Rich Panel containing formatted trace
        """
        sections = []
        
        # Header with summary
        summary_text = Text()
        summary_text.append(f"Phase: ", style="bold")
        summary_text.append(f"{trace.phase}\n", style="cyan")
        summary_text.append(f"Selected: ", style="bold")
        summary_text.append(f"{trace.selected_rule or 'none'}\n", style="green" if trace.selected_rule else "dim")
        summary_text.append(f"Evaluated: ", style="bold")
        summary_text.append(f"{trace.rules_evaluated()} rules\n")
        summary_text.append(f"Ready: ", style="bold")
        summary_text.append(f"{trace.rules_with_met_preconditions()} rules")
        sections.append(summary_text)
        
        # Rule evaluations
        if trace.evaluations:
            sections.append(Text("\n"))
            eval_tree = Tree("📋 Rule Evaluations")
            for eval in trace.evaluations:
                status_icon = "✓" if eval.preconditions_met else "✗"
                status_style = "green" if eval.preconditions_met else "red"
                selected_marker = " 🎯 [SELECTED]" if eval.was_selected else ""
                
                label = Text()
                label.append(f"{status_icon} ", style=status_style)
                label.append(f"{eval.rule_name}", style="bold" if eval.was_selected else "")
                label.append(f" (p={eval.priority})", style="dim")
                label.append(selected_marker, style="bold green")
                
                node = eval_tree.add(label)
                if eval.reason:
                    node.add(Text(eval.reason, style="dim italic"))
            
            sections.append(eval_tree)
        
        # State diff if available
        if trace.diff and trace.diff.has_changes():
            sections.append(Text("\n"))
            sections.append(Text("State Changes:", style="bold underline"))
            sections.append(Text(trace.diff.format_summary(), style="yellow"))
        
        group = Group(*sections)
        return Panel(
            group,
            title=f"[bold white]{title}",
            subtitle=f"t={trace.timestamp}",
            border_style="magenta"
        )

    def print_state(self, state: InformationState, title: str = "Information State") -> None:
        """Print information state to console.
        
        Args:
            state: Information state to print
            title: Title for the output
        """
        panel = self.render_state(state, title)
        self.console.print(panel)

    def print_diff(self, diff: StateDiff, title: str = "State Changes") -> None:
        """Print state diff to console.
        
        Args:
            diff: State diff to print
            title: Title for the output
        """
        panel = self.render_diff(diff, title)
        self.console.print(panel)

    def print_rule_trace(self, trace: RuleTrace, title: str = "Rule Execution") -> None:
        """Print rule trace to console.
        
        Args:
            trace: Rule trace to print
            title: Title for the output
        """
        panel = self.render_rule_trace(trace, title)
        self.console.print(panel)
