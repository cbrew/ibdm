"""Tests for scenario runner."""

from __future__ import annotations

from io import StringIO
from unittest.mock import Mock, patch

import pytest
from rich.console import Console

from ibdm.demo.execution_controller import ExecutionController, ExecutionMode
from ibdm.demo.scenario_loader import Scenario, ScenarioMetadata, ScenarioTurn
from ibdm.demo.scenario_runner import ScenarioRunner, run_scenario


@pytest.fixture
def minimal_scenario() -> Scenario:
    """Create minimal test scenario."""
    metadata = ScenarioMetadata(
        scenario_id="test_minimal",
        title="Test Minimal Scenario",
        description="A minimal test scenario",
        business_narrative="Tests basic functionality",
        larsson_algorithms=["Algorithm 1", "Algorithm 2"],
        expected_outcomes={"turns": 2, "qud_depth_max": 1},
        confidence_mode="heuristic",
        metrics={"efficiency": "100%"},
    )

    turns = [
        ScenarioTurn(
            turn=1,
            speaker="user",
            utterance="Hello",
            move_type="greet",
            business_explanation="User initiates conversation",
            larsson_rule="Greeting rule",
            state_changes={"greeting": "received"},
            is_payoff=False,
        ),
        ScenarioTurn(
            turn=2,
            speaker="system",
            utterance="Hi there!",
            move_type="greet",
            business_explanation="System responds",
            larsson_rule="Greeting response",
            state_changes={"greeting": "sent"},
            is_payoff=True,
        ),
    ]

    return Scenario(metadata=metadata, turns=turns)


@pytest.fixture
def mock_controller() -> Mock:
    """Create mock execution controller."""
    controller = Mock(spec=ExecutionController)
    controller.mode = ExecutionMode.REPLAY
    controller.wait_at_banner = Mock()
    controller.wait_between_turns = Mock()
    controller.wait_at_end = Mock()
    return controller


