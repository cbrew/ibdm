"""Rule execution trace for visualization.

Captures which rules were evaluated, which were selected, and what effects
they had. Used for visualizing the rule execution process and understanding
dialogue manager behavior.
"""

from dataclasses import dataclass, field
from typing import Any

from ibdm.visualization.state_diff import StateDiff


@dataclass
class RuleEvaluation:
    """Record of a single rule's evaluation.

    Attributes:
        rule_name: Name of the rule
        priority: Rule priority (higher = earlier)
        preconditions_met: Whether preconditions were satisfied
        was_selected: Whether this rule was selected for execution
        reason: Explanation of why it was/wasn't selected
    """

    rule_name: str
    priority: int
    preconditions_met: bool
    was_selected: bool
    reason: str = ""

    def __str__(self) -> str:
        """Return string representation."""
        status = "✓" if self.preconditions_met else "✗"
        selected = " [SELECTED]" if self.was_selected else ""
        return f"{status} {self.rule_name} (p={self.priority}){selected}"


@dataclass
class RuleTrace:
    """Trace of rule execution for a single phase.

    Captures the complete rule selection and execution process:
    1. Which rules were evaluated
    2. Which had their preconditions met
    3. Which rule was selected (highest priority with met preconditions)
    4. What state changes the rule caused

    Attributes:
        phase: Phase name ("interpret", "integrate", "select", "generate")
        timestamp: When this trace was captured
        label: Human-readable label
        evaluations: List of rule evaluations (in priority order)
        selected_rule: Name of the selected rule (if any)
        state_before: State snapshot before rule execution
        state_after: State snapshot after rule execution
        diff: Computed diff showing what changed
        metadata: Additional context (e.g., current move, user utterance)
    """

    phase: str
    timestamp: int
    label: str
    evaluations: list[RuleEvaluation] = field(default_factory=list)
    selected_rule: str | None = None
    state_before: Any = None  # StateSnapshot (avoid circular import)
    state_after: Any = None  # StateSnapshot
    diff: StateDiff | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def rules_evaluated(self) -> int:
        """Count how many rules were evaluated."""
        return len(self.evaluations)

    def rules_with_met_preconditions(self) -> int:
        """Count how many rules had their preconditions met."""
        return sum(1 for e in self.evaluations if e.preconditions_met)

    def get_selected_evaluation(self) -> RuleEvaluation | None:
        """Get the evaluation for the selected rule."""
        for eval in self.evaluations:
            if eval.was_selected:
                return eval
        return None

    def format_summary(self) -> str:
        """Generate a summary of rule execution.

        Returns:
            Summary like "integrate: accommodate_skip_question (3/12 rules ready)"
        """
        selected = self.selected_rule or "none"
        met = self.rules_with_met_preconditions()
        total = self.rules_evaluated()
        return f"{self.phase}: {selected} ({met}/{total} rules ready)"

    def __str__(self) -> str:
        """Return string representation."""
        return f"RuleTrace(t={self.timestamp}, {self.format_summary()})"
