"""
Tests for the validation framework.

Tests parsers, validators, pipeline, retry strategies, extractors, and metrics.
"""

from typing import Any

import pytest
from pydantic import BaseModel, Field

from ibdm.nlu.validation import (
    AutoParser,
    CustomValidator,
    EnumValidator,
    ExponentialBackoff,
    FieldExtractor,
    JSONParser,
    ParseFormat,
    ParseResult,
    PartialExtractor,
    PipelineBuilder,
    PydanticValidator,
    RangeValidator,
    RetryContext,
    SchemaValidator,
    StructuredTextParser,
    ValidationMetrics,
    ValidationPipeline,
    ValidationResult,
    XMLParser,
    extract_partial_response,
)


# Test fixtures
class TestModel(BaseModel):
    """Test Pydantic model."""

    name: str
    age: int = Field(ge=0, le=150)
    confidence: float = Field(ge=0.0, le=1.0)
    active: bool = True


# ========== Parser Tests ==========


class TestJSONParser:
    """Tests for JSONParser."""

    def test_parse_pure_json(self):
        """Test parsing pure JSON object."""
        parser = JSONParser()
        content = '{"name": "Alice", "age": 30}'

        result = parser.parse(content)

        assert result.success
        assert result.data == {"name": "Alice", "age": 30}
        assert result.format == ParseFormat.JSON

    def test_parse_json_in_markdown(self):
        """Test parsing JSON within markdown code blocks."""
        parser = JSONParser()
        content = """
Here's the result:
```json
{
  "name": "Bob",
  "age": 25
}
```
        """

        result = parser.parse(content)

        assert result.success
        assert result.data == {"name": "Bob", "age": 25}
        assert result.extracted_content is not None

    def test_parse_json_with_text(self):
        """Test parsing JSON mixed with text."""
        parser = JSONParser()
        content = 'The answer is: {"name": "Charlie", "age": 35}'

        result = parser.parse(content)

        assert result.success
        assert result.data["name"] == "Charlie"

    def test_parse_invalid_json(self):
        """Test parsing invalid JSON."""
        parser = JSONParser()
        content = '{"name": "Dave", "age": }'  # Missing value

        result = parser.parse(content)

        assert result.failed
        assert len(result.errors) > 0

    def test_can_parse(self):
        """Test format detection."""
        parser = JSONParser()

        assert parser.can_parse('{"key": "value"}')
        assert parser.can_parse("```json\n{}\n```")
        assert not parser.can_parse("<root></root>")


class TestXMLParser:
    """Tests for XMLParser."""

    def test_parse_simple_xml(self):
        """Test parsing simple XML."""
        parser = XMLParser()
        content = "<person><name>Alice</name><age>30</age></person>"

        result = parser.parse(content)

        assert result.success
        assert result.data["name"] == "Alice"
        assert result.data["age"] == "30"

    def test_parse_xml_with_attributes(self):
        """Test parsing XML with attributes."""
        parser = XMLParser()
        content = '<person id="123"><name>Bob</name></person>'

        result = parser.parse(content)

        assert result.success
        assert result.data["@attributes"]["id"] == "123"
        assert result.data["name"] == "Bob"

    def test_parse_xml_in_markdown(self):
        """Test parsing XML in markdown."""
        parser = XMLParser()
        content = """
```xml
<response>
  <status>success</status>
</response>
```
        """

        result = parser.parse(content)

        assert result.success
        assert result.data["status"] == "success"

    def test_parse_invalid_xml(self):
        """Test parsing invalid XML."""
        parser = XMLParser()
        content = "<person><name>Alice</person>"  # Missing close tag

        result = parser.parse(content)

        assert result.failed


class TestStructuredTextParser:
    """Tests for StructuredTextParser."""

    def test_parse_colon_format(self):
        """Test parsing colon-separated key-value pairs."""
        parser = StructuredTextParser()
        content = """
name: Alice
age: 30
city: Seattle
        """

        result = parser.parse(content)

        assert result.success
        assert result.data["name"] == "Alice"
        assert result.data["age"] == "30"

    def test_parse_equals_format(self):
        """Test parsing equals-separated pairs."""
        parser = StructuredTextParser()
        content = """
name = Bob
age = 25
        """

        result = parser.parse(content)

        assert result.success
        assert result.data["name"] == "Bob"


