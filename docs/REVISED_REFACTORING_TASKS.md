# REVISED: NLU + IBDM + NLG Integration Tasks

**Supersedes**: Previous refactoring plan that incorrectly suggested keyword matching
**Based on**:
- ARCHITECTURE_NLU_IBDM_NLG_INTEGRATION.md
- PYTRINDIKIT_VERDICT.md (py-trindikit analysis findings)
**Updated**: 2025-11-14 - Phase 0, 2, 3 complete
**Key Principles**:
- Use existing NLU (no keywords)
- Add domain semantic layer (per py-trindikit analysis)
- Move task plan formation to integration
- Enhance plan-aware NLG

---

## The Correct Approach

**DO NOT** regress to keyword matching. We already have sophisticated NLU!

**DO** integrate the four layers properly:
1. **NLU** (already working) → interprets utterances semantically
2. **Domain Model** (NEW - needs implementation) → semantic grounding, type checking
3. **IBDM Integration** (needs fix) → forms task plans, manages QUD
4. **NLG** (needs enhancement) → generates context-aware responses

---

## Critical Finding from py-trindikit Analysis

**py-trindikit shows domain abstraction is integral to Larsson's IBDM!**

Current issues:
- ❌ Predicates are magic strings ("legal_entities", "time_period")
- ❌ No semantic grounding - what does "legal_entities" mean?
- ❌ No type checking - is "42" a valid legal_entity?
- ❌ No connection between NLU entities and IBDM predicates
- ❌ Hardcoded plans - can't reuse rules across domains

Solution: Add lightweight domain model (WITHOUT grammar, keep LLM-based NLU)

---

## Status Summary

### ✅ Completed Phases

**Phase 0: Domain Semantic Layer** (2025-11-14)
- All 6 tasks complete
- 61 tests passing (20 domain model + 25 NDA domain + 16 integration)
- Commits: 82fd7ac (integration rules), 38fa6c7 (domain semantic layer)

**Phase 2: Clean Up Interpretation Rules** (2025-11-14)
- Old accommodation code removed
- Terminology corrected (task plan formation, not accommodation)
- Commit: fd2e462

**Phase 3: Enhance NLG with Plan Context** (2025-11-14)
- Plan context helpers added
- Plan-aware question generation
- NDA-specific templates with progress indicators
- Commit: 21cdc04

### 🔄 In Progress / Pending

**Phase 4: Integration Testing**
- Task 4.3: Domain model integration verified ✅
- Tasks 4.1, 4.2: Pending (require LLM engine testing)

**Phase 5: Documentation**
- In progress

---

## Task Breakdown

### Phase 0: Domain Semantic Layer ⭐ COMPLETE

**Epic**: Add domain abstraction layer for semantic grounding
**Time**: 8 hours
**Priority**: P0
**Rationale**: py-trindikit analysis shows domain model is integral to Larsson's IBDM

#### Task 0.1: Create domain model core (P0)
**File**: `src/ibdm/core/domain.py`

