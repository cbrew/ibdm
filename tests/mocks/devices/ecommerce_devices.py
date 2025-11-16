"""E-commerce and payment service mock devices.

Simulates payment processing, inventory management, and shipping services.
"""

from typing import Any
import random
from datetime import datetime, timedelta
from decimal import Decimal

from ibdm.core.actions import Action
from ibdm.core.information_state import InformationState
from ibdm.interfaces.device import ActionResult, ActionStatus, DeviceInterface


class PaymentDevice(DeviceInterface):
    """Mock payment processing service (e.g., Stripe, PayPal, Square).

    Simulates payment authorization, capture, refund, and verification.

    Actions:
    - authorize_payment: Authorize payment (hold funds)
    - capture_payment: Capture authorized payment
    - process_payment: Authorize and capture in one step
    - refund_payment: Refund captured payment
    - verify_card: Verify card details

    Preconditions:
    - Valid payment method
    - Sufficient funds (simulated)
    - Amount > 0

    Postconditions:
    - payment_authorized(transaction_id=...)
    - payment_captured(transaction_id=...)
    - payment_refunded(transaction_id=...)
    """

    CARD_NETWORKS = ["visa", "mastercard", "amex", "discover"]
    DECLINE_REASONS = [
        "insufficient_funds",
        "card_declined",
        "expired_card",
        "invalid_cvv",
        "suspected_fraud",
    ]

    def __init__(self, fail_rate: float = 0.1):
        """Initialize payment device.

        Args:
            fail_rate: Probability of payment declines (0.0-1.0)
        """
        self.transactions: dict[str, Any] = {}
        self.fail_rate = fail_rate
        self.transaction_count = 0

    def execute_action(self, action: Action, state: InformationState) -> ActionResult:
        """Execute payment action."""
        # Check preconditions
        if not self.check_preconditions(action, state):
            return ActionResult(
                status=ActionStatus.PRECONDITION_FAILED,
                action=action,
                error_message="Required payment parameters missing",
            )

        # Simulate payment declines
        if random.random() < self.fail_rate:
            decline_reason = random.choice(self.DECLINE_REASONS)
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Payment declined: {decline_reason}",
            )

        # Route to specific action handler
        if action.name == "authorize_payment":
            return self._authorize_payment(action)
        elif action.name == "capture_payment":
            return self._capture_payment(action)
        elif action.name == "process_payment":
            return self._process_payment(action)
        elif action.name == "refund_payment":
            return self._refund_payment(action)
        elif action.name == "verify_card":
            return self._verify_card(action)
        else:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Unknown action: {action.name}",
            )

    def check_preconditions(self, action: Action, state: InformationState) -> bool:
        """Check if payment preconditions are satisfied."""
        params = action.parameters

        if action.name in ["authorize_payment", "process_payment"]:
            # Require amount and payment method
            if "amount" not in params or "payment_method" not in params:
                return False
            # Amount must be positive
            try:
                amount = Decimal(str(params["amount"]))
                return amount > 0
            except (ValueError, TypeError):
                return False
        elif action.name in ["capture_payment", "refund_payment"]:
            # Require transaction ID
            return "transaction_id" in params
        elif action.name == "verify_card":
            # Require card details
            return "card_number" in params

        return True

    def get_postconditions(self, action: Action) -> list[str]:
        """Get postconditions for payment action."""
        if action.name == "authorize_payment":
            txn_id = f"TXN-{self.transaction_count:08d}"
            return [f"payment_authorized(transaction_id={txn_id})"]
        elif action.name == "capture_payment":
            return ["payment_captured"]
        elif action.name == "process_payment":
            txn_id = f"TXN-{self.transaction_count:08d}"
            return [
                f"payment_authorized(transaction_id={txn_id})",
                "payment_captured",
            ]
        elif action.name == "refund_payment":
            return ["payment_refunded"]
        elif action.name == "verify_card":
            return ["card_verified"]

        return []

    def _authorize_payment(self, action: Action) -> ActionResult:
        """Authorize payment (hold funds)."""
        self.transaction_count += 1
        txn_id = f"TXN-{self.transaction_count:08d}"

        params = action.parameters
        amount = Decimal(str(params["amount"]))

        transaction = {
            "transaction_id": txn_id,
            "amount": str(amount),
            "currency": params.get("currency", "USD"),
            "payment_method": params["payment_method"],
            "status": "authorized",
            "authorized_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(days=7)).isoformat(),
        }

        self.transactions[txn_id] = transaction

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "transaction_id": txn_id,
                "status": "authorized",
                "amount": str(amount),
                "currency": transaction["currency"],
                "expires_at": transaction["expires_at"],
            },
            postconditions=[f"payment_authorized(transaction_id={txn_id})"],
        )

    def _capture_payment(self, action: Action) -> ActionResult:
        """Capture authorized payment."""
        txn_id = action.parameters.get("transaction_id")

        if not txn_id or txn_id not in self.transactions:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Transaction {txn_id} not found",
            )

        transaction = self.transactions[txn_id]

        if transaction["status"] != "authorized":
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Transaction {txn_id} not in authorized state",
            )

        # Capture amount (can be less than authorized)
        capture_amount = action.parameters.get("amount", transaction["amount"])

        transaction["status"] = "captured"
        transaction["captured_at"] = datetime.now().isoformat()
        transaction["captured_amount"] = str(capture_amount)

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "transaction_id": txn_id,
                "status": "captured",
                "captured_amount": str(capture_amount),
            },
            postconditions=["payment_captured"],
        )

    def _process_payment(self, action: Action) -> ActionResult:
        """Process payment (authorize and capture in one step)."""
        self.transaction_count += 1
        txn_id = f"TXN-{self.transaction_count:08d}"

        params = action.parameters
        amount = Decimal(str(params["amount"]))

        transaction = {
            "transaction_id": txn_id,
            "amount": str(amount),
            "currency": params.get("currency", "USD"),
            "payment_method": params["payment_method"],
            "status": "captured",
            "processed_at": datetime.now().isoformat(),
        }

        self.transactions[txn_id] = transaction

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "transaction_id": txn_id,
                "status": "captured",
                "amount": str(amount),
                "currency": transaction["currency"],
            },
            postconditions=[
                f"payment_authorized(transaction_id={txn_id})",
                "payment_captured",
            ],
        )

    def _refund_payment(self, action: Action) -> ActionResult:
        """Refund captured payment."""
        txn_id = action.parameters.get("transaction_id")

        if not txn_id or txn_id not in self.transactions:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Transaction {txn_id} not found",
            )

        transaction = self.transactions[txn_id]

        if transaction["status"] != "captured":
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message="Can only refund captured transactions",
            )

        # Refund amount (can be partial)
        refund_amount = action.parameters.get("amount", transaction["amount"])

        refund_id = f"RFD-{self.transaction_count:08d}"
        self.transaction_count += 1

        transaction["status"] = "refunded"
        transaction["refunded_at"] = datetime.now().isoformat()
        transaction["refund_amount"] = str(refund_amount)
        transaction["refund_id"] = refund_id

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "transaction_id": txn_id,
                "refund_id": refund_id,
                "status": "refunded",
                "refund_amount": str(refund_amount),
            },
            postconditions=["payment_refunded"],
        )

    def _verify_card(self, action: Action) -> ActionResult:
        """Verify card details."""
        card_number = action.parameters.get("card_number", "")

        # Simulate card verification (last digit determines validity)
        is_valid = int(card_number[-1]) % 2 == 0 if card_number else False

        if not is_valid:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message="Invalid card number",
            )

        # Determine card network from first digit
        network = "unknown"
        if card_number.startswith("4"):
            network = "visa"
        elif card_number.startswith("5"):
            network = "mastercard"
        elif card_number.startswith("3"):
            network = "amex"
        elif card_number.startswith("6"):
            network = "discover"

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "valid": True,
                "card_network": network,
                "last_four": card_number[-4:],
            },
            postconditions=["card_verified"],
        )


