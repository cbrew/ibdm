"""
Partial result extraction from malformed LLM responses.

Attempts to salvage useful data even when parsing or validation fails.
"""

import json
import re
from dataclasses import dataclass
from dataclasses import field as dataclass_field
from typing import Any


@dataclass
class ExtractionResult:
    """
    Result of partial extraction attempt.

    Attributes:
        success: Whether any data was extracted
        data: Extracted partial data
        fields_found: Set of field names successfully extracted
        fields_missing: Set of field names that could not be extracted
        confidence: Confidence in extracted data (0.0-1.0)
        metadata: Additional extraction metadata
    """

    success: bool
    data: dict[str, Any] = dataclass_field(default_factory=dict)
    fields_found: set[str] = dataclass_field(default_factory=set)
    fields_missing: set[str] = dataclass_field(default_factory=set)
    confidence: float = 0.0
    metadata: dict[str, Any] = dataclass_field(default_factory=dict)

    @property
    def partial(self) -> bool:
        """Check if extraction was only partial."""
        return len(self.fields_missing) > 0

    @property
    def completeness(self) -> float:
        """Calculate completeness ratio."""
        total = len(self.fields_found) + len(self.fields_missing)
        if total == 0:
            return 0.0
        return len(self.fields_found) / total


class PartialExtractor:
    """
    Extractor for salvaging data from malformed responses.

    Uses pattern matching and heuristics to extract fields.
    """

    def __init__(self, required_fields: set[str] | None = None):
        """
        Initialize extractor.

        Args:
            required_fields: Fields to attempt extraction (None = extract all)
        """
        self.required_fields = required_fields

    def extract(self, content: str, expected_fields: set[str] | None = None) -> ExtractionResult:
        """
        Extract partial data from malformed content.

        Args:
            content: Malformed response content
            expected_fields: Fields to look for (overrides required_fields)

        Returns:
            ExtractionResult with any salvaged data
        """
        fields = expected_fields or self.required_fields

        result = ExtractionResult(success=False)

        if not fields:
            # No specific fields requested, try generic extraction
            data = self._extract_generic(content)
            if data:
                result.success = True
                result.data = data
                result.fields_found = set(data.keys())
                result.confidence = 0.5  # Lower confidence for generic extraction
            return result

        # Extract specific fields
        for field in fields:
            value = self._extract_field(field, content)
            if value is not None:
                result.data[field] = value
                result.fields_found.add(field)
            else:
                result.fields_missing.add(field)

        # Calculate confidence based on extraction success
        if result.fields_found:
            result.success = True
            result.confidence = result.completeness
            result.metadata["extraction_method"] = "field_patterns"

        return result

    def _extract_field(self, field_name: str, content: str) -> Any | None:
        """
        Extract a specific field from content.

        Tries multiple patterns to find the field value.
        """
        # Pattern 1: JSON-like "field": value
        pattern1 = rf'"{field_name}"\s*:\s*("(?:[^"\\]|\\.)*"|\d+\.?\d*|true|false|null)'
        match = re.search(pattern1, content, re.IGNORECASE)
        if match:
            value_str = match.group(1)
            return self._parse_value(value_str)

        # Pattern 2: Field without quotes: field: value
        pattern2 = rf"\b{field_name}\s*:\s*(.+?)(?:\n|,|\}}|$)"
        match = re.search(pattern2, content, re.IGNORECASE)
        if match:
            value_str = match.group(1).strip()
            return self._parse_value(value_str)

        # Pattern 3: Assignment: field = value
        pattern3 = rf"\b{field_name}\s*=\s*(.+?)(?:\n|,|;|$)"
        match = re.search(pattern3, content, re.IGNORECASE)
        if match:
            value_str = match.group(1).strip()
            return self._parse_value(value_str)

        # Pattern 4: Natural language: "field is value" or "field: value"
        pattern4 = rf"\b{field_name}\s+is\s+(.+?)(?:\n|\.|\,|$)"
        match = re.search(pattern4, content, re.IGNORECASE)
        if match:
            value_str = match.group(1).strip()
            return self._parse_value(value_str)

        return None

    def _parse_value(self, value_str: str) -> Any:
        """
        Parse a value string into appropriate Python type.

        Args:
            value_str: String representation of value

        Returns:
            Parsed value
        """
        value_str = value_str.strip().rstrip(",;")

        # Try JSON parsing first
        try:
            return json.loads(value_str)
        except (json.JSONDecodeError, ValueError):
            pass

        # Try boolean
        if value_str.lower() in ("true", "yes"):
            return True
        if value_str.lower() in ("false", "no"):
            return False

        # Try null
        if value_str.lower() in ("null", "none"):
            return None

        # Try number
        try:
            if "." in value_str:
                return float(value_str)
            return int(value_str)
        except ValueError:
            pass

        # Remove quotes if present
        if (value_str.startswith('"') and value_str.endswith('"')) or (
            value_str.startswith("'") and value_str.endswith("'")
        ):
            return value_str[1:-1]

        # Return as string
        return value_str

    def _extract_generic(self, content: str) -> dict[str, Any]:
        """
        Extract any key-value pairs from content without specific fields.

        Args:
            content: Content to extract from

        Returns:
            Dictionary of extracted key-value pairs
        """
        data: dict[str, Any] = {}

        # Try to find JSON-like key-value pairs
        # Pattern: "key": value or key: value
        pattern = r'(?:"([^"]+)"|(\w+))\s*:\s*("(?:[^"\\]|\\.)*"|\d+\.?\d*|true|false|null|\[.*?\])'
        matches = re.finditer(pattern, content, re.IGNORECASE)

        for match in matches:
            key = match.group(1) or match.group(2)
            value_str = match.group(3)
            data[key] = self._parse_value(value_str)

        return data


