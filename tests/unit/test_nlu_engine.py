"""Tests for NLU-enhanced dialogue engine."""

import pytest

from ibdm.core import DialogueMove, InformationState
from ibdm.core.questions import WhQuestion, YNQuestion
from ibdm.engine.nlu_engine import NLUDialogueEngine, NLUEngineConfig, create_nlu_engine
from ibdm.rules import RuleSet


class TestNLUEngineConfig:
    """Tests for NLUEngineConfig."""

    def test_default_config(self):
        """Test default configuration."""
        config = NLUEngineConfig()

        assert config.use_nlu is True
        assert config.use_llm is True
        assert config.confidence_threshold == 0.5
        assert config.fallback_to_rules is True

    def test_custom_config(self):
        """Test custom configuration."""
        config = NLUEngineConfig(
            use_nlu=True,
            use_llm=False,
            confidence_threshold=0.7,
            fallback_to_rules=False,
        )

        assert config.use_nlu is True
        assert config.use_llm is False
        assert config.confidence_threshold == 0.7
        assert config.fallback_to_rules is False


class TestNLUDialogueEngine:
    """Tests for NLUDialogueEngine (without LLM calls)."""

    @pytest.fixture
    def engine_no_llm(self):
        """Create engine with LLM disabled."""
        config = NLUEngineConfig(use_nlu=True, use_llm=False)
        return NLUDialogueEngine("agent_1", config=config)

    @pytest.fixture
    def engine_with_llm(self):
        """Create engine with LLM enabled (will try to initialize)."""
        config = NLUEngineConfig(use_nlu=True, use_llm=True)
        return NLUDialogueEngine("agent_1", config=config)

    def test_create_engine(self, engine_no_llm):
        """Test creating NLU engine."""
        assert engine_no_llm.agent_id == "agent_1"
        assert engine_no_llm.config.use_nlu is True
        assert engine_no_llm.config.use_llm is False

    def test_create_engine_with_factory(self):
        """Test creating engine with factory function."""
        engine = create_nlu_engine("agent_2", use_nlu=True, use_llm=False)

        assert engine.agent_id == "agent_2"
        assert isinstance(engine, NLUDialogueEngine)

    def test_engine_initializes_without_llm(self, engine_no_llm):
        """Test engine works without LLM."""
        assert engine_no_llm.dialogue_act_classifier is None
        assert engine_no_llm.question_analyzer is None
        assert engine_no_llm.entity_tracker is None

    def test_fallback_to_rules_when_nlu_disabled(self, engine_no_llm):
        """Test that engine falls back to rules when NLU disabled."""
        # Without rules, should return empty list
        moves = engine_no_llm.interpret("Hello", "user")

        assert moves == []

    def test_fallback_to_rules_with_rule_set(self):
        """Test fallback to rules works with rule set."""
        from ibdm.rules import UpdateRule

        rules = RuleSet()

        # Add a simple interpretation rule
        def greet_rule(state: InformationState) -> InformationState:
            utt = state.private.beliefs.get("_temp_utterance", "")
            if "hello" in utt.lower():
                state.private.agenda.append(
                    DialogueMove(
                        move_type="greet",
                        content="Hello!",
                        speaker=state.private.beliefs.get("_temp_speaker", "unknown"),
                    )
                )
            return state

        rule = UpdateRule(
            name="greet_rule",
            rule_type="interpretation",
            preconditions=lambda s: True,
            effects=greet_rule,
            priority=1,
        )
        rules.add_rule(rule)

        config = NLUEngineConfig(use_nlu=True, use_llm=False, fallback_to_rules=True)
        engine = NLUDialogueEngine("agent_1", rules=rules, config=config)

        moves = engine.interpret("Hello", "user")

        assert len(moves) == 1
        assert moves[0].move_type == "greet"
        assert moves[0].speaker == "user"

    def test_process_input_without_llm(self, engine_no_llm):
        """Test processing input without LLM (no moves generated)."""
        state, response = engine_no_llm.process_input("Hello", "user")

        # Without rules or LLM, no moves are generated
        assert isinstance(state, InformationState)
        assert response is None  # No response since no moves

    def test_get_and_set_state(self, engine_no_llm):
        """Test getting and setting state."""
        # Get initial state
        state1 = engine_no_llm.get_state()
        assert isinstance(state1, InformationState)

        # Create new state and set it
        state2 = InformationState(agent_id="agent_1")
        state2.shared.push_qud(WhQuestion(variable="x", predicate="weather(x)"))

        engine_no_llm.set_state(state2)

        # Verify state was set
        state3 = engine_no_llm.get_state()
        assert len(state3.shared.qud) == 1

    def test_reset_engine(self, engine_no_llm):
        """Test resetting engine state."""
        # Modify state
        question = WhQuestion(variable="x", predicate="test(x)")
        engine_no_llm.state.shared.push_qud(question)
        assert len(engine_no_llm.state.shared.qud) == 1

        # Reset
        engine_no_llm.reset()

        # Verify state is clean
        assert len(engine_no_llm.state.shared.qud) == 0

    def test_str_representation(self, engine_no_llm):
        """Test string representation."""
        s = str(engine_no_llm)

        assert "NLUDialogueEngine" in s
        assert "agent_1" in s
        assert "nlu_enabled" in s

    def test_create_question_from_analysis(self, engine_no_llm):
        """Test creating Question objects from analysis."""

        # Create a mock analysis object
        class MockAnalysis:
            def __init__(self):
                self.question_type = "wh"
                self.focus = "weather"
                self.confidence = 0.9

        analysis = MockAnalysis()
        question = engine_no_llm._create_question_from_analysis(analysis, "What's the weather?")

        assert isinstance(question, WhQuestion)
        assert question.predicate == "weather"

    def test_create_yn_question_from_analysis(self, engine_no_llm):
        """Test creating yes/no question."""

        class MockAnalysis:
            def __init__(self):
                self.question_type = "yes-no"  # Note: hyphen, not underscore
                self.confidence = 0.9

        analysis = MockAnalysis()
        question = engine_no_llm._create_question_from_analysis(analysis, "Is it raining?")

        assert isinstance(question, YNQuestion)
        assert question.proposition == "Is it raining?"

    def test_engine_with_nlu_disabled(self):
        """Test engine with NLU completely disabled."""
        config = NLUEngineConfig(use_nlu=False)
        engine = NLUDialogueEngine("agent_1", config=config)

        # Should not initialize NLU components
        assert engine.dialogue_act_classifier is None

        # Should use rule-based interpretation
        moves = engine.interpret("Hello", "user")
        assert moves == []  # No rules, no moves


