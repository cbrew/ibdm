"""NLU-Enhanced Dialogue Engine for IBDM.

This module extends the DialogueMoveEngine with LLM-based natural language understanding
capabilities, providing sophisticated interpretation of user utterances.
"""

import logging
from dataclasses import dataclass
from typing import Any

from ibdm.core import Answer, DialogueMove, Question
from ibdm.core.questions import AltQuestion, WhQuestion, YNQuestion
from ibdm.engine.dialogue_engine import DialogueMoveEngine
from ibdm.nlu import (
    ContextInterpreter,
    ContextInterpreterConfig,
    DialogueActClassifier,
    DialogueActClassifierConfig,
    DialogueActType,
    EntityTracker,
    EntityTrackerConfig,
    FallbackConfig,
    HybridFallbackStrategy,
    InterpretationStrategy,
    LLMConfig,
    ModelType,
    QuestionAnalyzer,
    QuestionAnalyzerConfig,
    QuestionType,
    ReferenceResolver,
    ReferenceResolverConfig,
)
from ibdm.rules import RuleSet

logger = logging.getLogger(__name__)


@dataclass
class NLUEngineConfig:
    """Configuration for NLU-enhanced dialogue engine.

    Attributes:
        use_nlu: Whether to use NLU for interpretation (vs pure rules)
        use_llm: Whether to enable LLM-based NLU components
        llm_model: Which LLM model to use (Sonnet or Haiku)
        confidence_threshold: Minimum confidence for NLU results
        fallback_to_rules: Fall back to rule-based interpretation if NLU fails
        enable_hybrid_fallback: Use hybrid fallback strategy for smart model selection
        fallback_config: Configuration for hybrid fallback strategy (if None, uses defaults)
    """

    use_nlu: bool = True
    use_llm: bool = True
    llm_model: ModelType = ModelType.HAIKU  # Use Haiku for fast classification
    confidence_threshold: float = 0.5
    fallback_to_rules: bool = True
    enable_hybrid_fallback: bool = True
    fallback_config: FallbackConfig | None = None


