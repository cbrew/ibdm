"""
Retry strategies for LLM response validation.

Provides configurable retry logic with corrective feedback generation.
"""

import time
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from dataclasses import field as dataclass_field
from typing import Any

from .parsers import ParseResult
from .validators import ValidationResult


@dataclass
class RetryContext:
    """
    Context for retry attempts.

    Tracks history and generates diagnostic feedback.

    Attributes:
        attempt: Current attempt number (1-indexed)
        max_attempts: Maximum number of attempts
        original_prompt: Original prompt sent to LLM
        original_response: Original LLM response
        parse_results: History of parse results
        validation_results: History of validation results
        feedback_history: History of feedback messages sent
        metadata: Additional context metadata
    """

    attempt: int = 1
    max_attempts: int = 3
    original_prompt: str = ""
    original_response: str = ""
    parse_results: list[ParseResult] = dataclass_field(default_factory=list)
    validation_results: list[ValidationResult] = dataclass_field(default_factory=list)
    feedback_history: list[str] = dataclass_field(default_factory=list)
    metadata: dict[str, Any] = dataclass_field(default_factory=dict)

    def can_retry(self) -> bool:
        """Check if more retries are available."""
        return self.attempt < self.max_attempts

    def record_attempt(
        self, parse_result: ParseResult, validation_result: ValidationResult
    ) -> None:
        """Record a retry attempt."""
        self.parse_results.append(parse_result)
        self.validation_results.append(validation_result)
        self.attempt += 1

    def add_feedback(self, feedback: str) -> None:
        """Add feedback message to history."""
        self.feedback_history.append(feedback)


class RetryStrategy(ABC):
    """Abstract base for retry strategies."""

    @abstractmethod
    def should_retry(
        self,
        parse_result: ParseResult,
        validation_result: ValidationResult,
        context: RetryContext,
    ) -> bool:
        """
        Determine if retry should be attempted.

        Args:
            parse_result: Result of parsing attempt
            validation_result: Result of validation attempt
            context: Retry context with history

        Returns:
            True if retry should be attempted
        """
        pass

    @abstractmethod
    def generate_feedback(
        self,
        parse_result: ParseResult,
        validation_result: ValidationResult,
        context: RetryContext,
    ) -> str:
        """
        Generate corrective feedback for retry prompt.

        Args:
            parse_result: Result of failed parsing attempt
            validation_result: Result of failed validation attempt
            context: Retry context with history

        Returns:
            Feedback message to append to retry prompt
        """
        pass

    @abstractmethod
    def get_delay(self, context: RetryContext) -> float:
        """
        Get delay before retry in seconds.

        Args:
            context: Retry context

        Returns:
            Delay in seconds
        """
        pass


