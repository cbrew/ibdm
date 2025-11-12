"""
Multi-format response parsers for LLM outputs.

Supports JSON, XML, and structured text formats with robust error handling
and diagnostic information.
"""

import json
import re
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from dataclasses import dataclass
from dataclasses import field as dataclass_field
from enum import Enum
from typing import Any


class ParseFormat(Enum):
    """Supported parsing formats."""

    JSON = "json"
    XML = "xml"
    STRUCTURED_TEXT = "structured_text"
    UNKNOWN = "unknown"


@dataclass
class ParseResult:
    """
    Result of parsing an LLM response.

    Attributes:
        success: Whether parsing succeeded
        data: Parsed data (if successful)
        format: Detected format
        raw_content: Original unparsed content
        errors: List of error messages
        extracted_content: Content extracted before parsing (e.g., from code blocks)
        metadata: Additional parsing metadata
    """

    success: bool
    data: Any = None
    format: ParseFormat = ParseFormat.UNKNOWN
    raw_content: str = ""
    errors: list[str] = dataclass_field(default_factory=list)
    extracted_content: str | None = None
    metadata: dict[str, Any] = dataclass_field(default_factory=dict)

    @property
    def failed(self) -> bool:
        """Whether parsing failed."""
        return not self.success

    def add_error(self, error: str) -> None:
        """Add an error message."""
        self.errors.append(error)


class ResponseParser(ABC):
    """Abstract base class for response parsers."""

    @abstractmethod
    def parse(self, content: str) -> ParseResult:
        """
        Parse LLM response content.

        Args:
            content: Raw response text from LLM

        Returns:
            ParseResult with parsed data or errors
        """
        pass

    @abstractmethod
    def can_parse(self, content: str) -> bool:
        """
        Check if this parser can handle the content.

        Args:
            content: Content to check

        Returns:
            True if this parser can handle the content
        """
        pass

    @staticmethod
    def detect_format(content: str) -> ParseFormat:
        """
        Detect the format of the content.

        Args:
            content: Content to analyze

        Returns:
            Detected ParseFormat
        """
        content = content.strip()

        # Check for JSON
        if content.startswith("{") or content.startswith("["):
            return ParseFormat.JSON

        # Check for XML
        if content.startswith("<") and ">" in content:
            return ParseFormat.XML

        # Check for JSON in markdown code blocks
        if "```json" in content.lower() or "```" in content:
            return ParseFormat.JSON

        return ParseFormat.UNKNOWN


class JSONParser(ResponseParser):
    """
    Parser for JSON responses.

    Handles:
    - Pure JSON objects/arrays
    - JSON within markdown code blocks
    - JSON with surrounding text
    """

    def can_parse(self, content: str) -> bool:
        """Check if content appears to be JSON."""
        return self.detect_format(content) == ParseFormat.JSON or "```json" in content.lower()

    def parse(self, content: str) -> ParseResult:
        """
        Parse JSON from LLM response.

        Handles multiple formats:
        1. Pure JSON: {"key": "value"}
        2. Markdown code blocks: ```json\n{...}\n```
        3. Mixed content: "Here's the result: {...}"
        """
        result = ParseResult(
            success=False, format=ParseFormat.JSON, raw_content=content, metadata={}
        )

        # Extract JSON from markdown code blocks
        extracted = self._extract_from_code_block(content)
        if extracted:
            result.extracted_content = extracted
            content_to_parse = extracted
        else:
            content_to_parse = content.strip()

        # Try to find JSON object/array in the content
        json_content = self._find_json(content_to_parse)
        if not json_content:
            result.add_error("No JSON object or array found in content")
            return result

        # Parse JSON
        try:
            result.data = json.loads(json_content)
            result.success = True
            result.metadata["content_length"] = len(json_content)
            return result
        except json.JSONDecodeError as e:
            result.add_error(f"JSON decode error: {e.msg} at position {e.pos}")
            result.metadata["error_position"] = e.pos
            return result

    def _extract_from_code_block(self, content: str) -> str | None:
        """Extract JSON from markdown code blocks."""
        # Pattern for ```json ... ``` or ``` ... ```
        pattern = r"```(?:json)?\s*\n(.*?)\n```"
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None

    def _find_json(self, content: str) -> str | None:
        """Find JSON object or array in content."""
        content = content.strip()

        # Try the whole content first
        if content.startswith(("{", "[")):
            return content

        # Look for JSON object
        obj_match = re.search(r"\{.*\}", content, re.DOTALL)
        if obj_match:
            return obj_match.group(0)

        # Look for JSON array
        arr_match = re.search(r"\[.*\]", content, re.DOTALL)
        if arr_match:
            return arr_match.group(0)

        return None


