"""Tests for NDA domain."""

from ibdm.core.domain import DomainModel
from ibdm.core.questions import AltQuestion, WhQuestion
from ibdm.domains.nda_domain import _build_nda_plan, create_nda_domain, get_nda_domain


class TestNDADomainCreation:
    """Tests for NDA domain creation."""

    def test_create_nda_domain(self):
        """Test creating NDA domain."""
        domain = create_nda_domain()

        assert isinstance(domain, DomainModel)
        assert domain.name == "nda_drafting"

    def test_nda_domain_has_predicates(self):
        """Test NDA domain has all required predicates."""
        domain = create_nda_domain()

        expected_predicates = [
            "legal_entities",
            "nda_type",
            "date",
            "time_period",
            "jurisdiction",
        ]

        for pred in expected_predicates:
            assert pred in domain.predicates, f"Missing predicate: {pred}"

    def test_legal_entities_predicate(self):
        """Test legal_entities predicate definition."""
        domain = create_nda_domain()

        pred_spec = domain.predicates["legal_entities"]
        assert pred_spec.name == "legal_entities"
        assert pred_spec.arity == 1
        assert pred_spec.arg_types == ["organization_list"]
        assert "Organizations entering into NDA" in pred_spec.description

    def test_nda_type_predicate(self):
        """Test nda_type predicate definition."""
        domain = create_nda_domain()

        pred_spec = domain.predicates["nda_type"]
        assert pred_spec.name == "nda_type"
        assert pred_spec.arity == 1
        assert pred_spec.arg_types == ["nda_kind"]
        assert "mutual or one-way" in pred_spec.description

    def test_date_predicate(self):
        """Test date predicate definition."""
        domain = create_nda_domain()

        pred_spec = domain.predicates["date"]
        assert pred_spec.name == "date"
        assert pred_spec.arity == 1
        assert pred_spec.arg_types == ["date_string"]
        assert "Effective date" in pred_spec.description

    def test_time_period_predicate(self):
        """Test time_period predicate definition."""
        domain = create_nda_domain()

        pred_spec = domain.predicates["time_period"]
        assert pred_spec.name == "time_period"
        assert pred_spec.arity == 1
        assert pred_spec.arg_types == ["duration_string"]
        assert "Duration" in pred_spec.description

    def test_jurisdiction_predicate(self):
        """Test jurisdiction predicate definition."""
        domain = create_nda_domain()

        pred_spec = domain.predicates["jurisdiction"]
        assert pred_spec.name == "jurisdiction"
        assert pred_spec.arity == 1
        assert pred_spec.arg_types == ["us_state"]
        assert "Governing law" in pred_spec.description


class TestNDADomainSorts:
    """Tests for NDA domain sorts."""

    def test_nda_domain_has_sorts(self):
        """Test NDA domain has all required sorts."""
        domain = create_nda_domain()

        assert "nda_kind" in domain.sorts
        assert "us_state" in domain.sorts

    def test_nda_kind_sort(self):
        """Test nda_kind sort values."""
        domain = create_nda_domain()

        nda_kinds = domain.sorts["nda_kind"]
        assert "mutual" in nda_kinds
        assert "one-way" in nda_kinds
        assert "unilateral" in nda_kinds
        assert len(nda_kinds) == 3

    def test_us_state_sort(self):
        """Test us_state sort values."""
        domain = create_nda_domain()

        us_states = domain.sorts["us_state"]
        assert "California" in us_states
        assert "Delaware" in us_states
        assert "New York" in us_states
        assert len(us_states) == 3


