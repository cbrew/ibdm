"""State snapshot for visualization.

Provides an immutable snapshot of InformationState at a specific point in time.
Used as input to diff computation and for timeline visualization.
"""

from dataclasses import dataclass, field
from typing import Any

from ibdm.core import DialogueMove, InformationState, Plan, Question


@dataclass(frozen=True)
class StateSnapshot:
    """Immutable snapshot of dialogue state at a point in time.

    Captures the full InformationState plus metadata about when/why this
    snapshot was taken (e.g., "after integrate phase", "after rule X").

    Attributes:
        timestamp: Monotonic counter for ordering (0, 1, 2, ...)
        label: Human-readable description ("Turn 3: After Integration")
        qud: Snapshot of QUD stack
        commitments: Snapshot of commitments
        plan: Snapshot of active plans
        agenda: Snapshot of agenda
        issues: Snapshot of private issues
        beliefs: Snapshot of beliefs dict
        overridden_questions: Snapshot of overridden questions
        actions: Snapshot of actions
        last_move: Last dialogue move
        agent_id: Agent identifier
    """

    timestamp: int
    label: str

    # Shared state
    qud: tuple[Question, ...] = field(default_factory=tuple)
    commitments: tuple[Any, ...] = field(default_factory=tuple)

    # Private state
    plan: tuple[Plan, ...] = field(default_factory=tuple)
    agenda: tuple[DialogueMove, ...] = field(default_factory=tuple)
    issues: tuple[Question, ...] = field(default_factory=tuple)
    beliefs: dict[str, Any] = field(default_factory=dict)
    overridden_questions: tuple[Question, ...] = field(default_factory=tuple)
    actions: tuple[Any, ...] = field(default_factory=tuple)
    last_move: DialogueMove | None = None

    # Metadata
    agent_id: str = "system"

    @classmethod
    def from_state(cls, state: InformationState, timestamp: int, label: str) -> "StateSnapshot":
        """Create snapshot from InformationState.

        Args:
            state: Current information state
            timestamp: Monotonic timestamp (0, 1, 2, ...)
            label: Human-readable label

        Returns:
            Immutable snapshot of the state
        """
        return cls(
            timestamp=timestamp,
            label=label,
            # Shared state (convert lists to tuples for immutability)
            qud=tuple(state.shared.qud),
            commitments=tuple(state.shared.commitments),
            # Private state
            plan=tuple(state.private.plan),
            agenda=tuple(state.private.agenda),
            issues=tuple(state.private.issues),
            beliefs=state.private.beliefs.copy(),  # Shallow copy is OK
            overridden_questions=tuple(state.private.overridden_questions),
            actions=tuple(state.private.actions),
            last_move=state.private.last_utterance,
            agent_id=state.agent_id,
        )

    def field_value(self, field_name: str) -> Any:
        """Get value of a field by name.

        Args:
            field_name: Name of field (e.g., "qud", "commitments")

        Returns:
            Value of the field

        Raises:
            AttributeError: If field doesn't exist
        """
        return getattr(self, field_name)

    def __str__(self) -> str:
        """Return string representation."""
        return (
            f"StateSnapshot(t={self.timestamp}, "
            f"qud={len(self.qud)}, "
            f"com={len(self.commitments)}, "
            f"plan={len(self.plan)}, "
            f"issues={len(self.issues)})"
        )
