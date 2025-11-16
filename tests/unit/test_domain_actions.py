"""Unit tests for domain model action postcondition support.

Tests the DomainModel's ability to generate postconditions for actions.
"""

from ibdm.core.actions import Action, ActionType, Proposition
from ibdm.core.domain import DomainModel


class TestDomainPreconditions:
    """Test precondition checking in domain model."""

    def test_register_precond_function(self) -> None:
        """Test registering a precondition function."""
        domain = DomainModel(name="test")

        def book_hotel_precond(action: Action, commitments: set[str]) -> tuple[bool, str]:
            if "check_in_date" not in commitments:
                return (False, "Check-in date required")
            return (True, "")

        domain.register_precond_function("book_hotel", book_hotel_precond)

        # Verify it's registered
        assert domain.has_precond_function("book_hotel")

    def test_check_preconditions_with_registered_function(self) -> None:
        """Test check_preconditions() with a registered function."""
        domain = DomainModel(name="test")

        # Register precondition function
        def book_hotel_precond(action: Action, commitments: set[str]) -> tuple[bool, str]:
            # Check required parameters
            if "hotel_id" not in action.parameters:
                return (False, "Missing hotel_id parameter")

            # Check required commitments
            if "check_in_date" not in commitments and not any(
                c.startswith("check_in_date") for c in commitments
            ):
                return (False, "Check-in date must be known before booking")

            if "check_out_date" not in commitments and not any(
                c.startswith("check_out_date") for c in commitments
            ):
                return (False, "Check-out date must be known before booking")

            return (True, "")

        domain.register_precond_function("book_hotel", book_hotel_precond)

        # Test with satisfied preconditions
        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H123"},
        )

        commitments = {"check_in_date: 2025-01-05", "check_out_date: 2025-01-10"}

        satisfied, error = domain.check_preconditions(action, commitments)

        assert satisfied
        assert error == ""

    def test_check_preconditions_missing_parameter(self) -> None:
        """Test check_preconditions() with missing parameter."""
        domain = DomainModel(name="test")

        def book_hotel_precond(action: Action, commitments: set[str]) -> tuple[bool, str]:
            if "hotel_id" not in action.parameters:
                return (False, "Missing hotel_id parameter")
            return (True, "")

        domain.register_precond_function("book_hotel", book_hotel_precond)

        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={},  # Missing hotel_id
        )

        commitments: set[str] = set()

        satisfied, error = domain.check_preconditions(action, commitments)

        assert not satisfied
        assert "Missing hotel_id parameter" in error

    def test_check_preconditions_missing_commitment(self) -> None:
        """Test check_preconditions() with missing commitment."""
        domain = DomainModel(name="test")

        def book_hotel_precond(action: Action, commitments: set[str]) -> tuple[bool, str]:
            if "check_in_date" not in commitments and not any(
                c.startswith("check_in_date") for c in commitments
            ):
                return (False, "Check-in date must be known")
            return (True, "")

        domain.register_precond_function("book_hotel", book_hotel_precond)

        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H123"},
        )

        commitments: set[str] = set()  # Empty commitments

        satisfied, error = domain.check_preconditions(action, commitments)

        assert not satisfied
        assert "Check-in date must be known" in error

    def test_check_preconditions_with_declared_preconditions(self) -> None:
        """Test check_preconditions() using action's declared preconditions."""
        domain = DomainModel(name="test")

        # No registered function - will use fallback

        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H123"},
            preconditions=["check_in_date", "check_out_date"],
        )

        # Test with all preconditions satisfied
        commitments = {"check_in_date: 2025-01-05", "check_out_date: 2025-01-10"}

        satisfied, error = domain.check_preconditions(action, commitments)

        assert satisfied
        assert error == ""

    def test_check_preconditions_declared_preconditions_missing(self) -> None:
        """Test check_preconditions() with missing declared preconditions."""
        domain = DomainModel(name="test")

        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            preconditions=["check_in_date", "check_out_date", "hotel_selected"],
        )

        # Only partial commitments
        commitments = {"check_in_date: 2025-01-05"}

        satisfied, error = domain.check_preconditions(action, commitments)

        assert not satisfied
        assert "Missing required information" in error
        assert "check_out_date" in error or "hotel_selected" in error

    def test_check_preconditions_exact_match(self) -> None:
        """Test precondition checking with exact match."""
        domain = DomainModel(name="test")

        action = Action(
            action_type=ActionType.EXECUTE,
            name="complete_task",
            preconditions=["task_ready"],
        )

        commitments = {"task_ready"}  # Exact match

        satisfied, _ = domain.check_preconditions(action, commitments)

        assert satisfied

    def test_check_preconditions_prefix_match(self) -> None:
        """Test precondition checking with prefix match."""
        domain = DomainModel(name="test")

        action = Action(
            action_type=ActionType.BOOK,
            name="book_flight",
            preconditions=["departure_city", "destination_city"],
        )

        # Commitments with full values (prefix match)
        commitments = {"departure_city: London", "destination_city: Paris"}

        satisfied, _ = domain.check_preconditions(action, commitments)

        assert satisfied

    def test_check_preconditions_no_preconditions(self) -> None:
        """Test check_preconditions() with action that has no preconditions."""
        domain = DomainModel(name="test")

        action = Action(
            action_type=ActionType.GET,
            name="get_status",
            parameters={},
        )

        commitments: set[str] = set()

        satisfied, error = domain.check_preconditions(action, commitments)

        # No preconditions = always satisfied
        assert satisfied
        assert error == ""

    def test_check_preconditions_registered_function_takes_precedence(self) -> None:
        """Test that registered function takes precedence over declared preconditions."""
        domain = DomainModel(name="test")

        # Register custom precondition function
        def custom_precond(action: Action, commitments: set[str]) -> tuple[bool, str]:
            return (True, "")  # Always satisfied

        domain.register_precond_function("book_hotel", custom_precond)

        # Create action with declared preconditions that would fail
        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            preconditions=["impossible_condition"],
        )

        commitments: set[str] = set()  # Empty commitments

        satisfied, _ = domain.check_preconditions(action, commitments)

        # Should use registered function (always satisfied), not declared preconditions
        assert satisfied

    def test_domain_repr_includes_precond_functions(self) -> None:
        """Test that __repr__ includes precond_functions count."""
        domain = DomainModel(name="test")

        # Initially no precond functions
        repr_str = repr(domain)
        assert "precond_functions=0" in repr_str

        # Add a precond function
        def dummy_precond(action: Action, commitments: set[str]) -> tuple[bool, str]:
            return (True, "")

        domain.register_precond_function("dummy", dummy_precond)

        # Should now show 1
        repr_str = repr(domain)
        assert "precond_functions=1" in repr_str


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
