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
from ibdm.nlu.prompts import (
    Example,
    PromptTemplate,
    create_answer_parsing_template,
    create_dialogue_act_template,
    create_entity_extraction_template,
    create_question_understanding_template,
    create_reference_resolution_template,
    create_semantic_parsing_template,
    get_template,
    list_templates,
)

__all__ = [
    # LLM Adapter
    "LLMAdapter",
    "LLMConfig",
    "LLMResponse",
    "LLMError",
    "LLMAPIError",
    "LLMParsingError",
    "ModelType",
    "create_adapter",
    # Prompt Templates
    "Example",
    "PromptTemplate",
    "create_answer_parsing_template",
    "create_dialogue_act_template",
    "create_entity_extraction_template",
    "create_question_understanding_template",
    "create_reference_resolution_template",
    "create_semantic_parsing_template",
    "get_template",
    "list_templates",
]
