"""NLU Engine for natural language understanding.

This module provides a standalone NLU engine that processes utterances and returns
structured NLU results, separating NLU from dialogue move creation.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Any

from ibdm.burr_integration.nlu_context import NLUContext
from ibdm.core import InformationState
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
)
from ibdm.nlu.nlu_result import NLUResult

logger = logging.getLogger(__name__)


@dataclass
class NLUEngineConfig:
    """Configuration for NLU engine.

    Attributes:
        llm_model: Which LLM model to use (defaults to Sonnet per Policy #9)
        confidence_threshold: Minimum confidence for NLU results
        temperature: LLM temperature for generation
        max_tokens: Maximum tokens for LLM responses
    """

    llm_model: ModelType = ModelType.SONNET
    confidence_threshold: float = 0.5
    temperature: float = 0.3
    max_tokens: int = 2000


class NLUEngine:
    """Standalone NLU engine for natural language understanding.

    This engine performs NLU processing on utterances and returns structured
    NLU results. It is stateless - all state is managed via NLUContext which
    is passed in and returned.

    The engine performs:
    - Dialogue act classification
    - Entity extraction
    - Question analysis (for questions)
    - Answer parsing (for answers)
    - Intent classification (for commands)
    - Reference resolution

    Example:
        >>> config = NLUEngineConfig()
        >>> engine = NLUEngine(config)
        >>> context = NLUContext.create_empty()
        >>> result, updated_context = engine.process("What's the weather?", "user", state, context)
        >>> print(result.dialogue_act)
        "question"
    """

    def __init__(self, config: NLUEngineConfig | None = None):
        """Initialize the NLU engine.

        Args:
            config: NLU configuration (uses defaults if None)
        """
        self.config = config or NLUEngineConfig()

        # Store LLM config for creating components
        self.llm_config = LLMConfig(
            model=self.config.llm_model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
        )

        # Initialize stateless NLU components
        self.dialogue_act_classifier: DialogueActClassifier | None = None
        self.question_analyzer: QuestionAnalyzer | None = None
        self.context_interpreter: ContextInterpreter | None = None

        self._initialize_components()

        logger.info("Initialized NLU engine")

    def _initialize_components(self) -> None:
        """Initialize NLU components."""
        try:
            # Dialogue act classifier
            self.dialogue_act_classifier = DialogueActClassifier(
                DialogueActClassifierConfig(llm_config=self.llm_config)
            )

            # Question analyzer
            self.question_analyzer = QuestionAnalyzer(
                QuestionAnalyzerConfig(llm_config=self.llm_config)
            )

            # Context interpreter (integrates other components)
            self.context_interpreter = ContextInterpreter(
                ContextInterpreterConfig(llm_config=self.llm_config)
            )

            logger.info("NLU components initialized successfully")

        except ValueError as e:
            logger.error(f"Failed to initialize NLU components: {e}")
            raise

    def process(
        self,
        utterance: str,
        speaker: str,
        state: InformationState,
        nlu_context: NLUContext,
    ) -> tuple[NLUResult, NLUContext]:
        """Process utterance and return NLU result.

        This is the main entry point for NLU processing. It performs dialogue act
        classification, entity extraction, and dialogue-act-specific analysis.

        Args:
            utterance: The utterance to process
            speaker: ID of the speaker
            state: Current information state (for context)
            nlu_context: NLU context from previous turn

        Returns:
            Tuple of (NLU result, updated NLU context)
        """
        start_time = time.time()

        # Use context interpreter for comprehensive analysis
        if self.context_interpreter:
            interpretation = self.context_interpreter.interpret(utterance, state)

            # Build NLU result from interpretation
            nlu_result = self._build_result_from_interpretation(
                interpretation, utterance, start_time
            )

            # Update NLU context with tokens and latency
            nlu_context.last_interpretation_tokens = self.context_interpreter.last_tokens_used
            nlu_context.last_interpretation_latency = time.time() - start_time

            # Extract and store entities in context (if available)
            entities_attr = getattr(interpretation, "entities", None)
            if entities_attr:
                # Serialize entities to dicts for storage
                entity_dicts: list[dict[str, Any]] = []  # type: ignore[reportUnknownVariableType]
                for entity in entities_attr:
                    if hasattr(entity, "model_dump"):
                        entity_dicts.append(entity.model_dump())
                    elif hasattr(entity, "__dict__"):
                        entity_dicts.append(dict(entity.__dict__))
                    else:
                        entity_dicts.append({"raw": str(entity)})
                nlu_context.entities.extend(entity_dicts)
                logger.debug(f"Extracted {len(entity_dicts)} entities")

            return nlu_result, nlu_context

        # Fallback: use dialogue act classifier only
        if self.dialogue_act_classifier:
            act_result = self.dialogue_act_classifier.classify(utterance)
            dialogue_act_str = getattr(act_result, "dialogue_act", DialogueActType.OTHER.value)
            confidence_val = getattr(act_result, "confidence", 0.0)

            if confidence_val >= self.config.confidence_threshold:
                nlu_result = NLUResult(
                    dialogue_act=dialogue_act_str,
                    confidence=confidence_val,
                    latency=time.time() - start_time,
                )
                return nlu_result, nlu_context

        # No classification possible - return generic result
        nlu_result = NLUResult(
            dialogue_act=DialogueActType.OTHER.value,
            confidence=0.0,
            latency=time.time() - start_time,
        )
        return nlu_result, nlu_context

    def _build_result_from_interpretation(
        self, interpretation: Any, utterance: str, start_time: float
    ) -> NLUResult:
        """Build NLUResult from context interpreter output.

        Args:
            interpretation: Result from context interpreter
            utterance: Original utterance
            start_time: Processing start time

        Returns:
            Structured NLU result
        """
        # Extract basic classification
        dialogue_act_val = getattr(interpretation, "dialogue_act", DialogueActType.OTHER.value)
        dialogue_act = dialogue_act_val if dialogue_act_val else DialogueActType.OTHER.value
        confidence = getattr(interpretation, "confidence", 0.0)

        # Extract entities (if available)
        entities: list[dict[str, Any]] = []  # type: ignore[reportUnknownVariableType]
        entities_attr = getattr(interpretation, "entities", None)
        if entities_attr:
            for entity in entities_attr:
                if hasattr(entity, "model_dump"):
                    entities.append(entity.model_dump())
                elif hasattr(entity, "__dict__"):
                    entities.append(dict(entity.__dict__))
                else:
                    entities.append({"raw": str(entity)})

        # Extract intent (for commands)
        intent = None
        if dialogue_act == DialogueActType.COMMAND.value:
            intent = getattr(interpretation, "intent", None)

        # Extract question details (for questions)
        question_details = None
        if dialogue_act == DialogueActType.QUESTION.value:
            if hasattr(interpretation, "question_analysis"):
                qa = interpretation.question_analysis
                question_details = {
                    "question_type": getattr(qa, "question_type", "unknown"),
                    "focus": getattr(qa, "focus", None),
                    "variable": getattr(qa, "variable", None),
                    "alternatives": getattr(qa, "alternatives", None),
                    "confidence": getattr(qa, "confidence", 0.0),
                }

        # Extract answer content (for answers)
        answer_content = None
        if dialogue_act == DialogueActType.ANSWER.value:
            if hasattr(interpretation, "answer_analysis"):
                aa = interpretation.answer_analysis
                answer_content = {
                    "content": getattr(aa, "content", utterance),
                    "answer_type": getattr(aa, "answer_type", "unknown"),
                }

        # Build result
        return NLUResult(
            dialogue_act=dialogue_act,
            confidence=confidence,
            entities=entities,
            intent=intent,
            question_details=question_details,
            answer_content=answer_content,
            raw_interpretation=self._serialize_interpretation(interpretation),
            tokens_used=getattr(self.context_interpreter, "last_tokens_used", 0)
            if self.context_interpreter
            else 0,
            latency=time.time() - start_time,
        )

    def _serialize_interpretation(self, interpretation: Any) -> dict[str, Any]:
        """Serialize interpretation for storage.

        Args:
            interpretation: Interpretation result

        Returns:
            Dictionary representation
        """
        try:
            # Try Pydantic model_dump first
            if hasattr(interpretation, "model_dump"):
                return interpretation.model_dump()
            # Try dict() for dataclasses
            elif hasattr(interpretation, "__dict__"):
                return dict(interpretation.__dict__)
            else:
                return {"raw": str(interpretation)}
        except Exception as e:
            logger.warning(f"Failed to serialize interpretation: {e}")
            return {"error": str(e)}

    def update_context(self, nlu_result: NLUResult, nlu_context: NLUContext) -> NLUContext:
        """Update NLU context with results.

        This method is for explicit context updates if needed. The process() method
        already updates context automatically.

        Args:
            nlu_result: NLU result to incorporate
            nlu_context: Current NLU context

        Returns:
            Updated NLU context
        """
        # Add entities to context if not already there
        for entity in nlu_result.entities:
            if entity not in nlu_context.entities:
                nlu_context.entities.append(entity)

        # Update tokens and latency
        nlu_context.last_interpretation_tokens = nlu_result.tokens_used
        nlu_context.last_interpretation_latency = nlu_result.latency

        return nlu_context

    def __str__(self) -> str:
        """Return string representation."""
        return f"NLUEngine(model={self.config.llm_model.value})"


def create_nlu_engine(config: NLUEngineConfig | None = None) -> NLUEngine:
    """Convenience function to create an NLU engine.

    Args:
        config: Optional configuration (uses defaults if None)

    Returns:
        Configured NLUEngine

    Example:
        >>> engine = create_nlu_engine()
        >>> context = NLUContext.create_empty()
        >>> result, context = engine.process("Hello!", "user", state, context)
    """
    return NLUEngine(config)
