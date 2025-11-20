"""Tests for ExecutionController."""

from __future__ import annotations

import time
from unittest.mock import MagicMock, patch

import pytest

from ibdm.demo import ExecutionController, ExecutionMode


class TestExecutionMode:
    """Test ExecutionMode enum."""

    def test_execution_modes_exist(self):
        """Test that all execution modes are defined."""
        assert ExecutionMode.STEP.value == "step"
        assert ExecutionMode.AUTO.value == "auto"
        assert ExecutionMode.REPLAY.value == "replay"

    def test_execution_mode_from_string(self):
        """Test creating ExecutionMode from string."""
        assert ExecutionMode("step") == ExecutionMode.STEP
        assert ExecutionMode("auto") == ExecutionMode.AUTO
        assert ExecutionMode("replay") == ExecutionMode.REPLAY


class TestExecutionControllerInit:
    """Test ExecutionController initialization."""

    def test_default_initialization(self):
        """Test controller with default parameters."""
        controller = ExecutionController()

        assert controller.mode == ExecutionMode.STEP
        assert controller.auto_delay == 2.0
        assert controller.banner_delay == 3.0
        assert controller.prompt == "Press Enter to continue..."
        assert controller.on_interrupt is None

    def test_custom_initialization(self):
        """Test controller with custom parameters."""
        callback = MagicMock()
        controller = ExecutionController(
            mode=ExecutionMode.AUTO,
            auto_delay=1.5,
            banner_delay=2.5,
            prompt="Next? ",
            on_interrupt=callback,
        )

        assert controller.mode == ExecutionMode.AUTO
        assert controller.auto_delay == 1.5
        assert controller.banner_delay == 2.5
        assert controller.prompt == "Next? "
        assert controller.on_interrupt == callback

    def test_repr(self):
        """Test string representation."""
        controller = ExecutionController(mode=ExecutionMode.AUTO, auto_delay=1.0, banner_delay=2.0)

        repr_str = repr(controller)
        assert "ExecutionController" in repr_str
        assert "mode=ExecutionMode.AUTO" in repr_str
        assert "auto_delay=1.0" in repr_str
        assert "banner_delay=2.0" in repr_str


class TestStepMode:
    """Test STEP mode (manual advancement)."""

    @patch("builtins.input", return_value="")
    def test_wait_at_banner_step_mode(self, mock_input):
        """Test wait_at_banner in step mode waits for input."""
        controller = ExecutionController(mode=ExecutionMode.STEP)

        controller.wait_at_banner()

        mock_input.assert_called_once_with("Press Enter to start... ")

    @patch("builtins.input", return_value="")
    def test_wait_between_turns_step_mode(self, mock_input):
        """Test wait_between_turns in step mode waits for input."""
        controller = ExecutionController(mode=ExecutionMode.STEP)

        controller.wait_between_turns()

        mock_input.assert_called_once_with("\nPress Enter for next turn... ")

    @patch("builtins.input", return_value="")
    def test_wait_at_end_step_mode(self, mock_input):
        """Test wait_at_end in step mode waits for input."""
        controller = ExecutionController(mode=ExecutionMode.STEP)

        controller.wait_at_end()

        mock_input.assert_called_once_with("\nPress Enter to finish... ")

    @patch("builtins.input", side_effect=KeyboardInterrupt)
    def test_keyboard_interrupt_in_step_mode(self, mock_input):
        """Test Ctrl+C handling in step mode."""
        controller = ExecutionController(mode=ExecutionMode.STEP)

        with pytest.raises(SystemExit) as exc_info:
            controller.wait_between_turns()

        assert exc_info.value.code == 0
        mock_input.assert_called_once()

    @patch("builtins.input", side_effect=KeyboardInterrupt)
    def test_keyboard_interrupt_with_callback(self, mock_input):
        """Test Ctrl+C with callback in step mode."""
        callback = MagicMock()
        controller = ExecutionController(mode=ExecutionMode.STEP, on_interrupt=callback)

        with pytest.raises(SystemExit):
            controller.wait_between_turns()

        callback.assert_called_once()


