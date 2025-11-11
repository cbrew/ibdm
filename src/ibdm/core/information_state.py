"""Information State representations for Issue-Based Dialogue Management.

The Information State (IS) captures all relevant information about the dialogue
at any point. It consists of private, shared, and control components.

Based on Larsson (2002) Issue-based Dialogue Management.
"""

import copy
from dataclasses import dataclass, field
from typing import Any

from ibdm.core.moves import DialogueMove
from ibdm.core.plans import Plan
from ibdm.core.questions import Question


@dataclass
class PrivateIS:
    """Private information state.

    Contains information that is private to one agent, including their
    plans, agenda, beliefs, and recent utterances.
    """

    plan: list[Plan] = field(default_factory=lambda: [])
    """Stack of dialogue plans/goals"""

    agenda: list[DialogueMove] = field(default_factory=lambda: [])
    """Ordered list of immediate actions to perform"""

    beliefs: dict[str, Any] = field(default_factory=lambda: {})
    """Private beliefs about the world"""

    last_utterance: DialogueMove | None = None
    """Latest utterance produced by this agent"""

    def __str__(self) -> str:
        """Return string representation."""
        return (
            f"PrivateIS(plans={len(self.plan)}, "
            f"agenda={len(self.agenda)}, "
            f"beliefs={len(self.beliefs)})"
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
