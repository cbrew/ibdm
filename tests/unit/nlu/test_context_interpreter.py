"""Tests for context-aware interpretation pipeline."""

import pytest

from ibdm.core.information_state import InformationState
from ibdm.core.questions import WhQuestion, YNQuestion
from ibdm.nlu.context_interpreter import (
    ContextInterpreter,
    ContextInterpreterConfig,
    ImplicatureType,
    TopicShiftType,
    create_interpreter,
)


class TestContextInterpreterConfig:
    """Tests for ContextInterpreterConfig."""

    def test_default_config(self):
        """Test default configuration."""
        config = ContextInterpreterConfig()

        assert config.llm_config is None
        assert config.use_semantic_parser is True
        assert config.use_dialogue_act_classifier is True
        assert config.use_question_analyzer is True
        assert config.use_answer_parser is True
        assert config.detect_implicatures is True
        assert config.track_topics is True
        assert config.confidence_threshold == 0.5

    def test_custom_config(self):
        """Test custom configuration."""
        config = ContextInterpreterConfig(
            use_semantic_parser=False,
            detect_implicatures=False,
            track_topics=False,
            confidence_threshold=0.7,
        )

        assert config.use_semantic_parser is False
        assert config.detect_implicatures is False
        assert config.track_topics is False
        assert config.confidence_threshold == 0.7


class TestContextInterpreterInitialization:
    """Tests for ContextInterpreter initialization."""

    def test_initialization_without_api_key(self):
        """Test that initialization fails gracefully without API key."""
        try:
            interpreter = ContextInterpreter()
            # If we get here, API key must be set
            assert interpreter is not None
        except ValueError as e:
            # Expected if IBDM_API_KEY not set
            assert "IBDM_API_KEY" in str(e)

    def test_initialization_with_custom_config(self):
        """Test initialization with custom config."""
        config = ContextInterpreterConfig(use_semantic_parser=False)

        try:
            interpreter = ContextInterpreter(config)
            assert interpreter.config.use_semantic_parser is False
            assert interpreter.semantic_parser is None
        except ValueError as e:
            # Expected if API key not set
            assert "IBDM_API_KEY" in str(e)


class TestContextExtraction:
    """Tests for context extraction from Information State."""

    def test_extract_empty_context(self):
        """Test extracting context from empty information state."""
        try:
            interpreter = ContextInterpreter()
            state = InformationState()

            context = interpreter._extract_context_summary(state)

            assert context["qud_stack"] == []
            assert context["qud_top"] is None
            assert context["commitments"] == []
            assert context["recent_moves"] == []
            assert context["current_topic"] is None
            assert context["topic_history"] == []
        except ValueError:
            # Expected if API key not set
            pytest.skip("IBDM_API_KEY not configured")

    def test_extract_context_with_qud(self):
        """Test extracting context with QUD stack."""
        try:
            interpreter = ContextInterpreter()
            state = InformationState()

            # Add questions to QUD stack
            q1 = WhQuestion(variable="x", predicate="weather(x)")
            q2 = YNQuestion(proposition="raining")
            state.shared.push_qud(q1)
            state.shared.push_qud(q2)

            context = interpreter._extract_context_summary(state)

            assert len(context["qud_stack"]) == 2
            assert context["qud_top"] is not None
            assert "raining" in context["qud_top"]
        except ValueError:
            pytest.skip("IBDM_API_KEY not configured")

    def test_extract_context_with_commitments(self):
        """Test extracting context with commitments."""
        try:
            interpreter = ContextInterpreter()
            state = InformationState()

            state.shared.commitments.add("weather(sunny)")
            state.shared.commitments.add("temperature(warm)")

            context = interpreter._extract_context_summary(state)

            assert len(context["commitments"]) == 2
            assert "weather(sunny)" in context["commitments"]
            assert "temperature(warm)" in context["commitments"]
        except ValueError:
            pytest.skip("IBDM_API_KEY not configured")