class XMLParser(ResponseParser):
    """
    Parser for XML responses.

    Handles:
    - Pure XML documents
    - XML within markdown code blocks
    - XML with surrounding text
    """

    def can_parse(self, content: str) -> bool:
        """Check if content appears to be XML."""
        return self.detect_format(content) == ParseFormat.XML or "```xml" in content.lower()

    def parse(self, content: str) -> ParseResult:
        """
        Parse XML from LLM response.

        Returns a dictionary representation of the XML tree.
        """
        result = ParseResult(
            success=False, format=ParseFormat.XML, raw_content=content, metadata={}
        )

        # Extract XML from markdown code blocks
        extracted = self._extract_from_code_block(content)
        if extracted:
            result.extracted_content = extracted
            content_to_parse = extracted
        else:
            content_to_parse = content.strip()

        # Find XML content
        xml_content = self._find_xml(content_to_parse)
        if not xml_content:
            result.add_error("No XML document found in content")
            return result

        # Parse XML
        try:
            root = ET.fromstring(xml_content)
            result.data = self._xml_to_dict(root)
            result.success = True
            result.metadata["root_tag"] = root.tag
            result.metadata["content_length"] = len(xml_content)
            return result
        except ET.ParseError as e:
            result.add_error(f"XML parse error: {e.msg} at position {e.position}")
            result.metadata["error_position"] = e.position
            return result

    def _extract_from_code_block(self, content: str) -> str | None:
        """Extract XML from markdown code blocks."""
        pattern = r"```(?:xml)?\s*\n(.*?)\n```"
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None

    def _find_xml(self, content: str) -> str | None:
        """Find XML document in content."""
        content = content.strip()

        # Try the whole content first
        if content.startswith("<"):
            return content

        # Look for XML document
        match = re.search(r"<\w+[^>]*>.*</\w+>", content, re.DOTALL)
        if match:
            return match.group(0)

        return None

    def _xml_to_dict(self, element: ET.Element) -> dict[str, Any]:
        """Convert XML element tree to dictionary."""
        result: dict[str, Any] = {}

        # Add attributes
        if element.attrib:
            result["@attributes"] = dict(element.attrib)

        # Add text content
        if element.text and element.text.strip():
            result["@text"] = element.text.strip()

        # Add child elements
        children = list(element)
        if children:
            for child in children:
                child_data = self._xml_to_dict(child)
                if child.tag in result:
                    # Multiple children with same tag -> convert to list
                    if not isinstance(result[child.tag], list):
                        result[child.tag] = [result[child.tag]]
                    result[child.tag].append(child_data)
                else:
                    result[child.tag] = child_data

        # If only text, return text directly
        if len(result) == 1 and "@text" in result:
            return result["@text"]

        return result or element.text or ""


class StructuredTextParser(ResponseParser):
    """
    Parser for structured text responses.

    Handles key-value pairs in various formats:
    - "key: value"
    - "key = value"
    - "key -> value"
    """

    def can_parse(self, content: str) -> bool:
        """Check if content appears to be structured text."""
        # Look for key-value patterns
        patterns = [r"\w+\s*:\s*", r"\w+\s*=\s*", r"\w+\s*->\s*"]
        return any(re.search(pattern, content) for pattern in patterns)

    def parse(self, content: str) -> ParseResult:
        """
        Parse structured text into dictionary.

        Handles formats like:
            key1: value1
            key2: value2
        Or:
            key1 = value1
            key2 = value2
        """
        result = ParseResult(
            success=False, format=ParseFormat.STRUCTURED_TEXT, raw_content=content, metadata={}
        )

        data: dict[str, str] = {}
        lines = content.strip().split("\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Try different separators
            for separator in [":", "=", "->"]:
                if separator in line:
                    parts = line.split(separator, 1)
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value = parts[1].strip()
                        data[key] = value
                    break

        if data:
            result.data = data
            result.success = True
            result.metadata["num_fields"] = len(data)
        else:
            result.add_error("No structured key-value pairs found")

        return result


class AutoParser:
    """
    Automatic parser that tries multiple formats.

    Attempts to parse content using available parsers in priority order.
    """

    def __init__(self):
        """Initialize with default parsers."""
        self.parsers: list[ResponseParser] = [
            JSONParser(),
            XMLParser(),
            StructuredTextParser(),
        ]

    def parse(self, content: str, prefer_format: ParseFormat | None = None) -> ParseResult:
        """
        Parse content using best available parser.

        Args:
            content: Content to parse
            prefer_format: Preferred format to try first

        Returns:
            ParseResult from first successful parser
        """
        # Try preferred format first
        if prefer_format:
            for parser in self.parsers:
                if ResponseParser.detect_format(content) == prefer_format:
                    if parser.can_parse(content):
                        result = parser.parse(content)
                        if result.success:
                            return result

        # Try all parsers
        for parser in self.parsers:
            if parser.can_parse(content):
                result = parser.parse(content)
                if result.success:
                    return result

        # All parsers failed
        return ParseResult(
            success=False,
            raw_content=content,
            errors=["No parser could successfully parse the content"],
        )

    def add_parser(self, parser: ResponseParser) -> None:
        """Add a custom parser."""
        self.parsers.insert(0, parser)  # Add at front for priority
