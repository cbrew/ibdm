"""SVG export for state visualization.

Provides functionality to export state components (like plans) to SVG
using Graphviz.
"""

import graphviz

from ibdm.core import Plan
from ibdm.visualization.state_snapshot import StateSnapshot


class SvgExporter:
    """Exports state components to SVG."""

    def export_plan_tree(self, snapshot: StateSnapshot) -> str:
        """Generate SVG string for the plan tree.

        Args:
            snapshot: The state snapshot containing plans

        Returns:
            SVG string of the plan tree
        """
        if not snapshot.plan:
            return (
                '<svg width="200" height="50">'
                '<text x="10" y="30" font-family="sans-serif">No active plans</text>'
                "</svg>"
            )

        dot = graphviz.Digraph(comment="Plan Tree")
        dot.attr(rankdir="TB")
        dot.attr(
            "node", shape="box", style="rounded,filled", fillcolor="white", fontname="sans-serif"
        )
        dot.attr("edge", fontname="sans-serif")

        # Add nodes and edges
        # Since snapshot.plan is a list/tuple of root plans
        for i, plan in enumerate(snapshot.plan):
            # Create a subgraph for each root plan to keep them somewhat separate
            with dot.subgraph(name=f"cluster_{i}") as c:
                c.attr(style="invis")
                root_id = f"root_{i}"
                self._add_plan_node(c, plan, root_id)

        try:
            return dot.pipe(format="svg").decode("utf-8")
        except Exception as e:
            # Fallback if graphviz is not installed or fails
            return (
                f'<div class="error">Error generating SVG: {str(e)}'
                "<br>Ensure graphviz is installed.</div>"
            )

    def _add_plan_node(self, dot: graphviz.Digraph, plan: Plan, node_id: str) -> None:
        """Recursively add plan nodes to the graph."""
        label = f"{plan.plan_type}\n{str(plan.content)}"

        # Style based on status
        color = "#333333"
        fillcolor = "#ffffff"
        if getattr(plan, "status", "active") == "completed":
            color = "#888888"
            fillcolor = "#f0f0f0"
        elif getattr(plan, "status", "active") == "abandoned":
            color = "#cc3333"
            fillcolor = "#ffeeee"

        dot.node(node_id, label, color=color, fillcolor=fillcolor)

        # Handle subplans
        # Note: Plan might be a reconstructed object or original
        subplans = getattr(plan, "subplans", [])

        for i, subplan in enumerate(subplans):
            child_id = f"{node_id}_{i}"
            self._add_plan_node(dot, subplan, child_id)
            dot.edge(node_id, child_id)

    def export_qud_stack(self, snapshot: StateSnapshot) -> str:
        """Generate SVG for QUD stack."""
        if not snapshot.qud:
            return (
                '<svg width="200" height="50">'
                '<text x="10" y="30" font-family="sans-serif">Empty QUD</text>'
                "</svg>"
            )

        dot = graphviz.Digraph(comment="QUD Stack")
        dot.attr(rankdir="BT")  # Bottom to Top for stack
        dot.attr("node", shape="note", style="filled", fillcolor="#e6f7ff", fontname="sans-serif")

        previous_id = None
        for i, question in enumerate(snapshot.qud):
            node_id = f"q_{i}"
            dot.node(node_id, str(question))
            if previous_id:
                # Invisible edge to enforce ordering
                dot.edge(previous_id, node_id, style="invis")
            previous_id = node_id

        try:
            return dot.pipe(format="svg").decode("utf-8")
        except Exception as e:
            return f'<div class="error">Error generating SVG: {str(e)}</div>'
