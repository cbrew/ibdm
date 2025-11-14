# Claude Development Guide for IBDM

Quick reference for AI agents working on the Issue-Based Dialogue Management (IBDM) project.

## Table of Contents

- [Quick Start](#quick-start)
- [Architecture Principles](#architecture-principles)
- [Development Tooling](#development-tooling)
- [Development Process](#development-process)
- [IBDM-Specific Policies](#ibdm-specific-policies)
- [Workflow Cheatsheet](#workflow-cheatsheet)

## Quick Start

```bash
# 1. Verify environment
python -c "import os; assert os.getenv('IBDM_API_KEY'), 'IBDM_API_KEY missing'"

# 2. Install dependencies
uv pip install --system -e ".[dev]"

# 3. Check ready tasks
.claude/beads-helpers.sh ready

# 4. Before every commit
ruff format src/ tests/ && ruff check --fix src/ tests/ && pyright src/ && pytest

# 5. Make small commits
git commit -m "feat(scope): description"
```

## Architecture Principles

### 0. Architectural Clarity and Simplicity (HIGHEST PRIORITY)

**Policy**: Prioritize clarity over cleverness. Avoid complexity, fallbacks, and defensive programming.

**Five Core Principles**:
1. **Assume Resource Availability** - No fallback logic for missing API keys/models
2. **Single Path Execution** - Direct model selection, no cascading (Sonnet for complexity, Haiku for speed)
3. **Explicit State Management** - All state in Burr State, engines are pure functions
4. **Minimal Error Handling** - Fail fast, log clearly, don't retry
5. **Direct Configuration** - Simple config objects, no feature flags

**📖 Details**: See [`docs/architecture_principles.md`](docs/architecture_principles.md)

### 10. Domain Semantic Layer

**Policy**: Define predicates, sorts, and semantic operations explicitly using domain models.

**Key Points**:
- Use `src/ibdm/core/domain.py` for domain definitions
- Register plan builders with `domain.register_plan_builder()`
- Use `domain.get_plan()` not hardcoded plans
- Map NLU entities to domain predicates

**Why**: Domain abstraction increased Larsson fidelity from ~85% to ~95%.

**Example**: See `src/ibdm/domains/nda_domain.py`

### 11. Task Plan Formation in Integration Phase

**Policy**: Create dialogue plans in INTEGRATION phase, not interpretation.

**Phases**:
1. **INTERPRET**: Utterance → DialogueMove (syntactic/semantic only)
2. **INTEGRATE**: DialogueMove → State updates + plan formation
3. **SELECT**: Choose next system move
4. **GENERATE**: Produce natural language

**📖 Details**: See CLAUDE.md lines 640-701 (original)

### 12. Larsson Algorithmic Principles (Source of Truth)

**Policy**: Implementation MUST follow Larsson (2002) algorithms.

**Critical Rules**:
- QUD is a stack (LIFO), not a set
- Single rule application per update cycle
- Explicit state passing (no hidden state)
- Questions accommodated (`private.issues`) before raised (`shared.qud`)
- Domain-independent rules (domain knowledge in resources)

**📖 Details**: See [`docs/LARSSON_ALGORITHMS.md`](docs/LARSSON_ALGORITHMS.md)

**Verification Checklist**:
- [ ] Control flow matches Algorithm 2.2
- [ ] Information State structure matches Larsson figures
- [ ] Update/Select rules match specifications
- [ ] No hidden state in engines
- [ ] QUD is stack (LIFO)
- [ ] Plans formed in integration, not interpretation

## Development Tooling

### 1. Dependency Management: uv

```bash
# Install dependencies
uv pip install --system -e ".[dev]"

# Add new package
uv pip install --system <package>
# Then add to pyproject.toml dependencies
```

**Why uv**: Fast, reliable, modern Python dependency management.

### 2. Formatting: ruff

```bash
# Format code
ruff format src/ tests/

# Check and fix issues
ruff check --fix src/ tests/

# Before every commit
ruff format src/ tests/ && ruff check --fix src/ tests/
```

**Why ruff**: Extremely fast, replaces black/isort/flake8.

### 3. Type Checking: pyright

```bash
# Type check entire project
pyright

# Type check specific module
pyright src/ibdm/core/
```

**Why pyright**: Strict type checking, excellent performance.

**Config**: `pyproject.toml` sets `typeCheckingMode = "strict"`

### 9. LLM Provider: LiteLLM

**Policy**: Use LiteLLM for all LLM calls. Primary models: Claude Sonnet 4.5 / Haiku 4.5.

```python
import os
from litellm import completion

api_key = os.getenv("IBDM_API_KEY")

# Complex tasks: Sonnet 4.5
response = completion(
    model="claude-sonnet-4-5-20250929",
    messages=[{"role": "user", "content": "..."}],
    api_key=api_key
)

# Quick tasks: Haiku 4.5
response = completion(
    model="claude-haiku-4-5-20251001",
    messages=[{"role": "user", "content": "..."}],
    api_key=api_key
)
```

**Key Points**:
- **Always pass `api_key=os.getenv("IBDM_API_KEY")`** - Prevents billing conflicts
- Use Sonnet for: complex reasoning, generation, multi-step tasks
- Use Haiku for: classification, control flow, structured data
- No fallbacks to Gemini/OpenAI

**📖 Details**: See [`docs/llm_configuration.md`](docs/llm_configuration.md) and [`docs/environment_setup.md`](docs/environment_setup.md)

## Development Process

### 4. Make Small Commits

**Policy**: One logical change per commit (~300 lines max).

**Commit Format**:
```
<type>(<scope>): <description>

[optional body]
```

**Types**: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`, `ci`

**Good Examples**:
- `feat(core): add WhQuestion class with tests`
- `fix(rules): correct QUD pop logic in answer integration`
- `refactor(engine): extract interpretation to separate method`

**Bad Examples**:
- `WIP`
- `fix stuff`
- `Implemented everything for phase 1`

### 5. Test After Every Commit

**Policy**: Run tests before committing.

```bash
# Run relevant tests
pytest tests/unit/test_questions.py -v

# Full test suite
pytest

# Quality checks
ruff format src/ tests/
ruff check --fix src/ tests/
pyright src/

# Commit only if all pass
git add <files>
git commit -m "feat(core): ..."
```

### 6. Document via Beads

**Policy**: Track design decisions and tasks in beads.

```bash
# Check ready tasks
.claude/beads-helpers.sh ready

# Start task
.claude/beads-helpers.sh start ibdm-brm.1

# Complete task
.claude/beads-helpers.sh done ibdm-brm.1 "Implemented with tests"
```

**When to Create Beads Issues**:
- Before starting work (check ready tasks)
- When starting a task (mark in_progress)
- Discovered issues (document in commit messages)
- Design decisions (commit messages + code comments)
- Future work (TODO comments with task references)

### 7. Own All Code Quality Issues

**Policy**: Fix all quality issues in files you touch, regardless of when introduced.

**Never say**: "The type errors are pre-existing issues."

**Always do**:
1. Fix immediate issues in your changes
2. Fix other issues in the same function
3. If too many, create a beads task for systematic cleanup

**Rationale**: Every change is an opportunity to improve the codebase.

### 8. Work Step by Step

**Policy**: Break work into small, verifiable steps.

**Red-Green-Refactor Pattern**:
1. **Red**: Write failing test
2. **Green**: Write minimal code to pass
3. **Refactor**: Improve code quality
4. **Commit**: Each step separately

**Example Workflow**:
```bash
# 1. Write test
vim tests/unit/test_questions.py

# 2. Run test (should fail)
pytest tests/unit/test_questions.py::test_wh_question_creation -v

# 3. Implement minimal code
vim src/ibdm/core/questions.py

# 4. Run test (should pass)
pytest tests/unit/test_questions.py::test_wh_question_creation -v

# 5. Commit
git add src/ibdm/core/questions.py tests/unit/test_questions.py
git commit -m "feat(core): add WhQuestion class structure"

# 6. Repeat for next step
```

## IBDM-Specific Policies

### Environment

- **Container**: Podman (not Docker)
- **API Keys**: Available via `IBDM_API_KEY`, `GEMINI_API_KEY`, `OPENAI_API_KEY`
- **Primary Key**: `IBDM_API_KEY` for Anthropic Claude
- **Config**: `.env` file in project root (gitignored)

**📖 Details**: See [`docs/environment_setup.md`](docs/environment_setup.md)

### Code Style

- **No `sys.path` manipulations** - Use `uv` and `pyproject.toml`
- **No dynamic imports** - Use proper package structure
- **Small commits** - Run quality checks after each commit
- **Avoid fallback options** - Get it right the first time (see Policy #0)

### Textual Applications

- **Don't run Textual apps** - They make a mess in the terminal
- **Use `compose` heavily** - Avoid manual mounting/unmounting

## Workflow Cheatsheet

### Daily Work Session

```bash
# 1. Check ready tasks
.claude/beads-helpers.sh ready

# 2. Start highest priority task
.claude/beads-helpers.sh start ibdm-brm.1

# 3. Work step-by-step (see Policy #8)
# - Write test → Implement → Test → Commit

# 4. Before each commit
ruff format src/ tests/ && ruff check --fix src/ tests/
pyright src/
pytest

# 5. Commit
git commit -m "feat(scope): description"

# 6. Complete task
.claude/beads-helpers.sh done ibdm-brm.1 "Implemented with tests"
```

### Before Pushing

```bash
# Full validation
pytest                          # All tests
ruff format src/ tests/         # Format
ruff check src/ tests/          # Lint
pyright src/                    # Type check

# Push
git push -u origin <branch>
```

### Weekly Review

```bash
# Check phase progress
.claude/beads-helpers.sh progress 1

# Review completed tasks
git log --oneline --since="1 week ago" --grep="feat\\|fix"

# Check current status
grep '"status":"open"' .beads/issues.jsonl | jq -r '"\(.id): \(.title)"'
```

### Tool Configuration

Ensure `pyproject.toml` contains:

```toml
[tool.ruff]
line-length = 100
target-version = "py310"

[tool.pyright]
pythonVersion = "3.10"
typeCheckingMode = "strict"

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
addopts = "-v --cov=ibdm --cov-report=term-missing"
```

## References

- **Architecture**: [`docs/architecture_principles.md`](docs/architecture_principles.md)
- **Environment**: [`docs/environment_setup.md`](docs/environment_setup.md)
- **LLM Config**: [`docs/llm_configuration.md`](docs/llm_configuration.md)
- **Larsson Algorithms**: [`docs/LARSSON_ALGORITHMS.md`](docs/LARSSON_ALGORITHMS.md)
- **Burr State Refactoring**: [`docs/burr_state_refactoring.md`](docs/burr_state_refactoring.md)

### External Links

- [uv Documentation](https://github.com/astral-sh/uv)
- [ruff Documentation](https://docs.astral.sh/ruff/)
- [pyright Documentation](https://github.com/microsoft/pyright)
- [LiteLLM Documentation](https://docs.litellm.ai/)
- [Conventional Commits](https://www.conventionalcommits.org/)

## Questions or Updates

If these policies need updating:
1. Create a beads task: `bd create "Policy question: ..."`
2. Discuss in task comments
3. Update this document with decision
4. Commit with: `docs(policy): update CLAUDE.md`