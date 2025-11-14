#!/usr/bin/env python3
"""
Larsson Compliance Metrics Helper Script.

Provides CLI for measuring Larsson framework compliance before/after tasks
and reporting deltas.

Usage:
    # Take snapshot
    python .claude/larsson-metrics-helper.py snapshot --output /tmp/before.json

    # Compare snapshots
    python .claude/larsson-metrics-helper.py compare \
        --before /tmp/before.json \
        --after /tmp/after.json

    # Wrap task execution
    python .claude/larsson-metrics-helper.py wrap-task \
        --command "pytest tests/" \
        --description "Run tests"

    # Session tracking
    python .claude/larsson-metrics-helper.py start-session --session-id "feature-123"
    python .claude/larsson-metrics-helper.py check-session --session-id "feature-123"
    python .claude/larsson-metrics-helper.py end-session --session-id "feature-123"

Author: Claude Code
Date: 2025-11-14
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_components() -> tuple[Any, Any, Any, Any]:
    """
    Load IBDM components for metrics evaluation.

    Returns:
        Tuple of (engine, burr_app, domain, rule_set)
    """
    try:
        # Import components
        from ibdm.core.domain import DomainModel
        from ibdm.rules import RuleSet

        # Initialize components with defaults
        domain = DomainModel(name="compliance_check")
        rule_set = RuleSet()

        # Engine and Burr app are optional (graceful degradation)
        engine = None
        burr_app = None

        try:
            from ibdm.engine import DialogueMoveEngine

            engine = DialogueMoveEngine
        except ImportError:
            pass

        return engine, burr_app, domain, rule_set

    except ImportError as e:
        print(f"Error: Failed to import IBDM components: {e}", file=sys.stderr)
        print("Ensure IBDM is installed: uv pip install --system -e .", file=sys.stderr)
        sys.exit(1)


def take_snapshot(verbose: bool = False, components: list[str] | None = None) -> dict[str, Any]:
    """
    Take a Larsson compliance metrics snapshot.

    Args:
        verbose: Include full details and recommendations
        components: Which components to measure (default: all)

    Returns:
        Dictionary with metrics snapshot
    """
    from ibdm.metrics import evaluate_larsson_fidelity

    # Load components
    engine, burr_app, domain, rule_set = load_components()

    # Evaluate metrics
    score = evaluate_larsson_fidelity(
        engine=engine,
        burr_app=burr_app,
        domain=domain,
        rule_set=rule_set,
    )

    # Convert to dict
    result = score.to_dict()

    # Add timestamp
    result["timestamp"] = datetime.now(timezone.utc).isoformat()

    # Filter components if specified
    if components:
        filtered_components = {}
        for comp in components:
            comp_key = comp.lower().replace(" ", "_")
            if comp_key in result["components"]:
                filtered_components[comp_key] = result["components"][comp_key]
        result["components"] = filtered_components

    # Remove verbose details if not requested
    if not verbose:
        for comp_data in result["components"].values():
            if "recommendations" in comp_data:
                comp_data.pop("recommendations", None)

    return result


def format_delta(before: float, after: float) -> str:
    """Format delta with sign and color indicators."""
    delta = after - before
    if abs(delta) < 0.01:
        return "(no change)"
    sign = "+" if delta > 0 else ""
    return f"({sign}{delta:.1f})"


def compare_snapshots(
    before: dict[str, Any],
    after: dict[str, Any],
    format_type: str = "detailed",
    threshold: float = 1.0,
) -> str:
    """
    Compare two metric snapshots and generate report.

    Args:
        before: Before snapshot
        after: After snapshot
        format_type: Output format (summary|detailed|json)
        threshold: Minimum change to highlight (default: 1.0)

    Returns:
        Formatted comparison report
    """
    # Extract scores
    before_overall = before["overall_score"]
    after_overall = after["overall_score"]
    delta_overall = after_overall - before_overall

    # Check pass status change
    before_passed = before["passed"]
    after_passed = after["passed"]

    if format_type == "json":
        # JSON format
        delta_components = {}
        for comp_name, comp_data in after["components"].items():
            before_comp = before["components"].get(comp_name, {})
            delta_components[comp_name] = comp_data["score"] - before_comp.get("score", 0)

        result = {
            "before": before,
            "after": after,
            "delta": {
                "overall_score": delta_overall,
                "components": delta_components,
                "passed_before": before_passed,
                "passed_after": after_passed,
            },
        }
        return json.dumps(result, indent=2)

    elif format_type == "summary":
        # Summary format
        status = ""
        if after_passed and not before_passed:
            status = " ✓ NOW PASSING"
        elif not after_passed and before_passed:
            status = " ✗ NOW FAILING"
        elif after_passed:
            status = " ✓"
        else:
            status = " ✗"

        delta_str = format_delta(before_overall, after_overall)
        return f"Larsson Compliance: {before_overall:.1f} → {after_overall:.1f} {delta_str}{status}"

    else:
        # Detailed format
        lines = []
        lines.append("Larsson Compliance Delta Report")
        lines.append("=" * 80)

        # Overall score
        status = ""
        if after_passed and not before_passed:
            status = " ✓ NOW PASSING"
        elif not after_passed and before_passed:
            status = " ✗ NOW FAILING"
        elif after_passed:
            status = " ✓"
        else:
            status = " ✗"

        lines.append(
            f"Overall: {before_overall:.1f} → {after_overall:.1f} "
            f"{format_delta(before_overall, after_overall)}{status}"
        )
        lines.append("")

        # Component changes
        lines.append("Component Changes:")
        for comp_name, comp_data in after["components"].items():
            before_comp = before["components"].get(comp_name, {})
            before_score = before_comp.get("score", 0)
            after_score = comp_data["score"]
            delta = after_score - before_score

            # Skip if below threshold
            if abs(delta) < threshold:
                indicator = "[=]"
            elif delta > 0:
                indicator = "[+]"
            else:
                indicator = "[-]"

            comp_display = comp_data.get("name", comp_name.replace("_", " ").title())
            status_mark = " ✓" if comp_data.get("passed", False) else " ✗"

            lines.append(
                f"  {indicator} {comp_display}: {before_score:.1f} → {after_score:.1f} "
                f"{format_delta(before_score, after_score)}{status_mark}"
            )

        lines.append("")

        # Issues analysis
        before_issues = set()
        after_issues = set()

        for comp_data in before["components"].values():
            before_issues.update(comp_data.get("issues", []))

        for comp_data in after["components"].values():
            after_issues.update(comp_data.get("issues", []))

        resolved_issues = before_issues - after_issues
        new_issues = after_issues - before_issues

        lines.append("Issues:")
        if resolved_issues:
            lines.append(f"  Resolved ({len(resolved_issues)}):")
            for issue in sorted(resolved_issues):
                lines.append(f"    ✓ {issue}")
        else:
            lines.append("  Resolved (0)")

        lines.append("")

        if new_issues:
            lines.append(f"  New ({len(new_issues)}):")
            for issue in sorted(new_issues):
                lines.append(f"    ✗ {issue}")
        else:
            lines.append("  New (0):")
            lines.append("    (none)")

        lines.append("")

        # Recommendations
        all_recommendations = set()
        for comp_data in after["components"].values():
            all_recommendations.update(comp_data.get("recommendations", []))

        if all_recommendations:
            lines.append(f"Recommendations ({len(all_recommendations)} remaining):")
            for rec in sorted(all_recommendations):
                lines.append(f"  • {rec}")
        else:
            lines.append("Recommendations: None")

        return "\n".join(lines)


def wrap_task(
    command: str,
    description: str | None = None,
    fail_on_regression: bool = False,
    auto_commit: bool = False,
) -> int:
    """
    Execute command with before/after metrics tracking.

    Args:
        command: Command to execute
        description: Human-readable task description
        fail_on_regression: Exit with error if compliance decreases
        auto_commit: Create git commit if compliance improves

    Returns:
        Exit code from command
    """
    print(f"Task: {description or command}")
    print("=" * 80)
    print()

    # Take before snapshot
    print("Taking baseline metrics snapshot...")
    before = take_snapshot()
    print(f"Baseline: {before['overall_score']:.1f}/100 {'✓' if before['passed'] else '✗'}")
    print()

    # Execute command
    print(f"Executing: {command}")
    print("-" * 80)
    result = subprocess.run(command, shell=True)
    print("-" * 80)
    print()

    # Take after snapshot
    print("Taking post-task metrics snapshot...")
    after = take_snapshot()
    print(f"Result: {after['overall_score']:.1f}/100 {'✓' if after['passed'] else '✗'}")
    print()

    # Compare
    print("Compliance Delta:")
    print("-" * 80)
    report = compare_snapshots(before, after, format_type="detailed")
    print(report)
    print()

    # Check for regression
    delta = after["overall_score"] - before["overall_score"]
    if fail_on_regression and delta < 0:
        print(f"ERROR: Compliance regressed by {abs(delta):.1f} points", file=sys.stderr)
        return 1

    # Auto-commit if improved
    if auto_commit and delta > 0:
        commit_msg = f"improve(compliance): +{delta:.1f}% Larsson compliance"
        if description:
            commit_msg += f"\n\n{description}"
        print(f"Auto-committing improvements: {commit_msg}")
        subprocess.run(["git", "add", "-A"])
        subprocess.run(["git", "commit", "-m", commit_msg])

    return result.returncode


def start_session(session_id: str, session_dir: Path = Path("/tmp/ibdm-sessions")) -> None:
    """
    Start a metrics tracking session.

    Args:
        session_id: Unique session identifier
        session_dir: Where to store session snapshots
    """
    session_path = session_dir / session_id
    if session_path.exists():
        print(f"ERROR: Session '{session_id}' already exists", file=sys.stderr)
        print(f"Remove it first: rm -rf {session_path}", file=sys.stderr)
        sys.exit(1)

    # Create session directory
    session_path.mkdir(parents=True, exist_ok=True)

    # Take initial snapshot
    print(f"Starting session: {session_id}")
    snapshot = take_snapshot(verbose=True)
    snapshot_file = session_path / "start.json"
    with open(snapshot_file, "w") as f:
        json.dump(snapshot, f, indent=2)

    print(f"Baseline: {snapshot['overall_score']:.1f}/100 {'✓' if snapshot['passed'] else '✗'}")
    print(f"Session data: {session_path}")


def check_session(session_id: str, session_dir: Path = Path("/tmp/ibdm-sessions")) -> None:
    """
    Check progress during a metrics tracking session.

    Args:
        session_id: Session identifier
        session_dir: Where session snapshots are stored
    """
    session_path = session_dir / session_id
    if not session_path.exists():
        print(f"ERROR: Session '{session_id}' not found", file=sys.stderr)
        sys.exit(1)

    # Load start snapshot
    start_file = session_path / "start.json"
    with open(start_file) as f:
        start_snapshot = json.load(f)

    # Take current snapshot
    print(f"Checking session: {session_id}")
    current_snapshot = take_snapshot(verbose=True)

    # Save checkpoint
    checkpoint_file = session_path / f"checkpoint-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(checkpoint_file, "w") as f:
        json.dump(current_snapshot, f, indent=2)

    # Compare
    print()
    report = compare_snapshots(start_snapshot, current_snapshot, format_type="detailed")
    print(report)


def end_session(session_id: str, session_dir: Path = Path("/tmp/ibdm-sessions")) -> None:
    """
    End a metrics tracking session with final report.

    Args:
        session_id: Session identifier
        session_dir: Where session snapshots are stored
    """
    session_path = session_dir / session_id
    if not session_path.exists():
        print(f"ERROR: Session '{session_id}' not found", file=sys.stderr)
        sys.exit(1)

    # Load start snapshot
    start_file = session_path / "start.json"
    with open(start_file) as f:
        start_snapshot = json.load(f)

    # Take final snapshot
    print(f"Ending session: {session_id}")
    end_snapshot = take_snapshot(verbose=True)

    # Save final snapshot
    end_file = session_path / "end.json"
    with open(end_file, "w") as f:
        json.dump(end_snapshot, f, indent=2)

    # Generate report
    print()
    print("=" * 80)
    print(f"SESSION SUMMARY: {session_id}")
    print("=" * 80)
    print()
    report = compare_snapshots(start_snapshot, end_snapshot, format_type="detailed")
    print(report)
    print()
    print(f"Session data: {session_path}")


def visualize(input_file: Path, output_file: Path) -> None:
    """
    Generate visual dashboard from metrics snapshot.

    Args:
        input_file: Path to metrics snapshot JSON
        output_file: Where to save dashboard image
    """
    try:
        from ibdm.metrics.visualization import MetricsVisualizer
    except ImportError:
        print("ERROR: matplotlib not available", file=sys.stderr)
        print("Install with: uv pip install --system matplotlib", file=sys.stderr)
        sys.exit(1)

    # Load snapshot
    with open(input_file) as f:
        snapshot = json.load(f)

    # Create LarsonFidelityScore object
    from ibdm.metrics import LarsonFidelityScore, MetricResult

    # Reconstruct metric results
    components = {}
    for comp_name, comp_data in snapshot["components"].items():
        components[comp_name] = MetricResult(
            name=comp_data["name"],
            score=comp_data["score"],
            passed=comp_data["passed"],
            details=comp_data.get("details", {}),
            issues=comp_data.get("issues", []),
            recommendations=comp_data.get("recommendations", []),
        )

    score = LarsonFidelityScore(
        architectural_compliance=components.get("architectural_compliance"),
        information_state=components.get("information_state"),
        semantic_operations=components.get("semantic_operations"),
        rules_coverage=components.get("rules_coverage"),
        domain_independence=components.get("domain_independence"),
    )

    # Generate visualization
    print(f"Generating dashboard: {output_file}")
    visualizer = MetricsVisualizer(score)
    visualizer.create_dashboard(str(output_file))
    print("Done!")


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Larsson Compliance Metrics Helper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="subcommand", help="Command to execute")

    # Snapshot command
    snapshot_parser = subparsers.add_parser("snapshot", help="Take metrics snapshot")
    snapshot_parser.add_argument(
        "--output", "-o", type=Path, required=True, help="Output JSON file path"
    )
    snapshot_parser.add_argument(
        "--verbose", "-v", action="store_true", help="Include full details"
    )
    snapshot_parser.add_argument(
        "--components", "-c", nargs="+", help="Which components to measure (default: all)"
    )

    # Compare command
    compare_parser = subparsers.add_parser("compare", help="Compare two snapshots")
    compare_parser.add_argument("--before", "-b", type=Path, required=True, help="Before snapshot")
    compare_parser.add_argument("--after", "-a", type=Path, required=True, help="After snapshot")
    compare_parser.add_argument(
        "--format",
        "-f",
        choices=["summary", "detailed", "json"],
        default="detailed",
        help="Output format",
    )
    compare_parser.add_argument(
        "--threshold",
        "-t",
        type=float,
        default=1.0,
        help="Minimum change to highlight (default: 1.0)",
    )

    # Wrap-task command
    wrap_parser = subparsers.add_parser("wrap-task", help="Execute task with metrics tracking")
    wrap_parser.add_argument("--command", "-c", required=True, help="Command to execute")
    wrap_parser.add_argument("--description", "-d", help="Task description")
    wrap_parser.add_argument(
        "--fail-on-regression", action="store_true", help="Exit with error if compliance decreases"
    )
    wrap_parser.add_argument(
        "--auto-commit", action="store_true", help="Create git commit if compliance improves"
    )

    # Session commands
    start_parser = subparsers.add_parser("start-session", help="Start metrics tracking session")
    start_parser.add_argument("--session-id", required=True, help="Session identifier")
    start_parser.add_argument(
        "--session-dir",
        type=Path,
        default=Path("/tmp/ibdm-sessions"),
        help="Session storage directory",
    )

    check_parser = subparsers.add_parser("check-session", help="Check session progress")
    check_parser.add_argument("--session-id", required=True, help="Session identifier")
    check_parser.add_argument(
        "--session-dir",
        type=Path,
        default=Path("/tmp/ibdm-sessions"),
        help="Session storage directory",
    )

    end_parser = subparsers.add_parser("end-session", help="End session with final report")
    end_parser.add_argument("--session-id", required=True, help="Session identifier")
    end_parser.add_argument(
        "--session-dir",
        type=Path,
        default=Path("/tmp/ibdm-sessions"),
        help="Session storage directory",
    )

    # Visualize command
    viz_parser = subparsers.add_parser("visualize", help="Generate visual dashboard")
    viz_parser.add_argument("--input", "-i", type=Path, required=True, help="Input snapshot JSON")
    viz_parser.add_argument("--output", "-o", type=Path, required=True, help="Output image file")

    # Parse arguments
    args = parser.parse_args()

    if args.subcommand is None:
        parser.print_help()
        sys.exit(1)

    # Execute command
    try:
        if args.subcommand == "snapshot":
            snapshot = take_snapshot(verbose=args.verbose, components=args.components)
            with open(args.output, "w") as f:
                json.dump(snapshot, f, indent=2)
            print(f"Snapshot saved: {args.output}")
            print(
                f"Overall: {snapshot['overall_score']:.1f}/100 "
                f"{'✓ PASS' if snapshot['passed'] else '✗ FAIL'}"
            )

        elif args.subcommand == "compare":
            with open(args.before) as f:
                before = json.load(f)
            with open(args.after) as f:
                after = json.load(f)
            report = compare_snapshots(
                before, after, format_type=args.format, threshold=args.threshold
            )
            print(report)

        elif args.subcommand == "wrap-task":
            exit_code = wrap_task(
                command=args.command,
                description=args.description,
                fail_on_regression=args.fail_on_regression,
                auto_commit=args.auto_commit,
            )
            sys.exit(exit_code)

        elif args.subcommand == "start-session":
            start_session(session_id=args.session_id, session_dir=args.session_dir)

        elif args.subcommand == "check-session":
            check_session(session_id=args.session_id, session_dir=args.session_dir)

        elif args.subcommand == "end-session":
            end_session(session_id=args.session_id, session_dir=args.session_dir)

        elif args.subcommand == "visualize":
            visualize(input_file=args.input, output_file=args.output)

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
