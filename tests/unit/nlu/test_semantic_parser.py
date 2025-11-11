"""Tests for semantic parser module."""

import pytest

from ibdm.nlu.semantic_parser import (
    SemanticArgument,
    SemanticModifier,
    SemanticParse,
    SemanticParser,
    SemanticParserConfig,
    create_parser,
)


class TestSemanticParseModel:
    """Tests for SemanticParse Pydantic model."""

    def test_create_basic_parse(self):
        """Test creating a basic semantic parse."""
        parse = SemanticParse(
            predicate="drive",
            arguments=[SemanticArgument(role="agent", value="Alice")],
            modifiers=[SemanticModifier(type="time", value="yesterday")],
        )

        assert parse.predicate == "drive"
        assert len(parse.arguments) == 1
        assert len(parse.modifiers) == 1
        assert parse.arguments[0].role == "agent"
        assert parse.arguments[0].value == "Alice"

    def test_empty_arguments_and_modifiers(self):
        """Test parse with no arguments or modifiers."""
        parse = SemanticParse(predicate="rain")

        assert parse.predicate == "rain"
        assert parse.arguments == []
        assert parse.modifiers == []


class TestSemanticParserConfig:
    """Tests for SemanticParserConfig."""

    def test_default_config(self):
        """Test default configuration."""
        config = SemanticParserConfig()

        assert config.llm_config is None
        assert config.include_reasoning is True
        assert config.use_fast_model is False

    def test_custom_config(self):
        """Test custom configuration."""
        config = SemanticParserConfig(include_reasoning=False, use_fast_model=True)

        assert config.include_reasoning is False
        assert config.use_fast_model is True


@pytest.mark.skipif(
    "not config.getoption('--run-llm')",
    reason="Requires --run-llm flag and IBDM_API_KEY",
)
class TestSemanticParser:
    """Tests for SemanticParser (requires LLM API)."""

    def test_parser_initialization(self):
        """Test parser can be initialized."""
        parser = SemanticParser()
        assert parser is not None
        assert parser.llm is not None
        assert parser.template is not None

    def test_parse_simple_sentence(self):
        """Test parsing a simple sentence."""
        parser = create_parser(use_fast_model=True, include_reasoning=False)

        result = parser.parse("Alice drove to the airport.")

        assert result.predicate is not None
        assert len(result.arguments) > 0
        # Should identify Alice as agent
        agent_args = [arg for arg in result.arguments if arg.role == "agent"]
        assert len(agent_args) > 0

    def test_parse_with_modifiers(self):
        """Test parsing sentence with modifiers."""
        parser = create_parser(use_fast_model=True, include_reasoning=False)

        result = parser.parse("Alice quickly drove to the airport yesterday.")

        assert result.predicate is not None
        assert len(result.modifiers) > 0
        # Should have manner and/or time modifiers
        modifier_types = [mod.type for mod in result.modifiers]
        assert any(t in ["manner", "time"] for t in modifier_types)

    def test_parse_with_context(self):
        """Test parsing with context."""
        parser = create_parser(use_fast_model=True, include_reasoning=False)
        context = {"domain": "travel"}

        result = parser.parse("She went there.", context=context)

        assert result.predicate is not None

    @pytest.mark.asyncio
    async def test_async_parse(self):
        """Test async parsing."""
        parser = create_parser(use_fast_model=True, include_reasoning=False)

        result = await parser.aparse("The cat is sleeping on the couch.")

        assert result.predicate is not None
        assert len(result.arguments) > 0

    @pytest.mark.asyncio
    async def test_batch_parse(self):
        """Test batch parsing multiple utterances."""
        parser = create_parser(use_fast_model=True, include_reasoning=False)

        utterances = [
            "Alice drove to work.",
            "Bob is reading a book.",
            "The weather is nice.",
        ]

        results = await parser.batch_parse(utterances)

        assert len(results) == 3
        for result in results:
            assert result.predicate is not None


class TestCreateParser:
    """Tests for create_parser convenience function."""

    def test_create_fast_parser(self):
        """Test creating a parser with fast model."""
        # This will fail without API key, but we can test the config
        try:
            parser = create_parser(use_fast_model=True, include_reasoning=False)
            assert parser.config.use_fast_model is True
            assert parser.config.include_reasoning is False
        except ValueError as e:
            # Expected if API key not set
            assert "IBDM_API_KEY" in str(e)

    def test_create_detailed_parser(self):
        """Test creating a parser with detailed reasoning."""
        try:
            parser = create_parser(use_fast_model=False, include_reasoning=True)
            assert parser.config.use_fast_model is False
            assert parser.config.include_reasoning is True
        except ValueError as e:
            # Expected if API key not set
            assert "IBDM_API_KEY" in str(e)