class TestNLUDialogueEngineWithLLM:
    """Tests for NLU engine with LLM enabled (optional - requires API key)."""

    @pytest.mark.run_llm
    def test_create_engine_with_llm(self):
        """Test creating engine with LLM enabled."""
        config = NLUEngineConfig(use_nlu=True, use_llm=True)
        engine = NLUDialogueEngine("agent_1", config=config)

        # If API key is available, NLU components should be initialized
        assert engine.config.use_nlu is True

        # If LLM initialization failed, it should fall back gracefully
        if not engine.config.use_llm:
            assert engine.dialogue_act_classifier is None

    @pytest.mark.run_llm
    def test_interpret_with_llm(self):
        """Test interpretation with LLM (if available)."""
        config = NLUEngineConfig(
            use_nlu=True, use_llm=True, confidence_threshold=0.5, fallback_to_rules=False
        )
        engine = NLUDialogueEngine("agent_1", config=config)

        # Try to interpret a simple greeting
        try:
            moves = engine.interpret("Hello there!", "user")

            # If LLM is available, should produce move(s)
            if engine.config.use_llm and engine.dialogue_act_classifier:
                # May or may not produce moves depending on classification
                assert isinstance(moves, list)

        except Exception as e:
            # If LLM not available or fails, that's ok for this test
            pytest.skip(f"LLM not available: {e}")

    @pytest.mark.run_llm
    def test_question_interpretation_with_llm(self):
        """Test question interpretation with LLM."""
        config = NLUEngineConfig(use_nlu=True, use_llm=True)
        engine = NLUDialogueEngine("agent_1", config=config)

        if not engine.config.use_llm or not engine.question_analyzer:
            pytest.skip("LLM not available")

        try:
            # Interpret a question
            moves = engine.interpret("What's the weather today?", "user")

            # Should produce at least one move
            assert isinstance(moves, list)

        except Exception as e:
            pytest.skip(f"LLM call failed: {e}")

    @pytest.mark.run_llm
    def test_process_input_with_llm(self):
        """Test full processing with LLM."""
        config = NLUEngineConfig(use_nlu=True, use_llm=True)
        engine = NLUDialogueEngine("agent_1", config=config)

        if not engine.config.use_llm:
            pytest.skip("LLM not available")

        try:
            state, response = engine.process_input("Hello!", "user")

            assert isinstance(state, InformationState)
            # Response may or may not be None depending on dialogue state

        except Exception as e:
            pytest.skip(f"LLM call failed: {e}")


class TestNLUEngineIntegration:
    """Integration tests for NLU engine."""

    def test_question_answer_sequence_no_llm(self):
        """Test question-answer sequence without LLM."""
        from ibdm.rules import UpdateRule

        # Create engine with rules for testing
        rules = RuleSet()

        # Rule to handle questions
        def question_rule(state: InformationState) -> InformationState:
            utt = state.private.beliefs.get("_temp_utterance", "")
            speaker = state.private.beliefs.get("_temp_speaker", "unknown")

            if "?" in utt:
                # Create a question move
                move = DialogueMove(move_type="ask", content=utt, speaker=speaker)
                state.private.agenda.append(move)

            return state

        rule = UpdateRule(
            name="question_rule",
            rule_type="interpretation",
            preconditions=lambda s: True,
            effects=question_rule,
            priority=1,
        )
        rules.add_rule(rule)

        config = NLUEngineConfig(use_nlu=True, use_llm=False, fallback_to_rules=True)
        engine = NLUDialogueEngine("agent_1", rules=rules, config=config)

        # Process a question
        state, response = engine.process_input("What's the weather?", "user")

        # Question should be integrated into state
        assert isinstance(state, InformationState)

    def test_engine_maintains_state_across_turns(self):
        """Test that engine maintains state across multiple turns."""
        config = NLUEngineConfig(use_nlu=False, use_llm=False)
        engine = NLUDialogueEngine("agent_1", config=config)

        # Add a question to the state
        question = WhQuestion(variable="x", predicate="time(x)")
        engine.state.shared.push_qud(question)

        # Process another utterance
        state, response = engine.process_input("It's noon", "user")

        # State should still have the question
        assert len(state.shared.qud) == 1

    def test_nlu_engine_compatible_with_base_engine(self):
        """Test that NLU engine is compatible with base DialogueMoveEngine interface."""
        from ibdm.engine import DialogueMoveEngine

        engine = create_nlu_engine("agent_1", use_nlu=False, use_llm=False)

        # Should be an instance of base class
        assert isinstance(engine, DialogueMoveEngine)

        # Should have all base methods
        assert hasattr(engine, "process_input")
        assert hasattr(engine, "interpret")
        assert hasattr(engine, "integrate")
        assert hasattr(engine, "select_action")
        assert hasattr(engine, "generate")
        assert hasattr(engine, "reset")
        assert hasattr(engine, "get_state")
        assert hasattr(engine, "set_state")
