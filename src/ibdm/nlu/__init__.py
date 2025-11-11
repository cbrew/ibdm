"""Natural Language Understanding module for IBDM.

This module provides LLM-based natural language understanding capabilities including:
- LLM adapter interface for unified model access
- Prompt templates for NLU tasks
- Semantic parsing
- Dialogue act classification
- Question understanding and analysis
- Answer parsing and QUD matching
- Entity extraction and reference resolution
"""

from ibdm.nlu.answer_parser import (
    AnswerAnalysis,
    AnswerParser,
    AnswerParserConfig,
    AnswerType,
)
from ibdm.nlu.answer_parser import (
    create_parser as create_answer_parser,
)
from ibdm.nlu.dialogue_act_classifier import (
    DialogueActClassifier,
    DialogueActClassifierConfig,
    DialogueActResult,
    DialogueActType,
    create_classifier,
)
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
from ibdm.nlu.question_analyzer import (
    QuestionAnalysis,
    QuestionAnalyzer,
    QuestionAnalyzerConfig,
    QuestionType,
    create_analyzer,
)
from ibdm.nlu.semantic_parser import (
    SemanticArgument,
    SemanticModifier,
    SemanticParse,
    SemanticParser,
    SemanticParserConfig,
)
from ibdm.nlu.semantic_parser import (
    create_parser as create_semantic_parser,
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
    # Semantic Parser
    "SemanticParser",
    "SemanticParserConfig",
    "SemanticParse",
    "SemanticArgument",
    "SemanticModifier",
    "create_semantic_parser",
    # Dialogue Act Classifier
    "DialogueActClassifier",
    "DialogueActClassifierConfig",
    "DialogueActResult",
    "DialogueActType",
    "create_classifier",
    # Question Analyzer
    "QuestionAnalyzer",
    "QuestionAnalyzerConfig",
    "QuestionAnalysis",
    "QuestionType",
    "create_analyzer",
    # Answer Parser
    "AnswerParser",
    "AnswerParserConfig",
    "AnswerAnalysis",
    "AnswerType",
    "create_answer_parser",
]
