"""HTML export for state visualization.

Provides functionality to export StateSnapshot and StateDiff objects to HTML
for documentation and sharing purposes.
"""

import html
from typing import Any

from ibdm.visualization.rule_trace import RuleTrace
from ibdm.visualization.state_diff import ChangedField, StateDiff
from ibdm.visualization.state_snapshot import StateSnapshot


class HtmlExporter:
    """Exports state snapshots and diffs to HTML."""

    CSS = """
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        line-height: 1.6;
        color: #333;
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        background: #f5f5f7;
    }
    .snapshot {
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        padding: 20px;
        margin-bottom: 20px;
    }
    .header {
        border-bottom: 1px solid #eee;
        padding-bottom: 10px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .title { font-size: 1.2em; font-weight: 600; margin: 0; }
    .meta { font-size: 0.9em; color: #666; display: flex; gap: 10px; align-items: center; }
    .timestamp { background: #eee; padding: 2px 8px; border-radius: 4px; font-family: monospace; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
    @media (max-width: 768px) { .grid { grid-template-columns: 1fr; } }
    .section {
        border: 1px solid #eee;
        border-radius: 6px;
        padding: 15px;
        background: #fafafa;
    }
    .section h3 {
        margin-top: 0;
        font-size: 0.85em;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #666;
        border-bottom: 2px solid #ddd;
        padding-bottom: 5px;
        margin-bottom: 10px;
    }
    .item-list { list-style: none; padding: 0; margin: 0; }
    .item-list li {
        padding: 6px 8px;
        border-bottom: 1px solid #eee;
        font-family: "SF Mono", Consolas, "Liberation Mono", Menlo, monospace;
        font-size: 0.9em;
        word-break: break-word;
        background: white;
    }
    .item-list li:last-child { border-bottom: none; }
    .empty { color: #999; font-style: italic; padding: 5px; }

    /* Diff Styles */
    .diff-added {
        background-color: #e6fffa !important;
        border-left: 3px solid #38b2ac;
        color: #004d40;
    }
    .diff-removed {
        background-color: #fff5f5 !important;
        border-left: 3px solid #fc8181;
        color: #9b2c2c;
        text-decoration: line-through;
        opacity: 0.7;
    }
    .diff-modified {
        background-color: #fffbea !important;
        border-left: 3px solid #f6e05e;
        color: #744210;
    }
    .change-tag {
        display: inline-block;
        font-size: 0.75em;
        padding: 1px 5px;
        border-radius: 3px;
        margin-right: 6px;
        text-transform: uppercase;
        font-weight: bold;
    }
    .tag-added { background: #38b2ac; color: white; }
    .tag-removed { background: #fc8181; color: white; }
    .tag-modified { background: #f6e05e; color: #744210; }

    /* Syntax Highlighting for JSON/Objects */
    .key { color: #555; font-weight: 600; }
    .string { color: #22863a; }
    .number { color: #005cc5; }
    .boolean { color: #005cc5; }
    .null { color: #005cc5; }

    /* Rule Trace Styles */
    .rule-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.9em;
    }
    .rule-table th {
        text-align: left;
        padding: 8px;
        background: #f8f9fa;
        border-bottom: 2px solid #dee2e6;
        color: #666;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.8em;
    }
    .rule-table td {
        padding: 8px;
        border-bottom: 1px solid #eee;
    }
    .rule-table tr:last-child td {
        border-bottom: none;
    }

    .rule-selected { background-color: #e6fffa; font-weight: 600; }
    .rule-met { color: #333; }
    .rule-unmet { color: #999; }

    .col-status { width: 30px; text-align: center; font-weight: bold; }
    .col-priority { width: 40px; text-align: center; color: #666; font-family: monospace; }
    .col-name { font-family: monospace; }
    .col-selected {
        width: 30px;
        text-align: center;
        color: #38b2ac;
        font-weight: bold;
        font-size: 1.2em;
    }
    .col-reason { color: #666; font-style: italic; font-size: 0.9em; }

    .trace-header {
        padding: 10px 15px;
        border-radius: 6px;
        margin-bottom: 15px;
        font-weight: 600;
        display: inline-block;
    }
    .trace-success { background-color: #e6fffa; color: #004d40; border: 1px solid #b2f5ea; }
    .trace-warning { background-color: #fffaf0; color: #744210; border: 1px solid #fbd38d; }
    .stats {
        background: #eee;
        padding: 2px 8px;
        border-radius: 4px;
        font-family: monospace;
        margin-left: 10px;
    }

    /* Collapsible Timeline Styles */
    details.timeline-step {
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        overflow: hidden;
    }
    details.timeline-step summary {
        padding: 15px 20px;
        cursor: pointer;
        background: #fff;
        border-bottom: 1px solid #eee;
        font-weight: 600;
        list-style: none;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    details.timeline-step summary::-webkit-details-marker {
        display: none;
    }
    details.timeline-step summary:hover {
        background: #f8f9fa;
    }
    details.timeline-step[open] summary {
        background: #f8f9fa;
        border-bottom: 1px solid #e0e0e0;
    }
    .step-header {
        display: flex;
        align-items: center;
        gap: 15px;
        flex-grow: 1;
    }
    .step-marker {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: #38b2ac;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.8em;
        font-weight: bold;
    }
    .step-title {
        font-size: 1.1em;
        color: #333;
    }
    .step-meta {
        font-size: 0.9em;
        color: #666;
        font-family: monospace;
    }
    .step-content {
        padding: 20px;
        border-top: 1px solid #eee;
    }
    /* Nest the existing snapshot styles inside the details */
    details.timeline-step .snapshot {
        box-shadow: none;
        margin-bottom: 0;
        padding: 0;
    }
    """

    def export_snapshot(self, snapshot: StateSnapshot, title: str | None = None) -> str:
        """Export a single state snapshot to HTML.

        Args:
            snapshot: The state snapshot to export
            title: Optional title for the page (defaults to snapshot label)

        Returns:
            Complete HTML document string
        """
        content = self._render_snapshot(snapshot)
        page_title = title or f"State Snapshot: {snapshot.label}"
        return self._wrap_page(content, page_title)

    def export_diff(self, diff: StateDiff, title: str | None = None) -> str:
        """Export a state diff to HTML.

        Args:
            diff: The state diff to export
            title: Optional title for the page

        Returns:
            Complete HTML document string
        """
        content = self._render_diff(diff)
        page_title = title or f"State Change: {diff.summary}"
        return self._wrap_page(content, page_title)

    def export_timeline(
        self, snapshots: list[StateSnapshot], title: str = "Dialogue Timeline"
    ) -> str:
        """Export a sequence of snapshots as a timeline with collapsible history.

        Args:
            snapshots: List of state snapshots
            title: Title for the timeline page

        Returns:
            Complete HTML document string
        """
        content_parts = []

        # Create diffs between consecutive snapshots
        from ibdm.visualization.diff_engine import DiffEngine

        diff_engine = DiffEngine()

        if snapshots:
            # Process each snapshot
            for i, snapshot in enumerate(snapshots):
                # Determine content (Diff or Full Snapshot)
                # For the first item, always show full snapshot
                # For subsequent items, if there are changes, show Diff + Full Snapshot inside

                step_content = ""
                summary_text = snapshot.label or f"Step {i + 1}"

                if i > 0:
                    prev = snapshots[i - 1]
                    diff = diff_engine.compute_diff(prev, snapshot)

                    if diff.has_changes():
                        # Show the diff view
                        step_content = self._render_diff(diff)
                        # Append summary of changes to title
                        summary_text += f" ({diff.summary})"
                    else:
                        # No changes, just show snapshot
                        step_content = self._render_snapshot(snapshot)
                else:
                    # First snapshot
                    step_content = self._render_snapshot(snapshot)

                # Wrap in collapsible details
                # Open by default if it's the last item
                is_open = i == len(snapshots) - 1
                open_attr = " open" if is_open else ""

                content_parts.append(f"""
                <details class="timeline-step"{open_attr}>
                    <summary>
                        <div class="step-header">
                            <div class="step-marker">{i + 1}</div>
                            <div class="step-title">{html.escape(summary_text)}</div>
                        </div>
                        <div class="step-meta">t={snapshot.timestamp}</div>
                    </summary>
                    <div class="step-content">
                        {step_content}
                    </div>
                </details>
                """)

        return self._wrap_page("\n".join(content_parts), title)

    def _wrap_page(self, content: str, title: str) -> str:
        """Wrap content in HTML boilerplate."""
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{html.escape(title)}</title>
    <style>{self.CSS}</style>