class InventoryDevice(DeviceInterface):
    """Mock inventory management service (e.g., ShipStation, TradeGecko).

    Simulates product inventory tracking, reservations, and stock updates.

    Actions:
    - check_stock: Check product availability
    - reserve_inventory: Reserve items for order
    - release_reservation: Release reserved inventory
    - update_stock: Update stock levels
    - get_stock_alerts: Get low stock alerts

    Preconditions:
    - Valid product SKU
    - Sufficient inventory

    Postconditions:
    - inventory_reserved(reservation_id=...)
    - stock_updated(sku=..., quantity=...)
    """

    def __init__(self, fail_rate: float = 0.0):
        """Initialize inventory device.

        Args:
            fail_rate: Probability of simulated failures (0.0-1.0)
        """
        # Initialize with sample inventory
        self.inventory: dict[str, Any] = {
            "SKU-001": {"name": "Widget A", "quantity": 100, "reserved": 0},
            "SKU-002": {"name": "Widget B", "quantity": 50, "reserved": 0},
            "SKU-003": {"name": "Gadget X", "quantity": 25, "reserved": 0},
            "SKU-004": {"name": "Gadget Y", "quantity": 75, "reserved": 0},
            "SKU-005": {"name": "Tool Z", "quantity": 10, "reserved": 0},
        }
        self.reservations: dict[str, Any] = {}
        self.fail_rate = fail_rate
        self.reservation_count = 0

    def execute_action(self, action: Action, state: InformationState) -> ActionResult:
        """Execute inventory action."""
        # Check preconditions
        if not self.check_preconditions(action, state):
            return ActionResult(
                status=ActionStatus.PRECONDITION_FAILED,
                action=action,
                error_message="Required inventory parameters missing",
            )

        # Simulate random failures
        if random.random() < self.fail_rate:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message="Inventory service temporarily unavailable",
            )

        # Route to specific action handler
        if action.name == "check_stock":
            return self._check_stock(action)
        elif action.name == "reserve_inventory":
            return self._reserve_inventory(action)
        elif action.name == "release_reservation":
            return self._release_reservation(action)
        elif action.name == "update_stock":
            return self._update_stock(action)
        elif action.name == "get_stock_alerts":
            return self._get_stock_alerts(action)
        else:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Unknown action: {action.name}",
            )

    def check_preconditions(self, action: Action, state: InformationState) -> bool:
        """Check if inventory preconditions are satisfied."""
        params = action.parameters

        if action.name in ["check_stock", "reserve_inventory", "update_stock"]:
            # Require SKU
            return "sku" in params
        elif action.name == "release_reservation":
            # Require reservation ID
            return "reservation_id" in params
        elif action.name == "get_stock_alerts":
            # No preconditions
            return True

        return True

    def get_postconditions(self, action: Action) -> list[str]:
        """Get postconditions for inventory action."""
        if action.name == "check_stock":
            return ["stock_checked"]
        elif action.name == "reserve_inventory":
            res_id = f"RES-{self.reservation_count:06d}"
            return [f"inventory_reserved(reservation_id={res_id})"]
        elif action.name == "release_reservation":
            return ["reservation_released"]
        elif action.name == "update_stock":
            sku = action.parameters.get("sku", "unknown")
            qty = action.parameters.get("quantity", 0)
            return [f"stock_updated(sku={sku}, quantity={qty})"]
        elif action.name == "get_stock_alerts":
            return ["stock_alerts_retrieved"]

        return []

    def _check_stock(self, action: Action) -> ActionResult:
        """Check product stock availability."""
        sku = action.parameters.get("sku")

        if sku not in self.inventory:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Product {sku} not found",
            )

        item = self.inventory[sku]
        available = item["quantity"] - item["reserved"]

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "sku": sku,
                "name": item["name"],
                "total_quantity": item["quantity"],
                "reserved": item["reserved"],
                "available": available,
            },
            postconditions=["stock_checked"],
        )

    def _reserve_inventory(self, action: Action) -> ActionResult:
        """Reserve inventory for an order."""
        sku = action.parameters.get("sku")
        quantity = action.parameters.get("quantity", 1)

        if sku not in self.inventory:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Product {sku} not found",
            )

        item = self.inventory[sku]
        available = item["quantity"] - item["reserved"]

        if available < quantity:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Insufficient stock: {available} available, {quantity} requested",
            )

        # Create reservation
        self.reservation_count += 1
        res_id = f"RES-{self.reservation_count:06d}"

        item["reserved"] += quantity

        reservation = {
            "reservation_id": res_id,
            "sku": sku,
            "quantity": quantity,
            "reserved_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(hours=24)).isoformat(),
        }

        self.reservations[res_id] = reservation

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "reservation_id": res_id,
                "sku": sku,
                "quantity": quantity,
                "expires_at": reservation["expires_at"],
            },
            postconditions=[f"inventory_reserved(reservation_id={res_id})"],
        )

    def _release_reservation(self, action: Action) -> ActionResult:
        """Release reserved inventory."""
        res_id = action.parameters.get("reservation_id")

        if not res_id or res_id not in self.reservations:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Reservation {res_id} not found",
            )

        reservation = self.reservations[res_id]
        sku = reservation["sku"]
        quantity = reservation["quantity"]

        # Release reservation
        self.inventory[sku]["reserved"] -= quantity
        del self.reservations[res_id]

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "reservation_id": res_id,
                "sku": sku,
                "quantity_released": quantity,
            },
            postconditions=["reservation_released"],
        )

    def _update_stock(self, action: Action) -> ActionResult:
        """Update stock levels."""
        sku = action.parameters.get("sku")
        quantity = action.parameters.get("quantity")

        if sku not in self.inventory:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Product {sku} not found",
            )

        # Update quantity
        self.inventory[sku]["quantity"] = quantity

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "sku": sku,
                "new_quantity": quantity,
                "reserved": self.inventory[sku]["reserved"],
            },
            postconditions=[f"stock_updated(sku={sku}, quantity={quantity})"],
        )

    def _get_stock_alerts(self, action: Action) -> ActionResult:
        """Get low stock alerts."""
        threshold = action.parameters.get("threshold", 20)

        alerts = []
        for sku, item in self.inventory.items():
            available = item["quantity"] - item["reserved"]
            if available < threshold:
                alerts.append(
                    {
                        "sku": sku,
                        "name": item["name"],
                        "available": available,
                        "reserved": item["reserved"],
                    }
                )

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "alerts_count": len(alerts),
                "alerts": alerts,
                "threshold": threshold,
            },
            postconditions=["stock_alerts_retrieved"],
        )


