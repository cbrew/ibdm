"""Hybrid rule/LLM fallback strategies for NLU.

This module implements intelligent fallback strategies that optimize cost, latency,
and accuracy by choosing the right interpretation approach for each utterance.
"""

import logging
import re
from dataclasses import dataclass
from enum import Enum
from re import Pattern

logger = logging.getLogger(__name__)


class InterpretationStrategy(Enum):
    """Available interpretation strategies."""

    RULES = "rules"  # Pure rule-based interpretation
    HAIKU = "haiku"  # Fast LLM (Claude Haiku)
    SONNET = "sonnet"  # Powerful LLM (Claude Sonnet)


@dataclass
class UtteranceComplexity:
    """Analysis of utterance complexity."""

    word_count: int
    sentence_count: int
    has_question: bool
    has_negation: bool
    has_pronouns: bool
    has_temporal_refs: bool
    complexity_score: float  # 0.0 (simple) to 1.0 (complex)


@dataclass
class FallbackConfig:
    """Configuration for hybrid fallback strategy.

    Attributes:
        enable_fast_path: Use pattern matching for common utterances
        enable_complexity_analysis: Analyze utterance complexity for model selection
        enable_cost_tracking: Track and limit LLM costs
        enable_cascading: Try progressively more powerful strategies

        # Thresholds
        simple_threshold: Complexity below this uses rules only
        moderate_threshold: Complexity below this uses Haiku
        # Above moderate uses Sonnet

        # Cost limits (in tokens)
        max_tokens_per_turn: Maximum tokens to use per turn
        max_tokens_per_session: Maximum tokens to use per session

        # Latency budgets (in seconds)
        latency_budget: Maximum latency budget (use faster models if exceeded)
    """

    enable_fast_path: bool = True
    enable_complexity_analysis: bool = True
    enable_cost_tracking: bool = True
    enable_cascading: bool = True

    simple_threshold: float = 0.3
    moderate_threshold: float = 0.6

    max_tokens_per_turn: int = 1000
    max_tokens_per_session: int = 100000

    latency_budget: float = 2.0  # seconds


@dataclass
class FallbackStats:
    """Statistics for fallback strategy performance."""

    total_utterances: int = 0
    rules_count: int = 0
    haiku_count: int = 0
    sonnet_count: int = 0
    fast_path_hits: int = 0
    tokens_used: int = 0
    total_latency: float = 0.0


class FastPathMatcher:
    """Fast-path pattern matching for common utterances."""

    # Common patterns that can be handled by rules
    GREETING_PATTERNS: list[Pattern[str]] = [
        re.compile(r"^(hi|hello|hey|greetings?)[\s!.]*$", re.IGNORECASE),
        re.compile(r"^good\s+(morning|afternoon|evening)[\s!.]*$", re.IGNORECASE),
    ]

    FAREWELL_PATTERNS: list[Pattern[str]] = [
        re.compile(r"^(bye|goodbye|see you|farewell)[\s!.]*$", re.IGNORECASE),
        re.compile(r"^(good\s*night|take care)[\s!.]*$", re.IGNORECASE),
    ]

    ACKNOWLEDGMENT_PATTERNS: list[Pattern[str]] = [
        re.compile(r"^(yes|yeah|yep|ok|okay|sure|alright)[\s!.]*$", re.IGNORECASE),
        re.compile(r"^(no|nope|nah)[\s!.]*$", re.IGNORECASE),
        re.compile(r"^(thanks?|thank you)[\s!.]*$", re.IGNORECASE),
    ]

    SIMPLE_COMMAND_PATTERNS: list[Pattern[str]] = [
        re.compile(r"^(help|stop|quit|exit)[\s!.]*$", re.IGNORECASE),
        re.compile(r"^(show|list|get)\s+\w+[\s!.]*$", re.IGNORECASE),
    ]

    @classmethod
    def matches_fast_path(cls, utterance: str) -> bool:
        """Check if utterance matches any fast-path pattern.

        Args:
            utterance: The utterance to check

        Returns:
            True if matches a fast-path pattern
        """
        utterance = utterance.strip()

        for pattern_list in [
            cls.GREETING_PATTERNS,
            cls.FAREWELL_PATTERNS,
            cls.ACKNOWLEDGMENT_PATTERNS,
            cls.SIMPLE_COMMAND_PATTERNS,
        ]:
            for pattern in pattern_list:
                if pattern.match(utterance):
                    return True

        return False


