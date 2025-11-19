"""Natural Language Generation module for IBDM.

This module provides natural language generation capabilities for producing
system utterances from dialogue moves.
"""

# Import NLGResult first to avoid circular imports
# Then import engine (which depends on nlg_result)
from ibdm.nlg.nlg_engine import NLGEngine, NLGEngineConfig, create_nlg_engine
from ibdm.nlg.nlg_result import NLGResult, StructuredNLGResponse

__all__ = [
    "NLGResult",
    "StructuredNLGResponse",
    "NLGEngine",
    "NLGEngineConfig",
    "create_nlg_engine",
]
