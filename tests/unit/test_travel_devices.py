"""Unit tests for travel domain mock devices.

Tests FlightBookingDevice, HotelBookingDevice, and CarRentalDevice.
"""

import sys
from pathlib import Path

# Add tests directory to path
tests_dir = Path(__file__).parent.parent
sys.path.insert(0, str(tests_dir))

from mocks.devices.travel_devices import (  # noqa: E402
    CarRentalDevice,
    FlightBookingDevice,
    HotelBookingDevice,
)

from ibdm.core.actions import Action, ActionType  # noqa: E402
from ibdm.core.information_state import InformationState  # noqa: E402
from ibdm.interfaces.device import ActionStatus  # noqa: E402


class TestFlightBookingDevice:
    """Test FlightBookingDevice."""

    def test_initialization(self) -> None:
        """Test device initialization."""
        device = FlightBookingDevice()

        assert device.bookings == {}
        assert device.fail_rate == 0.0
        assert device.request_count == 0

    def test_search_flights_success(self) -> None:
        """Test successful flight search."""
        device = FlightBookingDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.GET,
            name="search_flights",
            parameters={
                "from": "SFO",
                "to": "JFK",
                "date": "2025-06-01",
            },
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert result.status == ActionStatus.SUCCESS
        assert "flights" in result.return_value
        assert len(result.return_value["flights"]) > 0

    def test_search_flights_missing_parameters(self) -> None:
        """Test flight search with missing parameters."""
        device = FlightBookingDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.GET,
            name="search_flights",
            parameters={"from": "SFO"},  # Missing destination and date
        )

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert result.status == ActionStatus.PRECONDITION_FAILED

    def test_book_flight_success(self) -> None:
        """Test successful flight booking."""
        device = FlightBookingDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.BOOK,
            name="book_flight",
            parameters={
                "from": "SFO",
                "to": "JFK",
                "date": "2025-06-01",
                "passengers": 1,
            },
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert "booking_reference" in result.return_value
        assert result.return_value["booking_reference"].startswith("FLT-")
        assert "booked" in result.postconditions[0]

    def test_cancel_flight_success(self) -> None:
        """Test successful flight cancellation."""
        device = FlightBookingDevice()
        state = InformationState()

        # First book a flight
        book_action = Action(
            action_type=ActionType.BOOK,
            name="book_flight",
            parameters={
                "from": "SFO",
                "to": "JFK",
                "date": "2025-06-01",
                "passengers": 1,
            },
        )

        book_result = device.execute_action(book_action, state)
        booking_ref = book_result.return_value["booking_reference"]

        # Now cancel it
        cancel_action = Action(
            action_type=ActionType.CANCEL,
            name="cancel_flight",
            parameters={"booking_reference": booking_ref},
        )

        cancel_result = device.execute_action(cancel_action, state)

        assert cancel_result.is_successful()
        assert "refund_amount" in cancel_result.return_value
        assert cancel_result.return_value["status"] == "cancelled"

    def test_cancel_nonexistent_flight(self) -> None:
        """Test cancelling a non-existent booking."""
        device = FlightBookingDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.CANCEL,
            name="cancel_flight",
            parameters={"booking_reference": "INVALID-123"},
        )

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert result.status == ActionStatus.FAILURE

    def test_rate_limiting(self) -> None:
        """Test rate limiting enforcement."""
        device = FlightBookingDevice()
        device.rate_limit = 5  # Set low limit
        state = InformationState()

        action = Action(
            action_type=ActionType.GET,
            name="search_flights",
            parameters={
                "from": "SFO",
                "to": "JFK",
                "date": "2025-06-01",
            },
        )

        # Make requests up to limit
        for _ in range(5):
            device.execute_action(action, state)

        # Next request should fail
        result = device.execute_action(action, state)
        assert not result.is_successful()
        assert "rate limit" in result.error_message.lower()