class TestAutoParser:
    """Tests for AutoParser."""

    def test_auto_detect_json(self):
        """Test automatic JSON detection and parsing."""
        parser = AutoParser()
        content = '{"type": "test"}'

        result = parser.parse(content)

        assert result.success
        assert result.data["type"] == "test"

    def test_auto_detect_xml(self):
        """Test automatic XML detection and parsing."""
        parser = AutoParser()
        content = "<root><type>test</type></root>"

        result = parser.parse(content)

        assert result.success
        assert result.data["type"] == "test"


# ========== Validator Tests ==========


class TestPydanticValidator:
    """Tests for PydanticValidator."""

    def test_valid_data(self):
        """Test validation of valid data."""
        validator = PydanticValidator(TestModel)
        data = {"name": "Alice", "age": 30, "confidence": 0.9}

        result = validator.validate(data)

        assert result.valid
        assert isinstance(result.data, TestModel)
        assert result.data.name == "Alice"

    def test_missing_required_field(self):
        """Test validation with missing required field."""
        validator = PydanticValidator(TestModel)
        data = {"age": 30, "confidence": 0.9}  # Missing 'name'

        result = validator.validate(data)

        assert result.invalid
        assert any("name" in issue.field for issue in result.errors)

    def test_type_error(self):
        """Test validation with wrong type."""
        validator = PydanticValidator(TestModel)
        data = {"name": "Bob", "age": "thirty", "confidence": 0.9}  # Wrong type

        result = validator.validate(data)

        assert result.invalid

    def test_range_constraint(self):
        """Test validation with range constraint violation."""
        validator = PydanticValidator(TestModel)
        data = {"name": "Charlie", "age": 200, "confidence": 0.9}  # Age > 150

        result = validator.validate(data)

        assert result.invalid


class TestSchemaValidator:
    """Tests for SchemaValidator."""

    def test_required_fields(self):
        """Test required field validation."""
        validator = SchemaValidator(
            required_fields=["name", "age"], field_types={"name": str, "age": int}
        )

        data = {"name": "Alice", "age": 30}
        result = validator.validate(data)
        assert result.valid

        data = {"name": "Bob"}  # Missing 'age'
        result = validator.validate(data)
        assert result.invalid

    def test_type_checking(self):
        """Test type checking."""
        validator = SchemaValidator(field_types={"age": int})

        data = {"age": "thirty"}  # Wrong type
        result = validator.validate(data)
        assert result.invalid

    def test_unknown_fields(self):
        """Test warning for unknown fields."""
        validator = SchemaValidator(required_fields=["name"])

        data = {"name": "Alice", "unknown": "value"}
        result = validator.validate(data)

        assert result.valid  # Still valid
        assert len(result.warnings) > 0  # But has warning


class TestRangeValidator:
    """Tests for RangeValidator."""

    def test_value_in_range(self):
        """Test value within range."""
        validator = RangeValidator("score", min_value=0.0, max_value=1.0)

        data = {"score": 0.75}
        result = validator.validate(data)
        assert result.valid

    def test_value_below_min(self):
        """Test value below minimum."""
        validator = RangeValidator("score", min_value=0.0)

        data = {"score": -0.5}
        result = validator.validate(data)
        assert result.invalid

    def test_value_above_max(self):
        """Test value above maximum."""
        validator = RangeValidator("score", max_value=1.0)

        data = {"score": 1.5}
        result = validator.validate(data)
        assert result.invalid


class TestCustomValidator:
    """Tests for CustomValidator."""

    def test_custom_validation(self):
        """Test custom validation logic."""

        def validate_positive(data: Any) -> tuple[bool, list[str]]:
            if not isinstance(data, dict):
                return False, ["Data must be dict"]
            if "value" in data and data["value"] <= 0:
                return False, ["Value must be positive"]
            return True, []

        validator = CustomValidator(validate_positive, "PositiveValidator")

        data = {"value": 10}
        result = validator.validate(data)
        assert result.valid

        data = {"value": -5}
        result = validator.validate(data)
        assert result.invalid


class TestEnumValidator:
    """Tests for EnumValidator."""

    def test_valid_enum_value(self):
        """Test valid enum value."""
        validator = EnumValidator("status", {"active", "inactive", "pending"})

        data = {"status": "active"}
        result = validator.validate(data)
        assert result.valid

    def test_invalid_enum_value(self):
        """Test invalid enum value."""
        validator = EnumValidator("status", {"active", "inactive"})

        data = {"status": "unknown"}
        result = validator.validate(data)
        assert result.invalid


