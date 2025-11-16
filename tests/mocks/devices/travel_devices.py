"""Mock travel booking devices (Flight, Hotel, Car Rental APIs).

Simulates realistic web API behavior for travel booking services.
"""

import random
from typing import Any

from ibdm.core.actions import Action
from ibdm.core.information_state import InformationState
from ibdm.interfaces.device import ActionResult, ActionStatus, DeviceInterface


class FlightBookingDevice(DeviceInterface):
    """Mock flight booking API (e.g., Amadeus, Sabre, Skyscanner).

    Simulates a flight booking web service with realistic behavior:
    - Search for flights between cities
    - Book flights with passenger details
    - Cancel bookings
    - Handle rate limits, sold out flights, invalid dates

    Example:
        >>> device = FlightBookingDevice()
        >>> action = Action(
        ...     action_type=ActionType.BOOK,
        ...     name="book_flight",
        ...     parameters={
        ...         "from": "London",
        ...         "to": "Paris",
        ...         "date": "2025-01-15",
        ...         "passengers": 2
        ...     }
        ... )
        >>> result = device.execute_action(action, state)
        >>> result.is_successful()  # True
        >>> result.return_value["booking_reference"]  # "FLT-ABC123"
    """

    def __init__(self, fail_rate: float = 0.0):
        """Initialize flight booking device.

        Args:
            fail_rate: Probability of booking failure (0.0 to 1.0)
        """
        self.bookings: dict[str, Any] = {}  # booking_ref -> booking details
        self.fail_rate = fail_rate
        self.request_count = 0
        self.rate_limit = 100  # requests per session

    def execute_action(self, action: Action, state: InformationState) -> ActionResult:
        """Execute flight booking action."""
        self.request_count += 1

        # Check rate limit
        if self.request_count > self.rate_limit:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Rate limit exceeded ({self.rate_limit} requests)",
                metadata={"rate_limit_reset": "3600s"},
            )

        # Check preconditions
        if not self.check_preconditions(action, state):
            return ActionResult(
                status=ActionStatus.PRECONDITION_FAILED,
                action=action,
                error_message="Missing required flight booking information",
            )

        # Route to specific action handler
        if action.name == "search_flights":
            return self._search_flights(action)
        elif action.name == "book_flight":
            return self._book_flight(action)
        elif action.name == "cancel_flight":
            return self._cancel_flight(action)
        else:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Unknown flight action: {action.name}",
            )

    def _search_flights(self, action: Action) -> ActionResult:
        """Search for available flights."""
        origin = action.parameters.get("from", "")
        destination = action.parameters.get("to", "")
        date = action.parameters.get("date", "")

        # Simulate search results
        flights = [
            {
                "flight_id": f"FL{random.randint(100, 999)}",
                "from": origin,
                "to": destination,
                "date": date,
                "price": random.randint(50, 500),
                "airline": random.choice(["BA", "AF", "LH", "KL"]),
                "duration": f"{random.randint(1, 8)}h {random.randint(0, 59)}m",
            }
            for _ in range(random.randint(3, 10))
        ]

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={"flights": flights, "count": len(flights)},
            postconditions=[f"searched_flights(from={origin}, to={destination}, date={date})"],
        )

    def _book_flight(self, action: Action) -> ActionResult:
        """Book a flight."""
        # Simulate random booking failure
        if random.random() < self.fail_rate:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message="Flight sold out or booking system unavailable",
            )

        # Generate booking reference
        booking_ref = f"FLT-{random.randint(100000, 999999)}"

        # Store booking
        self.bookings[booking_ref] = {
            "from": action.parameters.get("from"),
            "to": action.parameters.get("to"),
            "date": action.parameters.get("date"),
            "passengers": action.parameters.get("passengers", 1),
            "price": action.parameters.get("price", 100),
            "status": "confirmed",
        }

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "booking_reference": booking_ref,
                "status": "confirmed",
                "confirmation_email": "sent",
            },
            postconditions=[f"booked_flight(ref={booking_ref})"],
        )

    def _cancel_flight(self, action: Action) -> ActionResult:
        """Cancel a flight booking."""
        booking_ref = action.parameters.get("booking_reference", "")

        if booking_ref not in self.bookings:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Booking {booking_ref} not found",
            )

        # Update booking status
        self.bookings[booking_ref]["status"] = "cancelled"

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "booking_reference": booking_ref,
                "status": "cancelled",
                "refund_amount": self.bookings[booking_ref]["price"],
            },
            postconditions=[f"cancelled_flight(ref={booking_ref})"],
        )

    def check_preconditions(self, action: Action, state: InformationState) -> bool:
        """Check flight booking preconditions."""
        if action.name == "search_flights":
            required = ["from", "to", "date"]
        elif action.name == "book_flight":
            required = ["from", "to", "date", "passengers"]
        elif action.name == "cancel_flight":
            required = ["booking_reference"]
        else:
            return False

        return all(param in action.parameters for param in required)

    def get_postconditions(self, action: Action) -> list[str]:
        """Get flight booking postconditions."""
        if action.name == "book_flight":
            return ["booked_flight(confirmed=true)"]
        elif action.name == "cancel_flight":
            return ["cancelled_flight(refunded=true)"]
        elif action.name == "search_flights":
            return ["searched_flights(results_available=true)"]
        return []


