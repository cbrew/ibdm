# Burr-Centric State Management Refactoring

**Author**: Claude
**Date**: 2025-11-12
**Status**: Design Phase
**Related**: Phase 2 Burr Integration (ibdm-zfl)

## Executive Summary

This document describes a refactoring to move **all dialogue state** under Burr management, transforming the current hybrid architecture into a clean, Burr-centric design where the dialogue engine becomes a stateless processor and Burr State becomes the single source of truth.

## Current Architecture

### State Management Split

Currently, dialogue state is split across two locations:

1. **Burr State** (superficial orchestration state):
   - `utterance`: Current input text
   - `speaker`: Current speaker ID
   - `moves`: Interpreted dialogue moves
   - `integrated`: Boolean flag
   - `response_move`: Selected response
   - `has_response`: Boolean flag
   - `utterance_text`: Generated output
   - `engine`: Reference to stateful engine object

2. **Engine Internal State** (deep dialogue state):
   - `InformationState` containing:
     - `private`: Private beliefs, plans, agenda
     - `shared`: QUD stack, commitments, last moves
     - `control`: Turn-taking, initiative, dialogue state
   - NLU components: EntityTracker, ReferenceResolver state
   - Fallback strategy statistics

### Current Flow

```
Burr State                           Engine
┌──────────────┐                    ┌──────────────────┐
│ utterance    │────────────────────>│ interpret()      │
│ speaker      │                     │   reads:         │
│ engine ──────┼────────────────────>│     self.state   │
└──────────────┘                     │   modifies:      │
                                     │     self.state   │
      │                              │   returns: moves │
      │                              └──────────────────┘
      │                                      │
      v                                      │
┌──────────────┐                            │
│ moves ◄──────┼────────────────────────────┘
└──────────────┘
```

### Problems with Current Architecture

1. **Incomplete State Capture**: Burr persistence only saves surface state, not InformationState
2. **Hidden Mutations**: Engine mutates its own state, invisible to Burr
3. **Rollback Impossible**: Can't restore InformationState from Burr snapshots
4. **Visualization Gaps**: State machine visualization doesn't show dialogue state evolution
5. **Multi-Agent Complexity**: Each agent needs separate engine instance with state management
6. **Testing Difficulty**: Can't easily inject/inspect InformationState through Burr
7. **Unclear Ownership**: Both Burr and Engine "own" different parts of state

## Proposed Architecture

### Burr as Single Source of Truth

All dialogue state moves into Burr State. Engine becomes a stateless transformation library.

```
Burr State (Complete)                Stateless Engine
┌──────────────────────┐            ┌──────────────────┐
│ utterance            │            │ interpret()      │
│ speaker              │            │   (pure function)│
│ information_state ───┼───────────>│   reads: IS      │
│   - private          │            │   returns: moves │
│   - shared (QUD)     │            └──────────────────┘
│   - control          │
│ nlu_context          │            ┌──────────────────┐
│   - entities         │            │ integrate()      │
│   - references       │            │   (pure function)│
│ moves                │───────────>│   reads: IS, move│
│ response_move        │            │   returns: IS'   │
└──────────────────────┘            └──────────────────┘
```

### Key Design Principles

1. **Clarity**: State is explicitly visible in Burr
2. **Simplicity**: No hidden state, no mutable objects
3. **Immutability**: Engine functions return new state, never mutate
4. **Functional**: Engine methods are pure transformations
5. **Complete**: All dialogue state captured in Burr State
6. **Traceable**: Every state change visible in Burr tracking

## Refactoring Plan

### Phase 1: State Extraction

**Goal**: Move InformationState from engine to Burr State

**Changes**:
- `DialogueMoveEngine.__init__()`: Remove `self.state`, accept initial IS as parameter
- `DialogueMoveEngine.process_input()`: Accept IS, return new IS
- Burr actions: Store `information_state` in Burr State
- `initialize` action: Create initial InformationState, write to Burr State

**Before**:
```python
class DialogueMoveEngine:
    def __init__(self, agent_id: str, rules: RuleSet | None = None):
        self.state = InformationState(agent_id=agent_id)

    def interpret(self, utterance: str, speaker: str) -> list[DialogueMove]:
        temp_state = self.state.clone()
        # ... process using self.state
        return moves
```

