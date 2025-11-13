"""NLU-Enhanced Dialogue Engine for IBDM.

This module extends the DialogueMoveEngine with LLM-based natural language understanding
capabilities, providing sophisticated interpretation of user utterances.
"""

import logging
from dataclasses import dataclass
from typing import Any

from ibdm.burr_integration.nlu_context import NLUContext
from ibdm.core import Answer, DialogueMove, InformationState, Question
from ibdm.core.questions import AltQuestion, WhQuestion, YNQuestion
from ibdm.engine.dialogue_engine import DialogueMoveEngine
from ibdm.nlu import (
    ContextInterpreter,
    ContextInterpreterConfig,
    DialogueActClassifier,
    DialogueActClassifierConfig,
    DialogueActType,
    LLMConfig,
    ModelType,
    QuestionAnalyzer,
    QuestionAnalyzerConfig,
    QuestionType,
)
from ibdm.rules import RuleSet

logger = logging.getLogger(__name__)


@dataclass
class NLUEngineConfig:
    """Configuration for NLU-enhanced dialogue engine.

    Attributes:
        llm_model: Which LLM model to use (defaults to Sonnet per Policy #9)
        confidence_threshold: Minimum confidence for NLU results
        temperature: LLM temperature for generation
        max_tokens: Maximum tokens for LLM responses
    """

    llm_model: ModelType = ModelType.SONNET  # Use Sonnet by default (Policy #9)
    confidence_threshold: float = 0.5
    temperature: float = 0.3
    max_tokens: int = 2000


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

        # Store LLM config for creating stateful components on-demand
        self.llm_config = LLMConfig(
            model=self.config.llm_model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
        )

        # Initialize stateless NLU components (dialogue act classifier,
        # question analyzer, context interpreter).
        # Note: Entity tracker and reference resolver are NOT instance variables -
        # they're managed via NLUContext
        self.dialogue_act_classifier: DialogueActClassifier | None = None
        self.question_analyzer: QuestionAnalyzer | None = None
        self.context_interpreter: ContextInterpreter | None = None

        self._initialize_nlu_components()

        logger.info(f"Initialized NLU engine for agent {agent_id}")

    def _initialize_nlu_components(self) -> None:
        """Initialize stateless NLU components based on configuration.

        Note: EntityTracker and ReferenceResolver are NOT initialized here.
        They are created fresh for each interpretation from NLUContext data.
        """
        try:
            # Dialogue act classifier (stateless)
            self.dialogue_act_classifier = DialogueActClassifier(
                DialogueActClassifierConfig(llm_config=self.llm_config)
            )

            # Question analyzer (stateless)
            self.question_analyzer = QuestionAnalyzer(
                QuestionAnalyzerConfig(llm_config=self.llm_config)
            )

            # Context interpreter (stateless - integrates other components)
            self.context_interpreter = ContextInterpreter(
                ContextInterpreterConfig(llm_config=self.llm_config)
            )

            logger.info("NLU components initialized successfully")

        except ValueError as e:
            logger.error(f"Failed to initialize NLU components: {e}")
            raise

    def interpret(
        self, utterance: str, speaker: str, state: InformationState
    ) -> list[DialogueMove]:
        """Interpret utterance using NLU.

        This overrides the base interpret() to use LLM-based NLU interpretation:
        1. Use context-aware interpretation to understand the utterance
        2. Classify the dialogue act
        3. Extract entities and resolve references
        4. Create appropriate DialogueMove objects

        Args:
            utterance: The utterance to interpret
            speaker: ID of the speaker
            state: Current information state

        Returns:
            List of interpreted dialogue moves
        """
        # Use empty NLU context for backwards compatibility
        nlu_context = NLUContext.create_empty()
        moves, _ = self.interpret_with_nlu_context(utterance, speaker, state, nlu_context)
        return moves

    def interpret_with_nlu_context(
        self, utterance: str, speaker: str, state: InformationState, nlu_context: NLUContext
    ) -> tuple[list[DialogueMove], NLUContext]:
        """Interpret utterance using NLU with explicit context management.

        This method accepts and returns NLUContext, enabling stateless engine design
        where NLU state (entities, references) is managed by Burr State.

        Args:
            utterance: The utterance to interpret
            speaker: ID of the speaker
            state: Current information state
            nlu_context: NLU context from previous turn

        Returns:
            Tuple of (dialogue moves, updated NLU context)
        """
        return self._interpret_with_nlu(utterance, speaker, state, nlu_context)

    def _interpret_with_nlu(
        self,
        utterance: str,
        speaker: str,
        state: InformationState,
        nlu_context: NLUContext,
    ) -> tuple[list[DialogueMove], NLUContext]:
        """Interpret utterance using NLU components.

        Args:
            utterance: The utterance to interpret
            speaker: ID of the speaker
            state: Current information state
            nlu_context: NLU context from previous turn

        Returns:
            Tuple of (dialogue moves, updated NLU context)
        """
        import time

        start_time = time.time()
        moves: list[DialogueMove] = []

        # Use context interpreter for comprehensive analysis
        if self.context_interpreter:
            interpretation = self.context_interpreter.interpret(utterance, state)

            # Track token usage and latency in NLU context
            nlu_context.last_interpretation_tokens = self.context_interpreter.last_tokens_used
            nlu_context.last_interpretation_latency = time.time() - start_time

            # Extract entities and update tracker (if available)
            if hasattr(interpretation, "entities") and interpretation.entities:
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

        return moves, nlu_context

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

        # Assertion
        elif dialogue_act == DialogueActType.ASSERTION.value:
            moves.append(
                DialogueMove(
                    move_type="assert",
                    content=utterance,
                    speaker=speaker,
                )
            )

        # Command
        elif dialogue_act == DialogueActType.COMMAND.value:
            moves.append(
                DialogueMove(
                    move_type="command",
                    content=utterance,
                    speaker=speaker,
                )
            )

        # Acknowledgment
        elif dialogue_act == DialogueActType.ACKNOWLEDGMENT.value:
            moves.append(
                DialogueMove(
                    move_type="acknowledge",
                    content=utterance,
                    speaker=speaker,
                )
            )

        # Clarification
        elif dialogue_act == DialogueActType.CLARIFICATION.value:
            moves.append(
                DialogueMove(
                    move_type="clarify",
                    content=utterance,
                    speaker=speaker,
                )
            )

        # Greeting
        elif dialogue_act == DialogueActType.GREETING.value:
            moves.append(
                DialogueMove(
                    move_type="greet",
                    content=utterance,
                    speaker=speaker,
                )
            )

        # Default: create generic move (includes OTHER and any unrecognized acts)
        else:
            moves.append(
                DialogueMove(
                    move_type="inform",
                    content=utterance,
                    speaker=speaker,
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

    def reset(self) -> None:
        """Reset the engine.

        Note: NLU context (entities, references) is now managed by Burr State,
        not by the engine. Callers should reset NLUContext separately if needed.
        """
        super().reset()

    def __str__(self) -> str:
        """Return string representation."""
        return (
            f"NLUDialogueEngine(agent={self.agent_id}, "
            f"model={self.config.llm_model.value}, "
            f"rules={self.rules.rule_count()})"
        )


def create_nlu_engine(
    agent_id: str,
    rules: RuleSet | None = None,
    config: NLUEngineConfig | None = None,
) -> NLUDialogueEngine:
    """Convenience function to create an NLU-enhanced dialogue engine.

    Args:
        agent_id: Unique identifier for the agent
        rules: Optional rule set
        config: Optional configuration (uses defaults if None)

    Returns:
        Configured NLUDialogueEngine

    Example:
        >>> engine = create_nlu_engine("agent_1")
        >>> state = engine.create_initial_state()
        >>> state, response = engine.process_input("Hello!", "user", state)
    """
    return NLUDialogueEngine(agent_id, rules=rules, config=config)