```python
"""Domain model for Issue-Based Dialogue Management.

Provides semantic grounding for predicates without requiring grammar-based parsing.
Inspired by py-trindikit but adapted for LLM-based NLU.
"""

from dataclasses import dataclass, field
from typing import Any

from ibdm.core.answers import Answer
from ibdm.core.questions import Question, WhQuestion, YNQuestion
from ibdm.core.plans import Plan


@dataclass
class PredicateSpec:
    """Specification for a domain predicate.

    Example:
        PredicateSpec(
            name="parties",
            arity=1,
            arg_types=["legal_entities"],
            description="Organizations entering into NDA"
        )
    """
    name: str
    arity: int
    arg_types: list[str] = field(default_factory=list)
    description: str = ""


class DomainModel:
    """Lightweight domain model for IBDM.

    Provides:
    • Predicate definitions with types
    • Sort constraints (semantic types)
    • Semantic operations (relevant, resolves)
    • Plan retrieval

    Does NOT provide:
    • Grammar-based parsing (use LLM-based NLU instead)
    • Compositional semantics (accept emergent semantics from LLM)
    • Database integration (can add later if needed)

    Based on py-trindikit's Domain class but adapted for modern LLM approach.
    """

    def __init__(self, name: str):
        self.name = name
        self.predicates: dict[str, PredicateSpec] = {}
        self.sorts: dict[str, list[str]] = {}
        self._plan_builders: dict[str, callable] = {}

    def add_predicate(
        self,
        name: str,
        arity: int,
        arg_types: list[str] | None = None,
        description: str = ""
    ):
        """Register predicate with type signature."""
        self.predicates[name] = PredicateSpec(
            name=name,
            arity=arity,
            arg_types=arg_types or [],
            description=description
        )

    def add_sort(self, name: str, individuals: list[str]):
        """Register semantic sort with valid values.

        Example:
            domain.add_sort("nda_kind", ["mutual", "one-way"])
        """
        self.sorts[name] = individuals

    def register_plan_builder(self, task: str, builder: callable):
        """Register plan builder function for task."""
        self._plan_builders[task] = builder

    def resolves(self, answer: Answer, question: Question) -> bool:
        """Check if answer resolves question (with type checking).

        Delegates to Question.resolves_with() but adds domain-level
        type validation using predicate specs and sorts.
        """
        # First check basic resolution
        if not question.resolves_with(answer):
            return False

        # Then check types if predicate defined
        return self._check_types(answer, question)

    def relevant(self, prop: Any, question: Question) -> bool:
        """Check semantic relevance.

        Simple heuristic: same predicate = relevant
        Can be overridden in domain-specific implementations.
        """
        if hasattr(prop, "predicate") and hasattr(question, "predicate"):
            return prop.predicate == question.predicate
        return False

    def get_plan(self, task: str, context: dict | None = None) -> Plan:
        """Get dialogue plan for task.

        Dispatches to registered plan builder.
        """
        if task not in self._plan_builders:
            raise ValueError(f"No plan builder registered for task: {task}")

        return self._plan_builders[task](context or {})

    def _check_types(self, answer: Answer, question: Question) -> bool:
        """Verify answer value has correct type."""
        # Get predicate spec
        if not hasattr(question, "predicate"):
            return True

        pred_spec = self.predicates.get(question.predicate)
        if not pred_spec:
            return True  # No spec, accept

        # Type checking logic
        if pred_spec.arg_types:
            expected_type = pred_spec.arg_types[0]
            return self._value_has_type(answer.content, expected_type)

        return True

    def _value_has_type(self, value: Any, type_name: str) -> bool:
        """Check if value belongs to sort."""
        if type_name in self.sorts:
            # For now, accept any non-empty value for sorts
            # More sophisticated checking can be added
            return value is not None and str(value).strip() != ""
        return True  # Unknown type, accept
```

**Test**:
```python
def test_domain_model_creation():
    domain = DomainModel(name="test_domain")
    assert domain.name == "test_domain"
    assert len(domain.predicates) == 0

def test_add_predicate():
    domain = DomainModel(name="test")
    domain.add_predicate("parties", arity=1, arg_types=["legal_entities"])

    assert "parties" in domain.predicates
    assert domain.predicates["parties"].arity == 1
    assert domain.predicates["parties"].arg_types == ["legal_entities"]
```

**Time**: 2 hours

---

#### Task 0.2: Define NDA domain (P0)
**File**: `src/ibdm/domains/nda_domain.py`

```python
"""NDA drafting domain model.

Defines predicates, sorts, and plan builder for NDA drafting tasks.
"""

from ibdm.core.domain import DomainModel
from ibdm.core.plans import Plan
from ibdm.core.questions import WhQuestion, AltQuestion


def create_nda_domain() -> DomainModel:
    """Create NDA drafting domain model.

    Defines:
    • Predicates: parties, nda_type, effective_date, duration, governing_law
    • Sorts: nda_kind, jurisdiction
    • Plan builder: nda_drafting
    """
    domain = DomainModel(name="nda_drafting")

    # Define predicates
    domain.add_predicate(
        "legal_entities",
        arity=1,
        arg_types=["organization_list"],
        description="Organizations entering into NDA"
    )
    domain.add_predicate(
        "nda_type",
        arity=1,
        arg_types=["nda_kind"],
        description="Type of NDA (mutual or one-way)"
    )
    domain.add_predicate(
        "date",
        arity=1,
        arg_types=["date_string"],
        description="Effective date when NDA takes effect"
    )
    domain.add_predicate(
        "time_period",
        arity=1,
        arg_types=["duration_string"],
        description="Duration of confidentiality obligations"
    )
    domain.add_predicate(
        "jurisdiction",
        arity=1,
        arg_types=["us_state"],
        description="Governing law jurisdiction"
    )

    # Define sorts
    domain.add_sort("nda_kind", ["mutual", "one-way", "unilateral"])
    domain.add_sort("us_state", ["California", "Delaware", "New York"])

    # Register plan builder
    domain.register_plan_builder("nda_drafting", _build_nda_plan)

    return domain


def _build_nda_plan(context: dict) -> Plan:
    """Build NDA drafting plan.

    Creates findout plan for gathering NDA requirements.
    """
    subplans = [
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

    return Plan(
        plan_type="nda_drafting",
        content="nda_requirements",
        status="active",
        subplans=subplans
    )


# Singleton
_nda_domain = None

def get_nda_domain() -> DomainModel:
    """Get or create NDA domain singleton."""
    global _nda_domain
    if _nda_domain is None:
        _nda_domain = create_nda_domain()
    return _nda_domain
```