class ExponentialBackoff(RetryStrategy):
    """
    Retry strategy with exponential backoff delays.

    Generates detailed diagnostic feedback based on errors.
    """

    def __init__(
        self,
        max_attempts: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 10.0,
        backoff_factor: float = 2.0,
    ):
        """
        Initialize strategy.

        Args:
            max_attempts: Maximum retry attempts
            base_delay: Base delay in seconds
            max_delay: Maximum delay in seconds
            backoff_factor: Delay multiplier per attempt
        """
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor

    def should_retry(
        self,
        parse_result: ParseResult,
        validation_result: ValidationResult,
        context: RetryContext,
    ) -> bool:
        """Retry if attempts remaining and errors present."""
        if not context.can_retry():
            return False

        # Retry if parsing failed or validation failed
        return parse_result.failed or validation_result.invalid

    def generate_feedback(
        self,
        parse_result: ParseResult,
        validation_result: ValidationResult,
        context: RetryContext,
    ) -> str:
        """Generate diagnostic feedback for retry."""
        feedback_parts = [
            (
                f"\n\n❌ **Response validation failed "
                f"(attempt {context.attempt}/{self.max_attempts})**\n"
            )
        ]

        # Parse errors
        if parse_result.failed:
            feedback_parts.append("**Parsing Errors:**")
            for error in parse_result.errors:
                feedback_parts.append(f"- {error}")
            feedback_parts.append("")

            # Add format-specific guidance
            if parse_result.format.name:
                feedback_parts.append(f"Expected format: {parse_result.format.value.upper()}")
                feedback_parts.append(self._get_format_guidance(parse_result.format.value))
                feedback_parts.append("")

        # Validation errors
        if validation_result.errors:
            feedback_parts.append("**Validation Errors:**")
            for issue in validation_result.errors:
                msg = f"- {issue.message}"
                if issue.field:
                    msg = f"- Field '{issue.field}': {issue.message}"
                if issue.suggestion:
                    msg += f" ({issue.suggestion})"
                feedback_parts.append(msg)
            feedback_parts.append("")

        # Validation warnings
        if validation_result.warnings:
            feedback_parts.append("**Warnings:**")
            for issue in validation_result.warnings:
                msg = f"- {issue.message}"
                if issue.suggestion:
                    msg += f" ({issue.suggestion})"
                feedback_parts.append(msg)
            feedback_parts.append("")

        # Add corrective instructions
        feedback_parts.append("**Please:**")
        feedback_parts.append("1. Follow the exact format specified")
        feedback_parts.append("2. Include all required fields")
        feedback_parts.append("3. Ensure values match expected types and constraints")
        feedback_parts.append("4. Double-check JSON/XML syntax")
        feedback_parts.append("\nProvide a corrected response:")

        return "\n".join(feedback_parts)

    def get_delay(self, context: RetryContext) -> float:
        """Calculate exponential backoff delay."""
        delay = self.base_delay * (self.backoff_factor ** (context.attempt - 1))
        return min(delay, self.max_delay)

    def _get_format_guidance(self, format_name: str) -> str:
        """Get format-specific guidance."""
        guidance = {
            "json": (
                "Use proper JSON format:\n"
                "```json\n"
                '{\n  "field1": "value1",\n  "field2": "value2"\n}\n'
                "```"
            ),
            "xml": (
                "Use proper XML format:\n"
                "```xml\n"
                "<root>\n  <field1>value1</field1>\n  <field2>value2</field2>\n</root>\n"
                "```"
            ),
        }
        return guidance.get(format_name, "Check format specification above.")