class HotelBookingDevice(DeviceInterface):
    """Mock hotel booking API (e.g., Booking.com, Expedia, Hotels.com).

    Simulates a hotel booking web service with realistic behavior:
    - Search for hotels in a city
    - Book rooms with guest details
    - Modify/cancel reservations
    - Handle availability, pricing, special requests
    """

    def __init__(self, fail_rate: float = 0.0):
        """Initialize hotel booking device.

        Args:
            fail_rate: Probability of booking failure (0.0 to 1.0)
        """
        self.reservations: dict[str, Any] = {}
        self.fail_rate = fail_rate
        self.available_hotels = {
            "H001": {"name": "Grand Hotel", "stars": 5, "price_per_night": 200},
            "H002": {"name": "City Inn", "stars": 3, "price_per_night": 80},
            "H003": {"name": "Airport Lodge", "stars": 2, "price_per_night": 50},
        }

    def execute_action(self, action: Action, state: InformationState) -> ActionResult:
        """Execute hotel booking action."""
        if not self.check_preconditions(action, state):
            return ActionResult(
                status=ActionStatus.PRECONDITION_FAILED,
                action=action,
                error_message="Missing required hotel booking information",
            )

        if action.name == "search_hotels":
            return self._search_hotels(action)
        elif action.name == "book_hotel":
            return self._book_hotel(action)
        elif action.name == "cancel_hotel":
            return self._cancel_hotel(action)
        else:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Unknown hotel action: {action.name}",
            )

    def _search_hotels(self, action: Action) -> ActionResult:
        """Search for available hotels."""
        city = action.parameters.get("city", "")

        # Return available hotels
        hotels = [
            {
                "hotel_id": hotel_id,
                **details,
                "city": city,
                "available": True,
            }
            for hotel_id, details in self.available_hotels.items()
        ]

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={"hotels": hotels, "count": len(hotels)},
            postconditions=[f"searched_hotels(city={city}, results={len(hotels)})"],
        )

    def _book_hotel(self, action: Action) -> ActionResult:
        """Book a hotel room."""
        # Simulate random booking failure
        if random.random() < self.fail_rate:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message="No rooms available or booking system error",
            )

        # Generate reservation code
        reservation_code = f"HTL-{random.randint(100000, 999999)}"

        # Calculate total price
        hotel_id = action.parameters.get("hotel_id", "H001")
        nights = action.parameters.get("nights", 1)
        price_per_night = self.available_hotels.get(hotel_id, {}).get("price_per_night", 100)
        total_price = price_per_night * nights

        # Store reservation
        self.reservations[reservation_code] = {
            "hotel_id": hotel_id,
            "guest_name": action.parameters.get("guest_name"),
            "check_in": action.parameters.get("check_in"),
            "check_out": action.parameters.get("check_out"),
            "nights": nights,
            "total_price": total_price,
            "status": "confirmed",
        }

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "reservation_code": reservation_code,
                "hotel_id": hotel_id,
                "total_price": total_price,
                "status": "confirmed",
            },
            postconditions=[f"booked_hotel(ref={reservation_code})"],
        )

    def _cancel_hotel(self, action: Action) -> ActionResult:
        """Cancel a hotel reservation."""
        reservation_code = action.parameters.get("reservation_code", "")

        if reservation_code not in self.reservations:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Reservation {reservation_code} not found",
            )

        # Cancel and calculate refund (90% refund policy)
        reservation = self.reservations[reservation_code]
        reservation["status"] = "cancelled"
        refund = int(reservation["total_price"] * 0.9)

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "reservation_code": reservation_code,
                "status": "cancelled",
                "refund_amount": refund,
            },
            postconditions=[f"cancelled_hotel(ref={reservation_code})"],
        )

    def check_preconditions(self, action: Action, state: InformationState) -> bool:
        """Check hotel booking preconditions."""
        if action.name == "search_hotels":
            required = ["city", "check_in", "check_out"]
        elif action.name == "book_hotel":
            required = ["hotel_id", "guest_name", "check_in", "check_out"]
        elif action.name == "cancel_hotel":
            required = ["reservation_code"]
        else:
            return False

        return all(param in action.parameters for param in required)

    def get_postconditions(self, action: Action) -> list[str]:
        """Get hotel booking postconditions."""
        if action.name == "book_hotel":
            return ["booked_hotel(confirmed=true)"]
        elif action.name == "cancel_hotel":
            return ["cancelled_hotel(refunded=true)"]
        elif action.name == "search_hotels":
            return ["searched_hotels(results_available=true)"]
        return []


