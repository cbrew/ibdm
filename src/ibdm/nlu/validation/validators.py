"""
Validation framework for parsed LLM responses.

Provides composable validators with rich diagnostic information.
"""

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from dataclasses import field as dataclass_field
from enum import Enum
from typing import Any

from pydantic import BaseModel, ValidationError


class ValidationSeverity(Enum):
    """Severity levels for validation issues."""

    ERROR = "error"  # Validation failed, cannot proceed
    WARNING = "warning"  # Issue detected but can proceed
    INFO = "info"  # Informational message


@dataclass
class ValidationIssue:
    """
    A single validation issue.

    Attributes:
        severity: Issue severity level
        message: Human-readable message
        field: Field name where issue occurred (if applicable)
        code: Machine-readable error code
        suggestion: Suggested fix or correction
        metadata: Additional diagnostic information
    """

    severity: ValidationSeverity
    message: str
    field: str | None = None
    code: str | None = None
    suggestion: str | None = None
    metadata: dict[str, Any] = dataclass_field(default_factory=dict)

    def is_error(self) -> bool:
        """Check if this is an error-level issue."""
        return self.severity == ValidationSeverity.ERROR

    def is_warning(self) -> bool:
        """Check if this is a warning-level issue."""
        return self.severity == ValidationSeverity.WARNING


@dataclass
class ValidationResult:
    """
    Result of validation process.

    Attributes:
        valid: Whether validation passed
        data: Validated/transformed data
        issues: List of validation issues
        metadata: Additional validation metadata
    """

    valid: bool
    data: Any = None
    issues: list[ValidationIssue] = dataclass_field(default_factory=list)
    metadata: dict[str, Any] = dataclass_field(default_factory=dict)

    @property
    def invalid(self) -> bool:
        """Whether validation failed."""
        return not self.valid

    @property
    def errors(self) -> list[ValidationIssue]:
        """Get only error-level issues."""
        return [issue for issue in self.issues if issue.is_error()]

    @property
    def warnings(self) -> list[ValidationIssue]:
        """Get only warning-level issues."""
        return [issue for issue in self.issues if issue.is_warning()]

    def add_error(
        self,
        message: str,
        field: str | None = None,
        code: str | None = None,
        suggestion: str | None = None,
    ) -> None:
        """Add an error issue."""
        self.issues.append(
            ValidationIssue(
                severity=ValidationSeverity.ERROR,
                message=message,
                field=field,
                code=code,
                suggestion=suggestion,
            )
        )
        self.valid = False

    def add_warning(
        self,
        message: str,
        field: str | None = None,
        code: str | None = None,
        suggestion: str | None = None,
    ) -> None:
        """Add a warning issue."""
        self.issues.append(
            ValidationIssue(
                severity=ValidationSeverity.WARNING,
                message=message,
                field=field,
                code=code,
                suggestion=suggestion,
            )
        )

    def merge(self, other: "ValidationResult") -> None:
        """
        Merge another validation result into this one.

        Updates valid status and combines issues.
        """
        self.issues.extend(other.issues)
        if other.invalid:
            self.valid = False
        self.metadata.update(other.metadata)


class Validator(ABC):
    """Abstract base class for validators."""

    @abstractmethod
    def validate(self, data: Any) -> ValidationResult:
        """
        Validate data.

        Args:
            data: Data to validate

        Returns:
            ValidationResult with issues and validated data
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Validator name for diagnostics."""
        pass


class PydanticValidator(Validator):
    """
    Validator using Pydantic models.

    Validates data against a Pydantic model schema.
    """

    def __init__(self, model: type[BaseModel]):
        """
        Initialize validator.

        Args:
            model: Pydantic model class to validate against
        """
        self.model = model

    @property
    def name(self) -> str:
        """Get validator name."""
        return f"PydanticValidator({self.model.__name__})"

    def validate(self, data: Any) -> ValidationResult:
        """
        Validate data against Pydantic model.

        Args:
            data: Data to validate (usually dict)

        Returns:
            ValidationResult with validated model or errors
        """
        result = ValidationResult(valid=True)

        try:
            # Validate and construct model
            validated_model = self.model.model_validate(data)
            result.data = validated_model
            result.metadata["model"] = self.model.__name__
            return result

        except ValidationError as e:
            result.valid = False
            # Convert Pydantic errors to ValidationIssues
            for error in e.errors():
                field_path = ".".join(str(loc) for loc in error["loc"])
                result.add_error(
                    message=error["msg"],
                    field=field_path,
                    code=error["type"],
                    suggestion=self._generate_suggestion(error),
                )
            return result

    def _generate_suggestion(self, error: dict[str, Any]) -> str:
        """Generate helpful suggestion from Pydantic error."""
        error_type = error["type"]

        if error_type == "missing":
            return f"Add required field: {error['loc'][-1]}"
        elif error_type == "value_error":
            return "Check value format and constraints"
        elif error_type == "type_error":
            expected = error.get("expected")
            if expected:
                return f"Convert value to type: {expected}"
            return "Check value type"
        else:
            return "Review field value and constraints"


