"""Tests for demo scenarios module."""

from __future__ import annotations

from ibdm.demo.scenarios import (
    ALL_SCENARIOS,
    DemoScenario,
    ScenarioStep,
    get_ibis2_scenarios,
    get_ibis3_scenarios,
    get_scenario,
    list_scenarios,
    scenario_clarification,
    scenario_dependent_questions,
    scenario_grounding_cautious,
    scenario_grounding_mixed,
    scenario_grounding_optimistic,
    scenario_grounding_pessimistic,
    scenario_incremental_questioning,
    scenario_reaccommodation,
    scenario_volunteer_information,
)


class TestScenarioStep:
    """Test ScenarioStep dataclass."""

    def test_creation_basic(self) -> None:
        """Test basic ScenarioStep creation."""
        step = ScenarioStep(speaker="user", utterance="Hello")

        assert step.speaker == "user"
        assert step.utterance == "Hello"
        assert step.description is None
        assert step.expected_state is None

    def test_creation_full(self) -> None:
        """Test full ScenarioStep creation."""
        step = ScenarioStep(
            speaker="user",
            utterance="Hello",
            description="User greets system",
            expected_state={"qud_depth": 0},
        )

        assert step.speaker == "user"
        assert step.utterance == "Hello"
        assert step.description == "User greets system"
        assert step.expected_state == {"qud_depth": 0}


class TestDemoScenario:
    """Test DemoScenario dataclass."""

    def test_creation_basic(self) -> None:
        """Test basic DemoScenario creation."""
        steps = [
            ScenarioStep("user", "Hello"),
            ScenarioStep("system", "Hi there"),
        ]

        scenario = DemoScenario(
            name="Test Scenario",
            description="A test scenario",
            features=["feature1", "feature2"],
            steps=steps,
        )

        assert scenario.name == "Test Scenario"
        assert scenario.description == "A test scenario"
        assert scenario.features == ["feature1", "feature2"]
        assert len(scenario.steps) == 2
        assert scenario.confidence_mode == "heuristic"  # Default

    def test_creation_with_confidence_mode(self) -> None:
        """Test DemoScenario with custom confidence mode."""
        scenario = DemoScenario(
            name="Test",
            description="Test",
            features=[],
            steps=[],
            confidence_mode="optimistic",
        )

        assert scenario.confidence_mode == "optimistic"


class TestIBiS3Scenarios:
    """Test IBiS3 scenario functions."""

    def test_scenario_incremental_questioning(self) -> None:
        """Test incremental questioning scenario."""
        scenario = scenario_incremental_questioning()

        assert scenario.name == "Incremental Questioning"
        assert "Rule 4.2" in scenario.features[0]
        assert len(scenario.steps) > 0
        assert scenario.confidence_mode == "optimistic"

        # Check scenario structure
        assert any("I need to draft an NDA" in step.utterance for step in scenario.steps)
        assert any(step.speaker == "system" for step in scenario.steps)

    def test_scenario_volunteer_information(self) -> None:
        """Test volunteer information scenario."""
        scenario = scenario_volunteer_information()

        assert scenario.name == "Volunteer Information"
        assert "Volunteer information integration" in scenario.features
        assert len(scenario.steps) > 0

        # Check for volunteer info step
        volunteer_steps = [s for s in scenario.steps if "effective January 1, 2025" in s.utterance]
        assert len(volunteer_steps) > 0

    def test_scenario_clarification(self) -> None:
        """Test clarification scenario."""
        scenario = scenario_clarification()

        assert scenario.name == "Clarification Questions"
        assert "Rule 4.3" in scenario.features[0]
        assert len(scenario.steps) > 0

        # Check for invalid answer and clarification
        invalid_answer = [s for s in scenario.steps if s.utterance == "blue"]
        assert len(invalid_answer) > 0

        clarification = [s for s in scenario.steps if "valid parties" in s.utterance]
        assert len(clarification) > 0

    def test_scenario_dependent_questions(self) -> None:
        """Test dependent questions scenario."""
        scenario = scenario_dependent_questions()

        assert scenario.name == "Dependent Questions"
        assert "Rule 4.4" in scenario.features[0]
        assert len(scenario.steps) > 0

        # Check for dependency structure
        assert any("departure city" in step.utterance for step in scenario.steps)
        assert any("price" in step.utterance for step in scenario.steps)

    def test_scenario_reaccommodation(self) -> None:
        """Test reaccommodation scenario."""
        scenario = scenario_reaccommodation()

        assert scenario.name == "Belief Revision (Reaccommodation)"
        assert "Rule 4.6" in scenario.features[0]
        assert len(scenario.steps) > 0

        # Check for changed answer
        changed_answer = [s for s in scenario.steps if "Actually" in s.utterance]
        assert len(changed_answer) > 0


