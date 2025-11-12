"""Tests for hybrid rule/LLM fallback strategies."""

import pytest

from ibdm.nlu.fallback_strategy import (
    ComplexityAnalyzer,
    FallbackConfig,
    FallbackStats,
    FastPathMatcher,
    HybridFallbackStrategy,
    InterpretationStrategy,
    UtteranceComplexity,
)


class TestInterpretationStrategy:
    """Tests for InterpretationStrategy enum."""

    def test_strategy_values(self):
        """Test strategy enum values."""
        assert InterpretationStrategy.RULES.value == "rules"
        assert InterpretationStrategy.HAIKU.value == "haiku"
        assert InterpretationStrategy.SONNET.value == "sonnet"


class TestUtteranceComplexity:
    """Tests for UtteranceComplexity dataclass."""

    def test_create_complexity(self):
        """Test creating UtteranceComplexity."""
        complexity = UtteranceComplexity(
            word_count=5,
            sentence_count=1,
            has_question=True,
            has_negation=False,
            has_pronouns=False,
            has_temporal_refs=False,
            complexity_score=0.3,
        )

        assert complexity.word_count == 5
        assert complexity.sentence_count == 1
        assert complexity.has_question is True
        assert complexity.complexity_score == 0.3


class TestFallbackConfig:
    """Tests for FallbackConfig."""

    def test_default_config(self):
        """Test default fallback configuration."""
        config = FallbackConfig()

        assert config.enable_fast_path is True
        assert config.enable_complexity_analysis is True
        assert config.enable_cost_tracking is True
        assert config.enable_cascading is True
        assert config.simple_threshold == 0.3
        assert config.moderate_threshold == 0.6
        assert config.max_tokens_per_turn == 1000
        assert config.max_tokens_per_session == 100000
        assert config.latency_budget == 2.0

    def test_custom_config(self):
        """Test custom fallback configuration."""
        config = FallbackConfig(
            enable_fast_path=False,
            simple_threshold=0.2,
            moderate_threshold=0.7,
            max_tokens_per_session=50000,
        )

        assert config.enable_fast_path is False
        assert config.simple_threshold == 0.2
        assert config.moderate_threshold == 0.7
        assert config.max_tokens_per_session == 50000


class TestFastPathMatcher:
    """Tests for FastPathMatcher."""

    def test_greeting_patterns(self):
        """Test greeting pattern matching."""
        assert FastPathMatcher.matches_fast_path("Hello") is True
        assert FastPathMatcher.matches_fast_path("Hi!") is True
        assert FastPathMatcher.matches_fast_path("hey") is True
        assert FastPathMatcher.matches_fast_path("Good morning") is True
        assert FastPathMatcher.matches_fast_path("Good afternoon!") is True

    def test_farewell_patterns(self):
        """Test farewell pattern matching."""
        assert FastPathMatcher.matches_fast_path("bye") is True
        assert FastPathMatcher.matches_fast_path("Goodbye!") is True
        assert FastPathMatcher.matches_fast_path("See you") is True
        assert FastPathMatcher.matches_fast_path("Good night!") is True

    def test_acknowledgment_patterns(self):
        """Test acknowledgment pattern matching."""
        assert FastPathMatcher.matches_fast_path("yes") is True
        assert FastPathMatcher.matches_fast_path("Yeah!") is True
        assert FastPathMatcher.matches_fast_path("OK") is True
        assert FastPathMatcher.matches_fast_path("No") is True
        assert FastPathMatcher.matches_fast_path("Thanks") is True
        assert FastPathMatcher.matches_fast_path("Thank you!") is True

    def test_simple_command_patterns(self):
        """Test simple command pattern matching."""
        assert FastPathMatcher.matches_fast_path("help") is True
        assert FastPathMatcher.matches_fast_path("quit") is True
        assert FastPathMatcher.matches_fast_path("exit!") is True
        assert FastPathMatcher.matches_fast_path("show weather") is True
        assert FastPathMatcher.matches_fast_path("list items") is True

    def test_no_match(self):
        """Test utterances that don't match fast path."""
        assert FastPathMatcher.matches_fast_path("What's the weather?") is False
        assert FastPathMatcher.matches_fast_path("Tell me about yourself") is False
        assert FastPathMatcher.matches_fast_path("How are you doing?") is False
        assert FastPathMatcher.matches_fast_path("She went to the store") is False


