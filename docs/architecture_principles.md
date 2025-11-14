# IBDM Architecture Principles

This document provides detailed guidelines for maintaining architectural clarity and simplicity in the IBDM project.

## Core Principle

**Clarity and simplicity are paramount.** Avoid unnecessary complexity, fallback strategies, conditional logic, and defensive programming.

## Why Simplicity Matters

Complex systems are harder to understand, debug, and maintain. The IBDM project prioritizes clean, understandable code over "clever" solutions or over-engineered resilience.

## Five Key Principles

### 1. Assume Resource Availability

**Don't write defensive code for missing resources.**

- Assume API keys (IBDM_API_KEY) are configured and available
- Assume models (Claude Sonnet 4.5, Claude Haiku 4.5) are accessible
- Assume imports and dependencies are installed
- Do NOT add fallback logic for missing resources

**Rationale**: If resources are missing, fail fast with a clear error rather than cascading through fallback strategies.

### 2. Single Path Execution

**Avoid hybrid fallback strategies and cascading model calls.**

- Use direct model selection based on task type:
  - Claude Sonnet 4.5 for complex reasoning, generation, multi-step tasks
  - Claude Haiku 4.5 for quick classification, control flow, structured data
- No automatic cascading between models
- No rules → Haiku → Sonnet fallback chains

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

### 3. Explicit State Management

**All dialogue state must be visible in Burr State, not hidden in engine internals.**

- Engine methods are pure functions accepting and returning state
- No hidden mutations, no internal state
- State transitions are explicit and traceable

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

### 4. Minimal Error Handling

**Let errors propagate (fail fast).**

- Use basic logging, not complex retry/circuit breaker patterns
- Trust that resources are available
- Clear error messages over silent fallbacks

**Rationale**: Hidden failures and silent fallbacks make debugging nearly impossible. Explicit failures reveal configuration problems immediately.

### 5. Direct Configuration

**Keep configuration simple and flat.**

- Simple, flat configuration objects
- No conditional initialization based on feature flags
- No "use_nlu", "use_llm", "fallback_to_rules" toggles
- Clear defaults, minimal options

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

## Architecture Guidelines

Apply these principles across all components:

- **Burr State**: Single source of truth for all dialogue state
- **Engine**: Stateless transformation functions
- **NLU Components**: Accept context, return results (no internal state)
- **Configuration**: Simple, assume resources available
- **Error Handling**: Fail fast, log clearly, don't retry

## Related Documentation

- `docs/burr_state_refactoring.md` - Complete refactoring design
- `docs/llm_configuration.md` - Model selection and LLM setup
- `CLAUDE.md` - Development policies (Policy #0)