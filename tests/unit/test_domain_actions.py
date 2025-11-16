"""Unit tests for domain model action postcondition support.

Tests the DomainModel's ability to generate postconditions for actions.
"""

from ibdm.core.actions import Action, ActionType, Proposition
from ibdm.core.domain import DomainModel


class TestDomainPostconditions:
    """Test postcondition generation in domain model."""

    def test_register_postcond_function(self) -> None:
        """Test registering a postcondition function."""
        domain = DomainModel(name="test")

        def book_hotel_postconds(action: Action) -> list[Proposition]:
            hotel_id = action.parameters.get("hotel_id", "unknown")
            return [
                Proposition(
                    predicate="booked",
                    arguments={"hotel_id": hotel_id},
                )
            ]

        domain.register_postcond_function("book_hotel", book_hotel_postconds)

        # Verify it's registered
        assert domain.has_postcond_function("book_hotel")

    def test_postcond_with_registered_function(self) -> None:
        """Test postcond() with a registered function."""
        domain = DomainModel(name="test")

        # Register postcondition function
        def book_hotel_postconds(action: Action) -> list[Proposition]:
            hotel_id = action.parameters.get("hotel_id", "unknown")
            check_in = action.parameters.get("check_in", "unknown")
            return [
                Proposition(
                    predicate="booked",
                    arguments={"hotel_id": hotel_id},
                ),
                Proposition(
                    predicate="check_in_date",
                    arguments={"date": check_in},
                ),
            ]

        domain.register_postcond_function("book_hotel", book_hotel_postconds)

        # Create action
        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H123", "check_in": "2025-01-05"},
        )

        # Get postconditions
        postconds = domain.postcond(action)

        assert len(postconds) == 2
        assert postconds[0].predicate == "booked"
        assert postconds[0].arguments["hotel_id"] == "H123"
        assert postconds[1].predicate == "check_in_date"
        assert postconds[1].arguments["date"] == "2025-01-05"

    def test_postcond_with_declared_postconditions(self) -> None:
        """Test postcond() using action's declared postconditions."""
        domain = DomainModel(name="test")

        # Create action with declared postconditions
        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H123"},
            postconditions=["booked(hotel_id=H123)", "confirmed(status=true)"],
        )

        # Get postconditions (fallback to parsing declared postconditions)
        postconds = domain.postcond(action)

        assert len(postconds) == 2
        assert postconds[0].predicate == "booked"
        assert postconds[0].arguments["hotel_id"] == "H123"
        assert postconds[1].predicate == "confirmed"
        assert postconds[1].arguments["status"] == "true"

    def test_postcond_no_postconditions(self) -> None:
        """Test postcond() with action that has no postconditions."""
        domain = DomainModel(name="test")

        action = Action(
            action_type=ActionType.GET,
            name="get_status",
            parameters={},
        )

        postconds = domain.postcond(action)

        # Should return empty list
        assert postconds == []

    def test_postcond_registered_function_takes_precedence(self) -> None:
        """Test that registered function takes precedence over declared postconditions."""
        domain = DomainModel(name="test")

        # Register postcondition function
        def custom_postconds(action: Action) -> list[Proposition]:
            return [
                Proposition(
                    predicate="custom",
                    arguments={"value": "from_function"},
                )
            ]

        domain.register_postcond_function("book_hotel", custom_postconds)

        # Create action with declared postconditions
        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            postconditions=["declared(value=from_action)"],
        )

        postconds = domain.postcond(action)

        # Should use registered function, not declared postconditions
        assert len(postconds) == 1
        assert postconds[0].predicate == "custom"
        assert postconds[0].arguments["value"] == "from_function"

    def test_parse_postconditions_simple_predicate(self) -> None:
        """Test parsing simple postcondition (no arguments)."""
        domain = DomainModel(name="test")

        action = Action(
            action_type=ActionType.EXECUTE,
            name="complete_task",
            postconditions=["completed"],
        )

        postconds = domain.postcond(action)

        assert len(postconds) == 1
        assert postconds[0].predicate == "completed"
        assert postconds[0].arguments == {}

    def test_parse_postconditions_multiple_arguments(self) -> None:
        """Test parsing postcondition with multiple arguments."""
        domain = DomainModel(name="test")

        action = Action(
            action_type=ActionType.BOOK,
            name="book_flight",
            postconditions=["booked(from=London, to=Paris, date=2025-01-10)"],
        )

        postconds = domain.postcond(action)

        assert len(postconds) == 1
        assert postconds[0].predicate == "booked"
        assert postconds[0].arguments["from"] == "London"
        assert postconds[0].arguments["to"] == "Paris"
        assert postconds[0].arguments["date"] == "2025-01-10"

    def test_parse_postconditions_empty_arguments(self) -> None:
        """Test parsing postcondition with empty argument list."""
        domain = DomainModel(name="test")

        action = Action(
            action_type=ActionType.EXECUTE,
            name="initialize",
            postconditions=["initialized()"],
        )

        postconds = domain.postcond(action)

        assert len(postconds) == 1
        assert postconds[0].predicate == "initialized"
        assert postconds[0].arguments == {}

    def test_domain_repr_includes_postcond_functions(self) -> None:
        """Test that __repr__ includes postcond_functions count."""
        domain = DomainModel(name="test")

        # Initially no postcond functions
        repr_str = repr(domain)
        assert "postcond_functions=0" in repr_str

        # Add a postcond function
        def dummy_postconds(action: Action) -> list[Proposition]:
            return []

        domain.register_postcond_function("dummy", dummy_postconds)

        # Should now show 1
        repr_str = repr(domain)
        assert "postcond_functions=1" in repr_str


