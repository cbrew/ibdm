#!/usr/bin/env python3
"""Business Demo Launcher for IBDM.

One-command demo script that runs pre-configured dialogue scenarios
with professional output and auto-generated HTML reports.

ARCHITECTURAL NOTE - Loading Semantic Representations vs NLU:
    This demo LOADS semantic representations from scenario JSON
    (e.g., state_changes.qud_pushed: "?x.legal_entities(x)") and converts
    them to DialogueMove objects. This is NOT parsing natural language text.

    What the demo shows:  MEANING → TEXT (NLG)
    Future work:          TEXT → MEANING (NLU)

    Inferring DialogueMoves from natural language utterances would be NLU work,
    which is explicitly out of scope for this demo.

Usage:
    python scripts/run_business_demo.py                    # Run default (nda_basic)
    python scripts/run_business_demo.py --scenario nda_volunteer
    python scripts/run_business_demo.py --all              # Run all scenarios
    python scripts/run_business_demo.py --scenario nda_basic --no-report
    python scripts/run_business_demo.py --nlg-mode compare # Show NLG comparison
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

# Required imports - fail fast if not available
from ibdm.core import InformationState
from ibdm.core.plans import Plan
from ibdm.core.questions import Question
from ibdm.domains.nda_domain import get_nda_domain


# Simple classes for demo reporting (no external dependencies)
class DialogueHistory:
    """Lightweight dialogue history for demo reporting."""

    def __init__(self, session_id: str, start_time: str, metadata: dict[str, Any]):
        self.session_id = session_id
        self.start_time = start_time
        self.end_time: str | None = None
        self.metadata = metadata
        self.turns: list[dict[str, Any]] = []

    def add_turn(
        self,
        turn_number: int,
        speaker: str,
        utterance: str,
        move_type: str,
        state_snapshot: dict[str, Any] | None = None,
    ) -> None:
        """Add a turn to the history."""
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
    """Lightweight visualizer placeholder (not used in this demo)."""

    def __init__(self, width: int = 80):
        self.width = width


class BusinessDemo:
    """Run pre-scripted business demonstration scenarios."""

    def __init__(
        self,
        scenario_path: Path,
        verbose: bool = True,
        auto_advance: bool = True,
        nlg_mode: str = "off",
    ):
        """Initialize business demo.

        Args:
            scenario_path: Path to scenario JSON file
            verbose: Whether to print detailed output
            auto_advance: Whether to auto-advance turns (vs manual)
            nlg_mode: NLG mode - "off" (scripted only), "compare" (both), or "replace" (NLG only)
        """
        self.scenario_path = scenario_path
        self.verbose = verbose
        self.auto_advance = auto_advance
        self.nlg_mode = nlg_mode

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
                "nlg_mode": nlg_mode,
            },
        )

        # Initialize visualizer
        self.visualizer = DialogueVisualizer(width=80)

        # Domain model
        self.domain = get_nda_domain()

        # Mock state for tracking (simplified)
        self.state = InformationState(agent_id="system")

        # Initialize NLG engine conditionally (only if needed)
        self.nlg_engine = None
        if self.nlg_mode != "off":
            from ibdm.nlg.nlg_engine import NLGEngine, NLGEngineConfig

            config = NLGEngineConfig(
                default_strategy="plan_aware",
                use_plan_awareness=True,
                use_domain_descriptions=True,
            )
            self.nlg_engine = NLGEngine(config)
            if self.verbose:
                print(f"✓ NLG engine initialized (mode: {nlg_mode})")

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

        # Apply state changes to real InformationState
        if "state_changes" in turn_data:
            self._apply_state_changes(self.state, turn_data["state_changes"])

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

        # Generate NLG utterance for system turns if needed
        nlg_utterance = None
        if speaker == "system" and self.nlg_engine is not None and self.nlg_mode != "off":
            # Create DialogueMove from semantic annotations in turn data
            # NOTE: This LOADS structured semantic data from JSON (qud_pushed, etc.),
            # NOT from natural language text. The scenario JSON contains
            # semantic representations that we convert to DialogueMove objects.
            # This demonstrates: SEMANTIC REPRESENTATION → NATURAL LANGUAGE (NLG)
            # Future NLU work would be: NATURAL LANGUAGE → SEMANTIC REPRESENTATION
            move = self._create_system_dialogue_move(turn_data)

            # Generate natural language using NLG engine
            nlg_result = self.nlg_engine.generate(move, self.state)
            nlg_utterance = nlg_result.utterance_text

        # Display utterances based on mode
        if speaker == "user" or self.nlg_mode == "off":
            # User turns: always show scripted
            # System turns in "off" mode: show scripted
            print(f"{utterance}")

        elif self.nlg_mode == "compare":
            # Compare mode: show both scripted and NLG
            print("\n📜 SCRIPTED (Gold Standard):")
            print(f'   "{utterance}"')

            if nlg_utterance:
                print("\n🤖 NLG GENERATED:")
                print(f'   "{nlg_utterance}"')
            else:
                print("\n🤖 NLG GENERATED: (generation failed, using scripted)")

        elif self.nlg_mode == "replace":
            # Replace mode: show NLG only (or fallback to scripted)
            if nlg_utterance:
                print(f"{nlg_utterance}")
            else:
                print(f"{utterance}")
                if self.verbose:
                    print("   (using scripted - NLG unavailable)")

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

        # Record in dialogue history (use NLG utterance if in replace mode)
        displayed_utterance = utterance
        if speaker == "system" and self.nlg_mode == "replace" and nlg_utterance:
            displayed_utterance = nlg_utterance

        self.dialogue_history.add_turn(
            turn_number=turn_num,
            speaker=speaker,
            utterance=displayed_utterance,
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

    def export_report(self, output_dir: Path) -> tuple[Path, Path]:
        """Export HTML reports (business and engineer).

        Args:
            output_dir: Directory to save reports

        Returns:
            Tuple of (business_report_path, engineer_report_path)
        """
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

        # Generate business report
        business_filename = f"business-demo-{self.scenario['scenario_id']}-{timestamp}.html"
        business_report_path = output_dir / business_filename
        business_html_content = self._generate_business_report_html()
        business_report_path.write_text(business_html_content)

        # Generate engineer report
        engineer_filename = f"engineer-demo-{self.scenario['scenario_id']}-{timestamp}.html"
        engineer_report_path = output_dir / engineer_filename
        engineer_html_content = self._generate_engineer_report_html()
        engineer_report_path.write_text(engineer_html_content)

        return business_report_path, engineer_report_path

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

    def _generate_engineer_report_html(self) -> str:
        """Generate engineer-focused HTML report with full state details.

        Returns:
            HTML content as string
        """
        html_parts = []

        # Header
        html_parts.append(
            """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>IBDM Engineer Report</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            background: #1e1e1e;
            color: #d4d4d4;
        }
        .header {
            background: linear-gradient(135deg, #0078d4 0%, #00bcf2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .header h1 {
            margin: 0 0 10px 0;
            font-family: 'Segoe UI', sans-serif;
        }
        .mock-warning {
            background: #fff3cd;
            color: #856404;
            padding: 15px;
            margin: 20px 0;
            border-left: 4px solid #ffc107;
            border-radius: 4px;
        }
        .section {
            background: #252526;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
            border: 1px solid #3e3e42;
        }
        .section h2 {
            color: #4ec9b0;
            margin-top: 0;
            border-bottom: 2px solid #4ec9b0;
            padding-bottom: 10px;
            font-family: 'Segoe UI', sans-serif;
        }
        .section h3 {
            color: #dcdcaa;
            margin-top: 15px;
            font-size: 1.1em;
        }
        .turn {
            margin: 20px 0;
            padding: 20px;
            border: 1px solid #3e3e42;
            background: #1e1e1e;
            border-radius: 5px;
        }
        .turn-header {
            font-weight: bold;
            font-size: 1.2em;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #3e3e42;
        }
        .turn.user .turn-header {
            color: #4ec9b0;
        }
        .turn.system .turn-header {
            color: #569cd6;
        }
        .utterance {
            background: #2d2d30;
            padding: 15px;
            margin: 10px 0;
            border-left: 3px solid #007acc;
            font-size: 1.1em;
        }
        .state-box {
            background: #1e1e1e;
            border: 1px solid #007acc;
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
        }
        .state-box h4 {
            color: #dcdcaa;
            margin: 0 0 10px 0;
            font-size: 0.9em;
            text-transform: uppercase;
        }
        .state-content {
            background: #252526;
            padding: 10px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            white-space: pre-wrap;
            overflow-x: auto;
        }
        .json-view {
            background: #1e1e1e;
            border: 1px solid #3e3e42;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
        }
        .json-key {
            color: #9cdcfe;
        }
        .json-string {
            color: #ce9178;
        }
        .json-number {
            color: #b5cea8;
        }
        .json-boolean {
            color: #569cd6;
        }
        .mock-indicator {
            display: inline-block;
            background: #ffc107;
            color: #000;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 0.8em;
            font-weight: bold;
            margin-left: 10px;
        }
        .algorithm-box {
            background: #2d2d30;
            border-left: 3px solid #4ec9b0;
            padding: 15px;
            margin: 10px 0;
        }
        .algorithm-box .title {
            color: #4ec9b0;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .state-diff {
            background: #1e1e1e;
            padding: 10px;
            margin: 10px 0;
            border-radius: 4px;
        }
        .state-diff .added {
            color: #4ec9b0;
        }
        .state-diff .removed {
            color: #f48771;
        }
        .state-diff .modified {
            color: #dcdcaa;
        }
        .footer {
            text-align: center;
            padding: 20px;
            color: #808080;
            font-size: 0.9em;
            font-family: 'Segoe UI', sans-serif;
        }
        pre {
            margin: 0;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        .metadata {
            background: #252526;
            padding: 10px;
            margin: 10px 0;
            border-radius: 4px;
            font-size: 0.9em;
        }
        .metadata strong {
            color: #569cd6;
        }
    </style>
</head>
<body>"""
        )

        # Title section with mocking warning
        html_parts.append(
            f"""
    <div class="header">
        <h1>🔧 Engineer Report: {self.scenario["title"]}</h1>
        <p><strong>Scenario ID:</strong> {self.scenario["scenario_id"]}</p>
        <p>{self.scenario["description"]}</p>
        <p><em>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</em></p>
    </div>

    <div class="mock-warning">
        ⚠️ <strong>MOCKING IN EFFECT:</strong> This demonstration uses pre-scripted dialogues.
        In production, NLU (Natural Language Understanding) and NLG (Natural Language Generation)
        are handled by Claude 4.5 Sonnet/Haiku models. State management and dialogue update rules
        follow Larsson (2002) algorithms exactly as implemented in the core engine.
    </div>"""
        )

        # Overview section
        html_parts.append(
            """
    <div class="section">
        <h2>📋 System Overview</h2>
        <div class="metadata">
            <strong>Architecture:</strong> Burr state machine with Larsson update rules<br>
            <strong>Domain:</strong> NDA (Non-Disclosure Agreement) drafting<br>
            <strong>NLU Engine:</strong> <span class="mock-indicator">MOCKED</span>
            (Production: Claude 4.5 Sonnet via LiteLLM)<br>
            <strong>NLG Engine:</strong> <span class="mock-indicator">MOCKED</span>
            (Production: Claude 4.5 Haiku via LiteLLM)<br>
            <strong>Dialogue Manager:</strong> <strong style="color: #4ec9b0;">LIVE</strong>
            (Larsson algorithms in src/ibdm/core/)<br>
            <strong>State Management:</strong> <strong style="color: #4ec9b0;">LIVE</strong>
            (InformationState with QUD stack, commitments, plans)
        </div>
    </div>"""
        )

        # Expected outcomes section
        expected = self.scenario.get("expected_outcomes", {})
        if expected:
            html_parts.append(
                """
    <div class="section">
        <h2>🎯 Expected Outcomes</h2>
        <div class="json-view">
            <pre>"""
            )
            html_parts.append(json.dumps(expected, indent=2))
            html_parts.append("</pre>\n        </div>\n    </div>")

        # Detailed turn-by-turn analysis
        html_parts.append(
            """
    <div class="section">
        <h2>🔍 Turn-by-Turn State Analysis</h2>"""
        )

        # Track cumulative state for display
        cumulative_state = {
            "qud": [],
            "commitments": [],
            "private_issues": [],
            "plans": [],
            "latest_move": None,
        }

        for turn in self.scenario["turns"]:
            speaker_class = turn["speaker"]
            speaker_icon = "👤" if speaker_class == "user" else "🤖"
            speaker_name = turn["speaker"].upper()
            move_type = turn.get("move_type", "")
            turn_num = turn["turn"]

            # Update cumulative state based on state_changes
            state_changes = turn.get("state_changes", {})
            self._update_cumulative_state(cumulative_state, state_changes)

            html_parts.append(
                f"""
        <div class="turn {speaker_class}">
            <div class="turn-header">
                {speaker_icon} Turn {turn_num}: {speaker_name}
                <span style="color: #dcdcaa;">[{move_type}]</span>
            </div>

            <div class="utterance">
                <strong>Utterance:</strong> {turn["utterance"]}
            </div>"""
            )

            # Mocking indicators
            if speaker_class == "user":
                html_parts.append(
                    """
            <div class="metadata">
                <span class="mock-indicator">MOCKED NLU</span>
                In production, utterance would be processed by Claude 4.5 Sonnet to extract:
                <ul>
                    <li>Dialogue move type (answer, question, request, greet, etc.)</li>
                    <li>Semantic content (propositions, entities)</li>
                    <li>Contextual information (reference resolution)</li>
                </ul>
            </div>"""
                )
            else:
                html_parts.append(
                    """
            <div class="metadata">
                <span class="mock-indicator">MOCKED NLG</span>
                In production, system move would be generated by Claude 4.5 Haiku based on:
                <ul>
                    <li>Selected dialogue move from Larsson select phase</li>
                    <li>Current information state (QUD, commitments)</li>
                    <li>Domain-specific templates and conventions</li>
                </ul>
            </div>"""
                )

            # Larsson algorithm explanation
            if "larsson_rule" in turn:
                html_parts.append(
                    f"""
            <div class="algorithm-box">
                <div class="title">📚 Larsson Algorithm:</div>
                {turn["larsson_rule"]}
            </div>"""
                )

            # Business explanation
            if "business_explanation" in turn:
                html_parts.append(
                    f"""
            <div class="metadata">
                <strong>Business Context:</strong> {turn["business_explanation"]}
            </div>"""
                )

            # State changes (delta)
            if state_changes:
                html_parts.append(
                    """
            <div class="state-box">
                <h4>🔄 State Changes (Delta)</h4>
                <div class="json-view">
                    <pre>"""
                )
                html_parts.append(json.dumps(state_changes, indent=2))
                html_parts.append("</pre>\n                </div>\n            </div>")

            # Full state snapshot after this turn
            html_parts.append(
                """
            <div class="state-box">
                <h4>📸 Full State After Turn</h4>
                <div class="json-view">
                    <pre>"""
            )
            html_parts.append(json.dumps(cumulative_state, indent=2))
            html_parts.append("</pre>\n                </div>\n            </div>")

            html_parts.append("        </div>")

        html_parts.append("    </div>")

        # Larsson algorithms demonstrated
        html_parts.append(
            """
    <div class="section">
        <h2>📚 Larsson Algorithms Demonstrated</h2>
        <div class="metadata">
            This scenario demonstrates the following algorithms from Larsson (2002):
        </div>
        <ul style="line-height: 1.8;">"""
        )

        for algo in self.scenario.get("larsson_algorithms", []):
            html_parts.append(f"            <li>{algo}</li>")

        html_parts.append("        </ul>\n    </div>")

        # Performance metrics
        html_parts.append(
            """
    <div class="section">
        <h2>📊 Performance Metrics</h2>
        <div class="json-view">
            <pre>"""
        )
        html_parts.append(json.dumps(self.scenario.get("metrics", {}), indent=2))
        html_parts.append("</pre>\n        </div>\n    </div>")

        # Implementation notes
        html_parts.append(
            """
    <div class="section">
        <h2>🔧 Implementation Notes</h2>
        <div class="metadata">
            <h3>What's Real vs. Mocked</h3>
            <ul>
                <li><strong style="color: #4ec9b0;">REAL:</strong> All Larsson update rules
                (integrate, select phases)</li>
                <li><strong style="color: #4ec9b0;">REAL:</strong> QUD stack management
                (push, pop, accommodation)</li>
                <li><strong style="color: #4ec9b0;">REAL:</strong> Commitment tracking
                (shared.com)</li>
                <li><strong style="color: #4ec9b0;">REAL:</strong> Plan formation and
                progression</li>
                <li><strong style="color: #4ec9b0;">REAL:</strong> Domain semantic layer
                (NDA domain model)</li>
                <li><span class="mock-indicator">MOCKED:</span> NLU - Utterance interpretation
                (would use Claude 4.5 Sonnet)</li>
                <li><span class="mock-indicator">MOCKED:</span> NLG - Response generation
                (would use Claude 4.5 Haiku)</li>
            </ul>

            <h3>State Management Architecture</h3>
            <p>The Information State consists of:</p>
            <ul>
                <li><strong>SHARED.QUD:</strong> Stack of questions under discussion
                (LIFO ordering)</li>
                <li><strong>SHARED.COM:</strong> Shared commitments (agreed facts)</li>
                <li><strong>PRIVATE.ISSUES:</strong> Pending issues to be raised</li>
                <li><strong>PRIVATE.PLAN:</strong> Hierarchical plan structures</li>
                <li><strong>PRIVATE.AGENDA:</strong> System's current action agenda</li>
            </ul>

            <h3>Code Locations</h3>
            <ul>
                <li><code>src/ibdm/core/dialogue_state.py</code> - InformationState class</li>
                <li><code>src/ibdm/core/update_rules.py</code> - Larsson update rules</li>
                <li><code>src/ibdm/core/domain.py</code> - Domain semantic layer</li>
                <li><code>src/ibdm/domains/nda_domain.py</code> - NDA-specific domain model</li>
                <li><code>src/ibdm/engines/burr_dialogue_manager.py</code> - Burr integration</li>
            </ul>
        </div>
    </div>"""
        )

        # Footer
        html_parts.append(
            """
    <div class="footer">
        <p>Generated by IBDM Engineer Demo System</p>
        <p>Issue-Based Dialogue Management • Larsson (2002) Implementation</p>
        <p>For production integration details, see docs/llm_configuration.md</p>
    </div>
</body>
</html>"""
        )

        return "\n".join(html_parts)

    def _parse_question_from_string(self, question_str: str) -> Question | None:
        """Load a Question from semantic representation string.

        This loads from SEMANTIC NOTATION loaded from JSON (e.g., "?x.legal_entities(x)"),
        NOT from natural language text (e.g., "What are the parties?").
        This is loading semantic representations for the NLG demo, not NLU.

        Args:
            question_str: Semantic notation like "?x.legal_entities(x)" or "?nda_type"

        Returns:
            Question object or None if loading fails
        """
        import re

        from ibdm.core.questions import WhQuestion, YNQuestion

        if not question_str:
            return None

        # Wh-question pattern: ?x.predicate(x) or ?x.predicate
        wh_match = re.match(r"\?(\w+)\.(\w+)(?:\(.*\))?", question_str)
        if wh_match:
            variable = wh_match.group(1)
            predicate = wh_match.group(2)
            return WhQuestion(variable=variable, predicate=predicate)

        # Simple proposition (default to YN question)
        proposition = question_str.replace("?", "").strip()
        if proposition:
            return YNQuestion(proposition=proposition)

        return None

    def _create_plan_from_description(self, plan_description: str) -> Plan:
        """Create a Plan object from description string.

        Args:
            plan_description: String describing the plan

        Returns:
            Plan object
        """
        # Simple plan creation - in production this would be more sophisticated
        return Plan(plan_type="findout", content=plan_description, status="active")

    def _create_system_dialogue_move(self, turn_data: dict[str, Any]) -> Any:
        """Create DialogueMove for SYSTEM turns (for NLG generation).

        IMPORTANT ARCHITECTURAL NOTE:
        This method LOADS semantic representations from JSON
        (e.g., state_changes.qud_pushed: "?x.legal_entities(x)") and converts
        them to DialogueMove objects. This is NOT parsing natural language text.

        What we ARE doing (loading semantic representations for NLG demo):
        - Load semantic representations from JSON → DialogueMove
        - Example: "?x.legal_entities(x)" → WhQuestion(variable="x", predicate="legal_entities")
        - Pass DialogueMove to NLG → Generate natural language

        What we are NOT doing (NLU - future work):
        - Infer DialogueMove from natural language text
        - Example: "What are the parties?" → WhQuestion (this would be NLU)

        The demo shows: MEANING → TEXT (NLG)
        Future work:    TEXT → MEANING (NLU)

        For NLG purposes, we only construct moves for system turns, since user
        turns are already natural language in the scenario JSON.

        Args:
            turn_data: Turn data from scenario JSON (must be system turn)

        Returns:
            DialogueMove with properly typed content

        Note:
            This loads from semantic annotations in JSON, not utterance text.
            Inferring from utterance text would be NLU (not implemented).
        """
        from ibdm.core.moves import DialogueMove

        move_type = turn_data.get("move_type", "unknown")
        speaker = turn_data.get("speaker", "system")
        state_changes = turn_data.get("state_changes", {})

        # Construct content based on move_type
        content: Any = None

        if move_type == "ask":
            # For ask moves, extract the Question from state_changes
            # This Question will be passed to NLG to generate the question text
            question_str = state_changes.get("qud_pushed", "")
            content = self._parse_question_from_string(question_str)
            if content is None:
                # Fallback to utterance if we can't parse the question
                content = turn_data.get("utterance", "")
        else:
            # For other system moves (greet, assert, etc.), use utterance as content
            content = turn_data.get("utterance", "")

        return DialogueMove(move_type=move_type, content=content, speaker=speaker)

    def _apply_state_changes(self, state: InformationState, state_changes: dict[str, Any]) -> None:
        """Apply state_changes from JSON to InformationState.

        This method updates the real InformationState object based on the
        state_changes recorded in the scenario JSON files.

        Args:
            state: InformationState to update
            state_changes: Dictionary of state changes from turn
        """
        # Handle QUD operations
        if "qud_pushed" in state_changes:
            question_str = state_changes["qud_pushed"]
            question = self._parse_question_from_string(question_str)
            if question:
                state.shared.qud.append(question)

        if "qud_popped" in state_changes:
            if state.shared.qud:
                state.shared.qud.pop()

        # Handle commitments
        if "commitment_added" in state_changes:
            proposition = state_changes["commitment_added"]
            state.shared.commitments.add(proposition)

        # Handle private issues (IBiS3)
        if "issues_added" in state_changes:
            issues_list = state_changes["issues_added"]
            if isinstance(issues_list, list):
                for issue_item in issues_list:
                    issue_str = str(issue_item)  # Ensure string type
                    question = self._parse_question_from_string(issue_str)
                    if question:
                        state.private.issues.append(question)

        # Handle plans
        if "plan_created" in state_changes:
            plan_description = state_changes["plan_created"]
            plan = self._create_plan_from_description(plan_description)
            state.private.plan.append(plan)

        if "plan_status" in state_changes:
            # Update status of most recent plan
            if state.private.plan:
                status = state_changes["plan_status"]
                state.private.plan[-1].status = status

    def _update_cumulative_state(
        self, cumulative_state: dict[str, Any], state_changes: dict[str, Any]
    ) -> None:
        """Update cumulative state based on state changes.

        DEPRECATED: This method maintains the old dictionary-based state
        for backward compatibility with HTML reports. New code should use
        _apply_state_changes() which updates the real InformationState.

        Args:
            cumulative_state: Running state to update (dict)
            state_changes: Changes from this turn
        """
        # Handle QUD operations
        if "qud_pushed" in state_changes:
            cumulative_state["qud"].append(state_changes["qud_pushed"])

        if "qud_popped" in state_changes:
            if cumulative_state["qud"]:
                cumulative_state["qud"].pop()

        # Handle commitments
        if "commitment_added" in state_changes:
            cumulative_state["commitments"].append(state_changes["commitment_added"])

        # Handle issues
        if "issues_added" in state_changes:
            cumulative_state["private_issues"].extend(state_changes["issues_added"])

        if "issues_pending" in state_changes:
            # Simplified: just track the count
            remaining = state_changes["issues_pending"]
            cumulative_state["issues_remaining"] = remaining

        # Handle plans
        if "plan_created" in state_changes:
            cumulative_state["plans"].append(state_changes["plan_created"])

        if "plan_status" in state_changes:
            cumulative_state["plan_status"] = state_changes["plan_status"]

        # Track latest move type
        cumulative_state["latest_move"] = state_changes.get(
            "move_type", cumulative_state.get("latest_move")
        )

        # Handle other state changes generically
        for key, value in state_changes.items():
            if key not in [
                "qud_pushed",
                "qud_popped",
                "commitment_added",
                "issues_added",
                "issues_pending",
                "plan_created",
            ]:
                cumulative_state[key] = value


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
    parser.add_argument(
        "--nlg-mode",
        choices=["off", "compare", "replace"],
        default="off",
        help=(
            "NLG mode: 'off' (scripted only, default), 'compare' (show both), 'replace' (NLG only)"
        ),
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
        demo = BusinessDemo(
            scenario_file,
            verbose=not args.quiet,
            auto_advance=not args.manual,
            nlg_mode=args.nlg_mode,
        )

        demo.run_scenario()

        # Generate reports
        if not args.no_report:
            business_report, engineer_report = demo.export_report(args.output_dir)
            print(f"✓ Business report saved: {business_report}")
            print(f"✓ Engineer report saved: {engineer_report}")

    print("\n✓ All demonstrations complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
