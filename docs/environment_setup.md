# IBDM Environment Setup

This document describes the containerized development environment and API key configuration.

## Container Environment

This project runs in a containerized environment where:
- Environment variables are set at container startup
- API keys are pre-configured and available via environment variables
- No manual key configuration is needed during development

## Environment Variables

The following environment variables are available:

| Variable | Purpose | Status |
|----------|---------|--------|
| `IBDM_API_KEY` | Anthropic Claude API key | **Primary** (used for all LLM operations) |
| `GEMINI_API_KEY` | Google/Gemini API key | Available but not actively used |
| `OPENAI_API_KEY` | OpenAI API key | Available but not actively used |

**Note**: This project primarily uses `IBDM_API_KEY` for Claude models. The other keys are available for compatibility but not recommended (see LLM configuration policy).

## .env File

A `.env` file exists in the project root containing these API keys:

```bash
IBDM_API_KEY=<key>
GEMINI_API_KEY=<key>
OPENAI_API_KEY=<key>
```

**Important Notes**:
- The `.env` file is automatically gitignored
- Keys are already available in the environment; the `.env` file is for reference
- Never commit API keys to version control
- Python code can access keys directly via `os.getenv()` without python-dotenv

## Verifying Environment

To verify that the environment is properly configured:

```python
import os

# Verify primary API key is available
ibdm_api_key = os.getenv("IBDM_API_KEY")

assert ibdm_api_key, "IBDM_API_KEY not found"

# Optional: Verify other keys if needed
# gemini_key = os.getenv("GEMINI_API_KEY")
# openai_key = os.getenv("OPENAI_API_KEY")
```

## Troubleshooting

### API Key Not Found

If you get an `AssertionError: IBDM_API_KEY not found`:

1. Check that the `.env` file exists in the project root
2. Verify the file contains `IBDM_API_KEY=<your-key>`
3. If running in a container, ensure environment variables are passed at startup
4. For local development, ensure your shell session has the variables exported

### Container Startup

Environment variables should be automatically available in the container. If not:

```bash
# Check if variables are set
env | grep API_KEY

# If missing, restart the container with environment variables
podman-compose down
podman-compose up -d
```

## Security Best Practices

1. **Never commit `.env` file** - Already in `.gitignore`
2. **Rotate keys regularly** - Update both `.env` and container environment
3. **Use separate keys for development/production** - Current setup is for development only
4. **Audit key usage** - Monitor Anthropic dashboard for unexpected usage

## Related Documentation

- `docs/llm_configuration.md` - LLM provider setup and model selection
- `CLAUDE.md` - Development policies