class ShippingDevice(DeviceInterface):
    """Mock shipping/fulfillment service (e.g., ShipStation, EasyPost).

    Simulates shipment creation, tracking, and label generation.

    Actions:
    - create_shipment: Create new shipment
    - get_shipping_rates: Get shipping rate quotes
    - track_shipment: Track shipment status
    - cancel_shipment: Cancel shipment
    - generate_label: Generate shipping label

    Preconditions:
    - Valid address
    - Valid package dimensions/weight

    Postconditions:
    - shipment_created(tracking_number=...)
    - label_generated(tracking_number=...)
    """

    CARRIERS = ["USPS", "UPS", "FedEx", "DHL"]
    SERVICE_LEVELS = ["Ground", "2-Day", "Overnight", "International"]
    SHIPMENT_STATUSES = [
        "created",
        "label_printed",
        "in_transit",
        "out_for_delivery",
        "delivered",
        "exception",
    ]

    def __init__(self, fail_rate: float = 0.0):
        """Initialize shipping device.

        Args:
            fail_rate: Probability of simulated failures (0.0-1.0)
        """
        self.shipments: dict[str, Any] = {}
        self.fail_rate = fail_rate
        self.shipment_count = 0

    def execute_action(self, action: Action, state: InformationState) -> ActionResult:
        """Execute shipping action."""
        # Check preconditions
        if not self.check_preconditions(action, state):
            return ActionResult(
                status=ActionStatus.PRECONDITION_FAILED,
                action=action,
                error_message="Required shipping parameters missing",
            )

        # Simulate random failures
        if random.random() < self.fail_rate:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message="Shipping service temporarily unavailable",
            )

        # Route to specific action handler
        if action.name == "create_shipment":
            return self._create_shipment(action)
        elif action.name == "get_shipping_rates":
            return self._get_shipping_rates(action)
        elif action.name == "track_shipment":
            return self._track_shipment(action)
        elif action.name == "cancel_shipment":
            return self._cancel_shipment(action)
        elif action.name == "generate_label":
            return self._generate_label(action)
        else:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Unknown action: {action.name}",
            )

    def check_preconditions(self, action: Action, state: InformationState) -> bool:
        """Check if shipping preconditions are satisfied."""
        params = action.parameters

        if action.name == "create_shipment":
            # Require addresses and package info
            required = ["from_address", "to_address", "weight"]
            return all(key in params for key in required)
        elif action.name == "get_shipping_rates":
            # Require addresses
            required = ["from_address", "to_address"]
            return all(key in params for key in required)
        elif action.name in ["track_shipment", "cancel_shipment", "generate_label"]:
            # Require tracking number
            return "tracking_number" in params

        return True

    def get_postconditions(self, action: Action) -> list[str]:
        """Get postconditions for shipping action."""
        if action.name == "create_shipment":
            tracking = f"TRK-{self.shipment_count:010d}"
            return [f"shipment_created(tracking_number={tracking})"]
        elif action.name == "get_shipping_rates":
            return ["shipping_rates_retrieved"]
        elif action.name == "track_shipment":
            return ["shipment_tracked"]
        elif action.name == "cancel_shipment":
            return ["shipment_cancelled"]
        elif action.name == "generate_label":
            return ["label_generated"]

        return []

    def _create_shipment(self, action: Action) -> ActionResult:
        """Create new shipment."""
        self.shipment_count += 1
        tracking_number = f"TRK-{self.shipment_count:010d}"

        params = action.parameters
        carrier = params.get("carrier", random.choice(self.CARRIERS))
        service = params.get("service_level", "Ground")

        # Calculate estimated delivery
        days_map = {"Ground": 5, "2-Day": 2, "Overnight": 1, "International": 10}
        days = days_map.get(service, 5)
        estimated_delivery = (datetime.now() + timedelta(days=days)).date().isoformat()

        shipment = {
            "tracking_number": tracking_number,
            "carrier": carrier,
            "service_level": service,
            "from_address": params["from_address"],
            "to_address": params["to_address"],
            "weight": params["weight"],
            "status": "created",
            "created_at": datetime.now().isoformat(),
            "estimated_delivery": estimated_delivery,
        }

        self.shipments[tracking_number] = shipment

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "tracking_number": tracking_number,
                "carrier": carrier,
                "service_level": service,
                "estimated_delivery": estimated_delivery,
                "status": "created",
            },
            postconditions=[f"shipment_created(tracking_number={tracking_number})"],
        )

    def _get_shipping_rates(self, action: Action) -> ActionResult:
        """Get shipping rate quotes."""
        # Generate sample rates
        rates = []
        base_rate = random.uniform(5.0, 15.0)

        for carrier in self.CARRIERS:
            for service in self.SERVICE_LEVELS:
                multiplier = {"Ground": 1.0, "2-Day": 1.5, "Overnight": 3.0, "International": 2.5}
                rate = base_rate * multiplier.get(service, 1.0)

                rates.append(
                    {
                        "carrier": carrier,
                        "service_level": service,
                        "rate": round(rate, 2),
                        "currency": "USD",
                        "delivery_days": {
                            "Ground": 5,
                            "2-Day": 2,
                            "Overnight": 1,
                            "International": 10,
                        }.get(service, 5),
                    }
                )

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "rates_count": len(rates),
                "rates": sorted(rates, key=lambda x: x["rate"])[:8],  # Return 8 cheapest
            },
            postconditions=["shipping_rates_retrieved"],
        )

    def _track_shipment(self, action: Action) -> ActionResult:
        """Track shipment status."""
        tracking_number = action.parameters.get("tracking_number")

        if not tracking_number or tracking_number not in self.shipments:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Tracking number {tracking_number} not found",
            )

        shipment = self.shipments[tracking_number]

        # Simulate status progression
        current_status = shipment["status"]
        if current_status == "created" and random.random() < 0.3:
            shipment["status"] = "label_printed"
        elif current_status == "label_printed" and random.random() < 0.4:
            shipment["status"] = "in_transit"
        elif current_status == "in_transit" and random.random() < 0.3:
            shipment["status"] = "out_for_delivery"
        elif current_status == "out_for_delivery" and random.random() < 0.5:
            shipment["status"] = "delivered"
            shipment["delivered_at"] = datetime.now().isoformat()

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "tracking_number": tracking_number,
                "status": shipment["status"],
                "carrier": shipment["carrier"],
                "estimated_delivery": shipment["estimated_delivery"],
                "last_update": datetime.now().isoformat(),
            },
            postconditions=["shipment_tracked"],
        )

    def _cancel_shipment(self, action: Action) -> ActionResult:
        """Cancel shipment."""
        tracking_number = action.parameters.get("tracking_number")

        if not tracking_number or tracking_number not in self.shipments:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Tracking number {tracking_number} not found",
            )

        shipment = self.shipments[tracking_number]

        # Can only cancel before in_transit
        if shipment["status"] in ["in_transit", "out_for_delivery", "delivered"]:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Cannot cancel shipment in {shipment['status']} status",
            )

        shipment["status"] = "cancelled"
        shipment["cancelled_at"] = datetime.now().isoformat()

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "tracking_number": tracking_number,
                "status": "cancelled",
            },
            postconditions=["shipment_cancelled"],
        )

    def _generate_label(self, action: Action) -> ActionResult:
        """Generate shipping label."""
        tracking_number = action.parameters.get("tracking_number")

        if not tracking_number or tracking_number not in self.shipments:
            return ActionResult(
                status=ActionStatus.FAILURE,
                action=action,
                error_message=f"Tracking number {tracking_number} not found",
            )

        shipment = self.shipments[tracking_number]
        shipment["status"] = "label_printed"
        shipment["label_generated_at"] = datetime.now().isoformat()

        return ActionResult(
            status=ActionStatus.SUCCESS,
            action=action,
            return_value={
                "tracking_number": tracking_number,
                "label_url": f"https://api.shipping.example/labels/{tracking_number}.pdf",
                "format": "pdf",
                "status": "label_printed",
            },
            postconditions=["label_generated"],
        )
