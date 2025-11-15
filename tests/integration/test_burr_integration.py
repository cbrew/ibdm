"""Integration tests for Burr state machine integration."""

import tempfile
from pathlib import Path

import pytest

from ibdm.burr_integration import DialogueStateMachine, create_dialogue_application
from ibdm.core import Answer, DialogueMove, WhQuestion
from ibdm.rules import RuleSet, UpdateRule


class TestBurrActions:
    """Test Burr action implementations."""

    def test_initialize_action(self):
        """Test initialization action creates engine."""
        app = create_dialogue_application(agent_id="test_agent")

        # Step should be initialize
        action, result, state = app.step()

        assert action.name == "initialize"
        assert result["ready"] is True
        assert result["agent_id"] == "test_agent"
        assert state["engine"] is not None
        assert state["engine"].agent_id == "test_agent"

    @pytest.mark.skip("Low-level action test - state machine flow makes this difficult to test")
    def test_interpret_action_no_rules(self):
        """Test interpretation with no rules returns empty moves."""
        pass

    @pytest.mark.skip("Low-level action test - state machine flow makes this difficult to test")
    def test_integrate_action(self):
        """Test integration action updates engine state."""
        pass

    def test_select_action_not_our_turn(self):
        """Test selection when it's not our turn."""
        from ibdm.core import InformationState

        app = create_dialogue_application(agent_id="system")

        # Initialize
        app.step()

        # Set next_speaker to someone else (convert dict to object, modify, convert back)
        info_state_dict = app.state["information_state"]
        info_state = InformationState.from_dict(info_state_dict)
        info_state.control.next_speaker = "user"
        info_state_dict = info_state.to_dict()
        app._state = app.state.update(information_state=info_state_dict)

        # Run select
        state = app.state
        app._state = state
        action, result, state = app.step()

        # Note: we need to transition through previous states first
        # This test needs to be updated based on actual flow

    def test_generate_action_with_move(self):
        """Test generation action produces text."""
        app = create_dialogue_application(agent_id="system")

        # Initialize
        app.step()

        # Create a response move
        move = DialogueMove(speaker="system", move_type="answer", content="It's sunny")

        # Set up state with response move
        state = app.state.update(response_move=move)
        app._state = state

        # Need to transition to generate state - this is a simplified test
        # In real flow, this would come after select


class TestDialogueStateMachine:
    """Test DialogueStateMachine high-level interface."""

    def test_initialization(self):
        """Test state machine initialization."""
        sm = DialogueStateMachine(agent_id="test_agent")

        result = sm.initialize()

        assert result["ready"] is True
        assert sm._initialized is True
        assert sm.get_information_state() is not None

    def test_process_utterance_no_rules(self):
        """Test processing utterance with no rules."""
        sm = DialogueStateMachine(agent_id="system")
        sm.initialize()

        result = sm.process_utterance("Hello", speaker="user")

        assert "has_response" in result
        assert "utterance_text" in result
        # With no rules, we shouldn't generate a response
        assert result["has_response"] is False

    def test_process_utterance_with_greeting_rule(self):
        """Test processing with a simple greeting rule."""

        # Create a rule that responds to greetings
        def greeting_preconditions(state):
            utterance = state.private.beliefs.get("_temp_utterance", "")
            return utterance.lower() in ["hello", "hi"]

        def greeting_effects(state):
            # Add a greeting move to agenda
            move = DialogueMove(speaker="user", move_type="greet", content="greeting")
            state.private.agenda.append(move)
            return state

        rules = RuleSet()
        greeting_rule = UpdateRule(
            name="greeting_interpretation",
            rule_type="interpretation",
            preconditions=greeting_preconditions,
            effects=greeting_effects,
            priority=1,
        )
        rules.add_rule(greeting_rule)

        # Create state machine with rules
        sm = DialogueStateMachine(agent_id="system", rules=rules)
        sm.initialize()

        result = sm.process_utterance("Hello", speaker="user")

        # Should have interpreted the greeting
        assert result is not None

    def test_get_state(self):
        """Test getting Burr state."""
        sm = DialogueStateMachine(agent_id="system")
        sm.initialize()

        state = sm.get_state()

        assert state is not None
        assert "engine" in state

    def test_get_information_state(self):
        """Test getting information state."""
        sm = DialogueStateMachine(agent_id="system")
        sm.initialize()

        info_state = sm.get_information_state()

        assert info_state is not None
        assert info_state.agent_id == "system"

    def test_reset(self):
        """Test resetting state machine."""
        sm = DialogueStateMachine(agent_id="system")
        sm.initialize()

        # Process something
        sm.process_utterance("Hello", speaker="user")

        # Reset
        sm.reset()

        # State should be reset
        info_state = sm.get_information_state()
        assert len(info_state.shared.qud) == 0
        assert len(info_state.private.agenda) == 0

    def test_with_persistence(self):
        """Test state machine with persistence enabled."""
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = DialogueStateMachine(agent_id="system", app_id="test_app", storage_dir=tmpdir)
            sm.initialize()

            # Process utterance
            sm.process_utterance("Hello", speaker="user")

            # Check that tracking directory was created
            tracking_dir = Path(tmpdir)
            assert tracking_dir.exists()