**Test**:
```python
def test_nda_domain_creation():
    domain = create_nda_domain()
    assert domain.name == "nda_drafting"
    assert "legal_entities" in domain.predicates
    assert "nda_kind" in domain.sorts
    assert domain.sorts["nda_kind"] == ["mutual", "one-way", "unilateral"]

def test_nda_domain_get_plan():
    domain = create_nda_domain()
    plan = domain.get_plan("nda_drafting", {})

    assert plan.plan_type == "nda_drafting"
    assert len(plan.subplans) == 5
    assert plan.subplans[0].content.predicate == "legal_entities"
```

**Time**: 1.5 hours

---

#### Task 0.3: Add NLU-domain entity mapper (P0)
**File**: `src/ibdm/nlu/domain_mapper.py`

```python
"""NLU entity to domain predicate mapper.

Maps generic NLU entities to domain-specific predicates.
"""

from ibdm.core.domain import DomainModel
from ibdm.nlu.entity_extractor import Entity, EntityType


class NLUDomainMapper:
    """Maps NLU entities to domain predicates.

    Bridges the gap between:
    • NLU's generic entities (ORGANIZATION, TEMPORAL, etc.)
    • Domain's semantic predicates (legal_entities, effective_date, etc.)
    """

    def __init__(self, domain: DomainModel):
        self.domain = domain

        # Define mapping rules
        self.entity_to_predicate = {
            EntityType.ORGANIZATION: "legal_entities",
            EntityType.TEMPORAL: "date",
            EntityType.DURATION: "time_period",
            EntityType.LOCATION: "jurisdiction",
        }

    def map_entities_to_answer(
        self,
        entities: list[Entity],
        question_predicate: str
    ) -> str | None:
        """Map extracted entities to answer content.

        Args:
            entities: List of entities from NLU
            question_predicate: Predicate being asked about

        Returns:
            Formatted answer content or None
        """
        # Filter entities by predicate type
        relevant_entities = []

        for entity_type, predicate in self.entity_to_predicate.items():
            if predicate == question_predicate:
                relevant_entities = [
                    e for e in entities
                    if e.entity_type == entity_type
                ]
                break

        if not relevant_entities:
            return None

        # Format based on predicate
        if question_predicate == "legal_entities":
            # Multiple organizations
            return ", ".join([e.text for e in relevant_entities])
        else:
            # Single value
            return relevant_entities[0].text
```

**Test**:
```python
def test_entity_mapper_maps_organizations():
    domain = create_nda_domain()
    mapper = NLUDomainMapper(domain)

    entities = [
        Entity(text="Acme Corp", entity_type=EntityType.ORGANIZATION),
        Entity(text="Beta Inc", entity_type=EntityType.ORGANIZATION),
    ]

    result = mapper.map_entities_to_answer(entities, "legal_entities")
    assert result == "Acme Corp, Beta Inc"
```

**Time**: 1.5 hours

---

#### Task 0.4: Update integration rules to use domain (P0)
**File**: `src/ibdm/rules/integration_rules.py`

Add domain parameter and update `_create_nda_plan()` to use domain:

```python
def _form_task_plan(state):
    """Form execution plan for user's task.

    RENAMED from _accommodate_task to clarify this is task plan formation,
    not Larsson's presupposition accommodation.

    Uses domain model to get appropriate plan.
    """
    move = state.private.beliefs.get("_temp_move")
    new_state = state.clone()

    # Get task type
    task_type = move.metadata.get("task_type")
    intent = move.metadata.get("intent")

    if not task_type:
        classifier = _get_task_classifier()
        result = classifier.classify(str(move.content))
        task_type = result.task_type
        intent = result.parameters.get("document_type", "")

    # Dispatch to domain
    if task_type == "DRAFT_DOCUMENT" or "draft" in intent.lower():
        if "NDA" in intent.upper() or "NDA" in str(move.content).upper():
            # Get domain and plan
            from ibdm.domains.nda_domain import get_nda_domain
            domain = get_nda_domain()

            # Use domain to get plan (not hardcoded!)
            context = _extract_context(move, state)
            plan = domain.get_plan("nda_drafting", context)

            new_state.private.plan.append(plan)

            # Push first question to QUD
            if plan.subplans:
                first_question = plan.subplans[0].content
                new_state.shared.push_qud(first_question)

    new_state.shared.last_moves.append(move)
    new_state.control.next_speaker = new_state.agent_id

    return new_state

def _extract_context(move, state):
    """Extract context from move for plan building."""
    # Can extract entities, intent details, etc.
    return {}
```

