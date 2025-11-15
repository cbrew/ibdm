# Plan Evaluation: Does Our Refactoring Plan Still Make Sense?

**Date**: 2025-11-13
**Context**: After deep analysis of py-trindikit (Larsson's reference implementation)
**Question**: Does REVISED_REFACTORING_TASKS.md need changes based on py-trindikit findings?

---

## Executive Summary

**TL;DR**: Our plan is **80% correct but incomplete**. We need to add a **Domain Semantic Layer** to achieve proper Larsson fidelity.

### Key Findings

1. ✅ **Keep**: LLM-based NLU (better than grammar for our use case)
2. ✅ **Keep**: Move task plan formation to integration phase
3. ✅ **Keep**: Plan-aware NLG generation
4. ➕ **ADD**: Lightweight domain model layer (predicates, sorts, semantic operations)
5. 🔧 **FIX**: Terminology - "accommodation" → "task plan formation"

### Impact

- **Current plan duration**: 9 hours (5 phases)
- **With domain layer**: 14-17 hours (7 phases)
- **Additional work**: 5-8 hours for domain model implementation

---

## What py-trindikit Teaches Us

### 1. Domain Model is Integral, Not Optional

**py-trindikit has an explicit Domain class**:

```python
class Domain:
    """Domain model with predicates, sorts, and individuals."""

    def __init__(self,
                 predicates0: list[str],      # 0-arity predicates
                 predicates1: dict[str, str], # 1-arity predicates with types
                 sorts: dict[str, list[str]]) # Sorts with individuals

    def relevant(self, prop: Prop, question: Question) -> bool:
        """Check if proposition is relevant to question."""
        return prop.predicate == question.predicate

    def resolves(self, prop: Prop, question: Question) -> bool:
        """Check if proposition resolves question."""
        if isinstance(question, WhQ):
            return (prop.predicate == question.predicate and
                    prop.individual is not None)
        return False

    def get_plan(self, task: str) -> Plan:
        """Return dialogue plan for task."""
        # Returns plan based on task type

    def consultDB(self, question: Question, context: dict) -> Prop:
        """Query database using question and context."""
        # Database lookup
```

**Travel domain example**:

```python
# Define predicates with types
predicates1 = {
    "price": "int",
    "how": "means",           # how(x) where x ∈ {plane, train}
    "dest_city": "city",      # dest_city(x) where x ∈ {paris, london, berlin}
    "depart_city": "city",
    "depart_day": "day",
}

# Define sorts (semantic types)
sorts = {
    "means": ["plane", "train"],
    "city": ["paris", "london", "berlin"],
    "day": ["today", "tomorrow"],
}

domain = Domain(predicates0=[], predicates1=predicates1, sorts=sorts)
```

### 2. Domain Methods Enable Domain-Independent Rules

**Key insight**: Update rules call domain methods, not hardcoded logic!

```python
# py-trindikit update rule (domain-independent!)
@update_rule
def integrate_answer(IS, DOMAIN):
    """Integrate answer and resolve QUD."""

    @precondition
    def V():
        for move in IS.LATEST_MOVES:
            if isinstance(move, Answer):
                answer = move.content

                if not IS.shared.qud.is_empty():
                    question = IS.shared.qud.top()

                    # Uses domain method!
                    if DOMAIN.resolves(answer, question):
                        yield R(answer=answer, question=question)

    IS.shared.com.add(V.answer)
    IS.shared.qud.pop()
```

**This works for ANY domain** (travel, NDA, contracts) because `DOMAIN.resolves()` encapsulates domain-specific logic!

### 3. What We're Missing

**Our current implementation**:

```python
# src/ibdm/rules/interpretation_rules.py (lines 434-505)
def _create_nda_plan():
    """Create NDA drafting plan."""
    subplans = [
        Plan(
            plan_type="findout",
            content=WhQuestion(variable="parties", predicate="legal_entities"),  # HARDCODED!
            status="active",
        ),
        Plan(
            plan_type="findout",
            content=WhQuestion(variable="duration", predicate="time_period"),  # HARDCODED!
            status="active",
        ),
    ]
    return Plan(plan_type="nda_drafting", content="nda_requirements", subplans=subplans)
```

**Problems**:
1. ❌ Predicates are magic strings ("legal_entities", "time_period")
2. ❌ No semantic grounding - what does "legal_entities" mean?
3. ❌ No type checking - is "42" a valid legal_entity?
4. ❌ No connection to NLU's extracted entities (ORGANIZATION vs legal_entities?)
5. ❌ Cannot reuse rules across domains

---

## Gap Analysis: Our Plan vs py-trindikit

### What Our Current Plan Gets Right ✅

| Aspect | Our Plan | py-trindikit | Status |
|--------|----------|--------------|--------|
| LLM-based NLU | ✅ Use existing NLU | ❌ Grammar-based | ✅ Better approach |
| Task plan formation in integration | ✅ Phase 1 | ✅ Same | ✅ Correct |
| Plan-aware NLG | ✅ Phase 3 | ✅ Same | ✅ Correct |
| QUD management | ✅ Existing | ✅ Same | ✅ Correct |
| Update rules | ✅ Existing | ✅ Same | ✅ Correct |

### What Our Current Plan is Missing ⚠️

| Aspect | Our Plan | py-trindikit | Gap |
|--------|----------|--------------|-----|
| Domain model | ❌ None | ✅ Explicit Domain class | **MISSING** |
| Predicate definitions | ❌ Magic strings | ✅ predicates1 dict | **MISSING** |
| Sort/type system | ❌ None | ✅ sorts dict | **MISSING** |
| Domain.resolves() | ❌ Built into Question | ✅ Domain method | **MISSING** |
| Domain.relevant() | ❌ None | ✅ Domain method | **MISSING** |
| Domain.get_plan() | ❌ Hardcoded | ✅ Domain method | **MISSING** |
| Type checking | ❌ None | ✅ _typecheck() | **MISSING** |

### Critical Finding

**py-trindikit shows that domain abstraction is INTEGRAL to Larsson's IBDM**, not optional!

The domain layer provides:
1. **Semantic grounding** - predicates have meaning, not just strings
2. **Type safety** - values must match sorts
3. **Domain-independent rules** - same rules work across domains
4. **Extensibility** - add new domains without changing core rules

---

## Does Our Plan Still Make Sense?

### Short Answer: YES, but incomplete

Our plan addresses:
- ✅ Moving task plan formation to integration (correct per Larsson)
- ✅ Using LLM-based NLU (better than grammar)
- ✅ Plan-aware NLG (natural conversations)

Our plan misses:
- ❌ Domain semantic layer (integral to Larsson)
- ❌ Predicate definitions (semantic grounding)
- ❌ Type system (validation)
- ❌ Domain-independent rule methods

### What Needs to Change

**Add new phase** to our plan:
- **Phase 0**: Create domain semantic layer (BEFORE moving accommodation)

**Why Phase 0?**
- Domain model needed for proper task plan formation
- Integration rules should use `domain.get_plan(task_type)` not hardcoded plans
- Question resolution should use `domain.resolves(answer, question)` for type checking

---

## Recommended Changes to Our Plan

### Option 1: Minimal Domain Layer (Recommended)

**Add lightweight domain model without full grammar/compositional semantics**

#### New Phase 0: Domain Model Foundation (5-8 hours)

**Objective**: Add domain abstraction layer that py-trindikit has, without grammar

**Tasks**:

1. **Create domain model core** (2 hours)
   ```python
   # src/ibdm/core/domain.py

   @dataclass
   class PredicateSpec:
       """Specification for a domain predicate."""
       name: str
       arity: int
       arg_types: list[str] = field(default_factory=list)
       description: str = ""

   class DomainModel:
       """Lightweight domain model for IBDM.

       Provides predicate definitions and semantic operations
       without requiring grammar-based parsing.
       """

       def __init__(self, name: str):
           self.name = name
           self.predicates: dict[str, PredicateSpec] = {}
           self.sorts: dict[str, list[str]] = {}

       def add_predicate(self, name: str, arity: int,
                         arg_types: list[str] = None,
                         description: str = ""):
           """Register predicate with type signature."""
           self.predicates[name] = PredicateSpec(
               name=name, arity=arity,
               arg_types=arg_types or [],
               description=description
           )

       def add_sort(self, name: str, individuals: list[str]):
           """Register semantic sort with values."""
           self.sorts[name] = individuals

       def resolves(self, answer: Answer, question: Question) -> bool:
           """Check if answer resolves question (with type checking)."""
           # Delegate to Question but add type validation
           if question.resolves_with(answer):
               return self._check_types(answer, question)
           return False

       def relevant(self, prop: Any, question: Question) -> bool:
           """Check semantic relevance."""
           if hasattr(prop, "predicate") and hasattr(question, "predicate"):
               return prop.predicate == question.predicate
           return False

       def get_plan(self, task: str, context: dict = None) -> Plan:
           """Get dialogue plan for task."""
           # Dispatch to registered plan builder
           return self._plan_builders[task](context or {})
   ```

2. **Define NDA domain** (1.5 hours)
   ```python
   # src/ibdm/domains/nda_domain.py

   def create_nda_domain() -> DomainModel:
       """Create NDA drafting domain model."""
       domain = DomainModel(name="nda_drafting")

       # Add predicates
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
           description="When NDA takes effect"
       )
       domain.add_predicate(
           "duration",
           arity=1,
           arg_types=["time_period"],
           description="How long confidentiality obligations last"
       )
       domain.add_predicate(
           "governing_law",
           arity=1,
           arg_types=["jurisdiction"],
           description="Jurisdiction for legal disputes"
       )

       # Add sorts
       domain.add_sort("nda_kind", ["mutual", "one-way"])
       domain.add_sort("jurisdiction", ["California", "Delaware", "New York"])

       # Register plan builder
       domain.register_plan_builder("nda_drafting", _build_nda_plan)

       return domain

   def _build_nda_plan(context: dict) -> Plan:
       """Build NDA drafting plan."""
       return Plan(
           plan_type="nda_drafting",
           content="nda_requirements",
           status="active",
           subplans=[
               Plan(
                   plan_type="findout",
                   content=WhQuestion(variable="parties", predicate="legal_entities"),
                   status="active"
               ),
               Plan(
                   plan_type="findout",
                   content=AltQuestion(alternatives=["mutual", "one-way"]),
                   status="active"
               ),
               Plan(
                   plan_type="findout",
                   content=WhQuestion(variable="effective_date", predicate="date"),
                   status="active"
               ),
               Plan(
                   plan_type="findout",
                   content=WhQuestion(variable="duration", predicate="time_period"),
                   status="active"
               ),
               Plan(
                   plan_type="findout",
                   content=AltQuestion(alternatives=["California", "Delaware", "New York"]),
                   status="active"
               ),
           ]
       )
   ```

3. **Map NLU entities to domain predicates** (1.5 hours)
   ```python
   # src/ibdm/nlu/domain_mapper.py

   class NLUDomainMapper:
       """Maps NLU entities to domain predicates."""

       def __init__(self, domain: DomainModel):
           self.domain = domain
           # Define mapping rules
           self.entity_to_predicate = {
               EntityType.ORGANIZATION: "legal_entities",
               EntityType.TEMPORAL: "effective_date",
               EntityType.DURATION: "time_period",
               EntityType.LOCATION: "jurisdiction",
           }

       def map_entities(self, entities: list[Entity], question: Question) -> Answer:
           """Map extracted entities to domain answer."""
           # Use domain knowledge to validate and structure
           predicate = question.predicate
           pred_spec = self.domain.predicates.get(predicate)

           if pred_spec:
               # Filter entities by expected type
               expected_type = pred_spec.arg_types[0]
               valid_entities = self._filter_by_sort(entities, expected_type)

               # Create answer
               return Answer(
                   content=self._format_entities(valid_entities),
                   question_ref=question
               )
   ```

4. **Update integration rules to use domain** (1 hour)
   ```python
   # src/ibdm/rules/integration_rules.py (updated)

   def _form_task_plan(state):  # Renamed from _accommodate_task
       """Form execution plan for user's task.

       Uses domain model to get appropriate plan.
       """
       move = state.private.beliefs.get("_temp_move")
       task_type = move.metadata.get("task_type")

       # Get domain for task
       domain = _get_domain_for_task(task_type)

       # Get plan from domain (not hardcoded!)
       context = _extract_context(move, state)
       plan = domain.get_plan(task_type, context)

       # Add to state
       new_state = state.clone()
       new_state.private.plan.append(plan)

       # Push first question to QUD
       if plan.subplans:
           first_question = plan.subplans[0].content
           new_state.shared.push_qud(first_question)

       new_state.control.next_speaker = new_state.agent_id
       return new_state
   ```

5. **Unit tests for domain model** (1 hour)
   ```python
   # tests/unit/test_domain_model.py

   def test_nda_domain_creation():
       domain = create_nda_domain()
       assert "parties" in domain.predicates
       assert "legal_entities" in domain.predicates["parties"].arg_types

   def test_domain_resolves_with_type_checking():
       domain = create_nda_domain()
       question = WhQuestion(variable="x", predicate="nda_type")
       answer_valid = Answer(content="mutual")
       answer_invalid = Answer(content="three-way")  # Not in sorts

       assert domain.resolves(answer_valid, question) == True
       assert domain.resolves(answer_invalid, question) == False

   def test_domain_get_plan():
       domain = create_nda_domain()
       plan = domain.get_plan("nda_drafting", {})
       assert plan.plan_type == "nda_drafting"
       assert len(plan.subplans) == 5
   ```

6. **Integration tests with domain** (1 hour)
   ```python
   # tests/integration/test_nda_with_domain.py

   def test_nda_workflow_uses_domain():
       """Test complete NDA workflow using domain model."""
       domain = create_nda_domain()
       engine = NLUDialogueEngine(agent_id="system", domain=domain)
       state = InformationState(agent_id="system")

       # User: "I need to draft an NDA"
       moves = engine.interpret("I need to draft an NDA", "user", state)

       for move in moves:
           state = engine.integrate(move, state)

       # Verify domain.get_plan() was called
       assert len(state.private.plan) == 1
       assert state.private.plan[0].plan_type == "nda_drafting"

       # Verify type checking works
       question = state.shared.qud.top()
       answer = Answer(content="Acme Corp and Beta Industries")

       # Domain validates answer
       assert domain.resolves(answer, question) == True
   ```

**Total Phase 0**: 8 hours

### Updated Plan Timeline

| Phase | Tasks | Original Time | With Domain | Priority |
|-------|-------|--------------|-------------|----------|
| **0. Domain Model** | 6 | - | **8 hours** | **P0** |
| 1. Move Task Plan Formation | 3 | 3 hours | 3 hours | P0 |
| 2. Clean Up | 3 | 1 hour | 1 hour | P1 |
| 3. Enhance NLG | 4 | 2 hours | 2 hours | P1 |
| 4. Integration Testing | 3 | 2 hours | 2 hours | P1 |
| 5. Documentation | 4 | 1 hour | 1 hour | P2 |
| **TOTAL** | **23** | **9 hours** | **17 hours** | |

### Changes to Existing Phases

**Phase 1: Move Task Plan Formation** - Update to use domain:

```python
# Before (hardcoded)
if task_type == "DRAFT_DOCUMENT" or "draft" in intent.lower():
    if "NDA" in intent.upper():
        plan = _create_nda_plan()  # Hardcoded function
        new_state.private.plan.append(plan)

# After (domain-driven)
domain = _get_domain_for_task(task_type)
plan = domain.get_plan(task_type, context)  # Domain method
new_state.private.plan.append(plan)
```

**Phase 2: Clean Up** - Also remove hardcoded `_create_nda_plan()`:
- Move to `nda_domain.py` as `_build_nda_plan()`
- No longer in `interpretation_rules.py` or `integration_rules.py`

**Phase 3: Enhance NLG** - Use domain for question generation:

```python
# Can look up predicate descriptions
def _generate_nda_question(question, plan, state):
    domain = get_active_domain(state)
    pred_spec = domain.predicates.get(question.predicate)

    if pred_spec:
        # Use domain description
        return f"{pred_spec.description}? (Step {completed+1} of {total})"
```

---

## Option 2: Full py-trindikit Style (NOT Recommended)

**What it would include**:
- Grammar-based parsing (NLTK FeatureParser)
- Compositional semantics
- Full type system with _typecheck()
- Database integration (consultDB)

**Why NOT recommended**:
1. ❌ Grammar maintenance overhead
2. ❌ Limited linguistic coverage
3. ❌ LLM-based NLU is better for our use case
4. ❌ Over-engineering for business dialogue

**When it WOULD make sense**:
- Safety-critical domains (medical, aviation)
- Legally-binding interactions
- Need formal guarantees about semantic correctness

---

## Terminology Fixes (Based on Larsson Critique)

### Issue: "Accommodation" is Misleading

**Larsson's "accommodation"**: Presupposition accommodation
```
User: "The king of France is bald"
→ Presupposition: France has a king
→ Accommodate: Add "exists(king(france))" to IS
```

**Our "accommodation"**: Task plan formation
```
User: "I need to draft an NDA"
→ "Accommodate": Infer task=NDA_DRAFTING, create plan
→ Better name: Form Task Plan
```

### Recommended Renaming

| Current Name | Better Name | Rationale |
|--------------|-------------|-----------|
| `accommodate_command` | `form_task_plan` | Clearer, accurate |
| `_accommodate_task()` | `_form_task_plan()` | Not Larsson's accommodation |
| "Accommodation phase" | "Task plan formation" | Avoids confusion |

**Update in documentation**:
```markdown
## Task Plan Formation (Not Accommodation!)

Our system performs **task plan formation** when users request tasks.
This is distinct from Larsson's **presupposition accommodation**.

- **Task Plan Formation** (ours): User says "draft NDA" → create NDA plan
- **Presupposition Accommodation** (Larsson): User says "the CEO" → accommodate: CEO exists
```

---

## Final Recommendations

### What to Do

1. **Add Phase 0: Domain Model** (8 hours, P0)
   - Create `src/ibdm/core/domain.py`
   - Define NDA domain in `src/ibdm/domains/nda_domain.py`
   - Add NLU→domain mapping
   - Unit and integration tests

2. **Update Phase 1: Use Domain Model** (add 30 min)
   - Change `_accommodate_task` → `_form_task_plan`
   - Use `domain.get_plan(task_type)` instead of hardcoded plans
   - Update tests

3. **Update Phase 2: Move Plan Builder** (same time)
   - Move `_create_nda_plan` → `nda_domain._build_nda_plan`
   - Remove from interpretation and integration rules

4. **Update Documentation: Terminology** (add 20 min)
   - Clarify "task plan formation" vs "accommodation"
   - Document domain model design
   - Explain py-trindikit influence

### What NOT to Do

1. ❌ **Don't add grammar-based parsing** - LLM is better
2. ❌ **Don't add full compositional semantics** - Not needed
3. ❌ **Don't add database integration yet** - Can add later if needed
4. ❌ **Don't add formal verification** - Out of scope

### Success Criteria (Updated)

After implementing the updated plan, we should have:

1. ✅ **Domain Model**: Explicit predicates, sorts, and semantic operations
2. ✅ **Type Safety**: Answer validation using domain sorts
3. ✅ **Domain-Independent Rules**: Same rules work across tasks
4. ✅ **Clear Terminology**: "Task plan formation" not "accommodation"
5. ✅ **NLU Integration**: Domain bridges NLU entities to IBDM predicates
6. ✅ **Larsson Fidelity**: ~95% (up from ~85%)
7. ✅ **Extensibility**: Easy to add new domains (contracts, emails, etc.)

---

## Conclusion

### Does Our Plan Still Make Sense?

**YES**, but it needs **one critical addition**: the domain semantic layer.

### Why Domain Layer Matters

py-trindikit shows that Larsson's IBDM framework includes domain abstraction as a core component. Without it:

1. ❌ Predicates are magic strings (no semantic grounding)
2. ❌ No type checking (accept invalid answers)
3. ❌ Rules are domain-specific (can't reuse)
4. ❌ NLU and IBDM layers are disconnected

With domain layer:

1. ✅ Predicates have definitions (semantic grounding)
2. ✅ Type checking validates answers (reject "42" for legal_entities)
3. ✅ Rules are domain-independent (reusable)
4. ✅ Domain bridges NLU entities to IBDM predicates

### Recommended Path Forward

1. **Accept**: Current plan is good foundation
2. **Add**: Phase 0 - Domain Model (8 hours)
3. **Update**: Phases 1-2 to use domain (add 30 min)
4. **Fix**: Terminology in documentation (add 20 min)
5. **Total**: 17 hours (up from 9)

### Long-Term Benefits

The domain layer investment pays off:

- **Extensibility**: Add contracts domain in 2 hours (reuse everything else)
- **Validation**: Catch errors early via type checking
- **Clarity**: Explicit predicate definitions make system understandable
- **Testing**: Can unit test domain logic separately
- **Documentation**: Domain model IS the specification

**ROI**: 8 hours upfront → saves weeks of debugging and refactoring later

---

## Appendix: Comparison Table

| Aspect | Current Plan | py-trindikit | Recommended |
|--------|-------------|--------------|-------------|
| **Interpretation** |
| Method | LLM-based NLU | Grammar (FCFG) | ✅ Keep LLM |
| Output | DialogueMoves | DialogueMoves | ✅ Same |
| **Domain Model** |
| Predicates | ❌ Magic strings | ✅ Explicit defs | ➕ **Add explicit** |
| Sorts/Types | ❌ None | ✅ sorts dict | ➕ **Add sorts** |
| Domain class | ❌ None | ✅ Domain | ➕ **Add DomainModel** |
| Type checking | ❌ None | ✅ _typecheck() | ➕ **Add validation** |
| **Semantic Operations** |
| resolves() | ⚠️ In Question | ✅ Domain method | 🔧 **Add domain.resolves()** |
| relevant() | ❌ None | ✅ Domain method | ➕ **Add domain.relevant()** |
| get_plan() | ⚠️ Hardcoded | ✅ Domain method | 🔧 **Add domain.get_plan()** |
| consultDB() | ❌ None | ✅ Domain method | ⏸️ **Later (not urgent)** |
| **Integration** |
| Phase | ✅ Correct | ✅ Same | ✅ Keep |
| Plan formation | ✅ Integration | ✅ Same | ✅ Keep |
| Terminology | ⚠️ "accommodation" | N/A | 🔧 **Fix to "task plan formation"** |
| **Generation** |
| Method | ✅ Plan-aware NLG | ✅ Templates | ✅ Keep (hybrid) |
| Context | ✅ Plan progress | ✅ Same | ✅ Keep |

**Legend**:
- ✅ Keep as-is
- ➕ Add (missing)
- 🔧 Fix (incorrect)
- ⚠️ Needs work
- ⏸️ Defer (not urgent)

---

## Next Steps

1. **Review this evaluation** with team/user
2. **Decide**: Add domain layer now or defer?
3. **If now**: Create beads tasks for Phase 0
4. **If defer**: Document as technical debt, proceed with current plan
5. **Either way**: Fix terminology ("task plan formation" not "accommodation")

**Recommendation**: **Add domain layer now**. 8 hours investment prevents months of technical debt.