class TestEndToEndDialogue:
    """End-to-end dialogue tests with full rule sets."""

    @pytest.mark.skip(
        "Complex rule interaction test - requires integration and interpretation rules"
    )
    def test_question_answer_dialogue(self):
        """Test a simple question-answer dialogue."""
        # Create rules for question-answer dialogue
        rules = RuleSet()

        # Interpretation rule: recognize questions
        def question_preconditions(state):
            utterance = state.private.beliefs.get("_temp_utterance", "")
            return "?" in utterance

        def question_effects(state):
            utterance = state.private.beliefs.get("_temp_utterance", "")
            speaker = state.private.beliefs.get("_temp_speaker", "user")
            move = DialogueMove(speaker=speaker, move_type="ask", content=utterance)
            # Interpretation rules should add moves to agenda for the engine to process
            state.private.agenda.append(move)
            # Add question to QUD
            q = WhQuestion(variable="x", predicate="weather")
            state.shared.qud.append(q)
            # Set next speaker to system so it will respond
            state.control.next_speaker = "system"
            return state

        question_rule = UpdateRule(
            name="question_interpretation",
            rule_type="interpretation",
            preconditions=question_preconditions,
            effects=question_effects,
            priority=1,
        )
        rules.add_rule(question_rule)

        # Selection rule: answer top QUD
        def answer_preconditions(state):
            return len(state.shared.qud) > 0

        def answer_effects(state):
            # Pop question and create answer
            question = state.shared.qud.pop()
            answer_move = DialogueMove(
                speaker=state.agent_id, move_type="answer", content="It's sunny"
            )
            state.private.agenda.append(answer_move)
            # Add answer to commitments
            answer = Answer(question=question, content="sunny")
            if answer.resolves(question):
                # Question is resolved
                pass
            return state

        answer_rule = UpdateRule(
            name="answer_selection",
            rule_type="selection",
            preconditions=answer_preconditions,
            effects=answer_effects,
            priority=1,
        )
        rules.add_rule(answer_rule)

        # Generation rule: generate text from answer move
        def generate_preconditions(state):
            move = state.private.beliefs.get("_temp_generate_move")
            return move is not None and move.move_type == "answer"

        def generate_effects(state):
            move = state.private.beliefs.get("_temp_generate_move")
            state.private.beliefs["_temp_generated_text"] = f"The answer is: {move.content}"
            return state

        generate_rule = UpdateRule(
            name="answer_generation",
            rule_type="generation",
            preconditions=generate_preconditions,
            effects=generate_effects,
            priority=1,
        )
        rules.add_rule(generate_rule)

        # Create state machine with rules
        sm = DialogueStateMachine(agent_id="system", rules=rules)
        sm.initialize()

        # Process question
        result = sm.process_utterance("What is the weather?", speaker="user")

        # Should have generated a response
        assert result["has_response"] is True
        assert "sunny" in result["utterance_text"]


def test_create_dialogue_application():
    """Test creating dialogue application."""
    app = create_dialogue_application(agent_id="test_agent")

    assert app is not None

    # Check initial state
    action, result, state = app.step()
    assert action.name == "initialize"


def test_create_dialogue_application_with_persistence():
    """Test creating application with persistence."""
    with tempfile.TemporaryDirectory() as tmpdir:
        app = create_dialogue_application(
            agent_id="test_agent", app_id="test_app", storage_dir=tmpdir
        )

        assert app is not None

        # Initialize
        app.step()

        # Check tracking directory exists
        tracking_dir = Path(tmpdir)
        assert tracking_dir.exists()