Also rename rule:
```python
UpdateRule(
    name="form_task_plan",  # Renamed from accommodate_command
    preconditions=_is_command_or_request_move,
    effects=_form_task_plan,  # Renamed from _accommodate_task
    priority=13,
    rule_type="integration"
)
```

**Time**: 1 hour

---

#### Task 0.5: Unit tests for domain model (P0)
**File**: `tests/unit/test_domain_model.py`

```python
"""Tests for domain model core."""

import pytest

from ibdm.core.domain import DomainModel, PredicateSpec
from ibdm.core.answers import Answer
from ibdm.core.questions import WhQuestion


def test_domain_model_creation():
    domain = DomainModel(name="test_domain")
    assert domain.name == "test_domain"
    assert len(domain.predicates) == 0
    assert len(domain.sorts) == 0


def test_add_predicate():
    domain = DomainModel(name="test")
    domain.add_predicate(
        "parties",
        arity=1,
        arg_types=["legal_entities"],
        description="Test description"
    )

    assert "parties" in domain.predicates
    spec = domain.predicates["parties"]
    assert spec.name == "parties"
    assert spec.arity == 1
    assert spec.arg_types == ["legal_entities"]
    assert spec.description == "Test description"


def test_add_sort():
    domain = DomainModel(name="test")
    domain.add_sort("nda_kind", ["mutual", "one-way"])

    assert "nda_kind" in domain.sorts
    assert domain.sorts["nda_kind"] == ["mutual", "one-way"]


def test_resolves_with_valid_answer():
    domain = DomainModel(name="test")
    domain.add_predicate("parties", arity=1, arg_types=["legal_entities"])

    question = WhQuestion(variable="x", predicate="parties")
    answer = Answer(content="Acme Corp, Beta Inc")

    # Should resolve (has content)
    assert domain.resolves(answer, question) == True


def test_register_and_get_plan():
    domain = DomainModel(name="test")

    def test_plan_builder(context):
        from ibdm.core.plans import Plan
        return Plan(plan_type="test_plan", content="test")

    domain.register_plan_builder("test_task", test_plan_builder)

    plan = domain.get_plan("test_task", {})
    assert plan.plan_type == "test_plan"


def test_get_plan_unknown_task_raises():
    domain = DomainModel(name="test")

    with pytest.raises(ValueError, match="No plan builder"):
        domain.get_plan("unknown_task", {})
```

**File**: `tests/unit/test_nda_domain.py`

```python
"""Tests for NDA domain."""

from ibdm.domains.nda_domain import create_nda_domain, get_nda_domain


def test_nda_domain_creation():
    domain = create_nda_domain()
    assert domain.name == "nda_drafting"


def test_nda_domain_has_predicates():
    domain = create_nda_domain()

    assert "legal_entities" in domain.predicates
    assert "nda_type" in domain.predicates
    assert "date" in domain.predicates
    assert "time_period" in domain.predicates
    assert "jurisdiction" in domain.predicates


def test_nda_domain_has_sorts():
    domain = create_nda_domain()

    assert "nda_kind" in domain.sorts
    assert domain.sorts["nda_kind"] == ["mutual", "one-way", "unilateral"]

    assert "us_state" in domain.sorts
    assert "California" in domain.sorts["us_state"]


def test_nda_domain_get_plan():
    domain = create_nda_domain()
    plan = domain.get_plan("nda_drafting", {})

    assert plan.plan_type == "nda_drafting"
    assert len(plan.subplans) == 5

    # Check first subplan
    first = plan.subplans[0]
    assert first.plan_type == "findout"
    assert first.content.predicate == "legal_entities"


def test_get_nda_domain_singleton():
    domain1 = get_nda_domain()
    domain2 = get_nda_domain()
    assert domain1 is domain2
```

**Time**: 1 hour

---

#### Task 0.6: Integration test with domain (P0)
**File**: `tests/integration/test_nda_with_domain.py`

```python
"""Integration test: NDA workflow with domain model."""

from ibdm.core.information_state import InformationState
from ibdm.engine.nlu_engine import NLUDialogueEngine
from ibdm.domains.nda_domain import get_nda_domain


def test_nda_workflow_uses_domain():
    """Test complete NDA workflow using domain model."""
    domain = get_nda_domain()
    engine = NLUDialogueEngine(agent_id="system")
    state = InformationState(agent_id="system")

    # User: "I need to draft an NDA"
    moves = engine.interpret("I need to draft an NDA", "user", state)

    for move in moves:
        state = engine.integrate(move, state)

    # Verify domain.get_plan() was called
    assert len(state.private.plan) == 1
    assert state.private.plan[0].plan_type == "nda_drafting"

    # Verify first question on QUD
    assert len(state.shared.qud) == 1
    question = state.shared.qud.top()
    assert question.predicate == "legal_entities"

    # Verify predicate is defined in domain
    assert "legal_entities" in domain.predicates
```

