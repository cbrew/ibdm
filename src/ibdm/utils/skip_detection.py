"""Utility for detecting when users want to skip/override questions.

This module provides pattern matching for user utterances that indicate
they want to proceed without answering the current question.
"""

import re


def is_skip_request(utterance: str) -> bool:
    """Detect if user wants to skip the current question.

    Recognizes patterns like:
    - "skip that"
    - "I don't have that information"
    - "move on without it"
    - "proceed anyway"
    - "don't know"
    - "not available"

    Args:
        utterance: User's utterance text

    Returns:
        True if utterance indicates skip request

    Examples:
        >>> is_skip_request("skip that question")
        True
        >>> is_skip_request("I don't have that info")
        True
        >>> is_skip_request("Paris")
        False
    """
    if not utterance:
        return False

    # Normalize to lowercase for matching
    text = utterance.lower().strip()

    # Skip patterns
    skip_patterns = [
        r"\b(skip|pass)\b",  # "skip", "pass"
        r"\bdon'?t\s+(have|know)\b",  # "don't have", "don't know"
        r"\b(not|no)\s+available\b",  # "not available", "no available"
        r"\bmove\s+on\b",  # "move on"
        r"\bproceed\s+(anyway|without)\b",  # "proceed anyway", "proceed without"
        r"\bcan'?t\s+provide\b",  # "can't provide"
        r"\bno\s+info(rmation)?\b",  # "no info", "no information"
        r"^(idk|dunno)$",  # "idk", "dunno"
    ]

    # Check if any pattern matches
    for pattern in skip_patterns:
        if re.search(pattern, text):
            return True

    return False
