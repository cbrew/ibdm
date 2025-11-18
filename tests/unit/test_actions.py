"""Tests for Action and Proposition classes (IBiS-4).

Based on Larsson (2002) Chapter 5: Action-Oriented and Negotiative Dialogue.
"""

from ibdm.core.actions import Action, ActionType, Proposition, dominates


class TestActionType:
    """Tests for ActionType enum."""

    def test_action_types_exist(self):
        """Test that all action types are defined."""
        assert ActionType.BOOK.value == "book"
        assert ActionType.CANCEL.value == "cancel"
        assert ActionType.SET.value == "set"
        assert ActionType.GET.value == "get"
        assert ActionType.EXECUTE.value == "execute"
        assert ActionType.CONFIRM.value == "confirm"
        assert ActionType.GENERATE.value == "generate"
        assert ActionType.SEND.value == "send"


class TestAction:
    """Tests for Action dataclass."""

    def test_action_creation_minimal(self):
        """Test creating an action with minimal parameters."""
        action = Action(action_type=ActionType.BOOK, name="book_hotel")

        assert action.action_type == ActionType.BOOK
        assert action.name == "book_hotel"
        assert action.parameters == {}
        assert action.preconditions == []
        assert action.postconditions == []
        assert action.requires_confirmation is True
        assert action.metadata == {}

    def test_action_creation_full(self):
        """Test creating an action with all parameters."""
        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H123", "check_in": "2025-01-05"},
            preconditions=["check_in_date_known", "check_out_date_known"],
            postconditions=["booked(hotel_id=H123)"],
            requires_confirmation=True,
            metadata={"confidence": 0.9},
        )

        assert action.action_type == ActionType.BOOK
        assert action.name == "book_hotel"
        assert action.parameters["hotel_id"] == "H123"
        assert len(action.preconditions) == 2
        assert len(action.postconditions) == 1
        assert action.requires_confirmation is True
        assert action.metadata["confidence"] == 0.9

    def test_action_serialization(self):
        """Test action to_dict and from_dict round-trip."""
        original = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H123", "nights": 3},
            preconditions=["dates_known"],
            postconditions=["booked(H123)"],
            requires_confirmation=False,
            metadata={"priority": "high"},
        )

        # Serialize
        data = original.to_dict()

        # Verify serialized data
        assert data["action_type"] == "book"
        assert data["name"] == "book_hotel"
        assert data["parameters"]["hotel_id"] == "H123"
        assert "dates_known" in data["preconditions"]
        assert data["requires_confirmation"] is False

        # Deserialize
        restored = Action.from_dict(data)

        # Verify restoration
        assert restored.action_type == original.action_type
        assert restored.name == original.name
        assert restored.parameters == original.parameters
        assert restored.preconditions == original.preconditions
        assert restored.postconditions == original.postconditions
        assert restored.requires_confirmation == original.requires_confirmation
        assert restored.metadata == original.metadata

    def test_action_string_representation(self):
        """Test action string representation."""
        action = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H123"},
            requires_confirmation=True,
        )

        action_str = str(action)
        assert "book" in action_str
        assert "book_hotel" in action_str
        assert "hotel_id=H123" in action_str
        assert "needs confirmation" in action_str

    def test_action_equality(self):
        """Test action equality comparison."""
        action1 = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H123"},
        )
        action2 = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H123"},
        )
        action3 = Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={"hotel_id": "H456"},
        )

        assert action1 == action2
        assert action1 != action3

    def test_action_hashable(self):
        """Test that actions can be used in sets and dicts."""
        action1 = Action(action_type=ActionType.BOOK, name="book_hotel")
        action2 = Action(action_type=ActionType.CANCEL, name="cancel_booking")

        action_set = {action1, action2}
        assert len(action_set) == 2
        assert action1 in action_set

        action_dict = {action1: "booking", action2: "cancellation"}
        assert action_dict[action1] == "booking"


