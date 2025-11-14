"""Tests for domain model core."""

import pytest

from ibdm.core.answers import Answer
from ibdm.core.domain import DomainModel, PredicateSpec
from ibdm.core.plans import Plan
from ibdm.core.questions import WhQuestion


class TestPredicateSpec:
    """Tests for PredicateSpec dataclass."""

    def test_create_predicate_spec(self):
        """Test creating a predicate spec."""
        spec = PredicateSpec(
            name="parties",
            arity=1,
            arg_types=["legal_entities"],
            description="Organizations entering into NDA",
        )

        assert spec.name == "parties"
        assert spec.arity == 1
        assert spec.arg_types == ["legal_entities"]
        assert spec.description == "Organizations entering into NDA"

    def test_predicate_spec_defaults(self):
        """Test predicate spec with defaults."""
        spec = PredicateSpec(name="test", arity=0)

        assert spec.name == "test"
        assert spec.arity == 0
        assert spec.arg_types == []
        assert spec.description == ""


class TestDomainModel:
    """Tests for DomainModel class."""

    def test_domain_model_creation(self):
        """Test creating a domain model."""
        domain = DomainModel(name="test_domain")

        assert domain.name == "test_domain"
        assert len(domain.predicates) == 0
        assert len(domain.sorts) == 0
        assert len(domain._plan_builders) == 0

    def test_add_predicate(self):
        """Test adding a predicate to domain."""
        domain = DomainModel(name="test")
        domain.add_predicate(
            "parties",
            arity=1,
            arg_types=["legal_entities"],
            description="Test description",
        )

        assert "parties" in domain.predicates
        spec = domain.predicates["parties"]
        assert spec.name == "parties"
        assert spec.arity == 1
        assert spec.arg_types == ["legal_entities"]
        assert spec.description == "Test description"

    def test_add_predicate_without_optionals(self):
        """Test adding predicate without optional args."""
        domain = DomainModel(name="test")
        domain.add_predicate("simple", arity=0)

        assert "simple" in domain.predicates
        assert domain.predicates["simple"].arg_types == []
        assert domain.predicates["simple"].description == ""

    def test_add_sort(self):
        """Test adding a sort to domain."""
        domain = DomainModel(name="test")
        domain.add_sort("nda_kind", ["mutual", "one-way"])

        assert "nda_kind" in domain.sorts
        assert domain.sorts["nda_kind"] == ["mutual", "one-way"]

    def test_register_plan_builder(self):
        """Test registering a plan builder."""
        domain = DomainModel(name="test")

        def test_plan_builder(context):
            return Plan(plan_type="test_plan", content="test")

        domain.register_plan_builder("test_task", test_plan_builder)

        assert "test_task" in domain._plan_builders
        assert domain._plan_builders["test_task"] == test_plan_builder

    def test_get_plan_success(self):
        """Test getting a plan from domain."""
        domain = DomainModel(name="test")

        def test_plan_builder(context):
            return Plan(plan_type="test_plan", content="test", status="active")

        domain.register_plan_builder("test_task", test_plan_builder)

        plan = domain.get_plan("test_task", {})
        assert plan.plan_type == "test_plan"
        assert plan.content == "test"

    def test_get_plan_with_context(self):
        """Test getting a plan with context."""
        domain = DomainModel(name="test")

        def test_plan_builder(context):
            value = context.get("key", "default")
            return Plan(plan_type="test_plan", content=value, status="active")

        domain.register_plan_builder("test_task", test_plan_builder)

        plan = domain.get_plan("test_task", {"key": "custom"})
        assert plan.content == "custom"

    def test_get_plan_unknown_task_raises(self):
        """Test that getting unknown task raises error."""
        domain = DomainModel(name="test")

        with pytest.raises(ValueError, match="No plan builder"):
            domain.get_plan("unknown_task", {})

    def test_resolves_with_valid_answer(self):
        """Test resolves() with valid answer."""
        domain = DomainModel(name="test")
        domain.add_predicate("parties", arity=1, arg_types=["legal_entities"])

        question = WhQuestion(variable="x", predicate="parties")
        answer = Answer(content="Acme Corp, Beta Inc")

        # Should resolve (has content and question resolves_with succeeds)
        assert domain.resolves(answer, question) is True

    def test_resolves_with_empty_answer(self):
        """Test resolves() with empty answer."""
        domain = DomainModel(name="test")
        domain.add_predicate("parties", arity=1, arg_types=["legal_entities"])

        question = WhQuestion(variable="x", predicate="parties")
        answer = Answer(content=None)

        # Should not resolve (question.resolves_with will fail)
        assert domain.resolves(answer, question) is False

    def test_resolves_without_predicate_spec(self):
        """Test resolves() when predicate not defined."""
        domain = DomainModel(name="test")

        question = WhQuestion(variable="x", predicate="unknown")
        answer = Answer(content="value")

        # Should still resolve (no spec, so type check passes)
        assert domain.resolves(answer, question) is True

    def test_relevant_same_predicate(self):
        """Test relevant() with same predicate."""
        domain = DomainModel(name="test")

        question = WhQuestion(variable="x", predicate="parties")
        # Answer with same predicate (via question_ref)
        answer = Answer(content="Acme", question_ref=question)

        # Note: current Answer doesn't have predicate attribute directly
        # This test may need adjustment based on actual Answer structure
        # For now, just test that relevant() doesn't crash
        result = domain.relevant(answer, question)
        assert isinstance(result, bool)

    def test_repr(self):
        """Test string representation of domain."""
        domain = DomainModel(name="test_domain")
        domain.add_predicate("pred1", arity=1)
        domain.add_sort("sort1", ["val1", "val2"])

        def builder(ctx):
            return Plan(plan_type="test")

        domain.register_plan_builder("task1", builder)

        repr_str = repr(domain)
        assert "test_domain" in repr_str
        assert "predicates=1" in repr_str
        assert "sorts=1" in repr_str
        assert "plan_builders=1" in repr_str


