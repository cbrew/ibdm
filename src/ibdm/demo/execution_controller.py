"""Execution flow controller for IBDM demos and scenarios.

Provides consistent execution timing and flow control across different demo types
(scripted scenarios, interactive sessions, replays).
"""

from __future__ import annotations

import sys
import time
from collections.abc import Callable
from enum import Enum


class ExecutionMode(Enum):
    """Execution mode for dialogue scenarios."""

    STEP = "step"  # Manual: wait for user input
    AUTO = "auto"  # Automatic: timed delays
    REPLAY = "replay"  # Playback: from saved session


class ExecutionController:
    """Controls execution flow for dialogue scenarios.

    Provides consistent execution timing and flow control across
    different demo types (scripted scenarios, interactive sessions,
    replays).

    Examples:
        >>> # Step mode (manual advancement)
        >>> controller = ExecutionController(mode=ExecutionMode.STEP)
        >>> controller.wait_between_turns()  # Waits for Enter key

        >>> # Auto mode (automatic advancement)
        >>> controller = ExecutionController(
        ...     mode=ExecutionMode.AUTO,
        ...     auto_delay=2.0
        ... )
        >>> controller.wait_between_turns()  # Sleeps for 2 seconds

        >>> # Dynamic mode switching
        >>> controller.set_mode(ExecutionMode.AUTO)

        >>> # Runtime configuration
        >>> controller.configure(auto_delay=1.0, prompt="Continue? ")
    """

    def __init__(
        self,
        mode: ExecutionMode = ExecutionMode.STEP,
        auto_delay: float = 2.0,
        banner_delay: float = 3.0,
        prompt: str = "Press Enter to continue...",
        on_interrupt: Callable[[], None] | None = None,
    ):
        """Initialize execution controller.

        Args:
            mode: Execution mode (step/auto/replay)
            auto_delay: Delay between turns in auto mode (seconds)
            banner_delay: Delay after showing banner in auto mode (seconds)
            prompt: Prompt message for step mode
            on_interrupt: Callback when user interrupts (Ctrl+C)
        """
        self.mode = mode
        self.auto_delay = auto_delay
        self.banner_delay = banner_delay
        self.prompt = prompt
        self.on_interrupt = on_interrupt
        self._paused = False

    def wait_at_banner(self) -> None:
        """Wait after displaying banner/intro.

        In STEP mode: waits for user to press Enter
        In AUTO mode: sleeps for banner_delay seconds
        In REPLAY mode: no delay

        Examples:
            >>> controller = ExecutionController(mode=ExecutionMode.AUTO, banner_delay=3.0)
            >>> controller.wait_at_banner()  # Sleeps for 3 seconds
        """
        if self.mode == ExecutionMode.STEP:
            self._wait_for_input("Press Enter to start... ")
        elif self.mode == ExecutionMode.AUTO:
            self._sleep(self.banner_delay)
        # REPLAY mode: no delay

    def wait_between_turns(self) -> None:
        """Wait between dialogue turns.

        In STEP mode: waits for user to press Enter
        In AUTO mode: sleeps for auto_delay seconds
        In REPLAY mode: no delay

        Examples:
            >>> controller = ExecutionController(mode=ExecutionMode.AUTO, auto_delay=2.0)
            >>> controller.wait_between_turns()  # Sleeps for 2 seconds
        """
        if self.mode == ExecutionMode.STEP:
            self._wait_for_input("\nPress Enter for next turn... ")
        elif self.mode == ExecutionMode.AUTO:
            self._sleep(self.auto_delay)
        # REPLAY mode: no delay

    def wait_at_end(self) -> None:
        """Wait at end of scenario.

        In STEP mode: waits for user to press Enter
        In AUTO mode: brief pause to let user see results
        In REPLAY mode: no delay

        Examples:
            >>> controller = ExecutionController(mode=ExecutionMode.STEP)
            >>> controller.wait_at_end()  # Waits for Enter
        """
        if self.mode == ExecutionMode.STEP:
            self._wait_for_input("\nPress Enter to finish... ")
        elif self.mode == ExecutionMode.AUTO:
            self._sleep(1.0)  # Brief pause at end
        # REPLAY mode: no delay

    def pause(self) -> None:
        """Pause execution until user action.

        Always waits for user input regardless of mode.
        Use this for breakpoints or interactive choices.

        Examples:
            >>> controller = ExecutionController(mode=ExecutionMode.AUTO)
            >>> controller.pause()  # Waits even in auto mode
        """
        self._paused = True
        self._wait_for_input("\n⏸️  PAUSED - Press Enter to resume... ")
        self._paused = False

    def set_mode(self, mode: ExecutionMode) -> None:
        """Change execution mode dynamically.

        Args:
            mode: New execution mode

        Examples:
            >>> controller = ExecutionController(mode=ExecutionMode.STEP)
            >>> controller.set_mode(ExecutionMode.AUTO)
            >>> controller.mode
            <ExecutionMode.AUTO: 'auto'>
        """
        self.mode = mode

    def configure(self, **kwargs: float | str) -> None:
        """Update configuration dynamically.

        Args:
            **kwargs: Configuration parameters to update
                - auto_delay: float
                - banner_delay: float
                - prompt: str

        Examples:
            >>> controller = ExecutionController(auto_delay=2.0)
            >>> controller.configure(auto_delay=1.0, prompt="Next? ")
            >>> controller.auto_delay
            1.0
        """
        if "auto_delay" in kwargs:
            self.auto_delay = float(kwargs["auto_delay"])
        if "banner_delay" in kwargs:
            self.banner_delay = float(kwargs["banner_delay"])
        if "prompt" in kwargs:
            self.prompt = str(kwargs["prompt"])

    def _wait_for_input(self, prompt: str | None = None) -> None:
        """Wait for user to press Enter.

        Args:
            prompt: Optional prompt to display (default: self.prompt)
        """
        try:
            input(prompt or self.prompt)
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user (Ctrl+C)")
            if self.on_interrupt:
                self.on_interrupt()
            sys.exit(0)

    def _sleep(self, duration: float) -> None:
        """Sleep for specified duration with interrupt handling.

        Args:
            duration: Sleep duration in seconds
        """
        try:
            time.sleep(duration)
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user (Ctrl+C)")
            if self.on_interrupt:
                self.on_interrupt()
            sys.exit(0)

    def is_paused(self) -> bool:
        """Check if controller is currently paused.

        Returns:
            True if paused, False otherwise
        """
        return self._paused

    def __repr__(self) -> str:
        """String representation of controller.

        Returns:
            String showing mode and configuration
        """
        return (
            f"ExecutionController(mode={self.mode}, "
            f"auto_delay={self.auto_delay}, "
            f"banner_delay={self.banner_delay})"
        )
