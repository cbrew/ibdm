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
- `IBDM_API_KEY` - Anthropic Claude API key (primary, used for all LLM operations)
- `GEMINI_API_KEY` - Google/Gemini API key (available but not actively used)
- `OPENAI_API_KEY` - OpenAI API key (available but not actively used)

**Note**: This project primarily uses `IBDM_API_KEY` for Claude models. The other keys are available for compatibility but not recommended per Policy #9.

### .env File

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

### Verifying Environment

```python
import os

# Verify primary API key is available
ibdm_api_key = os.getenv("IBDM_API_KEY")

assert ibdm_api_key, "IBDM_API_KEY not found"

# Optional: Verify other keys if needed
# gemini_key = os.getenv("GEMINI_API_KEY")
# openai_key = os.getenv("OPENAI_API_KEY")
```

## Core Policies

### 0. Architectural Clarity and Simplicity (HIGHEST PRIORITY)

**Policy**: Clarity and simplicity are paramount in the IBDM architecture. Avoid unnecessary complexity, fallback strategies, conditional logic, and defensive programming.

**Rationale**: Complex systems are harder to understand, debug, and maintain. The IBDM project prioritizes clean, understandable code over "clever" solutions or over-engineered resilience.

**Principles**:

1. **Assume Resource Availability**
   - Assume API keys (IBDM_API_KEY) are configured and available
   - Assume models (Claude Sonnet 4.5, Claude Haiku 4.5) are accessible
   - Assume imports and dependencies are installed
   - Do NOT add fallback logic for missing resources

2. **Single Path Execution**
   - Avoid hybrid fallback strategies (rules → Haiku → Sonnet cascading)
   - Use direct model selection based on task type:
     - Claude Sonnet 4.5 for complex reasoning, generation, multi-step tasks
     - Claude Haiku 4.5 for quick classification, control flow, structured data
   - No automatic cascading between models

3. **Explicit State Management**
   - All dialogue state visible in Burr State (not hidden in engine internals)
   - Engine methods are pure functions accepting and returning state
   - No hidden mutations, no internal state
   - State transitions are explicit and traceable

4. **Minimal Error Handling**
   - Let errors propagate (fail fast)
   - Use basic logging, not complex retry/circuit breaker patterns
   - Trust that resources are available

5. **Direct Configuration**
   - Simple, flat configuration objects
   - No conditional initialization based on feature flags
   - No "use_nlu", "use_llm", "fallback_to_rules" toggles
   - Clear defaults, minimal options

**Examples**:

❌ **Avoid** (Complex fallback):
```python
if self.fallback_strategy:
    strategy = self.fallback_strategy.select_strategy(utterance, available)
    moves, confidence = self._try_strategy(strategy, utterance, speaker)
    next_strategy = self.fallback_strategy.should_cascade(strategy, ...)
    if next_strategy:
        cascade_moves, cascade_conf = self._try_strategy(next_strategy, ...)
        if cascade_conf > confidence:
            moves = cascade_moves
elif self.config.use_nlu and self.config.use_llm and self.context_interpreter:
    try:
        moves = self._interpret_with_nlu(utterance, speaker)
    except Exception as e:
        if self.config.fallback_to_rules:
            moves = super().interpret(utterance, speaker)
else:
    moves = super().interpret(utterance, speaker)
```

✅ **Prefer** (Simple direct):
```python
# Select model based on task complexity
if is_complex_task(utterance):
    interpreter = self.sonnet_interpreter
else:
    interpreter = self.haiku_interpreter

interpretation = interpreter.interpret(utterance, state)
moves = self._create_moves_from_interpretation(interpretation)
```

❌ **Avoid** (Hidden state):
```python
class DialogueMoveEngine:
    def __init__(self, agent_id: str):
        self.state = InformationState(agent_id=agent_id)  # Hidden!

    def interpret(self, utterance: str, speaker: str) -> list[DialogueMove]:
        temp_state = self.state.clone()  # Mutates self.state
        return moves
```

✅ **Prefer** (Explicit state):
```python
class DialogueMoveEngine:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        # No internal state!

    def interpret(
        self, utterance: str, speaker: str, state: InformationState
    ) -> list[DialogueMove]:
        # State passed explicitly, no hidden mutations
        temp_state = state.clone()
        return moves
```