class FieldExtractor:
    """
    Specialized extractor for specific field types.

    Provides domain-specific extraction logic.
    """

    @staticmethod
    def extract_confidence(content: str) -> float | None:
        """
        Extract confidence score from content.

        Looks for confidence values between 0.0 and 1.0.
        """
        # Look for patterns like "confidence: 0.85" or "confidence = 0.85"
        patterns = [
            r"confidence\s*[:=]\s*(\d+\.?\d*)",
            r"confidence[\"']?\s*:\s*(\d+\.?\d*)",
            r"score\s*[:=]\s*(\d+\.?\d*)",
        ]

        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                value = float(match.group(1))
                # Normalize to 0.0-1.0 range
                if value > 1.0 and value <= 100.0:
                    value = value / 100.0
                if 0.0 <= value <= 1.0:
                    return value

        return None

    @staticmethod
    def extract_list(content: str, field_name: str) -> list[Any] | None:
        """
        Extract a list/array field from content.

        Args:
            content: Content to search
            field_name: Name of list field

        Returns:
            Extracted list or None
        """
        # Pattern: "field": [...]
        pattern = rf'"{field_name}"\s*:\s*\[(.*?)\]'
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            list_content = match.group(1)
            try:
                return json.loads(f"[{list_content}]")
            except json.JSONDecodeError:
                # Try splitting by comma
                items = [item.strip().strip("\"'") for item in list_content.split(",")]
                return [item for item in items if item]

        # Pattern: field: item1, item2, item3
        pattern2 = rf"\b{field_name}\s*:\s*(.+?)(?:\n|$)"
        match = re.search(pattern2, content, re.IGNORECASE)
        if match:
            items_str = match.group(1)
            # Try to parse as list
            items = [item.strip().strip("\"'") for item in items_str.split(",")]
            if len(items) > 1:
                return items

        return None

    @staticmethod
    def extract_boolean(content: str, field_name: str) -> bool | None:
        """
        Extract a boolean field from content.

        Args:
            content: Content to search
            field_name: Name of boolean field

        Returns:
            Extracted boolean or None
        """
        # Pattern: "field": true/false
        pattern = rf'"{field_name}"\s*:\s*(true|false)'
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return match.group(1).lower() == "true"

        # Pattern: field is yes/no/true/false
        pattern2 = rf"\b{field_name}\s+is\s+(yes|no|true|false)"
        match = re.search(pattern2, content, re.IGNORECASE)
        if match:
            value = match.group(1).lower()
            return value in ("yes", "true")

        return None

    @staticmethod
    def extract_number(content: str, field_name: str, is_float: bool = False) -> int | float | None:
        """
        Extract a numeric field from content.

        Args:
            content: Content to search
            field_name: Name of numeric field
            is_float: Whether to parse as float

        Returns:
            Extracted number or None
        """
        # Pattern: "field": number
        pattern = rf'"{field_name}"\s*:\s*(\d+\.?\d*)'
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            num_str = match.group(1)
            return float(num_str) if is_float or "." in num_str else int(float(num_str))

        # Pattern: field = number or field: number
        pattern2 = rf"\b{field_name}\s*[:=]\s*(\d+\.?\d*)"
        match = re.search(pattern2, content, re.IGNORECASE)
        if match:
            num_str = match.group(1)
            return float(num_str) if is_float or "." in num_str else int(float(num_str))

        return None


def extract_partial_response(
    content: str, expected_fields: set[str] | None = None
) -> ExtractionResult:
    """
    Convenience function for partial extraction.

    Args:
        content: Malformed response content
        expected_fields: Fields to extract

    Returns:
        ExtractionResult with salvaged data
    """
    extractor = PartialExtractor(required_fields=expected_fields)
    return extractor.extract(content, expected_fields)
