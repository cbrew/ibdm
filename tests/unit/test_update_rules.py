"""Unit tests for UpdateRule and RuleSet classes."""

from ibdm.core import InformationState, WhQuestion
from ibdm.rules import RuleSet, UpdateRule


class TestUpdateRule:
    """Tests for UpdateRule class."""

    def test_creation(self):
        """Test creating an UpdateRule."""

        def precond(state: InformationState) -> bool:
            return True

        def effect(state: InformationState) -> InformationState:
            return state

        rule = UpdateRule(
            name="test_rule",
            preconditions=precond,
            effects=effect,
            priority=0,
            rule_type="integration",
        )

        assert rule.name == "test_rule"
        assert rule.preconditions == precond
        assert rule.effects == effect
        assert rule.priority == 0
        assert rule.rule_type == "integration"

    def test_default_values(self):
        """Test UpdateRule with default values."""

        def precond(state: InformationState) -> bool:
            return True

        def effect(state: InformationState) -> InformationState:
            return state

        rule = UpdateRule(name="test_rule", preconditions=precond, effects=effect)

        assert rule.priority == 0
        assert rule.rule_type == "integration"

    def test_applies_true(self):
        """Test applies method when preconditions are satisfied."""

        def precond(state: InformationState) -> bool:
            return len(state.shared.qud) > 0

        def effect(state: InformationState) -> InformationState:
            return state

        rule = UpdateRule(name="test_rule", preconditions=precond, effects=effect)

        state = InformationState()
        q = WhQuestion(variable="x", predicate="test(x)")
        state.shared.push_qud(q)

        assert rule.applies(state)

    def test_applies_false(self):
        """Test applies method when preconditions are not satisfied."""

        def precond(state: InformationState) -> bool:
            return len(state.shared.qud) > 0

        def effect(state: InformationState) -> InformationState:
            return state

        rule = UpdateRule(name="test_rule", preconditions=precond, effects=effect)

        state = InformationState()
        assert not rule.applies(state)

    def test_apply_modifies_state(self):
        """Test that apply method modifies the state correctly."""

        def precond(state: InformationState) -> bool:
            return True

        def effect(state: InformationState) -> InformationState:
            new_state = state.clone()
            new_state.private.beliefs["test"] = "value"
            return new_state

        rule = UpdateRule(name="test_rule", preconditions=precond, effects=effect)

        state = InformationState()
        new_state = rule.apply(state)

        assert "test" not in state.private.beliefs
        assert new_state.private.beliefs["test"] == "value"

    def test_apply_pushes_qud(self):
        """Test that apply can push to QUD stack."""

        def precond(state: InformationState) -> bool:
            return True

        def effect(state: InformationState) -> InformationState:
            new_state = state.clone()
            q = WhQuestion(variable="x", predicate="weather(x)")
            new_state.shared.push_qud(q)
            return new_state

        rule = UpdateRule(name="push_qud_rule", preconditions=precond, effects=effect)

        state = InformationState()
        assert len(state.shared.qud) == 0

        new_state = rule.apply(state)
        assert len(new_state.shared.qud) == 1

    def test_different_rule_types(self):
        """Test creating rules with different types."""

        def precond(state: InformationState) -> bool:
            return True

        def effect(state: InformationState) -> InformationState:
            return state

        for rule_type in ["interpretation", "integration", "selection", "generation"]:
            rule = UpdateRule(
                name=f"test_{rule_type}",
                preconditions=precond,
                effects=effect,
                rule_type=rule_type,
            )
            assert rule.rule_type == rule_type

    def test_str_representation(self):
        """Test string representation."""

        def precond(state: InformationState) -> bool:
            return True

        def effect(state: InformationState) -> InformationState:
            return state

        rule = UpdateRule(
            name="my_rule", preconditions=precond, effects=effect, priority=5, rule_type="selection"
        )

        s = str(rule)
        assert "my_rule" in s
        assert "selection" in s
        assert "5" in s


