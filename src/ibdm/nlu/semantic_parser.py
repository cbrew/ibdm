"""Semantic parsing for converting natural language utterances to structured dialogue moves.

This module uses LLM-based parsing to convert natural language utterances into
structured DialogueMove representations with predicates, arguments, and semantic roles.
"""

import logging
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, Field

from ibdm.nlu.llm_adapter import LLMAdapter, LLMConfig, ModelType
from ibdm.nlu.prompts import get_template

logger = logging.getLogger(__name__)


class SemanticArgument(BaseModel):
    """A semantic argument with role and value.

    Attributes:
        role: The semantic role (agent, patient, theme, location, etc.)
        value: The argument value
    """

    role: str = Field(..., description="Semantic role of the argument")
    value: str = Field(..., description="Value of the argument")


class SemanticModifier(BaseModel):
    """A semantic modifier.

    Attributes:
        type: The modifier type (time, manner, degree, location, etc.)
        value: The modifier value
    """

    type: str = Field(..., description="Type of modifier")
    value: str = Field(..., description="Value of the modifier")


class SemanticParse(BaseModel):
    """Structured semantic parse result.

    Attributes:
        predicate: The main predicate (action, state, or relation)
        arguments: List of semantic arguments with roles
        modifiers: List of modifiers
    """

    predicate: str = Field(..., description="Main predicate")
    arguments: list[SemanticArgument] = Field(
        default_factory=list, description="Semantic arguments"
    )
    modifiers: list[SemanticModifier] = Field(default_factory=list, description="Modifiers")


@dataclass
class SemanticParserConfig:
    """Configuration for semantic parser.

    Attributes:
        llm_config: Configuration for the LLM adapter
        include_reasoning: Whether to use chain-of-thought reasoning
        use_fast_model: Whether to use Haiku instead of Sonnet
    """

    llm_config: LLMConfig | None = None
    include_reasoning: bool = True
    use_fast_model: bool = False


class SemanticParser:
    """Parser for converting natural language to structured semantic representations.

    Uses LLM-based parsing with prompt templates to extract predicates, arguments,
    and semantic roles from utterances.

    Example:
        >>> parser = SemanticParser()
        >>> result = parser.parse("Alice quickly drove to the airport yesterday.")
        >>> print(result.predicate)
        'drive'
        >>> print(result.arguments[0].role, result.arguments[0].value)
        'agent' 'Alice'
    """

    def __init__(self, config: SemanticParserConfig | None = None):
        """Initialize the semantic parser.

        Args:
            config: Parser configuration. Uses defaults if not provided.
        """
        self.config = config or SemanticParserConfig()

        # Configure LLM
        llm_config = self.config.llm_config or LLMConfig(
            model=ModelType.HAIKU if self.config.use_fast_model else ModelType.SONNET,
            temperature=0.3,  # Lower temperature for more consistent parsing
            max_tokens=2000,
        )

        self.llm = LLMAdapter(llm_config)
        self.template = get_template("semantic_parsing")
        self.template.include_reasoning = self.config.include_reasoning

        logger.info(
            f"Initialized semantic parser with model: {llm_config.model.value}, "
            f"reasoning: {self.config.include_reasoning}"
        )

    def parse(self, utterance: str, context: dict[str, Any] | None = None) -> SemanticParse:
        """Parse an utterance into a structured semantic representation.

        Args:
            utterance: The natural language utterance to parse
            context: Optional contextual information for disambiguation

        Returns:
            SemanticParse with predicate, arguments, and modifiers

        Raises:
            LLMError: If parsing fails
        """
        # Format the prompt with the template
        system_prompt, user_prompt = self.template.format(
            input_text=utterance, variables=context, include_examples=True
        )

        logger.debug(f"Parsing utterance: {utterance}")

        # Call LLM with structured output
        result = self.llm.call_structured(
            prompt=user_prompt, response_model=SemanticParse, system_prompt=system_prompt
        )

        logger.info(
            f"Parsed '{utterance}' -> predicate: {result.predicate}, "
            f"{len(result.arguments)} args, {len(result.modifiers)} modifiers"
        )

        return result

    async def aparse(self, utterance: str, context: dict[str, Any] | None = None) -> SemanticParse:
        """Async version of parse.

        Args:
            utterance: The natural language utterance to parse
            context: Optional contextual information for disambiguation

        Returns:
            SemanticParse with predicate, arguments, and modifiers

        Raises:
            LLMError: If parsing fails
        """
        system_prompt, user_prompt = self.template.format(
            input_text=utterance, variables=context, include_examples=True
        )

        logger.debug(f"Async parsing utterance: {utterance}")

        result = await self.llm.acall_structured(
            prompt=user_prompt, response_model=SemanticParse, system_prompt=system_prompt
        )

        logger.info(
            f"Async parsed '{utterance}' -> predicate: {result.predicate}, "
            f"{len(result.arguments)} args, {len(result.modifiers)} modifiers"
        )

        return result

    async def batch_parse(
        self, utterances: list[str], context: dict[str, Any] | None = None
    ) -> list[SemanticParse]:
        """Parse multiple utterances in parallel.

        Args:
            utterances: List of utterances to parse
            context: Optional contextual information

        Returns:
            List of SemanticParse results in the same order as input

        Raises:
            LLMError: If any parse fails
        """
        import asyncio

        tasks = [self.aparse(utterance, context) for utterance in utterances]
        return await asyncio.gather(*tasks)


def create_parser(use_fast_model: bool = False, include_reasoning: bool = True) -> SemanticParser:
    """Convenience function to create a semantic parser.

    Args:
        use_fast_model: Whether to use Haiku (fast) instead of Sonnet
        include_reasoning: Whether to use chain-of-thought reasoning

    Returns:
        Configured SemanticParser instance

    Example:
        >>> # For production with fast responses
        >>> parser = create_parser(use_fast_model=True, include_reasoning=False)
        >>>
        >>> # For development/debugging with detailed reasoning
        >>> parser = create_parser(use_fast_model=False, include_reasoning=True)
    """
    config = SemanticParserConfig(
        use_fast_model=use_fast_model, include_reasoning=include_reasoning
    )

    return SemanticParser(config)
