# Claude Development Guide for IBDM

Quick reference for AI agents working on the Issue-Based Dialogue Management (IBDM) project.

## Quick Start

```bash
# 0. Setup environment (ALWAYS RUN FIRST - at start of every session)
uv pip install --system -e .

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

- [Architecture](#architecture) - Policies 0, 10, 11, 12, 14
- [Tooling](#tooling) - Policies 1, 2, 3, 9
- [Process](#process) - Policies 4, 5, 6, 7, 8, 13, 15
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

#### NO SILENT FALLBACKS (CRITICAL)

**Rule**: NEVER use silent fallbacks. If something fails, raise an exception or log an error loudly. Silent fallbacks hide bugs and make debugging impossible.

**Examples of FORBIDDEN patterns**:
```python
# ❌ NEVER DO THIS - Silent fallback
try:
    result = parse_question(text)
except:
    result = text  # Silent fallback - hides the bug!

# ❌ NEVER DO THIS - Silent fallback with None check
result = parse_question(text)
if result is None:
    result = text  # Silent fallback - hides the bug!

# ✅ DO THIS - Fail fast with clear error
result = parse_question(text)
if result is None:
    raise ValueError(f"Failed to parse question: {text!r}")

# ✅ OR THIS - Log loudly and fail
result = parse_question(text)
if result is None:
    logger.error(f"CRITICAL: Failed to parse question: {text!r}")
    raise ValueError(f"Cannot proceed without valid question")
```

**Why this matters**:
- Silent fallbacks hide bugs that should be fixed
- Makes it impossible to know when something is broken
- Creates "working but wrong" behavior
- Wastes debugging time trying to figure out why output is wrong

**When you think about adding a fallback, DON'T. Fix the root cause instead.**

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

### 14. ZFC Principles: Selective Compliance

**Policy**: Use Zero Framework Cognition (ZFC) for language processing, intentionally violate it for dialogue management.

**ZFC says**: "Delegate ALL reasoning to external AI"
**IBDM says**: "Implement Larsson's algorithms explicitly"

**These are opposite philosophies - we use both selectively.**

#### ✅ Use ZFC For: Language & Infrastructure

**NLU/NLG** (Delegate to AI):
- ✅ DO: Delegate utterance interpretation to Claude 4.5
- ✅ DO: Delegate text generation to templates/LLM
- ❌ DON'T: Keyword matching, fallback heuristics, template selection logic

**Infrastructure** (Pure orchestration):
- ✅ DO: Burr state machine (mechanical execution)
- ✅ DO: Structural validation (schema, types)
- ❌ DON'T: Decision logic in orchestration

#### ❌ Violate ZFC For: Dialogue Management

**Update Rules** (INTENTIONAL VIOLATION):
- ✅ DO: Implement Larsson's algorithms explicitly
- ✅ DO: Semantic reasoning (domain.resolves)
- ✅ DO: Priority-based rule selection
- **Why**: This IS the research contribution

**Semantic Operations** (INTENTIONAL VIOLATION):
- ✅ DO: domain.resolves(answer, question)
- ✅ DO: Type matching, semantic validation
- **Why**: Larsson Section 2.4.3 defines these

**QUD & Plans** (INTENTIONAL VIOLATION):
- ✅ DO: Explicit stack operations (push, pop)
- ✅ DO: Plan progression logic
- **Why**: Core IBDM structures must be transparent

#### The Boundary

```
Language (ZFC) → Dialogue Semantics (NOT ZFC) → Language (ZFC)
   ↑ AI              ↑ Larsson Algorithms           ↑ AI
```

#### Why We Violate

**Violations are intentional** because:
1. Research goal: Demonstrate Larsson's algorithms work
2. Transparency: Dialogue behavior must be inspectable
3. Validation: Can measure fidelity to Larsson (2002)

**Philosophy**: "Use AI for what humans are bad at (language). Use explicit algorithms for what we understand (dialogue)."

📖 **Details**: [`reports/zfc-analysis-ibdm.md`](reports/zfc-analysis-ibdm.md)

---

## Tooling

### 0. Environment Setup: ALWAYS RUN FIRST

**Policy**: Run setup at the start of EVERY session to ensure all dependencies are installed.

```bash
uv pip install --system -e .                 # Install all dependencies (RUN THIS FIRST!)
```

**What this does**:
- Installs the project in editable mode from `pyproject.toml`
- Installs all runtime dependencies (burr, pydantic, litellm, rich, graphviz)
- Installs all dev tools (pytest, pyright, ruff, ipython, jupyter)
- Makes `ibdm` package importable from anywhere

**Why this matters**: Without this, you'll get "module not found" errors and waste time debugging imports.

### 1. Dependency Management: uv

```bash
uv pip install --system -e .                 # Install dependencies (see Policy #0 above)
uv pip install --system <package>            # Add package (then update pyproject.toml)
```

### 2. Formatting: ruff

```bash
ruff format src/ tests/                      # Format code
ruff check --fix src/ tests/                 # Check and fix issues
```

### 3. Type Checking: pyright

**Policy**: Type errors are indicators of bad code and MUST be fixed. Zero tolerance for type errors in code you write or modify.

```bash
pyright                                      # Type check entire project
pyright src/ibdm/core/                       # Type check specific module
```

**Config**: `pyproject.toml` sets `typeCheckingMode = "strict"`

**Requirements**:
- ALL new code must pass pyright with zero errors
- When modifying existing code, fix ALL type errors in functions/classes you touch
- Type errors indicate design problems: incomplete error handling, missing None checks, unclear types
- Never suppress type errors with `# type: ignore` without understanding and documenting why
- For type errors in code you don't touch, an effort to fix the error is still appreciated

