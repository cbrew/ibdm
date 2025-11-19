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

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict.

        Returns:
            Dictionary representation
        """
        return {
            "timestamp": self.timestamp,
            "label": self.label,
            "qud": [q.to_dict() if hasattr(q, "to_dict") else str(q) for q in self.qud],
            "commitments": [str(c) for c in self.commitments],
            "plan": [p.to_dict() if hasattr(p, "to_dict") else str(p) for p in self.plan],
            "agenda": [m.to_dict() if hasattr(m, "to_dict") else str(m) for m in self.agenda],
            "issues": [q.to_dict() if hasattr(q, "to_dict") else str(q) for q in self.issues],
            "beliefs": self.beliefs.copy(),
            "overridden_questions": [
                q.to_dict() if hasattr(q, "to_dict") else str(q) for q in self.overridden_questions
            ],
            "actions": [a.to_dict() if hasattr(a, "to_dict") else str(a) for a in self.actions],
            "last_move": (
                self.last_move.to_dict()
                if self.last_move and hasattr(self.last_move, "to_dict")
                else str(self.last_move)
                if self.last_move
                else None
            ),
            "agent_id": self.agent_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "StateSnapshot":
        """Reconstruct snapshot from dict.

        Note: This is a lossy reconstruction if only used for visualization.
        We reconstruct basic objects but some type information might be simplified
        if we rely only on dict structure. However, for monitoring, this is sufficient.

        Args:
            data: Dictionary from to_dict()

        Returns:
            Reconstructed StateSnapshot
        """
        from ibdm.core import DialogueMove, Plan, Question
        from ibdm.core.actions import Action

        # Helper to reconstruct objects if possible
        def _reconstruct_question(q_data: Any) -> Any:
            if isinstance(q_data, dict) and "type" in q_data:
                return Question.from_dict(q_data)
            return q_data

        def _reconstruct_plan(p_data: Any) -> Any:
            if isinstance(p_data, dict):
                return Plan.from_dict(p_data)
            return p_data

        def _reconstruct_move(m_data: Any) -> Any:
            if isinstance(m_data, dict):
                return DialogueMove.from_dict(m_data)
            return m_data

        def _reconstruct_action(a_data: Any) -> Any:
            if isinstance(a_data, dict):
                return Action.from_dict(a_data)
            return a_data

        return cls(
            timestamp=data.get("timestamp", 0),
            label=data.get("label", ""),
            qud=tuple(_reconstruct_question(q) for q in data.get("qud", [])),
            commitments=tuple(data.get("commitments", [])),
            plan=tuple(_reconstruct_plan(p) for p in data.get("plan", [])),
            agenda=tuple(_reconstruct_move(m) for m in data.get("agenda", [])),
            issues=tuple(_reconstruct_question(q) for q in data.get("issues", [])),
            beliefs=data.get("beliefs", {}),
            overridden_questions=tuple(
                _reconstruct_question(q) for q in data.get("overridden_questions", [])
            ),
            actions=tuple(_reconstruct_action(a) for a in data.get("actions", [])),
            last_move=_reconstruct_move(data.get("last_move")),
            agent_id=data.get("agent_id", "system"),
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
