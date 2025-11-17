"""Exhaustive path exploration for dialogue scenarios.

Explores all possible dialogue paths up to a specified depth using breadth-first search.
Depth is configurable - default is 3, but can be set to any positive integer.
Note: Path count grows exponentially (depth 5+ may generate thousands of paths).

Useful for:
- Testing all distractor behaviors
- Understanding state transitions
- Validating scenario logic
- Coverage analysis
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Any

from ibdm.core import InformationState
from ibdm.demo.scenario_explorer import ChoiceOption, ScenarioExplorer
from ibdm.demo.scenarios import DemoScenario


def _extract_commitment_from_utterance(utterance: str) -> str | None:
    """Extract commitment from user utterance (simple pattern matching for demo).

    Args:
        utterance: User's utterance

    Returns:
        Commitment string or None
    """
    # Simple mapping for common NDA scenario utterances
    if "Acme Corp and Smith Inc" in utterance:
        return "parties(Acme Corp and Smith Inc)"
    elif utterance.lower() == "mutual":
        return "nda_type(mutual)"
    elif utterance.lower() == "one-way":
        return "nda_type(one-way)"
    elif "January 1, 2025" in utterance or "2025" in utterance:
        if "January 1, 2025" in utterance:
            return "effective_date(January 1, 2025)"
    elif "5 years" in utterance or "5 year" in utterance:
        return "duration(5 years)"
    elif utterance == "Perpetual" or utterance.lower() == "perpetual":
        return "duration(perpetual)"
    elif utterance == "California":
        return "governing_law(California)"
    elif utterance == "Delaware":
        return "governing_law(Delaware)"
    elif utterance == "New York":
        return "governing_law(New York)"

    return None


@dataclass
class PathNode:
    """A node in the exploration tree representing a dialogue state.

    Attributes:
        depth: How many user choices deep (0 = initial state)
        step_index: Current position in scenario
        choice_made: The choice that led to this node (None for root)
        state_snapshot: Snapshot of dialogue state at this node
        parent: Parent node in the tree (None for root)
        path_id: String representation of path (e.g., "1→3→2")
        children: Child nodes (filled during exploration)
    """

    depth: int
    step_index: int
    choice_made: ChoiceOption | None
    state_snapshot: dict[str, Any]
    parent: PathNode | None
    path_id: str
    children: list[PathNode] = field(default_factory=lambda: [])

    def get_path_choices(self) -> list[str]:
        """Get the sequence of choices that led to this node.

        Returns:
            List of choice utterances from root to this node
        """
        path: list[str] = []
        node: PathNode | None = self
        while node is not None and node.choice_made is not None:
            path.append(node.choice_made.utterance)
            node = node.parent
        return list(reversed(path))

    def get_state_signature(self) -> frozenset[tuple[str, Any]]:
        """Get a hashable signature of the dialogue state.

        Returns:
            Frozenset of state key-value pairs for comparison
        """
        # Extract key state components
        commitments = frozenset(self.state_snapshot.get("commitments", set()))
        qud_size = self.state_snapshot.get("qud_size", 0)
        issues_size = self.state_snapshot.get("issues_size", 0)

        return frozenset(
            [
                ("commitments", commitments),
                ("qud_size", qud_size),
                ("issues_size", issues_size),
            ]
        )


@dataclass
class ExplorationResult:
    """Results of path exploration.

    Attributes:
        scenario_name: Name of explored scenario
        max_depth: Maximum depth explored
        total_paths: Total number of paths explored
        paths_by_depth: Paths organized by depth
        unique_states: Set of unique state signatures encountered
        state_convergence: Paths that led to same state
        coverage_metrics: Distractor coverage statistics
    """

    scenario_name: str
    max_depth: int
    total_paths: int
    paths_by_depth: dict[int, list[PathNode]]
    unique_states: set[frozenset[tuple[str, Any]]]
    state_convergence: dict[frozenset[tuple[str, Any]], list[PathNode]]
    coverage_metrics: dict[str, Any]


class PathExplorer:
    """Exhaustive path exploration engine using breadth-first search."""

    def __init__(self, scenario: DemoScenario, domain: Any) -> None:
        """Initialize path explorer.

        Args:
            scenario: Scenario to explore
            domain: Domain model for the scenario
        """
        self.scenario = scenario
        self.domain = domain
        self.explorer: ScenarioExplorer | None = None

    def explore_paths(self, max_depth: int = 3) -> ExplorationResult:
        """Explore all dialogue paths up to specified depth.

        Args:
            max_depth: Maximum depth to explore (default: 3).
                Can be any positive integer. Note that path count grows
                exponentially - depth 5+ may generate thousands of paths.

        Returns:
            ExplorationResult with all explored paths and metrics
        """
        # Initialize state and explorer
        initial_state = InformationState(agent_id="system")
        initial_state.private.beliefs["domain"] = self.domain
        self.explorer = ScenarioExplorer(self.scenario, initial_state, self.domain)

        # Create root node
        root = PathNode(
            depth=0,
            step_index=0,
            choice_made=None,
            state_snapshot=self._capture_state(initial_state),
            parent=None,
            path_id="root",
        )

        # BFS exploration
        paths_by_depth: dict[int, list[PathNode]] = {0: [root]}
        queue: deque[PathNode] = deque([root])
        all_paths: list[PathNode] = [root]
        unique_states: set[frozenset[tuple[str, Any]]] = {root.get_state_signature()}
        state_convergence: dict[frozenset[tuple[str, Any]], list[PathNode]] = {}

        while queue:
            node = queue.popleft()

            # Stop if we've reached max depth
            if node.depth >= max_depth:
                continue

            # Get available choices at this node
            choices = self._get_choices_at_node(node, initial_state)
            if not choices:
                continue

            # Explore each choice
            for choice in choices:
                # Create child node
                child_state = self._simulate_choice(node, choice, initial_state)
                child_path_id = (
                    f"{node.path_id}→{choice.id}" if node.path_id != "root" else str(choice.id)
                )

                child = PathNode(
                    depth=node.depth + 1,
                    step_index=node.step_index + 1,
                    choice_made=choice,
                    state_snapshot=self._capture_state(child_state),
                    parent=node,
                    path_id=child_path_id,
                )

                # Track state
                state_sig = child.get_state_signature()
                unique_states.add(state_sig)

                # Track convergence
                if state_sig not in state_convergence:
                    state_convergence[state_sig] = []
                state_convergence[state_sig].append(child)

                # Add to tree
                node.children.append(child)
                all_paths.append(child)

                # Add to depth tracking
                if child.depth not in paths_by_depth:
                    paths_by_depth[child.depth] = []
                paths_by_depth[child.depth].append(child)

                # Add to queue for further exploration
                queue.append(child)

        # Calculate coverage metrics
        coverage_metrics = self._calculate_coverage(all_paths)

        return ExplorationResult(
            scenario_name=self.scenario.name,
            max_depth=max_depth,
            total_paths=len(all_paths),
            paths_by_depth=paths_by_depth,
            unique_states=unique_states,
            state_convergence=state_convergence,
            coverage_metrics=coverage_metrics,
        )

    def _get_choices_at_node(
        self, node: PathNode, base_state: InformationState
    ) -> list[ChoiceOption]:
        """Get available choices at a given node.

        Args:
            node: Current node
            base_state: Base information state

        Returns:
            List of available choices
        """
        # Find the current user turn
        step_index = node.step_index
        if step_index >= len(self.scenario.steps):
            return []

        # Skip system turns
        while step_index < len(self.scenario.steps):
            step = self.scenario.steps[step_index]
            if step.speaker == "user":
                break
            step_index += 1

        if step_index >= len(self.scenario.steps):
            return []

        # Get choices for this turn
        assert self.explorer is not None
        # Temporarily set explorer's step index
        original_index = self.explorer.current_step_index
        self.explorer.current_step_index = step_index
        choices = self.explorer.get_current_choices()
        self.explorer.current_step_index = original_index

        return choices

    def _simulate_choice(
        self, node: PathNode, choice: ChoiceOption, base_state: InformationState
    ) -> InformationState:
        """Simulate making a choice and return the resulting state.

        Args:
            node: Current node
            choice: Choice to make
            base_state: Base state to copy from

        Returns:
            New state after applying choice
        """
        # Create a copy of the state
        new_state = InformationState(agent_id="system")
        new_state.private.beliefs["domain"] = self.domain

        # Restore parent state
        for commitment in node.state_snapshot.get("commitments", set()):
            new_state.shared.commitments.add(commitment)

        # Apply the choice (simple simulation for demo)
        # In a real system, this would run the dialogue engine
        commitment = _extract_commitment_from_utterance(choice.utterance)
        if commitment:
            new_state.shared.commitments.add(commitment)

        return new_state

    def _capture_state(self, state: InformationState) -> dict[str, Any]:
        """Capture a snapshot of the dialogue state.

        Args:
            state: Information state to capture

        Returns:
            Dictionary with state snapshot
        """
        return {
            "commitments": set(state.shared.commitments),
            "qud_size": len(state.shared.qud),
            "issues_size": len(state.private.issues),
        }

    def _calculate_coverage(self, all_paths: list[PathNode]) -> dict[str, Any]:
        """Calculate distractor coverage metrics.

        Args:
            all_paths: All explored paths

        Returns:
            Coverage metrics dictionary
        """
        # Count unique choices exercised
        unique_choices: set[str] = set()
        expected_count = 0
        distractor_count = 0

        for path in all_paths:
            if path.choice_made:
                unique_choices.add(path.choice_made.utterance)
                if path.choice_made.category.value == "expected":
                    expected_count += 1
                else:
                    distractor_count += 1

        return {
            "unique_choices": len(unique_choices),
            "expected_paths": expected_count,
            "distractor_paths": distractor_count,
            "total_choices": expected_count + distractor_count,
        }


def generate_exploration_report(result: ExplorationResult) -> str:
    """Generate a human-readable exploration report.

    Args:
        result: Exploration result to report on

    Returns:
        Formatted report string
    """
    lines: list[str] = []

    # Header
    lines.append("=" * 70)
    lines.append(f"  Path Exploration Report: {result.scenario_name}")
    lines.append(f"  Max Depth: {result.max_depth}")
    lines.append("=" * 70)
    lines.append("")

    # Summary
    lines.append("Summary")
    lines.append("-" * 70)
    lines.append(f"Total paths explored: {result.total_paths}")
    lines.append(f"Unique states reached: {len(result.unique_states)}")
    convergence_count = sum(
        1 for nodes in result.state_convergence.values() if len(nodes) > 1
    )
    lines.append(f"State convergence instances: {convergence_count}")
    lines.append("")

    # Coverage
    metrics = result.coverage_metrics
    lines.append("Coverage")
    lines.append("-" * 70)
    lines.append(f"Unique choices exercised: {metrics['unique_choices']}")
    lines.append(f"Expected path choices: {metrics['expected_paths']}")
    lines.append(f"Distractor choices: {metrics['distractor_paths']}")
    lines.append(f"Total choices made: {metrics['total_choices']}")
    lines.append("")

    # Paths by depth
    lines.append("Paths by Depth")
    lines.append("-" * 70)
    for depth in sorted(result.paths_by_depth.keys()):
        paths = result.paths_by_depth[depth]
        lines.append(f"\nDepth {depth}: {len(paths)} path(s)")

        # Show first 10 paths at each depth
        for i, path in enumerate(paths[:10], 1):
            path_desc = path.path_id if path.path_id != "root" else "root"
            commitments = len(path.state_snapshot.get("commitments", set()))
            qud = path.state_snapshot.get("qud_size", 0)
            lines.append(f"  [{path_desc}] commitments: {commitments}, qud: {qud}")

        if len(paths) > 10:
            lines.append(f"  ... and {len(paths) - 10} more paths")

    lines.append("")

    # State convergence (paths that lead to same state)
    convergent_states = [
        (sig, nodes) for sig, nodes in result.state_convergence.items() if len(nodes) > 1
    ]
    if convergent_states:
        lines.append("State Convergence")
        lines.append("-" * 70)
        lines.append(f"Found {len(convergent_states)} state(s) reached by multiple paths")
        lines.append("")

        # Show first 5 convergent states
        for i, (_sig, nodes) in enumerate(convergent_states[:5], 1):
            lines.append(f"State {i}: {len(nodes)} paths converge")
            for node in nodes[:3]:
                lines.append(f"  - Path: {node.path_id}")
            if len(nodes) > 3:
                lines.append(f"  ... and {len(nodes) - 3} more paths")
            lines.append("")

    lines.append("=" * 70)

    return "\n".join(lines)


def generate_tree_visualization(result: ExplorationResult, max_depth: int = 2) -> str:
    """Generate a tree visualization of explored paths.

    Args:
        result: Exploration result
        max_depth: Maximum depth to visualize (default: 2)

    Returns:
        Tree visualization string
    """
    lines: list[str] = []
    lines.append(f"Path Tree: {result.scenario_name}")
    lines.append("=" * 70)
    lines.append("")

    # Get root
    root_paths = result.paths_by_depth.get(0, [])
    if not root_paths:
        return "No paths found"

    root = root_paths[0]

    def render_node(node: PathNode, prefix: str = "", is_last: bool = True) -> None:
        """Recursively render node and children."""
        if node.depth > max_depth:
            return

        # Render current node
        connector = "└── " if is_last else "├── "
        if node.depth == 0:
            lines.append("root")
        else:
            choice_desc = node.choice_made.utterance[:40] if node.choice_made else "?"
            category = node.choice_made.category.value if node.choice_made else "?"
            commitments = len(node.state_snapshot.get("commitments", set()))
            lines.append(
                f'{prefix}{connector}[{node.path_id}] {category}: "{choice_desc}" (C:{commitments})'
            )

        # Render children
        if node.children:
            extension = "    " if is_last else "│   "
            new_prefix = prefix + extension

            for i, child in enumerate(node.children):
                is_last_child = i == len(node.children) - 1
                render_node(child, new_prefix, is_last_child)

    render_node(root)
    lines.append("")
    lines.append("=" * 70)

    return "\n".join(lines)
