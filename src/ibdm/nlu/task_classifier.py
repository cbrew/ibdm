"""Task classification for domain-specific intent understanding.

This module provides LLM-based task classification to identify user intents
and map them to semantic task representations within specific domains.

Architecture:
    1. Domain Model: Semantic representation of dialogue domains
       - name: Domain identifier (e.g., "legal_documents")
       - supported_tasks: List of TaskType enums
       - task_signatures: Semantic signatures (e.g., "draft(doc_type, parties)")

    2. TaskClassifier: LLM-powered intent classifier
       - Uses Claude Haiku for fast classification (default)
       - Maps utterances → (task_type, domain, parameters, confidence)
       - Handles natural language variations robustly

    3. Integration with Rules: Rule preconditions use task classification
       - No keyword matching - pure semantic understanding
       - Confidence thresholding for reliability
       - Cached in state.private.beliefs to avoid redundant LLM calls

Example:
    Basic usage:
        >>> from ibdm.nlu.task_classifier import create_task_classifier
        >>> classifier = create_task_classifier()
        >>> result = classifier.classify("I need to draft an NDA")
        >>> print(result.task_type, result.parameters)
        'draft_document' {'document_type': 'NDA'}

    With custom domains:
        >>> from ibdm.nlu.task_classifier import Domain, TaskType
        >>> restaurant_domain = Domain(
        ...     name="restaurant_booking",
        ...     description="Restaurant reservation management",
        ...     supported_tasks=[TaskType.BOOK_SERVICE],
        ...     task_signatures={TaskType.BOOK_SERVICE: "book(restaurant, time, size)"}
        ... )
        >>> classifier = create_task_classifier(domains=[restaurant_domain])

    Integration with rules:
        >>> def _is_nda_request(state):
        ...     result = classifier.classify(state.private.beliefs["_temp_utterance"])
        ...     return (result.task_type == "draft_document"
        ...             and result.domain == "legal_documents"
        ...             and result.confidence >= 0.7)

See Also:
    - docs/TASK_CLASSIFICATION.md: Complete documentation
    - demos/RULE_DRIVEN_PLAN.md: Rule-driven dialogue architecture
    - src/ibdm/rules/interpretation_rules.py: Rule integration examples
"""

import logging
from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel, Field

from ibdm.nlu.llm_adapter import LLMAdapter, LLMConfig, ModelType

logger = logging.getLogger(__name__)


class TaskType(str, Enum):
    """Common task types across domains."""

    UNKNOWN = "unknown"
    DRAFT_DOCUMENT = "draft_document"
    REVIEW_DOCUMENT = "review_document"
    QUERY_INFORMATION = "query_information"
    BOOK_SERVICE = "book_service"
    CANCEL_SERVICE = "cancel_service"
    MODIFY_SERVICE = "modify_service"


@dataclass
class Domain:
    """Semantic representation of a dialogue domain.

    Attributes:
        name: Domain identifier (e.g., "legal_documents", "restaurant_booking")
        description: Natural language description of the domain
        supported_tasks: List of task types supported in this domain
        task_signatures: Mapping of task types to their semantic signatures
    """

    name: str
    description: str
    supported_tasks: list[TaskType]
    task_signatures: dict[TaskType, str]


# Predefined domains
LEGAL_DOCUMENTS_DOMAIN = Domain(
    name="legal_documents",
    description="Legal document drafting and review including NDAs, contracts, agreements",
    supported_tasks=[TaskType.DRAFT_DOCUMENT, TaskType.REVIEW_DOCUMENT],
    task_signatures={
        TaskType.DRAFT_DOCUMENT: "draft(document_type, parties, terms)",
        TaskType.REVIEW_DOCUMENT: "review(document_type, issues)",
    },
)


class TaskClassificationResult(BaseModel):
    """Result of task classification.

    Attributes:
        task_type: The identified task type
        domain: The domain this task belongs to
        confidence: Confidence score (0-1)
        parameters: Extracted task parameters (e.g., document_type="NDA")
    """

    task_type: str = Field(..., description="The task type")
    domain: str = Field(..., description="The domain identifier")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    parameters: dict[str, str] = Field(
        default_factory=dict, description="Extracted task parameters"
    )

    def to_enum(self) -> TaskType:
        """Convert task_type string to TaskType enum.

        Returns:
            TaskType enum value
        """
        try:
            return TaskType(self.task_type)
        except ValueError:
            logger.warning(f"Unknown task type: {self.task_type}, defaulting to UNKNOWN")
            return TaskType.UNKNOWN


@dataclass
class TaskClassifierConfig:
    """Configuration for task classifier.

    Attributes:
        llm_config: Configuration for the LLM adapter
        domains: List of domains to classify against
        confidence_threshold: Minimum confidence for classification
        use_fast_model: Whether to use Haiku for classification
    """

    llm_config: LLMConfig | None = None
    domains: list[Domain] | None = None
    confidence_threshold: float = 0.7
    use_fast_model: bool = True