class TestHotelBookingDevice:
    """Test HotelBookingDevice."""

    def test_initialization(self) -> None:
        """Test device initialization."""
        device = HotelBookingDevice()

        assert device.reservations == {}
        assert len(device.available_hotels) > 0

    def test_search_hotels_success(self) -> None:
        """Test successful hotel search."""
        device = HotelBookingDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.GET,
            name="search_hotels",
            parameters={
                "city": "New York",
                "check_in": "2025-06-01",
                "check_out": "2025-06-05",
            },
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert "hotels" in result.return_value
        assert len(result.return_value["hotels"]) > 0

        # Verify hotel structure
        hotel = result.return_value["hotels"][0]
        assert "hotel_id" in hotel
        assert "name" in hotel
        assert "price_per_night" in hotel

    def test_book_hotel_success(self) -> None:
        """Test successful hotel booking."""
        device = HotelBookingDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={
                "hotel_id": "H001",
                "check_in": "2025-06-01",
                "check_out": "2025-06-05",
                "guest_name": "Jane Doe",
            },
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert "reservation_code" in result.return_value
        assert result.return_value["reservation_code"].startswith("HTL-")
        assert "total_price" in result.return_value

    def test_cancel_hotel_with_refund(self) -> None:
        """Test hotel cancellation with refund."""
        device = HotelBookingDevice()
        state = InformationState()

        # First book a hotel
        book_action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={
                "hotel_id": "H001",
                "check_in": "2025-06-01",
                "check_out": "2025-06-05",
                "guest_name": "Jane Doe",
            },
        )

        book_result = device.execute_action(book_action, state)
        reservation_code = book_result.return_value["reservation_code"]
        original_price = book_result.return_value["total_price"]

        # Cancel it
        cancel_action = Action(
            action_type=ActionType.CANCEL,
            name="cancel_hotel",
            parameters={"reservation_code": reservation_code},
        )

        cancel_result = device.execute_action(cancel_action, state)

        assert cancel_result.is_successful()
        assert "refund_amount" in cancel_result.return_value

        # Refund should be 90% of original
        expected_refund = original_price * 0.9
        assert abs(cancel_result.return_value["refund_amount"] - expected_refund) < 0.01


class TestCarRentalDevice:
    """Test CarRentalDevice."""

    def test_initialization(self) -> None:
        """Test device initialization."""
        device = CarRentalDevice()

        assert device.rentals == {}
        assert len(device.fleet) > 0

    def test_search_cars_success(self) -> None:
        """Test successful car search."""
        device = CarRentalDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.GET,
            name="search_cars",
            parameters={
                "location": "SFO Airport",
                "pickup_date": "2025-06-01",
                "return_date": "2025-06-05",
            },
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert "cars" in result.return_value
        assert len(result.return_value["cars"]) > 0

    def test_book_car_success(self) -> None:
        """Test successful car booking."""
        device = CarRentalDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.BOOK,
            name="book_car",
            parameters={
                "vehicle_type": "economy",
                "driver_name": "Bob Smith",
                "pickup_date": "2025-06-01",
                "return_date": "2025-06-05",
            },
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert "rental_code" in result.return_value
        assert result.return_value["rental_code"].startswith("CAR-")
        assert "total_cost" in result.return_value

    def test_book_car_with_insurance(self) -> None:
        """Test car booking with insurance."""
        device = CarRentalDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.BOOK,
            name="book_car",
            parameters={
                "vehicle_type": "economy",
                "driver_name": "Bob Smith",
                "pickup_date": "2025-06-01",
                "return_date": "2025-06-05",
                "insurance": True,
            },
        )

        result = device.execute_action(action, state)

        assert result.is_successful()

        # Price should include insurance (15/day)
        total_with_insurance = result.return_value["total_cost"]
        # Base rate for economy is 30/day, insurance is 15/day, so total should be 45/day
        assert total_with_insurance >= 45  # At least 1 day with insurance

    def test_book_unavailable_car(self) -> None:
        """Test booking when no cars available."""
        device = CarRentalDevice()
        state = InformationState()

        # Set all cars to unavailable
        for car in device.fleet.values():
            car["available"] = 0

        action = Action(
            action_type=ActionType.BOOK,
            name="book_car",
            parameters={
                "vehicle_type": "economy",
                "driver_name": "Bob Smith",
                "pickup_date": "2025-06-01",
                "return_date": "2025-06-05",
            },
        )

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert "available" in result.error_message.lower()

    def test_cancel_car_rental(self) -> None:
        """Test car rental cancellation."""
        device = CarRentalDevice()
        state = InformationState()

        # First book a car
        book_action = Action(
            action_type=ActionType.BOOK,
            name="book_car",
            parameters={
                "vehicle_type": "economy",
                "driver_name": "Bob Smith",
                "pickup_date": "2025-06-01",
                "return_date": "2025-06-05",
            },
        )

        book_result = device.execute_action(book_action, state)
        rental_code = book_result.return_value["rental_code"]

        # Cancel it
        cancel_action = Action(
            action_type=ActionType.CANCEL,
            name="cancel_car",
            parameters={"rental_code": rental_code},
        )

        cancel_result = device.execute_action(cancel_action, state)

        assert cancel_result.is_successful()
        assert cancel_result.return_value["status"] == "cancelled"

    def test_preconditions_check(self) -> None:
        """Test precondition checking."""
        device = CarRentalDevice()
        state = InformationState()

        # Missing required parameters
        action = Action(
            action_type=ActionType.BOOK,
            name="book_car",
            parameters={"vehicle_type": "economy"},  # Missing other required params
        )

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert result.status == ActionStatus.PRECONDITION_FAILED