class AdaptiveRetry(RetryStrategy):
    """
    Adaptive retry strategy that learns from error patterns.

    Adjusts retry behavior based on error types and history.
    """

    def __init__(
        self,
        max_attempts: int = 3,
        base_delay: float = 0.5,
        learn_from_history: bool = True,
    ):
        """
        Initialize strategy.

        Args:
            max_attempts: Maximum retry attempts
            base_delay: Base delay in seconds
            learn_from_history: Adjust based on error patterns
        """
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.learn_from_history = learn_from_history

    def should_retry(
        self,
        parse_result: ParseResult,
        validation_result: ValidationResult,
        context: RetryContext,
    ) -> bool:
        """Retry with adaptive logic."""
        if not context.can_retry():
            return False

        # Check if errors are improving
        if self.learn_from_history and len(context.validation_results) > 1:
            previous_errors = len(context.validation_results[-2].errors)
            current_errors = len(validation_result.errors)

            # If errors increasing, may not be worth retrying
            if current_errors > previous_errors:
                # Only retry if still have many attempts left
                return context.attempt < (self.max_attempts // 2)

        return parse_result.failed or validation_result.invalid

    def generate_feedback(
        self,
        parse_result: ParseResult,
        validation_result: ValidationResult,
        context: RetryContext,
    ) -> str:
        """Generate adaptive feedback based on error patterns."""
        feedback_parts = [
            f"\n\n**Attempt {context.attempt}/{self.max_attempts} - Corrections Needed:**\n"
        ]

        # Identify error patterns
        error_types = self._categorize_errors(validation_result)

        if "missing_fields" in error_types:
            feedback_parts.append("**Missing Required Fields:**")
            for issue in validation_result.errors:
                if "missing" in issue.message.lower() or issue.code == "missing_field":
                    feedback_parts.append(f"- Add: {issue.field or issue.message}")
            feedback_parts.append("")

        if "type_errors" in error_types:
            feedback_parts.append("**Type Errors:**")
            for issue in validation_result.errors:
                if "type" in issue.message.lower() or issue.code == "type_error":
                    if issue.suggestion:
                        feedback_parts.append(f"- {issue.suggestion}")
                    else:
                        feedback_parts.append(f"- {issue.message}")
            feedback_parts.append("")

        if "range_errors" in error_types:
            feedback_parts.append("**Value Range Errors:**")
            for issue in validation_result.errors:
                if (
                    (issue.code and "range" in issue.code)
                    or "above" in issue.message
                    or "below" in issue.message
                ):
                    feedback_parts.append(f"- {issue.suggestion or issue.message}")
            feedback_parts.append("")

        # Parse errors
        if parse_result.failed:
            feedback_parts.append("**Format Issues:**")
            feedback_parts.append(f"- Could not parse {parse_result.format.value} format")
            if parse_result.errors:
                feedback_parts.append(f"- {parse_result.errors[0]}")
            feedback_parts.append("")

        # Add progressive hints
        if context.attempt > 1:
            feedback_parts.append("**💡 Hint:** Focus on the specific errors listed above.")
        if context.attempt == self.max_attempts - 1:
            feedback_parts.append("**⚠️  Final attempt:** Carefully review ALL requirements.")

        feedback_parts.append("\nProvide corrected response:")

        return "\n".join(feedback_parts)

    def get_delay(self, context: RetryContext) -> float:
        """Calculate adaptive delay."""
        # Shorter delays for adaptive retry
        return self.base_delay * (1.5 ** (context.attempt - 1))

    def _categorize_errors(self, validation_result: ValidationResult) -> set[str]:
        """Categorize errors into patterns."""
        categories = set()

        for issue in validation_result.errors:
            if "missing" in issue.message.lower() or issue.code == "missing_field":
                categories.add("missing_fields")
            elif "type" in issue.message.lower() or issue.code == "type_error":
                categories.add("type_errors")
            elif "range" in str(issue.code) or "above" in issue.message or "below" in issue.message:
                categories.add("range_errors")
            else:
                categories.add("other_errors")

        return categories


class CustomRetry(RetryStrategy):
    """
    Custom retry strategy with user-defined logic.

    Allows full customization via callbacks.
    """

    def __init__(
        self,
        should_retry_fn: Callable[[ParseResult, ValidationResult, RetryContext], bool],
        feedback_fn: Callable[[ParseResult, ValidationResult, RetryContext], str],
        delay_fn: Callable[[RetryContext], float] | None = None,
    ):
        """
        Initialize with custom functions.

        Args:
            should_retry_fn: Function determining if retry should occur
            feedback_fn: Function generating feedback message
            delay_fn: Optional function calculating delay
        """
        self.should_retry_fn = should_retry_fn
        self.feedback_fn = feedback_fn
        self.delay_fn = delay_fn or (lambda ctx: 1.0)

    def should_retry(
        self,
        parse_result: ParseResult,
        validation_result: ValidationResult,
        context: RetryContext,
    ) -> bool:
        """Use custom retry logic."""
        return self.should_retry_fn(parse_result, validation_result, context)

    def generate_feedback(
        self,
        parse_result: ParseResult,
        validation_result: ValidationResult,
        context: RetryContext,
    ) -> str:
        """Use custom feedback generation."""
        return self.feedback_fn(parse_result, validation_result, context)

    def get_delay(self, context: RetryContext) -> float:
        """Use custom delay calculation."""
        return self.delay_fn(context)


def retry_with_feedback(
    llm_call: Callable[[str], str],
    prompt: str,
    validator_pipeline: Any,  # ValidationPipeline
    strategy: RetryStrategy | None = None,
) -> tuple[ParseResult, ValidationResult, RetryContext]:
    """
    Execute LLM call with retry and validation.

    Args:
        llm_call: Function that takes prompt and returns LLM response
        prompt: Initial prompt
        validator_pipeline: ValidationPipeline for validation
        strategy: Retry strategy (default: ExponentialBackoff)

    Returns:
        Tuple of (final ParseResult, final ValidationResult, RetryContext)
    """
    if strategy is None:
        strategy = ExponentialBackoff()

    # Initialize context - get max_attempts from strategy if it has it, otherwise default
    max_attempts = getattr(strategy, "max_attempts", 3)
    context = RetryContext(max_attempts=max_attempts, original_prompt=prompt)

    # First attempt
    response = llm_call(prompt)
    context.original_response = response

    parse_result, validation_result = validator_pipeline.validate(response)
    context.record_attempt(parse_result, validation_result)

    # Retry loop
    while strategy.should_retry(parse_result, validation_result, context):
        # Generate feedback
        feedback = strategy.generate_feedback(parse_result, validation_result, context)
        context.add_feedback(feedback)

        # Delay before retry
        delay = strategy.get_delay(context)
        if delay > 0:
            time.sleep(delay)

        # Retry with feedback
        retry_prompt = prompt + feedback
        response = llm_call(retry_prompt)

        parse_result, validation_result = validator_pipeline.validate(response)
        context.record_attempt(parse_result, validation_result)

    return parse_result, validation_result, context