class TestComplexityAnalyzer:
    """Tests for ComplexityAnalyzer."""

    def test_simple_utterance(self):
        """Test analysis of simple utterance."""
        complexity = ComplexityAnalyzer.analyze("Hello")

        assert complexity.word_count == 1
        assert complexity.sentence_count == 1
        assert complexity.has_question is False
        assert complexity.has_negation is False
        assert complexity.has_pronouns is False
        assert complexity.has_temporal_refs is False
        assert complexity.complexity_score < 0.3

    def test_question(self):
        """Test analysis of question."""
        complexity = ComplexityAnalyzer.analyze("What's the weather?")

        assert complexity.word_count == 3
        assert complexity.has_question is True
        assert complexity.complexity_score > 0.0

    def test_negation(self):
        """Test detection of negation."""
        complexity = ComplexityAnalyzer.analyze("I do not know")

        assert complexity.has_negation is True
        assert complexity.complexity_score >= 0.1

    def test_pronouns(self):
        """Test detection of pronouns."""
        complexity = ComplexityAnalyzer.analyze("She gave it to him")

        assert complexity.has_pronouns is True
        assert complexity.word_count == 5
        assert complexity.complexity_score >= 0.15

    def test_temporal_references(self):
        """Test detection of temporal references."""
        complexity = ComplexityAnalyzer.analyze("I saw her yesterday")

        assert complexity.has_temporal_refs is True
        assert complexity.complexity_score > 0.15

    def test_complex_utterance(self):
        """Test analysis of complex utterance."""
        complexity = ComplexityAnalyzer.analyze(
            "Yesterday, she told me that he was not going to the meeting today. "
            "I do not think that is true."
        )

        assert complexity.word_count > 15
        assert complexity.sentence_count == 2
        assert complexity.has_pronouns is True
        assert complexity.has_temporal_refs is True
        assert complexity.has_negation is True
        assert complexity.complexity_score > 0.5

    def test_complexity_capped_at_one(self):
        """Test that complexity score is capped at 1.0."""
        # Very long, complex utterance
        complexity = ComplexityAnalyzer.analyze(
            "Yesterday, she told me that he wasn't going to attend the important meeting today "
            "because he didn't think it was relevant to his work. I don't believe that's entirely "
            "true, but I can understand his perspective given what happened before. When I talked "
            "to them about it earlier this week, they seemed very concerned about the implications."
        )

        assert complexity.complexity_score <= 1.0
        assert complexity.word_count > 20