class TestRuleSet:
    """Tests for RuleSet class."""

    def test_creation(self):
        """Test creating an empty RuleSet."""
        ruleset = RuleSet()
        assert ruleset.rules["interpretation"] == []
        assert ruleset.rules["integration"] == []
        assert ruleset.rules["selection"] == []
        assert ruleset.rules["generation"] == []

    def test_add_rule(self):
        """Test adding a rule to the rule set."""

        def precond(state: InformationState) -> bool:
            return True

        def effect(state: InformationState) -> InformationState:
            return state

        ruleset = RuleSet()
        rule = UpdateRule(name="test_rule", preconditions=precond, effects=effect)

        ruleset.add_rule(rule)
        assert len(ruleset.rules["integration"]) == 1
        assert ruleset.rules["integration"][0] == rule

    def test_add_multiple_rules(self):
        """Test adding multiple rules."""

        def precond(state: InformationState) -> bool:
            return True

        def effect(state: InformationState) -> InformationState:
            return state

        ruleset = RuleSet()

        rule1 = UpdateRule(name="rule1", preconditions=precond, effects=effect)
        rule2 = UpdateRule(
            name="rule2", preconditions=precond, effects=effect, rule_type="selection"
        )
        rule3 = UpdateRule(name="rule3", preconditions=precond, effects=effect)

        ruleset.add_rule(rule1)
        ruleset.add_rule(rule2)
        ruleset.add_rule(rule3)

        assert len(ruleset.rules["integration"]) == 2
        assert len(ruleset.rules["selection"]) == 1

    def test_priority_ordering(self):
        """Test that rules are sorted by priority."""

        def precond(state: InformationState) -> bool:
            return True

        def effect(state: InformationState) -> InformationState:
            return state

        ruleset = RuleSet()

        rule_low = UpdateRule(name="low", preconditions=precond, effects=effect, priority=1)
        rule_high = UpdateRule(name="high", preconditions=precond, effects=effect, priority=10)
        rule_mid = UpdateRule(name="mid", preconditions=precond, effects=effect, priority=5)

        ruleset.add_rule(rule_low)
        ruleset.add_rule(rule_high)
        ruleset.add_rule(rule_mid)

        rules = ruleset.rules["integration"]
        assert rules[0].name == "high"
        assert rules[1].name == "mid"
        assert rules[2].name == "low"

    def test_get_rules(self):
        """Test getting rules by type."""

        def precond(state: InformationState) -> bool:
            return True

        def effect(state: InformationState) -> InformationState:
            return state

        ruleset = RuleSet()

        rule1 = UpdateRule(
            name="rule1", preconditions=precond, effects=effect, rule_type="integration"
        )
        rule2 = UpdateRule(
            name="rule2", preconditions=precond, effects=effect, rule_type="selection"
        )

        ruleset.add_rule(rule1)
        ruleset.add_rule(rule2)

        integration_rules = ruleset.get_rules("integration")
        selection_rules = ruleset.get_rules("selection")

        assert len(integration_rules) == 1
        assert len(selection_rules) == 1
        assert integration_rules[0].name == "rule1"
        assert selection_rules[0].name == "rule2"

    def test_remove_rule(self):
        """Test removing a rule."""

        def precond(state: InformationState) -> bool:
            return True

        def effect(state: InformationState) -> InformationState:
            return state

        ruleset = RuleSet()
        rule = UpdateRule(name="test_rule", preconditions=precond, effects=effect)

        ruleset.add_rule(rule)
        assert len(ruleset.rules["integration"]) == 1

        removed = ruleset.remove_rule("test_rule", "integration")
        assert removed
        assert len(ruleset.rules["integration"]) == 0

    def test_remove_rule_without_type(self):
        """Test removing a rule without specifying type."""

        def precond(state: InformationState) -> bool:
            return True

        def effect(state: InformationState) -> InformationState:
            return state

        ruleset = RuleSet()
        rule = UpdateRule(
            name="test_rule", preconditions=precond, effects=effect, rule_type="selection"
        )

        ruleset.add_rule(rule)
        removed = ruleset.remove_rule("test_rule")
        assert removed
        assert len(ruleset.rules["selection"]) == 0

    def test_remove_nonexistent_rule(self):
        """Test removing a rule that doesn't exist."""
        ruleset = RuleSet()
        removed = ruleset.remove_rule("nonexistent")
        assert not removed

    def test_apply_rules(self):
        """Test applying rules to a state."""

        def precond(state: InformationState) -> bool:
            return True

        def effect(state: InformationState) -> InformationState:
            new_state = state.clone()
            new_state.private.beliefs["applied"] = True
            return new_state

        ruleset = RuleSet()
        rule = UpdateRule(name="test_rule", preconditions=precond, effects=effect)
        ruleset.add_rule(rule)

        state = InformationState()
        new_state = ruleset.apply_rules("integration", state)

        assert "applied" not in state.private.beliefs
        assert new_state.private.beliefs["applied"] is True

    def test_apply_rules_with_preconditions(self):
        """Test that only rules with satisfied preconditions are applied."""

        def precond_false(state: InformationState) -> bool:
            return False

        def precond_true(state: InformationState) -> bool:
            return True

        def effect1(state: InformationState) -> InformationState:
            new_state = state.clone()
            new_state.private.beliefs["rule1"] = True
            return new_state

        def effect2(state: InformationState) -> InformationState:
            new_state = state.clone()
            new_state.private.beliefs["rule2"] = True
            return new_state

        ruleset = RuleSet()
        rule1 = UpdateRule(name="rule1", preconditions=precond_false, effects=effect1)
        rule2 = UpdateRule(name="rule2", preconditions=precond_true, effects=effect2)

        ruleset.add_rule(rule1)
        ruleset.add_rule(rule2)

        state = InformationState()
        new_state = ruleset.apply_rules("integration", state)

        assert "rule1" not in new_state.private.beliefs
        assert new_state.private.beliefs["rule2"] is True

    def test_apply_rules_sequentially(self):
        """Test that rules are applied sequentially."""

        def precond(state: InformationState) -> bool:
            return True

        def effect1(state: InformationState) -> InformationState:
            new_state = state.clone()
            new_state.private.beliefs["count"] = 1
            return new_state

        def effect2(state: InformationState) -> InformationState:
            new_state = state.clone()
            current = new_state.private.beliefs.get("count", 0)
            new_state.private.beliefs["count"] = current + 1
            return new_state

        ruleset = RuleSet()
        rule1 = UpdateRule(name="rule1", preconditions=precond, effects=effect1, priority=2)
        rule2 = UpdateRule(name="rule2", preconditions=precond, effects=effect2, priority=1)

        ruleset.add_rule(rule1)
        ruleset.add_rule(rule2)

        state = InformationState()
        new_state = ruleset.apply_rules("integration", state)

        # rule1 runs first (higher priority), sets count to 1
        # rule2 runs second, increments to 2
        assert new_state.private.beliefs["count"] == 2

    def test_apply_first_matching(self):
        """Test applying only the first matching rule."""

        def precond(state: InformationState) -> bool:
            return True

        def effect1(state: InformationState) -> InformationState:
            new_state = state.clone()
            new_state.private.beliefs["applied"] = "rule1"
            return new_state

        def effect2(state: InformationState) -> InformationState:
            new_state = state.clone()
            new_state.private.beliefs["applied"] = "rule2"
            return new_state

        ruleset = RuleSet()
        rule1 = UpdateRule(name="rule1", preconditions=precond, effects=effect1, priority=2)
        rule2 = UpdateRule(name="rule2", preconditions=precond, effects=effect2, priority=1)

        ruleset.add_rule(rule1)
        ruleset.add_rule(rule2)

        state = InformationState()
        new_state, applied_rule = ruleset.apply_first_matching("integration", state)

        # Only rule1 should be applied (higher priority)
        assert new_state.private.beliefs["applied"] == "rule1"
        assert applied_rule is not None
        assert applied_rule.name == "rule1"

    def test_apply_first_matching_no_match(self):
        """Test apply_first_matching when no rules match."""

        def precond(state: InformationState) -> bool:
            return False

        def effect(state: InformationState) -> InformationState:
            return state

        ruleset = RuleSet()
        rule = UpdateRule(name="rule", preconditions=precond, effects=effect)
        ruleset.add_rule(rule)

        state = InformationState()
        new_state, applied_rule = ruleset.apply_first_matching("integration", state)

        assert new_state == state
        assert applied_rule is None

    def test_clear_rules_specific_type(self):
        """Test clearing rules of a specific type."""

        def precond(state: InformationState) -> bool:
            return True

        def effect(state: InformationState) -> InformationState:
            return state

        ruleset = RuleSet()
        rule1 = UpdateRule(
            name="rule1", preconditions=precond, effects=effect, rule_type="integration"
        )
        rule2 = UpdateRule(
            name="rule2", preconditions=precond, effects=effect, rule_type="selection"
        )

        ruleset.add_rule(rule1)
        ruleset.add_rule(rule2)

        ruleset.clear_rules("integration")

        assert len(ruleset.rules["integration"]) == 0
        assert len(ruleset.rules["selection"]) == 1

    def test_clear_all_rules(self):
        """Test clearing all rules."""

        def precond(state: InformationState) -> bool:
            return True

        def effect(state: InformationState) -> InformationState:
            return state

        ruleset = RuleSet()
        rule1 = UpdateRule(
            name="rule1", preconditions=precond, effects=effect, rule_type="integration"
        )
        rule2 = UpdateRule(
            name="rule2", preconditions=precond, effects=effect, rule_type="selection"
        )

        ruleset.add_rule(rule1)
        ruleset.add_rule(rule2)

        ruleset.clear_rules()

        assert len(ruleset.rules["integration"]) == 0
        assert len(ruleset.rules["selection"]) == 0

    def test_rule_count_specific_type(self):
        """Test counting rules of a specific type."""

        def precond(state: InformationState) -> bool:
            return True

        def effect(state: InformationState) -> InformationState:
            return state

        ruleset = RuleSet()
        rule1 = UpdateRule(
            name="rule1", preconditions=precond, effects=effect, rule_type="integration"
        )
        rule2 = UpdateRule(
            name="rule2", preconditions=precond, effects=effect, rule_type="integration"
        )
        rule3 = UpdateRule(
            name="rule3", preconditions=precond, effects=effect, rule_type="selection"
        )

        ruleset.add_rule(rule1)
        ruleset.add_rule(rule2)
        ruleset.add_rule(rule3)

        assert ruleset.rule_count("integration") == 2
        assert ruleset.rule_count("selection") == 1

    def test_rule_count_all(self):
        """Test counting all rules."""

        def precond(state: InformationState) -> bool:
            return True

        def effect(state: InformationState) -> InformationState:
            return state

        ruleset = RuleSet()
        rule1 = UpdateRule(
            name="rule1", preconditions=precond, effects=effect, rule_type="integration"
        )
        rule2 = UpdateRule(
            name="rule2", preconditions=precond, effects=effect, rule_type="selection"
        )

        ruleset.add_rule(rule1)
        ruleset.add_rule(rule2)

        assert ruleset.rule_count() == 2

    def test_str_representation(self):
        """Test string representation."""

        def precond(state: InformationState) -> bool:
            return True

        def effect(state: InformationState) -> InformationState:
            return state

        ruleset = RuleSet()
        rule1 = UpdateRule(
            name="rule1", preconditions=precond, effects=effect, rule_type="integration"
        )
        rule2 = UpdateRule(
            name="rule2", preconditions=precond, effects=effect, rule_type="selection"
        )

        ruleset.add_rule(rule1)
        ruleset.add_rule(rule2)

        s = str(ruleset)
        assert "RuleSet" in s
        assert "integration=1" in s
        assert "selection=1" in s
