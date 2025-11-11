"""Update rule system for Issue-Based Dialogue Management.

This module provides the rule-based system for transforming information states
through precondition-action pairs.
"""

from ibdm.rules.update_rules import RuleSet, UpdateRule

__all__ = [
    "UpdateRule",
    "RuleSet",
]
