"""Tests for unified scenario loader."""


import pytest

from ibdm.demo.scenario_loader import (
    Scenario,
    ScenarioLoader,
    ScenarioMetadata,
    ScenarioTurn,
    get_loader,
    list_scenarios,
    list_scenarios_by_category,
    load_scenario,
    search_scenarios,
)


@pytest.fixture
def loader():
    """Create scenario loader for testing."""
    return ScenarioLoader()


def test_loader_initialization(loader):
    """Test scenario loader initializes correctly."""
    assert loader.scenarios_dir.exists()
    assert loader.scenarios_dir.is_dir()
    assert loader.scenarios_dir.name == "scenarios"


def test_list_scenarios(loader):
    """Test listing all scenarios."""
    scenarios = loader.list_scenarios()

    assert isinstance(scenarios, list)
    assert len(scenarios) > 0
    assert all(isinstance(s, str) for s in scenarios)

    # Should be sorted
    assert scenarios == sorted(scenarios)

    # Check some expected scenarios exist
    expected_scenarios = [
        "nda_basic",
        "ibis3_incremental_questioning",
        "ibis2_grounding_optimistic",
    ]
    for expected in expected_scenarios:
        assert expected in scenarios, f"Expected scenario '{expected}' not found"


def test_list_scenarios_by_category(loader):
    """Test listing scenarios grouped by category."""
    categories = loader.list_scenarios_by_category()

    assert isinstance(categories, dict)
    assert len(categories) > 0

    # Check expected categories
    assert "IBiS-3 (Question Accommodation)" in categories
    assert "IBiS-2 (Grounding)" in categories
    assert "Business Demos" in categories

    # Check IBiS-3 scenarios
    ibis3 = categories["IBiS-3 (Question Accommodation)"]
    assert "ibis3_incremental_questioning" in ibis3
    assert "ibis3_volunteer_information" in ibis3
    assert "ibis3_clarification" in ibis3
    assert "ibis3_dependent_questions" in ibis3
    assert "ibis3_reaccommodation" in ibis3

    # Check IBiS-2 scenarios
    ibis2 = categories["IBiS-2 (Grounding)"]
    assert "ibis2_grounding_optimistic" in ibis2
    assert "ibis2_grounding_cautious" in ibis2
    assert "ibis2_grounding_pessimistic" in ibis2
    assert "ibis2_grounding_mixed" in ibis2

    # Check business demos
    business = categories["Business Demos"]
    assert "nda_basic" in business


def test_load_scenario_basic(loader):
    """Test loading a basic scenario."""
    scenario = loader.load_scenario("nda_basic")

    assert isinstance(scenario, Scenario)
    assert scenario.scenario_id == "nda_basic"
    assert scenario.title
    assert len(scenario.turns) > 0


def test_load_scenario_metadata(loader):
    """Test scenario metadata is loaded correctly."""
    scenario = loader.load_scenario("ibis3_incremental_questioning")

    metadata = scenario.metadata
    assert isinstance(metadata, ScenarioMetadata)
    assert metadata.scenario_id == "ibis3_incremental_questioning"
    assert metadata.title == "Incremental Questioning"
    assert metadata.description
    assert metadata.business_narrative
    assert len(metadata.larsson_algorithms) > 0
    assert metadata.expected_outcomes
    assert metadata.confidence_mode


def test_load_scenario_turns(loader):
    """Test scenario turns are loaded correctly."""
    scenario = loader.load_scenario("ibis3_incremental_questioning")

    assert len(scenario.turns) > 0

    # Check first turn
    first_turn = scenario.turns[0]
    assert isinstance(first_turn, ScenarioTurn)
    assert first_turn.turn == 1
    assert first_turn.speaker in ["user", "system"]
    assert first_turn.utterance
    assert first_turn.move_type
    assert first_turn.business_explanation
    assert first_turn.larsson_rule
    assert isinstance(first_turn.state_changes, dict)


def test_load_nonexistent_scenario(loader):
    """Test loading nonexistent scenario raises error."""
    with pytest.raises(FileNotFoundError) as exc_info:
        loader.load_scenario("nonexistent_scenario")

    assert "not found" in str(exc_info.value).lower()
    assert "available scenarios" in str(exc_info.value).lower()


def test_scenario_properties(loader):
    """Test Scenario property methods."""
    scenario = loader.load_scenario("ibis3_incremental_questioning")

    # Test total_turns
    assert scenario.total_turns == len(scenario.turns)
    assert scenario.total_turns > 0

    # Test user_turns
    user_turns = scenario.user_turns
    assert all(t.speaker == "user" for t in user_turns)
    assert len(user_turns) > 0

    # Test system_turns
    system_turns = scenario.system_turns
    assert all(t.speaker == "system" for t in system_turns)
    assert len(system_turns) > 0

    # Test get_turn
    first_turn = scenario.get_turn(1)
    assert first_turn is not None
    assert first_turn.turn == 1

    # Test nonexistent turn
    assert scenario.get_turn(9999) is None


