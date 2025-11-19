"""Burr integration for IBDM.

This module provides Burr state machine integration for the IBDM dialogue engine.
It implements the IBDM control loop (interpret -> integrate -> select -> generate)
as a Burr application with state tracking and visualization.
"""

# Actions are not exported - they are used internally by state_machine
# Importing them here creates a circular dependency with engine module
from ibdm.burr_integration.nlu_context import NLUContext
from ibdm.burr_integration.state_machine import DialogueStateMachine, create_dialogue_application

__all__ = [
    # State machine
    "create_dialogue_application",
    "DialogueStateMachine",
    # NLU context
    "NLUContext",
]