**After**:
```python
class DialogueMoveEngine:
    def __init__(self, agent_id: str, rules: RuleSet | None = None):
        self.agent_id = agent_id
        self.rules = rules or RuleSet()
        # No self.state!

    def interpret(
        self, utterance: str, speaker: str, state: InformationState
    ) -> list[DialogueMove]:
        temp_state = state.clone()
        # ... process using passed state
        return moves
```

### Phase 2: Stateless Engine Methods

**Goal**: Convert all engine methods to accept and return state

**Methods to Refactor**:
- `interpret(utterance, speaker, state) -> list[DialogueMove]`
- `integrate(move, state) -> InformationState`
- `select_action(state) -> DialogueMove | None`
- `generate(move, state) -> str`
- `process_input(utterance, speaker, state) -> tuple[InformationState, DialogueMove | None]`

**Pattern**:
```python
# OLD: Mutates self.state
def integrate(self, move: DialogueMove) -> InformationState:
    temp_state = self.state.clone()
    new_state = self.rules.apply_rules("integration", temp_state)
    return new_state

# NEW: Pure function
def integrate(self, move: DialogueMove, state: InformationState) -> InformationState:
    temp_state = state.clone()
    temp_state.private.beliefs["_temp_move"] = move
    new_state = self.rules.apply_rules("integration", temp_state)
    # Clean up
    if "_temp_move" in new_state.private.beliefs:
        del new_state.private.beliefs["_temp_move"]
    return new_state
```

### Phase 3: Burr Actions Refactoring

**Goal**: Actions read/write InformationState from Burr State

**Current**:
```python
@action(reads=["utterance", "speaker", "engine"], writes=["moves"])
def interpret(state: State) -> tuple[dict[str, Any], State]:
    engine: DialogueMoveEngine = state["engine"]
    utterance: str = state["utterance"]
    speaker: str = state["speaker"]

    moves = engine.interpret(utterance, speaker)  # Uses engine.state internally!

    return {"moves": moves}, state.update(moves=moves)
```

**Proposed**:
```python
@action(reads=["utterance", "speaker", "information_state", "engine"], writes=["moves"])
def interpret(state: State) -> tuple[dict[str, Any], State]:
    engine: DialogueMoveEngine = state["engine"]
    utterance: str = state["utterance"]
    speaker: str = state["speaker"]
    info_state: InformationState = state["information_state"]

    # Engine is now stateless - pass IS explicitly
    moves = engine.interpret(utterance, speaker, info_state)

    return {"moves": moves}, state.update(moves=moves)
```

**Integration Action**:
```python
@action(
    reads=["moves", "information_state", "engine"],
    writes=["information_state", "integrated"]
)
def integrate(state: State) -> tuple[dict[str, Any], State]:
    moves: list[DialogueMove] = state["moves"]
    info_state: InformationState = state["information_state"]
    engine: DialogueMoveEngine = state["engine"]

    # Apply each move to update state (functional style)
    for move in moves:
        info_state = engine.integrate(move, info_state)

    return (
        {"integrated": True, "move_count": len(moves)},
        state.update(information_state=info_state, integrated=True)
    )
```

### Phase 4: NLU State Integration

**Goal**: Move NLU component state into Burr

**Current NLU State**:
- `EntityTracker`: Maintains entity history across turns
- `ReferenceResolver`: Uses entity tracker
- `HybridFallbackStrategy`: Maintains usage statistics

**Proposed Structure**:
```python
@dataclass
class NLUContext:
    """NLU state tracked across dialogue turns."""
    entities: list[Entity]
    entity_mentions: dict[str, list[str]]
    reference_chains: list[list[str]]
    last_interpretation_tokens: int = 0
    last_interpretation_latency: float = 0.0

# In Burr State:
{
    "information_state": InformationState(...),
    "nlu_context": NLUContext(...),
    "engine": DialogueMoveEngine(...),  # Still stateless
    ...
}
```

### Phase 5: Configuration Simplification

**Goal**: Eliminate fallback complexity, assume resource availability

Per user guidance:
- Remove hybrid fallback strategy
- Assume API keys available
- Use single model (Sonnet 4.5 as default)
- Simplify configuration

**Before**:
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

