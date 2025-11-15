"""Tests for travel booking domain."""

from ibdm.core.domain import DomainModel
from ibdm.core.questions import WhQuestion, YNQuestion
from ibdm.domains.travel_domain import (
    TRANSPORT_MODES,
    TRAVEL_CLASSES,
    _build_travel_plan,
    create_travel_domain,
    get_travel_domain,
)


class TestTravelDomainCreation:
    """Tests for travel domain creation."""

    def test_create_travel_domain(self):
        """Travel domain factory returns configured DomainModel."""
        domain = create_travel_domain()

        assert isinstance(domain, DomainModel)
        assert domain.name == "travel_booking"

    def test_travel_domain_predicates_present(self):
        """Travel domain contains Larsson travel predicates."""
        domain = create_travel_domain()

        expected = {
            "transport_mode",
            "depart_city",
            "dest_city",
            "depart_day",
            "return_day",
            "travel_class",
            "price_quote",
            "return_trip",
        }
        assert expected.issubset(domain.predicates.keys())

    def test_transport_mode_predicate(self):
        """transport_mode predicate matches transport_means sort."""
        domain = create_travel_domain()

        spec = domain.predicates["transport_mode"]
        assert spec.arity == 1
        assert spec.arg_types == ["transport_means"]
        assert "means of travel" in spec.description

    def test_return_trip_predicate(self):
        """return_trip predicate is arity 0."""
        domain = create_travel_domain()

        spec = domain.predicates["return_trip"]
        assert spec.arity == 0
        assert spec.arg_types == []
        assert "return" in spec.description


class TestTravelDomainSorts:
    """Tests for travel domain sorts."""

    def test_travel_domain_sorts_present(self):
        domain = create_travel_domain()

        for sort_name in [
            "transport_means",
            "city",
            "travel_day",
            "travel_class",
            "price_band",
        ]:
            assert sort_name in domain.sorts, f"Missing sort {sort_name}"

    def test_transport_means_values(self):
        domain = create_travel_domain()

        assert domain.sorts["transport_means"] == TRANSPORT_MODES

    def test_travel_class_values(self):
        domain = create_travel_domain()

        assert domain.sorts["travel_class"] == TRAVEL_CLASSES


class TestTravelDomainPlanBuilder:
    """Tests for travel domain plan builder."""

    def test_plan_builder_registered(self):
        domain = create_travel_domain()

        plan = domain.get_plan("travel_booking", {})
        assert plan.plan_type == "travel_booking"

    def test_build_travel_plan_default(self):
        plan = _build_travel_plan({})

        assert plan.plan_type == "travel_booking"
        assert plan.content == "travel_itinerary"
        assert plan.status == "active"
        assert len(plan.subplans) == 8  # includes return handling and price lookup

    def test_build_travel_plan_without_return(self):
        plan = _build_travel_plan({"include_return": False})

        assert len(plan.subplans) == 6  # skips return question + return day
        predicates = [
            sp.content.predicate for sp in plan.subplans[:4] if isinstance(sp.content, WhQuestion)
        ]
        assert "return_day" not in predicates

    def test_subplan_sequence(self):
        plan = _build_travel_plan({})

        first = plan.subplans[0]
        assert isinstance(first.content, WhQuestion)
        assert first.content.predicate == "transport_mode"

        second = plan.subplans[1]
        assert second.content.predicate == "depart_city"

        third = plan.subplans[2]
        assert third.content.predicate == "dest_city"

        fourth = plan.subplans[3]
        assert fourth.content.predicate == "depart_day"

        class_plan = plan.subplans[4]
        assert class_plan.content.predicate == "travel_class"

        return_gate = plan.subplans[5]
        assert isinstance(return_gate.content, YNQuestion)
        assert return_gate.content.proposition == "return_trip"

        return_day_plan = plan.subplans[6]
        assert isinstance(return_day_plan.content, WhQuestion)
        assert return_day_plan.content.predicate == "return_day"

        price_plan = plan.subplans[7]
        assert isinstance(price_plan.content, WhQuestion)
        assert price_plan.plan_type == "perform"
        assert price_plan.content.predicate == "price_quote"
        assert price_plan.status == "pending"

    def test_plan_uses_defined_predicates(self):
        domain = create_travel_domain()
        plan = _build_travel_plan({})

        for subplan in plan.subplans:
            if isinstance(subplan.content, WhQuestion):
                assert subplan.content.predicate in domain.predicates


class TestTravelDomainSingleton:
    """Tests for travel domain singleton."""

    def test_singleton_returns_domain(self):
        domain = get_travel_domain()

        assert isinstance(domain, DomainModel)
        assert domain.name == "travel_booking"

    def test_singleton_identity(self):
        domain1 = get_travel_domain()
        domain2 = get_travel_domain()

        assert domain1 is domain2
