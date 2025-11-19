"""Dialogue engine for Issue-Based Dialogue Management.

This module provides the core dialogue processing engine that orchestrates
the IBDM control loop, including NLU-enhanced interpretation.
"""

from typing import TYPE_CHECKING

from ibdm.engine.dialogue_engine import DialogueMoveEngine

# Lazy import to avoid circular dependency:
# nlu_engine → nlu → burr_integration → engine
# Import nlu_engine only when type checking or when explicitly accessed
if TYPE_CHECKING:
    from ibdm.engine.nlu_engine import NLUDialogueEngine, NLUEngineConfig, create_nlu_engine

__all__ = [
    "DialogueMoveEngine",
    "NLUDialogueEngine",
    "NLUEngineConfig",
    "create_nlu_engine",
]


def __getattr__(name: str):
    """Lazy import NLU engine components to avoid circular imports."""
    if name in ("NLUDialogueEngine", "NLUEngineConfig", "create_nlu_engine"):
        from ibdm.engine.nlu_engine import NLUDialogueEngine, NLUEngineConfig, create_nlu_engine

        if name == "NLUDialogueEngine":
            return NLUDialogueEngine
        elif name == "NLUEngineConfig":
            return NLUEngineConfig
        elif name == "create_nlu_engine":
            return create_nlu_engine
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