**Time**: 1 hour

**Total Phase 0 Time**: 8 hours

---

### Phase 1: Move Task Plan Formation to Integration ⭐ CRITICAL

**Epic**: Move task plan formation from interpretation to integration (RENAMED from "accommodation")
**Time**: 3 hours
**Priority**: P0
**Changes**:
- Renamed from "accommodation" to "task plan formation" per Larsson critique
- Now uses domain model from Phase 0

#### Task 1.1: Add form_task_plan integration rule (P0)
**File**: `src/ibdm/rules/integration_rules.py`

```python
# Add new rule (renamed from accommodate_command)
UpdateRule(
    name="form_task_plan",
    preconditions=_is_command_or_request_move,
    effects=_form_task_plan,  # Renamed from _accommodate_task
    priority=13,  # Highest - before other integrations
    rule_type="integration"
)

def _is_command_or_request_move(state):
    """Check for command or request moves from NLU or rules."""
    move = state.private.beliefs.get("_temp_move")
    return isinstance(move, DialogueMove) and \
           move.move_type in ["command", "request"]
```

**Test**:
```python
def test_form_task_plan_rule_triggers():
    state = create_test_state()
    move = DialogueMove(type="command", content="I need to draft an NDA")
    state.private.beliefs["_temp_move"] = move

    assert _is_command_or_request_move(state) == True
```

**Time**: 30 min

---

#### Task 1.2: Implement _form_task_plan() using domain (P0)
**File**: `src/ibdm/rules/integration_rules.py`

Implementation provided in Task 0.4 (already uses domain model).

**Additional test**:
```python
def test_form_task_plan_uses_domain():
    """Verify task plan formation uses domain model."""
    state = create_test_state()
    move = DialogueMove(
        type="command",
        content="I need to draft an NDA",
        metadata={"intent": "draft_document", "task_type": "NDA"}
    )
    state.private.beliefs["_temp_move"] = move

    new_state = _form_task_plan(state)

    # Plan should come from domain
    assert len(new_state.private.plan) == 1
    plan = new_state.private.plan[0]

    # Verify it's the domain-generated plan
    from ibdm.domains.nda_domain import get_nda_domain
    domain = get_nda_domain()
    expected_plan = domain.get_plan("nda_drafting", {})

    assert plan.plan_type == expected_plan.plan_type
    assert len(plan.subplans) == len(expected_plan.subplans)
```

**Time**: 1.5 hours

---

#### Task 1.3: Integration tests for task plan formation (P1)
**File**: `tests/unit/test_integration_rules.py`

Add tests:
- `test_form_task_plan_rule_exists()`
- `test_form_task_plan_uses_domain()`
- `test_qud_pushed_after_plan_formation()`
- `test_nlu_command_triggers_plan_formation()`
- `test_next_speaker_set_after_plan_formation()`

**Time**: 1 hour

**Total Phase 1 Time**: 3 hours

---

### Phase 2: Clean Up Interpretation Rules

**Epic**: Remove task plan formation from interpretation phase
**Time**: 1 hour
**Priority**: P1
**Changes**: Remove old accommodation code, update comments

#### Task 2.1: Remove accommodate_nda_task from interpretation (P1)
**File**: `src/ibdm/rules/interpretation_rules.py`

Delete:
- `accommodate_nda_task` rule
- `_is_nda_request()` function
- `_create_nda_plan()` function (now in `nda_domain.py`)
- `_task_classifier` global
- `_get_task_classifier()` function (moved to integration)

**Time**: 20 min

---

#### Task 2.2: Update interpretation docstrings (P2)
**File**: `src/ibdm/rules/interpretation_rules.py`

Update module docstring:
```python
"""Interpretation rules for Issue-Based Dialogue Management.

Interpretation rules map utterances to dialogue moves. They are SYNTACTIC/SEMANTIC ONLY.

Task plan formation (creating plans for user tasks) happens in the INTEGRATION phase,
not here. See integration_rules.py for task plan formation logic.

Key distinction (Larsson 2002):
• INTERPRETATION: Utterance → DialogueMove (syntactic/semantic)
• INTEGRATION: DialogueMove → State changes, plan formation (pragmatic)

Based on Larsson (2002) Issue-based Dialogue Management.
"""
```

**Time**: 10 min

---

