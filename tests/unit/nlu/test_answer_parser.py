"""Tests for answer parser module."""

import pytest

from ibdm.core.answers import Answer
from ibdm.core.questions import WhQuestion, YNQuestion
from ibdm.nlu.answer_parser import (
    AnswerAnalysis,
    AnswerParser,
    AnswerParserConfig,
    AnswerType,
    create_parser,
)


class TestAnswerAnalysis:
    """Tests for AnswerAnalysis Pydantic model."""

    def test_create_direct_answer_analysis(self):
        """Test creating a direct answer analysis."""
        analysis = AnswerAnalysis(
            addresses_question=True,
            answer_type="direct",
            propositional_content="store closes at 9pm",
            implied_info=[],
        )

        assert analysis.addresses_question is True
        assert analysis.answer_type == "direct"
        assert analysis.propositional_content == "store closes at 9pm"
        assert len(analysis.implied_info) == 0

    def test_create_over_informative_answer(self):
        """Test creating an over-informative answer analysis."""
        analysis = AnswerAnalysis(
            addresses_question=True,
            answer_type="over-informative",
            propositional_content="restaurant has Michelin star, entrees start at $45",
            implied_info=["yes, it is expensive", "it is high quality"],
        )

        assert analysis.answer_type == "over-informative"
        assert len(analysis.implied_info) == 2

    def test_get_type(self):
        """Test converting answer_type string to enum."""
        analysis = AnswerAnalysis(
            addresses_question=True,
            answer_type="direct",
            propositional_content="test",
        )
        assert analysis.get_type() == AnswerType.DIRECT

        analysis.answer_type = "partial"
        assert analysis.get_type() == AnswerType.PARTIAL

    def test_get_type_unknown(self):
        """Test unknown type raises ValueError (no silent fallback)."""
        analysis = AnswerAnalysis(
            addresses_question=True,
            answer_type="unknown_type",
            propositional_content="test",
        )
        with pytest.raises(ValueError, match="Cannot proceed with invalid answer type"):
            analysis.get_type()


class TestAnswerParserConfig:
    """Tests for AnswerParserConfig."""

    def test_default_config(self):
        """Test default configuration."""
        config = AnswerParserConfig()

        assert config.llm_config is None
        assert config.include_reasoning is True
        assert config.use_fast_model is False  # Answer parsing uses Sonnet

    def test_custom_config(self):
        """Test custom configuration."""
        config = AnswerParserConfig(include_reasoning=False, use_fast_model=True)

        assert config.include_reasoning is False
        assert config.use_fast_model is True