</head>
<body>
    <h1>{html.escape(title)}</h1>
    {content}
</body>
</html>"""

    def _render_snapshot(self, snapshot: StateSnapshot) -> str:
        """Render a snapshot as an HTML component."""
        qud_section = self._render_section("QUD (Questions Under Discussion)", snapshot.qud)
        commitments_section = self._render_section("Commitments", snapshot.commitments)
        agenda_section = self._render_section("Agenda", snapshot.agenda)
        plan_section = self._render_section("Plan", snapshot.plan)
        issues_section = self._render_section("Private Issues", snapshot.issues)
        beliefs_section = self._render_dict_section("Beliefs", snapshot.beliefs)
        last_move = self._render_last_move(snapshot.last_move)

        return f"""
        <div class="snapshot">
            <div class="header">
                <h2 class="title">{html.escape(snapshot.label)}</h2>
                <div class="meta">
                    <span class="timestamp">t={snapshot.timestamp}</span>
                    <span class="agent">Agent: {html.escape(snapshot.agent_id)}</span>
                </div>
            </div>

            <div class="grid">
                <!-- Shared State -->
                <div class="column">
                    {qud_section}
                    {commitments_section}
                </div>

                <!-- Private State -->
                <div class="column">
                    {agenda_section}
                    {plan_section}
                    {issues_section}
                    {beliefs_section}
                </div>
            </div>

            <div class="footer">
                {last_move}
            </div>
        </div>
        """

    def _render_diff(self, diff: StateDiff) -> str:
        """Render a diff as an HTML component."""
        snapshot = diff.after

        qud = self._render_diff_section("QUD", snapshot.qud, diff.get_changed_field("qud"))
        commitments = self._render_diff_section(
            "Commitments", snapshot.commitments, diff.get_changed_field("commitments")
        )
        agenda = self._render_diff_section(
            "Agenda", snapshot.agenda, diff.get_changed_field("agenda")
        )
        plan = self._render_diff_section("Plan", snapshot.plan, diff.get_changed_field("plan"))
        issues = self._render_diff_section(
            "Private Issues", snapshot.issues, diff.get_changed_field("issues")
        )
        beliefs = self._render_diff_dict_section(
            "Beliefs", snapshot.beliefs, diff.get_changed_field("beliefs")
        )

        return f"""
        <div class="snapshot diff-view">
            <div class="header">
                <h2 class="title">
                    <span class="change-tag tag-modified">Change</span>
                    {html.escape(diff.summary)}
                </h2>
                <div class="meta">
                    <span class="timestamp">t={snapshot.timestamp}</span>
                </div>
            </div>

            <div class="grid">
                <!-- Shared State -->
                <div class="column">
                    {qud}
                    {commitments}
                </div>

                <!-- Private State -->
                <div class="column">
                    {agenda}
                    {plan}
                    {issues}
                    {beliefs}
                </div>
            </div>
        </div>
        """

    def _render_section(self, title: str, items: tuple | list) -> str:
        """Render a standard list section."""
        content = ""
        if not items:
            content = '<div class="empty">Empty</div>'
        else:
            lis = []
            for item in items:
                lis.append(f"<li>{html.escape(str(item))}</li>")
            content = f'<ul class="item-list">{"".join(lis)}</ul>'

        return f"""
        <div class="section">
            <h3>{title}</h3>
            {content}
        </div>
        """

    def _render_dict_section(self, title: str, data: dict) -> str:
        """Render a dictionary section."""
        content = ""
        if not data:
            content = '<div class="empty">Empty</div>'
        else:
            lis = []
            for k, v in data.items():
                k_esc = html.escape(str(k))
                v_esc = html.escape(str(v))
                lis.append(f'<li><span class="key">{k_esc}:</span> {v_esc}</li>')
            content = f'<ul class="item-list">{"".join(lis)}</ul>'

        return f"""
        <div class="section">
            <h3>{title}</h3>
            {content}
        </div>
        """

    def _render_diff_section(
        self, title: str, current_items: tuple | list, changed_field: ChangedField | None
    ) -> str:
        """Render a section with diff highlighting."""
        if not changed_field or not changed_field.has_changes():
            return self._render_section(title, current_items)

        lis = []
        added_set = list(changed_field.added_items)

        for item in current_items:
            is_added = False
            if item in added_set:
                is_added = True
                added_set.remove(item)

            class_attr = ' class="diff-added"' if is_added else ""
            lis.append(f"<li{class_attr}>{html.escape(str(item))}</li>")

        for item in changed_field.removed_items:
            lis.append(f'<li class="diff-removed">{html.escape(str(item))}</li>')

        content = f'<ul class="item-list">{"".join(lis)}</ul>'

        return f"""
        <div class="section">
            <h3>{title} <span class="change-tag tag-modified">Changed</span></h3>
            {content}
        </div>
        """

    def _render_diff_dict_section(
        self, title: str, current_data: dict, changed_field: ChangedField | None
    ) -> str:
        """Render a dict section with diff highlighting."""
        if not changed_field or not changed_field.has_changes():
            return self._render_dict_section(title, current_data)

        lis = []

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

            class_attr = ""
            if is_added:
                class_attr = ' class="diff-added"'
            elif is_modified:
                class_attr = ' class="diff-modified"'

            k_esc = html.escape(str(k))
            v_esc = html.escape(str(v))
            lis.append(f'<li{class_attr}><span class="key">{k_esc}:</span> {v_esc}</li>')

        for item in changed_field.removed_items:
            lis.append(f'<li class="diff-removed">{html.escape(str(item))}</li>')

        content = f'<ul class="item-list">{"".join(lis)}</ul>'

        return f"""
        <div class="section">
            <h3>{title} <span class="change-tag tag-modified">Changed</span></h3>
            {content}
        </div>
        """

    def _render_last_move(self, move: Any) -> str:
        """Render the last move section."""
        if not move:
            return ""
        style = "margin-top: 20px; border-color: #b3d4fc; background: #e8f0fe;"
        h3_style = "color: #1a73e8; border-color: #b3d4fc;"
        return f"""
        <div class="section" style="{style}">
            <h3 style="{h3_style}">Last Move</h3>
            <div style="font-family: monospace;">{html.escape(str(move))}</div>
        </div>
        """

    def export_rule_trace(self, trace: RuleTrace, title: str | None = None) -> str:
        """Export a rule trace to HTML.

        Args:
            trace: The rule trace to export
            title: Optional title for the page

        Returns:
            Complete HTML document string
        """
        content = self._render_rule_trace(trace)
        page_title = title or f"Rule Trace: {trace.phase}"
        return self._wrap_page(content, page_title)

    def _render_rule_trace(self, trace: RuleTrace) -> str:
        """Render a rule trace as an HTML component."""
        # 1. Summary Header
        summary_class = "trace-header"
        if trace.selected_rule:
            summary_text = f"Selected: {trace.selected_rule}"
            status_class = "trace-success"
        else:
            summary_text = "No rule selected"
            status_class = "trace-warning"

        # 2. Rule Evaluations Table
        rows = []
        for eval in trace.evaluations:
            row_class = ""
            if eval.was_selected:
                row_class = "rule-selected"
            elif eval.preconditions_met:
                row_class = "rule-met"
            else:
                row_class = "rule-unmet"

            status_icon = "✓" if eval.preconditions_met else "✗"
            selected_icon = "★" if eval.was_selected else ""

            rows.append(f"""
            <tr class="{row_class}">
                <td class="col-status">{status_icon}</td>
                <td class="col-priority">{eval.priority}</td>
                <td class="col-name">{html.escape(eval.rule_name)}</td>
                <td class="col-selected">{selected_icon}</td>
                <td class="col-reason">{html.escape(eval.reason)}</td>
            </tr>
            """)

        evaluations_table = f"""
        <table class="rule-table">
            <thead>
                <tr>
                    <th class="col-status">Met</th>
                    <th class="col-priority">Pri</th>
                    <th class="col-name">Rule Name</th>
                    <th class="col-selected">Sel</th>
                    <th class="col-reason">Reason</th>
                </tr>
            </thead>
            <tbody>
                {"".join(rows)}
            </tbody>
        </table>
        """

        # 3. State Changes (Diff)
        diff_html = ""
        if trace.diff and trace.diff.has_changes():
            diff_html = self._render_diff(trace.diff)
        else:
            diff_html = '<div class="no-changes">No state changes</div>'

        return f"""
        <div class="rule-trace">
            <div class="header">
                <h2 class="title">Phase: {html.escape(trace.phase)}</h2>
                <div class="{summary_class} {status_class}">
                    {html.escape(summary_text)}
                </div>
                <div class="meta">
                    <span class="timestamp">t={trace.timestamp}</span>
                    <span class="stats">{trace.rules_with_met_preconditions()}/{trace.rules_evaluated()} met</span>
                </div>
            </div>

            <div class="section">
                <h3>Rule Evaluations</h3>
                {evaluations_table}
            </div>

            <div class="section">
                <h3>Effects</h3>
                {diff_html}
            </div>
        </div>
        """