❌ **Avoid** (Conditional complexity):
```python
@dataclass
class NLUEngineConfig:
    use_nlu: bool = True
    use_llm: bool = True
    llm_model: ModelType = ModelType.HAIKU
    confidence_threshold: float = 0.5
    fallback_to_rules: bool = True
    enable_hybrid_fallback: bool = True
    fallback_config: FallbackConfig | None = None
```

✅ **Prefer** (Simple config):
```python
@dataclass
class NLUEngineConfig:
    """Assumes IBDM_API_KEY is available."""
    model: ModelType = ModelType.SONNET
    temperature: float = 0.3
    max_tokens: int = 2000
```

**Architecture Guidelines**:

- **Burr State**: Single source of truth for all dialogue state
- **Engine**: Stateless transformation functions
- **NLU Components**: Accept context, return results (no internal state)
- **Configuration**: Simple, assume resources available
- **Error Handling**: Fail fast, log clearly, don't retry

**See Also**:
- `docs/burr_state_refactoring.md` - Complete refactoring design
- Policy #9 (LLM Provider) - Model selection guidelines
- Policy #8 (Work Step by Step) - Incremental development

### 1. Dependency Management: Use uv

**Policy**: All Python dependency management must use [uv](https://github.com/astral-sh/uv).

**Rationale**: uv provides fast, reliable dependency resolution and is designed for modern Python development.

**Commands**:
```bash
# Install dependencies from pyproject.toml
uv pip install --system -e ".[dev]"

# Add new dependency
uv pip install --system <package>
# Then add to pyproject.toml dependencies

# Reinstall to sync after pyproject.toml changes
uv pip install --system -e ".[dev]"
```

**Note**: Use `--system` flag when not in a virtual environment.

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

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]
ignore = []
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

**Note**: The beads CLI (`bd`) may not be installed. Use the helper script `.claude/beads-helpers.sh` or read `.beads/issues.jsonl` directly.

**When to Create Beads Issues**:

1. **Before Starting Work**: Check beads for ready tasks
   ```bash
   .claude/beads-helpers.sh ready
   # Or: grep '"status":"open"' .beads/issues.jsonl
   ```

2. **When Starting a Task**: Mark as in_progress
   ```bash
   .claude/beads-helpers.sh start ibdm-brm.1
   # Or manually update .beads/issues.jsonl
   ```

3. **Discovered Issues**: Document in task comments or commit messages
   - Add detailed notes in commit messages
   - Reference related task IDs
   - Document decision rationale

4. **Design Decisions**: Document in commit messages and code comments
   ```bash
   git commit -m "feat(core): use ABC for Question base class

   Decision: Using ABC to enforce resolves_with implementation across
   all Question subclasses. This provides compile-time safety.

   Related to ibdm-brm.1"
   ```

5. **Future Work**: Document in TODO comments with task references
   ```python
   # TODO(ibdm-brm.3): Optimize Question matching for large QUD stacks
   # Current O(n) scan is sufficient for <100 questions but may need
   # indexing for larger applications.
   ```

6. **Completing Work**: Use helper script
   ```bash
   .claude/beads-helpers.sh done ibdm-brm.1 "Implemented with full test coverage"
   ```

**Benefits**:
- Creates audit trail of decisions
- Enables long-term planning
- Allows context recovery after interruptions
- Facilitates collaboration between agents/developers

### 7. Own All Code Quality Issues

**Policy**: Take responsibility for all code quality issues in files you touch, regardless of when they were introduced.

**Guidelines**:
- **Never** dismiss errors as "pre-existing issues"
- If you modify a file, you own fixing any issues in that file
- Run full type checking and linting on all modified files
- Fix issues incrementally, don't let them accumulate
- If an issue is truly out of scope, create a beads task for it

**Rationale**: Dismissing issues as "pre-existing" leads to technical debt accumulation and erodes code quality over time. Every change is an opportunity to improve the codebase.

**Examples**:

❌ **Bad**:
```
"The type errors are mostly pre-existing issues. Let me just commit my changes."
```

✅ **Good**:
```
"I see type errors in the file I modified. Let me fix them:
1. Fix the immediate issues in my changes
2. Fix other issues in the same function
3. If there are many issues, create a beads task for systematic cleanup"
```

### 8. Work Step by Step

**Policy**: Break work into small, verifiable steps with frequent validation.

**Step-by-Step Workflow**:

