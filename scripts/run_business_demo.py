#!/usr/bin/env python3
"""Business Demo Launcher for IBDM.

One-command demo script that runs pre-configured dialogue scenarios
with professional output and auto-generated HTML reports.

Usage:
    python scripts/run_business_demo.py                    # Run default (nda_basic)
    python scripts/run_business_demo.py --scenario nda_volunteer
    python scripts/run_business_demo.py --all              # Run all scenarios
    python scripts/run_business_demo.py --scenario nda_basic --no-report
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Simplified imports for demo - avoid heavy dependencies
try:
    from ibdm.core import InformationState
    from ibdm.domains.nda_domain import get_nda_domain
except ImportError as e:
    print(f"Error importing IBDM modules: {e}")
    print("This script requires IBDM to be installed.")
    sys.exit(1)

# Mock DialogueHistory and DialogueVisualizer if not available
try:
    from ibdm.demo.visualization import DialogueHistory, DialogueVisualizer
except ImportError:
    # Lightweight fallbacks
    class DialogueHistory:
        def __init__(self, session_id, start_time, metadata):
            self.session_id = session_id
            self.start_time = start_time
            self.end_time = None
            self.metadata = metadata
            self.turns = []

        def add_turn(self, turn_number, speaker, utterance, move_type, state_snapshot=None):
            self.turns.append(
                {
                    "turn": turn_number,
                    "speaker": speaker,
                    "utterance": utterance,
                    "move_type": move_type,
                    "state": state_snapshot,
                }
            )

    class DialogueVisualizer:
        def __init__(self, width=80):
            self.width = width


class BusinessDemo:
    """Run pre-scripted business demonstration scenarios."""

    def __init__(self, scenario_path: Path, verbose: bool = True, auto_advance: bool = True):
        """Initialize business demo.

        Args:
            scenario_path: Path to scenario JSON file
            verbose: Whether to print detailed output
            auto_advance: Whether to auto-advance turns (vs manual)
        """
        self.scenario_path = scenario_path
        self.verbose = verbose
        self.auto_advance = auto_advance

        # Load scenario
        self.scenario = json.loads(scenario_path.read_text())

        # Initialize dialogue history for reporting
        self.dialogue_history = DialogueHistory(
            session_id=f"{self.scenario['scenario_id']}-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            start_time=datetime.now().isoformat(),
            metadata={
                "scenario_id": self.scenario["scenario_id"],
                "scenario_title": self.scenario["title"],
                "run_mode": "automated",
            },
        )

        # Initialize visualizer
        self.visualizer = DialogueVisualizer(width=80)

        # Domain model
        self.domain = get_nda_domain()

        # Mock state for tracking (simplified)
        self.state = InformationState(agent_id="system")

    def print_banner(self) -> None:
        """Print demo banner."""
        print("\n" + "=" * 80)
        print("IBDM BUSINESS DEMONSTRATION")
        print("=" * 80)
        print(f"\nScenario: {self.scenario['title']}")
        print(f"Description: {self.scenario['description']}")
        print("\n" + "-" * 80)
        print("BUSINESS VALUE:")
        print(self.scenario["business_narrative"])
        print("-" * 80 + "\n")

        if self.auto_advance:
            print("⏵ Auto-advance mode: Dialogue will play automatically")
            print("  (Press Ctrl+C to pause)\n")
        else:
            print("⏵ Manual mode: Press Enter to advance each turn\n")

    def print_turn(self, turn_data: dict[str, Any], turn_index: int) -> None:
        """Print a single turn with formatting.

        Args:
            turn_data: Turn data from scenario JSON
            turn_index: Index of turn in scenario
        """
        turn_num = turn_data["turn"]
        speaker = turn_data["speaker"]
        utterance = turn_data["utterance"]
        move_type = turn_data.get("move_type", "")

        # Format speaker name
        if speaker == "user":
            speaker_display = "👤 USER"
            color_code = "\033[94m"  # Blue
        else:
            speaker_display = "🤖 SYSTEM"
            color_code = "\033[92m"  # Green

        reset_code = "\033[0m"

        # Print turn header
        print(f"\n{'─' * 80}")
        print(f"{color_code}Turn {turn_num}: {speaker_display} [{move_type}]{reset_code}")
        print(f"{'─' * 80}")

        # Print utterance
        print(f"{utterance}")

        # Print business explanation if verbose
        if self.verbose and "business_explanation" in turn_data:
            print(f"\n💡 {turn_data['business_explanation']}")

        # Print Larsson algorithm reference
        if self.verbose and "larsson_rule" in turn_data:
            print(f"📚 Larsson: {turn_data['larsson_rule']}")

        # Print state changes
        if self.verbose and "state_changes" in turn_data:
            print("\n📊 State Changes:")
            for key, value in turn_data["state_changes"].items():
                key_display = key.replace("_", " ").title()
                print(f"   • {key_display}: {value}")

        # Record in dialogue history
        self.dialogue_history.add_turn(
            turn_number=turn_num,
            speaker=speaker,
            utterance=utterance,
            move_type=move_type,
            state_snapshot=turn_data.get("state_changes", {}),
        )

    def run_scenario(self) -> dict[str, Any]:
        """Run the scenario and return metrics.

        Returns:
            Dictionary of metrics from the run
        """
        self.print_banner()

        # Wait for user to read banner
        if self.auto_advance:
            time.sleep(3)
        else:
            input("Press Enter to start... ")

        # Run each turn
        for i, turn in enumerate(self.scenario["turns"]):
            self.print_turn(turn, i)

            # Auto-advance delay or manual control
            if i < len(self.scenario["turns"]) - 1:  # Not last turn
                if self.auto_advance:
                    time.sleep(2)  # 2 second delay between turns
                else:
                    input("\nPress Enter for next turn... ")

        # Final summary
        self.print_summary()

        # Mark end time
        self.dialogue_history.end_time = datetime.now().isoformat()

        # Return metrics
        return self.scenario.get("metrics", {})

    def print_summary(self) -> None:
        """Print final summary and metrics."""
        print("\n\n" + "=" * 80)
        print("DEMONSTRATION COMPLETE")
        print("=" * 80)

        print("\n📊 SCENARIO METRICS:")
        print("-" * 80)

        metrics = self.scenario.get("metrics", {})
        expected = self.scenario.get("expected_outcomes", {})

        # Print expected outcomes
        if expected:
            print("\nExpected Outcomes:")
            for key, value in expected.items():
                key_display = key.replace("_", " ").title()
                print(f"  • {key_display}: {value}")

        # Print metrics
        if metrics:
            print("\nActual Performance:")
            for key, value in metrics.items():
                key_display = key.replace("_", " ").title()
                print(f"  • {key_display}: {value}")

        # Print Larsson algorithms demonstrated
        print("\n📚 LARSSON ALGORITHMS DEMONSTRATED:")
        print("-" * 80)
        for i, algo in enumerate(self.scenario.get("larsson_algorithms", []), 1):
            print(f"{i}. {algo}")

        # Print business value
        if "business_value" in self.scenario:
            print("\n💼 BUSINESS VALUE:")
            print("-" * 80)
            print(self.scenario["business_value"])

        print("\n" + "=" * 80 + "\n")

    def export_report(self, output_dir: Path) -> Path:
        """Export HTML report.

        Args:
            output_dir: Directory to save report

        Returns:
            Path to generated report
        """
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"business-demo-{self.scenario['scenario_id']}-{timestamp}.html"
        report_path = output_dir / filename

        # Generate HTML using visualizer
        html_content = self._generate_business_report_html()

        report_path.write_text(html_content)

        return report_path

    def _generate_business_report_html(self) -> str:
        """Generate business-friendly HTML report.

        Returns:
            HTML content as string
        """
        # Build HTML report
        html_parts = []

        # Header
        html_parts.append(
            """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>IBDM Business Demo Report</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .header h1 {
            margin: 0 0 10px 0;
        }
        .section {
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .section h2 {
            color: #667eea;
            margin-top: 0;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        .turn {
            margin: 15px 0;
            padding: 15px;
            border-left: 4px solid #ddd;
            background: #f9f9f9;
        }
        .turn.user {
            border-left-color: #4CAF50;
        }
        .turn.system {
            border-left-color: #2196F3;
        }
        .turn-header {
            font-weight: bold;
            margin-bottom: 8px;
        }
        .explanation {
            margin-top: 10px;
            padding: 10px;
            background: #fff3cd;
            border-left: 3px solid #ffc107;
            font-size: 0.9em;
        }
        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }
        .metric-card {
            padding: 15px;
            background: #e3f2fd;
            border-radius: 5px;
            border-left: 4px solid #2196F3;
        }
        .metric-card h3 {
            margin: 0 0 5px 0;
            color: #1976D2;
        }
        .algorithms li {
            margin: 10px 0;
            line-height: 1.6;
        }
        .footer {
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 0.9em;
        }
    </style>
</head>
<body>"""
        )

        # Title section
        html_parts.append(
            f"""
    <div class="header">
        <h1>{self.scenario["title"]}</h1>
        <p><strong>Scenario ID:</strong> {self.scenario["scenario_id"]}</p>
        <p>{self.scenario["description"]}</p>
        <p><em>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</em></p>
    </div>"""
        )

        # Business narrative section
        html_parts.append(
            f"""
    <div class="section">
        <h2>💼 Business Value</h2>
        <p>{self.scenario["business_narrative"]}</p>
    </div>"""
        )

        # Dialogue transcript
        html_parts.append(
            """
    <div class="section">
        <h2>📝 Dialogue Transcript</h2>"""
        )

        for turn in self.scenario["turns"]:
            speaker_class = turn["speaker"]
            speaker_icon = "👤" if speaker_class == "user" else "🤖"
            speaker_name = turn["speaker"].upper()

            move_type = turn.get("move_type", "")
            turn_num = turn["turn"]
            turn_header = f"{speaker_icon} Turn {turn_num}: {speaker_name} [{move_type}]"
            html_parts.append(
                f"""
        <div class="turn {speaker_class}">
            <div class="turn-header">{turn_header}</div>
            <div>{turn["utterance"]}</div>"""
            )

            if "business_explanation" in turn:
                html_parts.append(
                    f"""
            <div class="explanation">
                💡 <strong>What's happening:</strong> {turn["business_explanation"]}<br>
                📚 <strong>Larsson:</strong> {turn.get("larsson_rule", "N/A")}
            </div>"""
                )

            html_parts.append("        </div>")

        html_parts.append("    </div>")

        # Metrics section
        html_parts.append(
            """
    <div class="section">
        <h2>📊 Performance Metrics</h2>
        <div class="metrics">"""
        )

        for key, value in self.scenario.get("metrics", {}).items():
            key_display = key.replace("_", " ").title()
            html_parts.append(
                f"""
            <div class="metric-card">
                <h3>{key_display}</h3>
                <p>{value}</p>
            </div>"""
            )

        html_parts.append("        </div>\n    </div>")

        # Larsson algorithms section
        html_parts.append(
            """
    <div class="section">
        <h2>📚 Larsson Algorithms Demonstrated</h2>
        <ul class="algorithms">"""
        )

        for algo in self.scenario.get("larsson_algorithms", []):
            html_parts.append(f"            <li>{algo}</li>")

        html_parts.append("        </ul>\n    </div>")

        # Additional business value (if present)
        if "business_value" in self.scenario:
            html_parts.append(
                f"""
    <div class="section">
        <h2>🎯 Key Takeaways</h2>
        <p>{self.scenario["business_value"]}</p>
    </div>"""
            )

        # Footer
        html_parts.append(
            """
    <div class="footer">
        <p>Generated by IBDM Business Demo System</p>
        <p>Issue-Based Dialogue Management • Larsson (2002) Implementation</p>
    </div>
</body>
</html>"""
        )

        return "\n".join(html_parts)


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run IBDM business demonstration scenarios",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--scenario",
        default="nda_basic",
        help=(
            "Scenario to run (nda_basic, nda_volunteer, nda_complex, "
            "nda_grounding, nda_comprehensive)"
        ),
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all scenarios sequentially",
    )
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Skip HTML report generation",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("demos/reports"),
        help="Directory for HTML reports (default: demos/reports)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Minimal output (no business explanations)",
    )
    parser.add_argument(
        "--manual",
        action="store_true",
        help="Manual mode (press Enter to advance)",
    )

    args = parser.parse_args()

    # Determine scenarios to run
    scenarios_dir = Path(__file__).parent.parent / "demos" / "scenarios"

    if args.all:
        scenario_files = [
            scenarios_dir / "nda_basic.json",
            scenarios_dir / "nda_volunteer.json",
            scenarios_dir / "nda_complex.json",
            scenarios_dir / "nda_grounding.json",
            scenarios_dir / "nda_comprehensive.json",
        ]
    else:
        scenario_file = scenarios_dir / f"{args.scenario}.json"
        if not scenario_file.exists():
            print(f"Error: Scenario file not found: {scenario_file}")
            print(f"\nAvailable scenarios in {scenarios_dir}:")
            for f in scenarios_dir.glob("*.json"):
                print(f"  - {f.stem}")
            return 1
        scenario_files = [scenario_file]

    # Run scenarios
    for scenario_file in scenario_files:
        try:
            demo = BusinessDemo(
                scenario_file,
                verbose=not args.quiet,
                auto_advance=not args.manual,
            )

            demo.run_scenario()

            # Generate report
            if not args.no_report:
                report_path = demo.export_report(args.output_dir)
                print(f"✓ Report saved: {report_path}")

        except KeyboardInterrupt:
            print("\n\nDemo interrupted by user.")
            return 130
        except Exception as e:
            print(f"\n✗ Error running scenario: {e}")
            import traceback

            traceback.print_exc()
            return 1

    print("\n✓ All demonstrations complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
