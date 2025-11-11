"""Tests for LLM adapter interface."""

import json
import os
from unittest.mock import Mock, patch

import pytest
from pydantic import BaseModel

from ibdm.nlu.llm_adapter import (
    LLMAdapter,
    LLMAPIError,
    LLMConfig,
    LLMParsingError,
    LLMResponse,
    ModelType,
    create_adapter,
)


class SampleResponse(BaseModel):
    """Sample Pydantic model for structured response tests."""

    answer: str
    confidence: float


@pytest.fixture
def mock_env():
    """Mock environment with API key."""
    with patch.dict(os.environ, {"IBDM_API_KEY": "test-key-123"}):
        yield


@pytest.fixture
def adapter(mock_env):
    """Create test adapter."""
    return LLMAdapter(LLMConfig(model=ModelType.HAIKU))


@pytest.fixture
def mock_completion_response():
    """Create mock completion response."""
    response = Mock()
    response.choices = [Mock()]
    response.choices[0].message.content = "Test response"
    response.usage = Mock()
    response.usage.total_tokens = 100
    response.usage.prompt_tokens = 50
    response.usage.completion_tokens = 50
    return response


def test_adapter_initialization(mock_env):
    """Test adapter initializes correctly."""
    adapter = LLMAdapter()
    assert adapter.api_key == "test-key-123"
    assert adapter.config.model == ModelType.SONNET