def test_scenario_payoff_turns(loader):
    """Test payoff turn detection."""
    # Load scenario with payoff turn
    scenario = loader.load_scenario("ibis3_incremental_questioning")

    payoff_turns = scenario.payoff_turns

    # Should have at least one payoff turn
    assert len(payoff_turns) > 0
    assert all(t.is_payoff for t in payoff_turns)


def test_search_scenarios(loader):
    """Test scenario search functionality."""
    # Search for "incremental"
    results = loader.search_scenarios("incremental")
    assert "ibis3_incremental_questioning" in results

    # Search for "grounding"
    results = loader.search_scenarios("grounding")
    assert len(results) >= 4  # At least 4 grounding scenarios

    # Search for "NDA"
    results = loader.search_scenarios("nda")
    assert "nda_basic" in results

    # Search for "Larsson" (should find scenarios mentioning Larsson rules)
    results = loader.search_scenarios("larsson")
    assert len(results) > 0

    # Case insensitive
    assert loader.search_scenarios("INCREMENTAL") == loader.search_scenarios("incremental")


def test_validate_scenario(loader):
    """Test scenario validation."""
    # Validate a known good scenario
    is_valid, issues = loader.validate_scenario("nda_basic")

    # Should be valid or have only warnings
    assert is_valid or all("Warning" in issue for issue in issues)


def test_all_scenarios_load(loader):
    """Test that all scenarios can be loaded without errors."""
    scenarios = loader.list_scenarios()

    for scenario_id in scenarios:
        try:
            scenario = loader.load_scenario(scenario_id)
            assert scenario.scenario_id == scenario_id
            assert len(scenario.turns) > 0
        except Exception as e:
            pytest.fail(f"Failed to load scenario '{scenario_id}': {e}")


def test_all_scenarios_have_metadata(loader):
    """Test that all scenarios have required metadata."""
    scenarios = loader.list_scenarios()

    for scenario_id in scenarios:
        scenario = loader.load_scenario(scenario_id)

        assert scenario.metadata.title
        assert scenario.metadata.description
        assert scenario.metadata.business_narrative
        assert len(scenario.metadata.larsson_algorithms) > 0
        assert scenario.metadata.expected_outcomes


def test_all_scenarios_have_turns(loader):
    """Test that all scenarios have properly formatted turns."""
    scenarios = loader.list_scenarios()

    for scenario_id in scenarios:
        scenario = loader.load_scenario(scenario_id)

        # Should have at least one turn
        assert len(scenario.turns) > 0

        # Turns should be numbered sequentially starting from 1
        for idx, turn in enumerate(scenario.turns, start=1):
            assert turn.turn == idx, f"Scenario '{scenario_id}' turn {idx} has wrong number"

        # Should have at least one user turn and one system turn
        assert len(scenario.user_turns) > 0, f"Scenario '{scenario_id}' has no user turns"
        assert len(scenario.system_turns) > 0, f"Scenario '{scenario_id}' has no system turns"


def test_global_functions():
    """Test global convenience functions."""
    # Test list_scenarios
    scenarios = list_scenarios()
    assert isinstance(scenarios, list)
    assert len(scenarios) > 0

    # Test list_scenarios_by_category
    categories = list_scenarios_by_category()
    assert isinstance(categories, dict)
    assert len(categories) > 0

    # Test load_scenario
    scenario = load_scenario("nda_basic")
    assert isinstance(scenario, Scenario)
    assert scenario.scenario_id == "nda_basic"

    # Test search_scenarios
    results = search_scenarios("nda")
    assert isinstance(results, list)
    assert len(results) > 0

    # Test get_loader
    loader = get_loader()
    assert isinstance(loader, ScenarioLoader)


def test_scenario_count():
    """Test that we have expected number of scenarios."""
    scenarios = list_scenarios()

    # We should have at least 15 scenarios:
    # - 5 IBiS-3 scenarios
    # - 4 IBiS-2 scenarios
    # - 6 business demos
    assert len(scenarios) >= 15, f"Expected at least 15 scenarios, found {len(scenarios)}"


def test_ibis3_scenarios_complete():
    """Test that all IBiS-3 scenarios are present."""
    categories = list_scenarios_by_category()
    ibis3 = categories.get("IBiS-3 (Question Accommodation)", [])

    expected = [
        "ibis3_incremental_questioning",
        "ibis3_volunteer_information",
        "ibis3_clarification",
        "ibis3_dependent_questions",
        "ibis3_reaccommodation",
    ]

    for scenario_id in expected:
        assert scenario_id in ibis3, f"Expected IBiS-3 scenario '{scenario_id}' not found"


def test_ibis2_scenarios_complete():
    """Test that all IBiS-2 scenarios are present."""
    categories = list_scenarios_by_category()
    ibis2 = categories.get("IBiS-2 (Grounding)", [])

    expected = [
        "ibis2_grounding_optimistic",
        "ibis2_grounding_cautious",
        "ibis2_grounding_pessimistic",
        "ibis2_grounding_mixed",
    ]

    for scenario_id in expected:
        assert scenario_id in ibis2, f"Expected IBiS-2 scenario '{scenario_id}' not found"