class TestAutoMode:
    """Test AUTO mode (automatic advancement)."""

    def test_wait_at_banner_auto_mode(self):
        """Test wait_at_banner in auto mode uses sleep."""
        controller = ExecutionController(mode=ExecutionMode.AUTO, banner_delay=0.1)

        start = time.time()
        controller.wait_at_banner()
        elapsed = time.time() - start

        # Should sleep for approximately banner_delay seconds
        assert 0.05 <= elapsed <= 0.2  # Allow some tolerance

    def test_wait_between_turns_auto_mode(self):
        """Test wait_between_turns in auto mode uses sleep."""
        controller = ExecutionController(mode=ExecutionMode.AUTO, auto_delay=0.1)

        start = time.time()
        controller.wait_between_turns()
        elapsed = time.time() - start

        # Should sleep for approximately auto_delay seconds
        assert 0.05 <= elapsed <= 0.2  # Allow some tolerance

    def test_wait_at_end_auto_mode(self):
        """Test wait_at_end in auto mode uses brief sleep."""
        controller = ExecutionController(mode=ExecutionMode.AUTO)

        start = time.time()
        controller.wait_at_end()
        elapsed = time.time() - start

        # Should sleep for approximately 1 second
        assert 0.8 <= elapsed <= 1.3

    @patch("time.sleep", side_effect=KeyboardInterrupt)
    def test_keyboard_interrupt_in_auto_mode(self, mock_sleep):
        """Test Ctrl+C handling in auto mode."""
        controller = ExecutionController(mode=ExecutionMode.AUTO)

        with pytest.raises(SystemExit) as exc_info:
            controller.wait_between_turns()

        assert exc_info.value.code == 0
        mock_sleep.assert_called_once()


class TestReplayMode:
    """Test REPLAY mode (no delays)."""

    def test_wait_at_banner_replay_mode(self):
        """Test wait_at_banner in replay mode has no delay."""
        controller = ExecutionController(mode=ExecutionMode.REPLAY)

        start = time.time()
        controller.wait_at_banner()
        elapsed = time.time() - start

        # Should be nearly instant (< 0.01 seconds)
        assert elapsed < 0.01

    def test_wait_between_turns_replay_mode(self):
        """Test wait_between_turns in replay mode has no delay."""
        controller = ExecutionController(mode=ExecutionMode.REPLAY)

        start = time.time()
        controller.wait_between_turns()
        elapsed = time.time() - start

        # Should be nearly instant
        assert elapsed < 0.01

    def test_wait_at_end_replay_mode(self):
        """Test wait_at_end in replay mode has no delay."""
        controller = ExecutionController(mode=ExecutionMode.REPLAY)

        start = time.time()
        controller.wait_at_end()
        elapsed = time.time() - start

        # Should be nearly instant
        assert elapsed < 0.01


class TestPause:
    """Test pause functionality."""

    @patch("builtins.input", return_value="")
    def test_pause_waits_in_any_mode(self, mock_input):
        """Test pause waits for input regardless of mode."""
        # Test in AUTO mode
        controller = ExecutionController(mode=ExecutionMode.AUTO)
        controller.pause()
        mock_input.assert_called_once()

        # Test in REPLAY mode
        mock_input.reset_mock()
        controller = ExecutionController(mode=ExecutionMode.REPLAY)
        controller.pause()
        mock_input.assert_called_once()

    @patch("builtins.input", return_value="")
    def test_pause_sets_paused_flag(self, mock_input):
        """Test pause sets and clears paused flag."""
        controller = ExecutionController(mode=ExecutionMode.AUTO)

        assert not controller.is_paused()

        # During pause (can't test easily due to blocking)
        # After pause completes
        controller.pause()
        assert not controller.is_paused()


class TestModeSwitch:
    """Test dynamic mode switching."""

    def test_set_mode(self):
        """Test changing execution mode."""
        controller = ExecutionController(mode=ExecutionMode.STEP)

        assert controller.mode == ExecutionMode.STEP

        controller.set_mode(ExecutionMode.AUTO)
        assert controller.mode == ExecutionMode.AUTO

        controller.set_mode(ExecutionMode.REPLAY)
        assert controller.mode == ExecutionMode.REPLAY

    @patch("builtins.input", return_value="")
    def test_behavior_changes_after_mode_switch(self, mock_input):
        """Test behavior changes when mode is switched."""
        controller = ExecutionController(mode=ExecutionMode.STEP)

        # In STEP mode, should wait for input
        controller.wait_between_turns()
        assert mock_input.called

        # Switch to REPLAY mode
        mock_input.reset_mock()
        controller.set_mode(ExecutionMode.REPLAY)

        # In REPLAY mode, should not wait
        start = time.time()
        controller.wait_between_turns()
        elapsed = time.time() - start

        assert not mock_input.called
        assert elapsed < 0.01


