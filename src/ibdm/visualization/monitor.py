"""Real-time monitor for IBDM dialogue state.

Provides infrastructure for publishing state updates to a file and monitoring
those updates in a separate process/terminal.
"""

import json
import os
import time

from rich.console import Console

from ibdm.visualization.state_snapshot import StateSnapshot
from ibdm.visualization.terminal import TerminalVisualizer


class StatePublisher:
    """Publishes state updates to a file for monitoring."""

    def __init__(self, filepath: str = ".ibdm_monitor_state.json"):
        """Initialize publisher.
        
        Args:
            filepath: Path to the state file
        """
        self.filepath = filepath

    def publish(self, snapshot: StateSnapshot) -> None:
        """Publish a state snapshot.
        
        Args:
            snapshot: State snapshot to publish
        """
        try:
            data = snapshot.to_dict()
            # Write atomically (write to temp then rename)
            temp_path = f"{self.filepath}.tmp"
            with open(temp_path, "w") as f:
                json.dump(data, f, indent=2)
            os.replace(temp_path, self.filepath)
        except Exception as e:
            # Don't crash the application if monitoring fails
            print(f"[StatePublisher] Failed to publish state: {e}")


class StateMonitor:
    """Monitors a state file and updates the terminal display."""

    def __init__(self, filepath: str = ".ibdm_monitor_state.json", poll_interval: float = 0.1):
        """Initialize monitor.
        
        Args:
            filepath: Path to the state file
            poll_interval: Polling interval in seconds
        """
        self.filepath = filepath
        self.poll_interval = poll_interval
        self.console = Console()
        self.visualizer = TerminalVisualizer(self.console)
        self.last_timestamp = -1

    def start(self) -> None:
        """Start the monitoring loop."""
        self.console.clear()
        self.console.print("[bold blue]IBDM State Monitor[/bold blue]")
        self.console.print(f"Watching {self.filepath} (Ctrl+C to stop)...")

        try:
            while True:
                self._check_and_update()
                time.sleep(self.poll_interval)
        except KeyboardInterrupt:
            self.console.print("\n[bold red]Monitor stopped[/bold red]")

    def _check_and_update(self) -> None:
        """Check file for updates and refresh display if changed."""
        if not os.path.exists(self.filepath):
            return

        try:
            with open(self.filepath) as f:
                data = json.load(f)

            timestamp = data.get("timestamp", -1)

            if timestamp > self.last_timestamp:
                self.last_timestamp = timestamp
                snapshot = StateSnapshot.from_dict(data)

                # Clear and redraw
                self.console.clear()
                self.visualizer.render_snapshot(snapshot)
                self.console.print(f"\n[dim]Last updated: {time.strftime('%H:%M:%S')}[/dim]")

        except (json.JSONDecodeError, OSError):
            # File might be partially written, ignore
            pass
        except Exception as e:
            self.console.print(f"[red]Error reading state: {e}[/red]")
