"""Mock implementations for testing IBDM dialogue managers.

This package provides mock implementations of key interfaces to enable
testing dialogue managers without real LLM calls or external dependencies.
"""

from tests.mocks.mock_nlu_service import MockNLUService, create_mock_nlu

__all__ = [
    "MockNLUService",
    "create_mock_nlu",
]