class TaskClassifier:
    """LLM-based classifier for domain-specific tasks.

    Classifies user utterances into semantic task representations within
    specific domains. Uses few-shot prompting with domain knowledge to
    achieve high accuracy.

    Example:
        >>> classifier = TaskClassifier()
        >>> result = classifier.classify("I need to draft an NDA")
        >>> print(result.task_type, result.domain, result.parameters)
        'draft_document' 'legal_documents' {'document_type': 'NDA'}
    """

    def __init__(self, config: TaskClassifierConfig | None = None):
        """Initialize the task classifier.

        Args:
            config: Classifier configuration. Uses defaults if not provided.
        """
        self.config = config or TaskClassifierConfig()

        # Set default domains if not provided
        if not self.config.domains:
            self.config.domains = [LEGAL_DOCUMENTS_DOMAIN]

        # Configure LLM - use Haiku for fast classification
        llm_config = self.config.llm_config or LLMConfig(
            model=ModelType.HAIKU if self.config.use_fast_model else ModelType.SONNET,
            temperature=0.2,
            max_tokens=500,
        )

        self.llm = LLMAdapter(llm_config)

        logger.info(
            f"Initialized task classifier with {len(self.config.domains)} domains: "
            f"{[d.name for d in self.config.domains]}"
        )

    def classify(self, utterance: str) -> TaskClassificationResult:
        """Classify an utterance into a domain-specific task.

        Args:
            utterance: The utterance to classify

        Returns:
            TaskClassificationResult with task type, domain, and parameters

        Raises:
            LLMError: If classification fails
        """
        # Build domain descriptions for the prompt
        domain_descriptions = self._build_domain_descriptions()

        # Create classification prompt
        system_prompt = (
            "You are a task classifier for a dialogue system. "
            "Your job is to identify what task the user wants to perform "
            "and which domain it belongs to.\n\n"
            f"Available domains:\n{domain_descriptions}\n\n"
            "Analyze the utterance and determine:\n"
            "1. The task type (e.g., draft_document, query_information)\n"
            "2. The domain it belongs to\n"
            "3. Any relevant parameters (e.g., document_type, subject)\n"
            "4. Your confidence level (0.0 to 1.0)"
        )

        user_prompt = f"Classify this utterance:\n\n'{utterance}'"

        logger.debug(f"Classifying task for: {utterance}")

        # Call LLM with structured output
        result = self.llm.call_structured(
            prompt=user_prompt, response_model=TaskClassificationResult, system_prompt=system_prompt
        )

        logger.info(
            f"Classified '{utterance}' as {result.task_type} in {result.domain} "
            f"(confidence: {result.confidence})"
        )

        return result

    async def aclassify(self, utterance: str) -> TaskClassificationResult:
        """Async version of classify.

        Args:
            utterance: The utterance to classify

        Returns:
            TaskClassificationResult
        """
        domain_descriptions = self._build_domain_descriptions()

        system_prompt = (
            "You are a task classifier for a dialogue system. "
            "Your job is to identify what task the user wants to perform "
            "and which domain it belongs to.\n\n"
            f"Available domains:\n{domain_descriptions}\n\n"
            "Analyze the utterance and determine:\n"
            "1. The task type (e.g., draft_document, query_information)\n"
            "2. The domain it belongs to\n"
            "3. Any relevant parameters (e.g., document_type, subject)\n"
            "4. Your confidence level (0.0 to 1.0)"
        )

        user_prompt = f"Classify this utterance:\n\n'{utterance}'"

        result = await self.llm.acall_structured(
            prompt=user_prompt, response_model=TaskClassificationResult, system_prompt=system_prompt
        )

        return result

    def is_high_confidence(self, result: TaskClassificationResult) -> bool:
        """Check if classification result has high confidence.

        Args:
            result: The classification result

        Returns:
            True if confidence meets threshold
        """
        return result.confidence >= self.config.confidence_threshold

    def _build_domain_descriptions(self) -> str:
        """Build formatted domain descriptions for the prompt.

        Returns:
            Formatted string describing all configured domains
        """
        if not self.config.domains:
            return "No domains configured"

        lines: list[str] = []
        for domain in self.config.domains:
            lines.append(f"- {domain.name}: {domain.description}")
            task_names = ", ".join(t.value for t in domain.supported_tasks)
            lines.append(f"  Supported tasks: {task_names}")

        return "\n".join(lines)


def create_task_classifier(
    domains: list[Domain] | None = None,
    use_fast_model: bool = True,
    confidence_threshold: float = 0.7,
) -> TaskClassifier:
    """Convenience function to create a task classifier.

    Args:
        domains: List of domains to support. Uses legal documents domain if None.
        use_fast_model: Whether to use Haiku (fast) instead of Sonnet
        confidence_threshold: Minimum confidence for classification

    Returns:
        Configured TaskClassifier instance

    Example:
        >>> # For legal documents domain
        >>> classifier = create_task_classifier()
        >>>
        >>> # For multiple domains
        >>> classifier = create_task_classifier(domains=[legal_domain, booking_domain])
    """
    config = TaskClassifierConfig(
        domains=domains, use_fast_model=use_fast_model, confidence_threshold=confidence_threshold
    )

    return TaskClassifier(config)
