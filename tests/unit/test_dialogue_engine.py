"""Unit tests for DialogueMoveEngine class."""

from ibdm.core import Answer, DialogueMove, InformationState, WhQuestion
from ibdm.engine import DialogueMoveEngine
from ibdm.rules import RuleSet, UpdateRule


class TestDialogueMoveEngine:
    """Tests for DialogueMoveEngine class."""

    def test_creation(self):
        """Test creating a DialogueMoveEngine."""
        engine = DialogueMoveEngine(agent_id="test_agent")
        assert engine.agent_id == "test_agent"
        assert isinstance(engine.rules, RuleSet)
        assert isinstance(engine.state, InformationState)
        assert engine.state.agent_id == "test_agent"

    def test_creation_with_rules(self):
        """Test creating a DialogueMoveEngine with custom rules."""
        rules = RuleSet()
        engine = DialogueMoveEngine(agent_id="test_agent", rules=rules)
        assert engine.rules is rules

    def test_reset(self):
        """Test resetting the engine state."""
        engine = DialogueMoveEngine(agent_id="test_agent")

        # Modify state
        q = WhQuestion(variable="x", predicate="test(x)")
        engine.state.shared.push_qud(q)
        assert len(engine.state.shared.qud) == 1

        # Reset
        engine.reset()
        assert len(engine.state.shared.qud) == 0

    def test_get_state(self):
        """Test getting the current state."""
        engine = DialogueMoveEngine(agent_id="test_agent")
        state = engine.get_state()
        assert state is engine.state

    def test_set_state(self):
        """Test setting a new state."""
        engine = DialogueMoveEngine(agent_id="test_agent")
        new_state = InformationState(agent_id="test_agent")
        new_state.private.beliefs["test"] = "value"

        engine.set_state(new_state)
        assert engine.state is new_state
        assert engine.state.private.beliefs["test"] == "value"

    def test_interpret_no_rules(self):
        """Test interpret with no interpretation rules."""
        engine = DialogueMoveEngine(agent_id="test_agent")
        moves = engine.interpret("Hello", "user")
        assert moves == []

    def test_interpret_with_rule(self):
        """Test interpret with an interpretation rule."""

        def precond(state: InformationState) -> bool:
            return "_temp_utterance" in state.private.beliefs

        def effect(state: InformationState) -> InformationState:
            new_state = state.clone()
            utterance = new_state.private.beliefs.get("_temp_utterance", "")
            speaker = new_state.private.beliefs.get("_temp_speaker", "")

            if "hello" in utterance.lower():
                move = DialogueMove(move_type="greet", content=utterance, speaker=speaker)
                new_state.private.agenda.append(move)

            return new_state

        rules = RuleSet()
        rule = UpdateRule(
            name="interpret_greeting",
            preconditions=precond,
            effects=effect,
            rule_type="interpretation",
        )
        rules.add_rule(rule)

        engine = DialogueMoveEngine(agent_id="test_agent", rules=rules)
        moves = engine.interpret("Hello there", "user")

        assert len(moves) == 1
        assert moves[0].move_type == "greet"
        assert moves[0].speaker == "user"

    def test_integrate_no_rules(self):
        """Test integrate with no integration rules."""
        engine = DialogueMoveEngine(agent_id="test_agent")
        move = DialogueMove(move_type="greet", content="Hello", speaker="user")

        original_state = engine.state.clone()
        new_state = engine.integrate(move)

        # State should be unchanged if no rules
        assert len(new_state.shared.qud) == len(original_state.shared.qud)

    def test_integrate_with_rule(self):
        """Test integrate with an integration rule."""

        def precond(state: InformationState) -> bool:
            move = state.private.beliefs.get("_temp_move")
            return move is not None and move.move_type == "ask"

        def effect(state: InformationState) -> InformationState:
            new_state = state.clone()
            move = new_state.private.beliefs.get("_temp_move")

            if isinstance(move.content, WhQuestion):
                new_state.shared.push_qud(move.content)

            return new_state

        rules = RuleSet()
        rule = UpdateRule(
            name="integrate_ask", preconditions=precond, effects=effect, rule_type="integration"
        )
        rules.add_rule(rule)

        engine = DialogueMoveEngine(agent_id="test_agent", rules=rules)

        q = WhQuestion(variable="x", predicate="weather(x)")
        move = DialogueMove(move_type="ask", content=q, speaker="user")

        assert len(engine.state.shared.qud) == 0
        engine.state = engine.integrate(move)
        assert len(engine.state.shared.qud) == 1
        assert engine.state.shared.qud[0] == q

    def test_select_action_from_agenda(self):
        """Test selecting action from agenda."""
        engine = DialogueMoveEngine(agent_id="test_agent")

        # Add move to agenda
        move = DialogueMove(move_type="greet", content="Hello", speaker="test_agent")
        engine.state.private.agenda.append(move)

        selected = engine.select_action()
        assert selected is move
        assert len(engine.state.private.agenda) == 0

    def test_select_action_no_rules(self):
        """Test selecting action with no selection rules."""
        engine = DialogueMoveEngine(agent_id="test_agent")
        selected = engine.select_action()
        assert selected is None

    def test_select_action_with_rule(self):
        """Test selecting action with a selection rule."""

        def precond(state: InformationState) -> bool:
            return len(state.shared.qud) > 0

        def effect(state: InformationState) -> InformationState:
            new_state = state.clone()
            # Create response move and add to agenda
            move = DialogueMove(
                move_type="answer",
                content=Answer(content="Response"),
                speaker=new_state.agent_id,
            )
            new_state.private.agenda.append(move)
            return new_state

        rules = RuleSet()
        rule = UpdateRule(
            name="select_response",
            preconditions=precond,
            effects=effect,
            rule_type="selection",
        )
        rules.add_rule(rule)

        engine = DialogueMoveEngine(agent_id="test_agent", rules=rules)

        # Add question to QUD
        q = WhQuestion(variable="x", predicate="weather(x)")
        engine.state.shared.push_qud(q)

        selected = engine.select_action()
        assert selected is not None
        assert selected.move_type == "answer"

    def test_generate_no_rules(self):
        """Test generate with no generation rules uses defaults."""
        engine = DialogueMoveEngine(agent_id="test_agent")

        move = DialogueMove(move_type="greet", content="", speaker="test_agent")
        text = engine.generate(move)

        assert text == "Hello!"

    def test_generate_with_rule(self):
        """Test generate with a generation rule."""

        def precond(state: InformationState) -> bool:
            move = state.private.beliefs.get("_temp_generate_move")
            return move is not None and move.move_type == "answer"

        def effect(state: InformationState) -> InformationState:
            new_state = state.clone()
            move = new_state.private.beliefs.get("_temp_generate_move")

            if isinstance(move.content, Answer):
                new_state.private.beliefs["_temp_generated_text"] = (
                    f"The answer is: {move.content.content}"
                )

            return new_state

        rules = RuleSet()
        rule = UpdateRule(
            name="generate_answer",
            preconditions=precond,
            effects=effect,
            rule_type="generation",
        )
        rules.add_rule(rule)

        engine = DialogueMoveEngine(agent_id="test_agent", rules=rules)

        move = DialogueMove(
            move_type="answer", content=Answer(content="sunny"), speaker="test_agent"
        )
        text = engine.generate(move)

        assert text == "The answer is: sunny"

    def test_default_generation_types(self):
        """Test default generation for different move types."""
        engine = DialogueMoveEngine(agent_id="test_agent")

        greet_move = DialogueMove(move_type="greet", content="", speaker="test_agent")
        assert engine.generate(greet_move) == "Hello!"

        quit_move = DialogueMove(move_type="quit", content="", speaker="test_agent")
        assert engine.generate(quit_move) == "Goodbye!"

        q = WhQuestion(variable="x", predicate="weather(x)")
        ask_move = DialogueMove(move_type="ask", content=q, speaker="test_agent")
        assert "Question:" in engine.generate(ask_move)

        answer_move = DialogueMove(
            move_type="answer", content=Answer(content="sunny"), speaker="test_agent"
        )
        assert "Answer:" in engine.generate(answer_move)

    def test_process_input_simple(self):
        """Test processing input with no rules."""
        engine = DialogueMoveEngine(agent_id="test_agent")
        state, response = engine.process_input("Hello", "user")

        assert state is not None
        # No response expected without rules
        assert response is None

    def test_process_input_with_interpretation_and_integration(self):
        """Test processing input with interpretation and integration rules."""

        def interp_precond(state: InformationState) -> bool:
            return "_temp_utterance" in state.private.beliefs

        def interp_effect(state: InformationState) -> InformationState:
            new_state = state.clone()
            utterance = new_state.private.beliefs.get("_temp_utterance", "")
            speaker = new_state.private.beliefs.get("_temp_speaker", "")

            if "weather" in utterance.lower():
                q = WhQuestion(variable="x", predicate="weather(x)")
                move = DialogueMove(move_type="ask", content=q, speaker=speaker)
                new_state.private.agenda.append(move)

            return new_state

        def integ_precond(state: InformationState) -> bool:
            move = state.private.beliefs.get("_temp_move")
            return move is not None and move.move_type == "ask"

        def integ_effect(state: InformationState) -> InformationState:
            new_state = state.clone()
            move = new_state.private.beliefs.get("_temp_move")

            if isinstance(move.content, WhQuestion):
                new_state.shared.push_qud(move.content)
                # Switch turn to system
                new_state.control.next_speaker = "test_agent"

            return new_state

        rules = RuleSet()
        rules.add_rule(
            UpdateRule(
                name="interp",
                preconditions=interp_precond,
                effects=interp_effect,
                rule_type="interpretation",
            )
        )
        rules.add_rule(
            UpdateRule(
                name="integ",
                preconditions=integ_precond,
                effects=integ_effect,
                rule_type="integration",
            )
        )

        engine = DialogueMoveEngine(agent_id="test_agent", rules=rules)
        state, response = engine.process_input("What's the weather?", "user")

        # Question should be on QUD
        assert len(state.shared.qud) == 1
        assert isinstance(state.shared.qud[0], WhQuestion)

    def test_process_input_full_cycle(self):
        """Test full processing cycle with all rule types."""

        # Interpretation: recognize "what's X" as ask(WhQuestion)
        def interp_precond(state: InformationState) -> bool:
            return "_temp_utterance" in state.private.beliefs

        def interp_effect(state: InformationState) -> InformationState:
            new_state = state.clone()
            utterance = new_state.private.beliefs.get("_temp_utterance", "")
            speaker = new_state.private.beliefs.get("_temp_speaker", "")

            if "what" in utterance.lower():
                q = WhQuestion(variable="x", predicate="test(x)")
                move = DialogueMove(move_type="ask", content=q, speaker=speaker)
                new_state.private.agenda.append(move)

            return new_state

        # Integration: push question to QUD and switch turn
        def integ_precond(state: InformationState) -> bool:
            move = state.private.beliefs.get("_temp_move")
            return move is not None and move.move_type == "ask"

        def integ_effect(state: InformationState) -> InformationState:
            new_state = state.clone()
            move = new_state.private.beliefs.get("_temp_move")

            if isinstance(move.content, WhQuestion):
                new_state.shared.push_qud(move.content)
                new_state.control.next_speaker = "test_agent"

            return new_state

        # Selection: respond to QUD
        def select_precond(state: InformationState) -> bool:
            return len(state.shared.qud) > 0

        def select_effect(state: InformationState) -> InformationState:
            new_state = state.clone()
            move = DialogueMove(
                move_type="answer",
                content=Answer(content="test_value"),
                speaker=new_state.agent_id,
            )
            new_state.private.agenda.append(move)
            return new_state

        # Generation: format answer
        def gen_precond(state: InformationState) -> bool:
            move = state.private.beliefs.get("_temp_generate_move")
            return move is not None and move.move_type == "answer"

        def gen_effect(state: InformationState) -> InformationState:
            new_state = state.clone()
            move = new_state.private.beliefs.get("_temp_generate_move")
            if isinstance(move.content, Answer):
                new_state.private.beliefs["_temp_generated_text"] = f"It is {move.content.content}"
            return new_state

        rules = RuleSet()
        rules.add_rule(
            UpdateRule(
                name="interp",
                preconditions=interp_precond,
                effects=interp_effect,
                rule_type="interpretation",
            )
        )
        rules.add_rule(
            UpdateRule(
                name="integ",
                preconditions=integ_precond,
                effects=integ_effect,
                rule_type="integration",
            )
        )
        rules.add_rule(
            UpdateRule(
                name="select",
                preconditions=select_precond,
                effects=select_effect,
                rule_type="selection",
            )
        )
        rules.add_rule(
            UpdateRule(
                name="gen",
                preconditions=gen_precond,
                effects=gen_effect,
                rule_type="generation",
            )
        )

        engine = DialogueMoveEngine(agent_id="test_agent", rules=rules)
        state, response = engine.process_input("What is it?", "user")

        # Should have interpreted, integrated, selected, and generated
        assert len(state.shared.qud) == 1
        assert response is not None
        assert response.move_type == "answer"
        assert response.content == "It is test_value"

    def test_str_representation(self):
        """Test string representation."""
        engine = DialogueMoveEngine(agent_id="my_agent")
        s = str(engine)
        assert "my_agent" in s
        assert "DialogueMoveEngine" in s