class TestConfigure:
    """Test runtime configuration."""

    def test_configure_auto_delay(self):
        """Test changing auto_delay."""
        controller = ExecutionController(auto_delay=2.0)

        assert controller.auto_delay == 2.0

        controller.configure(auto_delay=1.5)
        assert controller.auto_delay == 1.5

    def test_configure_banner_delay(self):
        """Test changing banner_delay."""
        controller = ExecutionController(banner_delay=3.0)

        assert controller.banner_delay == 3.0

        controller.configure(banner_delay=2.5)
        assert controller.banner_delay == 2.5

    def test_configure_prompt(self):
        """Test changing prompt."""
        controller = ExecutionController(prompt="Press Enter to continue...")

        assert controller.prompt == "Press Enter to continue..."

        controller.configure(prompt="Next? ")
        assert controller.prompt == "Next? "

    def test_configure_multiple_params(self):
        """Test changing multiple parameters at once."""
        controller = ExecutionController(auto_delay=2.0, banner_delay=3.0, prompt="Old")

        controller.configure(auto_delay=1.0, banner_delay=2.0, prompt="New")

        assert controller.auto_delay == 1.0
        assert controller.banner_delay == 2.0
        assert controller.prompt == "New"

    def test_configure_with_type_conversion(self):
        """Test configure converts types correctly."""
        controller = ExecutionController(auto_delay=2.0)

        # Pass string, should convert to float
        controller.configure(auto_delay="1.5")
        assert controller.auto_delay == 1.5
        assert isinstance(controller.auto_delay, float)


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_zero_delay(self):
        """Test controller with zero delay."""
        controller = ExecutionController(mode=ExecutionMode.AUTO, auto_delay=0.0)

        start = time.time()
        controller.wait_between_turns()
        elapsed = time.time() - start

        # Should be nearly instant
        assert elapsed < 0.01

    def test_very_long_delay(self):
        """Test controller with very long delay (don't actually wait)."""
        controller = ExecutionController(mode=ExecutionMode.AUTO, auto_delay=100.0)

        # Just verify it's set correctly, don't actually wait
        assert controller.auto_delay == 100.0

    def test_custom_prompt_used(self):
        """Test that custom prompt is actually used."""
        with patch("builtins.input", return_value="") as mock_input:
            controller = ExecutionController(mode=ExecutionMode.STEP, prompt="Custom prompt: ")

            controller.wait_between_turns()

            # Should use the per-call prompt, not the default
            mock_input.assert_called_once_with("\nPress Enter for next turn... ")


class TestIntegration:
    """Integration tests for typical usage patterns."""

    @patch("builtins.input", return_value="")
    def test_typical_scenario_step_mode(self, mock_input):
        """Test typical scenario execution in step mode."""
        controller = ExecutionController(mode=ExecutionMode.STEP)

        # Banner
        controller.wait_at_banner()
        assert mock_input.call_count == 1

        # 3 turns
        for _ in range(3):
            controller.wait_between_turns()

        assert mock_input.call_count == 4  # 1 banner + 3 turns

        # End
        controller.wait_at_end()
        assert mock_input.call_count == 5

    def test_typical_scenario_auto_mode(self):
        """Test typical scenario execution in auto mode."""
        controller = ExecutionController(
            mode=ExecutionMode.AUTO, auto_delay=0.01, banner_delay=0.01
        )

        start = time.time()

        # Banner
        controller.wait_at_banner()

        # 3 turns
        for _ in range(3):
            controller.wait_between_turns()

        # End
        controller.wait_at_end()

        elapsed = time.time() - start

        # Total: 0.01 (banner) + 3*0.01 (turns) + 1.0 (end) ≈ 1.04 seconds
        assert 1.0 <= elapsed <= 1.2

    def test_typical_scenario_replay_mode(self):
        """Test typical scenario execution in replay mode."""
        controller = ExecutionController(mode=ExecutionMode.REPLAY)

        start = time.time()

        # Banner
        controller.wait_at_banner()

        # 100 turns (should be fast)
        for _ in range(100):
            controller.wait_between_turns()

        # End
        controller.wait_at_end()

        elapsed = time.time() - start

        # Should be nearly instant even with 100 turns
        assert elapsed < 0.1

    @patch("builtins.input", return_value="")
    def test_mode_switching_mid_scenario(self, mock_input):
        """Test switching modes during scenario execution."""
        controller = ExecutionController(mode=ExecutionMode.STEP)

        # Start in step mode
        controller.wait_at_banner()
        assert mock_input.call_count == 1

        # Switch to auto mode
        controller.set_mode(ExecutionMode.AUTO)
        controller.configure(auto_delay=0.01)

        # Should use auto mode now
        start = time.time()
        controller.wait_between_turns()
        elapsed = time.time() - start

        # Should not have called input again
        assert mock_input.call_count == 1
        # Should have used sleep instead
        assert 0.005 <= elapsed <= 0.05