class TestProposition:
    """Tests for Proposition dataclass."""

    def test_proposition_creation_minimal(self):
        """Test creating a proposition with minimal parameters."""
        prop = Proposition(predicate="hotel")

        assert prop.predicate == "hotel"
        assert prop.arguments == {}
        assert prop.polarity is True
        assert prop.confidence == 1.0
        assert prop.metadata == {}

    def test_proposition_creation_full(self):
        """Test creating a proposition with all parameters."""
        prop = Proposition(
            predicate="hotel",
            arguments={"name": "Hotel A", "price": 180, "location": "Paris"},
            polarity=True,
            confidence=0.85,
            metadata={"source": "booking_api"},
        )

        assert prop.predicate == "hotel"
        assert prop.arguments["name"] == "Hotel A"
        assert prop.arguments["price"] == 180
        assert prop.polarity is True
        assert prop.confidence == 0.85
        assert prop.metadata["source"] == "booking_api"

    def test_proposition_serialization(self):
        """Test proposition to_dict and from_dict round-trip."""
        original = Proposition(
            predicate="hotel",
            arguments={"name": "Hotel B", "price": 150},
            polarity=True,
            confidence=0.9,
            metadata={"rating": 4.5},
        )

        # Serialize
        data = original.to_dict()

        # Verify serialized data
        assert data["predicate"] == "hotel"
        assert data["arguments"]["name"] == "Hotel B"
        assert data["polarity"] is True
        assert data["confidence"] == 0.9

        # Deserialize
        restored = Proposition.from_dict(data)

        # Verify restoration
        assert restored.predicate == original.predicate
        assert restored.arguments == original.arguments
        assert restored.polarity == original.polarity
        assert restored.confidence == original.confidence
        assert restored.metadata == original.metadata

    def test_proposition_string_representation(self):
        """Test proposition string representation."""
        prop = Proposition(predicate="hotel", arguments={"name": "Hotel A", "price": 180})

        prop_str = str(prop)
        assert "hotel" in prop_str
        assert "name=Hotel A" in prop_str
        assert "price=180" in prop_str

    def test_proposition_negative_polarity(self):
        """Test negative proposition representation."""
        prop = Proposition(predicate="available", polarity=False)

        prop_str = str(prop)
        assert "¬" in prop_str  # Negation symbol
        assert "available" in prop_str

    def test_proposition_equality(self):
        """Test proposition equality comparison."""
        prop1 = Proposition(predicate="hotel", arguments={"price": 150})
        prop2 = Proposition(predicate="hotel", arguments={"price": 150})
        prop3 = Proposition(predicate="hotel", arguments={"price": 180})

        assert prop1 == prop2
        assert prop1 != prop3

    def test_proposition_hashable(self):
        """Test that propositions can be used in sets (for IUN)."""
        prop1 = Proposition(predicate="hotel", arguments={"name": "Hotel A"})
        prop2 = Proposition(predicate="hotel", arguments={"name": "Hotel B"})

        iun = {prop1, prop2}
        assert len(iun) == 2
        assert prop1 in iun


class TestDominance:
    """Tests for dominance relation."""

    def test_dominance_by_price(self):
        """Test that lower price dominates higher price."""
        cheap = Proposition(predicate="hotel", arguments={"price": 150})
        expensive = Proposition(predicate="hotel", arguments={"price": 180})

        assert dominates(cheap, expensive) is True
        assert dominates(expensive, cheap) is False

    def test_dominance_by_rating(self):
        """Test that higher rating dominates lower rating."""
        high_rated = Proposition(predicate="hotel", arguments={"rating": 4.5})
        low_rated = Proposition(predicate="hotel", arguments={"rating": 3.0})

        assert dominates(high_rated, low_rated) is True
        assert dominates(low_rated, high_rated) is False

    def test_no_dominance_relation(self):
        """Test propositions with no dominance relation."""
        prop1 = Proposition(predicate="hotel", arguments={"location": "Paris"})
        prop2 = Proposition(predicate="hotel", arguments={"location": "London"})

        assert dominates(prop1, prop2) is False
        assert dominates(prop2, prop1) is False

    def test_dominance_with_invalid_price(self):
        """Test dominance with non-numeric price values."""
        prop1 = Proposition(predicate="hotel", arguments={"price": "cheap"})
        prop2 = Proposition(predicate="hotel", arguments={"price": "expensive"})

        # Should return False if values aren't numeric
        assert dominates(prop1, prop2) is False