class NLUDialogueEngine(DialogueMoveEngine):
    """Dialogue engine with integrated NLU capabilities.

    This engine extends the base DialogueMoveEngine by adding LLM-based natural
    language understanding during the interpretation phase. It can:
    - Classify dialogue acts
    - Understand questions and extract their structure
    - Track entities across turns
    - Resolve references (pronouns, descriptions)
    - Use dialogue context for interpretation

    Example:
        >>> config = NLUEngineConfig(use_nlu=True, use_llm=True)
        >>> engine = NLUDialogueEngine("agent_1", config=config)
        >>>
        >>> # Process user utterance
        >>> state, response = engine.process_input("What's the weather?", "user")
        >>> print(response.content if response else "No response")
    """

    def __init__(
        self,
        agent_id: str,
        rules: RuleSet | None = None,
        config: NLUEngineConfig | None = None,
    ):
        """Initialize the NLU-enhanced dialogue engine.

        Args:
            agent_id: Unique identifier for this agent
            rules: Rule set for dialogue processing (creates empty if None)
            config: NLU configuration (uses defaults if None)
        """
        super().__init__(agent_id, rules)

        self.config = config or NLUEngineConfig()

        # Initialize NLU components if enabled
        self.dialogue_act_classifier: DialogueActClassifier | None = None
        self.question_analyzer: QuestionAnalyzer | None = None
        self.entity_tracker: EntityTracker | None = None
        self.reference_resolver: ReferenceResolver | None = None
        self.context_interpreter: ContextInterpreter | None = None
        # Separate interpreters for different models (for hybrid fallback)
        self.haiku_interpreter: ContextInterpreter | None = None
        self.sonnet_interpreter: ContextInterpreter | None = None
        # Track last interpretation stats for token/latency reporting
        self.last_interpretation_tokens: int = 0
        self.last_interpretation_latency: float = 0.0

        # Initialize hybrid fallback strategy
        self.fallback_strategy: HybridFallbackStrategy | None = None
        if self.config.enable_hybrid_fallback:
            fallback_config = self.config.fallback_config or FallbackConfig()
            self.fallback_strategy = HybridFallbackStrategy(fallback_config)
            logger.info("Hybrid fallback strategy enabled")

        if self.config.use_nlu:
            self._initialize_nlu_components()

        logger.info(
            f"Initialized NLU engine for agent {agent_id} "
            f"(NLU: {self.config.use_nlu}, LLM: {self.config.use_llm})"
        )

    def _initialize_nlu_components(self) -> None:
        """Initialize NLU components based on configuration."""
        if not self.config.use_llm:
            logger.info("LLM disabled, NLU components will not be initialized")
            return

        try:
            # Configure LLM
            llm_config = LLMConfig(
                model=self.config.llm_model,
                temperature=0.3,  # Lower temp for classification
                max_tokens=1000,  # Shorter responses for NLU
            )

            # Dialogue act classifier
            self.dialogue_act_classifier = DialogueActClassifier(
                DialogueActClassifierConfig(llm_config=llm_config)
            )

            # Question analyzer
            self.question_analyzer = QuestionAnalyzer(QuestionAnalyzerConfig(llm_config=llm_config))

            # Entity tracker and reference resolver
            self.entity_tracker = EntityTracker(EntityTrackerConfig())
            self.reference_resolver = ReferenceResolver(
                self.entity_tracker,
                ReferenceResolverConfig(llm_config=llm_config, use_llm=self.config.use_llm),
            )

            # Context interpreter (integrates other components)
            self.context_interpreter = ContextInterpreter(
                ContextInterpreterConfig(llm_config=llm_config)
            )

            # For hybrid fallback: create separate interpreters for Haiku and Sonnet
            if self.config.enable_hybrid_fallback:
                haiku_config = LLMConfig(model=ModelType.HAIKU, temperature=0.3, max_tokens=1000)
                self.haiku_interpreter = ContextInterpreter(
                    ContextInterpreterConfig(llm_config=haiku_config)
                )

                sonnet_config = LLMConfig(model=ModelType.SONNET, temperature=0.3, max_tokens=2000)
                self.sonnet_interpreter = ContextInterpreter(
                    ContextInterpreterConfig(llm_config=sonnet_config)
                )

                logger.info("Created Haiku and Sonnet interpreters for hybrid fallback")

            logger.info("NLU components initialized successfully")

        except ValueError as e:
            logger.warning(f"Failed to initialize NLU components: {e}")
            logger.warning("Falling back to rule-based interpretation")
            self.config.use_llm = False

    def interpret(self, utterance: str, speaker: str) -> list[DialogueMove]:
        """Interpret utterance using NLU or rules.

        This overrides the base interpret() to add NLU-based interpretation.
        If NLU is enabled and configured, it will:
        1. Use hybrid fallback strategy to select interpretation approach
        2. Use context-aware interpretation to understand the utterance
        3. Classify the dialogue act
        4. Extract entities and resolve references
        5. Create appropriate DialogueMove objects
        6. Optionally cascade to more powerful strategies if needed

        If NLU fails or is disabled, falls back to rule-based interpretation.

        Args:
            utterance: The utterance to interpret
            speaker: ID of the speaker

        Returns:
            List of interpreted dialogue moves
        """
        # Use hybrid fallback strategy if enabled
        if self.fallback_strategy:
            return self._interpret_with_hybrid_fallback(utterance, speaker)

        # Legacy path: Try NLU-based interpretation first if enabled
        if self.config.use_nlu and self.config.use_llm and self.context_interpreter:
            try:
                moves = self._interpret_with_nlu(utterance, speaker)
                if moves:
                    logger.info(f"NLU interpreted {len(moves)} move(s) from utterance")
                    return moves
                elif not self.config.fallback_to_rules:
                    logger.warning("NLU produced no moves and fallback disabled")
                    return []

            except Exception as e:
                logger.warning(f"NLU interpretation failed: {e}")
                if not self.config.fallback_to_rules:
                    raise

        # Fall back to rule-based interpretation
        logger.debug("Using rule-based interpretation")
        return super().interpret(utterance, speaker)

    def _interpret_with_hybrid_fallback(self, utterance: str, speaker: str) -> list[DialogueMove]:
        """Interpret utterance using hybrid fallback strategy.

        This method uses the HybridFallbackStrategy to intelligently select
        which interpretation approach to use based on:
        - Fast-path pattern matching
        - Utterance complexity
        - Cost and latency budgets
        - Cascading fallback

        Args:
            utterance: The utterance to interpret
            speaker: ID of the speaker

        Returns:
            List of interpreted dialogue moves
        """
        if not self.fallback_strategy:
            logger.warning("Hybrid fallback called but strategy not initialized")
            return super().interpret(utterance, speaker)

        # Determine available strategies
        available = []
        if self.rules and self.rules.rule_count() > 0:
            available.append(InterpretationStrategy.RULES)
        if self.config.use_llm and self.context_interpreter:
            available.append(InterpretationStrategy.HAIKU)
            # Sonnet available if we want to use it (could add a config flag)
            available.append(InterpretationStrategy.SONNET)

        # Select initial strategy
        strategy = self.fallback_strategy.select_strategy(utterance, available)
        logger.debug(f"Selected strategy: {strategy.value}")

        # Try the selected strategy with timing
        import time

        start_time = time.time()
        self.last_interpretation_tokens = 0
        self.last_interpretation_latency = 0.0

        moves, confidence = self._try_strategy(strategy, utterance, speaker)

        latency = time.time() - start_time
        self.last_interpretation_latency = latency

        # Record usage with actual token count and latency
        self.fallback_strategy.record_usage(
            strategy, tokens=self.last_interpretation_tokens, latency=latency
        )

        # Check if we should cascade
        next_strategy = self.fallback_strategy.should_cascade(
            strategy, success=len(moves) > 0, confidence=confidence
        )

        if next_strategy and next_strategy in available:
            logger.info(f"Cascading from {strategy.value} to {next_strategy.value}")

            # Time the cascade attempt
            cascade_start = time.time()
            self.last_interpretation_tokens = 0

            cascade_moves, cascade_conf = self._try_strategy(next_strategy, utterance, speaker)

            cascade_latency = time.time() - cascade_start

            # Use cascade results if better
            if len(cascade_moves) > len(moves) or cascade_conf > confidence:
                moves = cascade_moves
                confidence = cascade_conf
                strategy = next_strategy

            # Record cascade usage with actual token count and latency
            self.fallback_strategy.record_usage(
                next_strategy, tokens=self.last_interpretation_tokens, latency=cascade_latency
            )

        if moves:
            logger.info(
                f"{strategy.value} interpreted {len(moves)} move(s) (confidence: {confidence:.2f})"
            )
        else:
            logger.debug(f"{strategy.value} produced no moves")

        return moves

    def _try_strategy(
        self, strategy: InterpretationStrategy, utterance: str, speaker: str
    ) -> tuple[list[DialogueMove], float]:
        """Try a specific interpretation strategy.

        Args:
            strategy: The strategy to try
            utterance: The utterance to interpret
            speaker: Speaker ID

        Returns:
            Tuple of (moves, confidence)
        """
        if strategy == InterpretationStrategy.RULES:
            # Use rule-based interpretation
            moves = super().interpret(utterance, speaker)
            # Rules don't have confidence, use 1.0 if successful
            confidence = 1.0 if moves else 0.0
            return moves, confidence

        elif strategy in [InterpretationStrategy.HAIKU, InterpretationStrategy.SONNET]:
            # Use LLM-based interpretation with model switching
            try:
                moves = self._interpret_with_nlu(utterance, speaker, strategy)
                # Get confidence from NLU results
                # For now, use a heuristic: 0.8 if moves produced, 0.0 otherwise
                confidence = 0.8 if moves else 0.0
                return moves, confidence
            except Exception as e:
                logger.warning(f"NLU interpretation failed: {e}")
                return [], 0.0

        return [], 0.0

    def _get_interpreter_for_strategy(
        self, strategy: InterpretationStrategy | None
    ) -> ContextInterpreter | None:
        """Get the appropriate context interpreter for the given strategy.

        Args:
            strategy: The interpretation strategy (HAIKU, SONNET, or None)

        Returns:
            The appropriate ContextInterpreter, or None if not available
        """
        if strategy == InterpretationStrategy.HAIKU:
            interpreter = self.haiku_interpreter
            if interpreter:
                logger.debug("Using Haiku interpreter")
                return interpreter
            logger.warning("Haiku interpreter not available, falling back to default")

        elif strategy == InterpretationStrategy.SONNET:
            interpreter = self.sonnet_interpreter
            if interpreter:
                logger.debug("Using Sonnet interpreter")
                return interpreter
            logger.warning("Sonnet interpreter not available, falling back to default")

        # Default to the main context interpreter
        return self.context_interpreter

    def _interpret_with_nlu(
        self, utterance: str, speaker: str, strategy: InterpretationStrategy | None = None
    ) -> list[DialogueMove]:
        """Interpret utterance using NLU components.

        Args:
            utterance: The utterance to interpret
            speaker: ID of the speaker
            strategy: Optional strategy to use specific model (HAIKU or SONNET)

        Returns:
            List of interpreted dialogue moves
        """
        moves: list[DialogueMove] = []

        # Select appropriate interpreter based on strategy
        interpreter = self._get_interpreter_for_strategy(strategy)

        # Use context interpreter for comprehensive analysis
        if interpreter:
            interpretation = interpreter.interpret(utterance, self.state)

            # Track token usage from this interpretation
            self.last_interpretation_tokens = interpreter.last_tokens_used

            # Extract entities and update tracker
            if interpretation.entities:
                logger.debug(f"Extracted {len(interpretation.entities)} entities")

            # Create moves based on dialogue act
            if interpretation.dialogue_act:
                act_moves = self._create_moves_from_act(
                    interpretation.dialogue_act,
                    utterance,
                    speaker,
                    interpretation,
                )
                moves.extend(act_moves)

        # If no moves created from context interpreter, try individual classifiers
        if not moves and self.dialogue_act_classifier:
            act_result = self.dialogue_act_classifier.classify(utterance)

            if act_result.confidence >= self.config.confidence_threshold:
                moves = self._create_moves_from_act_type(
                    act_result.dialogue_act, utterance, speaker
                )

        return moves

    def _create_moves_from_act(
        self,
        dialogue_act: str,
        utterance: str,
        speaker: str,
        interpretation: Any,
    ) -> list[DialogueMove]:
        """Create dialogue moves from dialogue act and interpretation.

        Args:
            dialogue_act: The classified dialogue act
            utterance: Original utterance
            speaker: Speaker ID
            interpretation: Full interpretation result

        Returns:
            List of dialogue moves
        """
        moves: list[DialogueMove] = []

        # Question
        if dialogue_act == DialogueActType.QUESTION.value:
            question_move = self._create_question_move(utterance, speaker, interpretation)
            if question_move:
                moves.append(question_move)

        # Answer
        elif dialogue_act == DialogueActType.ANSWER.value:
            answer_move = self._create_answer_move(utterance, speaker, interpretation)
            if answer_move:
                moves.append(answer_move)

        # Assertion/Statement
        elif dialogue_act in [DialogueActType.ASSERTION.value, DialogueActType.STATEMENT.value]:
            moves.append(
                DialogueMove(
                    move_type="assert",
                    content=utterance,
                    speaker=speaker,
                    metadata={"dialogue_act": dialogue_act},
                )
            )

        # Request
        elif dialogue_act == DialogueActType.REQUEST.value:
            moves.append(
                DialogueMove(
                    move_type="request",
                    content=utterance,
                    speaker=speaker,
                    metadata={"dialogue_act": dialogue_act},
                )
            )

        # Acknowledgment
        elif dialogue_act in [
            DialogueActType.ACKNOWLEDGMENT.value,
            DialogueActType.ACCEPTANCE.value,
        ]:
            moves.append(
                DialogueMove(
                    move_type="acknowledge",
                    content=utterance,
                    speaker=speaker,
                    metadata={"dialogue_act": dialogue_act},
                )
            )

        # Clarification
        elif dialogue_act == DialogueActType.CLARIFICATION.value:
            moves.append(
                DialogueMove(
                    move_type="clarify",
                    content=utterance,
                    speaker=speaker,
                    metadata={"dialogue_act": dialogue_act},
                )
            )

        # Greeting
        elif dialogue_act == DialogueActType.GREETING.value:
            moves.append(
                DialogueMove(
                    move_type="greet",
                    content=utterance,
                    speaker=speaker,
                    metadata={"dialogue_act": dialogue_act},
                )
            )

        # Farewell
        elif dialogue_act == DialogueActType.FAREWELL.value:
            moves.append(
                DialogueMove(
                    move_type="quit",
                    content=utterance,
                    speaker=speaker,
                    metadata={"dialogue_act": dialogue_act},
                )
            )

        # Default: create generic move
        else:
            moves.append(
                DialogueMove(
                    move_type="inform",
                    content=utterance,
                    speaker=speaker,
                    metadata={"dialogue_act": dialogue_act},
                )
            )

        return moves

    def _create_moves_from_act_type(
        self, act_type: str, utterance: str, speaker: str
    ) -> list[DialogueMove]:
        """Create moves from dialogue act type (simplified version).

        Args:
            act_type: Dialogue act type
            utterance: Original utterance
            speaker: Speaker ID

        Returns:
            List of dialogue moves
        """
        return self._create_moves_from_act(act_type, utterance, speaker, None)

    def _create_question_move(
        self, utterance: str, speaker: str, interpretation: Any
    ) -> DialogueMove | None:
        """Create a question move from utterance.

        Args:
            utterance: Original utterance
            speaker: Speaker ID
            interpretation: Full interpretation (may be None)

        Returns:
            DialogueMove with question, or None
        """
        # Try to analyze question structure if we have the analyzer
        if self.question_analyzer:
            try:
                analysis = self.question_analyzer.analyze(utterance)

                if analysis.confidence >= self.config.confidence_threshold:
                    # Create appropriate Question object based on type
                    question = self._create_question_from_analysis(analysis, utterance)

                    return DialogueMove(
                        move_type="ask",
                        content=question if question else utterance,
                        speaker=speaker,
                        metadata={
                            "question_type": analysis.question_type,
                            "confidence": analysis.confidence,
                        },
                    )

            except Exception as e:
                logger.warning(f"Question analysis failed: {e}")

        # Default: create simple question move
        return DialogueMove(
            move_type="ask",
            content=utterance,
            speaker=speaker,
            metadata={"question_type": "unknown"},
        )

    def _create_question_from_analysis(self, analysis: Any, utterance: str) -> Question | None:
        """Create a Question object from analysis.

        Args:
            analysis: Question analysis result
            utterance: Original utterance

        Returns:
            Question object or None
        """
        try:
            # Wh-question
            if analysis.question_type == QuestionType.WH.value:
                return WhQuestion(
                    variable="x",
                    predicate=analysis.focus or utterance,
                    constraints={},
                )

            # Yes/no question
            elif analysis.question_type in [QuestionType.YES_NO.value, "yes-no", "yes_no"]:
                return YNQuestion(proposition=utterance)

            # Alternative question
            elif analysis.question_type == QuestionType.ALTERNATIVE.value:
                alternatives = []
                if hasattr(analysis, "alternatives") and analysis.alternatives:
                    alternatives = analysis.alternatives
                return AltQuestion(alternatives=alternatives, variable="x")

        except Exception as e:
            logger.warning(f"Failed to create Question object: {e}")

        return None

    def _create_answer_move(
        self, utterance: str, speaker: str, interpretation: Any
    ) -> DialogueMove | None:
        """Create an answer move from utterance.

        Args:
            utterance: Original utterance
            speaker: Speaker ID
            interpretation: Full interpretation (may be None)

        Returns:
            DialogueMove with answer, or None
        """
        # Check if there's a question on the QUD stack to answer
        top_qud = self.state.shared.top_qud()

        if top_qud:
            # Create Answer object
            answer = Answer(content=utterance, addresses_question=top_qud)

            return DialogueMove(
                move_type="answer",
                content=answer,
                speaker=speaker,
                metadata={"addresses_qud": str(top_qud)},
            )

        # No question to answer - treat as statement
        return DialogueMove(
            move_type="inform",
            content=utterance,
            speaker=speaker,
            metadata={"intended_as_answer": True},
        )

    def get_fallback_stats(self):
        """Get fallback strategy statistics.

        Returns:
            FallbackStats object, or None if hybrid fallback disabled
        """
        if self.fallback_strategy:
            return self.fallback_strategy.get_stats()
        return None

    def reset_fallback_session(self):
        """Reset session-level fallback statistics."""
        if self.fallback_strategy:
            self.fallback_strategy.reset_session_stats()

    def reset(self) -> None:
        """Reset the engine and NLU components."""
        super().reset()

        # Reset NLU trackers
        if self.entity_tracker:
            self.entity_tracker = EntityTracker(EntityTrackerConfig())

        if self.reference_resolver and self.entity_tracker:
            self.reference_resolver = ReferenceResolver(
                self.entity_tracker,
                ReferenceResolverConfig(use_llm=self.config.use_llm),
            )

        # Reset fallback session stats
        if self.fallback_strategy:
            self.fallback_strategy.reset_session_stats()

    def __str__(self) -> str:
        """Return string representation."""
        base = (
            f"NLUDialogueEngine(agent={self.agent_id}, "
            f"nlu_enabled={self.config.use_nlu}, "
            f"llm_enabled={self.config.use_llm}, "
            f"rules={self.rules.rule_count()}, "
            f"qud={len(self.state.shared.qud)}"
        )

        if self.fallback_strategy:
            stats = self.fallback_strategy.get_stats()
            base += (
                f", fallback[total={stats.total_utterances}, "
                f"rules={stats.rules_count}, "
                f"haiku={stats.haiku_count}, "
                f"fast_path={stats.fast_path_hits}]"
            )

        return base + ")"


def create_nlu_engine(
    agent_id: str,
    use_nlu: bool = True,
    use_llm: bool = True,
    rules: RuleSet | None = None,
) -> NLUDialogueEngine:
    """Convenience function to create an NLU-enhanced dialogue engine.

    Args:
        agent_id: Unique identifier for the agent
        use_nlu: Whether to enable NLU interpretation
        use_llm: Whether to enable LLM-based NLU
        rules: Optional rule set for fallback

    Returns:
        Configured NLUDialogueEngine

    Example:
        >>> engine = create_nlu_engine("agent_1", use_nlu=True, use_llm=True)
        >>> state, response = engine.process_input("Hello!", "user")
    """
    config = NLUEngineConfig(use_nlu=use_nlu, use_llm=use_llm)
    return NLUDialogueEngine(agent_id, rules=rules, config=config)