#### Task 2.3: Verify tests still pass (P1)
**Command**: `pytest tests/unit/test_interpretation_rules.py -v`

Ensure no tests rely on task plan formation in interpretation.

**Time**: 30 min

**Total Phase 2 Time**: 1 hour

---

### Phase 3: Enhance NLG with Plan Context

**Epic**: Generate context-aware, natural responses
**Time**: 2 hours
**Priority**: P1
**Changes**: Can use domain descriptions for better generation

#### Task 3.1: Add plan context helpers (P1)
**File**: `src/ibdm/rules/generation_rules.py`

```python
def _get_active_plan(state):
    """Get currently active plan, if any."""
    for plan in state.private.plan:
        if plan.is_active():
            return plan
    return None

def _get_plan_progress(plan):
    """Get plan progress (completed, total)."""
    if not plan or not plan.subplans:
        return (0, 0)

    completed = sum(1 for sp in plan.subplans if sp.status == "completed")
    total = len(plan.subplans)
    return (completed, total)

def _get_domain_for_plan(plan):
    """Get domain model for plan."""
    if plan.plan_type == "nda_drafting":
        from ibdm.domains.nda_domain import get_nda_domain
        return get_nda_domain()
    return None
```

**Time**: 15 min

---

#### Task 3.2: Update _generate_question_text() for plan awareness (P1)
**File**: `src/ibdm/rules/generation_rules.py`

```python
def _generate_question_text(state):
    """Generate text for a question move with plan awareness."""
    new_state = state.clone()
    move = new_state.private.beliefs.get("_temp_generate_move")
    question = move.content

    # Check for active plan
    active_plan = _get_active_plan(state)

    if active_plan:
        # Plan-driven generation
        if active_plan.plan_type == "nda_drafting":
            text = _generate_nda_question(question, active_plan, state)
        else:
            # Fallback for unknown plan types
            text = _generate_generic_question(question)
    else:
        # No active plan - use generic
        text = _generate_generic_question(question)

    new_state.private.beliefs["_temp_generated_text"] = text
    return new_state

def _generate_generic_question(question):
    """Generic question generation (existing logic)."""
    if isinstance(question, WhQuestion):
        wh_word = question.constraints.get("wh_word", "what")
        predicate = question.predicate.replace("_", " ")
        return f"{wh_word.capitalize()} {predicate}?"
    elif isinstance(question, YNQuestion):
        proposition = question.proposition.replace("_", " ")
        return f"{proposition.capitalize()}?"
    elif isinstance(question, AltQuestion):
        if len(question.alternatives) == 2:
            return f"{question.alternatives[0].capitalize()} or {question.alternatives[1]}?"
        else:
            alt_list = ", ".join(question.alternatives[:-1])
            return f"{alt_list.capitalize()}, or {question.alternatives[-1]}?"
    else:
        return str(question)
```

**Time**: 30 min

---

#### Task 3.3: Implement NDA-specific question templates (P1)
**File**: `src/ibdm/rules/generation_rules.py`

```python
def _generate_nda_question(question, plan, state):
    """Generate NDA-specific question with context and progress.

    Can use domain model descriptions for better phrasing.
    """
    completed, total = _get_plan_progress(plan)

    # Get domain for predicate descriptions
    domain = _get_domain_for_plan(plan)

    # WhQuestions
    if isinstance(question, WhQuestion):
        # Can use domain.predicates[question.predicate].description
        if question.predicate == "legal_entities":
            prefix = "Let's start with the basics." if completed == 0 else ""
            return f"{prefix} Who are the organizations entering into this NDA?".strip()

        elif question.predicate == "date":
            return f"What effective date should we use for this agreement? (Step {completed+1} of {total})"

        elif question.predicate == "time_period":
            return f"How long should the confidentiality obligations last? Common periods are 2-5 years. (Step {completed+1} of {total})"

    # AltQuestions
    elif isinstance(question, AltQuestion):
        if "mutual" in [a.lower() for a in question.alternatives]:
            return f"Will this be a mutual NDA (both parties share confidential info) or one-way? (Step {completed+1} of {total})"

        elif "california" in [a.lower() for a in question.alternatives]:
            return f"Which state's laws should govern this agreement - California, Delaware, or New York? (Step {completed+1} of {total})"

    # Fallback
    return _generate_generic_question(question)
```

**Time**: 45 min

---

#### Task 3.4: Add progress feedback (P2)
**File**: `src/ibdm/rules/generation_rules.py`

Add acknowledgment templates that show progress:
```python
def _generate_answer_acknowledgment(state, active_plan):
    """Generate acknowledgment with progress."""
    if not active_plan:
        return "Thank you."

    completed, total = _get_plan_progress(active_plan)

    if completed < total:
        return f"Great! That's {completed} of {total} requirements."
    else:
        return "Perfect! I have all the information needed to draft your NDA."
```