class SchemaValidator(Validator):
    """
    Validator for dict/JSON schema.

    Checks for required fields, types, and basic constraints.
    """

    def __init__(
        self,
        required_fields: list[str] | None = None,
        optional_fields: list[str] | None = None,
        field_types: dict[str, type] | None = None,
    ):
        """
        Initialize validator.

        Args:
            required_fields: Fields that must be present
            optional_fields: Fields that may be present
            field_types: Expected types for fields
        """
        self.required_fields = set(required_fields or [])
        self.optional_fields = set(optional_fields or [])
        self.field_types = field_types or {}

    @property
    def name(self) -> str:
        """Get validator name."""
        return "SchemaValidator"

    def validate(self, data: Any) -> ValidationResult:
        """Validate data against schema."""
        result = ValidationResult(valid=True, data=data)

        # Check data is dict
        if not isinstance(data, dict):
            result.add_error(
                message=f"Expected dict, got {type(data).__name__}",
                code="type_error",
                suggestion="Ensure response is a JSON object",
            )
            return result

        # Check required fields
        for field in self.required_fields:
            if field not in data:
                result.add_error(
                    message=f"Missing required field: {field}",
                    field=field,
                    code="missing_field",
                    suggestion=f"Add '{field}' to response",
                )

        # Check unknown fields
        known_fields = self.required_fields | self.optional_fields
        for field in data:
            if known_fields and field not in known_fields:
                result.add_warning(
                    message=f"Unknown field: {field}",
                    field=field,
                    code="unknown_field",
                    suggestion=f"Remove '{field}' or add to schema",
                )

        # Check field types
        for field, expected_type in self.field_types.items():
            if field in data and data[field] is not None:
                if not isinstance(data[field], expected_type):
                    result.add_error(
                        message=(
                            f"Wrong type for {field}: "
                            f"expected {expected_type.__name__}, "
                            f"got {type(data[field]).__name__}"
                        ),
                        field=field,
                        code="type_error",
                        suggestion=f"Convert {field} to {expected_type.__name__}",
                    )

        return result


class RangeValidator(Validator):
    """
    Validator for numeric range constraints.

    Checks that numeric fields are within specified ranges.
    """

    def __init__(self, field: str, min_value: float | None = None, max_value: float | None = None):
        """
        Initialize validator.

        Args:
            field: Field name to validate
            min_value: Minimum allowed value (inclusive)
            max_value: Maximum allowed value (inclusive)
        """
        self.field = field
        self.min_value = min_value
        self.max_value = max_value

    @property
    def name(self) -> str:
        """Get validator name."""
        return f"RangeValidator({self.field})"

    def validate(self, data: Any) -> ValidationResult:
        """Validate numeric range."""
        result = ValidationResult(valid=True, data=data)

        # Check data is dict
        if not isinstance(data, dict):
            result.add_error(message="Cannot validate range on non-dict data", code="type_error")
            return result

        # Check field exists
        if self.field not in data:
            # Field doesn't exist - not an error for this validator
            return result

        value = data[self.field]

        # Check value is numeric
        if not isinstance(value, (int, float)):
            result.add_error(
                message=f"{self.field} must be numeric, got {type(value).__name__}",
                field=self.field,
                code="type_error",
            )
            return result

        # Check min value
        if self.min_value is not None and value < self.min_value:
            result.add_error(
                message=f"{self.field} ({value}) is below minimum ({self.min_value})",
                field=self.field,
                code="range_error",
                suggestion=f"Use value >= {self.min_value}",
            )

        # Check max value
        if self.max_value is not None and value > self.max_value:
            result.add_error(
                message=f"{self.field} ({value}) is above maximum ({self.max_value})",
                field=self.field,
                code="range_error",
                suggestion=f"Use value <= {self.max_value}",
            )

        return result


class CustomValidator(Validator):
    """
    Validator with custom validation function.

    Allows arbitrary validation logic via a callable.
    """

    def __init__(
        self,
        validation_fn: Callable[[Any], tuple[bool, list[str]]],
        validator_name: str = "CustomValidator",
    ):
        """
        Initialize validator.

        Args:
            validation_fn: Function that takes data and returns (valid, errors)
            validator_name: Name for this validator
        """
        self.validation_fn = validation_fn
        self.validator_name = validator_name

    @property
    def name(self) -> str:
        """Get validator name."""
        return self.validator_name

    def validate(self, data: Any) -> ValidationResult:
        """Run custom validation."""
        result = ValidationResult(valid=True, data=data)

        try:
            valid, errors = self.validation_fn(data)
            if not valid:
                result.valid = False
                for error in errors:
                    result.add_error(message=error, code="custom_error")
        except Exception as e:
            result.add_error(
                message=f"Validation function error: {str(e)}",
                code="validation_exception",
            )

        return result


class EnumValidator(Validator):
    """
    Validator for enum/choice fields.

    Checks that field values are in allowed set.
    """

    def __init__(self, field: str, allowed_values: set[Any]):
        """
        Initialize validator.

        Args:
            field: Field name to validate
            allowed_values: Set of allowed values
        """
        self.field = field
        self.allowed_values = allowed_values

    @property
    def name(self) -> str:
        """Get validator name."""
        return f"EnumValidator({self.field})"

    def validate(self, data: Any) -> ValidationResult:
        """Validate enum value."""
        result = ValidationResult(valid=True, data=data)

        if not isinstance(data, dict):
            result.add_error(message="Cannot validate enum on non-dict data", code="type_error")
            return result

        if self.field not in data:
            return result

        value = data[self.field]
        if value not in self.allowed_values:
            result.add_error(
                message=f"{self.field} value '{value}' not in allowed values",
                field=self.field,
                code="enum_error",
                suggestion=f"Use one of: {', '.join(str(v) for v in self.allowed_values)}",
            )

        return result
