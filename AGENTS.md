# Claude Development Guide for IBDM

Quick reference for AI agents working on the Issue-Based Dialogue Management (IBDM) project.

**⚠️ KEY INFORMATION FOR AI ASSISTANTS**:
- **Beads** (`bd` command) is YOUR task tracking tool, automatically installed by SessionStart
- YOU use beads commands like `.claude/beads-helpers.sh ready` to track YOUR work
- The human user does NOT use beads - it's for AI assistants only
- All beads commands in this guide are for YOU to execute, not the user

## Quick Start

```bash
# 0. Setup is automatic (SessionStart hook runs at session start)
#    Installs all dependencies and verifies environment

# 1. Check ready tasks
.claude/beads-helpers.sh ready

# 2. Before every commit
ruff format src/ tests/ && ruff check --fix src/ tests/ && pyright src/ && pytest

# 3. Commit
git commit -m "feat(scope): description"
```

## Table of Contents

- [Architecture](#architecture) - Policies 0, 10, 11, 12, 14
- [Tooling](#tooling) - Policies 1, 2, 3, 9
- [Process](#process) - Policies 4, 5, 6, 7, 8, 13, 15, 16, 17
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

### 0. Environment Setup: AUTOMATIC

**Policy**: The SessionStart hook automatically runs setup at the start of EVERY session.

**What it does** (`.claude/SessionStart`):
- Installs the project in editable mode from `pyproject.toml`
- Installs all runtime dependencies (burr, pydantic, litellm, rich, graphviz)
- Installs all dev tools (pytest, pyright, ruff, ipython, jupyter)
- Installs beads task tracker (`bd` command)
- Makes `ibdm` package importable from anywhere
- Verifies core imports and tools work
- Checks API key configuration

**Manual setup** (if needed):
```bash
uv pip install --system -e .                 # Install all dependencies
```

**Why this matters**: Without proper setup, you'll get "module not found" errors and waste time debugging imports.

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

### 4. Debugging with Logging

**Policy**: Use structured logging to trace dialogue engine execution. Logging is controlled via `IBDM_DEBUG` environment variable.

```bash
# Enable all debug logging
export IBDM_DEBUG=all

# Enable specific categories
export IBDM_DEBUG=rules                      # Rule evaluation only
export IBDM_DEBUG=qud                        # QUD stack operations only
export IBDM_DEBUG=phases                     # Dialogue phases only
export IBDM_DEBUG=rules,qud                  # Multiple categories

# Disable debug logging (default)
unset IBDM_DEBUG
```

**What's logged**:
- **phases**: INTERPRET → INTEGRATE → SELECT → GENERATE phases
- **rules**: Rule evaluation (✓/✗), selection, execution
- **qud**: QUD stack operations (PUSH/POP with depth)
- **state**: State transitions and modifications

**Example output** (with `IBDM_DEBUG=all`):
```
[INFO] ibdm.engine.dialogue_engine: Processing input from user: What's the NDA type?
[DEBUG] ibdm.engine.dialogue_engine: [INTERPRET] Starting interpretation phase
[DEBUG] ibdm.rules.update_rules: Evaluating 11 interpretation rules
[DEBUG] ibdm.rules.update_rules:   ✓ interpret_answer (priority=10)
[INFO] ibdm.rules.update_rules:   → Executing rule: interpret_answer
[DEBUG] ibdm.rules.update_rules:   ← Rule completed: interpret_answer
[DEBUG] ibdm.engine.dialogue_engine: [INTERPRET] Generated 1 move(s): ['answer']
[DEBUG] ibdm.engine.dialogue_engine: [INTEGRATE] Integrating move 1/1: answer
[DEBUG] ibdm.rules.update_rules: Evaluating 16 integration rules
[DEBUG] ibdm.rules.update_rules:   ✗ form_task_plan (priority=14)
[DEBUG] ibdm.rules.update_rules:   ✗ accommodate_issue_from_plan (priority=13)
[DEBUG] ibdm.rules.update_rules:   ✓ integrate_answer (priority=8)
[INFO] ibdm.rules.update_rules:   → Executing rule: integrate_answer
[DEBUG] ibdm.core.information_state: QUD POP: AltQuestion(alternatives=['mutual', 'one-way']) (depth: 0)
[DEBUG] ibdm.rules.update_rules:   ← Rule completed: integrate_answer
[INFO] ibdm.engine.dialogue_engine: Processing complete. Response: None
```

**Configuration**:
- Logging is configured automatically on module import
- Default level: WARNING (quiet unless `IBDM_DEBUG` is set)
- Uses Python standard logging module
- See `src/ibdm/config/debug_config.py` for implementation

**When to use**:
- Debugging dialogue flow issues
- Understanding which rules fire and why
- Tracing QUD stack evolution
- Investigating state transitions
- Validating Larsson algorithm implementation

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

**IMPORTANT FOR AI ASSISTANTS**: Beads is YOUR tool, not the user's tool. YOU (the AI assistant) use beads to track YOUR work. The human user does NOT use beads commands. When you see beads commands in this guide, they are instructions for YOU to execute, not suggestions for the user.

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

### 16. Scenario Alignment: Implementation Demonstrates Larsson, Scenarios Document Implementation

**Policy**: Implementation must properly demonstrate Larsson's algorithms. Scenarios then document that correct implementation.

**Key Principles**:
- **Implementation first**: Code must correctly implement Larsson (2002) algorithms before scenarios document it
- **Scenarios second**: Scenarios demonstrate what the working implementation actually does
- **Fix incomplete implementations**: If implementation doesn't properly demonstrate a Larsson rule, fix the implementation first
- **Then align scenarios**: Update scenarios to match the corrected implementation
- **Not prescriptive**: We are NOT committed to guessed state changes in existing scenarios

**Priority Order**:
1. Ensure implementation correctly demonstrates Larsson algorithms
2. If implementation is incomplete/incorrect, fix it
3. Run implementation with `IBDM_DEBUG=all` to observe behavior
4. Document observed behavior in scenario state_changes
5. Scenarios now accurately demonstrate the Larsson algorithm

**When working with scenarios**:

1. **Creating new scenarios**: Run with `IBDM_DEBUG=all`, observe actual behavior, document what happens
2. **Updating scenarios**: Verify implementation is correct per Larsson, then update scenario to match
3. **Fixing bugs**: Fix implementation first, then update scenarios to reflect fix
4. **Finding mismatches**: Check if implementation or scenario is wrong; fix implementation if needed

**Quick workflow**:
```bash
# Debug and observe behavior
export IBDM_DEBUG=all
python scripts/run_scenario.py <scenario> --step

# Implementation correct but scenario wrong?
vim demos/scenarios/<scenario>.json           # Update state_changes
git commit -m "docs(scenarios): align with implementation"

# Implementation wrong?
vim src/ibdm/rules/update_rules.py           # Fix implementation
pytest                                        # Verify fix
vim demos/scenarios/<scenario>.json           # Update scenario
git commit -m "fix(rules): correct behavior"
git commit -m "docs(scenarios): update for fix"
```

📖 **Details**: [`docs/SCENARIO_ALIGNMENT.md`](docs/SCENARIO_ALIGNMENT.md)

🔧 **Skill**: [`.claude/skills/scenario-alignment.md`](.claude/skills/scenario-alignment.md) - Use this skill to align scenarios incrementally in small, trackable steps (avoids API errors)

**Why**: Ensures scenarios accurately document system behavior and remain useful as demonstrations after implementation evolves.

**⚠️ CRITICAL INSTRUCTION FOR AI ASSISTANTS**:
**BEFORE working on ANY scenario-related task, you MUST:**
1. **USE** the Scenario Alignment Skill (`.claude/skills/scenario-alignment.md`) for incremental work
2. **READ** `docs/SCENARIO_ALIGNMENT.md` in full for philosophy and procedures
3. **FOLLOW** the step-by-step procedures for your task type (A, B, C, or D)
4. **NEVER** guess state changes - always observe with `IBDM_DEBUG=all`
5. **VERIFY** implementation correctness per Larsson (2002) before updating scenarios
6. **COMMIT** implementation fixes and scenario updates separately

**This is NOT optional.** Failure to follow SCENARIO_ALIGNMENT.md leads to incorrect documentation and wasted debugging time.

### 17. Always Verify Before Claiming Fixes (ZERO TOLERANCE)

**Policy**: NEVER claim scenarios are fixed without actually running them and verifying they work. This is non-negotiable.

**MANDATORY Requirements** (NO EXCEPTIONS):
- ❌ FORBIDDEN: Claiming "I've fixed the issues" without verification
- ❌ FORBIDDEN: Saying "the scenario should now work" without testing
- ❌ FORBIDDEN: Making edits and assuming they're correct

### 18. All Scenarios Must Run Through Live Dialogue Engine

**Policy**: ALL scenarios must execute through the actual dialogue engine. No pre-scripted demonstrations.

**Requirements**:
- ✅ REQUIRED: Scenarios execute via `python scripts/run_scenario.py <scenario>` through the live dialogue engine
- ✅ REQUIRED: User utterances processed by actual NLU/interpretation rules
- ✅ REQUIRED: System responses generated by actual dialogue engine (INTEGRATE → SELECT → GENERATE phases)
- ✅ REQUIRED: State changes reflect actual rule execution, not guessed behavior
- ❌ FORBIDDEN: Pre-scripted system responses that bypass the dialogue engine
- ❌ FORBIDDEN: Hardcoded responses that don't go through rule evaluation
- ❌ FORBIDDEN: "Demonstration only" scenarios that don't test real implementation

**Why**: Scenarios serve as both documentation AND integration tests. Pre-scripted scenarios cannot verify implementation correctness and will drift from reality.

**How to verify**:
```bash
# Run with debug to see actual rule execution
export IBDM_DEBUG=all
python scripts/run_scenario.py <scenario> --step

# Look for rule evaluation logs (proves live execution)
# Should see: "[DEBUG] Evaluating X rules", "[INFO] → Executing rule: Y"
# Should NOT see: pre-written responses with no rule logs
```

**If scenario is pre-scripted**: Create beads task to implement live version
- ✅ REQUIRED: Run `python scripts/run_scenario.py <scenario>` BEFORE claiming success
- ✅ REQUIRED: Check for JSON syntax errors with the scenario runner
- ✅ REQUIRED: Verify compliance passes (or report actual failures)
- ✅ REQUIRED: Report actual test results, not assumptions

**Why This Matters**:
- Unverified claims waste user time
- Users discover errors you should have caught
- Erodes trust when you claim fixes that don't work
- Shows you didn't actually test your work
- JSON syntax errors are caught instantly by the scenario runner

**Correct Workflow** (MANDATORY):
```bash
# 1. Make changes to implementation or scenario
vim src/ibdm/rules/update_rules.py
vim demos/scenarios/nda_comprehensive.json

# 2. ALWAYS verify IMMEDIATELY after editing
python scripts/run_scenario.py nda_comprehensive

# 3a. If scenario runner fails with JSON error, fix it immediately
# Example: "Error loading scenario: Invalid JSON... Expecting value: line 14"
# → Fix the JSON syntax error at line 14
# → Re-run to verify: python scripts/run_scenario.py nda_comprehensive

# 3b. If compliance fails, investigate and fix the real issues
# Report: "I ran the scenario and found mismatches on turns X, Y, Z. Investigating..."

# 3c. ONLY if verification succeeds, then commit
git commit -m "fix(scenarios): resolve state mismatches in nda_comprehensive"
```

**Communication Rules**:
- ❌ NEVER: "I've fixed the issues" (without verification)
- ✅ ALWAYS: "Let me verify the fix" → run scenario → report actual results
- ❌ NEVER: "This should work now" (assumption)
- ✅ ALWAYS: "I've verified it works: [paste actual results]"
- ❌ NEVER: Skip verification because "it's just a small change"
- ✅ ALWAYS: Test even trivial changes (JSON syntax errors count as failures)

**Special Case - JSON Syntax Errors**:
JSON syntax errors (trailing commas, missing brackets, etc.) are caught IMMEDIATELY by the scenario runner. There is NO EXCUSE for not catching these before claiming a fix. Always run the scenario after editing JSON files.

**Zero Tolerance**: If you claim a fix without verification, you have failed the task regardless of whether the fix was correct.

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

**NOTE**: The commands below are for YOU (the AI assistant) to execute during your work. These are not instructions for the user.

### Daily Session

```bash
# 0. Setup environment (ALWAYS RUN FIRST - at start of every session)
uv pip install --system -e .

# 1. Check and start task (with Larsson tracking) - YOU run these commands
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
- [`docs/SCENARIO_ALIGNMENT.md`](docs/SCENARIO_ALIGNMENT.md) - Policy #16 details (scenarios follow implementation)
- [`docs/UNIFIED_SCENARIO_SYSTEM.md`](docs/UNIFIED_SCENARIO_SYSTEM.md) - Scenario system usage
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
