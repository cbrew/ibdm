"""Answer parsing and question-answer matching for dialogue management.

This module parses answers and matches them to questions on the QUD stack,
handling different answer types (direct, partial, over-informative, indirect).
"""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from ibdm.core.answers import Answer
from ibdm.core.questions import Question
from ibdm.nlu.llm_adapter import LLMAdapter, LLMConfig, ModelType
from ibdm.nlu.prompts import get_template

logger = logging.getLogger(__name__)


class AnswerType(str, Enum):
    """Types of answers based on how they address questions."""

    DIRECT = "direct"
    PARTIAL = "partial"
    OVER_INFORMATIVE = "over-informative"
    INDIRECT = "indirect"
    NON_ANSWER = "non-answer"


class AnswerAnalysis(BaseModel):
    """Result of answer parsing and analysis.

    Attributes:
        addresses_question: Whether the answer addresses the question
        answer_type: Type of answer (direct, partial, etc.)
        propositional_content: The information provided by the answer
        implied_info: Any implied or additional information
    """

    addresses_question: bool = Field(..., description="Whether answer addresses the question")
    answer_type: str = Field(..., description="Type of answer")
    propositional_content: str = Field(..., description="Information provided")
    implied_info: list[str] = Field(default_factory=list, description="Implied information")

    def get_type(self) -> AnswerType:
        """Convert answer_type string to AnswerType enum.

        Returns:
            AnswerType enum value

        Raises:
            ValueError: If answer_type is not a valid AnswerType
        """
        try:
            return AnswerType(self.answer_type)
        except ValueError as e:
            logger.error(f"CRITICAL: Invalid answer type: {self.answer_type!r}")
            raise ValueError(
                f"Cannot proceed with invalid answer type: {self.answer_type!r}"
            ) from e


@dataclass
class AnswerParserConfig:
    """Configuration for answer parser.

    Attributes:
        llm_config: Configuration for the LLM adapter
        include_reasoning: Whether to use chain-of-thought reasoning
        use_fast_model: Whether to use Haiku instead of Sonnet
    """

    llm_config: LLMConfig | None = None
    include_reasoning: bool = True
    use_fast_model: bool = False  # Answer parsing benefits from Sonnet


