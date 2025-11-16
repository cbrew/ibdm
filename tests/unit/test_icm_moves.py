"""Unit tests for ICM (Interactive Communication Management) move types.

Tests IBiS2 grounding functionality based on Larsson (2002) Section 3.4.
"""

from ibdm.core import (
    DialogueMove,
    Polarity,
    WhQuestion,
    create_icm_acceptance_negative,
    create_icm_acceptance_positive,
    create_icm_perception_negative,
    create_icm_perception_positive,
    create_icm_understanding_interrogative,
    create_icm_understanding_negative,
    create_icm_understanding_positive,
)
from ibdm.core.grounding import ActionLevel


class TestPolarityEnum:
    """Tests for Polarity enum."""

    def test_polarity_values(self):
        """Test Polarity enum values."""
        assert Polarity.POSITIVE.value == "pos"
        assert Polarity.NEGATIVE.value == "neg"
        assert Polarity.INTERROGATIVE.value == "int"

    def test_polarity_from_value(self):
        """Test creating Polarity from value."""
        assert Polarity("pos") == Polarity.POSITIVE
        assert Polarity("neg") == Polarity.NEGATIVE
        assert Polarity("int") == Polarity.INTERROGATIVE


class TestDialogueMoveICMFields:
    """Tests for DialogueMove ICM-specific fields."""

    def test_create_basic_move(self):
        """Test creating basic (non-ICM) move works as before."""
        move = DialogueMove(move_type="greet", content="Hello", speaker="system")
        assert move.move_type == "greet"
        assert move.content == "Hello"
        assert move.speaker == "system"
        assert move.feedback_level is None
        assert move.polarity is None
        assert move.target_move_index is None

    def test_create_icm_move_with_fields(self):
        """Test creating ICM move with all fields."""
        move = DialogueMove(
            move_type="icm",
            content="I heard you",
            speaker="system",
            feedback_level=ActionLevel.PERCEPTION,
            polarity=Polarity.POSITIVE,
            target_move_index=5,
        )
        assert move.move_type == "icm"
        assert move.content == "I heard you"
        assert move.feedback_level == ActionLevel.PERCEPTION
        assert move.polarity == Polarity.POSITIVE
        assert move.target_move_index == 5

    def test_is_icm_true(self):
        """Test is_icm() returns True for ICM moves."""
        move = DialogueMove(move_type="icm", content="Okay", speaker="system")
        assert move.is_icm() is True

    def test_is_icm_false(self):
        """Test is_icm() returns False for non-ICM moves."""
        move = DialogueMove(move_type="ask", content="What?", speaker="user")
        assert move.is_icm() is False

    def test_get_icm_signature(self):
        """Test get_icm_signature() returns correct format."""
        move = DialogueMove(
            move_type="icm",
            content="Pardon?",
            speaker="system",
            feedback_level=ActionLevel.PERCEPTION,
            polarity=Polarity.NEGATIVE,
        )
        assert move.get_icm_signature() == "per*neg"

    def test_get_icm_signature_none_for_non_icm(self):
        """Test get_icm_signature() returns None for non-ICM moves."""
        move = DialogueMove(move_type="greet", content="Hi", speaker="user")
        assert move.get_icm_signature() is None

    def test_get_icm_signature_none_when_incomplete(self):
        """Test get_icm_signature() returns None when fields missing."""
        # ICM move but missing polarity
        move = DialogueMove(
            move_type="icm",
            content="test",
            speaker="system",
            feedback_level=ActionLevel.PERCEPTION,
        )
        assert move.get_icm_signature() is None

    def test_str_representation_icm(self):
        """Test string representation for ICM moves."""
        move = DialogueMove(
            move_type="icm",
            content="Okay",
            speaker="system",
            feedback_level=ActionLevel.ACCEPTANCE,
            polarity=Polarity.POSITIVE,
        )
        s = str(move)
        assert "icm:acc*pos" in s
        assert "Okay" in s

    def test_str_representation_non_icm(self):
        """Test string representation for non-ICM moves unchanged."""
        move = DialogueMove(move_type="greet", content="Hello", speaker="user")
        s = str(move)
        assert s == "user:greet(Hello)"