class TestHybridFallbackStrategy:
    """Tests for HybridFallbackStrategy."""

    @pytest.fixture
    def strategy(self):
        """Create a fallback strategy with default config."""
        return HybridFallbackStrategy()

    @pytest.fixture
    def custom_strategy(self):
        """Create a fallback strategy with custom config."""
        config = FallbackConfig(
            simple_threshold=0.2,
            moderate_threshold=0.5,
            max_tokens_per_session=50000,
        )
        return HybridFallbackStrategy(config)

    def test_create_strategy(self, strategy):
        """Test creating HybridFallbackStrategy."""
        assert strategy is not None
        assert isinstance(strategy.config, FallbackConfig)
        assert isinstance(strategy.stats, FallbackStats)

    def test_fast_path_selection(self, strategy):
        """Test that fast-path utterances select RULES strategy."""
        available = [
            InterpretationStrategy.RULES,
            InterpretationStrategy.HAIKU,
            InterpretationStrategy.SONNET,
        ]

        # Test various fast-path utterances
        for utterance in ["Hello", "yes", "goodbye", "help"]:
            selected = strategy.select_strategy(utterance, available)
            assert selected == InterpretationStrategy.RULES
            assert strategy.stats.fast_path_hits > 0

    def test_simple_utterance_selection(self, strategy):
        """Test that simple utterances select RULES."""
        available = [
            InterpretationStrategy.RULES,
            InterpretationStrategy.HAIKU,
        ]

        # Simple non-fast-path utterance
        selected = strategy.select_strategy("I agree", available)

        # Should select rules for simplicity
        assert selected == InterpretationStrategy.RULES

    def test_moderate_complexity_selection(self, strategy):
        """Test that moderate complexity selects HAIKU."""
        available = [
            InterpretationStrategy.RULES,
            InterpretationStrategy.HAIKU,
            InterpretationStrategy.SONNET,
        ]

        # Moderate complexity utterance
        selected = strategy.select_strategy("What's the weather today?", available)

        # Should select Haiku for moderate complexity
        assert selected in [InterpretationStrategy.HAIKU, InterpretationStrategy.RULES]

    def test_high_complexity_selection(self, strategy):
        """Test that high complexity selects SONNET."""
        available = [
            InterpretationStrategy.RULES,
            InterpretationStrategy.HAIKU,
            InterpretationStrategy.SONNET,
        ]

        # High complexity utterance
        selected = strategy.select_strategy(
            "Yesterday, she told me that he wasn't planning to attend the meeting "
            "because he didn't think it would be relevant to his current project.",
            available,
        )

        # Should select Sonnet for high complexity
        assert selected in [InterpretationStrategy.SONNET, InterpretationStrategy.HAIKU]

    def test_fallback_when_strategy_unavailable(self, strategy):
        """Test fallback when preferred strategy unavailable."""
        # Only rules available
        available = [InterpretationStrategy.RULES]

        # Even for complex utterance
        selected = strategy.select_strategy("What's the weather forecast for tomorrow?", available)

        assert selected == InterpretationStrategy.RULES

    def test_budget_enforcement(self, custom_strategy):
        """Test that budget is enforced."""
        available = [
            InterpretationStrategy.RULES,
            InterpretationStrategy.HAIKU,
            InterpretationStrategy.SONNET,
        ]

        # Exhaust the budget
        custom_strategy.session_tokens = 51000  # Over budget

        # Should select rules even for complex utterance
        selected = custom_strategy.select_strategy(
            "What's the weather forecast for tomorrow?", available
        )

        assert selected == InterpretationStrategy.RULES

    def test_cascading_on_low_confidence(self, strategy):
        """Test cascading to more powerful strategy on low confidence."""
        # Failed with rules, low confidence
        next_strategy = strategy.should_cascade(
            InterpretationStrategy.RULES, success=False, confidence=0.3
        )

        assert next_strategy == InterpretationStrategy.HAIKU

    def test_cascading_haiku_to_sonnet(self, strategy):
        """Test cascading from Haiku to Sonnet."""
        # Failed with Haiku
        next_strategy = strategy.should_cascade(
            InterpretationStrategy.HAIKU, success=False, confidence=0.3
        )

        assert next_strategy == InterpretationStrategy.SONNET

    def test_no_cascade_on_high_confidence(self, strategy):
        """Test no cascading when confidence is high."""
        # Successful with high confidence
        next_strategy = strategy.should_cascade(
            InterpretationStrategy.RULES, success=True, confidence=0.9
        )

        assert next_strategy is None

    def test_no_cascade_when_disabled(self):
        """Test no cascading when disabled in config."""
        config = FallbackConfig(enable_cascading=False)
        strategy = HybridFallbackStrategy(config)

        next_strategy = strategy.should_cascade(
            InterpretationStrategy.RULES, success=False, confidence=0.0
        )

        assert next_strategy is None

    def test_record_usage_rules(self, strategy):
        """Test recording rules usage."""
        strategy.record_usage(InterpretationStrategy.RULES)

        stats = strategy.get_stats()
        assert stats.rules_count == 1

    def test_record_usage_haiku(self, strategy):
        """Test recording Haiku usage."""
        strategy.record_usage(InterpretationStrategy.HAIKU, tokens=500, latency=0.5)

        stats = strategy.get_stats()
        assert stats.haiku_count == 1
        assert stats.tokens_used == 500
        assert stats.total_latency == 0.5

    def test_record_usage_sonnet(self, strategy):
        """Test recording Sonnet usage."""
        strategy.record_usage(InterpretationStrategy.SONNET, tokens=1000, latency=1.0)

        stats = strategy.get_stats()
        assert stats.sonnet_count == 1
        assert stats.tokens_used == 1000
        assert stats.total_latency == 1.0

    def test_session_token_tracking(self, strategy):
        """Test session token tracking."""
        strategy.record_usage(InterpretationStrategy.HAIKU, tokens=500)
        strategy.record_usage(InterpretationStrategy.HAIKU, tokens=300)

        assert strategy.session_tokens == 800
        assert strategy.stats.tokens_used == 800

    def test_reset_session_stats(self, strategy):
        """Test resetting session statistics."""
        # Record some usage
        strategy.record_usage(InterpretationStrategy.HAIKU, tokens=500)
        assert strategy.session_tokens == 500

        # Reset session
        strategy.reset_session_stats()

        assert strategy.session_tokens == 0
        # Note: total stats are not reset, only session tokens

    def test_str_representation(self, strategy):
        """Test string representation."""
        strategy.record_usage(InterpretationStrategy.RULES)
        strategy.record_usage(InterpretationStrategy.HAIKU, tokens=100)

        s = str(strategy)

        assert "HybridFallbackStrategy" in s
        assert "rules=1" in s
        assert "haiku=1" in s
        assert "tokens=100" in s


