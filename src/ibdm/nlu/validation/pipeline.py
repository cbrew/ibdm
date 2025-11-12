"""
Validation pipeline for composing multiple validators.

Allows chaining validators with flexible failure handling.
"""

from dataclasses import dataclass
from dataclasses import field as dataclass_field
from enum import Enum
from typing import Any

from .parsers import AutoParser, ParseFormat, ParseResult, ResponseParser
from .validators import ValidationResult, Validator


class FailureMode(Enum):
    """How to handle validation failures."""

    FAIL_FAST = "fail_fast"  # Stop on first error
    COLLECT_ALL = "collect_all"  # Run all validators, collect all errors
    CONTINUE_ON_WARNING = "continue_on_warning"  # Stop only on errors, not warnings


@dataclass
class ValidationConfig:
    """
    Configuration for validation pipeline.

    Attributes:
        failure_mode: How to handle failures
        parse_format: Expected response format (None = auto-detect)
        strict_parsing: Fail if parsing has any errors
        allow_partial: Allow partial validation results
        max_issues: Maximum number of issues before stopping (0 = unlimited)
    """

    failure_mode: FailureMode = FailureMode.COLLECT_ALL
    parse_format: ParseFormat | None = None
    strict_parsing: bool = True
    allow_partial: bool = False
    max_issues: int = 0


class ValidationPipeline:
    """
    Pipeline for validating LLM responses.

    Chains parsing and validation steps with configurable behavior.
    """

    def __init__(
        self,
        parser: ResponseParser | None = None,
        validators: list[Validator] | None = None,
        config: ValidationConfig | None = None,
    ):
        """
        Initialize pipeline.

        Args:
            parser: Response parser (default: AutoParser)
            validators: List of validators to apply
            config: Validation configuration
        """
        self.parser = parser or AutoParser()
        self.validators = validators or []
        self.config = config or ValidationConfig()

    def add_validator(self, validator: Validator) -> None:
        """Add a validator to the pipeline."""
        self.validators.append(validator)

    def validate(self, content: str) -> tuple[ParseResult, ValidationResult]:
        """
        Parse and validate LLM response.

        Args:
            content: Raw LLM response text

        Returns:
            Tuple of (ParseResult, ValidationResult)
        """
        # Step 1: Parse content
        parse_result = self.parser.parse(content)

        if parse_result.failed:
            # Parsing failed
            validation_result = ValidationResult(valid=False)
            for error in parse_result.errors:
                validation_result.add_error(
                    message=error, code="parse_error", suggestion="Check response format"
                )
            return parse_result, validation_result

        if not parse_result.data:
            # No data parsed
            validation_result = ValidationResult(valid=False)
            validation_result.add_error(
                message="No data extracted from response", code="empty_response"
            )
            return parse_result, validation_result

        # Step 2: Run validators
        validation_result = self._run_validators(parse_result.data)
        return parse_result, validation_result

    def _run_validators(self, data: Any) -> ValidationResult:
        """
        Run all validators on parsed data.

        Args:
            data: Parsed data to validate

        Returns:
            Combined ValidationResult
        """
        combined_result = ValidationResult(valid=True, data=data)

        for validator in self.validators:
            # Check if we should stop
            if self._should_stop(combined_result):
                combined_result.metadata["stopped_at"] = validator.name
                break

            # Run validator
            result = validator.validate(combined_result.data or data)

            # Track validator
            if "validators_run" not in combined_result.metadata:
                combined_result.metadata["validators_run"] = []
            combined_result.metadata["validators_run"].append(validator.name)

            # Merge results
            combined_result.merge(result)

            # Update data if validator transformed it
            if result.data is not None:
                combined_result.data = result.data

        return combined_result

    def _should_stop(self, result: ValidationResult) -> bool:
        """
        Check if pipeline should stop based on current result and config.

        Args:
            result: Current validation result

        Returns:
            True if pipeline should stop
        """
        # Check max issues limit
        if self.config.max_issues > 0 and len(result.issues) >= self.config.max_issues:
            return True

        # Check failure mode
        if self.config.failure_mode == FailureMode.FAIL_FAST:
            return result.invalid

        if self.config.failure_mode == FailureMode.CONTINUE_ON_WARNING:
            return len(result.errors) > 0

        # COLLECT_ALL never stops early
        return False

    def validate_structured(
        self, content: str, model: type[Any]
    ) -> tuple[ParseResult, ValidationResult]:
        """
        Parse and validate against a Pydantic model.

        Convenience method that adds a PydanticValidator automatically.

        Args:
            content: Raw LLM response
            model: Pydantic model to validate against

        Returns:
            Tuple of (ParseResult, ValidationResult)
        """
        from .validators import PydanticValidator

        # Create a temporary pipeline with Pydantic validator
        temp_validators = self.validators + [PydanticValidator(model)]
        temp_pipeline = ValidationPipeline(
            parser=self.parser, validators=temp_validators, config=self.config
        )

        return temp_pipeline.validate(content)


@dataclass
class PipelineBuilder:
    """
    Builder for creating validation pipelines.

    Provides fluent interface for configuration.
    """

    _parser: ResponseParser | None = None
    _validators: list[Validator] = dataclass_field(default_factory=list)
    _config: ValidationConfig = dataclass_field(default_factory=ValidationConfig)

    def with_parser(self, parser: ResponseParser) -> "PipelineBuilder":
        """Set the parser."""
        self._parser = parser
        return self

    def with_validator(self, validator: Validator) -> "PipelineBuilder":
        """Add a validator."""
        self._validators.append(validator)
        return self

    def with_validators(self, validators: list[Validator]) -> "PipelineBuilder":
        """Add multiple validators."""
        self._validators.extend(validators)
        return self

    def with_config(self, config: ValidationConfig) -> "PipelineBuilder":
        """Set configuration."""
        self._config = config
        return self

    def fail_fast(self) -> "PipelineBuilder":
        """Configure to fail on first error."""
        self._config.failure_mode = FailureMode.FAIL_FAST
        return self

    def collect_all(self) -> "PipelineBuilder":
        """Configure to collect all errors."""
        self._config.failure_mode = FailureMode.COLLECT_ALL
        return self

    def strict(self) -> "PipelineBuilder":
        """Configure strict mode."""
        self._config.strict_parsing = True
        return self

    def lenient(self) -> "PipelineBuilder":
        """Configure lenient mode."""
        self._config.strict_parsing = False
        self._config.allow_partial = True
        return self

    def build(self) -> ValidationPipeline:
        """Build the validation pipeline."""
        return ValidationPipeline(
            parser=self._parser, validators=self._validators, config=self._config
        )


def create_pipeline(
    parser: ResponseParser | None = None,
    validators: list[Validator] | None = None,
    **config_kwargs: Any,
) -> ValidationPipeline:
    """
    Create a validation pipeline.

    Convenience function for common use cases.

    Args:
        parser: Optional custom parser
        validators: List of validators
        **config_kwargs: Configuration options

    Returns:
        Configured ValidationPipeline
    """
    config = ValidationConfig(**config_kwargs)
    return ValidationPipeline(parser=parser, validators=validators, config=config)
