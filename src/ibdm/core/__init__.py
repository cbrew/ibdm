"""Core data structures for Issue-Based Dialogue Management.

This module provides the fundamental data structures for IBDM:
- Questions: Semantic representations of issues under discussion
- Answers: Values that resolve questions
- DialogueMoves: Communicative acts performed by participants
- Plans: Dialogue goals and strategies
- InformationState: Complete dialogue context
"""

from ibdm.core.answers import Answer
from ibdm.core.domain import DomainModel
from ibdm.core.information_state import ControlIS, InformationState, PrivateIS, SharedIS
from ibdm.core.moves import DialogueMove
from ibdm.core.plans import Plan
from ibdm.core.questions import AltQuestion, Question, WhQuestion, YNQuestion

__all__ = [
    # Questions
    "Question",
    "WhQuestion",
    "YNQuestion",
    "AltQuestion",
    # Answers
    "Answer",
    # Moves
    "DialogueMove",
    # Plans
    "Plan",
    # Information State
    "InformationState",
    "PrivateIS",
    "SharedIS",
    "ControlIS",
    # Domain
    "DomainModel",
]