class TestIBiS2Scenarios:
    """Test IBiS2 scenario functions."""

    def test_scenario_grounding_optimistic(self) -> None:
        """Test optimistic grounding scenario."""
        scenario = scenario_grounding_optimistic()

        assert scenario.name == "Optimistic Grounding"
        assert scenario.confidence_mode == "optimistic"
        assert "icm:acc*pos" in scenario.features
        assert len(scenario.steps) > 0

    def test_scenario_grounding_cautious(self) -> None:
        """Test cautious grounding scenario."""
        scenario = scenario_grounding_cautious()

        assert scenario.name == "Cautious Grounding"
        assert scenario.confidence_mode == "cautious"
        assert "icm:und*int" in scenario.features
        assert len(scenario.steps) > 0

        # Check for confirmation request
        confirmation = [s for s in scenario.steps if "icm:und*int" in s.utterance]
        assert len(confirmation) > 0

    def test_scenario_grounding_pessimistic(self) -> None:
        """Test pessimistic grounding scenario."""
        scenario = scenario_grounding_pessimistic()

        assert scenario.name == "Pessimistic Grounding"
        assert scenario.confidence_mode == "pessimistic"
        assert "icm:per*neg" in scenario.features
        assert len(scenario.steps) > 0

        # Check for repetition request
        repetition = [s for s in scenario.steps if "icm:per*neg" in s.utterance]
        assert len(repetition) > 0

    def test_scenario_grounding_mixed(self) -> None:
        """Test mixed grounding scenario."""
        scenario = scenario_grounding_mixed()

        assert scenario.name == "Mixed Grounding Strategies"
        assert scenario.confidence_mode == "random"
        assert len(scenario.steps) > 0


class TestScenarioRegistry:
    """Test scenario registry functions."""

    def test_get_scenario_valid(self) -> None:
        """Test getting a valid scenario."""
        scenario = get_scenario("incremental")

        assert scenario is not None
        assert scenario.name == "Incremental Questioning"

    def test_get_scenario_invalid(self) -> None:
        """Test getting invalid scenario returns None."""
        scenario = get_scenario("nonexistent")

        assert scenario is None

    def test_list_scenarios(self) -> None:
        """Test listing all scenario names."""
        scenarios = list_scenarios()

        assert "incremental" in scenarios
        assert "volunteer" in scenarios
        assert "clarification" in scenarios
        assert "dependent" in scenarios
        assert "reaccommodation" in scenarios
        assert "grounding-optimistic" in scenarios
        assert "grounding-cautious" in scenarios
        assert "grounding-pessimistic" in scenarios
        assert "grounding-mixed" in scenarios

    def test_get_ibis3_scenarios(self) -> None:
        """Test getting IBiS3 scenarios."""
        scenarios = get_ibis3_scenarios()

        assert len(scenarios) == 5
        names = [s.name for s in scenarios]

        assert "Incremental Questioning" in names
        assert "Volunteer Information" in names
        assert "Clarification Questions" in names
        assert "Dependent Questions" in names
        assert "Belief Revision (Reaccommodation)" in names

    def test_get_ibis2_scenarios(self) -> None:
        """Test getting IBiS2 scenarios."""
        scenarios = get_ibis2_scenarios()

        assert len(scenarios) == 4
        names = [s.name for s in scenarios]

        assert "Optimistic Grounding" in names
        assert "Cautious Grounding" in names
        assert "Pessimistic Grounding" in names
        assert "Mixed Grounding Strategies" in names

    def test_all_scenarios_registry(self) -> None:
        """Test ALL_SCENARIOS registry."""
        assert len(ALL_SCENARIOS) == 9  # 5 IBiS3 + 4 IBiS2

        # Check all scenarios are accessible
        for name in ALL_SCENARIOS:
            scenario = ALL_SCENARIOS[name]
            assert isinstance(scenario, DemoScenario)
            assert scenario.name
            assert scenario.description
            assert len(scenario.steps) > 0


class TestScenarioContent:
    """Test scenario content quality."""

    def test_all_scenarios_have_steps(self) -> None:
        """Test all scenarios have at least one step."""
        for name, scenario in ALL_SCENARIOS.items():
            assert len(scenario.steps) > 0, f"Scenario {name} has no steps"

    def test_all_scenarios_have_features(self) -> None:
        """Test all scenarios have at least one feature."""
        for name, scenario in ALL_SCENARIOS.items():
            assert len(scenario.features) > 0, f"Scenario {name} has no features"

    def test_all_scenarios_have_descriptions(self) -> None:
        """Test all scenarios have descriptions."""
        for name, scenario in ALL_SCENARIOS.items():
            assert scenario.description, f"Scenario {name} has no description"

    def test_ibis3_scenarios_mention_rules(self) -> None:
        """Test IBiS3 scenarios mention specific rules."""
        ibis3 = get_ibis3_scenarios()

        for scenario in ibis3:
            # Each IBiS3 scenario should reference at least one rule
            features_str = " ".join(scenario.features)
            assert "Rule" in features_str, f"Scenario {scenario.name} doesn't mention rules"

    def test_ibis2_scenarios_mention_grounding(self) -> None:
        """Test IBiS2 scenarios mention grounding."""
        ibis2 = get_ibis2_scenarios()

        for scenario in ibis2:
            # Each IBiS2 scenario should reference grounding
            features_str = " ".join(scenario.features)
            description_lower = scenario.description.lower()

            assert "grounding" in features_str.lower() or "grounding" in description_lower, (
                f"Scenario {scenario.name} doesn't mention grounding"
            )

    def test_scenarios_alternate_speakers(self) -> None:
        """Test scenarios alternate between user and system."""
        for name, scenario in ALL_SCENARIOS.items():
            if len(scenario.steps) < 2:
                continue

            # Most scenarios should have both user and system turns
            speakers = {step.speaker for step in scenario.steps}
            assert "user" in speakers, f"Scenario {name} has no user turns"
            assert "system" in speakers, f"Scenario {name} has no system turns"

    def test_scenario_confidence_modes_valid(self) -> None:
        """Test all scenarios use valid confidence modes."""
        valid_modes = {"heuristic", "random", "optimistic", "cautious", "pessimistic"}

        for name, scenario in ALL_SCENARIOS.items():
            assert scenario.confidence_mode in valid_modes, (
                f"Scenario {name} has invalid confidence mode: {scenario.confidence_mode}"
            )
