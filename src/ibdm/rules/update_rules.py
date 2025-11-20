"""Update rule system for Issue-Based Dialogue Management.

Update rules are condition-action pairs that modify the information state.
They form the core mechanism for dialogue state transitions.

Based on Larsson (2002) Issue-based Dialogue Management.
"""

import logging
from collections.abc import Callable
from dataclasses import dataclass

from ibdm.core import InformationState

logger = logging.getLogger(__name__)


@dataclass
class UpdateRule:
    """Information state update rule.

    Update rules consist of preconditions that check if the rule applies,
    and effects that transform the information state when the rule fires.

    Rule types:
    - interpretation: Map utterances to dialogue moves
    - integration: Update IS based on dialogue moves
    - selection: Choose next system action
    - generation: Produce utterance from dialogue move
    """

    name: str
    """Unique identifier for this rule"""

    preconditions: Callable[[InformationState], bool]
    """Function that checks if this rule applies to the current state"""

    effects: Callable[[InformationState], InformationState]
    """Function that transforms the state when the rule fires"""

    priority: int = 0
    """Priority for rule ordering (higher = applied first)"""

    rule_type: str = "integration"
    """Type of rule: 'interpretation', 'integration', 'selection', 'generation'"""

    def applies(self, state: InformationState) -> bool:
        """Check if this rule's preconditions are satisfied.

        Args:
            state: Current information state

        Returns:
            True if the rule can be applied
        """
        return self.preconditions(state)

    def apply(self, state: InformationState) -> InformationState:
        """Apply this rule's effects to the state.

        Args:
            state: Current information state

        Returns:
            Updated information state
        """
        return self.effects(state)

    def __str__(self) -> str:
        """Return string representation."""
        return f"UpdateRule({self.name}, type={self.rule_type}, priority={self.priority})"


class RuleSet:
    """Collection of update rules organized by type.

    The RuleSet manages multiple update rules and provides methods for
    applying them systematically to information states.
    """

    def __init__(self) -> None:
        """Initialize an empty rule set."""
        self.rules: dict[str, list[UpdateRule]] = {
            "interpretation": [],
            "integration": [],
            "selection": [],
            "generation": [],
        }

    def add_rule(self, rule: UpdateRule) -> None:
        """Add a rule to the rule set.

        Rules are automatically sorted by priority (highest first).

        Args:
            rule: The update rule to add
        """
        if rule.rule_type not in self.rules:
            self.rules[rule.rule_type] = []

        self.rules[rule.rule_type].append(rule)
        # Sort by priority (highest first)
        self.rules[rule.rule_type].sort(key=lambda r: r.priority, reverse=True)

    def remove_rule(self, rule_name: str, rule_type: str | None = None) -> bool:
        """Remove a rule from the rule set.

        Args:
            rule_name: Name of the rule to remove
            rule_type: Optional type to search in; if None, searches all types

        Returns:
            True if a rule was removed, False otherwise
        """
        types_to_search = [rule_type] if rule_type else self.rules.keys()

        for rtype in types_to_search:
            if rtype in self.rules:
                original_length = len(self.rules[rtype])
                self.rules[rtype] = [r for r in self.rules[rtype] if r.name != rule_name]
                if len(self.rules[rtype]) < original_length:
                    return True

        return False

    def get_rules(self, rule_type: str) -> list[UpdateRule]:
        """Get all rules of a specific type.

        Args:
            rule_type: Type of rules to retrieve

        Returns:
            List of rules of the specified type (sorted by priority)
        """
        return self.rules.get(rule_type, [])

    def apply_rules(self, rule_type: str, state: InformationState) -> InformationState:
        """Apply all applicable rules of a given type.

        Rules are applied in priority order. Each rule's preconditions are
        checked, and if they pass, the rule's effects are applied.

        Args:
            rule_type: Type of rules to apply
            state: Current information state

        Returns:
            Updated information state after applying all matching rules
        """
        rules_list = self.rules.get(rule_type, [])
        logger.debug(f"Evaluating {len(rules_list)} {rule_type} rules")

        current_state = state
        rules_fired = 0

        for rule in rules_list:
            preconditions_met = rule.applies(current_state)
            status = "✓" if preconditions_met else "✗"
            logger.debug(f"  {status} {rule.name} (priority={rule.priority})")

            if preconditions_met:
                logger.info(f"  → Executing rule: {rule.name}")
                current_state = rule.apply(current_state)
                rules_fired += 1
                logger.debug(f"  ← Rule completed: {rule.name}")

        logger.debug(f"Applied {rules_fired}/{len(rules_list)} {rule_type} rules")
        return current_state

    def apply_first_matching(
        self, rule_type: str, state: InformationState
    ) -> tuple[InformationState, UpdateRule | None]:
        """Apply only the first matching rule of a given type.

        Useful for selection rules where only one action should be chosen.

        Args:
            rule_type: Type of rules to apply
            state: Current information state

        Returns:
            Tuple of (updated state, rule that was applied or None)
        """
        rules_list = self.rules.get(rule_type, [])
        logger.debug(f"Evaluating {len(rules_list)} {rule_type} rules (first match only)")

        for rule in rules_list:
            preconditions_met = rule.applies(state)
            status = "✓" if preconditions_met else "✗"
            logger.debug(f"  {status} {rule.name} (priority={rule.priority})")

            if preconditions_met:
                logger.info(f"  → Executing first matching rule: {rule.name}")
                new_state = rule.apply(state)
                logger.debug(f"  ← Rule completed: {rule.name}")
                return new_state, rule

        logger.debug(f"No matching {rule_type} rules found")
        return state, None

    def clear_rules(self, rule_type: str | None = None) -> None:
        """Clear all rules of a specific type, or all rules if type is None.

        Args:
            rule_type: Type of rules to clear, or None to clear all
        """
        if rule_type is None:
            for rtype in self.rules:
                self.rules[rtype] = []
        elif rule_type in self.rules:
            self.rules[rule_type] = []

    def rule_count(self, rule_type: str | None = None) -> int:
        """Count rules of a specific type, or all rules if type is None.

        Args:
            rule_type: Type of rules to count, or None for total count

        Returns:
            Number of rules
        """
        if rule_type is None:
            return sum(len(rules) for rules in self.rules.values())
        return len(self.rules.get(rule_type, []))

    def __str__(self) -> str:
        """Return string representation."""
        counts = {rtype: len(rules) for rtype, rules in self.rules.items()}
        return (
            f"RuleSet(interpretation={counts['interpretation']}, "
            f"integration={counts['integration']}, "
            f"selection={counts['selection']}, "
            f"generation={counts['generation']})"
        )
