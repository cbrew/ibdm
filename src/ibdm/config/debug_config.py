"""Debug configuration for IBDM logging.

Controls logging levels based on IBDM_DEBUG environment variable.

Usage:
    export IBDM_DEBUG=all           # Enable all debug logging
    export IBDM_DEBUG=rules         # Enable rule logging only
    export IBDM_DEBUG=qud           # Enable QUD logging only
    export IBDM_DEBUG=rules,qud     # Enable multiple categories
    export IBDM_DEBUG=phases        # Enable phase logging
    export IBDM_DEBUG=state         # Enable state logging

Categories:
    - all: Enable all debug logging
    - rules: Log rule evaluation and selection
    - qud: Log QUD stack operations
    - phases: Log dialogue phases (INTERPRET/INTEGRATE/SELECT/GENERATE)
    - state: Log state transitions
"""

import logging
import os
from typing import Any

# Parse IBDM_DEBUG environment variable
_debug_env = os.getenv("IBDM_DEBUG", "").lower()
_debug_flags = set(flag.strip() for flag in _debug_env.split(",") if flag.strip())

# Check if specific debug categories are enabled
DEBUG_ENABLED = bool(_debug_flags)
DEBUG_ALL = "all" in _debug_flags
DEBUG_RULES = DEBUG_ALL or "rules" in _debug_flags
DEBUG_QUD = DEBUG_ALL or "qud" in _debug_flags
DEBUG_PHASES = DEBUG_ALL or "phases" in _debug_flags
DEBUG_STATE = DEBUG_ALL or "state" in _debug_flags


def is_debug_enabled(category: str = "all") -> bool:
    """Check if debug logging is enabled for a category.

    Args:
        category: Debug category to check (all, rules, qud, phases, state)

    Returns:
        True if debug logging is enabled for this category
    """
    if category == "all":
        return DEBUG_ENABLED
    elif category == "rules":
        return DEBUG_RULES
    elif category == "qud":
        return DEBUG_QUD
    elif category == "phases":
        return DEBUG_PHASES
    elif category == "state":
        return DEBUG_STATE
    else:
        return DEBUG_ALL


def configure_logging(level: int | None = None) -> None:
    """Configure IBDM logging based on debug flags.

    Sets up logging handlers and formatters for the IBDM package.

    Args:
        level: Optional logging level override. If None, uses debug flags to determine level.
    """
    # Determine logging level
    if level is None:
        if DEBUG_ENABLED:
            level = logging.DEBUG
        else:
            level = logging.WARNING

    # Configure root logger for ibdm package
    ibdm_logger = logging.getLogger("ibdm")
    ibdm_logger.setLevel(level)

    # Only add handler if none exists (avoid duplicate handlers)
    if not ibdm_logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(level)

        # Use detailed format when debugging
        if DEBUG_ENABLED:
            formatter = logging.Formatter("[%(levelname)s] %(name)s: %(message)s")
        else:
            formatter = logging.Formatter("%(levelname)s: %(message)s")

        handler.setFormatter(formatter)
        ibdm_logger.addHandler(handler)

    # Configure specific module loggers based on flags
    if DEBUG_RULES:
        logging.getLogger("ibdm.rules").setLevel(logging.DEBUG)

    if DEBUG_QUD:
        logging.getLogger("ibdm.core.information_state").setLevel(logging.DEBUG)

    if DEBUG_PHASES:
        logging.getLogger("ibdm.engine").setLevel(logging.DEBUG)

    if DEBUG_STATE:
        logging.getLogger("ibdm.core").setLevel(logging.DEBUG)


def get_debug_info() -> dict[str, Any]:
    """Get current debug configuration information.

    Returns:
        Dictionary with debug configuration details
    """
    return {
        "enabled": DEBUG_ENABLED,
        "flags": list(_debug_flags),
        "categories": {
            "all": DEBUG_ALL,
            "rules": DEBUG_RULES,
            "qud": DEBUG_QUD,
            "phases": DEBUG_PHASES,
            "state": DEBUG_STATE,
        },
        "env_var": _debug_env or "(not set)",
    }


# Auto-configure on module import
configure_logging()