**Time**: 30 min

**Total Phase 3 Time**: 2 hours

---

### Phase 4: Integration Testing

**Epic**: Verify complete NLU → Domain → IBDM → NLG pipeline
**Time**: 2 hours
**Priority**: P1

#### Task 4.1: Create comprehensive NDA workflow test (P1)
**File**: `tests/integration/test_complete_nda_workflow.py`

```python
def test_complete_nda_workflow_with_domain():
    """Test complete NDA workflow using domain model."""
    # Setup
    engine = NLUDialogueEngine(agent_id="system", rules=create_all_rules())
    state = InformationState(agent_id="system")

    # Turn 1: User requests NDA
    utterance = "I need to draft an NDA"
    moves = engine.interpret(utterance, "user", state)

    assert len(moves) == 1
    assert moves[0].move_type == "command"

    # Integrate (should trigger task plan formation via domain)
    for move in moves:
        state = engine.integrate(move, state)

    # Check plan was created from domain
    assert len(state.private.plan) == 1
    assert state.private.plan[0].plan_type == "nda_drafting"

    # Verify domain predicates in questions
    from ibdm.domains.nda_domain import get_nda_domain
    domain = get_nda_domain()

    first_question = state.shared.qud.top()
    assert first_question.predicate in domain.predicates

    # Select and generate
    response_move, state = engine.select_action(state)
    assert response_move.move_type == "ask"

    response_text = engine.generate(response_move, state)
    assert "parties" in response_text.lower() or "organizations" in response_text.lower()

    # Continue through all 5 questions...
    # (Full test would go through entire workflow)
```

**Time**: 1 hour

---

#### Task 4.2: Manual testing with interactive demo (P1)
**File**: `demos/03_nlu_integration_interactive.py`

Test scenarios:
1. "I need to draft an NDA" → should ask about parties
2. "Help me create an NDA" → same behavior
3. "Draft a confidentiality agreement" → same behavior
4. Answer all 5 questions → get final confirmation

Document results.

**Time**: 30 min

---

#### Task 4.3: Verify domain model integration (P2)
Test that:
- Domain predicates are used consistently
- Type checking works (if applicable)
- Plan comes from domain.get_plan()
- Generation can use domain descriptions

**Time**: 30 min

**Total Phase 4 Time**: 2 hours

---

### Phase 5: Documentation

**Epic**: Update all documentation
**Time**: 1 hour
**Priority**: P2

#### Task 5.1: Update architectural documentation (P2)

Mark resolved and document domain layer:
```markdown
# ✅ RESOLVED: 2025-11-13

Task plan formation has been moved to the integration phase.
Domain semantic layer has been added per py-trindikit analysis.

See:
- docs/ARCHITECTURE_NLU_IBDM_NLG_INTEGRATION.md
- docs/PYTRINDIKIT_VERDICT.md
- docs/PY_TRINDIKIT_ANALYSIS.md
```

**Time**: 10 min

---

#### Task 5.2: Update CLAUDE.md policy (P2)
**File**: `CLAUDE.md`

Add architectural principle:
```markdown
### Policy #10: Domain Semantic Layer

**Policy**: All domains must define predicates, sorts, and semantic operations explicitly.

**Rationale**: Per Larsson (2002) and py-trindikit analysis, domain abstraction is integral to IBDM. It provides semantic grounding, type safety, and enables domain-independent rules.

**Implementation**:
- Define domain model with predicates and sorts
- Register plan builders with domain
- Use domain.get_plan() not hardcoded plans
- Use domain.resolves() for type-checked answer validation

**Example**: NDA domain
- Predicates: legal_entities, nda_type, effective_date, duration, jurisdiction
- Sorts: nda_kind (mutual/one-way), us_state (CA/DE/NY)
- Plan builder: creates 5-step findout plan

### Policy #11: Task Plan Formation in Integration Phase

**Policy**: Task plan formation (creating plans for user tasks) belongs in the INTEGRATION phase, not interpretation.

**Terminology**: Call it "task plan formation" NOT "accommodation". Larsson's "accommodation" refers to presupposition accommodation, which is different.

**Implementation**:
- NLU engine interprets utterances → creates DialogueMoves
- Integration rules form task plans → create plans via domain
- Selection rules execute plans → choose next action
- Generation rules realize moves → produce natural language

**Example**: NDA request
1. INTERPRET: "I need an NDA" → DialogueMove(type="command")
2. INTEGRATE: Command move → domain.get_plan("nda_drafting") → push first question to QUD
3. SELECT: Execute plan → ask first question
4. GENERATE: Use NDA template → "Who are the organizations..."
```

