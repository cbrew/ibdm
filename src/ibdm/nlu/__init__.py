"""Natural Language Understanding module for IBDM.

This module provides LLM-based natural language understanding capabilities including:
- LLM adapter interface for unified model access
- Prompt templates for NLU tasks
- Semantic parsing
- Dialogue act classification
- Question understanding and analysis
- Answer parsing and QUD matching
- Context-aware interpretation pipeline
- Implicature detection and topic tracking
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

# Import base NLU service interface
from ibdm.nlu.base_nlu_service import (  # noqa: I001
    ActionRequest,
    AmbiguityInfo,
    BaseNLUService,
    ExtractedFact,
    MultiFact,
    NLUConfidence,
    RequestType,
    UserPreference,
)
from ibdm.nlu.context_interpreter import (
    ContextInterpreter,
    ContextInterpreterConfig,
    ContextualInterpretation,
    ImplicatureType,
    TopicShiftType,
    create_interpreter,
)
from ibdm.nlu.dialogue_act_classifier import (
    DialogueActClassifier,
    DialogueActClassifierConfig,
    DialogueActResult,
    DialogueActType,
    create_classifier,
)
from ibdm.nlu.entity_extractor import (
    Entity,
    EntityExtractionResult,
    EntityExtractor,
    EntityExtractorConfig,
    EntityTracker,
    EntityTrackerConfig,
    EntityType,
    create_extractor,
    create_tracker,
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
from ibdm.nlu.nlu_context import NLUContext

# Import at end to avoid circular import with nlu_engine
from ibdm.nlu.nlu_engine import NLUEngine, NLUEngineConfig, create_nlu_engine  # noqa: E402, I001

# Import nlu_result first (nlu_engine import moved to end to avoid circular import)
from ibdm.nlu.nlu_result import NLUResult  # noqa: I001

# Import NLU service adapter
from ibdm.nlu.nlu_service_adapter import (  # noqa: I001, E402
    NLUServiceAdapter,
    create_nlu_service,
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
from ibdm.nlu.reference_resolver import (
    Reference,
    ReferenceResolution,
    ReferenceResolver,
    ReferenceResolverConfig,
    ReferenceType,
    create_resolver,
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
    # Base NLU Service Interface
    "BaseNLUService",
    "NLUConfidence",
    "AmbiguityInfo",
    "ExtractedFact",
    "MultiFact",
    "ActionRequest",
    "RequestType",
    "UserPreference",
    # NLU Service Adapter
    "NLUServiceAdapter",
    "create_nlu_service",
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
    # Context Interpreter
    "ContextInterpreter",
    "ContextInterpreterConfig",
    "ContextualInterpretation",
    "ImplicatureType",
    "TopicShiftType",
    "create_interpreter",
    # Entity Extraction and Tracking
    "Entity",
    "EntityExtractor",
    "EntityExtractorConfig",
    "EntityExtractionResult",
    "EntityTracker",
    "EntityTrackerConfig",
    "EntityType",
    "create_extractor",
    "create_tracker",
    # Reference Resolution
    "Reference",
    "ReferenceResolution",
    "ReferenceResolver",
    "ReferenceResolverConfig",
    "ReferenceType",
    "create_resolver",
    # NLU Result
    "NLUResult",
    # NLU Engine
    "NLUEngine",
    "NLUEngineConfig",
    "create_nlu_engine",
    # NLU Context
    "NLUContext",
]
