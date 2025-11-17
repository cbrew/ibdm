"""Travel booking domain model inspired by Larsson (2002).

This mirrors the classic travel agency scenarios used in the IBiS / TRINDI
work, providing predicates, sorts, and dialogue plans for collecting itinerary
constraints before consulting a database.
"""

from typing import Any

from ibdm.core.actions import Action, Proposition
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

    # Add dependencies for IBiS3 Rule 4.8 (DependentQuestionReaccommodation)
    # Price depends on travel class and transport mode
    domain.add_dependency("price_quote", ["travel_class", "transport_mode"])

    domain.register_plan_builder("travel_booking", _build_travel_plan)

    # Register action precondition functions (IBiS4)
    domain.register_precond_function("book_flight", _check_book_flight_precond)
    domain.register_precond_function("book_hotel", _check_book_hotel_precond)
    domain.register_precond_function("reserve_car", _check_reserve_car_precond)

    # Register action postcondition functions (IBiS4)
    domain.register_postcond_function("book_flight", _book_flight_postcond)
    domain.register_postcond_function("book_hotel", _book_hotel_postcond)
    domain.register_postcond_function("reserve_car", _reserve_car_postcond)

    # Register dominance functions for negotiation (IBiS4)
    domain.register_dominance_function("hotel", _hotel_price_dominance)
    domain.register_dominance_function("flight", _flight_price_dominance)

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


# ============================================================================
# IBiS4 Action Precondition Functions
# ============================================================================


def _check_book_flight_precond(action: Action, commitments: set[str]) -> tuple[bool, str]:
    """Check preconditions for booking a flight.

    Requires:
    - Departure city
    - Destination city
    - Departure date
    - Travel class (optional, defaults to economy)

    Args:
        action: book_flight action
        commitments: Current commitments

    Returns:
        Tuple of (satisfied, error_message)
    """
    required_fields = ["depart_city", "dest_city", "depart_day"]

    missing_fields = []
    for field in required_fields:
        if not any(field in commit for commit in commitments):
            missing_fields.append(field)

    if missing_fields:
        return (False, f"Missing required information: {', '.join(missing_fields)}")

    return (True, "")


def _check_book_hotel_precond(action: Action, commitments: set[str]) -> tuple[bool, str]:
    """Check preconditions for booking a hotel.

    Requires:
    - Destination city
    - Check-in date
    - Check-out date

    Args:
        action: book_hotel action
        commitments: Current commitments

    Returns:
        Tuple of (satisfied, error_message)
    """
    # Check for required parameters in the action itself
    required_params = ["city", "check_in", "check_out"]

    missing_params = []
    for param in required_params:
        if param not in action.parameters:
            missing_params.append(param)

    if missing_params:
        return (
            False,
            f"Missing required parameters: {', '.join(missing_params)}",
        )

    return (True, "")


def _check_reserve_car_precond(action: Action, commitments: set[str]) -> tuple[bool, str]:
    """Check preconditions for reserving a car.

    Requires:
    - Pickup location
    - Pickup date
    - Return date

    Args:
        action: reserve_car action
        commitments: Current commitments

    Returns:
        Tuple of (satisfied, error_message)
    """
    required_params = ["pickup_location", "pickup_date", "return_date"]

    missing_params = []
    for param in required_params:
        if param not in action.parameters:
            missing_params.append(param)

    if missing_params:
        return (
            False,
            f"Missing required parameters: {', '.join(missing_params)}",
        )

    return (True, "")


# ============================================================================
# IBiS4 Action Postcondition Functions
# ============================================================================


def _book_flight_postcond(action: Action) -> list[Proposition]:
    """Generate postconditions for flight booking.

    Creates propositions indicating:
    - Flight booked
    - Confirmation number assigned
    - Booking details recorded

    Args:
        action: book_flight action

    Returns:
        List of postcondition propositions
    """
    confirmation_number = action.parameters.get("confirmation_number", "FL123456")
    depart_city = action.parameters.get("depart_city", "unknown")
    dest_city = action.parameters.get("dest_city", "unknown")
    depart_day = action.parameters.get("depart_day", "unknown")

    return [
        Proposition(
            predicate="flight_booked",
            arguments={
                "confirmation": confirmation_number,
                "from": depart_city,
                "to": dest_city,
                "date": depart_day,
            },
        ),
    ]


def _book_hotel_postcond(action: Action) -> list[Proposition]:
    """Generate postconditions for hotel booking.

    Creates propositions indicating:
    - Hotel booked
    - Reservation confirmed

    Args:
        action: book_hotel action

    Returns:
        List of postcondition propositions
    """
    hotel_id = action.parameters.get("hotel_id", "HOTEL_001")
    check_in = action.parameters.get("check_in", "2025-01-05")
    check_out = action.parameters.get("check_out", "2025-01-10")

    return [
        Proposition(
            predicate="hotel_booked",
            arguments={
                "hotel_id": hotel_id,
                "check_in": check_in,
                "check_out": check_out,
            },
        ),
    ]


def _reserve_car_postcond(action: Action) -> list[Proposition]:
    """Generate postconditions for car reservation.

    Creates propositions indicating:
    - Car reserved
    - Pickup details confirmed

    Args:
        action: reserve_car action

    Returns:
        List of postcondition propositions
    """
    confirmation = action.parameters.get("confirmation", "CAR123456")
    pickup_location = action.parameters.get("pickup_location", "airport")
    pickup_date = action.parameters.get("pickup_date", "2025-01-05")

    return [
        Proposition(
            predicate="car_reserved",
            arguments={
                "confirmation": confirmation,
                "pickup_location": pickup_location,
                "pickup_date": pickup_date,
            },
        ),
    ]


# ============================================================================
# IBiS4 Dominance Functions for Negotiation
# ============================================================================


def _hotel_price_dominance(prop1: Proposition, prop2: Proposition) -> bool:
    """Check if hotel1 dominates hotel2 by price.

    Lower price dominates higher price (all else being equal).

    Args:
        prop1: First hotel proposition
        prop2: Second hotel proposition

    Returns:
        True if prop1 has lower price than prop2
    """
    try:
        price1 = float(prop1.arguments.get("price", float("inf")))
        price2 = float(prop2.arguments.get("price", float("inf")))
        return price1 < price2
    except (ValueError, TypeError):
        return False


def _flight_price_dominance(prop1: Proposition, prop2: Proposition) -> bool:
    """Check if flight1 dominates flight2 by price.

    Lower price dominates higher price (all else being equal).

    Args:
        prop1: First flight proposition
        prop2: Second flight proposition

    Returns:
        True if prop1 has lower price than prop2
    """
    try:
        price1 = float(prop1.arguments.get("price", float("inf")))
        price2 = float(prop2.arguments.get("price", float("inf")))
        return price1 < price2
    except (ValueError, TypeError):
        return False


# ============================================================================
# Domain Singleton
# ============================================================================


_travel_domain: DomainModel | None = None


def get_travel_domain() -> DomainModel:
    """Get or create singleton travel domain."""
    global _travel_domain
    if _travel_domain is None:
        _travel_domain = create_travel_domain()
    return _travel_domain
