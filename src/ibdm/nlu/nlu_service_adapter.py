"""Adapter wrapping NLUEngine as BaseNLUService for IBiS dialogue management.

This adapter bridges the existing NLUEngine implementation to the BaseNLUService
interface, enabling:
1. Standardized NLU access across dialogue managers
2. Testing with mock NLU implementations
3. Progressive enhancement (IBiS1 → IBiS3 → IBiS2 → IBiS4)

Current Status: IBiS1 support (basic dialogue)
Future: Will be enhanced to IBiS3 for accommodation features
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ibdm.core.answers import Answer
    from ibdm.core.questions import Question

from ibdm.core import DialogueMove, InformationState
from ibdm.core.answers import Answer as AnswerClass
from ibdm.core.questions import AltQuestion, WhQuestion, YNQuestion
from ibdm.nlu.base_nlu_service import (
    BaseNLUService,
    NLUConfidence,
)
from ibdm.nlu.nlu_context import NLUContext
from ibdm.nlu.nlu_engine import NLUEngine, NLUEngineConfig
from ibdm.nlu.nlu_result import NLUResult

logger = logging.getLogger(__name__)


class NLUServiceAdapter(BaseNLUService):
    """Adapter wrapping NLUEngine as BaseNLUService implementation.

    This adapter provides IBiS1-level NLU capabilities by wrapping the existing
    NLUEngine. It serves as the bridge between the current NLU implementation
    and the BaseNLUService interface.

    IBiS Support Level: IBiS1 (basic dialogue)
    - ✅ Dialogue act classification
    - ✅ Question parsing
    - ✅ Answer parsing
    - ✅ Entity extraction
    - ⚠️  IBiS2 grounding (partial - confidence only)
    - ❌ IBiS3 accommodation (not yet implemented)
    - ❌ IBiS4 actions (not yet implemented)

    Example:
        >>> config = NLUEngineConfig()
        >>> nlu_service = NLUServiceAdapter(config)
        >>> act, conf = nlu_service.classify_dialogue_act("What are the parties?", state)
        >>> act
        "question"
    """

    def __init__(self, config: NLUEngineConfig | None = None):
        """Initialize the NLU service adapter.

        Args:
            config: NLU engine configuration (uses defaults if None)
        """
        self.config = config or NLUEngineConfig()
        self.engine = NLUEngine(self.config)

        # Track last NLU result for context
        self.last_result: NLUResult | None = None
        self.nlu_context = NLUContext.create_empty()

        logger.info("Initialized NLUServiceAdapter (IBiS1 support)")

    # ========================================================================
    # IBiS1: Core NLU Requirements (REQUIRED)
    # ========================================================================

    def classify_dialogue_act(self, utterance: str, state: InformationState) -> tuple[str, float]:
        """Classify utterance into dialogue act type (IBiS1 requirement).

        Args:
            utterance: User's utterance to classify
            state: Current dialogue state

        Returns:
            Tuple of (dialogue_act_type, confidence)
        """
        # Use NLUEngine's process method
        result, self.nlu_context = self.engine.process(utterance, "user", state, self.nlu_context)
        self.last_result = result

        # Map NLU result dialogue act to IBiS act types
        act_type = self._map_dialogue_act(result.dialogue_act)
        return act_type, result.confidence

    def parse_question(
        self, utterance: str, state: InformationState
    ) -> tuple[Question | None, float]:
        """Parse utterance into structured Question object (IBiS1 requirement).

        Args:
            utterance: User's question utterance
            state: Current dialogue state

        Returns:
            Tuple of (Question object or None, confidence)
        """
        # Process if we don't have a recent result
        if not self.last_result:
            result, self.nlu_context = self.engine.process(
                utterance, "user", state, self.nlu_context
            )
            self.last_result = result
        else:
            result = self.last_result

        # Check if it's a question
        if result.dialogue_act not in ["question", "ask"]:
            return None, 0.0

        # Extract question details if available
        if result.question_details:
            question = self._build_question_from_details(result.question_details, utterance)
            return question, result.confidence

        # Fallback: create generic WhQuestion
        return WhQuestion(variable="x", predicate=utterance, constraints={}), result.confidence

    def parse_answer(self, utterance: str, state: InformationState) -> tuple[Answer | None, float]:
        """Parse utterance into Answer object (IBiS1 requirement).

        Args:
            utterance: User's answer utterance
            state: Current dialogue state

        Returns:
            Tuple of (Answer object or None, confidence)
        """
        # Process if we don't have a recent result
        if not self.last_result:
            result, self.nlu_context = self.engine.process(
                utterance, "user", state, self.nlu_context
            )
            self.last_result = result
        else:
            result = self.last_result

        # Check if it's an answer
        if result.dialogue_act not in ["answer", "inform"]:
            return None, 0.0

        # Get top question from QUD
        top_qud = state.shared.top_qud()

        # Extract answer content
        content = utterance
        if result.answer_content:
            content = result.answer_content.get("content", utterance)

        # Create Answer object
        answer = AnswerClass(content=content, question_ref=top_qud)
        return answer, result.confidence

    def extract_entities(self, utterance: str, state: InformationState) -> list[dict[str, Any]]:
        """Extract named entities from utterance (IBiS1 requirement).

        Args:
            utterance: Utterance to extract entities from
            state: Current dialogue state

        Returns:
            List of entity dictionaries with 'type' and 'value' fields
        """
        # Process if we don't have a recent result
        if not self.last_result:
            result, self.nlu_context = self.engine.process(
                utterance, "user", state, self.nlu_context
            )
            self.last_result = result
        else:
            result = self.last_result

        return result.entities

    # ========================================================================
    # IBiS2: Grounding & Confidence Requirements (PARTIAL)
    # ========================================================================

    def get_confidence(self, utterance: str, state: InformationState) -> NLUConfidence:
        """Get confidence scores for utterance interpretation (IBiS2 requirement).

        Note:
            Current implementation only has overall confidence from NLUEngine.
            Full IBiS2 support would require separate perception and understanding
            confidence scores.

        Args:
            utterance: Utterance to assess
            state: Current dialogue state

        Returns:
            NLUConfidence with perception and understanding scores
        """
        # Process if we don't have a recent result
        if not self.last_result:
            result, self.nlu_context = self.engine.process(
                utterance, "user", state, self.nlu_context
            )
            self.last_result = result
        else:
            result = self.last_result

        # Use overall confidence for all fields (partial IBiS2 support)
        return NLUConfidence.from_overall(result.confidence)

    # ========================================================================
    # Main Entry Point
    # ========================================================================

    def process(self, utterance: str, speaker: str, state: InformationState) -> DialogueMove:
        """Process utterance and return DialogueMove (main entry point).

        Args:
            utterance: User's utterance
            speaker: Speaker ID
            state: Current information state

        Returns:
            DialogueMove with appropriate content and metadata
        """
        # Clear last result to force fresh processing
        self.last_result = None

        # Process utterance
        result, self.nlu_context = self.engine.process(utterance, speaker, state, self.nlu_context)
        self.last_result = result

        # Map to dialogue act type
        act_type = self._map_dialogue_act(result.dialogue_act)

        # Build move content based on act type
        content: Any = utterance
        metadata: dict[str, Any] = {
            "confidence": result.confidence,
            "entities": result.entities,
        }

        if act_type == "ask" and result.question_details:
            question = self._build_question_from_details(result.question_details, utterance)
            content = question
            metadata["question_type"] = result.question_details.get("question_type")

        elif act_type == "answer":
            top_qud = state.shared.top_qud()
            answer_text = utterance
            if result.answer_content:
                answer_text = result.answer_content.get("content", utterance)
            content = AnswerClass(content=answer_text, question_ref=top_qud)

        return DialogueMove(
            move_type=act_type,
            content=content,
            speaker=speaker,
            metadata=metadata,
        )

    # ========================================================================
    # Utility Methods
    # ========================================================================

    def get_supported_ibis_level(self) -> str:
        """Return which IBiS level this implementation supports.

        Returns:
            "IBiS1" (basic dialogue support)
        """
        return "IBiS1"

    def _map_dialogue_act(self, act: str) -> str:
        """Map NLU result dialogue act to IBiS act type.

        Args:
            act: Dialogue act from NLU result

        Returns:
            IBiS-compatible act type
        """
        # Map common variations
        act_map = {
            "question": "ask",
            "command": "request",
            "acknowledgment": "acknowledge",
            "clarification": "clarify",
            "greeting": "greet",
            "assertion": "assert",
            "other": "inform",
        }
        return act_map.get(act, act)

    def _build_question_from_details(self, details: dict[str, Any], utterance: str) -> Question:
        """Build Question object from question details.

        Args:
            details: Question details from NLU result
            utterance: Original utterance

        Returns:
            Appropriate Question subclass
        """
        q_type = details.get("question_type", "wh")
        variable = details.get("variable", "x")
        focus = details.get("focus", utterance)

        if q_type == "wh":
            return WhQuestion(variable=variable, predicate=focus, constraints={})
        elif q_type in ["yes-no", "yes_no", "yn"]:
            return YNQuestion(proposition=utterance)
        elif q_type in ["alternative", "alt"]:
            alternatives = details.get("alternatives", [])
            return AltQuestion(alternatives=alternatives)
        else:
            # Default to WhQuestion
            return WhQuestion(variable=variable, predicate=focus, constraints={})


def create_nlu_service(config: NLUEngineConfig | None = None) -> NLUServiceAdapter:
    """Convenience function to create NLU service adapter.

    Args:
        config: Optional NLU configuration

    Returns:
        Configured NLUServiceAdapter

    Example:
        >>> nlu_service = create_nlu_service()
        >>> move = nlu_service.process("What are the parties?", "user", state)
    """
    return NLUServiceAdapter(config)