class AnswerParser:
    """Parser for analyzing answers and matching them to questions.

    Uses LLM-based analysis to determine how answers relate to questions,
    extract propositional content, and identify implied information.

    Example:
        >>> parser = AnswerParser()
        >>> question = "What time does the store close?"
        >>> answer_text = "It closes at 9pm."
        >>> result = parser.parse(question, answer_text)
        >>> print(result.answer_type, result.propositional_content)
        'direct' 'store closes at 9pm'
    """

    def __init__(self, config: AnswerParserConfig | None = None):
        """Initialize the answer parser.

        Args:
            config: Parser configuration. Uses defaults if not provided.
        """
        self.config = config or AnswerParserConfig()

        # Configure LLM
        llm_config = self.config.llm_config or LLMConfig(
            model=ModelType.HAIKU if self.config.use_fast_model else ModelType.SONNET,
            temperature=0.3,  # Lower temperature for consistent parsing
            max_tokens=2000,
        )

        self.llm = LLMAdapter(llm_config)
        self.template = get_template("answer_parsing")
        self.template.include_reasoning = self.config.include_reasoning

        logger.info(
            f"Initialized answer parser with model: {llm_config.model.value}, "
            f"reasoning: {self.config.include_reasoning}"
        )

    def parse(self, question_text: str, answer_text: str) -> AnswerAnalysis:
        """Parse an answer in relation to a question.

        Args:
            question_text: The question being answered
            answer_text: The answer text to analyze

        Returns:
            AnswerAnalysis with answer type and content

        Raises:
            LLMError: If parsing fails
        """
        # Combine question and answer for analysis
        input_text = f'Question: "{question_text}"\nAnswer: "{answer_text}"'

        # Format the prompt
        system_prompt, user_prompt = self.template.format(
            input_text=input_text, include_examples=True
        )

        logger.debug(f"Parsing answer: Q='{question_text}' A='{answer_text}'")

        # Call LLM with structured output
        result = self.llm.call_structured(
            prompt=user_prompt, response_model=AnswerAnalysis, system_prompt=system_prompt
        )

        logger.info(
            f"Parsed answer: type={result.answer_type}, addresses={result.addresses_question}, "
            f"implied_info={len(result.implied_info)}"
        )

        return result

    async def aparse(self, question_text: str, answer_text: str) -> AnswerAnalysis:
        """Async version of parse.

        Args:
            question_text: The question being answered
            answer_text: The answer text to analyze

        Returns:
            AnswerAnalysis with answer type and content

        Raises:
            LLMError: If parsing fails
        """
        input_text = f'Question: "{question_text}"\nAnswer: "{answer_text}"'

        system_prompt, user_prompt = self.template.format(
            input_text=input_text, include_examples=True
        )

        logger.debug(f"Async parsing answer: Q='{question_text}' A='{answer_text}'")

        result = await self.llm.acall_structured(
            prompt=user_prompt, response_model=AnswerAnalysis, system_prompt=system_prompt
        )

        logger.info(
            f"Async parsed answer: type={result.answer_type}, addresses={result.addresses_question}"
        )

        return result

    def to_answer_object(
        self,
        answer_text: str,
        question: Question | None = None,
        analysis: AnswerAnalysis | None = None,
        question_text: str | None = None,
    ) -> Answer:
        """Convert parsed answer to an Answer object.

        Args:
            answer_text: The answer text
            question: Optional Question object this answers
            analysis: Optional pre-computed analysis
            question_text: Optional question text (needed if analysis is None)

        Returns:
            Answer object with content and metadata

        Raises:
            ValueError: If analysis is None and question_text is None
            LLMError: If analysis is needed and fails
        """
        if analysis is None:
            if question_text is None:
                raise ValueError("Either analysis or question_text must be provided")
            analysis = self.parse(question_text, answer_text)

        # Determine certainty based on answer type
        certainty = 1.0
        if analysis.get_type() == AnswerType.PARTIAL:
            certainty = 0.7
        elif analysis.get_type() == AnswerType.INDIRECT:
            certainty = 0.8
        elif analysis.get_type() == AnswerType.NON_ANSWER:
            certainty = 0.0

        # Use propositional content as answer content
        content: Any = analysis.propositional_content

        # For yes/no questions, try to extract boolean
        if question and hasattr(question, "proposition"):  # YNQuestion
            content_lower = analysis.propositional_content.lower()
            if "yes" in content_lower or "true" in content_lower:
                content = True
            elif "no" in content_lower or "false" in content_lower:
                content = False

        return Answer(content=content, question_ref=question, certainty=certainty)

    def match_to_qud(
        self,
        answer_text: str,
        qud_stack: list[tuple[str, Question]],
        threshold: float = 0.5,
    ) -> tuple[Question | None, AnswerAnalysis | None]:
        """Match an answer to the most relevant question on the QUD stack.

        Args:
            answer_text: The answer text
            qud_stack: Stack of (question_text, Question) tuples
            threshold: Minimum threshold for matching

        Returns:
            Tuple of (matched_question, analysis) or (None, None) if no match

        Raises:
            LLMError: If parsing fails
        """
        if not qud_stack:
            logger.warning("QUD stack is empty, cannot match answer")
            return None, None

        # Try to match against questions in order (most recent first)
        for question_text, question in reversed(qud_stack):
            analysis = self.parse(question_text, answer_text)

            if analysis.addresses_question:
                logger.info(f"Matched answer to question: {question_text}")
                return question, analysis

        logger.warning("No matching question found on QUD stack")
        return None, None


def create_parser(use_fast_model: bool = False, include_reasoning: bool = True) -> AnswerParser:
    """Convenience function to create an answer parser.

    Args:
        use_fast_model: Whether to use Haiku (fast) instead of Sonnet
        include_reasoning: Whether to use chain-of-thought reasoning

    Returns:
        Configured AnswerParser instance

    Example:
        >>> # For production with detailed analysis
        >>> parser = create_parser(use_fast_model=False, include_reasoning=True)
        >>>
        >>> # For faster processing
        >>> parser = create_parser(use_fast_model=True, include_reasoning=False)
    """
    config = AnswerParserConfig(use_fast_model=use_fast_model, include_reasoning=include_reasoning)

    return AnswerParser(config)
