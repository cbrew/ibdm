"""Best-first beam search path exploration for dialogue scenarios.

Uses best-first beam search with configurable beam size (default: 200) to explore
the most promising dialogue paths. Prioritizes complete paths (those with commitments
and progress toward scenario goals).

Useful for:
- Finding high-quality dialogue paths efficiently
- Testing scenario coverage with resource constraints
- Understanding most likely state transitions
- Evaluating path quality and completeness
"""

from __future__ import annotations

import heapq
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
        score: Quality score for beam search (higher is better)
    """

    depth: int
    step_index: int
    choice_made: ChoiceOption | None
    state_snapshot: dict[str, Any]
    parent: PathNode | None
    path_id: str
    children: list[PathNode] = field(default_factory=lambda: [])
    score: float = 0.0

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


def _empty_beam_metrics() -> dict[str, Any]:
    """Create empty beam metrics dict with correct type.

    Returns:
        Empty dictionary for beam metrics
    """
    return {}


def _calculate_path_score(node: PathNode, scenario: DemoScenario) -> float:
    """Calculate quality score for a path (higher is better).

    Scoring components:
    - Completeness: Paths with commitments are prioritized
    - Progress: Deeper paths with more commitments score higher
    - Expected choices: Paths following expected choices score higher
    - Scenario completion: Paths near end of scenario score higher

    Args:
        node: Path node to score
        scenario: Scenario being explored

    Returns:
        Quality score (higher is better)
    """
    score = 0.0

    # Completeness: Strong bonus for having commitments (indicates progress)
    commitments = len(node.state_snapshot.get("commitments", set()))
    if commitments > 0:
        score += 100.0  # Base bonus for any result
        score += commitments * 50.0  # Additional bonus per commitment

    # Progress: Reward depth (exploration)
    score += node.depth * 10.0

    # Expected path bonus: Prioritize following expected choices
    # Count how many choices in path are "expected"
    expected_count = 0
    current = node
    while current is not None and current.choice_made is not None:
        if current.choice_made.category.value == "expected":
            expected_count += 1
        current = current.parent
    score += expected_count * 20.0

    # Scenario completion: Reward being closer to end of scenario
    if scenario.steps:
        completion_ratio = node.step_index / len(scenario.steps)
        score += completion_ratio * 30.0

    # Small penalty for QUD size (prefer resolved questions)
    qud_size = node.state_snapshot.get("qud_size", 0)
    score -= qud_size * 2.0

    return score


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
        beam_metrics: Beam search statistics (paths pruned, avg score, etc.)
    """

    scenario_name: str
    max_depth: int
    total_paths: int
    paths_by_depth: dict[int, list[PathNode]]
    unique_states: set[frozenset[tuple[str, Any]]]
    state_convergence: dict[frozenset[tuple[str, Any]], list[PathNode]]
    coverage_metrics: dict[str, Any]
    beam_metrics: dict[str, Any] = field(default_factory=_empty_beam_metrics)