@pytest.mark.skipif(
    "not config.getoption('--run-llm')",
    reason="Requires --run-llm flag and IBDM_API_KEY",
)
class TestAnswerParser:
    """Tests for AnswerParser (requires LLM API)."""

    def test_parser_initialization(self):
        """Test parser can be initialized."""
        parser = AnswerParser()
        assert parser is not None
        assert parser.llm is not None
        assert parser.template is not None

    def test_parse_direct_answer(self):
        """Test parsing a direct answer."""
        parser = create_parser(use_fast_model=True, include_reasoning=False)

        result = parser.parse(
            question_text="What time does the store close?", answer_text="It closes at 9pm."
        )

        assert result.addresses_question is True
        assert result.answer_type == "direct"
        assert "9pm" in result.propositional_content.lower() or "9" in result.propositional_content

    def test_parse_over_informative_answer(self):
        """Test parsing an over-informative answer."""
        parser = create_parser(use_fast_model=True, include_reasoning=False)

        result = parser.parse(
            question_text="Is the restaurant expensive?",
            answer_text="It's a Michelin star restaurant with entrees starting at $45.",
        )

        assert result.addresses_question is True
        assert result.answer_type in ["over-informative", "indirect"]
        assert len(result.implied_info) > 0 or "expensive" in result.propositional_content.lower()

    def test_parse_partial_answer(self):
        """Test parsing a partial answer."""
        parser = create_parser(use_fast_model=True, include_reasoning=False)

        result = parser.parse(question_text="When can we meet?", answer_text="I'm free next week.")

        assert result.addresses_question is True
        # Should be partial since it doesn't give exact time
        assert result.answer_type in ["partial", "direct"]

    def test_to_answer_object(self):
        """Test converting parsed answer to Answer object."""
        parser = create_parser(use_fast_model=True, include_reasoning=False)

        answer_obj = parser.to_answer_object(
            answer_text="It closes at 9pm.", question_text="What time does the store close?"
        )

        assert isinstance(answer_obj, Answer)
        assert answer_obj.content is not None
        assert answer_obj.certainty > 0

    def test_to_answer_object_with_question(self):
        """Test converting with Question reference."""
        parser = create_parser(use_fast_model=True, include_reasoning=False)

        question = WhQuestion(variable="x", predicate="closing_time(store, x)")

        answer_obj = parser.to_answer_object(
            answer_text="It closes at 9pm.",
            question=question,
            question_text="What time does the store close?",
        )

        assert answer_obj.question_ref == question

    def test_to_answer_object_yn_question(self):
        """Test converting yes/no answer."""
        parser = create_parser(use_fast_model=True, include_reasoning=False)

        question = YNQuestion(proposition="raining")

        answer_obj = parser.to_answer_object(
            answer_text="Yes, it's raining.",
            question=question,
            question_text="Is it raining?",
        )

        # Should extract boolean for yes/no question
        assert isinstance(answer_obj.content, (bool, str))

    def test_to_answer_object_with_precomputed_analysis(self):
        """Test converting with pre-computed analysis."""
        parser = create_parser(use_fast_model=True, include_reasoning=False)

        analysis = AnswerAnalysis(
            addresses_question=True,
            answer_type="direct",
            propositional_content="9pm",
            implied_info=[],
        )

        answer_obj = parser.to_answer_object(
            answer_text="9pm", question_text="What time?", analysis=analysis
        )

        assert answer_obj.content == "9pm"
        assert answer_obj.certainty == 1.0

    def test_to_answer_object_partial_certainty(self):
        """Test partial answer has lower certainty."""
        parser = create_parser(use_fast_model=True, include_reasoning=False)

        analysis = AnswerAnalysis(
            addresses_question=True,
            answer_type="partial",
            propositional_content="next week",
            implied_info=[],
        )

        answer_obj = parser.to_answer_object(
            answer_text="next week", question_text="When?", analysis=analysis
        )

        assert answer_obj.certainty < 1.0

    def test_match_to_qud_empty_stack(self):
        """Test matching to empty QUD stack."""
        parser = create_parser(use_fast_model=True, include_reasoning=False)

        question, analysis = parser.match_to_qud(answer_text="It's sunny.", qud_stack=[])

        assert question is None
        assert analysis is None

    def test_match_to_qud_single_question(self):
        """Test matching to QUD stack with single question."""
        parser = create_parser(use_fast_model=True, include_reasoning=False)

        qud_stack = [
            ("What's the weather?", WhQuestion(variable="x", predicate="weather(x)")),
        ]

        question, analysis = parser.match_to_qud(answer_text="It's sunny.", qud_stack=qud_stack)

        # Should match if the answer addresses the question
        if question is not None:
            assert isinstance(question, WhQuestion)
            assert analysis is not None
            assert analysis.addresses_question is True

    def test_match_to_qud_multiple_questions(self):
        """Test matching to QUD stack with multiple questions."""
        parser = create_parser(use_fast_model=True, include_reasoning=False)

        qud_stack = [
            ("What's the weather?", WhQuestion(variable="x", predicate="weather(x)")),
            ("What time is it?", WhQuestion(variable="x", predicate="time(x)")),
        ]

        question, analysis = parser.match_to_qud(answer_text="It's 3pm.", qud_stack=qud_stack)

        # Should match the time question
        if question is not None:
            assert isinstance(question, WhQuestion)
            assert "time" in question.predicate.lower()

    @pytest.mark.asyncio
    async def test_async_parse(self):
        """Test async parsing."""
        parser = create_parser(use_fast_model=True, include_reasoning=False)

        result = await parser.aparse(question_text="What's your name?", answer_text="I'm Alice.")

        assert result.addresses_question is True
        assert result.propositional_content is not None


class TestCreateParser:
    """Tests for create_parser convenience function."""

    def test_create_detailed_parser(self):
        """Test creating a parser with detailed reasoning."""
        try:
            parser = create_parser(use_fast_model=False, include_reasoning=True)
            assert parser.config.use_fast_model is False
            assert parser.config.include_reasoning is True
        except ValueError as e:
            # Expected if API key not set
            assert "IBDM_API_KEY" in str(e)

    def test_create_fast_parser(self):
        """Test creating a fast parser."""
        try:
            parser = create_parser(use_fast_model=True, include_reasoning=False)
            assert parser.config.use_fast_model is True
            assert parser.config.include_reasoning is False
        except ValueError as e:
            # Expected if API key not set
            assert "IBDM_API_KEY" in str(e)