class TestScenarioRunner:
    """Test ScenarioRunner class."""

    def test_init_with_defaults(self, minimal_scenario: Scenario) -> None:
        """Test runner initialization with default parameters."""
        runner = ScenarioRunner(minimal_scenario)

        assert runner.scenario == minimal_scenario
        assert runner.controller is not None
        assert runner.console is not None
        assert runner.show_explanations is True
        assert runner.show_state_changes is True
        assert runner.show_larsson_rules is True
        assert runner.show_metrics is True

    def test_init_with_custom_controller(
        self, minimal_scenario: Scenario, mock_controller: Mock
    ) -> None:
        """Test runner initialization with custom controller."""
        runner = ScenarioRunner(minimal_scenario, controller=mock_controller)

        assert runner.controller == mock_controller

    def test_init_with_custom_console(self, minimal_scenario: Scenario) -> None:
        """Test runner initialization with custom console."""
        custom_console = Console(file=StringIO(), width=80)
        runner = ScenarioRunner(minimal_scenario, console=custom_console)

        assert runner.console == custom_console

    def test_init_with_display_options(self, minimal_scenario: Scenario) -> None:
        """Test runner initialization with custom display options."""
        runner = ScenarioRunner(
            minimal_scenario,
            show_explanations=False,
            show_state_changes=False,
            show_larsson_rules=False,
            show_metrics=False,
        )

        assert runner.show_explanations is False
        assert runner.show_state_changes is False
        assert runner.show_larsson_rules is False
        assert runner.show_metrics is False

    def test_run_calls_controller_methods(
        self, minimal_scenario: Scenario, mock_controller: Mock
    ) -> None:
        """Test that run() calls controller wait methods correctly."""
        output = StringIO()
        console = Console(file=output, width=80, force_terminal=True)
        runner = ScenarioRunner(minimal_scenario, controller=mock_controller, console=console)

        runner.run()

        # Verify controller methods were called
        mock_controller.wait_at_banner.assert_called_once()
        assert mock_controller.wait_between_turns.call_count == 2  # One per turn
        mock_controller.wait_at_end.assert_called_once()

    def test_run_displays_banner(self, minimal_scenario: Scenario, mock_controller: Mock) -> None:
        """Test that run() displays banner with scenario metadata."""
        output = StringIO()
        console = Console(file=output, width=80, force_terminal=True)
        runner = ScenarioRunner(minimal_scenario, controller=mock_controller, console=console)

        runner.run()
        output_text = output.getvalue()

        # Check that key metadata is displayed
        assert "Test Minimal Scenario" in output_text
        assert "A minimal test scenario" in output_text
        assert "Tests basic functionality" in output_text
        # Algorithm text may be formatted with ANSI codes, just check "Algorithm"
        assert "Algorithm" in output_text

    def test_run_displays_all_turns(
        self, minimal_scenario: Scenario, mock_controller: Mock
    ) -> None:
        """Test that run() displays all turns in sequence."""
        output = StringIO()
        console = Console(file=output, width=80, force_terminal=True)
        runner = ScenarioRunner(minimal_scenario, controller=mock_controller, console=console)

        runner.run()
        output_text = output.getvalue()

        # Check that both turns are displayed
        assert "Hello" in output_text
        assert "Hi there!" in output_text
        assert "USER" in output_text
        assert "SYSTEM" in output_text

    def test_run_displays_explanations(
        self, minimal_scenario: Scenario, mock_controller: Mock
    ) -> None:
        """Test that business explanations are displayed when enabled."""
        output = StringIO()
        console = Console(file=output, width=80, force_terminal=True)
        runner = ScenarioRunner(
            minimal_scenario,
            controller=mock_controller,
            console=console,
            show_explanations=True,
        )

        runner.run()
        output_text = output.getvalue()

        assert "User initiates conversation" in output_text
        assert "System responds" in output_text

    def test_run_hides_explanations(
        self, minimal_scenario: Scenario, mock_controller: Mock
    ) -> None:
        """Test that business explanations are hidden when disabled."""
        output = StringIO()
        console = Console(file=output, width=80, force_terminal=True)
        runner = ScenarioRunner(
            minimal_scenario,
            controller=mock_controller,
            console=console,
            show_explanations=False,
        )

        runner.run()
        output_text = output.getvalue()

        assert "User initiates conversation" not in output_text
        assert "System responds" not in output_text

    def test_run_displays_larsson_rules(
        self, minimal_scenario: Scenario, mock_controller: Mock
    ) -> None:
        """Test that Larsson rules are displayed when enabled."""
        output = StringIO()
        console = Console(file=output, width=80, force_terminal=True)
        runner = ScenarioRunner(
            minimal_scenario,
            controller=mock_controller,
            console=console,
            show_larsson_rules=True,
        )

        runner.run()
        output_text = output.getvalue()

        assert "Greeting rule" in output_text
        assert "Greeting response" in output_text

    def test_run_hides_larsson_rules(
        self, minimal_scenario: Scenario, mock_controller: Mock
    ) -> None:
        """Test that Larsson rules are hidden when disabled."""
        output = StringIO()
        console = Console(file=output, width=80, force_terminal=True)
        runner = ScenarioRunner(
            minimal_scenario,
            controller=mock_controller,
            console=console,
            show_larsson_rules=False,
        )

        runner.run()
        output_text = output.getvalue()

        assert "Greeting rule" not in output_text
        assert "Greeting response" not in output_text

    def test_run_displays_state_changes(
        self, minimal_scenario: Scenario, mock_controller: Mock
    ) -> None:
        """Test that state changes are displayed when enabled."""
        output = StringIO()
        console = Console(file=output, width=80, force_terminal=True)
        runner = ScenarioRunner(
            minimal_scenario,
            controller=mock_controller,
            console=console,
            show_state_changes=True,
        )

        runner.run()
        output_text = output.getvalue()

        assert "State Changes" in output_text
        assert "received" in output_text
        assert "sent" in output_text

    def test_run_hides_state_changes(
        self, minimal_scenario: Scenario, mock_controller: Mock
    ) -> None:
        """Test that state changes are hidden when disabled."""
        output = StringIO()
        console = Console(file=output, width=80, force_terminal=True)
        runner = ScenarioRunner(
            minimal_scenario,
            controller=mock_controller,
            console=console,
            show_state_changes=False,
        )

        runner.run()
        output_text = output.getvalue()

        assert "State Changes" not in output_text

    def test_run_displays_payoff_indicator(
        self, minimal_scenario: Scenario, mock_controller: Mock
    ) -> None:
        """Test that payoff turns are marked with indicator."""
        output = StringIO()
        console = Console(file=output, width=80, force_terminal=True)
        runner = ScenarioRunner(minimal_scenario, controller=mock_controller, console=console)

        runner.run()
        output_text = output.getvalue()

        # Second turn is marked as payoff
        assert "High-Value Output" in output_text

    def test_run_displays_summary(self, minimal_scenario: Scenario, mock_controller: Mock) -> None:
        """Test that summary with statistics is displayed."""
        output = StringIO()
        console = Console(file=output, width=80, force_terminal=True)
        runner = ScenarioRunner(minimal_scenario, controller=mock_controller, console=console)

        runner.run()
        output_text = output.getvalue()

        assert "Scenario Complete" in output_text
        assert "Total Turns" in output_text
        assert "2" in output_text  # Total turns count

    def test_run_displays_metrics(self, minimal_scenario: Scenario, mock_controller: Mock) -> None:
        """Test that quality metrics are displayed when enabled."""
        output = StringIO()
        console = Console(file=output, width=80, force_terminal=True)
        runner = ScenarioRunner(
            minimal_scenario,
            controller=mock_controller,
            console=console,
            show_metrics=True,
        )

        runner.run()
        output_text = output.getvalue()

        assert "Quality Metrics" in output_text
        # Check for "100" which appears in "100%", may be formatted with ANSI codes
        assert "100" in output_text
        assert "%" in output_text

    def test_run_hides_metrics(self, minimal_scenario: Scenario, mock_controller: Mock) -> None:
        """Test that quality metrics are hidden when disabled."""
        output = StringIO()
        console = Console(file=output, width=80, force_terminal=True)
        runner = ScenarioRunner(
            minimal_scenario,
            controller=mock_controller,
            console=console,
            show_metrics=False,
        )

        runner.run()
        output_text = output.getvalue()

        assert "Quality Metrics" not in output_text

    def test_different_execution_modes(self, minimal_scenario: Scenario) -> None:
        """Test runner works with different execution modes."""
        for mode in [ExecutionMode.STEP, ExecutionMode.AUTO, ExecutionMode.REPLAY]:
            controller = ExecutionController(mode=mode)
            output = StringIO()
            console = Console(file=output, width=80, force_terminal=True)

            # Mock the wait methods to avoid blocking
            with (
                patch.object(controller, "wait_at_banner"),
                patch.object(controller, "wait_between_turns"),
                patch.object(controller, "wait_at_end"),
            ):
                runner = ScenarioRunner(minimal_scenario, controller=controller, console=console)
                runner.run()

            output_text = output.getvalue()
            assert len(output_text) > 0  # Should produce output