class TestICMSerialization:
    """Tests for ICM move serialization."""

    def test_to_dict_with_icm_fields(self):
        """Test serialization includes ICM fields."""
        move = DialogueMove(
            move_type="icm",
            content="I heard 'Paris'",
            speaker="system",
            feedback_level=ActionLevel.PERCEPTION,
            polarity=Polarity.POSITIVE,
            target_move_index=3,
        )
        data = move.to_dict()
        assert data["move_type"] == "icm"
        assert data["feedback_level"] == "per"
        assert data["polarity"] == "pos"
        assert data["target_move_index"] == 3

    def test_to_dict_without_icm_fields(self):
        """Test serialization without ICM fields (backward compatible)."""
        move = DialogueMove(move_type="greet", content="Hi", speaker="user")
        data = move.to_dict()
        assert "feedback_level" not in data
        assert "polarity" not in data
        assert "target_move_index" not in data

    def test_from_dict_with_icm_fields(self):
        """Test deserialization with ICM fields."""
        data = {
            "move_type": "icm",
            "content": "Pardon?",
            "speaker": "system",
            "timestamp": 123.456,
            "metadata": {},
            "feedback_level": "per",
            "polarity": "neg",
            "target_move_index": 2,
        }
        move = DialogueMove.from_dict(data)
        assert move.move_type == "icm"
        assert move.content == "Pardon?"
        assert move.feedback_level == ActionLevel.PERCEPTION
        assert move.polarity == Polarity.NEGATIVE
        assert move.target_move_index == 2

    def test_from_dict_without_icm_fields(self):
        """Test deserialization without ICM fields (backward compatible)."""
        data = {
            "move_type": "ask",
            "content": "What?",
            "speaker": "user",
            "timestamp": 123.456,
            "metadata": {},
        }
        move = DialogueMove.from_dict(data)
        assert move.move_type == "ask"
        assert move.feedback_level is None
        assert move.polarity is None
        assert move.target_move_index is None

    def test_roundtrip_serialization(self):
        """Test roundtrip serialization preserves ICM fields."""
        original = DialogueMove(
            move_type="icm",
            content="Paris, is that correct?",
            speaker="system",
            feedback_level=ActionLevel.UNDERSTANDING,
            polarity=Polarity.INTERROGATIVE,
            target_move_index=1,
        )
        data = original.to_dict()
        reconstructed = DialogueMove.from_dict(data)

        assert reconstructed.move_type == original.move_type
        assert reconstructed.content == original.content
        assert reconstructed.speaker == original.speaker
        assert reconstructed.feedback_level == original.feedback_level
        assert reconstructed.polarity == original.polarity
        assert reconstructed.target_move_index == original.target_move_index


class TestICMPerceptionFactories:
    """Tests for perception-level ICM factory functions."""

    def test_create_icm_perception_positive(self):
        """Test creating positive perception ICM (icm:per*pos)."""
        move = create_icm_perception_positive("I heard 'to Paris'", "system")
        assert move.move_type == "icm"
        assert move.content == "I heard 'to Paris'"
        assert move.speaker == "system"
        assert move.feedback_level == ActionLevel.PERCEPTION
        assert move.polarity == Polarity.POSITIVE
        assert move.get_icm_signature() == "per*pos"

    def test_create_icm_perception_positive_with_target(self):
        """Test creating per*pos with target_move_index."""
        move = create_icm_perception_positive("I heard you", "system", target_move_index=3)
        assert move.target_move_index == 3

    def test_create_icm_perception_negative(self):
        """Test creating negative perception ICM (icm:per*neg)."""
        move = create_icm_perception_negative("Pardon?", "system")
        assert move.move_type == "icm"
        assert move.content == "Pardon?"
        assert move.speaker == "system"
        assert move.feedback_level == ActionLevel.PERCEPTION
        assert move.polarity == Polarity.NEGATIVE
        assert move.get_icm_signature() == "per*neg"

    def test_create_icm_perception_negative_with_target(self):
        """Test creating per*neg with target_move_index."""
        move = create_icm_perception_negative(
            "Sorry, I didn't hear that", "system", target_move_index=1
        )
        assert move.target_move_index == 1