# ========== Pipeline Tests ==========


class TestValidationPipeline:
    """Tests for ValidationPipeline."""

    def test_basic_pipeline(self):
        """Test basic pipeline with single validator."""
        pipeline = ValidationPipeline(
            parser=JSONParser(),
            validators=[SchemaValidator(required_fields=["name"])],
        )

        content = '{"name": "Alice"}'
        parse_result, validation_result = pipeline.validate(content)

        assert parse_result.success
        assert validation_result.valid

    def test_multiple_validators(self):
        """Test pipeline with multiple validators."""
        validators = [
            SchemaValidator(required_fields=["score"]),
            RangeValidator("score", min_value=0.0, max_value=1.0),
        ]
        pipeline = ValidationPipeline(validators=validators)

        content = '{"score": 0.8}'
        parse_result, validation_result = pipeline.validate(content)

        assert validation_result.valid
        assert "validators_run" in validation_result.metadata

    def test_validate_structured(self):
        """Test structured validation with Pydantic model."""
        pipeline = ValidationPipeline()

        content = '{"name": "Alice", "age": 30, "confidence": 0.9}'
        parse_result, validation_result = pipeline.validate_structured(content, TestModel)

        assert validation_result.valid
        assert isinstance(validation_result.data, TestModel)

    def test_builder(self):
        """Test PipelineBuilder."""
        pipeline = (
            PipelineBuilder()
            .with_parser(JSONParser())
            .with_validator(SchemaValidator(required_fields=["name"]))
            .fail_fast()
            .build()
        )

        content = '{"name": "Alice"}'
        parse_result, validation_result = pipeline.validate(content)

        assert validation_result.valid


# ========== Retry Tests ==========


class TestRetryStrategies:
    """Tests for retry strategies."""

    def test_retry_context(self):
        """Test RetryContext tracking."""
        context = RetryContext(max_attempts=3)

        assert context.can_retry()
        assert context.attempt == 1

        parse_result = ParseResult(success=False)
        validation_result = ValidationResult(valid=False)
        context.record_attempt(parse_result, validation_result)

        assert context.attempt == 2
        assert len(context.parse_results) == 1

    def test_exponential_backoff(self):
        """Test ExponentialBackoff strategy."""
        strategy = ExponentialBackoff(max_attempts=3, base_delay=1.0)

        context = RetryContext(attempt=1, max_attempts=3)
        parse_result = ParseResult(success=False, errors=["Parse error"])
        validation_result = ValidationResult(valid=False)
        validation_result.add_error("Validation error", field="test")

        # Should retry
        should_retry = strategy.should_retry(parse_result, validation_result, context)
        assert should_retry

        # Generate feedback
        feedback = strategy.generate_feedback(parse_result, validation_result, context)
        assert "Parse error" in feedback or "Validation error" in feedback

        # Calculate delay
        delay = strategy.get_delay(context)
        assert delay == 1.0

        context.attempt = 2
        delay = strategy.get_delay(context)
        assert delay == 2.0


# ========== Extractor Tests ==========


class TestPartialExtractor:
    """Tests for PartialExtractor."""

    def test_extract_from_malformed_json(self):
        """Test extraction from malformed JSON."""
        extractor = PartialExtractor()
        content = '{"name": "Alice", "age": 30, "invalid"}'  # Malformed

        result = extractor.extract(content, expected_fields={"name", "age"})

        assert result.success
        assert "name" in result.fields_found
        assert result.data["name"] == "Alice"

    def test_extract_missing_fields(self):
        """Test tracking of missing fields."""
        extractor = PartialExtractor()
        content = '{"name": "Alice"}'

        result = extractor.extract(content, expected_fields={"name", "age", "city"})

        assert "name" in result.fields_found
        assert "age" in result.fields_missing
        assert "city" in result.fields_missing
        assert result.partial

    def test_completeness(self):
        """Test completeness calculation."""
        extractor = PartialExtractor()
        content = '{"name": "Alice", "age": 30}'

        result = extractor.extract(content, expected_fields={"name", "age", "city"})

        # Found 2 out of 3
        assert result.completeness == pytest.approx(2 / 3)