**After**:
```python
@dataclass
class NLUEngineConfig:
    """Simple NLU configuration.

    Assumes:
    - IBDM_API_KEY is available
    - Claude Sonnet 4.5 for complex tasks
    - Claude Haiku 4.5 for quick classification
    """
    model: ModelType = ModelType.SONNET
    temperature: float = 0.3
    max_tokens: int = 2000
```

## State Schema

### Complete Burr State Schema

```python
{
    # Core dialogue state
    "information_state": InformationState(
        agent_id="system",
        private=PrivateIS(
            plan=[...],
            agenda=[...],
            beliefs={...},
            last_utterance=None
        ),
        shared=SharedIS(
            qud=[...],
            commitments=set(),
            last_moves=[...]
        ),
        control=ControlIS(
            speaker="user",
            next_speaker="system",
            initiative="mixed",
            dialogue_state="active"
        )
    ),

    # NLU context (if using NLU engine)
    "nlu_context": NLUContext(
        entities=[...],
        entity_mentions={...},
        reference_chains=[...],
        last_interpretation_tokens=0,
        last_interpretation_latency=0.0
    ),

    # Stateless engine instance
    "engine": DialogueMoveEngine(agent_id="system", rules=rules),

    # Orchestration state
    "utterance": "What's the weather?",
    "speaker": "user",
    "moves": [DialogueMove(...)],
    "response_move": DialogueMove(...),
    "has_response": True,
    "utterance_text": "The weather is sunny.",
    "integrated": True,

    # Configuration
    "agent_id": "system",
    "rules": RuleSet(...)
}
```

## Benefits of New Architecture

### 1. Complete State Visibility

**Before**: InformationState hidden inside engine
```python
# Can only see surface state
state = app.state
print(state["moves"])  # OK
print(state["???"])  # How to access QUD stack?
```

**After**: All state visible
```python
state = app.state
print(state["information_state"].shared.qud)  # Direct access!
print(state["nlu_context"].entities)  # Transparent
```

### 2. Full Persistence

Burr's persistence now captures complete dialogue state:
- InformationState with QUD stack
- All commitments and beliefs
- Entity tracking history
- Complete state for replay/rollback

### 3. Simplified Testing

```python
# Before: Must construct engine with internal state
engine = DialogueMoveEngine("agent")
engine.state = InformationState(...)  # Fragile

# After: Pure function testing
engine = DialogueMoveEngine("agent")
result = engine.interpret(utterance, speaker, test_state)
assert result == expected_moves
```

### 4. Multi-Agent Support

Each agent's InformationState in Burr:
```python
{
    "agent_1_information_state": InformationState(...),
    "agent_2_information_state": InformationState(...),
    "shared_information_state": InformationState(...),
}
```

### 5. Debugging and Visualization

- Burr UI shows complete state at each step
- Can inspect QUD evolution visually
- Can see commitment accumulation
- Entity tracking visible in timeline

### 6. Rollback and Time Travel

```python
# Save state at turn N
snapshot = app.state

# Process turns N+1, N+2, N+3
...

# Rollback to turn N
app._state = snapshot

# Try different path
...
```

## Migration Strategy

### Backward Compatibility

1. **Dual API Phase**: Support both old and new interfaces
   ```python
   class DialogueMoveEngine:
       def interpret(self, utterance, speaker, state=None):
           if state is None:
               # Legacy: use self.state
               warnings.warn("Pass state explicitly", DeprecationWarning)
               state = self.state
           # New: use passed state
           ...
   ```

2. **Adapter Pattern**: Wrap old engines for compatibility
   ```python
   class StatefulEngineAdapter:
       def __init__(self, engine):
           self.engine = engine

       def process(self, state: State) -> State:
           # Extract IS from Burr state, call old engine, put back
           self.engine.state = state["information_state"]
           self.engine.process_input(...)
           return state.update(information_state=self.engine.state)
   ```

3. **Gradual Migration**: Refactor one component at a time
   - Phase 1: DialogueMoveEngine
   - Phase 2: NLUDialogueEngine
   - Phase 3: Burr actions
   - Phase 4: Test suite
   - Phase 5: Remove deprecated code

### Testing Strategy

1. **Golden Tests**: Capture current behavior, ensure refactor preserves it
2. **Property Tests**: Ensure stateless methods have no side effects
3. **Integration Tests**: Verify complete Burr flows
4. **Snapshot Tests**: Compare state evolution before/after