class PathExplorer:
    """Best-first beam search path exploration engine."""

    def __init__(self, scenario: DemoScenario, domain: Any, beam_size: int = 200) -> None:
        """Initialize path explorer.

        Args:
            scenario: Scenario to explore
            domain: Domain model for the scenario
            beam_size: Maximum number of paths to maintain (default: 200)
        """
        self.scenario = scenario
        self.domain = domain
        self.beam_size = beam_size
        self.explorer: ScenarioExplorer | None = None

    def explore_paths(self, max_depth: int = 3) -> ExplorationResult:
        """Explore dialogue paths using best-first beam search.

        Uses beam search to explore the most promising paths up to specified depth.
        Maintains at most beam_size paths at any time, prioritizing paths with
        commitments and progress toward scenario completion.

        Args:
            max_depth: Maximum depth to explore (default: 3)

        Returns:
            ExplorationResult with explored paths and metrics
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
            score=0.0,
        )

        # Best-first beam search
        paths_by_depth: dict[int, list[PathNode]] = {0: [root]}
        # Priority queue: (negative_score, counter, node)
        # Use negative score because heapq is a min-heap
        counter = 0  # Tie-breaker for nodes with same score
        heap: list[tuple[float, int, PathNode]] = [(-root.score, counter, root)]
        counter += 1

        all_paths: list[PathNode] = [root]
        unique_states: set[frozenset[tuple[str, Any]]] = {root.get_state_signature()}
        state_convergence: dict[frozenset[tuple[str, Any]], list[PathNode]] = {}

        # Beam search metrics
        total_generated = 0
        total_pruned = 0
        scores_tracked: list[float] = []

        while heap:
            # Get highest-scoring node (lowest negative score)
            _, _, node = heapq.heappop(heap)

            # Stop if we've reached max depth
            if node.depth >= max_depth:
                continue

            # Get available choices at this node
            choices = self._get_choices_at_node(node, initial_state)
            if not choices:
                continue

            # Generate all children
            children: list[PathNode] = []
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

                # Calculate score for child
                child.score = _calculate_path_score(child, self.scenario)
                scores_tracked.append(child.score)

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
                children.append(child)

                # Add to depth tracking
                if child.depth not in paths_by_depth:
                    paths_by_depth[child.depth] = []
                paths_by_depth[child.depth].append(child)

                total_generated += 1

            # Add children to heap
            for child in children:
                heapq.heappush(heap, (-child.score, counter, child))
                counter += 1

            # Beam pruning: keep only top beam_size paths
            if len(heap) > self.beam_size:
                # Keep top beam_size
                top_paths = heapq.nsmallest(self.beam_size, heap)
                pruned_count = len(heap) - self.beam_size
                total_pruned += pruned_count
                heap = top_paths
                heapq.heapify(heap)  # Restore heap property

        # Calculate coverage metrics
        coverage_metrics = self._calculate_coverage(all_paths)

        # Calculate beam metrics
        beam_metrics = {
            "beam_size": self.beam_size,
            "total_generated": total_generated,
            "total_pruned": total_pruned,
            "avg_score": sum(scores_tracked) / len(scores_tracked) if scores_tracked else 0.0,
            "max_score": max(scores_tracked) if scores_tracked else 0.0,
            "min_score": min(scores_tracked) if scores_tracked else 0.0,
        }

        return ExplorationResult(
            scenario_name=self.scenario.name,
            max_depth=max_depth,
            total_paths=len(all_paths),
            paths_by_depth=paths_by_depth,
            unique_states=unique_states,
            state_convergence=state_convergence,
            coverage_metrics=coverage_metrics,
            beam_metrics=beam_metrics,
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


def _path_has_result(node: PathNode) -> bool:
    """Check if a path has produced a result (has commitments).

    Args:
        node: Path node to check

    Returns:
        True if path has at least one commitment, False otherwise
    """
    commitments = node.state_snapshot.get("commitments", set())
    return len(commitments) > 0


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
    convergence_count = sum(1 for nodes in result.state_convergence.values() if len(nodes) > 1)
    lines.append(f"State convergence instances: {convergence_count}")

    # Count paths with results
    all_paths = [path for paths in result.paths_by_depth.values() for path in paths]
    paths_with_results = sum(1 for path in all_paths if _path_has_result(path))
    lines.append(f"Paths with results: {paths_with_results}/{result.total_paths}")
    lines.append("")

    # Beam search metrics
    if result.beam_metrics:
        lines.append("Beam Search Metrics")
        lines.append("-" * 70)
        lines.append(f"Beam size: {result.beam_metrics.get('beam_size', 'N/A')}")
        lines.append(f"Total paths generated: {result.beam_metrics.get('total_generated', 0)}")
        lines.append(f"Paths pruned: {result.beam_metrics.get('total_pruned', 0)}")
        pruned = result.beam_metrics.get("total_pruned", 0)
        generated = result.beam_metrics.get("total_generated", 1)
        prune_rate = (pruned / generated * 100) if generated > 0 else 0
        lines.append(f"Pruning rate: {prune_rate:.1f}%")
        lines.append(f"Avg path score: {result.beam_metrics.get('avg_score', 0):.2f}")
        lines.append(
            f"Score range: [{result.beam_metrics.get('min_score', 0):.2f}, "
            f"{result.beam_metrics.get('max_score', 0):.2f}]"
        )
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

        # Show first 10 paths at each depth, sorted by score
        sorted_paths = sorted(paths[:10], key=lambda p: p.score, reverse=True)
        for i, path in enumerate(sorted_paths, 1):
            path_desc = path.path_id if path.path_id != "root" else "root"
            commitments = len(path.state_snapshot.get("commitments", set()))
            qud = path.state_snapshot.get("qud_size", 0)
            result_indicator = "✓" if _path_has_result(path) else "✗"
            lines.append(
                f"  {result_indicator} [{path_desc}] score: {path.score:.1f}, "
                f"commitments: {commitments}, qud: {qud}"
            )

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
            result_indicator = "✓" if _path_has_result(node) else "✗"
            node_info = (
                f"{prefix}{connector}{result_indicator} [{node.path_id}] "
                f'{category}: "{choice_desc}" (S:{node.score:.1f}, C:{commitments})'
            )
            lines.append(node_info)

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