class TestFieldExtractor:
    """Tests for FieldExtractor."""

    def test_extract_confidence(self):
        """Test confidence extraction."""
        content = "confidence: 0.85"

        confidence = FieldExtractor.extract_confidence(content)

        assert confidence == pytest.approx(0.85)

    def test_extract_list(self):
        """Test list extraction."""
        content = '"tags": ["python", "testing", "validation"]'

        tags = FieldExtractor.extract_list(content, "tags")

        assert tags == ["python", "testing", "validation"]

    def test_extract_boolean(self):
        """Test boolean extraction."""
        content = '"active": true'

        active = FieldExtractor.extract_boolean(content, "active")

        assert active is True

    def test_extract_number(self):
        """Test number extraction."""
        content = '"count": 42'

        count = FieldExtractor.extract_number(content, "count")

        assert count == 42


# ========== Metrics Tests ==========


class TestValidationMetrics:
    """Tests for ValidationMetrics."""

    def test_record_successful_validation(self):
        """Test recording successful validation."""
        metrics = ValidationMetrics()

        parse_result = ParseResult(success=True, format=ParseFormat.JSON)
        validation_result = ValidationResult(valid=True)

        metrics.record_validation(parse_result, validation_result)

        assert metrics.stats.total_attempts == 1
        assert metrics.stats.successful == 1
        assert metrics.stats.success_rate == 1.0

    def test_record_failed_validation(self):
        """Test recording failed validation."""
        metrics = ValidationMetrics()

        parse_result = ParseResult(success=False, errors=["Parse error"])
        validation_result = ValidationResult(valid=False)
        validation_result.add_error("Validation error", code="test_error")

        metrics.record_validation(parse_result, validation_result)

        assert metrics.stats.failed == 1
        assert metrics.stats.parse_errors == 1
        assert "test_error" in metrics.stats.error_codes

    def test_retry_tracking(self):
        """Test retry count tracking."""
        metrics = ValidationMetrics()

        parse_result = ParseResult(success=True)
        validation_result = ValidationResult(valid=True)

        metrics.record_validation(parse_result, validation_result, retry_count=2)

        assert metrics.stats.retries == 2

    def test_summary(self):
        """Test summary generation."""
        metrics = ValidationMetrics()

        # Record some validations
        for _ in range(3):
            metrics.record_validation(
                ParseResult(success=True, format=ParseFormat.JSON),
                ValidationResult(valid=True),
            )

        metrics.record_validation(ParseResult(success=False), ValidationResult(valid=False))

        summary = metrics.summary()

        assert "Total Attempts: 4" in summary
        assert "Successful: 3" in summary


# ========== Integration Tests ==========


class TestIntegration:
    """Integration tests for the full validation framework."""

    def test_end_to_end_validation(self):
        """Test complete validation flow."""
        # Create pipeline
        pipeline = (
            PipelineBuilder()
            .with_parser(JSONParser())
            .with_validator(PydanticValidator(TestModel))
            .collect_all()
            .build()
        )

        # Valid content
        content = '{"name": "Alice", "age": 30, "confidence": 0.95}'
        parse_result, validation_result = pipeline.validate(content)

        assert parse_result.success
        assert validation_result.valid
        assert validation_result.data.name == "Alice"

    def test_validation_with_metrics(self):
        """Test validation with metrics tracking."""
        metrics = ValidationMetrics()
        pipeline = ValidationPipeline(validators=[PydanticValidator(TestModel)])

        # Track validation
        val_id = metrics.start_validation()
        content = '{"name": "Bob", "age": 25, "confidence": 0.8}'
        parse_result, validation_result = pipeline.validate(content)
        metrics.record_validation(parse_result, validation_result, val_id)

        assert metrics.stats.successful == 1
        assert metrics.stats.avg_time > 0

    def test_partial_extraction_fallback(self):
        """Test partial extraction as fallback."""
        # Malformed JSON
        content = '{"name": "Charlie", "age": 35, "invalid syntax'

        # Try normal parsing
        parser = JSONParser()
        result = parser.parse(content)
        assert result.failed

        # Fallback to partial extraction
        extraction = extract_partial_response(content, {"name", "age"})
        assert extraction.success
        assert extraction.data["name"] == "Charlie"
        assert extraction.data["age"] == 35  # Parsed as int
