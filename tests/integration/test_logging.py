"""Integration test for logging functionality.

Tests that logging works correctly across the dialogue engine.
"""

import logging
import os

import pytest

from ibdm.config import configure_logging, get_debug_info
from ibdm.core import DialogueMove, InformationState, WhQuestion
from ibdm.engine import DialogueMoveEngine
from ibdm.rules import RuleSet, UpdateRule


@pytest.fixture
def engine():
    """Create a dialogue engine with simple test rules."""
    rules = RuleSet()

    # Simple interpretation rule: map "hello" to greet move
    rules.add_rule(
        UpdateRule(
            name="interpret_greeting",
            preconditions=lambda s: s.private.beliefs.get("_temp_utterance") == "hello",
            effects=lambda s: _add_greet_to_agenda(s),
            priority=10,
            rule_type="interpretation",
        )
    )

    # Simple integration rule: integrate greet move
    rules.add_rule(
        UpdateRule(
            name="integrate_greet",
            preconditions=lambda s: (
                isinstance(s.private.beliefs.get("_temp_move"), DialogueMove)
                and s.private.beliefs["_temp_move"].move_type == "greet"
            ),
            effects=lambda s: s,  # No state change
            priority=10,
            rule_type="integration",
        )
    )

    return DialogueMoveEngine(agent_id="test", rules=rules)


def _add_greet_to_agenda(state: InformationState) -> InformationState:
    """Helper to add greet move to agenda."""
    new_state = state.clone()
    move = DialogueMove(
        move_type="greet",
        content="greeting",
        speaker=new_state.private.beliefs.get("_temp_speaker", "user"),
    )
    new_state.private.agenda.append(move)
    return new_state


def test_logging_captures_dialogue_flow(engine, caplog):
    """Test that logging captures the dialogue flow."""
    with caplog.at_level(logging.DEBUG, logger="ibdm"):
        state = InformationState(agent_id="test")
        engine.process_input("hello", "user", state)

        # Should have log messages from dialogue phases
        log_text = "\n".join([rec.message for rec in caplog.records])
        assert "Processing input from user" in log_text, "Expected input processing log"


def test_logging_enabled_with_debug_all(engine, caplog):
    """Test that logging is enabled with IBDM_DEBUG=all."""
    # Set debug flag
    os.environ["IBDM_DEBUG"] = "all"

    # Reconfigure logging
    configure_logging()

    with caplog.at_level(logging.DEBUG, logger="ibdm"):
        state = InformationState(agent_id="test")
        engine.process_input("hello", "user", state)

        # Should have DEBUG messages
        debug_messages = [rec for rec in caplog.records if rec.levelno == logging.DEBUG]
        assert len(debug_messages) > 0, "Expected DEBUG messages with IBDM_DEBUG=all"

        # Check for expected log messages
        log_text = "\n".join([rec.message for rec in caplog.records])
        assert "[INTERPRET]" in log_text, "Expected INTERPRET phase logging"
        assert "[INTEGRATE]" in log_text, "Expected INTEGRATE phase logging"


def test_logging_rules_category(engine, caplog):
    """Test that IBDM_DEBUG=rules enables rule logging."""
    # Set debug flag
    os.environ["IBDM_DEBUG"] = "rules"

    # Reconfigure logging
    configure_logging()

    with caplog.at_level(logging.DEBUG, logger="ibdm"):
        state = InformationState(agent_id="test")
        engine.process_input("hello", "user", state)

        # Should have rule evaluation messages
        log_text = "\n".join([rec.message for rec in caplog.records])
        assert "interpretation rules" in log_text, "Expected rule evaluation logging"


def test_logging_qud_operations(caplog):
    """Test that QUD operations are logged."""
    # Set debug flag
    os.environ["IBDM_DEBUG"] = "qud"

    # Reconfigure logging
    configure_logging()

    with caplog.at_level(logging.DEBUG, logger="ibdm"):
        state = InformationState(agent_id="test")
        question = WhQuestion(variable="x", predicate="test")

        # Push and pop QUD
        state.shared.push_qud(question)
        state.shared.pop_qud()

        # Should have QUD operation messages
        log_text = "\n".join([rec.message for rec in caplog.records])
        assert "QUD PUSH" in log_text, "Expected QUD PUSH logging"
        assert "QUD POP" in log_text, "Expected QUD POP logging"


def test_get_debug_info():
    """Test debug info reporting."""
    os.environ["IBDM_DEBUG"] = "rules,qud"

    # Need to reload the module to pick up new env var
    import importlib

    from ibdm import config

    importlib.reload(config.debug_config)

    info = get_debug_info()

    assert info["enabled"] is True
    assert "rules" in info["flags"]
    assert "qud" in info["flags"]
    assert info["categories"]["rules"] is True
    assert info["categories"]["qud"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
