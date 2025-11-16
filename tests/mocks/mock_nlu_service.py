"""Mock NLU Service for testing dialogue managers independently.

This module provides MockNLUService, a test-friendly implementation of BaseNLUService
that allows dialogue managers to be tested without requiring real LLM calls.

Key Features:
1. Configurable responses for test scenarios
2. Pattern-based simple heuristics for basic tests
3. Support for IBiS1-3 features (can be configured to different levels)
4. No LLM dependencies - fast and deterministic

Usage:
    >>> mock_nlu = MockNLUService()
    >>> mock_nlu.configure_response(
    ...     utterance="Acme and Smith",
    ...     dialogue_act="answer",
    ...     confidence=1.0,
    ...     entities=[{"type": "ORGANIZATION", "value": "Acme Corp"}]
    ... )
    >>> act, conf = mock_nlu.classify_dialogue_act("Acme and Smith", state)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ibdm.core.answers import Answer
    from ibdm.core.questions import Question

from ibdm.core import DialogueMove, InformationState
from ibdm.core.answers import Answer as AnswerClass
from ibdm.core.questions import WhQuestion, YNQuestion
from ibdm.nlu.base_nlu_service import (
    BaseNLUService,
    ExtractedFact,
    MultiFact,
    NLUConfidence,
)


class MockNLUService(BaseNLUService):
    """Mock NLU service for testing dialogue managers.

    This implementation provides simple pattern-based NLU without LLM dependencies.
    Tests can configure specific responses for utterances, or rely on heuristics.

    IBiS Support Level: Configurable (IBiS1 by default)
    - ✅ IBiS1: Basic dialogue acts, questions, answers, entities
    - ⚠️  IBiS2: Partial (confidence only)
    - ✅ IBiS3: Multi-fact extraction (when configured)
    - ❌ IBiS4: Not implemented

    Example:
        >>> mock = MockNLUService()
        >>> entities = [{"type": "ORG", "value": "Acme Corp"}]
        >>> mock.configure_response("Acme Corp", "answer", entities=entities)
        >>> act, conf = mock.classify_dialogue_act("Acme Corp", state)
    """

    def __init__(self, ibis_level: str = "IBiS1"):
        """Initialize mock NLU service.

        Args:
            ibis_level: Which IBiS level to simulate ("IBiS1", "IBiS2", "IBiS3")
        """
        self.ibis_level = ibis_level
        self._configured_responses: dict[str, dict[str, Any]] = {}
        self._default_confidence = 1.0

    # ========================================================================
    # Configuration Methods (for tests)
    # ========================================================================

    def configure_response(
        self,
        utterance: str,
        dialogue_act: str,
        confidence: float = 1.0,
        entities: list[dict[str, Any]] | None = None,
        question: Question | None = None,
        answer: Answer | None = None,
        multi_fact: MultiFact | None = None,
    ) -> None:
        """Configure mock response for specific utterance.

        Args:
            utterance: Utterance to configure response for
            dialogue_act: Dialogue act to return
            confidence: Confidence score
            entities: Entities to extract
            question: Question object (for ask dialogue acts)
            answer: Answer object (for answer dialogue acts)
            multi_fact: MultiFact for IBiS3 multi-fact extraction
        """
        self._configured_responses[utterance.lower()] = {
            "dialogue_act": dialogue_act,
            "confidence": confidence,
            "entities": entities or [],
            "question": question,
            "answer": answer,
            "multi_fact": multi_fact,
        }

    def clear_responses(self) -> None:
        """Clear all configured responses."""
        self._configured_responses.clear()

    def set_default_confidence(self, confidence: float) -> None:
        """Set default confidence for heuristic responses.

        Args:
            confidence: Default confidence (0.0-1.0)
        """
        self._default_confidence = confidence

    # ========================================================================
    # IBiS1: Core NLU Requirements (REQUIRED)
    # ========================================================================

    def classify_dialogue_act(self, utterance: str, state: InformationState) -> tuple[str, float]:
        """Classify utterance using configured responses or heuristics.

        Args:
            utterance: User's utterance
            state: Current dialogue state

        Returns:
            Tuple of (dialogue_act_type, confidence)
        """
        # Check configured responses first
        if utterance.lower() in self._configured_responses:
            response = self._configured_responses[utterance.lower()]
            return response["dialogue_act"], response["confidence"]

        # Heuristic classification
        utterance_lower = utterance.lower()

        # Questions: start with wh-words or end with ?
        if (
            any(
                utterance_lower.startswith(w)
                for w in ["what", "who", "when", "where", "why", "how"]
            )
            or "?" in utterance
        ):
            return "ask", self._default_confidence

        # Greetings
        if any(g in utterance_lower for g in ["hello", "hi", "hey"]):
            return "greet", self._default_confidence

        # Quit signals
        if any(q in utterance_lower for q in ["bye", "goodbye", "quit", "exit"]):
            return "quit", self._default_confidence

        # Commands (imperative verbs)
        if any(utterance_lower.startswith(v) for v in ["create", "make", "draft", "help"]):
            return "request", self._default_confidence

        # If there's a QUD, assume it's an answer
        if state.shared.qud:
            return "answer", self._default_confidence

        # Default: inform
        return "inform", self._default_confidence

    def parse_question(
        self, utterance: str, state: InformationState
    ) -> tuple[Question | None, float]:
        """Parse question using configured responses or heuristics.

        Args:
            utterance: Question utterance
            state: Current dialogue state

        Returns:
            Tuple of (Question or None, confidence)
        """
        # Check configured responses
        if utterance.lower() in self._configured_responses:
            response = self._configured_responses[utterance.lower()]
            if response["question"]:
                return response["question"], response["confidence"]

        # Heuristic parsing
        act, conf = self.classify_dialogue_act(utterance, state)
        if act != "ask":
            return None, 0.0

        # Extract predicate from wh-questions
        predicate = utterance
        for wh in ["what", "who", "when", "where", "why", "how"]:
            if utterance.lower().startswith(wh):
                # Try to extract the focus (e.g., "What are the parties?" → "parties")
                words = utterance.lower().split()
                if len(words) > 3:  # e.g., "what are the parties"
                    predicate = words[-1].rstrip("?")
                break

        # Yes/no questions
        if "?" in utterance and not any(
            utterance.lower().startswith(w) for w in ["what", "who", "when", "where", "why", "how"]
        ):
            return YNQuestion(proposition=utterance), conf

        # Default: WhQuestion
        return WhQuestion(variable="x", predicate=predicate, constraints={}), conf

    def parse_answer(self, utterance: str, state: InformationState) -> tuple[Answer | None, float]:
        """Parse answer using configured responses or heuristics.

        Args:
            utterance: Answer utterance
            state: Current dialogue state

        Returns:
            Tuple of (Answer or None, confidence)
        """
        # Check configured responses
        if utterance.lower() in self._configured_responses:
            response = self._configured_responses[utterance.lower()]
            if response["answer"]:
                return response["answer"], response["confidence"]

        # Heuristic parsing
        act, conf = self.classify_dialogue_act(utterance, state)
        if act not in ["answer", "inform"]:
            return None, 0.0

        # Get top QUD
        top_qud = state.shared.top_qud()

        # Create answer
        answer = AnswerClass(content=utterance, question_ref=top_qud)
        return answer, conf

    def extract_entities(self, utterance: str, state: InformationState) -> list[dict[str, Any]]:
        """Extract entities using configured responses or heuristics.

        Args:
            utterance: Utterance to extract from
            state: Current dialogue state

        Returns:
            List of entity dictionaries
        """
        # Check configured responses
        if utterance.lower() in self._configured_responses:
            response = self._configured_responses[utterance.lower()]
            return response["entities"]

        # Simple heuristic: look for capitalized words (organizations/people)
        entities: list[dict[str, Any]] = []
        words = utterance.split()

        for word in words:
            # Capitalized words might be organizations or people
            if word and word[0].isupper() and word not in ["I", "The", "A", "An"]:
                entities.append(
                    {
                        "type": "ORGANIZATION",
                        "value": word,
                    }
                )

        return entities

    # ========================================================================
    # IBiS2: Grounding & Confidence Requirements (PARTIAL)
    # ========================================================================

    def get_confidence(self, utterance: str, state: InformationState) -> NLUConfidence:
        """Return configured or default confidence.

        Args:
            utterance: Utterance to assess
            state: Current dialogue state

        Returns:
            NLUConfidence with scores
        """
        # Check configured responses
        if utterance.lower() in self._configured_responses:
            response = self._configured_responses[utterance.lower()]
            conf = response["confidence"]
            return NLUConfidence.from_overall(conf)

        return NLUConfidence.from_overall(self._default_confidence)

    # ========================================================================
    # IBiS3: Accommodation Requirements (OPTIONAL)
    # ========================================================================

    def extract_multiple_facts(self, utterance: str, state: InformationState) -> MultiFact:
        """Extract multiple facts (IBiS3 capability).

        Args:
            utterance: Utterance with potential multiple facts
            state: Current dialogue state

        Returns:
            MultiFact containing primary and volunteer facts
        """
        # Check configured responses
        if utterance.lower() in self._configured_responses:
            response = self._configured_responses[utterance.lower()]
            if response["multi_fact"]:
                return response["multi_fact"]

        # Default: single fact from answer parser
        answer, conf = self.parse_answer(utterance, state)
        if answer:
            primary = ExtractedFact(
                predicate="unknown",
                value=answer.content,
                is_volunteer=False,
                confidence=conf,
            )
            return MultiFact(primary_fact=primary, volunteer_facts=[])

        return MultiFact()

    def match_answer_to_question(
        self, answer: Answer, question: Question, state: InformationState
    ) -> float:
        """Simple matching heuristic (IBiS3 capability).

        Args:
            answer: Answer to check
            question: Question to match against
            state: Current dialogue state

        Returns:
            Match confidence (0.0-1.0)
        """
        # Simple heuristic: if answer references this question, high confidence
        if answer.question_ref == question:
            return 1.0

        # Check if question predicate appears in answer content
        answer_str = str(answer.content).lower()
        question_str = str(question).lower()

        if any(word in answer_str for word in question_str.split() if len(word) > 3):
            return 0.7

        return 0.3

    # ========================================================================
    # Main Entry Point
    # ========================================================================

    def process(self, utterance: str, speaker: str, state: InformationState) -> DialogueMove:
        """Process utterance and return DialogueMove.

        Args:
            utterance: User's utterance
            speaker: Speaker ID
            state: Current information state

        Returns:
            DialogueMove with content and metadata
        """
        # Classify
        act, conf = self.classify_dialogue_act(utterance, state)

        # Build content
        content: Any = utterance
        metadata: dict[str, Any] = {"confidence": conf}

        if act == "ask":
            question, q_conf = self.parse_question(utterance, state)
            if question:
                content = question
                metadata["confidence"] = q_conf

        elif act in ["answer", "inform"]:
            answer, a_conf = self.parse_answer(utterance, state)
            if answer:
                content = answer
                metadata["confidence"] = a_conf

        # Extract entities
        entities = self.extract_entities(utterance, state)
        metadata["entities"] = entities

        return DialogueMove(
            move_type=act,
            content=content,
            speaker=speaker,
            metadata=metadata,
        )

    # ========================================================================
    # Utility Methods
    # ========================================================================

    def get_supported_ibis_level(self) -> str:
        """Return configured IBiS level.

        Returns:
            IBiS level string
        """
        return self.ibis_level


def create_mock_nlu(ibis_level: str = "IBiS1") -> MockNLUService:
    """Convenience function to create mock NLU service.

    Args:
        ibis_level: IBiS level to simulate

    Returns:
        Configured MockNLUService

    Example:
        >>> mock_nlu = create_mock_nlu("IBiS3")
        >>> mock_nlu.configure_response("Acme and Smith, effective Jan 1", ...)
    """
    return MockNLUService(ibis_level=ibis_level)
