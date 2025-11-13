# Domain Semantic Layer: Recommendation

**Date**: 2025-11-13
**Based on**: py-trindikit analysis
**Decision**: Add lightweight domain model (no grammar)

---

## Executive Summary

After comprehensive analysis of py-trindikit (Larsson's reference implementation), recommendation is:

**✅ Add Domain Model Layer**
- Explicit predicate and sort definitions
- Type validation for answers
- Domain-independent rule methods
- Plan management abstraction

**❌ Don't Add Grammar**
- LLM-based NLU is superior for our use case
- Grammar adds overhead without benefit
- Accept emergent (not compositional) semantics

---

## What py-trindikit Showed Us

### They Have (That We're Missing)

1. **Domain Model Class**
   ```python
   class Domain:
       predicates0: list[str]           # 0-arity predicates
       predicates1: dict[str, str]      # 1-arity: name → sort
       sorts: dict[str, list[str]]      # sort → [individuals]
       
       def relevant(prop, question) → bool
       def resolves(prop, question) → bool
       def get_plan(task) → Plan
       def consultDB(question, context) → Prop
   ```

2. **Semantic Type System**
   - Pred0, Pred1 (predicates)
   - Ind (individuals)
   - Prop (propositions)
   - WhQ, YNQ, AltQ (questions)
   - Type checking with _typecheck()

3. **Domain-Independent Rules**
   ```python
   @update_rule
   def integrate_answer(IS, DOMAIN):
       # Uses DOMAIN.resolves() - works for any domain!
       if DOMAIN.resolves(answer, question):
           IS.shared.com.add(answer)
           IS.shared.qud.pop()
   ```

### Key Insight

**Domain abstraction enables reusable rules**. Same rule code works for:
- Travel booking
- NDA drafting
- Contract generation
- Any other domain

---

## Recommended Architecture

### Lightweight Domain Model (No Grammar)

```python
# src/ibdm/core/domain.py

@dataclass
class PredicateSpec:
    """Domain predicate specification."""
    name: str
    arity: int
    arg_types: list[str]
    description: str = ""

class DomainModel:
    """Domain model for task-oriented dialogue.
    
    Provides predicate definitions, type constraints, and
    semantic operations WITHOUT requiring grammar-based parsing.
    """
    
    def __init__(self, name: str):
        self.name = name
        self.predicates: dict[str, PredicateSpec] = {}
        self.sorts: dict[str, list[str]] = {}
        self._plan_builders: dict[str, Callable] = {}
    
    def add_predicate(self, name: str, arity: int, 
                      arg_types: list[str] = None):
        """Register predicate with type signature."""
        self.predicates[name] = PredicateSpec(
            name=name,
            arity=arity,
            arg_types=arg_types or []
        )
    
    def add_sort(self, name: str, individuals: list[str]):
        """Register semantic sort."""
        self.sorts[name] = individuals
    
    def resolves(self, answer: Answer, question: Question) -> bool:
        """Check if answer resolves question (with type validation)."""
        # Use existing Question.resolves_with() + type checking
        if not question.resolves_with(answer):
            return False
        
        # Additional type validation
        return self._check_types(answer, question)
    
    def relevant(self, prop: Any, question: Question) -> bool:
        """Check semantic relevance."""
        if hasattr(prop, "predicate") and hasattr(question, "predicate"):
            return prop.predicate == question.predicate
        return False
    
    def get_plan(self, task: str, context: dict = None) -> Plan:
        """Get dialogue plan for task."""
        builder = self._plan_builders.get(task)
        if not builder:
            raise ValueError(f"No plan builder for task: {task}")
        return builder(context or {})
    
    def register_plan_builder(self, task: str, 
                              builder: Callable[[dict], Plan]):
        """Register plan builder function."""
        self._plan_builders[task] = builder
    
    def _check_types(self, answer: Answer, question: Question) -> bool:
        """Validate answer value against predicate types."""
        pred_spec = self.predicates.get(question.predicate)
        if not pred_spec or not pred_spec.arg_types:
            return True  # No type spec, accept
        
        expected_type = pred_spec.arg_types[0]
        if expected_type in self.sorts:
            # Check if value in allowed individuals
            return answer.value in self.sorts[expected_type]
        
        return True  # Unknown type, accept
```

---

## Example: NDA Domain

```python
# src/ibdm/domains/nda_domain.py

def create_nda_domain() -> DomainModel:
    """Create NDA drafting domain model."""
    domain = DomainModel(name="nda_drafting")
    
    # Predicates (what we ask about)
    domain.add_predicate(
        "parties",
        arity=1,
        arg_types=["legal_entities"],
        description="Parties entering into NDA"
    )
    domain.add_predicate(
        "nda_type",
        arity=1,
        arg_types=["nda_kind"],
        description="Type of NDA (mutual/one-way)"
    )
    domain.add_predicate(
        "effective_date",
        arity=1,
        arg_types=["date"],
        description="When NDA becomes effective"
    )
    domain.add_predicate(
        "duration",
        arity=1,
        arg_types=["time_period"],
        description="How long confidentiality lasts"
    )
    domain.add_predicate(
        "governing_law",
        arity=1,
        arg_types=["jurisdiction"],
        description="Which jurisdiction's laws apply"
    )
    
    # Sorts (constrained value types)
    domain.add_sort("nda_kind", ["mutual", "one-way"])
    domain.add_sort("jurisdiction", [
        "California",
        "Delaware",
        "New York",
        "Texas",
        "other"
    ])
    
    # Plan builder
    def build_nda_plan(context: dict) -> Plan:
        return Plan(
            plan_type="nda_drafting",
            description="Complete NDA drafting workflow",
            subplans=[
                Findout(WhQuestion(
                    variable="parties",
                    predicate="legal_entities"
                )),
                Findout(AltQuestion(
                    alternatives=["mutual", "one-way"],
                    predicate="nda_type"
                )),
                Findout(WhQuestion(
                    variable="date",
                    predicate="effective_date"
                )),
                Findout(WhQuestion(
                    variable="duration",
                    predicate="time_period"
                )),
                Findout(AltQuestion(
                    alternatives=["California", "Delaware", "New York"],
                    predicate="governing_law"
                ))
            ]
        )
    
    domain.register_plan_builder("nda_drafting", build_nda_plan)
    
    return domain
```

---

## Integration with Rules

### Before (Without Domain)

```python
# integration_rules.py
def _accommodate_task(state):
    """Create plan for task (ad-hoc)."""
    move = state.private.beliefs.get("_temp_move")
    
    # Ad-hoc plan creation
    if "NDA" in move.content:
        plan = Plan(
            plan_type="nda_drafting",
            subplans=[
                # Hardcoded here...
            ]
        )
    
    new_state = state.clone()
    new_state.private.plan.append(plan)
    return new_state

def _check_answer_resolves(state):
    """Check if answer resolves question (built into Question)."""
    answer = state.private.beliefs.get("_temp_answer")
    question = state.shared.qud.top()
    
    # Built into Question class, no type validation
    return question.resolves_with(answer)
```

### After (With Domain)

```python
# integration_rules.py
def _accommodate_task(state):
    """Create plan for task (using domain)."""
    move = state.private.beliefs.get("_temp_move")
    task_type = move.metadata.get("task_type")
    
    # Get domain for task
    domain = get_domain_for_task(task_type)
    
    # Get plan from domain (abstracted)
    plan = domain.get_plan(task_type, context={})
    
    new_state = state.clone()
    new_state.private.plan.append(plan)
    return new_state

def _check_answer_resolves(state):
    """Check if answer resolves question (with type validation)."""
    answer = state.private.beliefs.get("_temp_answer")
    question = state.shared.qud.top()
    
    # Get active domain
    domain = _get_active_domain(state)
    
    # Domain handles type checking
    return domain.resolves(answer, question)
```

**Benefits**:
1. ✅ Explicit predicate definitions
2. ✅ Type validation (catches "42" for "California")
3. ✅ Centralized plan management
4. ✅ Domain-independent rule code
5. ✅ Easy to add new domains

---

## Implementation Plan

### Phase 1: Foundation (2 days)

**Task**: Implement DomainModel class

- [ ] Create `src/ibdm/core/domain.py`
- [ ] Implement `DomainModel` class
- [ ] Implement `PredicateSpec` dataclass
- [ ] Implement `resolves()`, `relevant()`, `get_plan()` methods
- [ ] Unit tests for DomainModel
- [ ] Documentation

**Files**:
- `src/ibdm/core/domain.py` (new)
- `tests/unit/test_domain.py` (new)

### Phase 2: NDA Domain (1 day)

**Task**: Define NDA domain model

- [ ] Create `src/ibdm/domains/__init__.py`
- [ ] Create `src/ibdm/domains/nda_domain.py`
- [ ] Define NDA predicates
- [ ] Define NDA sorts
- [ ] Implement NDA plan builder
- [ ] Unit tests
- [ ] Documentation

**Files**:
- `src/ibdm/domains/nda_domain.py` (new)
- `tests/unit/domains/test_nda_domain.py` (new)

### Phase 3: Integration (2-3 days)

**Task**: Integrate domain with rules

- [ ] Update `integration_rules.py` to use domain
- [ ] Update `_accommodate_task()` to get plan from domain
- [ ] Update question resolution to use `domain.resolves()`
- [ ] Add domain registry (map task → domain)
- [ ] Update tests
- [ ] Integration tests

**Files**:
- `src/ibdm/rules/integration_rules.py` (update)
- `src/ibdm/core/domain_registry.py` (new)
- `tests/integration/test_domain_integration.py` (new)

### Phase 4: Validation (1-2 days)

**Task**: Test and document

- [ ] Full NDA workflow test with domain
- [ ] Type validation tests
- [ ] Error handling tests
- [ ] Update architecture docs
- [ ] Update CLAUDE.md with domain principles
- [ ] Demo with domain model

**Files**:
- `docs/DOMAIN_MODEL_GUIDE.md` (new)
- `CLAUDE.md` (update)
- `tests/integration/test_nda_workflow_with_domain.py` (new)

**Total Estimate**: 6-8 days

---

## Benefits

### Immediate Benefits

1. **Type Safety**: Catch invalid answers early
   ```python
   # Before: "42" accepted for jurisdiction
   # After: Type error, request clarification
   ```

2. **Clarity**: Explicit predicate definitions
   ```python
   # Before: Implicit in code
   # After: domain.add_predicate("parties", ...)
   ```

3. **Reusability**: Domain-independent rules
   ```python
   # Same rule works for NDA, contracts, etc.
   if domain.resolves(answer, question):
       qud.pop()
   ```

4. **Extensibility**: Easy to add domains
   ```python
   # Just define new domain
   contract_domain = create_contract_domain()
   ```

### Long-Term Benefits

1. **Maintainability**: Changes isolated to domain definitions
2. **Testability**: Domain logic separately testable
3. **Documentation**: Self-documenting predicate specs
4. **Scalability**: Support multiple task types easily
5. **Evolution**: Can add more domain features later

---

## What We're NOT Doing

1. ❌ **Grammar-based parsing**: Keeping LLM-based NLU
2. ❌ **Compositional semantics**: Not needed for our use case
3. ❌ **NLTK integration**: No .fcfg grammar files
4. ❌ **Full py-trindikit port**: Cherry-picking domain model only
5. ❌ **Formal verification**: Beyond scope

---

## Success Criteria

After implementation:

- ✅ Domain model exists with predicate/sort definitions
- ✅ NDA domain defined with all predicates
- ✅ Type validation works (rejects invalid answers)
- ✅ Plan retrieval uses domain.get_plan()
- ✅ Rules use domain.resolves() for validation
- ✅ Tests pass with domain integration
- ✅ Full NDA workflow works with domain
- ✅ Documentation updated
- ✅ Easy to add new domains (contracts, emails, etc.)

---

## Decision

**APPROVED**: Add lightweight domain model layer

**Rationale**:
1. py-trindikit demonstrates domain abstraction is core to IBDM
2. Benefits (structure, type safety, reusability) outweigh cost
3. Can add without changing LLM-based NLU (best of both worlds)
4. 6-8 days is reasonable investment
5. Sets foundation for future domains

**Next Steps**:
1. Review this recommendation with team
2. Create beads tasks for Phase 1-4
3. Start with Phase 1: DomainModel foundation
4. Iterate through phases

---

## References

- **Analysis**: docs/PY_TRINDIKIT_ANALYSIS.md (comprehensive)
- **py-trindikit**: https://github.com/heatherleaf/py-trindikit
- **Larsson (2002)**: Issue-Based Dialogue Management
- **Our critique**: docs/LARSSON_FRAMEWORK_CRITIQUE.md
- **Formal semantics**: docs/FORMAL_SEMANTICS_VS_LLM_NLU.md