class TestICMUnderstandingFactories:
    """Tests for understanding-level ICM factory functions."""

    def test_create_icm_understanding_positive(self):
        """Test creating positive understanding ICM (icm:und*pos)."""
        q = WhQuestion(variable="x", predicate="destination(x)")
        move = create_icm_understanding_positive(q, "system")
        assert move.move_type == "icm"
        assert move.content == q
        assert move.speaker == "system"
        assert move.feedback_level == ActionLevel.UNDERSTANDING
        assert move.polarity == Polarity.POSITIVE
        assert move.get_icm_signature() == "und*pos"

    def test_create_icm_understanding_positive_string_content(self):
        """Test creating und*pos with string content."""
        move = create_icm_understanding_positive("Paris", "system")
        assert move.content == "Paris"
        assert move.get_icm_signature() == "und*pos"

    def test_create_icm_understanding_negative(self):
        """Test creating negative understanding ICM (icm:und*neg)."""
        move = create_icm_understanding_negative("I don't understand", "system")
        assert move.move_type == "icm"
        assert move.content == "I don't understand"
        assert move.feedback_level == ActionLevel.UNDERSTANDING
        assert move.polarity == Polarity.NEGATIVE
        assert move.get_icm_signature() == "und*neg"

    def test_create_icm_understanding_interrogative(self):
        """Test creating interrogative understanding ICM (icm:und*int)."""
        move = create_icm_understanding_interrogative("Paris, is that correct?", "system")
        assert move.move_type == "icm"
        assert move.content == "Paris, is that correct?"
        assert move.feedback_level == ActionLevel.UNDERSTANDING
        assert move.polarity == Polarity.INTERROGATIVE
        assert move.get_icm_signature() == "und*int"

    def test_create_icm_understanding_interrogative_with_question(self):
        """Test creating und*int with Question content."""
        q = WhQuestion(variable="x", predicate="destination(x)")
        move = create_icm_understanding_interrogative(q, "system", target_move_index=2)
        assert move.content == q
        assert move.target_move_index == 2
        assert move.get_icm_signature() == "und*int"


class TestICMAcceptanceFactories:
    """Tests for acceptance-level ICM factory functions."""

    def test_create_icm_acceptance_positive(self):
        """Test creating positive acceptance ICM (icm:acc*pos)."""
        move = create_icm_acceptance_positive("Okay", "system")
        assert move.move_type == "icm"
        assert move.content == "Okay"
        assert move.speaker == "system"
        assert move.feedback_level == ActionLevel.ACCEPTANCE
        assert move.polarity == Polarity.POSITIVE
        assert move.get_icm_signature() == "acc*pos"

    def test_create_icm_acceptance_positive_variations(self):
        """Test different acc*pos variations."""
        variations = ["Okay", "Good", "I'll do that", "Alright"]
        for content in variations:
            move = create_icm_acceptance_positive(content, "system")
            assert move.content == content
            assert move.get_icm_signature() == "acc*pos"

    def test_create_icm_acceptance_negative(self):
        """Test creating negative acceptance ICM (icm:acc*neg)."""
        move = create_icm_acceptance_negative("Sorry, I can't do that", "system")
        assert move.move_type == "icm"
        assert move.content == "Sorry, I can't do that"
        assert move.feedback_level == ActionLevel.ACCEPTANCE
        assert move.polarity == Polarity.NEGATIVE
        assert move.get_icm_signature() == "acc*neg"

    def test_create_icm_acceptance_negative_with_reason(self):
        """Test creating acc*neg with explanation."""
        content = "Sorry, Paris is not a valid destination"
        move = create_icm_acceptance_negative(content, "system", target_move_index=4)
        assert move.content == content
        assert move.target_move_index == 4
        assert move.get_icm_signature() == "acc*neg"


