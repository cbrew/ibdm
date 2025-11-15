"""Unit tests for NLUResult dataclass."""

import pytest

from ibdm.nlu.nlu_result import NLUResult


class TestNLUResult:
    """Test NLUResult dataclass."""

    def test_create_minimal(self) -> None:
        """Test creating NLUResult with minimal required fields."""
        result = NLUResult(dialogue_act="question", confidence=0.95)

        assert result.dialogue_act == "question"
        assert result.confidence == 0.95
        assert result.entities == []
        assert result.intent is None
        assert result.question_details is None
        assert result.answer_content is None
        assert result.raw_interpretation is None
        assert result.tokens_used == 0
        assert result.latency == 0.0

    def test_create_full(self) -> None:
        """Test creating NLUResult with all fields."""
        entities = [{"type": "person", "value": "Alice", "start": 0, "end": 5}]
        question_details = {
            "question_type": "wh",
            "focus": "what",
            "variable": "x",
        }

        result = NLUResult(
            dialogue_act="question",
            confidence=0.95,
            entities=entities,
            intent="get_weather",
            question_details=question_details,
            answer_content={"content": "Paris"},
            raw_interpretation={"full": "data"},
            tokens_used=150,
            latency=0.5,
        )

        assert result.dialogue_act == "question"
        assert result.confidence == 0.95
        assert result.entities == entities
        assert result.intent == "get_weather"
        assert result.question_details == question_details
        assert result.answer_content == {"content": "Paris"}
        assert result.raw_interpretation == {"full": "data"}
        assert result.tokens_used == 150
        assert result.latency == 0.5

    def test_to_dict_minimal(self) -> None:
        """Test serialization to dict with minimal fields."""
        result = NLUResult(dialogue_act="greet", confidence=0.99)

        data = result.to_dict()

        assert data["dialogue_act"] == "greet"
        assert data["confidence"] == 0.99
        assert data["entities"] == []
        assert data["intent"] is None
        assert data["question_details"] is None
        assert data["answer_content"] is None
        assert data["raw_interpretation"] is None
        assert data["tokens_used"] == 0
        assert data["latency"] == 0.0

    def test_to_dict_full(self) -> None:
        """Test serialization to dict with all fields."""
        entities = [{"type": "location", "value": "London"}]
        question_details = {"question_type": "yn", "proposition": "Is it raining?"}

        result = NLUResult(
            dialogue_act="question",
            confidence=0.87,
            entities=entities,
            intent="check_weather",
            question_details=question_details,
            tokens_used=200,
            latency=0.35,
        )

        data = result.to_dict()

        assert data["dialogue_act"] == "question"
        assert data["confidence"] == 0.87
        assert data["entities"] == entities
        assert data["intent"] == "check_weather"
        assert data["question_details"] == question_details
        assert data["tokens_used"] == 200
        assert data["latency"] == 0.35

    def test_from_dict_minimal(self) -> None:
        """Test deserialization from dict with minimal fields."""
        data = {
            "dialogue_act": "command",
            "confidence": 0.92,
        }

        result = NLUResult.from_dict(data)

        assert result.dialogue_act == "command"
        assert result.confidence == 0.92
        assert result.entities == []
        assert result.intent is None
        assert result.question_details is None
        assert result.answer_content is None
        assert result.raw_interpretation is None
        assert result.tokens_used == 0
        assert result.latency == 0.0

    def test_from_dict_full(self) -> None:
        """Test deserialization from dict with all fields."""
        data = {
            "dialogue_act": "answer",
            "confidence": 0.88,
            "entities": [{"type": "date", "value": "tomorrow"}],
            "intent": "schedule",
            "question_details": None,
            "answer_content": {"short": "yes", "long": "Yes, that works"},
            "raw_interpretation": {"sentiment": "positive"},
            "tokens_used": 175,
            "latency": 0.42,
        }

        result = NLUResult.from_dict(data)

        assert result.dialogue_act == "answer"
        assert result.confidence == 0.88
        assert result.entities == [{"type": "date", "value": "tomorrow"}]
        assert result.intent == "schedule"
        assert result.question_details is None
        assert result.answer_content == {"short": "yes", "long": "Yes, that works"}
        assert result.raw_interpretation == {"sentiment": "positive"}
        assert result.tokens_used == 175
        assert result.latency == 0.42

    def test_serialization_roundtrip_minimal(self) -> None:
        """Test serialization round-trip with minimal fields preserves data."""
        original = NLUResult(dialogue_act="quit", confidence=1.0)

        # Serialize to dict
        data = original.to_dict()

        # Deserialize from dict
        restored = NLUResult.from_dict(data)

        # Check equality
        assert restored.dialogue_act == original.dialogue_act
        assert restored.confidence == original.confidence
        assert restored.entities == original.entities
        assert restored.intent == original.intent
        assert restored.question_details == original.question_details
        assert restored.answer_content == original.answer_content
        assert restored.raw_interpretation == original.raw_interpretation
        assert restored.tokens_used == original.tokens_used
        assert restored.latency == original.latency

    def test_serialization_roundtrip_full(self) -> None:
        """Test serialization round-trip with all fields preserves data."""
        original = NLUResult(
            dialogue_act="question",
            confidence=0.91,
            entities=[{"type": "person", "value": "Bob"}],
            intent="book_flight",
            question_details={"type": "alt", "alternatives": ["Paris", "London"]},
            answer_content=None,
            raw_interpretation={"context": "travel"},
            tokens_used=250,
            latency=0.55,
        )

        # Serialize to dict
        data = original.to_dict()

        # Deserialize from dict
        restored = NLUResult.from_dict(data)

        # Check equality
        assert restored.dialogue_act == original.dialogue_act
        assert restored.confidence == original.confidence
        assert restored.entities == original.entities
        assert restored.intent == original.intent
        assert restored.question_details == original.question_details
        assert restored.answer_content == original.answer_content
        assert restored.raw_interpretation == original.raw_interpretation
        assert restored.tokens_used == original.tokens_used
        assert restored.latency == original.latency

    def test_str_representation_minimal(self) -> None:
        """Test string representation with minimal fields."""
        result = NLUResult(dialogue_act="greet", confidence=0.99)

        s = str(result)

        assert "greet" in s
        assert "0.99" in s
        assert "NLUResult" in s

    def test_str_representation_with_entities(self) -> None:
        """Test string representation with entities."""
        result = NLUResult(
            dialogue_act="question",
            confidence=0.85,
            entities=[{"type": "location"}, {"type": "date"}],
        )

        s = str(result)

        assert "question" in s
        assert "2 entities" in s

    def test_str_representation_with_intent(self) -> None:
        """Test string representation with intent."""
        result = NLUResult(
            dialogue_act="command",
            confidence=0.90,
            intent="book_ticket",
        )

        s = str(result)

        assert "command" in s
        assert "intent=book_ticket" in s

    def test_str_representation_with_question_details(self) -> None:
        """Test string representation with question details."""
        result = NLUResult(
            dialogue_act="question",
            confidence=0.88,
            question_details={"type": "wh"},
        )

        s = str(result)

        assert "question" in s
        assert "question_details" in s

    def test_str_representation_with_answer_content(self) -> None:
        """Test string representation with answer content."""
        result = NLUResult(
            dialogue_act="answer",
            confidence=0.93,
            answer_content={"content": "yes"},
        )

        s = str(result)

        assert "answer" in s
        assert "answer_content" in s

    def test_field_validation(self) -> None:
        """Test that required fields are validated."""
        # Should raise TypeError if required fields are missing
        with pytest.raises(TypeError):
            NLUResult()  # type: ignore[call-arg]

        with pytest.raises(TypeError):
            NLUResult(dialogue_act="ask")  # type: ignore[call-arg]

        with pytest.raises(TypeError):
            NLUResult(confidence=0.5)  # type: ignore[call-arg]
