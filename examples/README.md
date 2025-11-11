# IBDM LiteLLM Examples

This directory contains example scripts demonstrating LiteLLM usage with the IBDM project's LLM configuration.

## Scripts

### `simple_llm_demo.py`

Demonstrates LiteLLM usage with Anthropic Claude 4.5 models:
- **Claude Sonnet 4.5** (`claude-sonnet-4-5-20250929`) - For large-scale generation, complex reasoning
- **Claude Haiku 4.5** (`claude-haiku-4-5-20251001`) - For control flow, analytics, classification
- Shows token usage statistics
- Explicit API key passing to avoid billing conflicts

**Usage:**
```bash
python3 examples/simple_llm_demo.py
```

**Note**: Requires `IBDM_API_KEY` environment variable. No fallback providers are used.

## Configuration

All scripts use the `IBDM_API_KEY` environment variable:
- `IBDM_API_KEY` - Anthropic API key for Claude models
  - Separate from Claude Code's own API usage
  - Must be passed explicitly via `api_key` parameter
  - Prevents billing conflicts

This is automatically available in the container environment. See `CLAUDE.md` for details.

## Model Selection

As documented in `CLAUDE.md`, the IBDM project uses Claude 4.5 exclusively:
1. **Claude Sonnet 4.5** - Content generation, complex reasoning, coding tasks ($3/$15 per million tokens)
2. **Claude Haiku 4.5** - Classification, control flow, quick tasks ($1/$5 per million tokens)
3. **No Fallbacks** - No automatic fallback to other providers

## LiteLLM Features Demonstrated

- ✅ Unified API across multiple providers
- ✅ Explicit API key passing to avoid env var conflicts
- ✅ Model selection based on task requirements
- ✅ Token usage tracking
- ✅ Temperature control for different use cases

## Adding New Examples

When creating new examples:
1. Follow the patterns in `simple_llm_demo.py`
2. Always pass `api_key=os.getenv("IBDM_API_KEY")` explicitly
3. Verify API keys at startup
4. Show token usage for cost tracking
5. Select appropriate model (Sonnet vs Haiku) based on task complexity
