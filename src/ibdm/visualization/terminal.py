from typing import Any

from rich.columns import Columns
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from ibdm.visualization.state_diff import ChangedField, StateDiff
from ibdm.visualization.state_snapshot import StateSnapshot


class TerminalVisualizer:
    """Visualizes IBDM states in the terminal using Rich."""

    def __init__(self, console: Console | None = None):
        """Initialize visualizer.

        Args:
            console: Optional Rich Console instance. If None, creates a new one.
        """
        self.console = console or Console()

    def render_snapshot(self, snapshot: StateSnapshot) -> None:
        """Render a state snapshot to the console.

        Args:
            snapshot: The state snapshot to render
        """
        # Create main layout
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body", ratio=1),
            Layout(name="footer", size=3)
        )

        # Header
        header_text = Text(
            f"{snapshot.label} (t={snapshot.timestamp})",
            style="bold white on blue",
            justify="center"
        )
        layout["header"].update(Panel(header_text, style="blue"))

        # Body - Split into Shared and Private
        layout["body"].split_row(
            Layout(name="shared"),
            Layout(name="private")
        )

        # Shared State Column
        shared_content = self._render_shared_state(snapshot)
        layout["shared"].update(Panel(shared_content, title="Shared State", border_style="green"))

        # Private State Column
        private_content = self._render_private_state(snapshot)
        layout["private"].update(
            Panel(private_content, title="Private State", border_style="yellow")
        )

        # Footer - Last Move
        last_move_str = str(snapshot.last_move) if snapshot.last_move else "None"
        layout["footer"].update(
            Panel(Text(f"Last Move: {last_move_str}", style="italic"), style="white")
        )

        self.console.print(layout)

    def render_diff(self, diff: StateDiff) -> None:
        """Render a state diff to the console.

        Args:
            diff: The state diff to render
        """
        snapshot = diff.after
        title = f"State Change: {diff.summary}"

        # Create main layout
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body", ratio=1)
        )

        layout["header"].update(
            Panel(Text(title, style="bold white on magenta", justify="center"))
        )

        # Body
        layout["body"].split_row(
            Layout(name="shared"),
            Layout(name="private")
        )

        # Shared State with Diff
        shared_content = self._render_shared_diff(snapshot, diff)
        layout["shared"].update(Panel(shared_content, title="Shared State", border_style="green"))

        # Private State with Diff
        private_content = self._render_private_diff(snapshot, diff)
        layout["private"].update(
            Panel(private_content, title="Private State", border_style="yellow")
        )

        self.console.print(layout)

    def _render_shared_state(self, snapshot: StateSnapshot) -> Any:
        """Render shared state components."""
        # QUD
        qud_table = Table(
            title="QUD (Questions Under Discussion)", show_header=False, box=None, expand=True
        )
        if not snapshot.qud:
            qud_table.add_row(Text("(Empty)", style="dim"))
        else:
            # Show top of stack at top for readability? Or bottom?
            # Larsson diagrams usually show stack growing upwards.
            # Let's list them with top first (LIFO view)
            for i, q in enumerate(reversed(snapshot.qud)):
                prefix = "►" if i == 0 else " "
                style = "bold cyan" if i == 0 else "cyan"
                qud_table.add_row(Text(f"{prefix} {str(q)}", style=style))

        # Commitments
        com_table = Table(title="Commitments", show_header=False, box=None, expand=True)
        if not snapshot.commitments:
            com_table.add_row(Text("(None)", style="dim"))
        else:
            for c in list(snapshot.commitments):
                com_table.add_row(Text(f"✓ {str(c)}", style="green"))

        return Columns([qud_table, com_table], expand=True)

    def _render_private_state(self, snapshot: StateSnapshot) -> Any:
        """Render private state components."""
        # Plan Tree
        plan_tree = Tree("Plans")
        if not snapshot.plan:
            plan_tree.add(Text("(No active plans)", style="dim"))
        else:
            for plan in snapshot.plan:
                self._add_plan_node(plan_tree, plan)

        # Agenda
        agenda_table = Table(title="Agenda", show_header=False, box=None, expand=True)
        if not snapshot.agenda:
            agenda_table.add_row(Text("(Empty)", style="dim"))
        else:
            for move in snapshot.agenda:
                agenda_table.add_row(Text(f"• {str(move)}", style="yellow"))

        # Issues
        issues_table = Table(title="Private Issues", show_header=False, box=None, expand=True)
        if not snapshot.issues:
            issues_table.add_row(Text("(Empty)", style="dim"))
        else:
            for issue in snapshot.issues:
                issues_table.add_row(Text(f"? {str(issue)}", style="magenta"))

        # Beliefs (collapsed view)
        beliefs_table = Table(title="Beliefs", show_header=False, box=None, expand=True)
        if not snapshot.beliefs:
            beliefs_table.add_row(Text("(Empty)", style="dim"))
        else:
            for k, v in snapshot.beliefs.items():
                beliefs_table.add_row(Text(f"{k}: {v}", style="white"))

        return Columns(
            [plan_tree, agenda_table, issues_table, beliefs_table], expand=True, equal=False
        )

    def _add_plan_node(self, tree: Tree, plan: Any) -> None:
        """Recursively add plan nodes to the tree."""
        # Handle Plan objects or deserialized dicts/strings
        # Assuming Plan object or similar interface
        plan_type = getattr(plan, "plan_type", "unknown")
        content = getattr(plan, "content", str(plan))

        node_text = Text(f"{plan_type}({content})", style="bold blue")
        sub_node = tree.add(node_text)

        subplans = getattr(plan, "subplans", [])
        for subplan in subplans:
            self._add_plan_node(sub_node, subplan)

    def _render_shared_diff(self, snapshot: StateSnapshot, diff: StateDiff) -> Any:
        """Render shared state with diff highlighting."""
        # QUD Diff
        qud_table = Table(title="QUD", show_header=False, box=None, expand=True)
        self._add_diff_rows(qud_table, snapshot.qud, diff.get_changed_field("qud"))

        # Commitments Diff
        com_table = Table(title="Commitments", show_header=False, box=None, expand=True)
        self._add_diff_rows(
            com_table, snapshot.commitments, diff.get_changed_field("commitments")
        )

        return Columns([qud_table, com_table], expand=True)

    def _render_private_diff(self, snapshot: StateSnapshot, diff: StateDiff) -> Any:
        """Render private state with diff highlighting."""
        # Agenda Diff
        agenda_table = Table(title="Agenda", show_header=False, box=None, expand=True)
        self._add_diff_rows(agenda_table, snapshot.agenda, diff.get_changed_field("agenda"))

        # Issues Diff
        issues_table = Table(title="Private Issues", show_header=False, box=None, expand=True)
        self._add_diff_rows(issues_table, snapshot.issues, diff.get_changed_field("issues"))

        # Beliefs Diff
        beliefs_table = Table(title="Beliefs", show_header=False, box=None, expand=True)
        self._add_dict_diff_rows(
            beliefs_table, snapshot.beliefs, diff.get_changed_field("beliefs")
        )

        # Plan Diff (Tree is hard to diff row-by-row, simplified view)
        plan_tree = Tree("Plans")
        plan_change = diff.get_changed_field("plan")
        if plan_change and plan_change.has_changes():
            plan_tree = Tree(Text("Plans (Changed)", style="bold yellow"))

        if not snapshot.plan:
            plan_tree.add(Text("(No active plans)", style="dim"))
        else:
            for plan in snapshot.plan:
                self._add_plan_node(plan_tree, plan)

        return Columns(
            [plan_tree, agenda_table, issues_table, beliefs_table], expand=True, equal=False
        )

    def _add_diff_rows(
        self,
        table: Table,
        current_items: tuple[Any, ...] | list[Any],
        changed_field: ChangedField | None,
    ) -> None:
        """Add rows to a table with diff highlighting."""
        if not changed_field or not changed_field.has_changes():
            if not current_items:
                table.add_row(Text("(Empty)", style="dim"))
            else:
                for item in current_items:
                    table.add_row(str(item))
            return

        # Show added items
        added_set = list(changed_field.added_items)
        for item in current_items:
            if item in added_set:
                table.add_row(Text(f"+ {str(item)}", style="bold green"))
                added_set.remove(item)
            else:
                table.add_row(str(item))

        # Show removed items
        for item in changed_field.removed_items:
            table.add_row(Text(f"- {str(item)}", style="bold red strike"))

    def _add_dict_diff_rows(
        self, table: Table, current_data: dict[str, Any], changed_field: ChangedField | None
    ) -> None:
        """Add rows to a dictionary table with diff highlighting."""
        if not changed_field or not changed_field.has_changes():
            if not current_data:
                table.add_row(Text("(Empty)", style="dim"))
            else:
                for k, v in current_data.items():
                    table.add_row(f"{k}: {v}")
            return

        # Show added/modified items
        for k, v in current_data.items():
            item_str = f"{k}={v}"
            is_added = False
            is_modified = False

            if item_str in changed_field.added_items:
                is_added = True

            if not is_added:
                for _, new_str in changed_field.modified_items:
                    if new_str == item_str:
                        is_modified = True
                        break

            if is_added:
                table.add_row(Text(f"+ {k}: {v}", style="bold green"))
            elif is_modified:
                table.add_row(Text(f"~ {k}: {v}", style="bold yellow"))
            else:
                table.add_row(f"{k}: {v}")

        # Show removed items
        for item in changed_field.removed_items:
            # Item is "key=value"
            table.add_row(Text(f"- {str(item)}", style="bold red strike"))
