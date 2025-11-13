"""Integration tests for hybrid fallback strategy with NLU engine.

These tests verify that the hybrid fallback system works end-to-end:
- Model switching between Haiku and Sonnet
- Token counting from LLM responses
- Latency measurement
- Cascading fallback logic
- Integration with NLUDialogueEngine
"""

import pytest

from ibdm.engine.nlu_engine import NLUDialogueEngine, NLUEngineConfig
from ibdm.nlu.fallback_strategy import FallbackConfig, InterpretationStrategy


class TestHybridFallbackIntegration:
    """Integration tests for hybrid fallback with NLU engine."""

    @pytest.fixture
    def engine_with_fallback(self):
        """Create NLU engine with hybrid fallback enabled."""
        fallback_config = FallbackConfig(
            enable_cascading=True,
            max_tokens_per_session=50000,
            latency_budget=30.0,
        )
        config = NLUEngineConfig(
            use_nlu=True,
            use_llm=True,
            enable_hybrid_fallback=True,
            fallback_config=fallback_config,
        )
        return NLUDialogueEngine("test_agent", config=config)

    def test_engine_creates_separate_interpreters(self, engine_with_fallback):
        """Test that engine creates separate Haiku and Sonnet interpreters."""
        assert engine_with_fallback.haiku_interpreter is not None
        assert engine_with_fallback.sonnet_interpreter is not None
        assert engine_with_fallback.context_interpreter is not None

        # Verify they use different models
        assert (
            engine_with_fallback.haiku_interpreter.llm.config.model.value
            == "claude-haiku-4-5-20251001"
        )
        assert (
            engine_with_fallback.sonnet_interpreter.llm.config.model.value
            == "claude-sonnet-4-5-20250929"
        )

    def test_simple_utterance_uses_rules(self, engine_with_fallback):
        """Test that simple utterances use rule-based interpretation."""
        # Reset stats first
        engine_with_fallback.reset_fallback_session()

        # Simple greeting should use fast-path/rules
        state = engine_with_fallback.create_initial_state()
        engine_with_fallback.interpret("hello", "user", state)

        stats_after = engine_with_fallback.get_fallback_stats()

        # Rules should have been used at least once
        assert stats_after.rules_count >= 1
        # Fast-path hits should be recorded
        assert stats_after.fast_path_hits >= 1

    @pytest.mark.skipif(
        True,  # Skip by default to avoid API calls in CI
        reason="Requires API key and makes actual LLM calls",
    )
    def test_moderate_complexity_uses_haiku(self, engine_with_fallback):
        """Test that moderate complexity utterances use Haiku model."""
        # Reset stats
        engine_with_fallback.reset_fallback_session()

        # Moderate complexity utterance
        utterance = "What is the capital of France?"
        engine_with_fallback.interpret(utterance, "user")

        stats = engine_with_fallback.get_fallback_stats()

        # Haiku should be used
        assert stats.haiku_count > 0
        # Sonnet should not be used (unless cascading occurred)
        # Token usage should be tracked
        assert stats.tokens_used > 0
        # Latency should be tracked
        assert stats.total_latency > 0.0

    @pytest.mark.skipif(
        True,  # Skip by default to avoid API calls in CI
        reason="Requires API key and makes actual LLM calls",
    )
    def test_complex_utterance_uses_sonnet(self, engine_with_fallback):
        """Test that complex utterances use Sonnet model."""
        # Reset stats
        engine_with_fallback.reset_fallback_session()

        # Complex utterance with multiple clauses
        utterance = (
            "If the weather is nice tomorrow and John can make it, "
            "should we reschedule the meeting that was planned for next week, "
            "or would it be better to stick with the original plan?"
        )
        engine_with_fallback.interpret(utterance, "user")

        stats = engine_with_fallback.get_fallback_stats()

        # Sonnet should be used for complex utterance
        assert stats.sonnet_count > 0
        # Token usage should be tracked
        assert stats.tokens_used > 0
        # Latency should be tracked
        assert stats.total_latency > 0.0

    def test_token_tracking_initialized(self, engine_with_fallback):
        """Test that token tracking fields are initialized."""
        assert hasattr(engine_with_fallback, "last_interpretation_tokens")
        assert hasattr(engine_with_fallback, "last_interpretation_latency")
        assert engine_with_fallback.last_interpretation_tokens == 0
        assert engine_with_fallback.last_interpretation_latency == 0.0

    def test_latency_measurement_for_rules(self, engine_with_fallback):
        """Test that latency is measured even for rule-based interpretation."""
        # Simple utterance using rules
        state = engine_with_fallback.create_initial_state()
        engine_with_fallback.interpret("yes", "user", state)

        # Latency should be measured (even if very small)
        stats = engine_with_fallback.get_fallback_stats()
        assert stats.total_latency >= 0.0

    def test_fallback_stats_accessible(self, engine_with_fallback):
        """Test that fallback stats are accessible via engine."""
        stats = engine_with_fallback.get_fallback_stats()

        assert hasattr(stats, "rules_count")
        assert hasattr(stats, "haiku_count")
        assert hasattr(stats, "sonnet_count")
        assert hasattr(stats, "tokens_used")
        assert hasattr(stats, "total_latency")
        assert hasattr(stats, "fast_path_hits")

    def test_reset_session_clears_stats(self, engine_with_fallback):
        """Test that reset_session_stats clears statistics."""
        # Reset first to ensure clean state
        engine_with_fallback.reset_fallback_session()

        # Interpret something to generate stats
        state = engine_with_fallback.create_initial_state()
        engine_with_fallback.interpret("hello", "user", state)

        stats_before = engine_with_fallback.get_fallback_stats()
        # Verify we have some stats
        total_before = (
            stats_before.rules_count + stats_before.haiku_count + stats_before.sonnet_count
        )
        assert total_before > 0

        # Reset
        engine_with_fallback.reset_fallback_session()

        stats_after = engine_with_fallback.get_fallback_stats()
        # All counts should be zero after reset
        assert stats_after.rules_count == 0
        assert stats_after.haiku_count == 0
        assert stats_after.sonnet_count == 0
        assert stats_after.tokens_used == 0
        assert stats_after.total_latency == 0.0
        assert stats_after.total_utterances == 0

    @pytest.mark.skipif(
        True,  # Skip by default to avoid API calls in CI
        reason="Requires API key and makes actual LLM calls",
    )
    def test_cascading_fallback(self, engine_with_fallback):
        """Test that cascading works when confidence is low."""
        # An ambiguous or complex utterance that might trigger cascading
        utterance = "That's interesting, but what about the other thing?"

        engine_with_fallback.interpret(utterance, "user")

        stats = engine_with_fallback.get_fallback_stats()

        # At least one strategy should have been used
        total_attempts = stats.rules_count + stats.haiku_count + stats.sonnet_count
        assert total_attempts > 0

        # If cascading occurred, multiple strategies might be used
        # (This is probabilistic and depends on interpretation confidence)

    def test_engine_str_includes_fallback_stats(self, engine_with_fallback):
        """Test that engine string representation includes fallback stats."""
        # Interpret something
        state = engine_with_fallback.create_initial_state()
        engine_with_fallback.interpret("hello", "user", state)

        engine_str = str(engine_with_fallback)

        # Should include fallback stats
        assert "fallback" in engine_str or "rules=" in engine_str


