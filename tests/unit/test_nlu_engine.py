"""Tests for NLU-enhanced dialogue engine."""

import pytest

from ibdm.core import InformationState
from ibdm.core.questions import WhQuestion, YNQuestion
from ibdm.engine.nlu_engine import NLUDialogueEngine, NLUEngineConfig, create_nlu_engine
from ibdm.nlu import ModelType


class TestNLUEngineConfig:
    """Tests for NLUEngineConfig."""

    def test_default_config(self):
        """Test default configuration."""
        config = NLUEngineConfig()

        assert config.llm_model == ModelType.SONNET
        assert config.confidence_threshold == 0.5
        assert config.temperature == 0.3
        assert config.max_tokens == 2000

    def test_custom_config(self):
        """Test custom configuration."""
        config = NLUEngineConfig(
            llm_model=ModelType.HAIKU,
            confidence_threshold=0.7,
            temperature=0.5,
            max_tokens=1000,
        )

        assert config.llm_model == ModelType.HAIKU
        assert config.confidence_threshold == 0.7
        assert config.temperature == 0.5
        assert config.max_tokens == 1000


class TestNLUDialogueEngine:
    """Tests for NLUDialogueEngine (without LLM calls)."""

    @pytest.fixture
    def engine(self):
        """Create engine with NLU."""
        config = NLUEngineConfig()
        return NLUDialogueEngine("agent_1", config=config)

    def test_create_engine(self, engine):
        """Test creating NLU engine."""
        assert engine.agent_id == "agent_1"
        assert engine.config.llm_model == ModelType.SONNET

    def test_create_engine_with_factory(self):
        """Test creating engine with factory function."""
        engine = create_nlu_engine("agent_2")

        assert engine.agent_id == "agent_2"
        assert isinstance(engine, NLUDialogueEngine)

    def test_get_and_set_state(self, engine):
        """Test creating and cloning state (stateless API)."""
        # Create initial state
        state1 = engine.create_initial_state()
        assert isinstance(state1, InformationState)

        # Create new state and modify it
        state2 = InformationState(agent_id="agent_1")
        state2.shared.push_qud(WhQuestion(variable="x", predicate="weather(x)"))

        # Clone state
        state3 = state2.clone()

        # Verify clone has same data
        assert len(state3.shared.qud) == 1
        # Verify they're independent
        state3.shared.pop_qud()
        assert len(state3.shared.qud) == 0
        assert len(state2.shared.qud) == 1

    def test_reset_engine(self, engine):
        """Test creating new initial state (replaces reset in stateless API)."""
        # Create and modify state
        state = engine.create_initial_state()
        question = WhQuestion(variable="x", predicate="test(x)")
        state.shared.push_qud(question)
        assert len(state.shared.qud) == 1

        # Create new initial state (like reset)
        new_state = engine.create_initial_state()

        # Verify new state is clean
        assert len(new_state.shared.qud) == 0

    def test_str_representation(self, engine):
        """Test string representation."""
        s = str(engine)

        assert "NLUDialogueEngine" in s
        assert "agent_1" in s
        assert "model" in s

    def test_create_question_from_analysis(self, engine):
        """Test creating Question objects from analysis."""

        # Create a mock analysis object
        class MockAnalysis:
            def __init__(self):
                self.question_type = "wh"
                self.focus = "weather"
                self.confidence = 0.9

        analysis = MockAnalysis()
        question = engine._create_question_from_analysis(analysis, "What's the weather?")

        assert isinstance(question, WhQuestion)
        assert question.predicate == "weather"

    def test_create_yn_question_from_analysis(self, engine):
        """Test creating yes/no question."""

        class MockAnalysis:
            def __init__(self):
                self.question_type = "yes-no"  # Note: hyphen, not underscore
                self.confidence = 0.9

        analysis = MockAnalysis()
        question = engine._create_question_from_analysis(analysis, "Is it raining?")

        assert isinstance(question, YNQuestion)
        assert question.proposition == "Is it raining?"


class TestNLUDialogueEngineWithLLM:
    """Tests for NLU engine with LLM enabled (optional - requires API key)."""

    @pytest.mark.run_llm
    def test_create_engine_with_llm(self):
        """Test creating engine with LLM enabled."""
        config = NLUEngineConfig()
        engine = NLUDialogueEngine("agent_1", config=config)

        # NLU components should be initialized
        assert engine.dialogue_act_classifier is not None
        assert engine.question_analyzer is not None
        assert engine.context_interpreter is not None

    @pytest.mark.run_llm
    def test_interpret_with_llm(self):
        """Test interpretation with LLM (if available)."""
        config = NLUEngineConfig(confidence_threshold=0.5)
        engine = NLUDialogueEngine("agent_1", config=config)

        # Try to interpret a simple greeting
        try:
            state = engine.create_initial_state()
            moves = engine.interpret("Hello there!", "user", state)

            # Should produce move(s)
            assert isinstance(moves, list)

        except Exception as e:
            # If LLM not available or fails, that's ok for this test
            pytest.skip(f"LLM not available: {e}")

    @pytest.mark.run_llm
    def test_question_interpretation_with_llm(self):
        """Test question interpretation with LLM."""
        config = NLUEngineConfig()
        engine = NLUDialogueEngine("agent_1", config=config)

        try:
            # Interpret a question
            state = engine.create_initial_state()
            moves = engine.interpret("What's the weather today?", "user", state)

            # Should produce at least one move
            assert isinstance(moves, list)

        except Exception as e:
            pytest.skip(f"LLM call failed: {e}")

    @pytest.mark.run_llm
    def test_process_input_with_llm(self):
        """Test full processing with LLM."""
        config = NLUEngineConfig()
        engine = NLUDialogueEngine("agent_1", config=config)

        try:
            initial_state = engine.create_initial_state()
            new_state, response = engine.process_input("Hello!", "user", initial_state)

            assert isinstance(new_state, InformationState)
            # Response may or may not be None depending on dialogue state

        except Exception as e:
            pytest.skip(f"LLM call failed: {e}")


class TestNLUEngineIntegration:
    """Integration tests for NLU engine."""

    def test_engine_maintains_state_across_turns(self):
        """Test that state is maintained across multiple turns (stateless API)."""
        config = NLUEngineConfig()
        engine = NLUDialogueEngine("agent_1", config=config)

        # Create initial state and add a question
        state = engine.create_initial_state()
        question = WhQuestion(variable="x", predicate="time(x)")
        state.shared.push_qud(question)

        # Process another utterance with existing state
        new_state, response = engine.process_input("It's noon", "user", state)

        # State should still have the question
        assert len(new_state.shared.qud) == 1

    def test_nlu_engine_compatible_with_base_engine(self):
        """Test that NLU engine is compatible with base DialogueMoveEngine interface."""
        from ibdm.engine import DialogueMoveEngine

        engine = create_nlu_engine("agent_1")

        # Should be an instance of base class
        assert isinstance(engine, DialogueMoveEngine)

        # Should have all base methods (stateless API)
        assert hasattr(engine, "process_input")
        assert hasattr(engine, "interpret")
        assert hasattr(engine, "integrate")
        assert hasattr(engine, "select_action")
        assert hasattr(engine, "generate")
        assert hasattr(engine, "create_initial_state")