class TestICMIntegration:
    """Integration tests for ICM moves in dialogue scenarios."""

    def test_icm_dialogue_flow(self):
        """Test typical ICM dialogue flow.

        Based on Larsson (2002) example:
        User: "To Paris" (low confidence)
        System: "Paris, is that correct?" (icm:und*int)
        User: "Yes" (icm:acc*pos)
        """
        # User utterance (simulated with low confidence)
        user_move = DialogueMove(
            move_type="answer", content="To Paris", speaker="user", metadata={"confidence": 0.6}
        )

        # System requests confirmation
        system_confirmation = create_icm_understanding_interrogative(
            "Paris, is that correct?", "system", target_move_index=0
        )

        # User confirms
        user_confirmation = create_icm_acceptance_positive("Yes", "user", target_move_index=1)

        # Verify flow
        assert user_move.metadata["confidence"] == 0.6
        assert system_confirmation.get_icm_signature() == "und*int"
        assert user_confirmation.get_icm_signature() == "acc*pos"
        assert system_confirmation.target_move_index == 0  # References user move
        assert user_confirmation.target_move_index == 1  # References system confirmation

    def test_icm_perception_failure_flow(self):
        """Test ICM flow for perception failure.

        System: "What is your destination?"
        User: [garbled speech] (very low confidence)
        System: "Pardon?" (icm:per*neg)
        User: "Paris" (clear)
        System: "Paris" (icm:und*pos)
        """
        # Initial system question
        _system_question = DialogueMove(
            move_type="ask",
            content=WhQuestion(variable="x", predicate="destination(x)"),
            speaker="system",
        )

        # User utterance with low confidence
        _user_garbled = DialogueMove(
            move_type="answer", content="[garbled]", speaker="user", metadata={"confidence": 0.2}
        )

        # System perception negative
        system_per_neg = create_icm_perception_negative("Pardon?", "system", target_move_index=1)

        # User repeats clearly
        _user_clear = DialogueMove(
            move_type="answer", content="Paris", speaker="user", metadata={"confidence": 0.95}
        )

        # System understanding positive
        system_und_pos = create_icm_understanding_positive("Paris", "system", target_move_index=3)

        # Verify flow
        assert system_per_neg.get_icm_signature() == "per*neg"
        assert system_und_pos.get_icm_signature() == "und*pos"
        assert system_per_neg.target_move_index == 1  # References garbled utterance
        assert system_und_pos.target_move_index == 3  # References clear utterance

    def test_icm_serialization_in_dialogue(self):
        """Test that ICM moves can be serialized and deserialized in dialogue context."""
        # Create a sequence of moves
        moves = [
            DialogueMove(move_type="ask", content="What?", speaker="system"),
            DialogueMove(move_type="answer", content="Paris", speaker="user"),
            create_icm_understanding_interrogative("Paris?", "system", target_move_index=1),
            create_icm_acceptance_positive("Yes", "user", target_move_index=2),
        ]

        # Serialize all moves
        serialized = [m.to_dict() for m in moves]

        # Deserialize all moves
        deserialized = [DialogueMove.from_dict(d) for d in serialized]

        # Verify ICM moves preserved correctly
        assert deserialized[2].get_icm_signature() == "und*int"
        assert deserialized[2].target_move_index == 1
        assert deserialized[3].get_icm_signature() == "acc*pos"
        assert deserialized[3].target_move_index == 2
