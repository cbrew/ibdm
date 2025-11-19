"""Real-time state monitor script.

Run this script in a separate terminal window to monitor the dialogue state
in real-time as you interact with the Scenario Explorer.
"""

import argparse

from ibdm.visualization.monitor import StateMonitor


def main():
    """Run the state monitor."""
    parser = argparse.ArgumentParser(description="IBDM State Monitor")
    parser.add_argument(
        "--file",
        default=".ibdm_monitor_state.json",
        help="Path to the state file to monitor",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=0.5,
        help="Polling interval in seconds",
    )
    args = parser.parse_args()

    monitor = StateMonitor(filepath=args.file, poll_interval=args.interval)
    monitor.start()


if __name__ == "__main__":
    main()
