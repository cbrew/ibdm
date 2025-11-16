"""Abstract base class for NLU services defining IBiS requirements.

This module provides BaseNLUService, an abstract interface that captures all NLU
requirements from Larsson's IBiS1-4 dialogue management variants. It serves as:

1. **Specification**: Documents what NLU must provide for each IBiS level
2. **Contract**: Defines the interface between NLU and dialogue management
3. **Documentation**: Makes IBiS requirements explicit and testable

Each IBiS variant adds new NLU capabilities:
- IBiS1: Basic dialogue acts, questions, answers, entities
- IBiS2: Confidence scores, ambiguity detection, ICM moves
- IBiS3: Multi-fact extraction, volunteer information, semantic matching
- IBiS4: Action detection, preferences, negotiation

Reference: reports/ibis-nlu-requirements-analysis.md

Note on type checking:
This module uses flexible types (dict[str, Any], etc.) in dataclass definitions
to support abstract interface specifications. Implementations should use more
specific types.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ibdm.core.answers import Answer
    from ibdm.core.moves import DialogueMove
    from ibdm.core.questions import Question

from ibdm.core import InformationState


# ============================================================================
# Confidence and Metadata Types (IBiS2+)
# ============================================================================


@dataclass
class NLUConfidence:
    """NLU confidence scores for IBiS2 grounding support.

    IBiS2 requires NLU to report uncertainty to enable adaptive grounding:
    - High confidence → Optimistic grounding (assume understood)
    - Medium confidence → Cautious grounding (request confirmation)
    - Low confidence → Pessimistic grounding (request repetition)

    Attributes:
        perception: Speech recognition confidence (0.0-1.0)
        understanding: Semantic interpretation confidence (0.0-1.0)
        overall: Overall confidence score (typically min of perception and understanding)
    """

    perception: float = 1.0
    understanding: float = 1.0
    overall: float = 1.0

    @staticmethod
    def from_overall(confidence: float) -> NLUConfidence:
        """Create confidence from single overall score.

        Args:
            confidence: Overall confidence score

        Returns:
            NLUConfidence with all fields set to same value
        """
        return NLUConfidence(
            perception=confidence, understanding=confidence, overall=confidence
        )


def _empty_interp_list() -> list[dict[str, Any]]:
    """Factory for empty interpretations list."""
    return []


@dataclass
class AmbiguityInfo:
    """Information about ambiguous interpretations (IBiS2).

    IBiS2 requires NLU to detect and report ambiguity so the dialogue manager
    can generate appropriate clarification questions.

    Attributes:
        is_ambiguous: Whether the utterance has multiple valid interpretations
        ambiguity_type: Type of ambiguity (lexical, syntactic, semantic, referential)
        interpretations: List of possible interpretations (if ambiguous)
        preferred_interpretation: Index of most likely interpretation (if any)
    """

    is_ambiguous: bool = False
    ambiguity_type: str | None = None
    interpretations: list[dict[str, Any]] = field(default_factory=_empty_interp_list)
    preferred_interpretation: int | None = None


# ============================================================================
# Multi-Fact Extraction Types (IBiS3)
# ============================================================================


def _empty_question_list() -> list[Question]:
    """Factory for empty Question list."""
    return []


def _empty_fact_list() -> list[ExtractedFact]:
    """Factory for empty ExtractedFact list."""
    return []


@dataclass
class ExtractedFact:
    """A single fact extracted from an utterance (IBiS3).

    IBiS3 requires NLU to extract MULTIPLE facts from single utterances, enabling
    the dialogue manager to handle volunteer information.

    Example:
        User: "Acme and Smith, effective January 1, 2025"
        Facts:
        - ExtractedFact(predicate="parties", value=["Acme", "Smith"], is_volunteer=False)
        - ExtractedFact(predicate="effective_date", value="2025-01-01", is_volunteer=True)

    Attributes:
        predicate: Domain predicate this fact relates to (e.g., "parties", "effective_date")
        value: The extracted value
        is_volunteer: Whether this was volunteered (not directly asked about)
        confidence: Confidence in this extraction
        potential_questions: Questions this fact might answer
    """

    predicate: str
    value: str | list[str] | dict[str, Any]
    is_volunteer: bool = False
    confidence: float = 1.0
    potential_questions: list[Question] = field(default_factory=_empty_question_list)


@dataclass
class MultiFact:
    """Result of multi-fact extraction from utterance (IBiS3).

    Attributes:
        primary_fact: The fact directly answering the current question (if any)
        volunteer_facts: Additional facts volunteered by user
        all_facts: Complete list of all extracted facts
    """

    primary_fact: ExtractedFact | None = None
    volunteer_facts: list[ExtractedFact] = field(default_factory=_empty_fact_list)

    @property
    def all_facts(self) -> list[ExtractedFact]:
        """Get all facts (primary + volunteer)."""
        facts: list[ExtractedFact] = []
        if self.primary_fact:
            facts.append(self.primary_fact)
        facts.extend(self.volunteer_facts)
        return facts


# ============================================================================
# Action and Preference Types (IBiS4)
# ============================================================================


def _empty_params_dict() -> dict[str, Any]:
    """Factory for empty parameters dict."""
    return {}


class RequestType(Enum):
    """Types of action requests (IBiS4)."""

    EXPLICIT = "explicit"  # "Book the hotel"
    IMPLICIT = "implicit"  # "I want to go to Paris" → implies booking


@dataclass
class ActionRequest:
    """Extracted action request from utterance (IBiS4).

    IBiS4 requires NLU to detect when users request actions (not just information).

    Attributes:
        action: Action name (e.g., "book_hotel", "cancel_reservation")
        parameters: Action parameters
        request_type: Whether explicit or implicit
        confidence: Confidence in action detection
    """

    action: str
    parameters: dict[str, Any] = field(default_factory=_empty_params_dict)
    request_type: RequestType = RequestType.EXPLICIT
    confidence: float = 1.0


@dataclass
class UserPreference:
    """User preference or constraint extracted from utterance (IBiS4).

    IBiS4 requires NLU to extract preferences for negotiative dialogue.

    Attributes:
        dimension: What the preference is about (e.g., "price", "location")
        value: Preferred value or constraint (e.g., "< 200", "Paris")
        is_hard_constraint: Whether this is mandatory (True) or soft preference (False)
        priority: Relative priority if multiple preferences (higher = more important)
    """

    dimension: str
    value: Any
    is_hard_constraint: bool = True
    priority: int = 0


# ============================================================================
# Base NLU Service Interface
# ============================================================================


class BaseNLUService(ABC):
    """Abstract base class defining NLU requirements for IBiS dialogue management.

    This interface specifies what NLU must provide for each IBiS variant level:

    **IBiS1 Requirements** (Basic dialogue):
    - classify_dialogue_act()
    - parse_question()
    - parse_answer()
    - extract_entities()

    **IBiS2 Requirements** (Grounding):
    - get_confidence()
    - detect_ambiguity()
    - recognize_icm()

    **IBiS3 Requirements** (Accommodation):
    - extract_multiple_facts()
    - match_answer_to_question()
    - detect_volunteer_information()

    **IBiS4 Requirements** (Actions):
    - detect_action_request()
    - extract_preferences()
    - parse_comparison()

    Implementations can choose which levels to support. A minimal implementation
    only needs IBiS1 methods.
    """

    # ========================================================================
    # IBiS1: Core NLU Requirements (REQUIRED)
    # ========================================================================

    @abstractmethod
    def classify_dialogue_act(
        self, utterance: str, state: InformationState
    ) -> tuple[str, float]:
        """Classify utterance into dialogue act type (IBiS1 requirement).

        Dialogue act types from Larsson Section 2.4.1:
        - "ask" - User asks question
        - "answer" - User provides answer
        - "request" - User requests task/service
        - "assert" - User makes statement
        - "greet" - Conversation opening
        - "quit" - Conversation closing
        - "icm" - Interactive communication management (IBiS2)

        Args:
            utterance: User's utterance to classify
            state: Current dialogue state (for context)

        Returns:
            Tuple of (dialogue_act_type, confidence)

        Example:
            >>> act, conf = nlu.classify_dialogue_act("What are the parties?", state)
            >>> act
            "ask"
            >>> conf
            0.95
        """
        ...

    @abstractmethod
    def parse_question(
        self, utterance: str, state: InformationState
    ) -> tuple[Question | None, float]:
        """Parse utterance into structured Question object (IBiS1 requirement).

        Question types from Larsson Section 2.4.2:
        - WhQuestion - Wh-questions (what, who, when, where, why, how)
        - YNQuestion - Yes/no questions
        - AltQuestion - Alternative questions ("A or B?")

        Args:
            utterance: User's question utterance
            state: Current dialogue state

        Returns:
            Tuple of (Question object or None if not a question, confidence)

        Example:
            >>> q, conf = nlu.parse_question("What are the parties?", state)
            >>> q.predicate
            "parties"
            >>> q.type
            "wh"
        """
        ...

    @abstractmethod
    def parse_answer(
        self, utterance: str, state: InformationState
    ) -> tuple[Answer | None, float]:
        """Parse utterance into Answer object (IBiS1 requirement).

        Extracts answer content and associates with question from QUD if possible.

        Args:
            utterance: User's answer utterance
            state: Current dialogue state (contains QUD for context)

        Returns:
            Tuple of (Answer object or None if not an answer, confidence)

        Example:
            >>> ans, conf = nlu.parse_answer("Acme Corp and Smith Inc", state)
            >>> ans.content
            {"entities": [{"type": "ORGANIZATION", "value": "Acme Corp"}, ...]}
        """
        ...

    @abstractmethod
    def extract_entities(
        self, utterance: str, state: InformationState
    ) -> list[dict[str, Any]]:
        """Extract named entities from utterance (IBiS1 requirement).

        Entity types from NDA domain:
        - ORGANIZATION - "Acme Corp", "Smith Inc"
        - DATE - "January 1, 2025", "2025-01-01"
        - PERSON - "John Smith"
        - LOCATION - "California", "Delaware"
        - DURATION - "5 years", "12 months"

        Args:
            utterance: Utterance to extract entities from
            state: Current dialogue state

        Returns:
            List of entity dictionaries with 'type' and 'value' fields

        Example:
            >>> entities = nlu.extract_entities("Acme and Smith on Jan 1", state)
            >>> entities
            [
                {"type": "ORGANIZATION", "value": "Acme Corp"},
                {"type": "ORGANIZATION", "value": "Smith Inc"},
                {"type": "DATE", "value": "2025-01-01"}
            ]
        """
        ...

    # ========================================================================
    # IBiS2: Grounding & Confidence Requirements (OPTIONAL)
    # ========================================================================

    def get_confidence(
        self, utterance: str, state: InformationState
    ) -> NLUConfidence:
        """Get confidence scores for utterance interpretation (IBiS2 requirement).

        IBiS2 uses confidence scores to select grounding strategy:
        - > 0.9: Optimistic (assume grounded)
        - 0.6-0.9: Cautious (request confirmation)
        - < 0.6: Pessimistic (request repetition)

        Args:
            utterance: Utterance to assess
            state: Current dialogue state

        Returns:
            NLUConfidence with perception and understanding scores

        Note:
            Default implementation returns perfect confidence (1.0).
            IBiS2-compliant implementations should override this.
        """
        return NLUConfidence(perception=1.0, understanding=1.0, overall=1.0)

    def detect_ambiguity(
        self, utterance: str, state: InformationState
    ) -> AmbiguityInfo:
        """Detect if utterance has ambiguous interpretations (IBiS2 requirement).

        Ambiguity types:
        - Lexical: "bank" = financial institution or river edge
        - Syntactic: "I saw the man with the telescope"
        - Semantic: "the contract" - which contract?
        - Referential: "he" - who?

        Args:
            utterance: Utterance to check for ambiguity
            state: Current dialogue state

        Returns:
            AmbiguityInfo describing any detected ambiguity

        Note:
            Default implementation reports no ambiguity.
            IBiS2-compliant implementations should override this.
        """
        return AmbiguityInfo(is_ambiguous=False)

    def recognize_icm(
        self, utterance: str, state: InformationState
    ) -> tuple[str | None, float]:
        """Recognize Interactive Communication Management moves (IBiS2 requirement).

        ICM types from Larsson Section 3.4:
        - "icm:per*pos" - Positive perception ("I heard you")
        - "icm:per*neg" - Negative perception ("Sorry, I didn't hear that")
        - "icm:und*pos" - Positive understanding ("Yes, that's correct")
        - "icm:und*neg" - Negative understanding ("No, I said Paris")
        - "icm:und*int" - Understanding confirmation ("Paris, is that right?")

        Args:
            utterance: Utterance to check for ICM
            state: Current dialogue state

        Returns:
            Tuple of (ICM type or None if not ICM, confidence)

        Note:
            Default implementation returns None (no ICM detected).
            IBiS2-compliant implementations should override this.
        """
        return None, 0.0

    # ========================================================================
    # IBiS3: Accommodation Requirements (OPTIONAL)
    # ========================================================================

    def extract_multiple_facts(
        self, utterance: str, state: InformationState
    ) -> MultiFact:
        """Extract multiple facts from single utterance (IBiS3 requirement).

        IBiS3's key capability: handle volunteer information by extracting ALL facts
        from an utterance, not just the one directly answering the current question.

        Args:
            utterance: Utterance potentially containing multiple facts
            state: Current dialogue state (contains QUD, private.issues)

        Returns:
            MultiFact containing primary and volunteer facts

        Example:
            >>> # System asked: "What are the parties?"
            >>> # User said: "Acme and Smith, effective January 1, 2025"
            >>> mf = nlu.extract_multiple_facts(utterance, state)
            >>> mf.primary_fact.predicate
            "parties"
            >>> mf.volunteer_facts[0].predicate
            "effective_date"
            >>> mf.volunteer_facts[0].is_volunteer
            True

        Note:
            Default implementation extracts only one fact.
            IBiS3-compliant implementations should override this to extract multiple facts.
        """
        # Default: extract single fact from answer parser
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
        """Determine if answer resolves question (IBiS3 requirement).

        Implements the semantic operation resolves(answer, question) from Larsson
        Section 2.4.3.

        Args:
            answer: Answer to check
            question: Question that might be resolved
            state: Current dialogue state

        Returns:
            Confidence score (0.0-1.0) that answer resolves question

        Example:
            >>> # Answer "January 1, 2025" resolves WhQuestion(predicate="effective_date")
            >>> score = nlu.match_answer_to_question(date_answer, date_question, state)
            >>> score
            0.95

        Note:
            Default implementation uses simple heuristics.
            IBiS3-compliant implementations should use semantic understanding.
        """
        # Default: very simple matching
        # IBiS3 implementations should do semantic matching
        return 0.5

    def detect_volunteer_information(
        self, utterance: str, state: InformationState
    ) -> list[ExtractedFact]:
        """Detect information volunteered beyond current question (IBiS3 requirement).

        Identifies facts user provided that weren't explicitly asked about but might
        answer questions in private.issues or future plan questions.

        Args:
            utterance: User utterance
            state: Current dialogue state (contains QUD, private.issues, plan)

        Returns:
            List of volunteer facts detected

        Example:
            >>> # System asked: "What are the parties?"
            >>> # User said: "Acme and Smith, governed by California law"
            >>> facts = nlu.detect_volunteer_information(utterance, state)
            >>> facts[0].predicate
            "governing_law"
            >>> facts[0].is_volunteer
            True

        Note:
            Default implementation returns empty list.
            IBiS3-compliant implementations should detect volunteer information.
        """
        # Default: no volunteer detection
        # IBiS3 implementations should extract this
        return []

    # ========================================================================
    # IBiS4: Action & Negotiation Requirements (OPTIONAL)
    # ========================================================================

    def detect_action_request(
        self, utterance: str, state: InformationState
    ) -> tuple[ActionRequest | None, float]:
        """Detect if utterance requests an action (IBiS4 requirement).

        Distinguishes between:
        - Information-seeking: "What hotels are available?" → WhQuestion
        - Action request: "Book the Paris hotel" → ActionRequest

        Args:
            utterance: User utterance
            state: Current dialogue state

        Returns:
            Tuple of (ActionRequest or None, confidence)

        Example:
            >>> req, conf = nlu.detect_action_request("Book Hotel du Louvre", state)
            >>> req.action
            "book_hotel"
            >>> req.parameters
            {"hotel_id": "hotel_du_louvre"}

        Note:
            Default implementation returns None (no action detected).
            IBiS4-compliant implementations should override this.
        """
        return None, 0.0

    def extract_preferences(
        self, utterance: str, state: InformationState
    ) -> list[UserPreference]:
        """Extract user preferences and constraints (IBiS4 requirement).

        Identifies both hard constraints (must satisfy) and soft preferences (nice to have).

        Args:
            utterance: User utterance
            state: Current dialogue state

        Returns:
            List of extracted preferences

        Example:
            >>> # "I want a hotel in Paris under $200, close to Eiffel Tower"
            >>> prefs = nlu.extract_preferences(utterance, state)
            >>> prefs[0]
            UserPreference(dimension="max_price", value=200, is_hard_constraint=True)
            >>> prefs[1]
            UserPreference(dimension="proximity", value="Eiffel Tower", is_hard_constraint=False)

        Note:
            Default implementation returns empty list.
            IBiS4-compliant implementations should extract preferences.
        """
        return []

    def parse_comparison(
        self, utterance: str, alternatives: list[Any], state: InformationState
    ) -> tuple[str | None, list[Any]]:
        """Parse comparative question about alternatives (IBiS4 requirement).

        Handles negotiative dialogue where user compares options.

        Args:
            utterance: User utterance (e.g., "Which is cheaper?")
            alternatives: Available alternatives to compare
            state: Current dialogue state

        Returns:
            Tuple of (comparison dimension, filtered alternatives)

        Example:
            >>> # System: "Hotel A is $180, Hotel B is $150"
            >>> # User: "Which is closer to the Eiffel Tower?"
            >>> dim, alts = nlu.parse_comparison(utterance, [hotel_a, hotel_b], state)
            >>> dim
            "proximity_to_landmark"

        Note:
            Default implementation returns None.
            IBiS4-compliant implementations should parse comparisons.
        """
        return None, alternatives

    # ========================================================================
    # Integrated Processing
    # ========================================================================

    @abstractmethod
    def process(
        self, utterance: str, speaker: str, state: InformationState
    ) -> DialogueMove:
        """Process utterance and return DialogueMove (main entry point).

        This is the primary method called by the dialogue manager. It should:
        1. Classify dialogue act
        2. Extract appropriate content based on act type
        3. Include confidence and metadata
        4. Return structured DialogueMove

        The level of sophistication depends on which IBiS variant is supported:
        - IBiS1: Basic classification + entity extraction
        - IBiS2: + confidence + ambiguity detection
        - IBiS3: + multi-fact extraction + volunteer detection
        - IBiS4: + action detection + preference extraction

        Args:
            utterance: User's utterance
            speaker: Speaker ID
            state: Current information state

        Returns:
            DialogueMove with appropriate content and metadata

        Example:
            >>> move = nlu.process("What are the parties?", "user", state)
            >>> move.move_type
            "ask"
            >>> isinstance(move.content, Question)
            True
        """
        ...

    # ========================================================================
    # Utility Methods
    # ========================================================================

    def get_supported_ibis_level(self) -> str:
        """Return which IBiS level this implementation supports.

        Returns:
            One of: "IBiS1", "IBiS2", "IBiS3", "IBiS4"

        Note:
            Implementations should override this to indicate their capability level.
            Default is "IBiS1" (minimal required implementation).
        """
        return "IBiS1"

    def __str__(self) -> str:
        """Return string representation."""
        return f"{self.__class__.__name__}(level={self.get_supported_ibis_level()})"
