"""Mock implementations for testing IBDM dialogue managers.

This package provides mock implementations of key interfaces to enable
testing dialogue managers without real LLM calls or external dependencies.
"""

from tests.mocks.mock_device import MockDevice

__all__ = [
    "MockDevice",
]

# Lazy imports for NLU mocks (require pydantic)
try:
    from tests.mocks.mock_nlu_service import (  # noqa: F401
        MockNLUService,
        create_mock_nlu,
    )

    __all__.extend(["MockNLUService", "create_mock_nlu"])
except ImportError:
    # NLU dependencies not available
    pass
