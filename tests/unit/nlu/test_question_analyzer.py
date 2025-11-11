"""Tests for question analyzer module."""

import pytest

from ibdm.core.questions import AltQuestion, WhQuestion, YNQuestion
from ibdm.nlu.question_analyzer import (
    QuestionAnalysis,
    QuestionAnalyzer,
    QuestionAnalyzerConfig,
    QuestionType,
    create_analyzer,
)


class TestQuestionAnalysis:
    """Tests for QuestionAnalysis Pydantic model."""

    def test_create_wh_analysis(self):
        """Test creating a wh-question analysis."""
        analysis = QuestionAnalysis(
            type="wh",
            focus="Italian restaurant",
            presuppositions=["There are Italian restaurants", "Some are better than others"],
            constraints=["Location: downtown", "Cuisine: Italian"],
        )

        assert analysis.type == "wh"
        assert analysis.focus == "Italian restaurant"
        assert len(analysis.presuppositions) == 2
        assert len(analysis.constraints) == 2

    def test_create_yn_analysis(self):
        """Test creating a yes-no question analysis."""
        analysis = QuestionAnalysis(
            type="yes-no",
            focus="museum opening status",
            presuppositions=["A museum exists"],
            constraints=["Day: Sunday"],
        )

        assert analysis.type == "yes-no"
        assert analysis.focus == "museum opening status"

    def test_get_type(self):
        """Test converting type string to enum."""
        analysis = QuestionAnalysis(type="wh", focus="test")
        assert analysis.get_type() == QuestionType.WH

        analysis = QuestionAnalysis(type="yes-no", focus="test")
        assert analysis.get_type() == QuestionType.YES_NO

        analysis = QuestionAnalysis(type="alternative", focus="test")
        assert analysis.get_type() == QuestionType.ALTERNATIVE

    def test_get_type_unknown(self):
        """Test unknown type defaults to WH."""
        analysis = QuestionAnalysis(type="unknown", focus="test")
        assert analysis.get_type() == QuestionType.WH


class TestQuestionAnalyzerConfig:
    """Tests for QuestionAnalyzerConfig."""

    def test_default_config(self):
        """Test default configuration."""
        config = QuestionAnalyzerConfig()

        assert config.llm_config is None
        assert config.include_reasoning is True
        assert config.use_fast_model is False  # Question understanding uses Sonnet

    def test_custom_config(self):
        """Test custom configuration."""
        config = QuestionAnalyzerConfig(include_reasoning=False, use_fast_model=True)

        assert config.include_reasoning is False
        assert config.use_fast_model is True


@pytest.mark.skipif(
    "not config.getoption('--run-llm')",
    reason="Requires --run-llm flag and IBDM_API_KEY",
)
class TestQuestionAnalyzer:
    """Tests for QuestionAnalyzer (requires LLM API)."""

    def test_analyzer_initialization(self):
        """Test analyzer can be initialized."""
        analyzer = QuestionAnalyzer()
        assert analyzer is not None
        assert analyzer.llm is not None
        assert analyzer.template is not None

    def test_analyze_wh_question(self):
        """Test analyzing a wh-question."""
        analyzer = create_analyzer(use_fast_model=True, include_reasoning=False)

        result = analyzer.analyze("What's the best Italian restaurant in downtown?")

        assert result.type == "wh"
        assert "restaurant" in result.focus.lower() or "italian" in result.focus.lower()
        assert len(result.constraints) > 0

    def test_analyze_yn_question(self):
        """Test analyzing a yes-no question."""
        analyzer = create_analyzer(use_fast_model=True, include_reasoning=False)

        result = analyzer.analyze("Is the museum open on Sundays?")

        assert result.type == "yes-no"
        assert "museum" in result.focus.lower() or "open" in result.focus.lower()

    def test_analyze_alternative_question(self):
        """Test analyzing an alternative question."""
        analyzer = create_analyzer(use_fast_model=True, include_reasoning=False)

        result = analyzer.analyze("Should we meet at 2pm or 3pm?")

        assert result.type == "alternative"
        assert "meeting" in result.focus.lower() or "time" in result.focus.lower()

    def test_to_question_object_wh(self):
        """Test converting analysis to WhQuestion object."""
        analyzer = create_analyzer(use_fast_model=True, include_reasoning=False)

        question = analyzer.to_question_object("What's the weather?")

        assert isinstance(question, WhQuestion)
        assert question.variable is not None
        assert question.predicate is not None

    def test_to_question_object_yn(self):
        """Test converting analysis to YNQuestion object."""
        analyzer = create_analyzer(use_fast_model=True, include_reasoning=False)

        question = analyzer.to_question_object("Is it raining?")

        # Should be YNQuestion if classified correctly
        assert isinstance(question, (YNQuestion, WhQuestion))
        if isinstance(question, YNQuestion):
            assert question.proposition is not None

    def test_to_question_object_alternative(self):
        """Test converting analysis to AltQuestion object."""
        analyzer = create_analyzer(use_fast_model=True, include_reasoning=False)

        question = analyzer.to_question_object("Tea or coffee?")

        # Should be AltQuestion if classified correctly
        assert isinstance(question, (AltQuestion, WhQuestion))
        if isinstance(question, AltQuestion):
            assert len(question.alternatives) > 0

    def test_to_question_object_with_precomputed_analysis(self):
        """Test converting with pre-computed analysis."""
        analyzer = create_analyzer(use_fast_model=True, include_reasoning=False)

        # Pre-compute analysis
        analysis = QuestionAnalysis(
            type="wh",
            focus="weather",
            presuppositions=[],
            constraints=["time: tomorrow"],
        )

        question = analyzer.to_question_object("What's the weather tomorrow?", analysis=analysis)

        assert isinstance(question, WhQuestion)
        assert question.predicate == "weather"

    @pytest.mark.asyncio
    async def test_async_analyze(self):
        """Test async analysis."""
        analyzer = create_analyzer(use_fast_model=True, include_reasoning=False)

        result = await analyzer.aanalyze("Where is Stockholm?")

        assert result.type == "wh"
        assert len(result.focus) > 0

    @pytest.mark.asyncio
    async def test_batch_analyze(self):
        """Test batch analysis."""
        analyzer = create_analyzer(use_fast_model=True, include_reasoning=False)

        questions = [
            "What's the time?",
            "Is it raining?",
            "Coffee or tea?",
        ]

        results = await analyzer.batch_analyze(questions)

        assert len(results) == 3
        assert results[0].type == "wh"
        assert results[1].type == "yes-no"
        assert results[2].type == "alternative"


class TestCreateAnalyzer:
    """Tests for create_analyzer convenience function."""

    def test_create_detailed_analyzer(self):
        """Test creating an analyzer with detailed reasoning."""
        try:
            analyzer = create_analyzer(use_fast_model=False, include_reasoning=True)
            assert analyzer.config.use_fast_model is False
            assert analyzer.config.include_reasoning is True
        except ValueError as e:
            # Expected if API key not set
            assert "IBDM_API_KEY" in str(e)

    def test_create_fast_analyzer(self):
        """Test creating a fast analyzer."""
        try:
            analyzer = create_analyzer(use_fast_model=True, include_reasoning=False)
            assert analyzer.config.use_fast_model is True
            assert analyzer.config.include_reasoning is False
        except ValueError as e:
            # Expected if API key not set
            assert "IBDM_API_KEY" in str(e)