class TestModelSwitching:
    """Test model switching functionality."""

    @pytest.fixture
    def engine(self):
        """Create NLU engine with hybrid fallback."""
        config = NLUEngineConfig(
            use_nlu=True,
            use_llm=True,
            enable_hybrid_fallback=True,
        )
        return NLUDialogueEngine("test_agent", config=config)

    def test_get_interpreter_for_haiku(self, engine):
        """Test getting Haiku interpreter."""
        interpreter = engine._get_interpreter_for_strategy(InterpretationStrategy.HAIKU)

        assert interpreter is not None
        assert interpreter == engine.haiku_interpreter

    def test_get_interpreter_for_sonnet(self, engine):
        """Test getting Sonnet interpreter."""
        interpreter = engine._get_interpreter_for_strategy(InterpretationStrategy.SONNET)

        assert interpreter is not None
        assert interpreter == engine.sonnet_interpreter

    def test_get_interpreter_for_rules(self, engine):
        """Test getting interpreter for rules (returns default)."""
        interpreter = engine._get_interpreter_for_strategy(InterpretationStrategy.RULES)

        # Rules don't use interpreter, so should return default
        assert interpreter == engine.context_interpreter

    def test_get_interpreter_none_returns_default(self, engine):
        """Test that None strategy returns default interpreter."""
        interpreter = engine._get_interpreter_for_strategy(None)

        assert interpreter == engine.context_interpreter


class TestEngineWithoutHybridFallback:
    """Test engine behavior when hybrid fallback is disabled."""

    @pytest.fixture
    def engine_no_fallback(self):
        """Create NLU engine without hybrid fallback."""
        config = NLUEngineConfig(
            use_nlu=True,
            use_llm=True,
            enable_hybrid_fallback=False,  # Disabled
        )
        return NLUDialogueEngine("test_agent", config=config)

    def test_no_separate_interpreters_created(self, engine_no_fallback):
        """Test that separate interpreters are not created when fallback disabled."""
        assert engine_no_fallback.haiku_interpreter is None
        assert engine_no_fallback.sonnet_interpreter is None
        assert engine_no_fallback.context_interpreter is not None

    def test_fallback_strategy_not_initialized(self, engine_no_fallback):
        """Test that fallback strategy is not initialized when disabled."""
        assert engine_no_fallback.fallback_strategy is None

    def test_interpret_works_without_fallback(self, engine_no_fallback):
        """Test that interpretation works without hybrid fallback."""
        # Should fall back to regular interpretation
        state = engine_no_fallback.create_initial_state()
        moves = engine_no_fallback.interpret("hello", "user", state)

        # Should work, just without hybrid fallback stats
        assert isinstance(moves, list)
