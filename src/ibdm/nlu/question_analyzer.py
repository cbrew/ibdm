"""Question understanding and classification for analyzing question semantics.

This module provides deep analysis of questions including type classification,
focus identification, presupposition extraction, and constraint detection.
"""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from ibdm.core.questions import AltQuestion, Question, WhQuestion, YNQuestion
from ibdm.nlu.llm_adapter import LLMAdapter, LLMConfig, ModelType
from ibdm.nlu.prompts import get_template

logger = logging.getLogger(__name__)


class QuestionType(str, Enum):
    """Types of questions."""

    WH = "wh"
    YES_NO = "yes-no"
    ALTERNATIVE = "alternative"
    RHETORICAL = "rhetorical"


class QuestionAnalysis(BaseModel):
    """Result of deep question understanding.

    Attributes:
        type: The question type (wh, yes-no, alternative, rhetorical)
        focus: What the question is asking about
        presuppositions: Assumptions the question makes
        constraints: Implicit constraints or preferences
    """

    type: str = Field(..., description="Question type")
    focus: str = Field(..., description="What the question asks about")
    presuppositions: list[str] = Field(default_factory=list, description="Question presuppositions")
    constraints: list[str] = Field(default_factory=list, description="Implicit constraints")

    def get_type(self) -> QuestionType:
        """Convert type string to QuestionType enum.

        Returns:
            QuestionType enum value
        """
        try:
            return QuestionType(self.type)
        except ValueError:
            logger.warning(f"Unknown question type: {self.type}, defaulting to WH")
            return QuestionType.WH


@dataclass
class QuestionAnalyzerConfig:
    """Configuration for question analyzer.

    Attributes:
        llm_config: Configuration for the LLM adapter
        include_reasoning: Whether to use chain-of-thought reasoning
        use_fast_model: Whether to use Haiku instead of Sonnet
    """

    llm_config: LLMConfig | None = None
    include_reasoning: bool = True
    use_fast_model: bool = False  # Question understanding benefits from Sonnet


