"""Tests for Phase 3 rule implementations.

Tests interpretation, integration, selection, and generation rules.
"""


from ibdm.core import (
    AltQuestion,
    Answer,
    DialogueMove,
    InformationState,
    WhQuestion,
    YNQuestion,
)
from ibdm.rules import (
    RuleSet,
    create_generation_rules,
    create_integration_rules,
    create_interpretation_rules,
    create_selection_rules,
)


class TestInterpretationRules:
    """Test interpretation rule implementations."""

    def test_interpret_greeting(self):
        """Test greeting interpretation."""
        rules = create_interpretation_rules()
        ruleset = RuleSet()
        for rule in rules:
            ruleset.add_rule(rule)

        state = InformationState(agent_id="system")
        state.private.beliefs["_temp_utterance"] = "Hello there!"
        state.private.beliefs["_temp_speaker"] = "user"

        new_state = ruleset.apply_rules("interpretation", state)

        assert len(new_state.private.agenda) == 1
        move = new_state.private.agenda[0]
        assert move.move_type == "greet"
        assert move.speaker == "user"

    def test_interpret_wh_question(self):
        """Test wh-question interpretation."""
        rules = create_interpretation_rules()
        ruleset = RuleSet()
        for rule in rules:
            ruleset.add_rule(rule)

        state = InformationState(agent_id="system")
        state.private.beliefs["_temp_utterance"] = "What is the weather?"
        state.private.beliefs["_temp_speaker"] = "user"

        new_state = ruleset.apply_rules("interpretation", state)

        assert len(new_state.private.agenda) == 1
        move = new_state.private.agenda[0]
        assert move.move_type == "ask"
        assert isinstance(move.content, WhQuestion)
        assert move.content.constraints.get("wh_word") == "what"

    def test_interpret_yn_question(self):
        """Test yes/no question interpretation."""
        rules = create_interpretation_rules()
        ruleset = RuleSet()
        for rule in rules:
            ruleset.add_rule(rule)

        state = InformationState(agent_id="system")
        state.private.beliefs["_temp_utterance"] = "Is it raining?"
        state.private.beliefs["_temp_speaker"] = "user"

        new_state = ruleset.apply_rules("interpretation", state)

        assert len(new_state.private.agenda) == 1
        move = new_state.private.agenda[0]
        assert move.move_type == "ask"
        assert isinstance(move.content, YNQuestion)

    def test_interpret_alt_question(self):
        """Test alternative question interpretation."""
        rules = create_interpretation_rules()
        ruleset = RuleSet()
        for rule in rules:
            ruleset.add_rule(rule)

        state = InformationState(agent_id="system")
        state.private.beliefs["_temp_utterance"] = "Tea or coffee?"
        state.private.beliefs["_temp_speaker"] = "user"

        new_state = ruleset.apply_rules("interpretation", state)

        assert len(new_state.private.agenda) == 1
        move = new_state.private.agenda[0]
        assert move.move_type == "ask"
        assert isinstance(move.content, AltQuestion)
        assert len(move.content.alternatives) == 2

    def test_interpret_yn_answer(self):
        """Test yes/no answer interpretation."""
        rules = create_interpretation_rules()
        ruleset = RuleSet()
        for rule in rules:
            ruleset.add_rule(rule)

        state = InformationState(agent_id="system")
        state.private.beliefs["_temp_utterance"] = "yes"
        state.private.beliefs["_temp_speaker"] = "user"
        # Add a question to QUD
        state.shared.push_qud(YNQuestion(proposition="is_raining"))

        new_state = ruleset.apply_rules("interpretation", state)

        assert len(new_state.private.agenda) == 1
        move = new_state.private.agenda[0]
        assert move.move_type == "answer"
        assert isinstance(move.content, Answer)
        assert move.content.content is True


class TestIntegrationRules:
    """Test integration rule implementations."""

    def test_integrate_question(self):
        """Test question integration pushes to QUD."""
        rules = create_integration_rules()
        ruleset = RuleSet()
        for rule in rules:
            ruleset.add_rule(rule)

        state = InformationState(agent_id="system")
        question = WhQuestion(variable="x", predicate="weather")
        move = DialogueMove(move_type="ask", content=question, speaker="user")
        state.private.beliefs["_temp_move"] = move

        new_state = ruleset.apply_rules("integration", state)

        assert len(new_state.shared.qud) == 1
        assert new_state.shared.qud[0] == question
        assert new_state.control.next_speaker == "system"

    def test_integrate_answer_resolves_qud(self):
        """Test answer integration resolves QUD."""
        rules = create_integration_rules()
        ruleset = RuleSet()
        for rule in rules:
            ruleset.add_rule(rule)

        state = InformationState(agent_id="system")
        question = YNQuestion(proposition="is_raining")
        state.shared.push_qud(question)

        answer = Answer(content=True, question_ref=question)
        move = DialogueMove(move_type="answer", content=answer, speaker="user")
        state.private.beliefs["_temp_move"] = move

        new_state = ruleset.apply_rules("integration", state)

        assert len(new_state.shared.qud) == 0  # QUD should be popped
        assert len(new_state.shared.commitments) > 0

    def test_integrate_greet_adds_response(self):
        """Test greeting integration adds response to agenda."""
        rules = create_integration_rules()
        ruleset = RuleSet()
        for rule in rules:
            ruleset.add_rule(rule)

        state = InformationState(agent_id="system")
        move = DialogueMove(move_type="greet", content="Hello", speaker="user")
        state.private.beliefs["_temp_move"] = move

        new_state = ruleset.apply_rules("integration", state)

        assert new_state.control.dialogue_state == "active"
        assert new_state.control.next_speaker == "system"
        assert len(new_state.private.agenda) == 1  # Greeting response added

    def test_integrate_quit_ends_dialogue(self):
        """Test quit integration ends dialogue."""
        rules = create_integration_rules()
        ruleset = RuleSet()
        for rule in rules:
            ruleset.add_rule(rule)

        state = InformationState(agent_id="system")
        move = DialogueMove(move_type="quit", content="Goodbye", speaker="user")
        state.private.beliefs["_temp_move"] = move

        new_state = ruleset.apply_rules("integration", state)

        assert new_state.control.dialogue_state == "ended"


