"""Dialogue act classification for identifying communicative functions of utterances.

This module classifies utterances into dialogue acts (question, answer, assertion, command, etc.)
to determine the speaker's communicative intention.
"""

import logging
from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel, Field

from ibdm.nlu.llm_adapter import LLMAdapter, LLMConfig, ModelType
from ibdm.nlu.prompts import get_template

logger = logging.getLogger(__name__)


class DialogueActType(str, Enum):
    """Types of dialogue acts supported by the classifier."""

    QUESTION = "question"
    ANSWER = "answer"
    ASSERTION = "assertion"
    COMMAND = "command"
    ACKNOWLEDGMENT = "acknowledgment"
    CLARIFICATION = "clarification"
    GREETING = "greeting"
    OTHER = "other"


class DialogueActResult(BaseModel):
    """Result of dialogue act classification.

    Attributes:
        act: The classified dialogue act type
        confidence: Confidence score (0-1)
    """

    act: str = Field(..., description="The dialogue act type")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")

    def to_enum(self) -> DialogueActType:
        """Convert act string to DialogueActType enum.

        Returns:
            DialogueActType enum value

        Raises:
            ValueError: If act is not a valid DialogueActType
        """
        try:
            return DialogueActType(self.act)
        except ValueError as e:
            logger.error(f"CRITICAL: Invalid dialogue act type: {self.act!r}")
            raise ValueError(f"Cannot proceed with invalid dialogue act: {self.act!r}") from e


@dataclass
class DialogueActClassifierConfig:
    """Configuration for dialogue act classifier.

    Attributes:
        llm_config: Configuration for the LLM adapter
        confidence_threshold: Minimum confidence for classification
        use_fast_model: Whether to use Haiku instead of Sonnet
    """

    llm_config: LLMConfig | None = None
    confidence_threshold: float = 0.5
    use_fast_model: bool = True  # Dialogue act classification is fast, use Haiku


class DialogueActClassifier:
    """Classifier for dialogue acts.

    Uses LLM-based classification to identify the communicative function of utterances.
    Optimized for fast classification using Haiku model by default.

    Example:
        >>> classifier = DialogueActClassifier()
        >>> result = classifier.classify("What's the weather like tomorrow?")
        >>> print(result.act, result.confidence)
        'question' 0.95
    """

    def __init__(self, config: DialogueActClassifierConfig | None = None):
        """Initialize the dialogue act classifier.

        Args:
            config: Classifier configuration. Uses defaults if not provided.
        """
        self.config = config or DialogueActClassifierConfig()

        # Configure LLM - use Haiku by default for fast classification
        llm_config = self.config.llm_config or LLMConfig(
            model=ModelType.HAIKU if self.config.use_fast_model else ModelType.SONNET,
            temperature=0.2,  # Lower temperature for consistent classification
            max_tokens=500,  # Short responses for classification
        )

        self.llm = LLMAdapter(llm_config)
        self.template = get_template("dialogue_act")

        logger.info(
            f"Initialized dialogue act classifier with model: {llm_config.model.value}, "
            f"confidence threshold: {self.config.confidence_threshold}"
        )

    def classify(self, utterance: str) -> DialogueActResult:
        """Classify an utterance into a dialogue act.

        Args:
            utterance: The utterance to classify

        Returns:
            DialogueActResult with act type and confidence score

        Raises:
            LLMError: If classification fails
        """
        # Format the prompt
        system_prompt, user_prompt = self.template.format(
            input_text=utterance, include_examples=True
        )

        logger.debug(f"Classifying utterance: {utterance}")

        # Call LLM with structured output
        result = self.llm.call_structured(
            prompt=user_prompt, response_model=DialogueActResult, system_prompt=system_prompt
        )

        logger.info(f"Classified '{utterance}' as {result.act} (confidence: {result.confidence})")

        return result

    async def aclassify(self, utterance: str) -> DialogueActResult:
        """Async version of classify.

        Args:
            utterance: The utterance to classify

        Returns:
            DialogueActResult with act type and confidence score

        Raises:
            LLMError: If classification fails
        """
        system_prompt, user_prompt = self.template.format(
            input_text=utterance, include_examples=True
        )

        logger.debug(f"Async classifying utterance: {utterance}")

        result = await self.llm.acall_structured(
            prompt=user_prompt, response_model=DialogueActResult, system_prompt=system_prompt
        )

        logger.info(
            f"Async classified '{utterance}' as {result.act} (confidence: {result.confidence})"
        )

        return result

    async def batch_classify(self, utterances: list[str]) -> list[DialogueActResult]:
        """Classify multiple utterances in parallel.

        Args:
            utterances: List of utterances to classify

        Returns:
            List of DialogueActResult in the same order as input

        Raises:
            LLMError: If any classification fails
        """
        import asyncio

        tasks = [self.aclassify(utterance) for utterance in utterances]
        return await asyncio.gather(*tasks)

    def is_high_confidence(self, result: DialogueActResult) -> bool:
        """Check if classification result has high confidence.

        Args:
            result: The classification result

        Returns:
            True if confidence meets threshold
        """
        return result.confidence >= self.config.confidence_threshold


def create_classifier(
    use_fast_model: bool = True, confidence_threshold: float = 0.5
) -> DialogueActClassifier:
    """Convenience function to create a dialogue act classifier.

    Args:
        use_fast_model: Whether to use Haiku (fast) instead of Sonnet
        confidence_threshold: Minimum confidence for classification

    Returns:
        Configured DialogueActClassifier instance

    Example:
        >>> # For production with fast classification
        >>> classifier = create_classifier(use_fast_model=True)
        >>>
        >>> # For higher accuracy with stricter threshold
        >>> classifier = create_classifier(use_fast_model=False, confidence_threshold=0.8)
    """
    config = DialogueActClassifierConfig(
        use_fast_model=use_fast_model, confidence_threshold=confidence_threshold
    )

    return DialogueActClassifier(config)