1. **Plan**: Review beads task and break into subtasks if needed
   ```bash
   # Check task details
   grep 'ibdm-brm.1' .beads/issues.jsonl | jq '.'

   # Document subtasks in commit messages or TODO comments
   # Large tasks should be broken down into smaller, focused commits
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

7. **Update Progress**: Record in commit messages
   ```bash
   # Progress is tracked via commit messages and git history
   git log --oneline --grep="ibdm-brm.1"
   ```

**Red-Green-Refactor Pattern**:
1. **Red**: Write failing test
2. **Green**: Write minimal code to pass
3. **Refactor**: Improve code quality
4. **Commit**: Each step separately

### 9. LLM Provider Configuration: Use LiteLLM

**Policy**: All LLM integrations must use [LiteLLM](https://github.com/BerriAI/litellm) as the unified interface.

**Rationale**: LiteLLM provides a consistent API across multiple providers, simplifies switching between models, and handles rate limiting and error handling.

**Model Selection**:
1. **Primary Models**: Anthropic Claude 4.5 series
   - `claude-sonnet-4-5-20250929` - For large-scale generation tasks, complex reasoning, and extended responses
   - `claude-haiku-4-5-20251001` - For control flow, analytics, quick classification, and structured data tasks
2. **No Fallback**: Do not use Google Gemini or OpenAI as fallbacks

**Usage Guidelines**:
- Use `claude-sonnet-4-5-20250929` for:
  - Content generation (essays, reports, creative writing)
  - Complex reasoning and problem-solving
  - Multi-step analysis
  - Summarization of long documents
  - Complex agents and coding tasks
- Use `claude-haiku-4-5-20251001` for:
  - Classification and categorization
  - Control flow decisions
  - Analytics and metrics
  - Quick question answering
  - Structured data extraction
  - Cost-sensitive applications (fastest model with near-frontier intelligence)

**API Keys**:
- API keys are provided via environment variables
- `IBDM_API_KEY` for Anthropic Claude models (primary)
  - Must be passed explicitly as `api_key` parameter to LiteLLM calls
  - This separate env var prevents billing conflicts with Claude Code's own Claude usage
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
assert os.getenv("IBDM_API_KEY"), "IBDM_API_KEY not found in environment"
```

**Configuration**:
```python
import os
import litellm
from litellm import completion

# Set default provider
litellm.set_verbose = False  # Set to True for debugging

# Get API key from environment
api_key = os.getenv("IBDM_API_KEY")

# Example usage - Large-scale generation
response = completion(
    model="claude-sonnet-4-5-20250929",
    messages=[{"role": "user", "content": "Write a detailed analysis..."}],
    api_key=api_key,  # Explicitly pass API key
    temperature=0.7,
    max_tokens=8000
)

# Example usage - Control and analytics
response = completion(
    model="claude-haiku-4-5-20251001",
    messages=[{"role": "user", "content": "Classify this text..."}],
    api_key=api_key,  # Explicitly pass API key
    temperature=0.3,
    max_tokens=500
)
```

**Implementation Guidelines**:
- Use LiteLLM's unified interface for all LLM calls
- **Always** pass `api_key=os.getenv("IBDM_API_KEY")` explicitly to avoid env var conflicts
- Select the appropriate Claude model based on task type (see Usage Guidelines above)
- Use `claude-sonnet-4-5-20250929` as the default for most tasks
- Use `claude-haiku-4-5-20251001` for quick, structured tasks to optimize cost and latency
- Use async operations where possible: `await acompletion(..., api_key=api_key)`
- Configure timeouts and retries through LiteLLM
- Monitor token usage and costs
- Pricing: Sonnet 4.5 ($3/$15 per million tokens), Haiku 4.5 ($1/$5 per million tokens)

**Benefits**:
- Single interface for multiple providers
- Easy model switching without code changes
- Built-in retry logic and error handling
- Cost tracking and monitoring
- Support for streaming responses

### 10. Domain Semantic Layer

**Policy**: All domains must define predicates, sorts, and semantic operations explicitly using the domain model abstraction.

**Rationale**: Per Larsson (2002) and py-trindikit analysis, domain abstraction is integral to IBDM. It provides semantic grounding, type safety, and enables domain-independent rules. Without explicit domain models, predicates are magic strings with no semantic meaning.

**Key Finding**: The py-trindikit analysis (November 2024) revealed that Larsson's original IBDM implementation included a sophisticated domain abstraction layer that was missing from our implementation. Adding this layer increased Larsson fidelity from ~85% to ~95%.