class TestTopicAnalysis:
    """Tests for topic tracking and shift detection."""

    def test_extract_topic_from_parse(self):
        """Test topic extraction from semantic parse."""
        try:
            interpreter = ContextInterpreter()

            parse = {
                "predicate": "weather",
                "arguments": [{"role": "location", "value": "Stockholm"}],
                "modifiers": [],
            }

            topic = interpreter._extract_topic_from_parse(parse)

            assert topic == "weather"
        except ValueError:
            pytest.skip("IBDM_API_KEY not configured")

    def test_topic_continuation(self):
        """Test detecting topic continuation."""
        try:
            interpreter = ContextInterpreter()
            interpreter.current_topic = "weather"

            context = {"current_topic": "weather", "topic_history": []}

            shift = interpreter._determine_topic_shift("weather", context)

            assert shift == TopicShiftType.CONTINUATION.value
        except ValueError:
            pytest.skip("IBDM_API_KEY not configured")

    def test_topic_shift(self):
        """Test detecting new topic."""
        try:
            interpreter = ContextInterpreter()
            interpreter.current_topic = "weather"

            context = {"current_topic": "weather", "topic_history": []}

            shift = interpreter._determine_topic_shift("traffic", context)

            assert shift == TopicShiftType.SHIFT.value
        except ValueError:
            pytest.skip("IBDM_API_KEY not configured")

    def test_topic_return(self):
        """Test detecting return to previous topic."""
        try:
            interpreter = ContextInterpreter()
            interpreter.current_topic = "traffic"

            context = {"current_topic": "traffic", "topic_history": ["weather", "time"]}

            shift = interpreter._determine_topic_shift("weather", context)

            assert shift == TopicShiftType.RETURN.value
        except ValueError:
            pytest.skip("IBDM_API_KEY not configured")

    def test_topics_related(self):
        """Test checking if topics are related."""
        try:
            interpreter = ContextInterpreter()

            # Related topics (share words)
            assert interpreter._topics_related("weather_forecast", "weather_report")
            assert interpreter._topics_related("travel_booking", "travel_info")

            # Unrelated topics
            assert not interpreter._topics_related("weather", "music")
        except ValueError:
            pytest.skip("IBDM_API_KEY not configured")


class TestImplicatureDetection:
    """Tests for conversational implicature detection."""

    def test_detect_indirect_request(self):
        """Test detecting indirect requests."""
        try:
            interpreter = ContextInterpreter()

            # Indirect requests
            assert interpreter._is_indirect_request("Can you help me?")
            assert interpreter._is_indirect_request("Could you please open the door?")
            assert interpreter._is_indirect_request("Would you turn on the light?")

            # Not indirect requests
            assert not interpreter._is_indirect_request("What time is it?")
            assert not interpreter._is_indirect_request("The weather is nice.")
        except ValueError:
            pytest.skip("IBDM_API_KEY not configured")

    def test_extract_presuppositions(self):
        """Test extracting presuppositions."""
        try:
            interpreter = ContextInterpreter()

            parse = {"predicate": "unknown", "arguments": [], "modifiers": []}

            # Definite description presupposition
            presups = interpreter._extract_presuppositions("Where is the cat?", parse)
            assert any("definite" in p.lower() for p in presups)

            # Factive verb presupposition
            parse_factive = {"predicate": "know", "arguments": [], "modifiers": []}
            presups = interpreter._extract_presuppositions("I know it's raining.", parse_factive)
            assert any("truth" in p.lower() or "proposition" in p.lower() for p in presups)
        except ValueError:
            pytest.skip("IBDM_API_KEY not configured")


class TestConfidenceCalculation:
    """Tests for confidence scoring."""

    def test_high_confidence(self):
        """Test high confidence with complete interpretation."""
        try:
            interpreter = ContextInterpreter()

            parse = {
                "predicate": "weather",
                "arguments": [{"role": "location", "value": "Stockholm"}],
                "modifiers": [],
            }

            confidence = interpreter._calculate_confidence(parse, "question", "weather")

            assert confidence > 0.6  # Should be relatively high
        except ValueError:
            pytest.skip("IBDM_API_KEY not configured")

    def test_low_confidence(self):
        """Test low confidence with incomplete interpretation."""
        try:
            interpreter = ContextInterpreter()

            parse = {"predicate": "unknown", "arguments": [], "modifiers": []}

            confidence = interpreter._calculate_confidence(parse, "unknown", None)

            assert confidence < 0.6  # Should be relatively low
        except ValueError:
            pytest.skip("IBDM_API_KEY not configured")