class ComplexityAnalyzer:
    """Analyzes utterance complexity to guide model selection."""

    # Patterns for complexity indicators
    PRONOUN_PATTERN = re.compile(
        r"\b(he|she|it|they|him|her|them|his|hers|its|their|this|that|these|those)\b",
        re.IGNORECASE,
    )
    TEMPORAL_PATTERN = re.compile(
        r"\b(yesterday|today|tomorrow|now|then|before|after|when|while)\b", re.IGNORECASE
    )
    NEGATION_PATTERN = re.compile(r"\b(not|no|never|none|nothing|neither|nor|n't)\b", re.IGNORECASE)

    @classmethod
    def analyze(cls, utterance: str) -> UtteranceComplexity:
        """Analyze utterance complexity.

        Args:
            utterance: The utterance to analyze

        Returns:
            UtteranceComplexity object
        """
        # Basic counts
        words = utterance.split()
        word_count = len(words)
        sentences = re.split(r"[.!?]+", utterance)
        sentence_count = len([s for s in sentences if s.strip()])

        # Pattern matching
        has_question = "?" in utterance
        has_negation = bool(cls.NEGATION_PATTERN.search(utterance))
        has_pronouns = bool(cls.PRONOUN_PATTERN.search(utterance))
        has_temporal_refs = bool(cls.TEMPORAL_PATTERN.search(utterance))

        # Calculate complexity score (0.0 to 1.0)
        score = 0.0

        # Length contributes to complexity
        if word_count > 20:
            score += 0.3
        elif word_count > 10:
            score += 0.2
        elif word_count > 5:
            score += 0.1

        # Multiple sentences increase complexity
        if sentence_count > 2:
            score += 0.2
        elif sentence_count > 1:
            score += 0.1

        # Linguistic features
        if has_pronouns:
            score += 0.15  # Requires reference resolution
        if has_temporal_refs:
            score += 0.15  # Requires temporal reasoning
        if has_negation:
            score += 0.1  # Negation is tricky
        if has_question:
            score += 0.1  # Questions need understanding

        # Cap at 1.0
        score = min(score, 1.0)

        return UtteranceComplexity(
            word_count=word_count,
            sentence_count=sentence_count,
            has_question=has_question,
            has_negation=has_negation,
            has_pronouns=has_pronouns,
            has_temporal_refs=has_temporal_refs,
            complexity_score=score,
        )


