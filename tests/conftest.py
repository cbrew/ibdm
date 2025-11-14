"""Pytest configuration for IBDM tests."""


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--run-llm",
        action="store_true",
        default=False,
        help="Run tests that require LLM API calls (needs IBDM_API_KEY)",
    )


def pytest_configure(config):
    """Configure custom markers."""
    config.addinivalue_line(
        "markers", "llm: marks tests that require LLM API access (deselect with '-m \"not llm\"')"
    )
