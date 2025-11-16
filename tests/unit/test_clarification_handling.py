"""Test clarification handling for invalid answers."""

from ibdm.core import Answer, DialogueMove, InformationState, WhQuestion
from ibdm.rules import (
    RuleSet,
    create_generation_rules,
    create_integration_rules,
    create_selection_rules,
)


def test_invalid_answer_triggers_clarification():
    """Test that an invalid answer (empty value) triggers clarification request."""
    # Setup
    state = InformationState(agent_id="system")

    # Create a question asking for parties (legal_entities)
    question = WhQuestion(variable="x", predicate="legal_entities")
    state.shared.push_qud(question)

    # Create an invalid answer (empty string fails type checking)
    invalid_answer = Answer(content="", question_ref=question)
    move = DialogueMove(move_type="answer", content=invalid_answer, speaker="user")

    # Store move for integration
    state.private.beliefs["_temp_move"] = move

    # Apply integration rules
    rules = create_integration_rules()
    ruleset = RuleSet()
    for rule in rules:
        ruleset.add_rule(rule)

    new_state = ruleset.apply_rules("integration", state)

    # Verify: Question should still be on QUD (not popped)
    assert len(new_state.shared.qud) == 1
    assert new_state.shared.top_qud() == question

    # Verify: Clarification marker should be set
    assert new_state.private.beliefs.get("_needs_clarification") is True
    assert new_state.private.beliefs.get("_invalid_answer") == ""
    assert new_state.private.beliefs.get("_clarification_question") == question


def test_selection_creates_clarification_move():
    """Test that selection phase creates an ICM clarification move."""
    # Setup
    state = InformationState(agent_id="system")
    question = WhQuestion(variable="x", predicate="legal_entities")

    # Mark that clarification is needed
    state.private.beliefs["_needs_clarification"] = True
    state.private.beliefs["_invalid_answer"] = ""
    state.private.beliefs["_clarification_question"] = question
    state.shared.push_qud(question)

    # Apply selection rules
    rules = create_selection_rules()
    ruleset = RuleSet()
    for rule in rules:
        ruleset.add_rule(rule)

    new_state = ruleset.apply_rules("selection", state)

    # Verify: ICM clarification move should be on agenda (might have fallback too)
    assert len(new_state.private.agenda) >= 1

    # Find the ICM clarification move (should be first due to priority)
    icm_moves = [m for m in new_state.private.agenda if m.move_type == "icm"]
    assert len(icm_moves) == 1

    move = icm_moves[0]
    assert isinstance(move.content, dict)
    assert move.content["icm_type"] == "clarify"
    assert move.content["question"] == question
    assert "valid response" in move.content["message"]

    # Verify: Clarification markers should be cleared
    assert new_state.private.beliefs.get("_needs_clarification") is False


def test_generation_creates_clarification_text():
    """Test that generation phase creates clarification message."""
    # Setup
    state = InformationState(agent_id="system")
    question = WhQuestion(variable="x", predicate="legal_entities")

    # Create ICM clarification move
    clarification_content = {
        "icm_type": "clarify",
        "question": question,
        "invalid_answer": "",
        "message": "I didn't understand that answer. Could you please provide a valid response?",
    }
    move = DialogueMove(
        move_type="icm",
        content=clarification_content,
        speaker="system",
        metadata={"icm_subtype": "clarify"},
    )

    state.private.beliefs["_temp_generate_move"] = move

    # Apply generation rules
    rules = create_generation_rules()
    ruleset = RuleSet()
    for rule in rules:
        ruleset.add_rule(rule)

    new_state = ruleset.apply_rules("generation", state)

    # Verify: Generated text should be the clarification message
    assert "_temp_generated_text" in new_state.private.beliefs
    text = new_state.private.beliefs["_temp_generated_text"]
    assert "didn't understand" in text or "valid response" in text


def test_valid_answer_does_not_trigger_clarification():
    """Test that a valid answer does NOT trigger clarification."""
    # Setup
    state = InformationState(agent_id="system")

    # Create a question asking for parties
    question = WhQuestion(variable="x", predicate="legal_entities")
    state.shared.push_qud(question)

    # Create a VALID answer (non-empty parties)
    valid_answer = Answer(content="Acme Corp, Beta Inc", question_ref=question)
    move = DialogueMove(move_type="answer", content=valid_answer, speaker="user")

    # Store move for integration
    state.private.beliefs["_temp_move"] = move

    # Apply integration rules
    rules = create_integration_rules()
    ruleset = RuleSet()
    for rule in rules:
        ruleset.add_rule(rule)

    new_state = ruleset.apply_rules("integration", state)

    # Verify: Question should be popped (resolved)
    assert len(new_state.shared.qud) == 0

    # Verify: Clarification marker should NOT be set
    assert new_state.private.beliefs.get("_needs_clarification") is not True

    # Verify: Commitment should be added
    assert len(new_state.shared.commitments) == 1