class TestSelectionRules:
    """Test selection rule implementations."""

    def test_select_answer_qud(self):
        """Test selection answers QUD when knowledge available."""
        rules = create_selection_rules()
        ruleset = RuleSet()
        for rule in rules:
            ruleset.add_rule(rule)

        state = InformationState(agent_id="system")
        question = WhQuestion(variable="x", predicate="weather")
        state.shared.push_qud(question)
        state.private.beliefs["weather"] = "sunny"

        new_state, matched_rule = ruleset.apply_first_matching("selection", state)

        assert matched_rule is not None
        assert len(new_state.private.agenda) == 1
        move = new_state.private.agenda[0]
        assert move.move_type == "answer"

    def test_select_generic_response(self):
        """Test generic response is selected when nothing else applies."""
        rules = create_selection_rules()
        ruleset = RuleSet()
        for rule in rules:
            ruleset.add_rule(rule)

        state = InformationState(agent_id="system")
        state.control.dialogue_state = "active"

        new_state, matched_rule = ruleset.apply_first_matching("selection", state)

        assert matched_rule is not None
        # At least one rule should match (generic response at minimum)


class TestGenerationRules:
    """Test generation rule implementations."""

    def test_generate_greeting(self):
        """Test greeting generation."""
        rules = create_generation_rules()
        ruleset = RuleSet()
        for rule in rules:
            ruleset.add_rule(rule)

        state = InformationState(agent_id="system")
        move = DialogueMove(move_type="greet", content="greeting_response", speaker="system")
        state.private.beliefs["_temp_generate_move"] = move

        new_state = ruleset.apply_rules("generation", state)

        text = new_state.private.beliefs.get("_temp_generated_text", "")
        assert "hello" in text.lower()

    def test_generate_wh_question(self):
        """Test wh-question generation."""
        rules = create_generation_rules()
        ruleset = RuleSet()
        for rule in rules:
            ruleset.add_rule(rule)

        state = InformationState(agent_id="system")
        question = WhQuestion(variable="x", predicate="weather", constraints={"wh_word": "what"})
        move = DialogueMove(move_type="ask", content=question, speaker="system")
        state.private.beliefs["_temp_generate_move"] = move

        new_state = ruleset.apply_rules("generation", state)

        text = new_state.private.beliefs.get("_temp_generated_text", "")
        assert text.endswith("?")
        assert "what" in text.lower()

    def test_generate_yn_answer(self):
        """Test yes/no answer generation."""
        rules = create_generation_rules()
        ruleset = RuleSet()
        for rule in rules:
            ruleset.add_rule(rule)

        state = InformationState(agent_id="system")
        answer = Answer(content=True)
        move = DialogueMove(move_type="answer", content=answer, speaker="system")
        state.private.beliefs["_temp_generate_move"] = move

        new_state = ruleset.apply_rules("generation", state)

        text = new_state.private.beliefs.get("_temp_generated_text", "")
        assert "yes" in text.lower()

    def test_generate_answer_text(self):
        """Test answer text generation."""
        rules = create_generation_rules()
        ruleset = RuleSet()
        for rule in rules:
            ruleset.add_rule(rule)

        state = InformationState(agent_id="system")
        answer = Answer(content="It is sunny")
        move = DialogueMove(move_type="answer", content=answer, speaker="system")
        state.private.beliefs["_temp_generate_move"] = move

        new_state = ruleset.apply_rules("generation", state)

        text = new_state.private.beliefs.get("_temp_generated_text", "")
        assert "sunny" in text.lower()


class TestEndToEndRuleIntegration:
    """Test end-to-end rule integration."""

    def test_question_answer_flow(self):
        """Test complete question-answer flow through all rule types."""
        # Create rulesets
        interp_rules = create_interpretation_rules()
        integ_rules = create_integration_rules()
        select_rules = create_selection_rules()
        gen_rules = create_generation_rules()

        ruleset = RuleSet()
        for rule in interp_rules + integ_rules + select_rules + gen_rules:
            ruleset.add_rule(rule)

        # Start with interpretation
        state = InformationState(agent_id="system")
        state.private.beliefs["_temp_utterance"] = "What is the weather?"
        state.private.beliefs["_temp_speaker"] = "user"

        # 1. Interpret
        state = ruleset.apply_rules("interpretation", state)
        assert len(state.private.agenda) == 1

        # Get the interpreted move
        move = state.private.agenda.pop(0)
        assert move.move_type == "ask"

        # 2. Integrate
        state.private.beliefs["_temp_move"] = move
        state = ruleset.apply_rules("integration", state)
        assert len(state.shared.qud) == 1

        # 3. Selection (add knowledge first)
        state.private.beliefs["weather"] = "sunny"
        state, _ = ruleset.apply_first_matching("selection", state)

        # Should have an answer on the agenda
        if state.private.agenda:
            response_move = state.private.agenda.pop(0)

            # 4. Generation
            state.private.beliefs["_temp_generate_move"] = response_move
            state = ruleset.apply_rules("generation", state)

            text = state.private.beliefs.get("_temp_generated_text", "")
            assert len(text) > 0
