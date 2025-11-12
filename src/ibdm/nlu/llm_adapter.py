"""LLM adapter interface for IBDM natural language understanding.

This module provides a unified interface to interact with LLMs (primarily Claude 4.5 models)
through LiteLLM. It handles API key management, model selection, error handling, and response
parsing.

Model Selection Guidelines:
- claude-sonnet-4-5-20250929: Large-scale generation, complex reasoning, extended responses
- claude-haiku-4-5-20251001: Control flow, analytics, classification, structured data
"""

import asyncio
import json
import logging
import os
from dataclasses import dataclass
from enum import Enum
from typing import Literal, TypeVar, cast

from litellm import acompletion, completion  # type: ignore[import-untyped]
from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class ModelType(str, Enum):
    """Supported Claude model types."""

    SONNET = "claude-sonnet-4-5-20250929"  # For complex reasoning and generation
    HAIKU = "claude-haiku-4-5-20251001"  # For fast classification and analytics


@dataclass
class LLMConfig:
    """Configuration for LLM adapter.

    Attributes:
        model: The model to use (Sonnet or Haiku)
        temperature: Sampling temperature (0.0-1.0)
        max_tokens: Maximum tokens in response
        timeout: Request timeout in seconds
        max_retries: Maximum number of retry attempts
    """

    model: ModelType = ModelType.SONNET
    temperature: float = 0.7
    max_tokens: int = 8000
    timeout: int = 60
    max_retries: int = 3


@dataclass
class LLMResponse:
    """Response from LLM call.

    Attributes:
        content: The response text
        model: The model that generated the response
        tokens_used: Total tokens consumed
        prompt_tokens: Tokens in the prompt
        completion_tokens: Tokens in the completion
    """

    content: str
    model: str
    tokens_used: int
    prompt_tokens: int
    completion_tokens: int


class LLMError(Exception):
    """Base exception for LLM-related errors."""

    pass


class LLMAPIError(LLMError):
    """API-related error (network, authentication, etc.)."""

    pass


class LLMParsingError(LLMError):
    """Error parsing LLM response."""

    pass


