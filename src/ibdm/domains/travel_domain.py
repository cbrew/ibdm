"""Travel booking domain model inspired by Larsson (2002).

This mirrors the classic travel agency scenarios used in the IBiS / TRINDI
work, providing predicates, sorts, and dialogue plans for collecting itinerary
constraints before consulting a database.
"""

from typing import Any

from ibdm.core.domain import DomainModel
from ibdm.core.plans import Plan
from ibdm.core.questions import WhQuestion, YNQuestion

TRANSPORT_MODES = ["plane", "train"]
MAJOR_CITIES = ["paris", "london", "berlin", "stockholm"]
TRAVEL_DAYS = ["today", "tomorrow", "next week"]
TRAVEL_CLASSES = ["economy", "business", "first"]


def create_travel_domain() -> DomainModel:
    """Create travel booking domain model.

    Defines:
    • Predicates: transport_mode, depart_city, dest_city, depart_day, return_day,
      travel_class, price_quote, return_trip
    • Sorts: transport_means, city, travel_day, travel_class, price_band
    • Plan builder: travel_booking

    Returns:
        Configured DomainModel for travel booking dialogues
    """
    domain = DomainModel(name="travel_booking")

    # Predicates covering Larsson's travel agency attributes
    domain.add_predicate(
        "transport_mode",
        arity=1,
        arg_types=["transport_means"],
        description="Preferred means of travel (plane/train)",
    )
    domain.add_predicate(
        "depart_city",
        arity=1,
        arg_types=["city"],
        description="City the traveler will depart from",
    )
    domain.add_predicate(
        "dest_city",
        arity=1,
        arg_types=["city"],
        description="Destination city",
    )
    domain.add_predicate(
        "depart_day",
        arity=1,
        arg_types=["travel_day"],
        description="Requested departure day",
    )
    domain.add_predicate(
        "return_day",
        arity=1,
        arg_types=["travel_day"],
        description="Requested return day for round trips",
    )
    domain.add_predicate(
        "travel_class",
        arity=1,
        arg_types=["travel_class"],
        description="Cabin class (economy/business/first)",
    )
    domain.add_predicate(
        "price_quote",
        arity=1,
        arg_types=["price_band"],
        description="Aggregated price quotation for itinerary",
    )
    domain.add_predicate(
        "return_trip",
        arity=0,
        description="Whether traveler needs a return ticket",
    )

    # Sorts that mirror Larsson's example inventory
    domain.add_sort("transport_means", TRANSPORT_MODES)
    domain.add_sort("city", MAJOR_CITIES)
    domain.add_sort("travel_day", TRAVEL_DAYS)
    domain.add_sort("travel_class", TRAVEL_CLASSES)
    domain.add_sort("price_band", ["budget", "standard", "flex"])

    domain.register_plan_builder("travel_booking", _build_travel_plan)
    return domain


def _build_travel_plan(context: dict[str, Any]) -> Plan:
    """Build Larsson-style travel booking plan.

    Collects itinerary slots before the system looks up fares.

    Args:
        context: Optional plan context (supports `include_return` flag)

    Returns:
        Plan with ordered subplans representing the travel dialogue strategy
    """
    include_return: bool = context.get("include_return", True)  # type: ignore[assignment]

    subplans: list[Plan] = [
        Plan(
            plan_type="findout",
            content=WhQuestion(variable="mode", predicate="transport_mode"),
        ),
        Plan(
            plan_type="findout",
            content=WhQuestion(variable="depart_city", predicate="depart_city"),
        ),
        Plan(
            plan_type="findout",
            content=WhQuestion(variable="dest_city", predicate="dest_city"),
        ),
        Plan(
            plan_type="findout",
            content=WhQuestion(variable="depart_day", predicate="depart_day"),
        ),
        Plan(
            plan_type="findout",
            content=WhQuestion(variable="class", predicate="travel_class"),
        ),
    ]

    if include_return:
        subplans.extend(
            [
                Plan(
                    plan_type="findout",
                    content=YNQuestion(proposition="return_trip"),
                ),
                Plan(
                    plan_type="findout",
                    content=WhQuestion(variable="return_day", predicate="return_day"),
                ),
            ]
        )

    subplans.append(
        Plan(
            plan_type="perform",
            content=WhQuestion(variable="price", predicate="price_quote"),
            status="pending",
        )
    )

    return Plan(
        plan_type="travel_booking",
        content="travel_itinerary",
        status="active",
        subplans=subplans,
    )


_travel_domain: DomainModel | None = None


def get_travel_domain() -> DomainModel:
    """Get or create singleton travel domain."""
    global _travel_domain
    if _travel_domain is None:
        _travel_domain = create_travel_domain()
    return _travel_domain
