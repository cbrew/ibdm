"""Tests for dialogue act classifier module."""

import pytest

from ibdm.nlu.dialogue_act_classifier import (
    DialogueActClassifier,
    DialogueActClassifierConfig,
    DialogueActResult,
    DialogueActType,
    create_classifier,
)


class TestDialogueActResult:
    """Tests for DialogueActResult Pydantic model."""

    def test_create_result(self):
        """Test creating a dialogue act result."""
        result = DialogueActResult(act="question", confidence=0.95)

        assert result.act == "question"
        assert result.confidence == 0.95

    def test_to_enum(self):
        """Test converting act string to enum."""
        result = DialogueActResult(act="question", confidence=0.9)
        assert result.to_enum() == DialogueActType.QUESTION

        result = DialogueActResult(act="answer", confidence=0.85)
        assert result.to_enum() == DialogueActType.ANSWER

    def test_to_enum_unknown(self):
        """Test converting unknown act to enum defaults to OTHER."""
        result = DialogueActResult(act="unknown_type", confidence=0.5)
        assert result.to_enum() == DialogueActType.OTHER

    def test_confidence_validation(self):
        """Test confidence score validation."""
        # Valid confidence
        result = DialogueActResult(act="question", confidence=0.5)
        assert result.confidence == 0.5

        # Confidence must be between 0 and 1
        with pytest.raises(Exception):  # Pydantic validation error
            DialogueActResult(act="question", confidence=1.5)


class TestDialogueActClassifierConfig:
    """Tests for DialogueActClassifierConfig."""

    def test_default_config(self):
        """Test default configuration."""
        config = DialogueActClassifierConfig()

        assert config.llm_config is None
        assert config.confidence_threshold == 0.5
        assert config.use_fast_model is True  # Default to Haiku for speed

    def test_custom_config(self):
        """Test custom configuration."""
        config = DialogueActClassifierConfig(confidence_threshold=0.8, use_fast_model=False)

        assert config.confidence_threshold == 0.8
        assert config.use_fast_model is False


@pytest.mark.skipif(
    "not config.getoption('--run-llm')",
    reason="Requires --run-llm flag and IBDM_API_KEY",
)
class TestDialogueActClassifier:
    """Tests for DialogueActClassifier (requires LLM API)."""

    def test_classifier_initialization(self):
        """Test classifier can be initialized."""
        classifier = DialogueActClassifier()
        assert classifier is not None
        assert classifier.llm is not None
        assert classifier.template is not None

    def test_classify_question(self):
        """Test classifying a question."""
        classifier = create_classifier(use_fast_model=True)

        result = classifier.classify("What's the weather like tomorrow?")

        assert result.act == "question"
        assert result.confidence > 0.5

    def test_classify_answer(self):
        """Test classifying an answer."""
        classifier = create_classifier(use_fast_model=True)

        result = classifier.classify("It will be sunny with a high of 75 degrees.")

        assert result.act == "answer"
        assert result.confidence > 0.5

    def test_classify_command(self):
        """Test classifying a command."""
        classifier = create_classifier(use_fast_model=True)

        result = classifier.classify("Please close the door.")

        assert result.act == "command"
        assert result.confidence > 0.5

    def test_classify_acknowledgment(self):
        """Test classifying an acknowledgment."""
        classifier = create_classifier(use_fast_model=True)

        result = classifier.classify("I understand, I'll take care of it.")

        assert result.act == "acknowledgment"
        assert result.confidence > 0.5

    def test_is_high_confidence(self):
        """Test high confidence checking."""
        classifier = DialogueActClassifier(DialogueActClassifierConfig(confidence_threshold=0.7))

        high_conf = DialogueActResult(act="question", confidence=0.9)
        low_conf = DialogueActResult(act="question", confidence=0.5)

        assert classifier.is_high_confidence(high_conf) is True
        assert classifier.is_high_confidence(low_conf) is False

    @pytest.mark.asyncio
    async def test_async_classify(self):
        """Test async classification."""
        classifier = create_classifier(use_fast_model=True)

        result = await classifier.aclassify("What time is it?")

        assert result.act == "question"
        assert result.confidence > 0.5

    @pytest.mark.asyncio
    async def test_batch_classify(self):
        """Test batch classification."""
        classifier = create_classifier(use_fast_model=True)

        utterances = [
            "What's the weather?",
            "It's sunny.",
            "Please open the window.",
            "Okay, will do.",
        ]

        results = await classifier.batch_classify(utterances)

        assert len(results) == 4
        assert results[0].act == "question"
        assert results[1].act == "answer"
        assert results[2].act == "command"
        assert results[3].act == "acknowledgment"


class TestCreateClassifier:
    """Tests for create_classifier convenience function."""

    def test_create_fast_classifier(self):
        """Test creating a classifier with fast model."""
        try:
            classifier = create_classifier(use_fast_model=True)
            assert classifier.config.use_fast_model is True
        except ValueError as e:
            # Expected if API key not set
            assert "IBDM_API_KEY" in str(e)

    def test_create_with_threshold(self):
        """Test creating a classifier with custom threshold."""
        try:
            classifier = create_classifier(use_fast_model=True, confidence_threshold=0.8)
            assert classifier.config.confidence_threshold == 0.8
        except ValueError as e:
            # Expected if API key not set
            assert "IBDM_API_KEY" in str(e)