**Implementation**:
- Define domain model with predicates and sorts (see `src/ibdm/core/domain.py`)
- Register plan builders with domain using `domain.register_plan_builder()`
- Use `domain.get_plan()` not hardcoded plans in rules
- Use `domain.resolves()` for type-checked answer validation
- Map NLU entities to domain predicates using domain mapper

**Example: NDA Domain** (`src/ibdm/domains/nda_domain.py`):

```python
from ibdm.core.domain import DomainModel

def create_nda_domain() -> DomainModel:
    domain = DomainModel(name="nda_drafting")

    # Define predicates with types and descriptions
    domain.add_predicate(
        "legal_entities",
        arity=1,
        arg_types=["organization_list"],
        description="Organizations entering into the NDA"
    )

    domain.add_predicate(
        "nda_type",
        arity=1,
        arg_types=["nda_kind"],
        description="Type of NDA (mutual or one-way)"
    )

    # Define semantic sorts (valid values)
    domain.add_sort("nda_kind", ["mutual", "one-way", "unilateral"])
    domain.add_sort("us_state", ["California", "Delaware", "New York"])

    # Register plan builder
    domain.register_plan_builder("nda_drafting", _build_nda_plan)

    return domain
```

**Benefits**:
- **Semantic grounding**: Predicates have meaning, not just strings
- **Type safety**: Domain validates answers against sorts
- **Reusability**: Rules work across domains
- **Extensibility**: Easy to add new domains
- **Larsson fidelity**: Matches original IBDM architecture

**Architecture**:
```
NLU Layer → Domain Model → IBDM Rules → NLG Layer
            ↓
    - Predicates (typed)
    - Sorts (valid values)
    - Plan builders
    - Semantic operations
```

### 11. Task Plan Formation in Integration Phase

**Policy**: Task plan formation (creating dialogue plans for user tasks) belongs in the INTEGRATION phase, not interpretation or accommodation.

**Rationale**: Larsson's IBDM has a clear four-phase architecture. Interpretation is syntactic/semantic (utterance → dialogue move). Integration is pragmatic (dialogue move → state updates, including plan formation). Mixing these phases creates architectural confusion.

**Terminology Clarification**:
- ✅ **Task Plan Formation**: Creating plans in response to user task requests (e.g., "I need an NDA" → create findout plan)
- ❌ **Accommodation**: Larsson's "accommodation" refers to presupposition accommodation (different concept)
- Use "task plan formation" NOT "accommodation" in code and docs

**Implementation**:

1. **Interpretation Phase** (`interpretation_rules.py`):
   - Parse utterance → DialogueMove
   - Syntactic/semantic only
   - No plan creation

   ```python
   # ✅ Correct: Create dialogue move
   move = DialogueMove(type="command", content=utterance, speaker=speaker)

   # ❌ Wrong: Don't create plans here
   # plan = create_nda_plan()  # NO!
   ```

2. **Integration Phase** (`integration_rules.py`):
   - Process dialogue moves → update state
   - Form task plans via domain model
   - Push questions to QUD

   ```python
   # ✅ Correct: Form task plan in integration
   def _form_task_plan(state: InformationState) -> InformationState:
       from ibdm.domains.nda_domain import get_nda_domain
       domain = get_nda_domain()
       plan = domain.get_plan("nda_drafting", context={})
       new_state.private.plan.append(plan)

       # Push first question to QUD
       if plan.subplans and len(plan.subplans) > 0:
           first_question = plan.subplans[0].content
           new_state.shared.push_qud(first_question)

       return new_state
   ```

**Example Workflow: "I need an NDA"**

1. **INTERPRET**: `"I need an NDA"` → `DialogueMove(type="command", content="draft NDA")`
2. **INTEGRATE**:
   - Recognize task request
   - Use domain: `plan = domain.get_plan("nda_drafting")`
   - Push first question to QUD
3. **SELECT**: Choose to ask question from QUD
4. **GENERATE**: Produce natural language question

**Benefits**:
- Clear phase separation (Larsson compliant)
- Domain-driven plan creation
- Reusable integration rules
- No mixing of syntactic and pragmatic processing

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

# Review completed tasks via git log
git log --oneline --since="1 week ago" --grep="feat\\|fix"

# Check current task status
grep '"status":"open"' .beads/issues.jsonl | jq -r '"\(.id): \(.title)"'

# Plan next priorities
.claude/beads-helpers.sh ready
```

## Tool Configuration

### pyproject.toml

Ensure these sections exist:

```toml
[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

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