class TestNDADomainPlanBuilder:
    """Tests for NDA domain plan builder."""

    def test_nda_plan_builder_registered(self):
        """Test that plan builder is registered."""
        domain = create_nda_domain()

        # Should not raise
        plan = domain.get_plan("nda_drafting", {})
        assert plan is not None

    def test_build_nda_plan(self):
        """Test _build_nda_plan function."""
        plan = _build_nda_plan({})

        assert plan.plan_type == "nda_drafting"
        assert plan.content == "nda_requirements"
        assert plan.status == "active"
        assert plan.subplans is not None

    def test_nda_plan_has_five_subplans(self):
        """Test NDA plan has 5 subplans."""
        plan = _build_nda_plan({})

        assert len(plan.subplans) == 5

    def test_nda_plan_subplan_types(self):
        """Test NDA plan subplan types."""
        plan = _build_nda_plan({})

        for subplan in plan.subplans:
            assert subplan.plan_type == "findout"
            assert subplan.status == "active"

    def test_nda_plan_first_subplan_parties(self):
        """Test first subplan is for legal entities."""
        plan = _build_nda_plan({})

        first = plan.subplans[0]
        assert isinstance(first.content, WhQuestion)
        assert first.content.predicate == "legal_entities"
        assert first.content.variable == "parties"

    def test_nda_plan_second_subplan_nda_type(self):
        """Test second subplan is for NDA type."""
        plan = _build_nda_plan({})

        second = plan.subplans[1]
        assert isinstance(second.content, AltQuestion)
        assert "mutual" in second.content.alternatives
        assert "one-way" in second.content.alternatives

    def test_nda_plan_third_subplan_effective_date(self):
        """Test third subplan is for effective date."""
        plan = _build_nda_plan({})

        third = plan.subplans[2]
        assert isinstance(third.content, WhQuestion)
        assert third.content.predicate == "date"
        assert third.content.variable == "effective_date"

    def test_nda_plan_fourth_subplan_duration(self):
        """Test fourth subplan is for duration."""
        plan = _build_nda_plan({})

        fourth = plan.subplans[3]
        assert isinstance(fourth.content, WhQuestion)
        assert fourth.content.predicate == "time_period"
        assert fourth.content.variable == "duration"

    def test_nda_plan_fifth_subplan_jurisdiction(self):
        """Test fifth subplan is for jurisdiction."""
        plan = _build_nda_plan({})

        fifth = plan.subplans[4]
        assert isinstance(fifth.content, AltQuestion)
        assert "California" in fifth.content.alternatives
        assert "Delaware" in fifth.content.alternatives
        assert "New York" in fifth.content.alternatives


class TestNDADomainSingleton:
    """Tests for NDA domain singleton pattern."""

    def test_get_nda_domain_returns_domain(self):
        """Test get_nda_domain returns DomainModel."""
        domain = get_nda_domain()

        assert isinstance(domain, DomainModel)
        assert domain.name == "nda_drafting"

    def test_get_nda_domain_is_singleton(self):
        """Test get_nda_domain returns same instance."""
        domain1 = get_nda_domain()
        domain2 = get_nda_domain()

        assert domain1 is domain2  # Same object instance

    def test_singleton_has_all_features(self):
        """Test singleton has all predicates and sorts."""
        domain = get_nda_domain()

        # Should have predicates
        assert len(domain.predicates) == 5

        # Should have sorts
        assert len(domain.sorts) == 2

        # Should have plan builder
        plan = domain.get_plan("nda_drafting", {})
        assert plan.plan_type == "nda_drafting"


class TestNDADomainIntegration:
    """Integration tests for NDA domain usage."""

    def test_domain_get_plan_via_singleton(self):
        """Test getting plan via singleton."""
        domain = get_nda_domain()
        plan = domain.get_plan("nda_drafting", {})

        assert plan.plan_type == "nda_drafting"
        assert len(plan.subplans) == 5

    def test_predicates_match_plan_questions(self):
        """Test that plan questions use defined predicates."""
        domain = get_nda_domain()
        plan = domain.get_plan("nda_drafting", {})

        # Collect predicates from plan questions
        plan_predicates = set()
        for subplan in plan.subplans:
            if isinstance(subplan.content, WhQuestion):
                plan_predicates.add(subplan.content.predicate)

        # All should be defined in domain
        for pred in plan_predicates:
            assert pred in domain.predicates, f"Plan uses undefined predicate: {pred}"

    def test_all_predicate_descriptions_present(self):
        """Test that all predicates have descriptions."""
        domain = get_nda_domain()

        for pred_name, pred_spec in domain.predicates.items():
            assert pred_spec.description, f"Predicate {pred_name} missing description"
            assert len(pred_spec.description) > 10, f"{pred_name} has too short description"
