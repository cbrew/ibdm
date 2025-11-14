# LLM Configuration Guide

This document provides detailed configuration guidance for LLM integration in the IBDM project.

## Overview

All LLM integrations use [LiteLLM](https://github.com/BerriAI/litellm) as the unified interface.

**Why LiteLLM?**
- Consistent API across multiple providers
- Easy model switching without code changes
- Built-in retry logic and error handling
- Cost tracking and monitoring
- Support for streaming responses

## Model Selection

### Primary Models: Anthropic Claude 4.5 Series

| Model | Model ID | Use Cases | Pricing (per million tokens) |
|-------|----------|-----------|------------------------------|
| **Sonnet 4.5** | `claude-sonnet-4-5-20250929` | Complex reasoning, generation, multi-step tasks | $3 input / $15 output |
| **Haiku 4.5** | `claude-haiku-4-5-20251001` | Control flow, analytics, quick classification | $1 input / $5 output |

### No Fallback Policy

**Do not use Google Gemini or OpenAI as fallbacks.** This project uses only Anthropic Claude models.

## When to Use Which Model

### Use Claude Sonnet 4.5 for:

- Content generation (essays, reports, creative writing)
- Complex reasoning and problem-solving
- Multi-step analysis
- Summarization of long documents
- Complex agents and coding tasks

### Use Claude Haiku 4.5 for:

- Classification and categorization
- Control flow decisions
- Analytics and metrics
- Quick question answering
- Structured data extraction
- Cost-sensitive applications (fastest model with near-frontier intelligence)

## API Keys

### Environment Variables

- `IBDM_API_KEY` - Anthropic Claude API key (primary)
  - Must be passed explicitly as `api_key` parameter to LiteLLM calls
  - This separate env var prevents billing conflicts with Claude Code's own Claude usage
- Keys are available in the runtime environment (container startup)
- A `.env` file is available in the project root for local development
- The `.env` file is gitignored and should never be committed

### Accessing Keys

```python
import os

# API keys are automatically available in the container environment
# They can also be loaded from .env file for local development
# Note: python-dotenv is optional; keys are already in the environment

# Verify keys are available
assert os.getenv("IBDM_API_KEY"), "IBDM_API_KEY not found in environment"
```

## Configuration Examples

### Basic Setup

```python
import os
import litellm
from litellm import completion

# Set default provider
litellm.set_verbose = False  # Set to True for debugging

# Get API key from environment
api_key = os.getenv("IBDM_API_KEY")
```

### Large-Scale Generation (Sonnet 4.5)

```python
response = completion(
    model="claude-sonnet-4-5-20250929",
    messages=[{"role": "user", "content": "Write a detailed analysis..."}],
    api_key=api_key,  # Explicitly pass API key
    temperature=0.7,
    max_tokens=8000
)
```

### Control and Analytics (Haiku 4.5)

```python
response = completion(
    model="claude-haiku-4-5-20251001",
    messages=[{"role": "user", "content": "Classify this text..."}],
    api_key=api_key,  # Explicitly pass API key
    temperature=0.3,
    max_tokens=500
)
```

### Async Operations

```python
from litellm import acompletion

response = await acompletion(
    model="claude-sonnet-4-5-20250929",
    messages=[{"role": "user", "content": "..."}],
    api_key=api_key,
    temperature=0.7
)
```

### Streaming Responses

```python
response = completion(
    model="claude-sonnet-4-5-20250929",
    messages=[{"role": "user", "content": "..."}],
    api_key=api_key,
    stream=True
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### Structured Output

```python
import json
from pydantic import BaseModel

class Classification(BaseModel):
    category: str
    confidence: float
    reasoning: str

response = completion(
    model="claude-haiku-4-5-20251001",
    messages=[
        {"role": "system", "content": "You are a classifier. Return JSON only."},
        {"role": "user", "content": "Classify: 'I need an NDA'"}
    ],
    api_key=api_key,
    temperature=0.0,
    response_format={"type": "json_object"}
)

result = Classification.model_validate_json(response.choices[0].message.content)
```

## Implementation Guidelines

### Always Pass API Key Explicitly

```python
# ✅ Correct
response = completion(
    model="claude-sonnet-4-5-20250929",
    messages=[...],
    api_key=os.getenv("IBDM_API_KEY")  # Explicitly pass
)

# ❌ Wrong - May use wrong env var
response = completion(
    model="claude-sonnet-4-5-20250929",
    messages=[...]
    # Missing api_key parameter - will use ANTHROPIC_API_KEY by default
)
```

### Default to Sonnet, Optimize with Haiku

```python
# Use Sonnet as default for most tasks
def get_model_for_task(task_type: str) -> str:
    """Select model based on task complexity."""
    if task_type in ["classify", "extract", "control"]:
        return "claude-haiku-4-5-20251001"  # Quick, structured tasks
    else:
        return "claude-sonnet-4-5-20250929"  # Default: complex reasoning
```

### Configure Timeouts and Retries

```python
import litellm

# Configure default timeout
litellm.request_timeout = 60  # seconds

# Configure retries
response = completion(
    model="claude-sonnet-4-5-20250929",
    messages=[...],
    api_key=api_key,
    num_retries=3,
    timeout=120
)
```

### Monitor Token Usage

```python
response = completion(
    model="claude-sonnet-4-5-20250929",
    messages=[...],
    api_key=api_key
)

# Check token usage
usage = response.usage
print(f"Input tokens: {usage.prompt_tokens}")
print(f"Output tokens: {usage.completion_tokens}")
print(f"Total tokens: {usage.total_tokens}")

# Calculate cost (Sonnet 4.5: $3/$15 per million tokens)
cost = (usage.prompt_tokens / 1_000_000 * 3) + \
       (usage.completion_tokens / 1_000_000 * 15)
print(f"Cost: ${cost:.4f}")
```

## Error Handling

### Basic Error Handling

```python
from litellm import completion
from litellm.exceptions import APIError, Timeout

try:
    response = completion(
        model="claude-sonnet-4-5-20250929",
        messages=[...],
        api_key=api_key
    )
except APIError as e:
    print(f"API error: {e}")
    raise
except Timeout as e:
    print(f"Request timeout: {e}")
    raise
```

### Debugging

```python
import litellm

# Enable verbose logging
litellm.set_verbose = True

# Run your completion
response = completion(...)

# Disable verbose logging
litellm.set_verbose = False
```

## Cost Optimization

### Use Haiku for High-Volume Tasks

```python
# High-volume classification task
for item in large_dataset:
    response = completion(
        model="claude-haiku-4-5-20251001",  # 5x cheaper than Sonnet
        messages=[{"role": "user", "content": f"Classify: {item}"}],
        api_key=api_key,
        max_tokens=50  # Limit output for simple tasks
    )
```

### Cache System Prompts

```python
# LiteLLM automatically uses Claude's prompt caching for repeated content
system_prompt = "You are an NDA drafting assistant..."  # Long system prompt

# First call - cache miss
response1 = completion(
    model="claude-sonnet-4-5-20250929",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Question 1"}
    ],
    api_key=api_key
)

