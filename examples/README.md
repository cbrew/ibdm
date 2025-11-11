# IBDM LiteLLM Examples

This directory contains example scripts demonstrating LiteLLM usage with the IBDM project's LLM configuration.

## Scripts

### `simple_llm_demo.py`

Demonstrates basic LiteLLM usage with provider fallback strategy:
- **Primary**: Attempts to use Gemini 1.5 Pro (Google)
- **Fallback**: Falls back to GPT-4o-mini (OpenAI) if Gemini fails
- Shows token usage statistics
- Handles errors gracefully

**Usage:**
```bash
python3 examples/simple_llm_demo.py
```

**Note**: The Gemini API key in the environment may have restrictions. The script demonstrates automatic fallback to OpenAI, which is part of the IBDM LLM strategy.

## Configuration

All scripts use environment variables for API keys:
- `GEMINI_API_KEY` - Google/Gemini models
- `OPENAI_API_KEY` - OpenAI models

These are automatically available in the container environment. See `CLAUDE.md` for details.

## Provider Priority

As documented in `CLAUDE.md`, the IBDM project uses this provider priority:
1. **Google/Gemini** (gemini-1.5-pro, gemini-1.5-flash) - Cost-effective
2. **OpenAI** (gpt-4o, gpt-4o-mini) - Reliable fallback
3. **Local models** (via Ollama) - For development/testing

## LiteLLM Features Demonstrated

- ✅ Unified API across multiple providers
- ✅ Automatic API key detection from environment
- ✅ Graceful fallback between providers
- ✅ Token usage tracking
- ✅ Error handling and retry logic

## Adding New Examples

When creating new examples:
1. Follow the patterns in `simple_llm_demo.py`
2. Always implement provider fallback
3. Verify API keys at startup
4. Show token usage for cost tracking
5. Handle errors gracefully