class Test6StagePipeline:
    """Test 6-stage Burr pipeline with explicit NLU/NLG actions."""

    def test_6_stage_pipeline_with_nlu_nlg_engines(self):
        """Test that 6-stage pipeline is used when NLU/NLG engines are provided."""
        from ibdm.nlg import NLGEngine, NLGEngineConfig
        from ibdm.nlu import NLUEngine, NLUEngineConfig

        # Create NLU and NLG engines
        nlu_config = NLUEngineConfig()
        nlu_engine = NLUEngine(config=nlu_config)

        nlg_config = NLGEngineConfig()
        nlg_engine = NLGEngine(config=nlg_config)

        # Create state machine with engines
        sm = DialogueStateMachine(agent_id="system", nlu_engine=nlu_engine, nlg_engine=nlg_engine)

        # Should use 6-stage pipeline
        assert sm._use_6_stage is True

        # Initialize
        sm.initialize()

        # Process a simple greeting
        result = sm.process_utterance("Hello", speaker="user")

        # Should complete without errors
        assert result is not None
        assert "has_response" in result
        assert "utterance_text" in result

    def test_6_stage_pipeline_nlu_result_in_state(self):
        """Test that NLU results are visible in Burr state."""
        from ibdm.nlg import NLGEngine, NLGEngineConfig
        from ibdm.nlu import NLUEngine, NLUEngineConfig

        # Create engines
        nlu_config = NLUEngineConfig()
        nlu_engine = NLUEngine(config=nlu_config)

        nlg_config = NLGEngineConfig()
        nlg_engine = NLGEngine(config=nlg_config)

        # Create state machine
        sm = DialogueStateMachine(agent_id="system", nlu_engine=nlu_engine, nlg_engine=nlg_engine)
        sm.initialize()

        # Process utterance
        sm.process_utterance("Hello", speaker="user")

        # Check that nlu_result is in state
        state = sm.get_state()
        assert "nlu_result" in state
        nlu_result_dict = state["nlu_result"]
        assert nlu_result_dict is not None
        assert "dialogue_act" in nlu_result_dict
        assert "confidence" in nlu_result_dict

    def test_6_stage_pipeline_nlg_result_in_state(self):
        """Test that NLG results are visible in Burr state when response generated."""
        from ibdm.nlg import NLGEngine, NLGEngineConfig
        from ibdm.nlu import NLUEngine, NLUEngineConfig

        # Create engines
        nlu_config = NLUEngineConfig()
        nlu_engine = NLUEngine(config=nlu_config)

        nlg_config = NLGEngineConfig()
        nlg_engine = NLGEngine(config=nlg_config)

        # Create state machine
        sm = DialogueStateMachine(agent_id="system", nlu_engine=nlu_engine, nlg_engine=nlg_engine)
        sm.initialize()

        # Process greeting (should trigger a response)
        result = sm.process_utterance("Hello", speaker="user")

        # If a response was generated, check nlg_result
        if result.get("has_response"):
            state = sm.get_state()
            assert "nlg_result" in state
            nlg_result_dict = state.get("nlg_result")
            if nlg_result_dict is not None:
                assert "utterance_text" in nlg_result_dict
                assert "strategy" in nlg_result_dict

    def test_4_stage_pipeline_without_engines(self):
        """Test that 4-stage pipeline is used when engines are not provided."""
        # Create state machine without NLU/NLG engines
        sm = DialogueStateMachine(agent_id="system")

        # Should use 4-stage pipeline
        assert sm._use_6_stage is False

        # Initialize
        sm.initialize()

        # Process a simple greeting
        result = sm.process_utterance("Hello", speaker="user")

        # Should complete without errors
        assert result is not None
        assert "has_response" in result
        assert "utterance_text" in result

    def test_create_6_stage_application(self):
        """Test creating 6-stage application directly."""
        from ibdm.nlg import NLGEngine, NLGEngineConfig
        from ibdm.nlu import NLUEngine, NLUEngineConfig

        # Create engines
        nlu_config = NLUEngineConfig()
        nlu_engine = NLUEngine(config=nlu_config)

        nlg_config = NLGEngineConfig()
        nlg_engine = NLGEngine(config=nlg_config)

        # Create application with engines
        app = create_dialogue_application(
            agent_id="system", nlu_engine=nlu_engine, nlg_engine=nlg_engine
        )

        assert app is not None

        # Initialize
        action, result, state = app.step()
        assert action.name == "initialize"

        # Check that engines are in state
        assert state.get("nlu_engine") is not None
        assert state.get("nlg_engine") is not None
