"""Visualization module for dialogue state and rule execution.

This module provides data structures and utilities for visualizing dialogue
states, state changes (deltas), and rule execution traces.

Key Components:
- StateSnapshot: Immutable snapshot of InformationState at a point in time
- StateDiff: Representation of changes between two states
- RuleTrace: Record of rule execution (preconditions, effects, selected rule)
- DiffEngine: Computes diffs between states
"""

from ibdm.visualization.diff_engine import DiffEngine, compute_diff
from ibdm.visualization.rule_trace import RuleTrace
from ibdm.visualization.state_diff import ChangedField, ChangeType, StateDiff
from ibdm.visualization.state_snapshot import StateSnapshot

__all__ = [
    "StateSnapshot",
    "StateDiff",
    "ChangeType",
    "ChangedField",
    "RuleTrace",
    "DiffEngine",
    "compute_diff",
]