class TestPostconditionIntegration:
    """Integration tests for postcondition functionality."""

    def test_hotel_booking_postconditions(self) -> None:
        """Test realistic hotel booking postconditions."""
        domain = DomainModel(name="travel")

        # Register hotel booking postconditions
        def book_hotel_postconds(action: Action) -> list[Proposition]:
            hotel_id = action.parameters.get("hotel_id")
            check_in = action.parameters.get("check_in")
            check_out = action.parameters.get("check_out")
            guest_name = action.parameters.get("guest_name")

            postconds: list[Proposition] = []

            if hotel_id:
                postconds.append(
                    Proposition(
                        predicate="hotel_booked",
                        arguments={"hotel_id": hotel_id},
                    )
                )

            if check_in and check_out:
                postconds.append(
                    Proposition(
                        predicate="reservation_dates",
                        arguments={"check_in": check_in, "check_out": check_out},
                    )
                )

            if guest_name:
                postconds.append(
                    Proposition(
                        predicate="guest_registered",
                        arguments={"name": guest_name},
                    )
                )

            return postconds

        domain.register_postcond_function("book_hotel", book_hotel_postconds)

        # Create complete booking action
        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={
                "hotel_id": "H456",
                "check_in": "2025-02-01",
                "check_out": "2025-02-05",
                "guest_name": "John Doe",
            },
        )

        postconds = domain.postcond(action)

        # Verify all postconditions generated
        assert len(postconds) == 3

        # Check predicates
        predicates = {p.predicate for p in postconds}
        assert "hotel_booked" in predicates
        assert "reservation_dates" in predicates
        assert "guest_registered" in predicates

    def test_nda_generation_postconditions(self) -> None:
        """Test NDA document generation postconditions."""
        domain = DomainModel(name="nda")

        # Register NDA generation postconditions
        def generate_nda_postconds(action: Action) -> list[Proposition]:
            parties = action.parameters.get("parties")
            effective_date = action.parameters.get("effective_date")

            return [
                Proposition(
                    predicate="nda_generated",
                    arguments={"parties": str(parties), "date": str(effective_date)},
                ),
                Proposition(predicate="document_ready", arguments={}),
            ]

        domain.register_postcond_function("generate_nda", generate_nda_postconds)

        # Create NDA generation action
        action = Action(
            action_type=ActionType.GENERATE,
            name="generate_nda",
            parameters={
                "parties": ["Acme Corp", "Smith Inc"],
                "effective_date": "2025-01-01",
            },
        )

        postconds = domain.postcond(action)

        assert len(postconds) == 2
        assert postconds[0].predicate == "nda_generated"
        assert postconds[1].predicate == "document_ready"