## Implementation Checklist

- [ ] Create `NLUContext` dataclass for NLU state
- [ ] Refactor `DialogueMoveEngine` to stateless methods
- [ ] Update `interpret()` signature: add `state` parameter
- [ ] Update `integrate()` signature: add `state` parameter, return new state
- [ ] Update `select_action()` signature: add `state` parameter
- [ ] Update `generate()` signature: add `state` parameter
- [ ] Remove `self.state` from `DialogueMoveEngine`
- [ ] Update `initialize` action to create and write InformationState
- [ ] Update `interpret` action to read/write InformationState
- [ ] Update `integrate` action to read/write InformationState
- [ ] Update `select` action to read InformationState
- [ ] Update `generate` action to write InformationState
- [ ] Refactor `NLUDialogueEngine` to use NLUContext in Burr State
- [ ] Remove hybrid fallback strategy code
- [ ] Simplify `NLUEngineConfig`
- [ ] Update all tests to pass state explicitly
- [ ] Update documentation and examples
- [ ] Add state schema validation
- [ ] Update CLAUDE.md with clarity/simplicity principles

## Risks and Mitigations

### Risk: Breaking Changes
**Mitigation**: Dual API phase, comprehensive tests, gradual migration

### Risk: Performance Overhead
**Mitigation**: State cloning is already used; immutability enables optimizations

### Risk: Burr State Size
**Mitigation**: InformationState is already serializable; no size increase

### Risk: Learning Curve
**Mitigation**: Clear documentation, examples, migration guide

## Success Criteria

1. ✓ All dialogue state in Burr State
2. ✓ Engine methods are pure functions
3. ✓ No hidden state in engine objects
4. ✓ Full state persistence and visualization
5. ✓ All tests passing
6. ✓ Documentation updated
7. ✓ Simplified configuration (no fallbacks)
8. ✓ Code clarity improved per CLAUDE.md

## References

- [Burr Documentation](https://burr.dagworks.io/)
- IBDM Phase 2: Burr Integration (ibdm-zfl)
- Larsson (2002): Issue-Based Dialogue Management
- Current implementation: `src/ibdm/burr_integration/`
- Current engines: `src/ibdm/engine/`

## Appendix: Code Examples

### Example: Complete State Access

```python
from ibdm.burr_integration import create_dialogue_application

# Create application
app = create_dialogue_application(agent_id="system", rules=rules)

# Initialize
app.step()  # initialize action

# Process utterance
state = app.state.update(utterance="What's the weather?", speaker="user")
app._state = state

# Step through control loop
for _ in range(4):
    action, result, state = app.step()

    # Access complete state at any point
    info_state = state["information_state"]
    print(f"QUD stack: {info_state.shared.qud}")
    print(f"Commitments: {info_state.shared.commitments}")
    print(f"Next speaker: {info_state.control.next_speaker}")

    if "nlu_context" in state:
        nlu = state["nlu_context"]
        print(f"Entities: {nlu.entities}")

# Save complete state for later
snapshot = app.state

# Replay from snapshot
app._state = snapshot
```

### Example: Pure Engine Testing

```python
from ibdm.core import InformationState, DialogueMove
from ibdm.engine import DialogueMoveEngine

def test_interpret_pure():
    """Test that interpret is a pure function."""
    engine = DialogueMoveEngine("agent", rules)
    state = InformationState(agent_id="agent")

    # Call interpret twice with same inputs
    moves1 = engine.interpret("Hello", "user", state)
    moves2 = engine.interpret("Hello", "user", state)

    # Results should be identical
    assert moves1 == moves2

    # State should be unchanged
    assert state.shared.qud == []
    assert state.private.agenda == []

def test_integrate_pure():
    """Test that integrate returns new state without mutation."""
    engine = DialogueMoveEngine("agent", rules)
    state = InformationState(agent_id="agent")
    move = DialogueMove(move_type="ask", content="Hello?", speaker="user")

    # Integrate should return new state
    new_state = engine.integrate(move, state)

    # Original state should be unchanged
    assert state is not new_state
    assert len(state.shared.qud) == 0
    assert len(new_state.shared.qud) >= 0  # May have changed
```

---

**Next Steps**: Create beads tasks for implementation, review with team, begin Phase 1.
