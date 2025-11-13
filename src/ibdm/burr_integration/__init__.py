"""Burr integration for IBDM.

This module provides Burr state machine integration for the IBDM dialogue engine.
It implements the IBDM control loop (interpret -> integrate -> select -> generate)
as a Burr application with state tracking and visualization.
"""

from ibdm.burr_integration.actions import generate, idle, initialize, integrate, interpret, select
from ibdm.burr_integration.nlu_context import NLUContext
from ibdm.burr_integration.state_machine import DialogueStateMachine, create_dialogue_application

__all__ = [
    # Actions
    "initialize",
    "idle",
    "interpret",
    "integrate",
    "select",
    "generate",
    # State machine
    "create_dialogue_application",
    "DialogueStateMachine",
    # NLU context
    "NLUContext",
]