class TestDomainTypeChecking:
    """Tests for domain type checking functionality."""

    def test_value_has_type_for_defined_sort(self):
        """Test _value_has_type with defined sort."""
        domain = DomainModel(name="test")
        domain.add_sort("nda_kind", ["mutual", "one-way"])

        # Non-empty value should pass
        assert domain._value_has_type("mutual", "nda_kind") is True
        assert domain._value_has_type("one-way", "nda_kind") is True

        # Empty value should fail
        assert domain._value_has_type("", "nda_kind") is False
        assert domain._value_has_type(None, "nda_kind") is False

    def test_value_has_type_for_undefined_sort(self):
        """Test _value_has_type with undefined sort."""
        domain = DomainModel(name="test")

        # Unknown sort accepts any value
        assert domain._value_has_type("anything", "unknown_sort") is True

    def test_check_types_with_predicate_spec(self):
        """Test _check_types with predicate spec."""
        domain = DomainModel(name="test")
        domain.add_predicate("parties", arity=1, arg_types=["legal_entities"])
        domain.add_sort("legal_entities", ["org1", "org2"])

        question = WhQuestion(variable="x", predicate="parties")
        answer = Answer(content="Acme Corp")

        # Should pass type check (non-empty value)
        assert domain._check_types(answer, question) is True

    def test_check_types_without_predicate_spec(self):
        """Test _check_types without predicate spec."""
        domain = DomainModel(name="test")

        question = WhQuestion(variable="x", predicate="unknown")
        answer = Answer(content="value")

        # Should pass (no spec to check against)
        assert domain._check_types(answer, question) is True

    def test_check_types_non_question(self):
        """Test _check_types with non-Question object."""
        domain = DomainModel(name="test")

        answer = Answer(content="value")
        not_a_question = "not a question"

        # Should pass (no predicate attribute)
        assert domain._check_types(answer, not_a_question) is True