# Second call - cache hit (90% discount on cached tokens)
response2 = completion(
    model="claude-sonnet-4-5-20250929",
    messages=[
        {"role": "system", "content": system_prompt},  # Same prompt - cached
        {"role": "user", "content": "Question 2"}
    ],
    api_key=api_key
)
```

## Testing and Development

### Mock LiteLLM for Tests

```python
from unittest.mock import patch, MagicMock

def test_llm_integration():
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Test response"

    with patch('litellm.completion', return_value=mock_response):
        result = my_llm_function()
        assert result == "Test response"
```

### Development vs Production

```python
import os

def get_model_config():
    """Get model configuration based on environment."""
    if os.getenv("ENVIRONMENT") == "production":
        return {
            "model": "claude-sonnet-4-5-20250929",
            "temperature": 0.7,
            "max_tokens": 8000
        }
    else:  # development
        return {
            "model": "claude-haiku-4-5-20251001",  # Cheaper for development
            "temperature": 0.7,
            "max_tokens": 2000
        }
```

## Related Documentation

- `docs/environment_setup.md` - Environment variables and API key setup
- `docs/architecture_principles.md` - Simplicity and single-path execution
- [LiteLLM Documentation](https://docs.litellm.ai/)
- [Anthropic Claude Documentation](https://docs.anthropic.com/)