def test_adapter_initialization_no_api_key():
    """Test adapter raises error without API key."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="IBDM_API_KEY not found"):
            LLMAdapter()


def test_adapter_call_success(adapter, mock_completion_response):
    """Test successful LLM call."""
    with patch("ibdm.nlu.llm_adapter.completion", return_value=mock_completion_response):
        response = adapter.call("Test prompt")

        assert isinstance(response, LLMResponse)
        assert response.content == "Test response"
        assert response.tokens_used == 100
        assert response.prompt_tokens == 50
        assert response.completion_tokens == 50


def test_adapter_call_with_system_prompt(adapter, mock_completion_response):
    """Test call with system prompt."""
    with patch(
        "ibdm.nlu.llm_adapter.completion", return_value=mock_completion_response
    ) as mock_call:
        adapter.call("Test prompt", system_prompt="You are a helpful assistant")

        # Verify system message was included
        messages = mock_call.call_args[1]["messages"]
        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[0]["content"] == "You are a helpful assistant"
        assert messages[1]["role"] == "user"


def test_adapter_call_with_overrides(adapter, mock_completion_response):
    """Test call with temperature and max_tokens overrides."""
    with patch(
        "ibdm.nlu.llm_adapter.completion", return_value=mock_completion_response
    ) as mock_call:
        adapter.call("Test prompt", temperature=0.5, max_tokens=1000)

        # Verify overrides were applied
        assert mock_call.call_args[1]["temperature"] == 0.5
        assert mock_call.call_args[1]["max_tokens"] == 1000


def test_adapter_call_retry_on_failure(adapter):
    """Test retry logic on API failure."""
    with patch("ibdm.nlu.llm_adapter.completion", side_effect=Exception("API Error")):
        with patch("time.sleep"):  # Speed up test
            with pytest.raises(LLMAPIError, match="failed after 3 attempts"):
                adapter.call("Test prompt")


def test_adapter_call_success_after_retry(adapter, mock_completion_response):
    """Test successful call after initial failures."""
    with patch(
        "ibdm.nlu.llm_adapter.completion",
        side_effect=[Exception("Error 1"), Exception("Error 2"), mock_completion_response],
    ):
        with patch("time.sleep"):  # Speed up test
            response = adapter.call("Test prompt")
            assert response.content == "Test response"


@pytest.mark.asyncio
async def test_adapter_acall_success(adapter, mock_completion_response):
    """Test successful async LLM call."""
    with patch("ibdm.nlu.llm_adapter.acompletion", return_value=mock_completion_response):
        response = await adapter.acall("Test prompt")

        assert isinstance(response, LLMResponse)
        assert response.content == "Test response"
        assert response.tokens_used == 100


@pytest.mark.asyncio
async def test_adapter_batch_call(adapter):
    """Test batch calling multiple prompts."""
    mock_responses = []
    for i in range(3):
        mock_resp = Mock()
        mock_resp.choices = [Mock()]
        mock_resp.choices[0].message.content = f"Response {i}"
        mock_resp.usage = Mock()
        mock_resp.usage.total_tokens = 100
        mock_resp.usage.prompt_tokens = 50
        mock_resp.usage.completion_tokens = 50
        mock_responses.append(mock_resp)

    with patch("ibdm.nlu.llm_adapter.acompletion", side_effect=mock_responses):
        prompts = ["Prompt 1", "Prompt 2", "Prompt 3"]
        responses = await adapter.batch_call(prompts)

        assert len(responses) == 3
        assert responses[0].content == "Response 0"
        assert responses[1].content == "Response 1"
        assert responses[2].content == "Response 2"


def test_adapter_call_structured_success(adapter):
    """Test structured output parsing."""
    json_response = json.dumps({"answer": "test answer", "confidence": 0.95})

    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = json_response
    mock_response.usage = Mock()
    mock_response.usage.total_tokens = 100
    mock_response.usage.prompt_tokens = 50
    mock_response.usage.completion_tokens = 50

    with patch("ibdm.nlu.llm_adapter.completion", return_value=mock_response):
        result = adapter.call_structured("Test prompt", SampleResponse)

        assert isinstance(result, SampleResponse)
        assert result.answer == "test answer"
        assert result.confidence == 0.95


def test_adapter_call_structured_with_markdown(adapter):
    """Test structured parsing with markdown code blocks."""
    json_response = '```json\n{"answer": "test answer", "confidence": 0.95}\n```'

    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = json_response
    mock_response.usage = Mock()
    mock_response.usage.total_tokens = 100
    mock_response.usage.prompt_tokens = 50
    mock_response.usage.completion_tokens = 50

    with patch("ibdm.nlu.llm_adapter.completion", return_value=mock_response):
        result = adapter.call_structured("Test prompt", SampleResponse)

        assert isinstance(result, SampleResponse)
        assert result.answer == "test answer"
        assert result.confidence == 0.95


def test_adapter_call_structured_parsing_error(adapter):
    """Test structured parsing with invalid JSON."""
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "Not valid JSON"
    mock_response.usage = Mock()
    mock_response.usage.total_tokens = 100
    mock_response.usage.prompt_tokens = 50
    mock_response.usage.completion_tokens = 50

    with patch("ibdm.nlu.llm_adapter.completion", return_value=mock_response):
        with pytest.raises(LLMParsingError, match="Failed to parse LLM response"):
            adapter.call_structured("Test prompt", SampleResponse)


def test_adapter_call_structured_validation_error(adapter):
    """Test structured parsing with schema mismatch."""
    # Missing required field 'confidence'
    json_response = json.dumps({"answer": "test answer"})

    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = json_response
    mock_response.usage = Mock()
    mock_response.usage.total_tokens = 100
    mock_response.usage.prompt_tokens = 50
    mock_response.usage.completion_tokens = 50

    with patch("ibdm.nlu.llm_adapter.completion", return_value=mock_response):
        with pytest.raises(LLMParsingError):
            adapter.call_structured("Test prompt", SampleResponse)


@pytest.mark.asyncio
async def test_adapter_acall_structured_success(adapter):
    """Test async structured output parsing."""
    json_response = json.dumps({"answer": "test answer", "confidence": 0.95})

    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = json_response
    mock_response.usage = Mock()
    mock_response.usage.total_tokens = 100
    mock_response.usage.prompt_tokens = 50
    mock_response.usage.completion_tokens = 50

    with patch("ibdm.nlu.llm_adapter.acompletion", return_value=mock_response):
        result = await adapter.acall_structured("Test prompt", SampleResponse)

        assert isinstance(result, SampleResponse)
        assert result.answer == "test answer"
        assert result.confidence == 0.95


def test_create_adapter_sonnet(mock_env):
    """Test convenience function creates Sonnet adapter."""
    adapter = create_adapter("sonnet")
    assert adapter.config.model == ModelType.SONNET
    assert adapter.config.temperature == 0.7


def test_create_adapter_haiku(mock_env):
    """Test convenience function creates Haiku adapter."""
    adapter = create_adapter("haiku", temperature=0.3, max_tokens=500)
    assert adapter.config.model == ModelType.HAIKU
    assert adapter.config.temperature == 0.3
    assert adapter.config.max_tokens == 500


def test_model_type_enum():
    """Test ModelType enum values."""
    assert ModelType.SONNET.value == "claude-sonnet-4-5-20250929"
    assert ModelType.HAIKU.value == "claude-haiku-4-5-20251001"
