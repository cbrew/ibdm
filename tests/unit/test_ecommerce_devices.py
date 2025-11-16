"""Unit tests for e-commerce domain mock devices.

Tests PaymentDevice, InventoryDevice, and ShippingDevice.
"""

import sys
from pathlib import Path

# Add tests directory to path
tests_dir = Path(__file__).parent.parent
sys.path.insert(0, str(tests_dir))

from mocks.devices.ecommerce_devices import (  # noqa: E402
    InventoryDevice,
    PaymentDevice,
    ShippingDevice,
)

from ibdm.core.actions import Action, ActionType  # noqa: E402
from ibdm.core.information_state import InformationState  # noqa: E402
from ibdm.interfaces.device import ActionStatus  # noqa: E402


class TestPaymentDevice:
    """Test PaymentDevice."""

    def test_initialization(self) -> None:
        """Test device initialization."""
        device = PaymentDevice()

        assert device.transactions == {}
        assert device.transaction_count == 0

    def test_authorize_payment_success(self) -> None:
        """Test successful payment authorization."""
        device = PaymentDevice(fail_rate=0.0)
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="authorize_payment",
            parameters={
                "amount": "100.00",
                "payment_method": "card_xxxx1234",
                "currency": "USD",
            },
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert "transaction_id" in result.return_value
        assert result.return_value["transaction_id"].startswith("TXN-")
        assert result.return_value["status"] == "authorized"

    def test_authorize_missing_parameters(self) -> None:
        """Test authorization with missing parameters."""
        device = PaymentDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="authorize_payment",
            parameters={"amount": "100.00"},  # Missing payment_method
        )

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert result.status == ActionStatus.PRECONDITION_FAILED

    def test_authorize_negative_amount(self) -> None:
        """Test authorization with negative amount."""
        device = PaymentDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="authorize_payment",
            parameters={
                "amount": "-100.00",
                "payment_method": "card_xxxx1234",
            },
        )

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert result.status == ActionStatus.PRECONDITION_FAILED

    def test_capture_payment_success(self) -> None:
        """Test successful payment capture."""
        device = PaymentDevice(fail_rate=0.0)
        state = InformationState()

        # Authorize first
        auth_action = Action(
            action_type=ActionType.EXECUTE,
            name="authorize_payment",
            parameters={
                "amount": "100.00",
                "payment_method": "card_xxxx1234",
            },
        )

        auth_result = device.execute_action(auth_action, state)
        txn_id = auth_result.return_value["transaction_id"]

        # Capture
        capture_action = Action(
            action_type=ActionType.EXECUTE,
            name="capture_payment",
            parameters={"transaction_id": txn_id},
        )

        capture_result = device.execute_action(capture_action, state)

        assert capture_result.is_successful()
        assert capture_result.return_value["status"] == "captured"

    def test_capture_nonexistent_transaction(self) -> None:
        """Test capturing non-existent transaction."""
        device = PaymentDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="capture_payment",
            parameters={"transaction_id": "INVALID-123"},
        )

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert result.status == ActionStatus.FAILURE

    def test_process_payment_one_step(self) -> None:
        """Test one-step payment processing."""
        device = PaymentDevice(fail_rate=0.0)
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="process_payment",
            parameters={
                "amount": "50.00",
                "payment_method": "card_xxxx1234",
            },
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert result.return_value["status"] == "captured"
        # Should have both postconditions
        assert len(result.postconditions) == 2

    def test_refund_payment_success(self) -> None:
        """Test successful payment refund."""
        device = PaymentDevice(fail_rate=0.0)
        state = InformationState()

        # Process payment first
        process_action = Action(
            action_type=ActionType.EXECUTE,
            name="process_payment",
            parameters={
                "amount": "100.00",
                "payment_method": "card_xxxx1234",
            },
        )

        process_result = device.execute_action(process_action, state)
        txn_id = process_result.return_value["transaction_id"]

        # Refund
        refund_action = Action(
            action_type=ActionType.EXECUTE,
            name="refund_payment",
            parameters={"transaction_id": txn_id},
        )

        refund_result = device.execute_action(refund_action, state)

        assert refund_result.is_successful()
        assert "refund_id" in refund_result.return_value
        assert refund_result.return_value["status"] == "refunded"

    def test_verify_card_valid(self) -> None:
        """Test card verification with valid card."""
        device = PaymentDevice()
        state = InformationState()

        # Card number ending in even digit is valid
        action = Action(
            action_type=ActionType.EXECUTE,
            name="verify_card",
            parameters={"card_number": "4532123456789012"},
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert result.return_value["valid"] is True
        assert result.return_value["card_network"] == "visa"

    def test_verify_card_invalid(self) -> None:
        """Test card verification with invalid card."""
        device = PaymentDevice()
        state = InformationState()

        # Card number ending in odd digit is invalid
        action = Action(
            action_type=ActionType.EXECUTE,
            name="verify_card",
            parameters={"card_number": "4532123456789013"},
        )

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert result.status == ActionStatus.FAILURE


class TestInventoryDevice:
    """Test InventoryDevice."""

    def test_initialization(self) -> None:
        """Test device initialization."""
        device = InventoryDevice()

        assert len(device.inventory) > 0
        assert device.reservations == {}

    def test_check_stock_success(self) -> None:
        """Test checking stock availability."""
        device = InventoryDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.GET,
            name="check_stock",
            parameters={"sku": "SKU-001"},
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert "sku" in result.return_value
        assert "available" in result.return_value
        assert "total_quantity" in result.return_value

    def test_check_nonexistent_sku(self) -> None:
        """Test checking non-existent SKU."""
        device = InventoryDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.GET,
            name="check_stock",
            parameters={"sku": "INVALID-SKU"},
        )

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert result.status == ActionStatus.FAILURE

    def test_reserve_inventory_success(self) -> None:
        """Test successful inventory reservation."""
        device = InventoryDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="reserve_inventory",
            parameters={"sku": "SKU-001", "quantity": 5},
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert "reservation_id" in result.return_value
        assert result.return_value["reservation_id"].startswith("RES-")

        # Check that inventory was reserved
        assert device.inventory["SKU-001"]["reserved"] == 5

    def test_reserve_insufficient_stock(self) -> None:
        """Test reservation with insufficient stock."""
        device = InventoryDevice()
        state = InformationState()

        # Try to reserve more than available
        action = Action(
            action_type=ActionType.EXECUTE,
            name="reserve_inventory",
            parameters={"sku": "SKU-001", "quantity": 999},
        )

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert "insufficient stock" in result.error_message.lower()

    def test_release_reservation_success(self) -> None:
        """Test releasing inventory reservation."""
        device = InventoryDevice()
        state = InformationState()

        # Reserve first
        reserve_action = Action(
            action_type=ActionType.EXECUTE,
            name="reserve_inventory",
            parameters={"sku": "SKU-001", "quantity": 5},
        )

        reserve_result = device.execute_action(reserve_action, state)
        res_id = reserve_result.return_value["reservation_id"]

        initial_reserved = device.inventory["SKU-001"]["reserved"]

        # Release
        release_action = Action(
            action_type=ActionType.EXECUTE,
            name="release_reservation",
            parameters={"reservation_id": res_id},
        )

        release_result = device.execute_action(release_action, state)

        assert release_result.is_successful()
        assert device.inventory["SKU-001"]["reserved"] == initial_reserved - 5

    def test_update_stock_success(self) -> None:
        """Test updating stock levels."""
        device = InventoryDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="update_stock",
            parameters={"sku": "SKU-001", "quantity": 200},
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert device.inventory["SKU-001"]["quantity"] == 200

    def test_get_stock_alerts(self) -> None:
        """Test getting low stock alerts."""
        device = InventoryDevice()
        state = InformationState()

        # Set low stock for a SKU
        device.inventory["SKU-005"]["quantity"] = 5
        device.inventory["SKU-005"]["reserved"] = 0

        action = Action(
            action_type=ActionType.GET,
            name="get_stock_alerts",
            parameters={"threshold": 20},
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert "alerts" in result.return_value
        assert result.return_value["alerts_count"] > 0


class TestShippingDevice:
    """Test ShippingDevice."""

    def test_initialization(self) -> None:
        """Test device initialization."""
        device = ShippingDevice()

        assert device.shipments == {}
        assert device.shipment_count == 0

    def test_create_shipment_success(self) -> None:
        """Test successful shipment creation."""
        device = ShippingDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="create_shipment",
            parameters={
                "from_address": "123 Main St, SF, CA",
                "to_address": "456 Elm St, NY, NY",
                "weight": "5.0",
                "carrier": "USPS",
                "service_level": "Ground",
            },
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert "tracking_number" in result.return_value
        assert result.return_value["tracking_number"].startswith("TRK-")
        assert "estimated_delivery" in result.return_value

    def test_create_shipment_missing_parameters(self) -> None:
        """Test shipment creation with missing parameters."""
        device = ShippingDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.EXECUTE,
            name="create_shipment",
            parameters={"from_address": "123 Main St"},  # Missing to_address, weight
        )

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert result.status == ActionStatus.PRECONDITION_FAILED

    def test_get_shipping_rates(self) -> None:
        """Test getting shipping rate quotes."""
        device = ShippingDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.GET,
            name="get_shipping_rates",
            parameters={
                "from_address": "123 Main St, SF, CA",
                "to_address": "456 Elm St, NY, NY",
            },
        )

        result = device.execute_action(action, state)

        assert result.is_successful()
        assert "rates" in result.return_value
        assert len(result.return_value["rates"]) > 0

        # Check rate structure
        rate = result.return_value["rates"][0]
        assert "carrier" in rate
        assert "service_level" in rate
        assert "rate" in rate

    def test_track_shipment_success(self) -> None:
        """Test tracking shipment status."""
        device = ShippingDevice()
        state = InformationState()

        # Create shipment first
        create_action = Action(
            action_type=ActionType.EXECUTE,
            name="create_shipment",
            parameters={
                "from_address": "123 Main St, SF, CA",
                "to_address": "456 Elm St, NY, NY",
                "weight": "5.0",
            },
        )

        create_result = device.execute_action(create_action, state)
        tracking_number = create_result.return_value["tracking_number"]

        # Track it
        track_action = Action(
            action_type=ActionType.GET,
            name="track_shipment",
            parameters={"tracking_number": tracking_number},
        )

        track_result = device.execute_action(track_action, state)

        assert track_result.is_successful()
        assert "status" in track_result.return_value
        assert "carrier" in track_result.return_value

    def test_track_nonexistent_shipment(self) -> None:
        """Test tracking non-existent shipment."""
        device = ShippingDevice()
        state = InformationState()

        action = Action(
            action_type=ActionType.GET,
            name="track_shipment",
            parameters={"tracking_number": "INVALID-123"},
        )

        result = device.execute_action(action, state)

        assert not result.is_successful()
        assert result.status == ActionStatus.FAILURE

    def test_cancel_shipment_success(self) -> None:
        """Test cancelling shipment."""
        device = ShippingDevice()
        state = InformationState()

        # Create shipment
        create_action = Action(
            action_type=ActionType.EXECUTE,
            name="create_shipment",
            parameters={
                "from_address": "123 Main St, SF, CA",
                "to_address": "456 Elm St, NY, NY",
                "weight": "5.0",
            },
        )

        create_result = device.execute_action(create_action, state)
        tracking_number = create_result.return_value["tracking_number"]

        # Cancel it
        cancel_action = Action(
            action_type=ActionType.CANCEL,
            name="cancel_shipment",
            parameters={"tracking_number": tracking_number},
        )

        cancel_result = device.execute_action(cancel_action, state)

        assert cancel_result.is_successful()
        assert device.shipments[tracking_number]["status"] == "cancelled"

    def test_cancel_in_transit_shipment(self) -> None:
        """Test cancelling shipment that's in transit."""
        device = ShippingDevice()
        state = InformationState()

        # Create shipment
        create_action = Action(
            action_type=ActionType.EXECUTE,
            name="create_shipment",
            parameters={
                "from_address": "123 Main St, SF, CA",
                "to_address": "456 Elm St, NY, NY",
                "weight": "5.0",
            },
        )

        create_result = device.execute_action(create_action, state)
        tracking_number = create_result.return_value["tracking_number"]

        # Set to in_transit
        device.shipments[tracking_number]["status"] = "in_transit"

        # Try to cancel
        cancel_action = Action(
            action_type=ActionType.CANCEL,
            name="cancel_shipment",
            parameters={"tracking_number": tracking_number},
        )

        cancel_result = device.execute_action(cancel_action, state)

        assert not cancel_result.is_successful()
        assert "cannot cancel" in cancel_result.error_message.lower()

    def test_generate_label_success(self) -> None:
        """Test generating shipping label."""
        device = ShippingDevice()
        state = InformationState()

        # Create shipment
        create_action = Action(
            action_type=ActionType.EXECUTE,
            name="create_shipment",
            parameters={
                "from_address": "123 Main St, SF, CA",
                "to_address": "456 Elm St, NY, NY",
                "weight": "5.0",
            },
        )

        create_result = device.execute_action(create_action, state)
        tracking_number = create_result.return_value["tracking_number"]

        # Generate label
        label_action = Action(
            action_type=ActionType.EXECUTE,
            name="generate_label",
            parameters={"tracking_number": tracking_number},
        )

        label_result = device.execute_action(label_action, state)

        assert label_result.is_successful()
        assert "label_url" in label_result.return_value
        assert device.shipments[tracking_number]["status"] == "label_printed"
