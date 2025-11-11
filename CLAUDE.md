# Claude Development Policies for IBDM

This document defines the development policies and workflows for AI agents working on the Issue-Based Dialogue Management (IBDM) project.

## Environment

### Container Environment

This project runs in a containerized environment where:
- Environment variables are set at container startup
- API keys are pre-configured and available via environment variables
- No manual key configuration is needed during development

### Environment Variables

The following environment variables are available:
- `GEMINI_API_KEY` - Google/Gemini API key for LLM access
- `OPENAI_API_KEY` - OpenAI API key for LLM access

### .env File

A `.env` file exists in the project root containing these API keys:
```bash
GEMINI_API_KEY=<key>
OPENAI_API_KEY=<key>
```

**Important Notes**:
- The `.env` file is automatically gitignored
- Keys are already available in the environment; the `.env` file is for reference
- Never commit API keys to version control
- Python code can access keys directly via `os.getenv()` without python-dotenv

### Verifying Environment

```python
import os

# Verify API keys are available
gemini_key = os.getenv("GEMINI_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

assert gemini_key, "GEMINI_API_KEY not found"
assert openai_key, "OPENAI_API_KEY not found"
```

## Core Policies

### 1. Dependency Management: Use uv

**Policy**: All Python dependency management must use [uv](https://github.com/astral-sh/uv).

**Rationale**: uv provides fast, reliable dependency resolution and is designed for modern Python development.

**Commands**:
```bash
# Install dependencies
uv pip install -e ".[dev]"

# Add new dependency
uv pip install <package>
# Then update pyproject.toml

# Sync dependencies
uv pip sync requirements.txt
```

### 2. Formatting and Basic Type Checking: Use ruff

**Policy**: Use [ruff](https://github.com/astral-sh/ruff) for code formatting and basic type checking.

**Rationale**: ruff is extremely fast and replaces multiple tools (black, isort, flake8, etc.).

**Commands**:
```bash
# Format code
ruff format src/ tests/

# Check for issues
ruff check src/ tests/

# Fix auto-fixable issues
ruff check --fix src/ tests/

# Run before every commit
ruff format src/ tests/ && ruff check --fix src/ tests/
```

**Configuration**: Settings in `pyproject.toml`:
```toml
[tool.ruff]
line-length = 100
target-version = "py310"
select = ["E", "F", "I", "N", "W", "UP"]
```

### 3. Heavy Type Checking: Use pyright

**Policy**: Use [pyright](https://github.com/microsoft/pyright) for comprehensive static type checking.

**Rationale**: pyright provides strict type checking with excellent performance and IDE integration.

**Commands**:
```bash
# Type check entire project
pyright

# Type check specific module
pyright src/ibdm/core/

# Run in strict mode
pyright --pythonversion 3.10
```

**Configuration**: Settings in `pyproject.toml`:
```toml
[tool.pyright]
pythonVersion = "3.10"
typeCheckingMode = "strict"
reportMissingTypeStubs = false
```

### 4. Make Small Commits

**Policy**: Commits should be small, focused, and single-purpose.

**Guidelines**:
- One logical change per commit
- Commits should compile and pass tests
- Maximum ~300 lines changed per commit (guideline, not hard rule)
- Use conventional commit messages

**Good Examples**:
```
feat(core): add WhQuestion class with tests
fix(rules): correct QUD pop logic in answer integration
refactor(engine): extract interpretation to separate method
test(core): add property tests for Question resolution
docs(api): document InformationState structure
```

**Bad Examples**:
```
WIP
fix stuff
updates
Implemented everything for phase 1
```

**Commit Message Format**:
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`, `ci`

### 5. Test After Every Commit

**Policy**: Run tests after every commit before pushing.

**Workflow**:
```bash
# Make changes
vim src/ibdm/core/questions.py

# Run relevant tests
pytest tests/unit/test_questions.py -v

# Run full test suite
pytest

# Format and check
ruff format src/ tests/
ruff check --fix src/ tests/

# Type check
pyright src/

# Commit only if all pass
git add src/ibdm/core/questions.py tests/unit/test_questions.py
git commit -m "feat(core): add WhQuestion class with tests"

# Run tests again to ensure commit is clean
pytest
```

**Test Requirements**:
- Unit tests must pass
- Type checking must pass
- Formatting must be clean
- No ruff violations

### 6. Document Every Decision via Beads

**Policy**: All design decisions, bugs discovered, and future work must be tracked in beads.

**When to Create Beads Issues**:

1. **Before Starting Work**: Check beads for ready tasks
   ```bash
   bd ready --json
   # Or use helper:
   .claude/beads-helpers.sh ready
   ```

2. **When Starting a Task**: Mark as in_progress
   ```bash
   bd update ibdm-brm.1 --status in_progress
   # Or use helper:
   .claude/beads-helpers.sh start ibdm-brm.1
   ```

3. **Discovered Issues**: Create new tasks
   ```bash
   bd create "Fix typing issue in Question.resolves_with" \
     -t bug \
     -p 0 \
     -l "core,typing" \
     --discovered-from ibdm-brm.1 \
     --json
   ```

4. **Design Decisions**: Document in task comments
   ```bash
   bd comment ibdm-brm.1 "Decision: Using ABC for Question base class to enforce resolves_with implementation"
   ```

5. **Future Work**: Create tasks with lower priority
   ```bash
   bd create "Optimize Question matching for large QUD stacks" \
     -t task \
     -p 3 \
     -l "performance,future" \
     --json
   ```

6. **Completing Work**: Close with detailed reason
   ```bash
   bd close ibdm-brm.1 --reason "Implemented WhQuestion, YNQuestion, AltQuestion with full test coverage. All tests passing."
   # Or use helper:
   .claude/beads-helpers.sh done ibdm-brm.1 "Implemented with full test coverage"
   ```

**Benefits**:
- Creates audit trail of decisions
- Enables long-term planning
- Allows context recovery after interruptions
- Facilitates collaboration between agents/developers

### 7. Work Step by Step

**Policy**: Break work into small, verifiable steps with frequent validation.

**Step-by-Step Workflow**:

1. **Plan**: Review beads task and break into subtasks if needed
   ```bash
   # Check task details
   bd show ibdm-brm.1 --json

   # If task is large, create subtasks
   bd create "Implement WhQuestion class" -t task --parent ibdm-brm.1
   bd create "Implement YNQuestion class" -t task --parent ibdm-brm.1
   bd create "Implement AltQuestion class" -t task --parent ibdm-brm.1
   ```

2. **Implement**: Write minimal code for one step
   ```python
   # Step 1: Just the class structure
   class WhQuestion(Question):
       variable: str
       predicate: str
   ```

3. **Test**: Write test for that step
   ```python
   def test_wh_question_creation():
       q = WhQuestion(variable="x", predicate="weather")
       assert q.variable == "x"
   ```

4. **Verify**: Run tests
   ```bash
   pytest tests/unit/test_questions.py::test_wh_question_creation -v
   ```

5. **Commit**: Small, focused commit
   ```bash
   git add src/ibdm/core/questions.py tests/unit/test_questions.py
   git commit -m "feat(core): add WhQuestion class structure"
   ```

6. **Repeat**: Next step (add methods, validation, etc.)

7. **Update Beads**: Record progress
   ```bash
   bd comment ibdm-brm.1 "✓ WhQuestion class implemented and tested"
   ```

**Red-Green-Refactor Pattern**:
1. **Red**: Write failing test
2. **Green**: Write minimal code to pass
3. **Refactor**: Improve code quality
4. **Commit**: Each step separately

### 8. LLM Provider Configuration: Use LiteLLM

**Policy**: All LLM integrations must use [LiteLLM](https://github.com/BerriAI/litellm) as the unified interface.

**Rationale**: LiteLLM provides a consistent API across multiple providers, simplifies switching between models, and handles rate limiting and error handling.

**Provider Priority**:
1. **First Choice**: Google models (Gemini)
   - `gemini/gemini-1.5-pro`
   - `gemini/gemini-1.5-flash`
2. **Second Choice**: OpenAI models
   - `gpt-4o`
   - `gpt-4o-mini`
3. **Fallback**: Local models via Ollama (if needed)

**API Keys**:
- API keys are provided via environment variables
- `GEMINI_API_KEY` for Google/Gemini models (note: use GEMINI_API_KEY, not GOOGLE_API_KEY)
- `OPENAI_API_KEY` for OpenAI models
- Keys are available in the runtime environment (container startup)
- A `.env` file is available in the project root for local development
- The `.env` file is gitignored and should never be committed

**Environment Setup**:
```python
import os

# API keys are automatically available in the container environment
# They can also be loaded from .env file for local development
# Note: python-dotenv is optional; keys are already in the environment

# Verify keys are available
assert os.getenv("GEMINI_API_KEY"), "GEMINI_API_KEY not found in environment"
assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY not found in environment"
```

**Configuration**:
```python
import litellm
from litellm import completion

# Set default provider
litellm.set_verbose = False  # Set to True for debugging

# LiteLLM automatically uses these environment variables:
# - GEMINI_API_KEY for gemini/* models
# - OPENAI_API_KEY for gpt-* models

# Example usage
response = completion(
    model="gemini/gemini-1.5-pro",  # Google model (first choice)
    messages=[{"role": "user", "content": "Hello"}],
    temperature=0.7,
    max_tokens=1000
)

# With fallback
try:
    response = completion(model="gemini/gemini-1.5-pro", ...)
except Exception:
    response = completion(model="gpt-4o-mini", ...)  # OpenAI fallback
```

**Implementation Guidelines**:
- Use LiteLLM's unified interface for all LLM calls
- Prefer Google models for cost-effectiveness and performance
- Implement graceful fallback to OpenAI if Google models fail
- Use async operations where possible: `await acompletion(...)`
- Configure timeouts and retries through LiteLLM
- Monitor token usage and costs

**Benefits**:
- Single interface for multiple providers
- Easy model switching without code changes
- Built-in retry logic and error handling
- Cost tracking and monitoring
- Support for streaming responses

## Workflow Integration

### Daily Work Session

```bash
# 1. Start of session - check ready work
.claude/beads-helpers.sh ready

# 2. Select highest priority task
.claude/beads-helpers.sh start ibdm-brm.1

# 3. Work step-by-step
# - Write test
# - Implement
# - Run tests: pytest tests/unit/test_questions.py -v
# - Format: ruff format src/ tests/
# - Check: ruff check --fix src/ tests/
# - Type check: pyright src/ibdm/core/
# - Commit: git commit -m "feat(core): ..."

# 4. Complete task
.claude/beads-helpers.sh done ibdm-brm.1 "Implemented with tests"

# 5. Check what's newly ready
.claude/beads-helpers.sh ready
```

### Before Pushing to Remote

```bash
# Full validation
pytest                          # All tests
ruff format src/ tests/         # Format
ruff check src/ tests/          # Lint
pyright src/                    # Type check

# If all pass
git push -u origin <branch>
```

### Weekly Review

```bash
# Check phase progress
.claude/beads-helpers.sh progress 1

# Review completed tasks
bd list --status closed --json | jq -r '.[] | "\(.id): \(.title)"'

# Identify blockers
bd list --status blocked --json

# Plan next week
bd list -p 0 -p 1 --status open --json
```

## Tool Configuration

### pyproject.toml

Ensure these sections exist:

```toml
[tool.ruff]
line-length = 100
target-version = "py310"
select = ["E", "F", "I", "N", "W", "UP"]
ignore = []

[tool.pyright]
pythonVersion = "3.10"
typeCheckingMode = "strict"
reportMissingTypeStubs = false

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
addopts = "-v --cov=ibdm --cov-report=term-missing"
```

### Pre-commit Checklist

Before every commit:
- [ ] Tests pass: `pytest`
- [ ] Code formatted: `ruff format src/ tests/`
- [ ] No lint errors: `ruff check src/ tests/`
- [ ] Types check: `pyright src/`
- [ ] Commit message follows convention
- [ ] Beads task updated

### Git Hooks (Optional)

Consider adding pre-commit hook:

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running pre-commit checks..."

# Format
ruff format src/ tests/

# Lint
if ! ruff check src/ tests/; then
    echo "❌ Ruff check failed"
    exit 1
fi

# Type check
if ! pyright src/; then
    echo "❌ Type check failed"
    exit 1
fi

# Tests
if ! pytest; then
    echo "❌ Tests failed"
    exit 1
fi

echo "✓ All checks passed"
```

## References

- [uv Documentation](https://github.com/astral-sh/uv)
- [ruff Documentation](https://docs.astral.sh/ruff/)
- [pyright Documentation](https://github.com/microsoft/pyright)
- [beads Documentation](https://github.com/steveyegge/beads)
- [LiteLLM Documentation](https://docs.litellm.ai/)
- [Conventional Commits](https://www.conventionalcommits.org/)

## Questions or Updates

If these policies need updating or you have questions:
1. Create a beads task: `bd create "Policy question: ..."`
2. Discuss in task comments
3. Update this document with decision
4. Commit with: `docs(policy): update CLAUDE.md`