**Common Issues & Fixes**:
- `reportOptionalMemberAccess`: Check for None before accessing attributes (`if obj is not None: obj.attr`)
- `reportUnknownVariableType`: Add proper type annotations to variables and function parameters
- `reportUnnecessaryIsInstance`: Remove redundant type checks after earlier isinstance() calls
- `reportUnknownArgumentType`: Ensure function parameters have proper type annotations

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

### 6. Document via Beads with Larsson Tracking

**Policy**: Track design decisions and tasks in beads with automatic Larsson alignment measurement.

**Larsson-Tracked Workflow** (PREFERRED):
```bash
.claude/beads-larsson.sh start <task-id>     # Start task (auto baseline + prediction prompt)
# ... work on task ...
.claude/beads-larsson.sh complete <task-id>  # Complete task (auto final + review)
```

**Standard Beads Commands** (untracked):
```bash
.claude/beads-helpers.sh ready               # Check ready tasks
.claude/beads-helpers.sh current             # Show in-progress tasks
.claude/beads-helpers.sh summary             # Project summary
```

**How Larsson Tracking Works**:
1. `start <task-id>`: Generates baseline fidelity report, prompts for prediction
2. Work on task with normal git workflow
3. `complete <task-id>`: Generates final report, compares with baseline, reviews prediction

All reports tagged with timestamp and git hash in `reports/` directory.

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

### 15. Update NEXT-TASK.md After Completing Tasks

**Policy**: When you complete tasks from NEXT-TASK.md, update the file and communicate the plan.

**After completing tasks**:
1. Update `NEXT-TASK.md` to reflect:
   - Mark completed tasks as done (✅)
   - Update progress percentages
   - Document what was accomplished
   - Clarify what's next in the sequence
2. Tell the user what was completed and what the next steps are
3. If tasks remain, summarize the plan forward
4. If all tasks complete, suggest next logical work or ask for direction

**Why**: Keeps task tracking synchronized, maintains project momentum, and ensures clear communication about progress and next steps.

**Example**:
```
Completed Week 2 IBiS3 tasks:
- ✅ Rule 4.1 (IssueAccommodation)
- ✅ Rule 4.2 (LocalQuestionAccommodation)
- ✅ Volunteer information handling

Progress: IBiS3 35% → 50%

Next: Week 3 tasks in NEXT-TASK.md (clarification questions + dependent issues)
```

### 13. Documentation Organization

**Policy**: Maintain organized, current documentation with clear status markers.

**Active Documentation** (keep current):
- Top-level: `CLAUDE.md`, `README.md`, `GETTING_STARTED.md`, `SYSTEM_ACHIEVEMENTS.md`, `LARSSON_PRIORITY_ROADMAP.md`
- `docs/architecture/`: Architecture principles and algorithms
- `docs/configuration/`: Setup and configuration guides
- `docs/reference/`: Larsson thesis material
- `docs/INDEX.md`: Complete documentation index

**Archive Old Docs**: Move historical/completed docs to `docs/archive/` with status markers:
- `docs/archive/design-discussions/`: Architectural analysis
- `docs/archive/refactoring-plans/`: Completed refactoring plans
- `docs/archive/planning/`: Original planning documents
- `docs/archive/reviews/`: One-time reviews

**Status Markers** (use in document headers):
- **✅ CURRENT**: Actively maintained, authoritative
- **📋 HISTORICAL**: Original planning, evolved significantly
- **✅ COMPLETED**: Implementation finished, kept for reference
- **❌ DEPRECATED**: Approach superseded by new design
- **📖 REFERENCE**: Background material, still valid

**No Duplicates**: Single source of truth
- `CLAUDE.md` is canonical (top-level)
- `AGENTS.md` is auto-synced from `CLAUDE.md` (don't edit)
- Delete or merge duplicates

**Update `docs/INDEX.md`**: When adding/moving documentation

**Never Create** (unless explicitly requested):
- README files for subdirectories (use INDEX.md)
- Duplicate docs (check existing first)
- Documentation for unimplemented features (wait until implemented)

---

## Workflow

### Daily Session

```bash
# 0. Setup environment (ALWAYS RUN FIRST - at start of every session)
uv pip install --system -e .

# 1. Check and start task (with Larsson tracking)
.claude/beads-helpers.sh ready
.claude/beads-larsson.sh start <task-id>
# → Generates baseline report, prompts for prediction

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

# 5. Complete task (with Larsson review)
.claude/beads-larsson.sh complete <task-id> "message"
# → Generates final report, compares with baseline, reviews prediction
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