@pytest.mark.skipif(
    "not config.getoption('--run-llm')",
    reason="Requires --run-llm flag and IBDM_API_KEY",
)
class TestContextInterpreterIntegration:
    """Integration tests for ContextInterpreter (requires LLM API)."""

    def test_interpret_simple_question(self):
        """Test interpreting a simple question."""
        interpreter = create_interpreter()
        state = InformationState()

        interpretation = interpreter.interpret("What's the weather like?", state)

        assert interpretation.utterance == "What's the weather like?"
        assert interpretation.dialogue_act in ["question", "unknown"]
        assert interpretation.semantic_parse is not None
        assert interpretation.confidence > 0.0

    def test_interpret_with_qud_context(self):
        """Test interpretation uses QUD context."""
        interpreter = create_interpreter()
        state = InformationState()

        # Add question to QUD
        q = WhQuestion(variable="x", predicate="weather(x)")
        state.shared.push_qud(q)

        interpretation = interpreter.interpret("It's sunny.", state)

        assert interpretation.dialogue_act is not None
        assert "qud_top" in interpretation.context_used
        assert interpretation.context_used["qud_top"] is not None

    def test_interpret_with_topic_tracking(self):
        """Test topic tracking across utterances."""
        interpreter = create_interpreter()
        state = InformationState()

        # First utterance - new topic
        interpreter.interpret("What's the weather?", state)

        # Second utterance - same topic
        interp2 = interpreter.interpret("Is it raining?", state)

        assert interp2.topic_shift in [
            TopicShiftType.CONTINUATION.value,
            TopicShiftType.SHIFT.value,
        ]

    def test_interpret_indirect_request(self):
        """Test detecting indirect requests."""
        interpreter = create_interpreter()
        state = InformationState()

        interpretation = interpreter.interpret("Can you help me?", state)

        # Should detect indirect request implicature
        implicature_types = [imp["type"] for imp in interpretation.implicatures]
        assert ImplicatureType.INDIRECT_REQUEST.value in implicature_types

    def test_interpret_with_presupposition(self):
        """Test detecting presuppositions."""
        interpreter = create_interpreter()
        state = InformationState()

        interpretation = interpreter.interpret("Where is the museum?", state)

        # Should detect presupposition
        implicature_types = [imp["type"] for imp in interpretation.implicatures]
        assert ImplicatureType.PRESUPPOSITION.value in implicature_types

    def test_interpret_empty_utterance(self):
        """Test that empty utterance raises ValueError."""
        interpreter = create_interpreter()
        state = InformationState()

        with pytest.raises(ValueError, match="empty"):
            interpreter.interpret("", state)

        with pytest.raises(ValueError, match="empty"):
            interpreter.interpret("   ", state)

    def test_minimal_interpreter(self):
        """Test creating minimal interpreter without optional features."""
        interpreter = create_interpreter(
            detect_implicatures=False,
            track_topics=False,
        )

        state = InformationState()
        interpretation = interpreter.interpret("Hello", state)

        # Should still work but with no implicatures or topic tracking
        assert interpretation.implicatures == []
        assert interpretation.topic_shift in [TopicShiftType.NONE.value, "none"]


class TestCreateInterpreter:
    """Tests for create_interpreter convenience function."""

    def test_create_full_interpreter(self):
        """Test creating full-featured interpreter."""
        try:
            interpreter = create_interpreter()
            assert interpreter.config.use_semantic_parser is True
            assert interpreter.config.detect_implicatures is True
            assert interpreter.config.track_topics is True
        except ValueError as e:
            assert "IBDM_API_KEY" in str(e)

    def test_create_minimal_interpreter(self):
        """Test creating minimal interpreter."""
        try:
            interpreter = create_interpreter(
                use_semantic_parser=False,
                detect_implicatures=False,
                track_topics=False,
            )
            assert interpreter.config.use_semantic_parser is False
            assert interpreter.config.detect_implicatures is False
            assert interpreter.config.track_topics is False
        except ValueError as e:
            assert "IBDM_API_KEY" in str(e)