class CarRentalDevice(DeviceInterface):
    """Mock car rental API (e.g., Hertz, Enterprise, Avis).

    Simulates a car rental web service with realistic behavior:
    - Search for available vehicles
    - Book rental cars with driver details
    - Modify/cancel reservations
    - Handle vehicle types, insurance, mileage
    """

    def __init__(self, fail_rate: float = 0.0):
        """Initialize car rental device.

        Args:
            fail_rate: Probability of booking failure (0.0 to 1.0)
        """
        self.rentals: dict[str, Any] = {}
        self.fail_rate = fail_rate
        self.fleet = {
            "economy": {"daily_rate": 30, "available": 10},
            "compact": {"daily_rate": 40, "available": 8},
            "suv": {"daily_rate": 70, "available": 5},
            "luxury": {"daily_rate": 150, "available": 2},
        }

    def execute_action(self, action: Action, state: InformationState) -> ActionResult:
        """Execute car rental action."""
        if not self.check_preconditions(action, state):
            return ActionResult(
                status=ActionStatus.PRECONDITION_FAILED,
                action=action,
                error_message="Missing required car rental information",
            )

        if action.name == "search_cars":
            return self._search_cars(action)
        elif action.name == "book_car":
            return self._book_car(action)
        elif action.name == "cancel_car":
            return self._cancel_car(action)
        else:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Unknown car rental action: {action.name}",
            )

    def _search_cars(self, action: Action) -> ActionResult:
        """Search for available rental cars."""
        location = action.parameters.get("location", "")

        # Return available vehicles
        available_cars = [
            {
                "vehicle_type": vehicle_type,
                "daily_rate": details["daily_rate"],
                "available_count": details["available"],
            }
            for vehicle_type, details in self.fleet.items()
            if details["available"] > 0
        ]

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={"cars": available_cars, "location": location},
            postconditions=[f"searched_cars(location={location}, results={len(available_cars)})"],
        )

    def _book_car(self, action: Action) -> ActionResult:
        """Book a rental car."""
        vehicle_type = action.parameters.get("vehicle_type", "economy")

        # Check availability
        if vehicle_type not in self.fleet or self.fleet[vehicle_type]["available"] == 0:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"No {vehicle_type} vehicles available",
            )

        # Simulate random booking failure
        if random.random() < self.fail_rate:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message="Booking system unavailable",
            )

        # Generate rental code
        rental_code = f"CAR-{random.randint(100000, 999999)}"

        # Calculate total cost
        days = action.parameters.get("days", 1)
        daily_rate = self.fleet[vehicle_type]["daily_rate"]
        insurance = action.parameters.get("insurance", False)
        insurance_cost = 15 * days if insurance else 0
        total_cost = (daily_rate * days) + insurance_cost

        # Update availability
        self.fleet[vehicle_type]["available"] -= 1

        # Store rental
        self.rentals[rental_code] = {
            "vehicle_type": vehicle_type,
            "driver_name": action.parameters.get("driver_name"),
            "pickup_date": action.parameters.get("pickup_date"),
            "return_date": action.parameters.get("return_date"),
            "days": days,
            "total_cost": total_cost,
            "status": "confirmed",
        }

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "rental_code": rental_code,
                "vehicle_type": vehicle_type,
                "total_cost": total_cost,
                "status": "confirmed",
            },
            postconditions=[f"booked_car(ref={rental_code})"],
        )

    def _cancel_car(self, action: Action) -> ActionResult:
        """Cancel a car rental."""
        rental_code = action.parameters.get("rental_code", "")

        if rental_code not in self.rentals:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Rental {rental_code} not found",
            )

        # Restore availability
        rental = self.rentals[rental_code]
        vehicle_type = rental["vehicle_type"]
        self.fleet[vehicle_type]["available"] += 1

        # Cancel and calculate refund (full refund if >24h notice)
        rental["status"] = "cancelled"
        refund = rental["total_cost"]

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "rental_code": rental_code,
                "status": "cancelled",
                "refund_amount": refund,
            },
            postconditions=[f"cancelled_car(ref={rental_code})"],
        )

    def check_preconditions(self, action: Action, state: InformationState) -> bool:
        """Check car rental preconditions."""
        if action.name == "search_cars":
            required = ["location", "pickup_date", "return_date"]
        elif action.name == "book_car":
            required = ["vehicle_type", "driver_name", "pickup_date", "return_date"]
        elif action.name == "cancel_car":
            required = ["rental_code"]
        else:
            return False

        return all(param in action.parameters for param in required)

    def get_postconditions(self, action: Action) -> list[str]:
        """Get car rental postconditions."""
        if action.name == "book_car":
            return ["booked_car(confirmed=true)"]
        elif action.name == "cancel_car":
            return ["cancelled_car(refunded=true)"]
        elif action.name == "search_cars":
            return ["searched_cars(results_available=true)"]
        return []