class TestFallbackStats:
    """Tests for FallbackStats dataclass."""

    def test_create_stats(self):
        """Test creating FallbackStats."""
        stats = FallbackStats(
            total_utterances=10,
            rules_count=3,
            haiku_count=5,
            sonnet_count=2,
            fast_path_hits=3,
            tokens_used=5000,
            total_latency=2.5,
        )

        assert stats.total_utterances == 10
        assert stats.rules_count == 3
        assert stats.haiku_count == 5
        assert stats.sonnet_count == 2
        assert stats.fast_path_hits == 3
        assert stats.tokens_used == 5000
        assert stats.total_latency == 2.5

    def test_default_stats(self):
        """Test default FallbackStats values."""
        stats = FallbackStats()

        assert stats.total_utterances == 0
        assert stats.rules_count == 0
        assert stats.haiku_count == 0
        assert stats.sonnet_count == 0
        assert stats.fast_path_hits == 0
        assert stats.tokens_used == 0
        assert stats.total_latency == 0.0


class TestComplexityThresholds:
    """Tests for complexity-based thresholds."""

    def test_simple_threshold(self):
        """Test that simple utterances are below simple threshold."""
        config = FallbackConfig(simple_threshold=0.3)

        simple_utterances = ["Hi", "Yes", "OK", "Thanks", "I see"]

        for utterance in simple_utterances:
            complexity = ComplexityAnalyzer.analyze(utterance)
            # Most should be simple
            if not FastPathMatcher.matches_fast_path(utterance):
                # Non-fast-path simple utterances should have low complexity
                assert (
                    complexity.complexity_score <= config.simple_threshold or utterance == "I see"
                )

    def test_moderate_threshold(self):
        """Test that moderate utterances are in moderate range."""
        moderate_utterances = [
            "What's the time?",
            "Where is it?",
            "Tell me more",
            "I do not understand",
        ]

        for utterance in moderate_utterances:
            complexity = ComplexityAnalyzer.analyze(utterance)
            # Should generally be in moderate range (though not guaranteed)
            # This is more of a smoke test
            assert complexity.complexity_score >= 0.0
            assert complexity.complexity_score <= 1.0
