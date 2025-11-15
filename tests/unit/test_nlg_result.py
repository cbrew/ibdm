"""Unit tests for NLGResult dataclass."""

import pytest

from ibdm.nlg.nlg_result import NLGResult


class TestNLGResult:
    """Test NLGResult dataclass."""

    def test_create_minimal(self) -> None:
        """Test creating NLGResult with minimal required fields."""
        result = NLGResult(utterance_text="Hello!", strategy="template")

        assert result.utterance_text == "Hello!"
        assert result.strategy == "template"
        assert result.generation_rule is None
        assert result.tokens_used == 0
        assert result.latency == 0.0
        assert result.metadata is None

    def test_create_full(self) -> None:
        """Test creating NLGResult with all fields."""
        metadata = {"template_name": "greeting", "variables": {"name": "Alice"}}

        result = NLGResult(
            utterance_text="What is the weather in Paris?",
            strategy="llm",
            generation_rule="generate_question",
            tokens_used=350,
            latency=0.65,
            metadata=metadata,
        )

        assert result.utterance_text == "What is the weather in Paris?"
        assert result.strategy == "llm"
        assert result.generation_rule == "generate_question"
        assert result.tokens_used == 350
        assert result.latency == 0.65
        assert result.metadata == metadata

    def test_to_dict_minimal(self) -> None:
        """Test serialization to dict with minimal fields."""
        result = NLGResult(utterance_text="Goodbye!", strategy="template")

        data = result.to_dict()

        assert data["utterance_text"] == "Goodbye!"
        assert data["strategy"] == "template"
        assert data["generation_rule"] is None
        assert data["tokens_used"] == 0
        assert data["latency"] == 0.0
        assert data["metadata"] is None

    def test_to_dict_full(self) -> None:
        """Test serialization to dict with all fields."""
        metadata = {"plan_items": ["introduce_topic", "ask_question"]}

        result = NLGResult(
            utterance_text="Let me help you with that.",
            strategy="plan_aware",
            generation_rule="respond_to_request",
            tokens_used=120,
            latency=0.25,
            metadata=metadata,
        )

        data = result.to_dict()

        assert data["utterance_text"] == "Let me help you with that."
        assert data["strategy"] == "plan_aware"
        assert data["generation_rule"] == "respond_to_request"
        assert data["tokens_used"] == 120
        assert data["latency"] == 0.25
        assert data["metadata"] == metadata

    def test_from_dict_minimal(self) -> None:
        """Test deserialization from dict with minimal fields."""
        data = {
            "utterance_text": "Yes.",
            "strategy": "template",
        }

        result = NLGResult.from_dict(data)

        assert result.utterance_text == "Yes."
        assert result.strategy == "template"
        assert result.generation_rule is None
        assert result.tokens_used == 0
        assert result.latency == 0.0
        assert result.metadata is None

    def test_from_dict_full(self) -> None:
        """Test deserialization from dict with all fields."""
        data = {
            "utterance_text": "The capital of France is Paris.",
            "strategy": "llm",
            "generation_rule": "answer_factual",
            "tokens_used": 450,
            "latency": 0.78,
            "metadata": {"model": "claude-sonnet-4-5", "temperature": 0.3},
        }

        result = NLGResult.from_dict(data)

        assert result.utterance_text == "The capital of France is Paris."
        assert result.strategy == "llm"
        assert result.generation_rule == "answer_factual"
        assert result.tokens_used == 450
        assert result.latency == 0.78
        assert result.metadata == {"model": "claude-sonnet-4-5", "temperature": 0.3}

    def test_serialization_roundtrip_minimal(self) -> None:
        """Test serialization round-trip with minimal fields preserves data."""
        original = NLGResult(utterance_text="OK.", strategy="template")

        # Serialize to dict
        data = original.to_dict()

        # Deserialize from dict
        restored = NLGResult.from_dict(data)

        # Check equality
        assert restored.utterance_text == original.utterance_text
        assert restored.strategy == original.strategy
        assert restored.generation_rule == original.generation_rule
        assert restored.tokens_used == original.tokens_used
        assert restored.latency == original.latency
        assert restored.metadata == original.metadata

    def test_serialization_roundtrip_full(self) -> None:
        """Test serialization round-trip with all fields preserves data."""
        original = NLGResult(
            utterance_text="I understand you want to book a flight to London.",
            strategy="plan_aware",
            generation_rule="acknowledge_intent",
            tokens_used=275,
            latency=0.42,
            metadata={"intent": "book_flight", "destination": "London"},
        )

        # Serialize to dict
        data = original.to_dict()

        # Deserialize from dict
        restored = NLGResult.from_dict(data)

        # Check equality
        assert restored.utterance_text == original.utterance_text
        assert restored.strategy == original.strategy
        assert restored.generation_rule == original.generation_rule
        assert restored.tokens_used == original.tokens_used
        assert restored.latency == original.latency
        assert restored.metadata == original.metadata

    def test_str_representation_minimal(self) -> None:
        """Test string representation with minimal fields."""
        result = NLGResult(utterance_text="Hi!", strategy="template")

        s = str(result)

        assert "strategy=template" in s
        assert "NLGResult" in s

    def test_str_representation_with_rule(self) -> None:
        """Test string representation with generation rule."""
        result = NLGResult(
            utterance_text="How can I help?",
            strategy="template",
            generation_rule="greet_user",
        )

        s = str(result)

        assert "strategy=template" in s
        assert "rule=greet_user" in s

    def test_str_representation_with_tokens(self) -> None:
        """Test string representation with tokens."""
        result = NLGResult(
            utterance_text="The weather is sunny.",
            strategy="llm",
            tokens_used=200,
        )

        s = str(result)

        assert "strategy=llm" in s
        assert "tokens=200" in s

    def test_str_representation_with_latency(self) -> None:
        """Test string representation with latency."""
        result = NLGResult(
            utterance_text="Let me check that for you.",
            strategy="plan_aware",
            latency=0.35,
        )

        s = str(result)

        assert "strategy=plan_aware" in s
        assert "latency=0.350s" in s

    def test_strategy_types(self) -> None:
        """Test that different strategy types are handled correctly."""
        # Template strategy
        template_result = NLGResult(
            utterance_text="Hello!",
            strategy="template",
        )
        assert template_result.strategy == "template"

        # Plan-aware strategy
        plan_result = NLGResult(
            utterance_text="Based on the plan...",
            strategy="plan_aware",
        )
        assert plan_result.strategy == "plan_aware"

        # LLM strategy
        llm_result = NLGResult(
            utterance_text="Generated by LLM...",
            strategy="llm",
        )
        assert llm_result.strategy == "llm"

    def test_field_validation(self) -> None:
        """Test that required fields are validated."""
        # Should raise TypeError if required fields are missing
        with pytest.raises(TypeError):
            NLGResult()  # type: ignore[call-arg]

        with pytest.raises(TypeError):
            NLGResult(utterance_text="Hi!")  # type: ignore[call-arg]

        with pytest.raises(TypeError):
            NLGResult(strategy="template")  # type: ignore[call-arg]

    def test_metadata_flexibility(self) -> None:
        """Test that metadata field can store various types of data."""
        # Empty metadata
        result1 = NLGResult(
            utterance_text="Text",
            strategy="template",
            metadata={},
        )
        assert result1.metadata == {}

        # Complex nested metadata
        result2 = NLGResult(
            utterance_text="Text",
            strategy="llm",
            metadata={
                "model_config": {
                    "temperature": 0.7,
                    "max_tokens": 1000,
                },
                "prompt_version": "v2.1",
                "retries": 0,
            },
        )
        assert result2.metadata is not None
        assert result2.metadata["model_config"]["temperature"] == 0.7
        assert result2.metadata["prompt_version"] == "v2.1"
