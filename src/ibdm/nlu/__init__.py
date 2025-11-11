"""Natural Language Understanding module for IBDM.

This module provides LLM-based natural language understanding capabilities including:
- LLM adapter interface for unified model access
- Prompt templates for NLU tasks
- Semantic parsing
- Dialogue act classification
- Entity extraction and reference resolution
"""

from ibdm.nlu.llm_adapter import (
    LLMAdapter,
    LLMAPIError,
    LLMConfig,
    LLMError,
    LLMParsingError,
    LLMResponse,
    ModelType,
    create_adapter,
)

__all__ = [
    "LLMAdapter",
    "LLMConfig",
    "LLMResponse",
    "LLMError",
    "LLMAPIError",
    "LLMParsingError",
    "ModelType",
    "create_adapter",
]
