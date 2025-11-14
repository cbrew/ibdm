# Claude Development Guide for IBDM

Quick reference for AI agents working on the Issue-Based Dialogue Management (IBDM) project.

## Quick Start

```bash
# 1. Verify environment
python -c "import os; assert os.getenv('IBDM_API_KEY'), 'Missing IBDM_API_KEY'"

# 2. Check ready tasks
.claude/beads-helpers.sh ready

# 3. Before every commit
ruff format src/ tests/ && ruff check --fix src/ tests/ && pyright src/ && pytest

# 4. Commit
git commit -m "feat(scope): description"
```

## Table of Contents

- [Architecture](#architecture) - Policies 0, 10, 11, 12
- [Tooling](#tooling) - Policies 1, 2, 3, 9
- [Process](#process) - Policies 4, 5, 6, 7, 8
- [Workflow](#workflow) - Daily tasks, commits, pushing

---

## Architecture

### 0. Architectural Clarity and Simplicity (HIGHEST PRIORITY)

**Policy**: Prioritize clarity over cleverness. Avoid complexity, fallbacks, and defensive programming.

- Assume resources available (API keys, models, imports)
- Single path execution (no cascading fallbacks)
- Explicit state management (all state in Burr, engines are pure functions)
- Minimal error handling (fail fast, log clearly)
- Direct configuration (no feature flags)

📖 **Details**: [`docs/architecture_principles.md`](docs/architecture_principles.md)

### 10. Domain Semantic Layer

**Policy**: Define predicates, sorts, and semantic operations explicitly using domain models.

- Use `src/ibdm/core/domain.py` for domain definitions
- Register plan builders with `domain.register_plan_builder()`
- Use `domain.get_plan()` not hardcoded plans
- Map NLU entities to domain predicates

**Why**: Increased Larsson fidelity from ~85% to ~95%

### 11. Task Plan Formation in Integration Phase

**Policy**: Create dialogue plans in INTEGRATION phase, not interpretation.

- **INTERPRET**: Utterance → DialogueMove (syntactic/semantic only)
- **INTEGRATE**: DialogueMove → State updates + plan formation
- **SELECT**: Choose next system move
- **GENERATE**: Produce natural language

### 12. Larsson Algorithmic Principles

**Policy**: Implementation MUST follow Larsson (2002) algorithms.

- QUD is a stack (LIFO), not a set
- Single rule application per update cycle
- Explicit state passing (no hidden state)
- Questions accommodated (`private.issues`) before raised (`shared.qud`)
- Domain-independent rules

📖 **Details**: [`docs/LARSSON_ALGORITHMS.md`](docs/LARSSON_ALGORITHMS.md)

---

## Tooling

### 1. Dependency Management: uv

```bash
uv pip install --system -e ".[dev]"          # Install dependencies
uv pip install --system <package>            # Add package (then update pyproject.toml)
```

### 2. Formatting: ruff

```bash
ruff format src/ tests/                      # Format code
ruff check --fix src/ tests/                 # Check and fix issues
```

### 3. Type Checking: pyright

```bash
pyright                                      # Type check entire project
pyright src/ibdm/core/                       # Type check specific module
```

**Config**: `pyproject.toml` sets `typeCheckingMode = "strict"`

### 9. LLM Provider: LiteLLM

**Policy**: Use LiteLLM with Claude models. Always pass `api_key=os.getenv("IBDM_API_KEY")`.

- **Sonnet 4.5** (`claude-sonnet-4-5-20250929`) - Complex reasoning, generation, multi-step tasks
- **Haiku 4.5** (`claude-haiku-4-5-20251001`) - Classification, control flow, structured data
- No fallbacks to Gemini/OpenAI

📖 **Details**: [`docs/llm_configuration.md`](docs/llm_configuration.md), [`docs/environment_setup.md`](docs/environment_setup.md)

---

## Process

### 4. Small Commits

**Policy**: One logical change per commit (~300 lines max).

- Format: `<type>(<scope>): <description>`
- Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`, `ci`
- Good: `feat(core): add WhQuestion class with tests`
- Bad: `WIP`, `fix stuff`, `updates`

### 5. Test After Every Commit

**Policy**: Run tests before committing.

```bash
pytest tests/unit/test_questions.py -v       # Run relevant tests
pytest                                       # Run full suite
```

### 6. Document via Beads

**Policy**: Track design decisions and tasks in beads.

```bash
.claude/beads-helpers.sh ready               # Check ready tasks
.claude/beads-helpers.sh start <task-id>     # Start task
.claude/beads-helpers.sh done <task-id> "msg" # Complete task
```

### 7. Own All Code Quality Issues

**Policy**: Fix all quality issues in files you touch, regardless of when introduced.

- Never say "pre-existing issues"
- Fix issues in your changes + same function
- If too many, create beads task for cleanup

### 8. Work Step by Step

**Policy**: Break work into small, verifiable steps.

**Red-Green-Refactor**:
1. Write failing test
2. Write minimal code to pass
3. Refactor code quality
4. Commit each step

---

## Workflow

### Daily Session

```bash
# 1. Check and start task
.claude/beads-helpers.sh ready
.claude/beads-helpers.sh start <task-id>

# 2. Work loop (repeat for each step)
#    - Write test → Implement → Run test
#    - Format, check, type check
#    - Commit

# 3. Before each commit
ruff format src/ tests/ && ruff check --fix src/ tests/
pyright src/
pytest

# 4. Commit
git commit -m "feat(scope): description"

# 5. Complete task
.claude/beads-helpers.sh done <task-id> "message"
```

### Before Pushing

```bash
pytest                          # All tests
ruff format src/ tests/         # Format
ruff check src/ tests/          # Lint
pyright src/                    # Type check
git push
```

### Project-Specific Notes

- **Container**: Podman (not Docker)
- **API Key**: `IBDM_API_KEY` (not `ANTHROPIC_API_KEY`)
- **No `sys.path` manipulations** - Use `uv` and `pyproject.toml`
- **Don't run Textual apps** - They make a mess

---

## References

### Documentation
- [`docs/architecture_principles.md`](docs/architecture_principles.md) - Policy #0 details
- [`docs/environment_setup.md`](docs/environment_setup.md) - Environment and API keys
- [`docs/llm_configuration.md`](docs/llm_configuration.md) - LLM integration guide
- [`docs/LARSSON_ALGORITHMS.md`](docs/LARSSON_ALGORITHMS.md) - Larsson compliance
- [`docs/burr_state_refactoring.md`](docs/burr_state_refactoring.md) - State design

### External Links
- [uv](https://github.com/astral-sh/uv) | [ruff](https://docs.astral.sh/ruff/) | [pyright](https://github.com/microsoft/pyright)
- [LiteLLM](https://docs.litellm.ai/) | [Conventional Commits](https://www.conventionalcommits.org/)

### Updates

To update these policies:
1. Create beads task: `bd create "Policy question: ..."`
2. Update document with decision
3. Edit CLAUDE.md only (AGENTS.md is auto-synced via pre-commit hook)
4. Commit: `docs(policy): update CLAUDE.md`

**Note**: AGENTS.md is automatically synchronized from CLAUDE.md via `.claude/sync-docs.sh` on every commit. Always edit CLAUDE.md, not AGENTS.md.