class QuestionAnalyzer:
    """Analyzer for deep question understanding.

    Uses LLM-based analysis to extract semantic structure from questions including
    type, focus, presuppositions, and constraints.

    Example:
        >>> analyzer = QuestionAnalyzer()
        >>> result = analyzer.analyze("What's the best Italian restaurant in downtown?")
        >>> print(result.type, result.focus)
        'wh' 'Italian restaurant'
        >>> print(result.constraints)
        ['Location: downtown', 'Cuisine: Italian', 'Quality: best']
    """

    def __init__(self, config: QuestionAnalyzerConfig | None = None):
        """Initialize the question analyzer.

        Args:
            config: Analyzer configuration. Uses defaults if not provided.
        """
        self.config = config or QuestionAnalyzerConfig()

        # Configure LLM
        llm_config = self.config.llm_config or LLMConfig(
            model=ModelType.HAIKU if self.config.use_fast_model else ModelType.SONNET,
            temperature=0.3,  # Lower temperature for consistent analysis
            max_tokens=2000,
        )

        self.llm = LLMAdapter(llm_config)
        self.template = get_template("question_understanding")
        self.template.include_reasoning = self.config.include_reasoning

        logger.info(
            f"Initialized question analyzer with model: {llm_config.model.value}, "
            f"reasoning: {self.config.include_reasoning}"
        )

    def analyze(self, question_text: str) -> QuestionAnalysis:
        """Analyze a question to extract its semantic structure.

        Args:
            question_text: The question text to analyze

        Returns:
            QuestionAnalysis with type, focus, presuppositions, and constraints

        Raises:
            LLMError: If analysis fails
        """
        # Format the prompt
        system_prompt, user_prompt = self.template.format(
            input_text=question_text, include_examples=True
        )

        logger.debug(f"Analyzing question: {question_text}")

        # Call LLM with structured output
        result = self.llm.call_structured(
            prompt=user_prompt, response_model=QuestionAnalysis, system_prompt=system_prompt
        )

        logger.info(
            f"Analyzed '{question_text}' -> type: {result.type}, focus: {result.focus}, "
            f"{len(result.presuppositions)} presuppositions, {len(result.constraints)} constraints"
        )

        return result

    async def aanalyze(self, question_text: str) -> QuestionAnalysis:
        """Async version of analyze.

        Args:
            question_text: The question text to analyze

        Returns:
            QuestionAnalysis with type, focus, presuppositions, and constraints

        Raises:
            LLMError: If analysis fails
        """
        system_prompt, user_prompt = self.template.format(
            input_text=question_text, include_examples=True
        )

        logger.debug(f"Async analyzing question: {question_text}")

        result = await self.llm.acall_structured(
            prompt=user_prompt, response_model=QuestionAnalysis, system_prompt=system_prompt
        )

        logger.info(
            f"Async analyzed '{question_text}' -> type: {result.type}, focus: {result.focus}"
        )

        return result

    async def batch_analyze(self, questions: list[str]) -> list[QuestionAnalysis]:
        """Analyze multiple questions in parallel.

        Args:
            questions: List of question texts to analyze

        Returns:
            List of QuestionAnalysis results in the same order as input

        Raises:
            LLMError: If any analysis fails
        """
        import asyncio

        tasks = [self.aanalyze(question) for question in questions]
        return await asyncio.gather(*tasks)

    def to_question_object(
        self, question_text: str, analysis: QuestionAnalysis | None = None
    ) -> Question:
        """Convert analyzed question to a Question object.

        Args:
            question_text: The original question text
            analysis: Optional pre-computed analysis. If not provided, will analyze.

        Returns:
            Question object (WhQuestion, YNQuestion, or AltQuestion)

        Raises:
            LLMError: If analysis is needed and fails
        """
        if analysis is None:
            analysis = self.analyze(question_text)

        question_type = analysis.get_type()

        # Convert constraints to dict
        constraints_dict: dict[str, Any] = {}
        for constraint in analysis.constraints:
            if ":" in constraint:
                key, value = constraint.split(":", 1)
                constraints_dict[key.strip().lower()] = value.strip()

        if question_type == QuestionType.WH:
            # Extract variable from focus
            variable = "x"  # Default variable
            predicate = analysis.focus

            return WhQuestion(variable=variable, predicate=predicate, constraints=constraints_dict)

        elif question_type == QuestionType.YES_NO:
            return YNQuestion(proposition=analysis.focus, parameters=constraints_dict)

        elif question_type == QuestionType.ALTERNATIVE:
            # Try to extract alternatives from constraints
            alternatives = [c for c in analysis.constraints if ":" not in c]

            if not alternatives:
                # Fallback: try to parse from focus
                alternatives = [alt.strip() for alt in analysis.focus.split(" or ")]

            return AltQuestion(alternatives=alternatives)

        else:  # RHETORICAL - treat as assertion, but represent as WhQuestion
            return WhQuestion(variable="x", predicate=analysis.focus, constraints=constraints_dict)


def create_analyzer(
    use_fast_model: bool = False, include_reasoning: bool = True
) -> QuestionAnalyzer:
    """Convenience function to create a question analyzer.

    Args:
        use_fast_model: Whether to use Haiku (fast) instead of Sonnet
        include_reasoning: Whether to use chain-of-thought reasoning

    Returns:
        Configured QuestionAnalyzer instance

    Example:
        >>> # For production with detailed analysis
        >>> analyzer = create_analyzer(use_fast_model=False, include_reasoning=True)
        >>>
        >>> # For faster processing
        >>> analyzer = create_analyzer(use_fast_model=True, include_reasoning=False)
    """
    config = QuestionAnalyzerConfig(
        use_fast_model=use_fast_model, include_reasoning=include_reasoning
    )

    return QuestionAnalyzer(config)