class LLMAdapter:
    """Unified interface for LLM interactions in IBDM.

    This adapter provides:
    - Consistent API across different LLM models
    - Automatic retry logic with exponential backoff
    - Structured output parsing and validation
    - Both sync and async operation modes
    - Token usage tracking

    Example:
        >>> adapter = LLMAdapter(LLMConfig(model=ModelType.HAIKU))
        >>> response = adapter.call("What is 2+2?")
        >>> print(response.content)
        "4"

        >>> # With structured output
        >>> class Answer(BaseModel):
        ...     result: int
        ...     explanation: str
        >>> answer = adapter.call_structured("What is 2+2?", Answer)
        >>> print(answer.result)
        4
    """

    def __init__(self, config: LLMConfig | None = None):
        """Initialize the LLM adapter.

        Args:
            config: Configuration for the adapter. Uses defaults if not provided.

        Raises:
            ValueError: If IBDM_API_KEY environment variable is not set.
        """
        self.config = config or LLMConfig()
        self.api_key = os.getenv("IBDM_API_KEY")

        if not self.api_key:
            raise ValueError(
                "IBDM_API_KEY not found in environment. "
                "Please set the IBDM_API_KEY environment variable."
            )

        # Track last response for token usage monitoring
        self.last_response: LLMResponse | None = None

        logger.info(f"Initialized LLM adapter with model: {self.config.model.value}")

    def call(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        """Make a synchronous call to the LLM.

        Args:
            prompt: The user prompt/question
            system_prompt: Optional system prompt to set context
            temperature: Override default temperature
            max_tokens: Override default max_tokens

        Returns:
            LLMResponse with the model's response and metadata

        Raises:
            LLMAPIError: If the API call fails after retries
        """
        messages: list[dict[str, str]] = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        temp = temperature if temperature is not None else self.config.temperature
        max_tok = max_tokens if max_tokens is not None else self.config.max_tokens

        for attempt in range(self.config.max_retries):
            try:
                response = completion(
                    model=self.config.model.value,
                    messages=messages,
                    api_key=self.api_key,
                    temperature=temp,
                    max_tokens=max_tok,
                    timeout=self.config.timeout,
                )

                content = response.choices[0].message.content  # type: ignore[union-attr]
                usage = response.usage  # type: ignore[attr-defined]

                logger.debug(
                    f"LLM call successful. Tokens: {usage.total_tokens} "  # type: ignore[attr-defined]
                    f"(prompt: {usage.prompt_tokens}, completion: {usage.completion_tokens})"  # type: ignore[attr-defined]
                )

                llm_response = LLMResponse(
                    content=cast(str, content or ""),
                    model=self.config.model.value,
                    tokens_used=usage.total_tokens,  # type: ignore[attr-defined]
                    prompt_tokens=usage.prompt_tokens,  # type: ignore[attr-defined]
                    completion_tokens=usage.completion_tokens,  # type: ignore[attr-defined]
                )

                # Store last response for token tracking
                self.last_response = llm_response

                return llm_response

            except Exception as e:
                logger.warning(f"LLM call attempt {attempt + 1} failed: {e}")

                if attempt == self.config.max_retries - 1:
                    raise LLMAPIError(
                        f"LLM API call failed after {self.config.max_retries} attempts: {e}"
                    )

                # Exponential backoff
                wait_time = 2**attempt
                logger.info(f"Retrying in {wait_time} seconds...")
                import time

                time.sleep(wait_time)

        raise LLMAPIError("Unexpected error in retry loop")

    async def acall(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        """Make an asynchronous call to the LLM.

        Args:
            prompt: The user prompt/question
            system_prompt: Optional system prompt to set context
            temperature: Override default temperature
            max_tokens: Override default max_tokens

        Returns:
            LLMResponse with the model's response and metadata

        Raises:
            LLMAPIError: If the API call fails after retries
        """
        messages: list[dict[str, str]] = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        temp = temperature if temperature is not None else self.config.temperature
        max_tok = max_tokens if max_tokens is not None else self.config.max_tokens

        for attempt in range(self.config.max_retries):
            try:
                response = await acompletion(
                    model=self.config.model.value,
                    messages=messages,
                    api_key=self.api_key,
                    temperature=temp,
                    max_tokens=max_tok,
                    timeout=self.config.timeout,
                )

                content = response.choices[0].message.content  # type: ignore[union-attr]
                usage = response.usage  # type: ignore[attr-defined]

                logger.debug(
                    f"Async LLM call successful. Tokens: {usage.total_tokens} "  # type: ignore[attr-defined]
                    f"(prompt: {usage.prompt_tokens}, completion: {usage.completion_tokens})"  # type: ignore[attr-defined]
                )

                llm_response = LLMResponse(
                    content=cast(str, content or ""),
                    model=self.config.model.value,
                    tokens_used=usage.total_tokens,  # type: ignore[attr-defined]
                    prompt_tokens=usage.prompt_tokens,  # type: ignore[attr-defined]
                    completion_tokens=usage.completion_tokens,  # type: ignore[attr-defined]
                )

                # Store last response for token tracking
                self.last_response = llm_response

                return llm_response

            except Exception as e:
                logger.warning(f"Async LLM call attempt {attempt + 1} failed: {e}")

                if attempt == self.config.max_retries - 1:
                    raise LLMAPIError(
                        f"Async LLM API call failed after {self.config.max_retries} attempts: {e}"
                    )

                # Exponential backoff
                wait_time = 2**attempt
                logger.info(f"Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)

        raise LLMAPIError("Unexpected error in retry loop")

    def call_structured(
        self,
        prompt: str,
        response_model: type[T],
        system_prompt: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> T:
        """Make an LLM call and parse the response into a structured Pydantic model.

        The LLM is instructed to return JSON matching the provided Pydantic model schema.
        If parsing fails, retries with corrective feedback.

        Args:
            prompt: The user prompt/question
            response_model: Pydantic model class to parse response into
            system_prompt: Optional system prompt to set context
            temperature: Override default temperature
            max_tokens: Override default max_tokens

        Returns:
            Instance of response_model populated with parsed data

        Raises:
            LLMParsingError: If response cannot be parsed after retries
            LLMAPIError: If the API call fails
        """
        # Add JSON schema instruction to system prompt
        schema_json = response_model.model_json_schema()
        schema_str = json.dumps(schema_json, indent=2)
        schema_instruction = f"\n\nRespond with valid JSON matching this schema:\n{schema_str}"

        enhanced_system_prompt = (system_prompt or "") + schema_instruction

        max_parse_attempts = 2

        for parse_attempt in range(max_parse_attempts):
            response = self.call(
                prompt=prompt,
                system_prompt=enhanced_system_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            try:
                # Try to extract JSON from response (may be wrapped in markdown code blocks)
                content = response.content.strip()

                # Remove markdown code blocks if present
                if content.startswith("```"):
                    # Find the first and last ``` markers
                    lines = content.split("\n")
                    start_idx = 0
                    end_idx = len(lines)

                    for i, line in enumerate(lines):
                        if line.startswith("```"):
                            if start_idx == 0:
                                start_idx = i + 1
                            else:
                                end_idx = i
                                break

                    content = "\n".join(lines[start_idx:end_idx]).strip()

                # Parse JSON
                data = json.loads(content)

                # Validate against Pydantic model
                return response_model.model_validate(data)

            except (json.JSONDecodeError, ValidationError) as e:
                logger.warning(f"Parse attempt {parse_attempt + 1} failed: {e}")

                if parse_attempt == max_parse_attempts - 1:
                    raise LLMParsingError(
                        f"Failed to parse LLM response into {response_model.__name__} "
                        f"after {max_parse_attempts} attempts. "
                        f"Response: {response.content[:200]}"
                    )

                # Retry with corrective feedback
                prompt = (
                    f"{prompt}\n\n"
                    f"Previous response had a parsing error: {e}\n"
                    f"Please respond with valid JSON only, no markdown formatting."
                )

        raise LLMParsingError("Unexpected error in parse loop")

    async def acall_structured(
        self,
        prompt: str,
        response_model: type[T],
        system_prompt: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> T:
        """Make an async LLM call and parse the response into a structured Pydantic model.

        Args:
            prompt: The user prompt/question
            response_model: Pydantic model class to parse response into
            system_prompt: Optional system prompt to set context
            temperature: Override default temperature
            max_tokens: Override default max_tokens

        Returns:
            Instance of response_model populated with parsed data

        Raises:
            LLMParsingError: If response cannot be parsed after retries
            LLMAPIError: If the API call fails
        """
        # Add JSON schema instruction to system prompt
        schema_json = response_model.model_json_schema()
        schema_str = json.dumps(schema_json, indent=2)
        schema_instruction = f"\n\nRespond with valid JSON matching this schema:\n{schema_str}"

        enhanced_system_prompt = (system_prompt or "") + schema_instruction

        max_parse_attempts = 2

        for parse_attempt in range(max_parse_attempts):
            response = await self.acall(
                prompt=prompt,
                system_prompt=enhanced_system_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            try:
                # Try to extract JSON from response
                content = response.content.strip()

                # Remove markdown code blocks if present
                if content.startswith("```"):
                    lines = content.split("\n")
                    start_idx = 0
                    end_idx = len(lines)

                    for i, line in enumerate(lines):
                        if line.startswith("```"):
                            if start_idx == 0:
                                start_idx = i + 1
                            else:
                                end_idx = i
                                break

                    content = "\n".join(lines[start_idx:end_idx]).strip()

                # Parse JSON
                data = json.loads(content)

                # Validate against Pydantic model
                return response_model.model_validate(data)

            except (json.JSONDecodeError, ValidationError) as e:
                logger.warning(f"Async parse attempt {parse_attempt + 1} failed: {e}")

                if parse_attempt == max_parse_attempts - 1:
                    raise LLMParsingError(
                        f"Failed to parse async LLM response into {response_model.__name__} "
                        f"after {max_parse_attempts} attempts. "
                        f"Response: {response.content[:200]}"
                    )

                # Retry with corrective feedback
                prompt = (
                    f"{prompt}\n\n"
                    f"Previous response had a parsing error: {e}\n"
                    f"Please respond with valid JSON only, no markdown formatting."
                )

        raise LLMParsingError("Unexpected error in parse loop")

    async def batch_call(
        self,
        prompts: list[str],
        system_prompt: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> list[LLMResponse]:
        """Make multiple LLM calls in parallel.

        Args:
            prompts: List of user prompts
            system_prompt: Optional system prompt for all calls
            temperature: Override default temperature
            max_tokens: Override default max_tokens

        Returns:
            List of LLMResponse objects in the same order as prompts

        Raises:
            LLMAPIError: If any call fails after retries
        """
        tasks = [
            self.acall(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            for prompt in prompts
        ]

        return await asyncio.gather(*tasks)


def create_adapter(
    model: Literal["sonnet", "haiku"] = "sonnet",
    temperature: float = 0.7,
    max_tokens: int = 8000,
) -> LLMAdapter:
    """Convenience function to create an LLM adapter with common configurations.

    Args:
        model: Which Claude model to use ("sonnet" or "haiku")
        temperature: Sampling temperature
        max_tokens: Maximum tokens in response

    Returns:
        Configured LLMAdapter instance

    Example:
        >>> # For complex reasoning tasks
        >>> adapter = create_adapter("sonnet", temperature=0.7)
        >>>
        >>> # For fast classification
        >>> adapter = create_adapter("haiku", temperature=0.3, max_tokens=500)
    """
    model_type = ModelType.SONNET if model == "sonnet" else ModelType.HAIKU

    config = LLMConfig(model=model_type, temperature=temperature, max_tokens=max_tokens)

    return LLMAdapter(config)
