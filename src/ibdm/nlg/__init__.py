"""Natural Language Generation module for IBDM.

This module provides natural language generation capabilities for producing
system utterances from dialogue moves.
"""

from ibdm.nlg.nlg_engine import NLGEngine, NLGEngineConfig, create_nlg_engine
from ibdm.nlg.nlg_result import NLGResult

__all__ = [
    "NLGResult",
    "NLGEngine",
    "NLGEngineConfig",
    "create_nlg_engine",
]