class TestRunScenarioFunction:
    """Test run_scenario convenience function."""

    @patch("ibdm.demo.scenario_runner.ScenarioLoader")
    @patch("ibdm.demo.scenario_runner.ExecutionController")
    @patch("ibdm.demo.scenario_runner.ScenarioRunner")
    def test_run_scenario_creates_components(
        self,
        mock_runner_class: Mock,
        mock_controller_class: Mock,
        mock_loader_class: Mock,
        minimal_scenario: Scenario,
    ) -> None:
        """Test that run_scenario creates all necessary components."""
        # Setup mocks
        mock_loader = Mock()
        mock_loader.load_scenario.return_value = minimal_scenario
        mock_loader_class.return_value = mock_loader

        mock_controller = Mock()
        mock_controller_class.return_value = mock_controller

        mock_runner = Mock()
        mock_runner_class.return_value = mock_runner

        # Call function
        run_scenario("test_scenario")

        # Verify component creation
        mock_loader_class.assert_called_once()
        mock_loader.load_scenario.assert_called_once_with("test_scenario")
        mock_controller_class.assert_called_once()
        mock_runner_class.assert_called_once()
        mock_runner.run.assert_called_once()

    @patch("ibdm.demo.scenario_runner.ScenarioLoader")
    @patch("ibdm.demo.scenario_runner.ExecutionController")
    @patch("ibdm.demo.scenario_runner.ScenarioRunner")
    def test_run_scenario_with_custom_mode(
        self,
        mock_runner_class: Mock,
        mock_controller_class: Mock,
        mock_loader_class: Mock,
        minimal_scenario: Scenario,
    ) -> None:
        """Test run_scenario with custom execution mode."""
        mock_loader = Mock()
        mock_loader.load_scenario.return_value = minimal_scenario
        mock_loader_class.return_value = mock_loader

        run_scenario("test_scenario", mode=ExecutionMode.STEP)

        # Verify controller was created with correct mode
        call_args = mock_controller_class.call_args
        assert call_args[1]["mode"] == ExecutionMode.STEP

    @patch("ibdm.demo.scenario_runner.ScenarioLoader")
    @patch("ibdm.demo.scenario_runner.ExecutionController")
    @patch("ibdm.demo.scenario_runner.ScenarioRunner")
    def test_run_scenario_with_custom_delay(
        self,
        mock_runner_class: Mock,
        mock_controller_class: Mock,
        mock_loader_class: Mock,
        minimal_scenario: Scenario,
    ) -> None:
        """Test run_scenario with custom auto delay."""
        mock_loader = Mock()
        mock_loader.load_scenario.return_value = minimal_scenario
        mock_loader_class.return_value = mock_loader

        run_scenario("test_scenario", auto_delay=1.5)

        # Verify controller was created with correct delay
        call_args = mock_controller_class.call_args
        assert call_args[1]["auto_delay"] == 1.5

    @patch("ibdm.demo.scenario_runner.ScenarioLoader")
    @patch("ibdm.demo.scenario_runner.ExecutionController")
    @patch("ibdm.demo.scenario_runner.ScenarioRunner")
    def test_run_scenario_with_display_options(
        self,
        mock_runner_class: Mock,
        mock_controller_class: Mock,
        mock_loader_class: Mock,
        minimal_scenario: Scenario,
    ) -> None:
        """Test run_scenario with custom display options."""
        mock_loader = Mock()
        mock_loader.load_scenario.return_value = minimal_scenario
        mock_loader_class.return_value = mock_loader

        run_scenario(
            "test_scenario",
            show_explanations=False,
            show_state_changes=False,
            show_larsson_rules=False,
            show_metrics=False,
        )

        # Verify runner was created with correct options
        call_args = mock_runner_class.call_args
        assert call_args[1]["show_explanations"] is False
        assert call_args[1]["show_state_changes"] is False
        assert call_args[1]["show_larsson_rules"] is False
        assert call_args[1]["show_metrics"] is False
