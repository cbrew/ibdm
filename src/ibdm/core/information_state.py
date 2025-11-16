"""Information State representations for Issue-Based Dialogue Management.

The Information State (IS) captures all relevant information about the dialogue
at any point. It consists of private, shared, and control components.

Based on Larsson (2002) Issue-based Dialogue Management.
"""

import copy
from dataclasses import dataclass, field
from typing import Any, cast

from ibdm.core.moves import DialogueMove
from ibdm.core.plans import Plan
from ibdm.core.questions import Question


@dataclass
class PrivateIS:
    """Private information state.

    Contains information that is private to one agent, including their
    plans, agenda, beliefs, and recent utterances.

    IBiS3 Extension: The 'issues' field supports question accommodation.
    Questions are accommodated to issues before being raised to the QUD.
    """

    plan: list[Plan] = field(default_factory=lambda: [])
    """Stack of dialogue plans/goals"""

    agenda: list[DialogueMove] = field(default_factory=lambda: [])
    """Ordered list of immediate actions to perform"""

    beliefs: dict[str, Any] = field(default_factory=lambda: {})
    """Private beliefs about the world"""

    last_utterance: DialogueMove | None = None
    """Latest utterance produced by this agent"""

    issues: list[Question] = field(default_factory=lambda: [])
    """Accommodated questions not yet raised to QUD (IBiS3 - Larsson Section 4.6)"""

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return {
            "plan": [getattr(p, "to_dict", lambda: str(p))() for p in self.plan],
            "agenda": [getattr(m, "to_dict", lambda: str(m))() for m in self.agenda],
            "beliefs": self.beliefs.copy(),
            "last_utterance": (
                getattr(self.last_utterance, "to_dict", lambda: str(self.last_utterance))()
                if self.last_utterance
                else None
            ),
            "issues": [getattr(q, "to_dict", lambda: str(q))() for q in self.issues],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PrivateIS":
        """Reconstruct from dict.

        Args:
            data: Dictionary representation from to_dict()

        Returns:
            Reconstructed PrivateIS object
        """
        from ibdm.core.moves import DialogueMove
        from ibdm.core.plans import Plan
        from ibdm.core.questions import Question

        # Reconstruct plans
        plan_data = data.get("plan", [])
        plans = [Plan.from_dict(p) for p in plan_data]

        # Reconstruct agenda
        agenda_data = data.get("agenda", [])
        agenda = [DialogueMove.from_dict(m) for m in agenda_data]

        # Reconstruct last_utterance
        last_utterance = None
        last_utterance_data = data.get("last_utterance")
        if last_utterance_data is not None:
            last_utterance = DialogueMove.from_dict(last_utterance_data)

        # Reconstruct issues (IBiS3)
        issues_data: list[Any] = data.get("issues", [])
        issues: list[Question] = []
        for q in issues_data:
            if isinstance(q, dict):
                issues.append(Question.from_dict(cast(dict[str, Any], q)))
            else:
                issues.append(q)

        return cls(
            plan=plans,
            agenda=agenda,
            beliefs=data.get("beliefs", {}).copy(),
            last_utterance=last_utterance,
            issues=issues,
        )

    def __str__(self) -> str:
        """Return string representation."""
        return (
            f"PrivateIS(plans={len(self.plan)}, "
            f"agenda={len(self.agenda)}, "
            f"beliefs={len(self.beliefs)}, "
            f"issues={len(self.issues)})"
        )


@dataclass
class SharedIS:
    """Shared information state.

    Contains information that is mutually believed to be shared between
    dialogue participants, including the QUD stack and shared commitments.
    """

    qud: list[Question] = field(default_factory=lambda: [])
    """Stack of Questions Under Discussion (last = top)"""

    commitments: set[str] = field(default_factory=lambda: set())
    """Shared commitments (propositions agreed upon)"""

    last_moves: list[DialogueMove] = field(default_factory=lambda: [])
    """Recent moves from dialogue partners"""

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict.

        Note: Converts set to list for JSON compatibility.
        """
        return {
            "qud": [q.to_dict() if hasattr(q, "to_dict") else str(q) for q in self.qud],
            "commitments": list(self.commitments),  # Convert set to list
            "last_moves": [
                m.to_dict() if hasattr(m, "to_dict") else str(m) for m in self.last_moves
            ],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SharedIS":
        """Reconstruct from dict.

        Note: QUD and moves are not fully reconstructed (stored as empty).
        For now, we only restore commitments which are simple strings.
        """
        return cls(
            qud=[],  # Questions would need Question.from_dict() - skip for now
            commitments=set(data.get("commitments", [])),  # Convert list back to set
            last_moves=[],  # Moves would need DialogueMove.from_dict() - skip for now
        )

    def __str__(self) -> str:
        """Return string representation."""
        qud_top = f", top={self.qud[-1]}" if self.qud else ""
        return f"SharedIS(qud={len(self.qud)}{qud_top}, commitments={len(self.commitments)})"

    def push_qud(self, question: Question) -> None:
        """Push a question onto the QUD stack."""
        self.qud.append(question)

    def pop_qud(self) -> Question | None:
        """Pop and return the top question from QUD stack."""
        return self.qud.pop() if self.qud else None

    def top_qud(self) -> Question | None:
        """Return the top question without removing it."""
        return self.qud[-1] if self.qud else None


@dataclass
class ControlIS:
    """Control information.

    Contains control flow information for managing turn-taking and
    dialogue state transitions.
    """

    speaker: str = "user"
    """Current speaker"""

    next_speaker: str = "system"
    """Who should speak next"""

    initiative: str = "mixed"
    """Dialogue initiative: 'user', 'system', or 'mixed'"""

    dialogue_state: str = "active"
    """Dialogue state: 'active', 'paused', 'ended'"""

    def to_dict(self) -> dict[str, str]:
        """Convert to JSON-serializable dict."""
        return {
            "speaker": self.speaker,
            "next_speaker": self.next_speaker,
            "initiative": self.initiative,
            "dialogue_state": self.dialogue_state,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "ControlIS":
        """Reconstruct from dict."""
        return cls(
            speaker=data.get("speaker", "user"),
            next_speaker=data.get("next_speaker", "system"),
            initiative=data.get("initiative", "mixed"),
            dialogue_state=data.get("dialogue_state", "active"),
        )

    def __str__(self) -> str:
        """Return string representation."""
        return (
            f"ControlIS(speaker={self.speaker}, "
            f"next={self.next_speaker}, "
            f"state={self.dialogue_state})"
        )


@dataclass
class InformationState:
    """Complete information state record.

    The Information State is the central data structure in IBDM, containing
    all information about the dialogue: private knowledge, shared knowledge,
    and control state.
    """

    private: PrivateIS = field(default_factory=PrivateIS)
    """Private information state"""

    shared: SharedIS = field(default_factory=SharedIS)
    """Shared information state"""

    control: ControlIS = field(default_factory=ControlIS)
    """Control information"""

    agent_id: str = "system"
    """ID of the agent owning this information state"""

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict.

        This ensures proper serialization for Burr's persistence layer.

        Returns:
            Dictionary representation suitable for JSON serialization
        """
        return {
            "private": self.private.to_dict(),
            "shared": self.shared.to_dict(),
            "control": self.control.to_dict(),
            "agent_id": self.agent_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "InformationState":
        """Reconstruct InformationState from dict.

        Args:
            data: Dictionary representation from to_dict()

        Returns:
            Reconstructed InformationState
        """
        return cls(
            private=PrivateIS.from_dict(data.get("private", {})),
            shared=SharedIS.from_dict(data.get("shared", {})),
            control=ControlIS.from_dict(data.get("control", {})),
            agent_id=data.get("agent_id", "system"),
        )

    def clone(self) -> "InformationState":
        """Create a deep copy of the information state.

        Used for state transitions and rollback operations.

        Returns:
            A deep copy of this information state
        """
        return copy.deepcopy(self)

    def __str__(self) -> str:
        """Return string representation."""
        return (
            f"InformationState(agent={self.agent_id}):\n"
            f"  {self.private}\n"
            f"  {self.shared}\n"
            f"  {self.control}"
        )