**Time**: 20 min

---

#### Task 5.3: Update burr_state_refactoring.md (P2)
**File**: `docs/burr_state_refactoring.md`

Update to reflect:
- Task plan formation in integration
- Domain model usage
- Correct terminology

**Time**: 15 min

---

#### Task 5.4: Update demo documentation (P2)
**File**: `demos/README.md`

Update description of 03_nlu_integration_interactive.py to explain:
- NLU interprets utterances
- Domain provides semantic grounding
- Integration forms task plans
- System asks context-aware questions
- Natural conversation flow

**Time**: 15 min

**Total Phase 5 Time**: 1 hour

---

## Summary

### Total Effort: 17 hours (was 9 hours)

| Phase | Tasks | Time | Priority |
|-------|-------|------|----------|
| **0. Domain Semantic Layer** | **6** | **8 hours** | **P0** |
| 1. Move Task Plan Formation | 3 | 3 hours | P0 |
| 2. Clean Up | 3 | 1 hour | P1 |
| 3. Enhance NLG | 4 | 2 hours | P1 |
| 4. Integration Testing | 3 | 2 hours | P1 |
| 5. Documentation | 4 | 1 hour | P2 |

### What Changed from Previous Version

**ADDED** (from py-trindikit analysis):
- ✅ Phase 0: Domain Semantic Layer (8 hours)
  - Domain model core with predicates, sorts
  - NDA domain definition
  - NLU-domain entity mapper
  - Type checking support

**RENAMED** (terminology fix):
- ✅ "Accommodation" → "Task Plan Formation"
- ✅ `accommodate_command` → `form_task_plan`
- ✅ `_accommodate_task()` → `_form_task_plan()`

**KEPT** (correct approach):
- ✅ Use existing NLU for interpretation
- ✅ Move task plan formation to integration
- ✅ Plan-aware NLG
- ✅ Clean separation of concerns

### Key Differences from Original Plan

**REMOVED** (wrong approach):
- ❌ Keyword-based request detection
- ❌ Hybrid rule + NLU approach
- ❌ Hardcoded plan creation

**KEPT** (correct approach):
- ✅ Use existing NLU for interpretation
- ✅ Task plan formation in integration (correct phase per Larsson)
- ✅ Plan-aware NLG
- ✅ Clean separation of concerns

**ADDED** (py-trindikit findings):
- ✅ Domain semantic layer (predicates, sorts, semantic operations)
- ✅ Domain-independent rule methods
- ✅ Type checking via domain model
- ✅ Systematic NLU-domain mapping

### Success Criteria

- ✅ No keyword matching (NLU does interpretation)
- ✅ Domain model provides semantic grounding
- ✅ Task plan formation in integration phase
- ✅ Plans come from domain.get_plan() not hardcoded
- ✅ Works with NLU-created moves
- ✅ Plan-aware NLG generates natural responses
- ✅ Terminology correct ("task plan formation" not "accommodation")
- ✅ ~95% Larsson fidelity (up from ~85%)
- ✅ Demo shows: "Let's start with the parties..." not "How can I help?"
- ✅ All tests pass

### Benefits of Domain Layer Addition

1. **Semantic Grounding**: Predicates have meaning, not just strings
2. **Type Safety**: Validate answers against sorts
3. **Extensibility**: Add new domains easily (contracts in 2 hours)
4. **Larsson Fidelity**: ~95% faithful to IBDM framework
5. **Code Clarity**: Domain model IS the specification
6. **Reusability**: Same rules work across domains
7. **Maintainability**: Changes localized to domain definitions

---

## Next Steps

1. Review this updated plan
2. Start with Phase 0, Task 0.1 (create domain model core)
3. Work through phases sequentially
4. Test after each task
5. Small commits following CLAUDE.md policy

---

## References

- **Correct Design**: docs/ARCHITECTURE_NLU_IBDM_NLG_INTEGRATION.md
- **py-trindikit Analysis**: docs/PY_TRINDIKIT_ANALYSIS.md (1,720 lines)
- **Plan Evaluation**: docs/PLAN_EVALUATION_AFTER_PYTRINDIKIT.md
- **Verdict**: docs/PYTRINDIKIT_VERDICT.md
- **Larsson Critique**: docs/LARSSON_FRAMEWORK_CRITIQUE.md
- **NLU Implementation**: src/ibdm/engine/nlu_engine.py (already correct!)
- **Integration Rules**: src/ibdm/rules/integration_rules.py (needs domain + task plan formation)
- **Generation Rules**: src/ibdm/rules/generation_rules.py (needs plan awareness)
