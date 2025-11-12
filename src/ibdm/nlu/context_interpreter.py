"""Context-aware interpretation pipeline for IBDM.

This module provides an end-to-end NLU pipeline that uses dialogue context
(Information State, QUD stack, commitments, history) to perform context-sensitive
interpretation, detect conversational implicatures, and track topics.
"""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from ibdm.core.information_state import InformationState
from ibdm.nlu.answer_parser import AnswerParser, AnswerParserConfig
from ibdm.nlu.dialogue_act_classifier import DialogueActClassifier, DialogueActClassifierConfig
from ibdm.nlu.llm_adapter import LLMAdapter, LLMConfig, ModelType
from ibdm.nlu.question_analyzer import QuestionAnalyzer, QuestionAnalyzerConfig
from ibdm.nlu.semantic_parser import SemanticParser, SemanticParserConfig

logger = logging.getLogger(__name__)


class TopicShiftType(str, Enum):
    """Types of topic shifts in dialogue."""

    NONE = "none"  # No topic shift
    CONTINUATION = "continuation"  # Continuation of current topic
    REFINEMENT = "refinement"  # Refinement/clarification of current topic
    RETURN = "return"  # Return to previous topic
    SHIFT = "shift"  # New topic introduced


class ImplicatureType(str, Enum):
    """Types of conversational implicatures."""

    NONE = "none"
    INDIRECT_REQUEST = "indirect_request"  # Request phrased as question
    PRESUPPOSITION = "presupposition"  # Assumed information
    SCALAR_IMPLICATURE = "scalar_implicature"  # "Some" implies "not all"
    RELEVANCE_IMPLICATURE = "relevance_implicature"  # Implied by relevance
    MANNER_IMPLICATURE = "manner_implicature"  # Implied by how it's said


class ContextualInterpretation(BaseModel):
    """Full contextual interpretation of an utterance.

    Attributes:
        utterance: The original utterance
        dialogue_act: The identified dialogue act
        semantic_parse: Structured semantic representation
        topic: Current topic
        topic_shift: Type of topic shift detected
        implicatures: List of detected implicatures
        context_used: Summary of context used in interpretation
        confidence: Overall confidence in interpretation
    """

    utterance: str = Field(..., description="Original utterance")
    dialogue_act: str = Field(..., description="Dialogue act type")
    semantic_parse: dict[str, Any] = Field(..., description="Semantic parse structure")
    topic: str | None = Field(default=None, description="Current topic")
    topic_shift: str = Field(default="none", description="Type of topic shift")
    implicatures: list[dict[str, str]] = Field(
        default_factory=list, description="Detected implicatures"
    )
    context_used: dict[str, Any] = Field(
        default_factory=dict, description="Context information used"
    )
    confidence: float = Field(..., ge=0.0, le=1.0, description="Overall confidence")


@dataclass
class ContextInterpreterConfig:
    """Configuration for context interpreter.

    Attributes:
        llm_config: Configuration for the LLM adapter
        use_semantic_parser: Enable semantic parsing
        use_dialogue_act_classifier: Enable dialogue act classification
        use_question_analyzer: Enable question analysis
        use_answer_parser: Enable answer parsing
        detect_implicatures: Enable implicature detection
        track_topics: Enable topic tracking
        confidence_threshold: Minimum confidence for interpretations
    """

    llm_config: LLMConfig | None = None
    use_semantic_parser: bool = True
    use_dialogue_act_classifier: bool = True
    use_question_analyzer: bool = True
    use_answer_parser: bool = True
    detect_implicatures: bool = True
    track_topics: bool = True
    confidence_threshold: float = 0.5


