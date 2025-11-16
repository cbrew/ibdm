"""Domain-specific mock device implementations.

This package provides realistic mock implementations of various web APIs
and services for testing action execution across different domains.
"""

from tests.mocks.devices.ecommerce_devices import (
    InventoryDevice,
    PaymentDevice,
    ShippingDevice,
)
from tests.mocks.devices.iot_devices import (
    AutomationDevice,
    SensorDevice,
    SmartHomeDevice,
)
from tests.mocks.devices.legal_devices import (
    ComplianceCheckDevice,
    DocumentGenerationDevice,
    SignatureDevice,
)
from tests.mocks.devices.travel_devices import (
    CarRentalDevice,
    FlightBookingDevice,
    HotelBookingDevice,
)

__all__ = [
    # Travel
    "FlightBookingDevice",
    "HotelBookingDevice",
    "CarRentalDevice",
    # Legal
    "DocumentGenerationDevice",
    "SignatureDevice",
    "ComplianceCheckDevice",
    # E-commerce
    "PaymentDevice",
    "InventoryDevice",
    "ShippingDevice",
    # IoT
    "SmartHomeDevice",
    "SensorDevice",
    "AutomationDevice",
]
