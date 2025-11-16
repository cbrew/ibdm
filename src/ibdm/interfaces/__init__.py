"""Device and external system interfaces for action execution.

This package provides abstract interfaces for connecting the dialogue system
to external devices and systems for action execution.
"""

from ibdm.interfaces.device import (
    ActionResult,
    ActionStatus,
    DeviceInterface,
)

__all__ = [
    "ActionResult",
    "ActionStatus",
    "DeviceInterface",
]