class ContextInterpreter:
    """Context-aware interpretation pipeline.

    Integrates all NLU components and uses dialogue context from InformationState
    to perform sophisticated interpretation including:
    - Context-sensitive semantic parsing
    - Dialogue act classification
    - Question understanding
    - Answer parsing and QUD matching
    - Conversational implicature detection
    - Topic tracking and shift detection

    Example:
        >>> interpreter = ContextInterpreter()
        >>> state = InformationState()
        >>> interpretation = interpreter.interpret("What's the weather?", state)
        >>> print(interpretation.dialogue_act)
        'question'
        >>> print(interpretation.topic)
        'weather'
    """

    def __init__(self, config: ContextInterpreterConfig | None = None):
        """Initialize the context interpreter.

        Args:
            config: Interpreter configuration. Uses defaults if not provided.
        """
        self.config = config or ContextInterpreterConfig()

        # Initialize LLM adapter
        llm_config = self.config.llm_config or LLMConfig(
            model=ModelType.SONNET,  # Use Sonnet for complex interpretation
            temperature=0.5,
            max_tokens=4000,
        )
        self.llm = LLMAdapter(llm_config)

        # Initialize NLU components
        self.semantic_parser = (
            SemanticParser(SemanticParserConfig(llm_config=llm_config))
            if self.config.use_semantic_parser
            else None
        )

        self.dialogue_act_classifier = (
            DialogueActClassifier(DialogueActClassifierConfig(llm_config=llm_config))
            if self.config.use_dialogue_act_classifier
            else None
        )

        self.question_analyzer = (
            QuestionAnalyzer(QuestionAnalyzerConfig(llm_config=llm_config))
            if self.config.use_question_analyzer
            else None
        )

        self.answer_parser = (
            AnswerParser(AnswerParserConfig(llm_config=llm_config))
            if self.config.use_answer_parser
            else None
        )

        # Topic tracking state
        self.current_topic: str | None = None
        self.topic_history: list[str] = []

        logger.info("Context interpreter initialized with all components")

    def interpret(
        self, utterance: str, information_state: InformationState
    ) -> ContextualInterpretation:
        """Interpret an utterance using dialogue context.

        Args:
            utterance: The utterance to interpret
            information_state: Current dialogue state providing context

        Returns:
            Full contextual interpretation including semantic parse, dialogue act,
            topic information, and detected implicatures

        Raises:
            ValueError: If utterance is empty
        """
        if not utterance or not utterance.strip():
            raise ValueError("Utterance cannot be empty")

        logger.info(f"Interpreting utterance with context: '{utterance}'")

        # Extract context information
        context_summary = self._extract_context_summary(information_state)

        # Run NLU components
        dialogue_act = self._classify_dialogue_act(utterance, context_summary)
        semantic_parse = self._parse_semantics(utterance, context_summary)

        # Topic analysis
        topic, topic_shift = self._analyze_topic(
            utterance, semantic_parse, context_summary, dialogue_act
        )

        # Implicature detection
        implicatures = (
            self._detect_implicatures(utterance, semantic_parse, context_summary, dialogue_act)
            if self.config.detect_implicatures
            else []
        )

        # Calculate overall confidence
        confidence = self._calculate_confidence(semantic_parse, dialogue_act, topic)

        interpretation = ContextualInterpretation(
            utterance=utterance,
            dialogue_act=dialogue_act,
            semantic_parse=semantic_parse,
            topic=topic,
            topic_shift=topic_shift,
            implicatures=implicatures,
            context_used=context_summary,
            confidence=confidence,
        )

        logger.info(
            f"Interpretation complete: act={dialogue_act}, topic={topic}, "
            f"shift={topic_shift}, confidence={confidence:.2f}"
        )

        return interpretation

    def _extract_context_summary(self, state: InformationState) -> dict[str, Any]:
        """Extract relevant context from information state.

        Args:
            state: Current information state

        Returns:
            Dictionary with context summary including QUD stack, commitments, history
        """
        context = {
            "qud_stack": [],
            "qud_top": None,
            "commitments": list(state.shared.commitments),
            "recent_moves": [],
            "current_topic": self.current_topic,
            "topic_history": self.topic_history[-5:],  # Last 5 topics
        }

        # Extract QUD information
        if state.shared.qud:
            context["qud_stack"] = [str(q) for q in state.shared.qud]
            context["qud_top"] = str(state.shared.qud[-1])

        # Extract recent dialogue moves
        if state.shared.last_moves:
            context["recent_moves"] = [
                {"type": str(type(m).__name__), "content": str(m)}
                for m in state.shared.last_moves[-3:]  # Last 3 moves
            ]

        return context

    def _classify_dialogue_act(self, utterance: str, context: dict[str, Any]) -> str:
        """Classify dialogue act with context.

        Args:
            utterance: The utterance to classify
            context: Context summary

        Returns:
            Dialogue act type as string
        """
        if not self.dialogue_act_classifier:
            return "unknown"

        try:
            result = self.dialogue_act_classifier.classify(utterance)
            return result.act
        except Exception as e:
            logger.warning(f"Dialogue act classification failed: {e}")
            return "unknown"

    def _parse_semantics(self, utterance: str, context: dict[str, Any]) -> dict[str, Any]:
        """Parse semantics with context.

        Args:
            utterance: The utterance to parse
            context: Context summary

        Returns:
            Semantic parse as dictionary
        """
        if not self.semantic_parser:
            return {"predicate": "unknown", "arguments": [], "modifiers": []}

        try:
            result = self.semantic_parser.parse(utterance)
            return {
                "predicate": result.predicate,
                "arguments": [{"role": arg.role, "value": arg.value} for arg in result.arguments],
                "modifiers": [{"type": mod.type, "value": mod.value} for mod in result.modifiers],
            }
        except Exception as e:
            logger.warning(f"Semantic parsing failed: {e}")
            return {"predicate": "unknown", "arguments": [], "modifiers": []}

    def _analyze_topic(
        self,
        utterance: str,
        semantic_parse: dict[str, Any],
        context: dict[str, Any],
        dialogue_act: str,
    ) -> tuple[str | None, str]:
        """Analyze topic and detect topic shifts.

        Args:
            utterance: The utterance
            semantic_parse: Semantic parse result
            context: Context summary
            dialogue_act: Dialogue act type

        Returns:
            Tuple of (current_topic, topic_shift_type)
        """
        if not self.config.track_topics:
            return None, TopicShiftType.NONE.value

        try:
            # Extract topic from semantic parse (typically the main predicate or object)
            topic = self._extract_topic_from_parse(semantic_parse)

            # Determine topic shift type
            shift_type = self._determine_topic_shift(topic, context)

            # Update topic tracking
            if topic and topic != self.current_topic:
                if self.current_topic:
                    self.topic_history.append(self.current_topic)
                self.current_topic = topic

            return topic, shift_type

        except Exception as e:
            logger.warning(f"Topic analysis failed: {e}")
            return None, TopicShiftType.NONE.value

    def _extract_topic_from_parse(self, semantic_parse: dict[str, Any]) -> str | None:
        """Extract topic from semantic parse.

        Args:
            semantic_parse: Semantic parse result

        Returns:
            Topic string or None
        """
        predicate = semantic_parse.get("predicate")
        if not predicate or predicate == "unknown":
            return None

        # For simple cases, use the predicate as the topic
        # In more sophisticated implementations, we could analyze arguments
        # to extract domain entities or themes
        return predicate

    def _determine_topic_shift(self, new_topic: str | None, context: dict[str, Any]) -> str:
        """Determine type of topic shift.

        Args:
            new_topic: The newly identified topic
            context: Context summary

        Returns:
            Topic shift type
        """
        if not new_topic:
            return TopicShiftType.NONE.value

        current_topic = context.get("current_topic")
        topic_history = context.get("topic_history", [])

        # No previous topic - first topic
        if not current_topic:
            return TopicShiftType.SHIFT.value

        # Same topic - continuation
        if new_topic == current_topic:
            return TopicShiftType.CONTINUATION.value

        # Return to previous topic
        if new_topic in topic_history:
            return TopicShiftType.RETURN.value

        # Check if related topic (refinement)
        # Simple heuristic: substring match or shared words
        if self._topics_related(new_topic, current_topic):
            return TopicShiftType.REFINEMENT.value

        # New topic - shift
        return TopicShiftType.SHIFT.value

    def _topics_related(self, topic1: str, topic2: str) -> bool:
        """Check if two topics are related.

        Args:
            topic1: First topic
            topic2: Second topic

        Returns:
            True if topics are related
        """
        # Simple heuristic: check for common words or substrings
        t1_words = set(topic1.lower().split("_"))
        t2_words = set(topic2.lower().split("_"))

        # Topics are related if they share words
        return len(t1_words & t2_words) > 0

    def _detect_implicatures(
        self,
        utterance: str,
        semantic_parse: dict[str, Any],
        context: dict[str, Any],
        dialogue_act: str,
    ) -> list[dict[str, str]]:
        """Detect conversational implicatures.

        Args:
            utterance: The utterance
            semantic_parse: Semantic parse result
            context: Context summary
            dialogue_act: Dialogue act type

        Returns:
            List of detected implicatures with type and description
        """
        implicatures = []

        # Detect indirect requests (questions that are actually requests)
        if dialogue_act == "question" and self._is_indirect_request(utterance):
            implicatures.append(
                {
                    "type": ImplicatureType.INDIRECT_REQUEST.value,
                    "description": "Question functioning as indirect request",
                }
            )

        # Detect presuppositions from questions
        presuppositions = self._extract_presuppositions(utterance, semantic_parse)
        for presup in presuppositions:
            implicatures.append(
                {
                    "type": ImplicatureType.PRESUPPOSITION.value,
                    "description": f"Presupposes: {presup}",
                }
            )

        # Detect relevance implicatures based on context
        if context.get("qud_top") and dialogue_act == "assertion":
            implicatures.append(
                {
                    "type": ImplicatureType.RELEVANCE_IMPLICATURE.value,
                    "description": f"Relevant to current question: {context['qud_top']}",
                }
            )

        return implicatures

    def _is_indirect_request(self, utterance: str) -> bool:
        """Check if utterance is an indirect request.

        Args:
            utterance: The utterance

        Returns:
            True if likely an indirect request
        """
        # Simple heuristic: questions starting with "can you", "could you", "would you"
        lower = utterance.lower().strip()
        indirect_markers = ["can you", "could you", "would you", "will you", "can i", "may i"]

        return any(lower.startswith(marker) for marker in indirect_markers)

    def _extract_presuppositions(self, utterance: str, semantic_parse: dict[str, Any]) -> list[str]:
        """Extract presuppositions from utterance.

        Args:
            utterance: The utterance
            semantic_parse: Semantic parse result

        Returns:
            List of presupposition descriptions
        """
        presuppositions = []

        # Detect definite descriptions ("the X") which presuppose existence
        if " the " in utterance.lower():
            # Simple heuristic - more sophisticated NLP could be used
            presuppositions.append("Existence of definite entity")

        # Detect factive verbs (know, realize, discover) which presuppose truth
        factive_verbs = ["know", "realize", "discover", "aware", "learned"]
        predicate = semantic_parse.get("predicate", "").lower()
        if any(verb in predicate for verb in factive_verbs):
            presuppositions.append("Truth of embedded proposition")

        return presuppositions

    def _calculate_confidence(
        self, semantic_parse: dict[str, Any], dialogue_act: str, topic: str | None
    ) -> float:
        """Calculate overall confidence in interpretation.

        Args:
            semantic_parse: Semantic parse result
            dialogue_act: Dialogue act type
            topic: Identified topic

        Returns:
            Confidence score between 0 and 1
        """
        # Simple confidence calculation based on completeness
        scores = []

        # Semantic parse confidence
        if semantic_parse.get("predicate") and semantic_parse["predicate"] != "unknown":
            scores.append(0.8)
        else:
            scores.append(0.3)

        # Dialogue act confidence
        if dialogue_act and dialogue_act != "unknown":
            scores.append(0.9)
        else:
            scores.append(0.4)

        # Topic confidence
        if topic:
            scores.append(0.7)
        else:
            scores.append(0.5)

        return sum(scores) / len(scores) if scores else 0.5


def create_interpreter(
    use_semantic_parser: bool = True,
    use_dialogue_act_classifier: bool = True,
    detect_implicatures: bool = True,
    track_topics: bool = True,
) -> ContextInterpreter:
    """Convenience function to create a context interpreter.

    Args:
        use_semantic_parser: Enable semantic parsing
        use_dialogue_act_classifier: Enable dialogue act classification
        detect_implicatures: Enable implicature detection
        track_topics: Enable topic tracking

    Returns:
        Configured ContextInterpreter instance

    Example:
        >>> # Full-featured interpreter
        >>> interpreter = create_interpreter()
        >>>
        >>> # Minimal interpreter
        >>> interpreter = create_interpreter(detect_implicatures=False, track_topics=False)
    """
    config = ContextInterpreterConfig(
        use_semantic_parser=use_semantic_parser,
        use_dialogue_act_classifier=use_dialogue_act_classifier,
        detect_implicatures=detect_implicatures,
        track_topics=track_topics,
    )

    return ContextInterpreter(config)