class HybridFallbackStrategy:
    """Intelligent fallback strategy that optimizes cost, latency, and accuracy.

    This class implements the core logic for deciding which interpretation approach
    to use for each utterance, based on:
    - Fast-path pattern matching
    - Utterance complexity analysis
    - Cost and latency budgets
    - Cascading fallback (try simpler methods first)
    """

    def __init__(self, config: FallbackConfig | None = None):
        """Initialize the fallback strategy.

        Args:
            config: Configuration for fallback behavior
        """
        self.config = config or FallbackConfig()
        self.stats = FallbackStats()
        self.session_tokens = 0

    def select_strategy(
        self, utterance: str, available_strategies: list[InterpretationStrategy]
    ) -> InterpretationStrategy:
        """Select the best interpretation strategy for the utterance.

        Args:
            utterance: The utterance to interpret
            available_strategies: List of available strategies

        Returns:
            Selected strategy
        """
        self.stats.total_utterances += 1

        # Fast-path matching (highest priority)
        if self.config.enable_fast_path and FastPathMatcher.matches_fast_path(utterance):
            logger.debug("Fast-path match - using rules")
            self.stats.fast_path_hits += 1
            return InterpretationStrategy.RULES

        # Check cost budget
        if self.config.enable_cost_tracking:
            if self.session_tokens >= self.config.max_tokens_per_session:
                logger.warning("Session token budget exceeded - using rules only")
                return InterpretationStrategy.RULES

        # Analyze complexity if enabled
        if self.config.enable_complexity_analysis:
            complexity = ComplexityAnalyzer.analyze(utterance)
            logger.debug(
                f"Utterance complexity: {complexity.complexity_score:.2f} "
                f"(words: {complexity.word_count}, "
                f"pronouns: {complexity.has_pronouns}, "
                f"temporal: {complexity.has_temporal_refs})"
            )

            # Simple utterances → rules
            if complexity.complexity_score < self.config.simple_threshold:
                if InterpretationStrategy.RULES in available_strategies:
                    logger.debug("Low complexity - using rules")
                    return InterpretationStrategy.RULES

            # Moderate complexity → Haiku
            elif complexity.complexity_score < self.config.moderate_threshold:
                if InterpretationStrategy.HAIKU in available_strategies:
                    logger.debug("Moderate complexity - using Haiku")
                    return InterpretationStrategy.HAIKU
                elif InterpretationStrategy.RULES in available_strategies:
                    return InterpretationStrategy.RULES

            # High complexity → Sonnet
            else:
                if InterpretationStrategy.SONNET in available_strategies:
                    logger.debug("High complexity - using Sonnet")
                    return InterpretationStrategy.SONNET
                elif InterpretationStrategy.HAIKU in available_strategies:
                    logger.debug("Sonnet unavailable - using Haiku")
                    return InterpretationStrategy.HAIKU
                elif InterpretationStrategy.RULES in available_strategies:
                    return InterpretationStrategy.RULES

        # Default: prefer Haiku for balanced cost/performance
        if InterpretationStrategy.HAIKU in available_strategies:
            return InterpretationStrategy.HAIKU
        elif InterpretationStrategy.SONNET in available_strategies:
            return InterpretationStrategy.SONNET
        else:
            return InterpretationStrategy.RULES

    def should_cascade(
        self, current_strategy: InterpretationStrategy, success: bool, confidence: float = 0.0
    ) -> InterpretationStrategy | None:
        """Determine if we should cascade to a more powerful strategy.

        Args:
            current_strategy: The strategy that was just tried
            success: Whether the strategy succeeded
            confidence: Confidence score of the result (if available)

        Returns:
            Next strategy to try, or None if no cascade needed
        """
        if not self.config.enable_cascading:
            return None

        # If successful and confident, no need to cascade
        if success and confidence >= 0.7:
            return None

        # Cascade from rules → Haiku → Sonnet
        if current_strategy == InterpretationStrategy.RULES:
            if not success or confidence < 0.5:
                logger.debug("Cascading from rules to Haiku")
                return InterpretationStrategy.HAIKU

        elif current_strategy == InterpretationStrategy.HAIKU:
            if not success or confidence < 0.5:
                # Check budget before cascading to expensive Sonnet
                if self.session_tokens < self.config.max_tokens_per_session * 0.8:
                    logger.debug("Cascading from Haiku to Sonnet")
                    return InterpretationStrategy.SONNET
                else:
                    logger.warning("Budget limit prevents cascade to Sonnet")

        return None

    def record_usage(self, strategy: InterpretationStrategy, tokens: int = 0, latency: float = 0.0):
        """Record usage statistics.

        Args:
            strategy: The strategy that was used
            tokens: Number of tokens consumed
            latency: Latency in seconds
        """
        if strategy == InterpretationStrategy.RULES:
            self.stats.rules_count += 1
        elif strategy == InterpretationStrategy.HAIKU:
            self.stats.haiku_count += 1
        elif strategy == InterpretationStrategy.SONNET:
            self.stats.sonnet_count += 1

        if tokens > 0:
            self.stats.tokens_used += tokens
            self.session_tokens += tokens

        if latency > 0:
            self.stats.total_latency += latency

    def get_stats(self) -> FallbackStats:
        """Get current statistics.

        Returns:
            FallbackStats object
        """
        return self.stats

    def reset_session_stats(self):
        """Reset session-level statistics."""
        self.session_tokens = 0
        logger.info("Session statistics reset")

    def __str__(self) -> str:
        """Return string representation."""
        return (
            f"HybridFallbackStrategy("
            f"total={self.stats.total_utterances}, "
            f"rules={self.stats.rules_count}, "
            f"haiku={self.stats.haiku_count}, "
            f"sonnet={self.stats.sonnet_count}, "
            f"fast_path={self.stats.fast_path_hits}, "
            f"tokens={self.stats.tokens_used})"
        )
