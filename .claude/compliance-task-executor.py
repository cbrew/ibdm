#!/usr/bin/env python3
"""
Larsson Compliance Task Executor.

Automatically selects and executes beads tasks that are likely to improve
Larsson framework compliance, measuring before/after impact.

Usage:
    # Interactive mode
    python .claude/compliance-task-executor.py

    # Auto-execute highest-impact task
    python .claude/compliance-task-executor.py --auto

    # Show top candidates without executing
    python .claude/compliance-task-executor.py --show-top 5 --dry-run

    # Target specific component
    python .claude/compliance-task-executor.py --component "Rules Coverage"

Author: Claude Code
Date: 2025-11-14
"""

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class TaskScore:
    """Scored task with impact prediction."""

    task_id: str
    title: str
    description: str
    priority: int
    status: str
    issue_type: str
    labels: list[str]
    score: float
    rationale: list[str]


def load_open_tasks() -> list[dict[str, Any]]:
    """
    Load open tasks from beads database.

    Returns:
        List of open task dictionaries
    """
    beads_file = Path(".beads/issues.jsonl")
    if not beads_file.exists():
        print("ERROR: .beads/issues.jsonl not found", file=sys.stderr)
        print("Run from project root directory", file=sys.stderr)
        sys.exit(1)

    tasks = []
    with open(beads_file) as f:
        for line in f:
            task = json.loads(line)
            if task.get("status") == "open":
                tasks.append(task)

    return tasks


def calculate_impact_score(task: dict[str, Any]) -> TaskScore:
    """
    Calculate likelihood that task will improve Larsson compliance.

    Uses heuristic scoring based on:
    - Labels (40% weight)
    - Task type (20% weight)
    - Priority (20% weight)
    - Phase alignment (10% weight)
    - Ready status (10% weight)

    Args:
        task: Task dictionary from beads

    Returns:
        TaskScore with score and rationale
    """
    score = 0.0
    rationale = []

    labels = set(task.get("labels", []))

    # Label analysis (40% total)
    if labels & {"burr", "state-extraction", "stateless", "architectural"}:
        points = 0.15
        score += points
        rationale.append(f"+{points:.2f}: High-impact architectural labels")

    if labels & {"rules", "ibis1", "update-rules", "selection-rules"}:
        points = 0.15
        score += points
        rationale.append(f"+{points:.2f}: Rules coverage improvement")

    if labels & {"domain", "semantic", "predicates"}:
        points = 0.10
        score += points
        rationale.append(f"+{points:.2f}: Domain independence improvement")

    if labels & {"qud", "information-state"}:
        points = 0.10
        score += points
        rationale.append(f"+{points:.2f}: Information state improvement")

    if labels & {"refactoring", "larsson-alignment"}:
        points = 0.10
        score += points
        rationale.append(f"+{points:.2f}: General Larsson alignment")

    # Task type (20%)
    task_type = task.get("issue_type", "task")
    type_weights = {
        "task": 0.20,
        "bug": 0.15,
        "feature": 0.12,
        "epic": 0.05,
    }
    points = type_weights.get(task_type, 0.10)
    score += points
    rationale.append(f"+{points:.2f}: Task type '{task_type}'")

    # Priority (20%)
    priority = task.get("priority", 2)
    priority_weights = {0: 0.20, 1: 0.15, 2: 0.10}
    points = priority_weights.get(priority, 0.05)
    score += points
    rationale.append(f"+{points:.2f}: Priority P{priority}")

    # Phase alignment (10%)
    if "phase-2.5" in labels:
        points = 0.10
        score += points
        rationale.append(f"+{points:.2f}: Current phase alignment")
    elif "phase-3" in labels or "phase-3.5" in labels:
        points = 0.08
        score += points
        rationale.append(f"+{points:.2f}: Near-term phase alignment")

    # Ready status (10%)
    status = task.get("status", "open")
    if status == "open":
        points = 0.10
        score += points
        rationale.append(f"+{points:.2f}: Task is ready (no blockers)")

    return TaskScore(
        task_id=task["id"],
        title=task["title"],
        description=task.get("description", ""),
        priority=priority,
        status=status,
        issue_type=task_type,
        labels=list(labels),
        score=score,
        rationale=rationale,
    )


def display_task_ranking(
    scored_tasks: list[TaskScore], limit: int = 10, verbose: bool = False
) -> None:
    """
    Display ranked tasks with scores.

    Args:
        scored_tasks: List of scored tasks
        limit: Number of tasks to display
        verbose: Show full rationale
    """
    print(f"\n{'=' * 80}")
    print(f"Top {limit} High-Impact Tasks for Larsson Compliance")
    print(f"{'=' * 80}\n")

    for i, task in enumerate(scored_tasks[:limit], 1):
        print(f"{i}. {task.task_id}: {task.title}")
        score_str = f"Score: {task.score:.2f}/1.00"
        priority_str = f"Priority: P{task.priority}"
        type_str = f"Type: {task.issue_type}"
        print(f"   {score_str} | {priority_str} | {type_str}")
        print(f"   Labels: {', '.join(task.labels[:5])}")

        if verbose:
            print("\n   Rationale:")
            for reason in task.rationale:
                print(f"     • {reason}")
            if task.description:
                desc_lines = task.description.split("\n")[:3]
                print("\n   Description:")
                for line in desc_lines:
                    print(f"     {line[:70]}")
                if len(task.description.split("\n")) > 3:
                    print("     ...")

        print()


def display_selected_task(task: TaskScore) -> None:
    """
    Display the selected task with full details.

    Args:
        task: Selected TaskScore
    """
    print("\n" + "=" * 80)
    print("SELECTED TASK")
    print("=" * 80)
    print(f"\nID: {task.task_id}")
    print(f"Title: {task.title}")
    print(f"Priority: P{task.priority}")
    print(f"Type: {task.issue_type}")
    print(f"Impact Score: {task.score:.2f}/1.00")
    print(f"\nLabels: {', '.join(task.labels)}")

    print("\nSelection Rationale:")
    for reason in task.rationale:
        print(f"  • {reason}")

    if task.description:
        print("\nDescription:")
        for line in task.description.split("\n")[:10]:
            print(f"  {line}")
        if len(task.description.split("\n")) > 10:
            print("  ...")

    print("\n" + "=" * 80)


def predict_impact(task: TaskScore, current_scores: dict[str, float]) -> None:
    """
    Predict compliance impact based on task labels.

    Args:
        task: Task to predict impact for
        current_scores: Current compliance component scores
    """
    labels = set(task.labels)

    predictions = []

    if labels & {"burr", "state-extraction", "stateless", "architectural"}:
        current = current_scores.get("architectural_compliance", 0)
        predicted = min(100, current + 5)
        predictions.append(("Architectural Compliance", current, predicted))

    if labels & {"rules", "ibis1", "update-rules", "selection-rules"}:
        current = current_scores.get("rules_coverage", 0)
        predicted = min(100, current + 8)
        predictions.append(("Rules Coverage", current, predicted))

    if labels & {"domain", "semantic", "predicates"}:
        current = current_scores.get("domain_independence", 0)
        predicted = min(100, current + 5)
        predictions.append(("Domain Independence", current, predicted))

    if labels & {"qud", "information-state"}:
        current = current_scores.get("information_state", 0)
        predicted = min(100, current + 3)
        predictions.append(("Information State", current, predicted))

    if predictions:
        print("\nPredicted Compliance Impact:")
        for component, current, predicted in predictions:
            delta = predicted - current
            print(f"  {component}: {current:.1f} → {predicted:.1f} (+{delta:.1f})")

        # Estimate overall impact
        overall_current = current_scores.get("overall", 0)
        avg_delta = sum(p[2] - p[1] for p in predictions) / len(predictions)
        overall_predicted = min(100, overall_current + avg_delta * 0.2)  # Weighted
        overall_delta = overall_predicted - overall_current
        overall_line = (
            f"  Overall (estimated): {overall_current:.1f} → "
            f"{overall_predicted:.1f} (+{overall_delta:.1f})"
        )
        print(overall_line)


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Larsson Compliance Task Executor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--auto",
        action="store_true",
        help="Auto-execute without confirmation",
    )
    parser.add_argument(
        "--show-top",
        type=int,
        default=1,
        metavar="N",
        help="Show top N candidates (default: 1)",
    )
    parser.add_argument(
        "--min-score",
        type=float,
        default=0.5,
        metavar="SCORE",
        help="Minimum impact score threshold (default: 0.5)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show selection without executing",
    )
    parser.add_argument(
        "--task",
        type=str,
        metavar="ID",
        help="Execute specific task by ID",
    )
    parser.add_argument(
        "--component",
        type=str,
        metavar="NAME",
        help="Focus on specific compliance component",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed rationale",
    )

    args = parser.parse_args()

    # Print header
    print("\n" + "=" * 80)
    print("LARSSON COMPLIANCE TASK EXECUTOR")
    print("=" * 80)

    # Step 1: Take baseline snapshot
    print("\nStep 1: Taking baseline compliance snapshot...")
    print("-" * 80)

    import subprocess

    baseline_file = Path("/tmp/compliance-baseline.json")

    # Try to take snapshot, but don't fail in dry-run mode if not available
    result = subprocess.run(
        [
            "python",
            ".claude/larsson-metrics-helper.py",
            "snapshot",
            "--output",
            str(baseline_file),
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        if args.dry_run:
            # In dry-run mode, use mock data
            print("(Using mock baseline data for dry-run)")
            baseline = {
                "overall_score": 87.5,
                "passed": False,
                "components": {
                    "architectural_compliance": {
                        "name": "Architectural Compliance",
                        "score": 95.0,
                        "passed": True,
                    },
                    "information_state": {
                        "name": "Information State",
                        "score": 100.0,
                        "passed": True,
                    },
                    "semantic_operations": {
                        "name": "Semantic Operations",
                        "score": 75.0,
                        "passed": False,
                    },
                    "rules_coverage": {
                        "name": "Rules Coverage",
                        "score": 70.0,
                        "passed": False,
                    },
                    "domain_independence": {
                        "name": "Domain Independence",
                        "score": 85.0,
                        "passed": True,
                    },
                },
            }
        else:
            print("ERROR: Failed to take baseline snapshot", file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            sys.exit(1)
    else:
        # Load baseline
        with open(baseline_file) as f:
            baseline = json.load(f)

    overall = baseline["overall_score"]
    passed = baseline["passed"]
    print(f"\nBaseline Compliance: {overall:.1f}/100 {'✓ PASS' if passed else '✗ FAIL'}")

    # Show component scores
    for comp_name, comp_data in baseline["components"].items():
        score = comp_data["score"]
        comp_passed = comp_data["passed"]
        display_name = comp_data.get("name", comp_name.replace("_", " ").title())
        status = "✓" if comp_passed else "✗"
        print(f"  {display_name}: {score:.1f}/100 {status}")

    # Extract current scores for predictions
    current_scores = {
        "overall": overall,
        "architectural_compliance": baseline["components"]["architectural_compliance"]["score"],
        "information_state": baseline["components"]["information_state"]["score"],
        "semantic_operations": baseline["components"]["semantic_operations"]["score"],
        "rules_coverage": baseline["components"]["rules_coverage"]["score"],
        "domain_independence": baseline["components"]["domain_independence"]["score"],
    }

    # Step 2: Load and score tasks
    print("\nStep 2: Analyzing open tasks...")
    print("-" * 80)

    tasks = load_open_tasks()
    print(f"Found {len(tasks)} open tasks")

    # Score all tasks
    scored_tasks = [calculate_impact_score(task) for task in tasks]

    # Filter by component if specified
    if args.component:
        component_keywords = {
            "Architectural Compliance": {"burr", "state", "architectural"},
            "Information State": {"qud", "information-state"},
            "Semantic Operations": {"semantic", "operations", "resolves", "combines"},
            "Rules Coverage": {"rules", "ibis1", "update-rules", "selection-rules"},
            "Domain Independence": {"domain", "predicates"},
        }
        keywords = component_keywords.get(args.component, set())
        scored_tasks = [t for t in scored_tasks if any(kw in t.labels for kw in keywords)]
        print(f"Filtered to {len(scored_tasks)} tasks for component '{args.component}'")

    # Filter by minimum score
    scored_tasks = [t for t in scored_tasks if t.score >= args.min_score]
    print(f"Found {len(scored_tasks)} tasks above threshold (score >= {args.min_score})")

    # Sort by score
    scored_tasks.sort(key=lambda t: t.score, reverse=True)

    if not scored_tasks:
        print("\nNo tasks meet the criteria.")
        print("Try lowering --min-score or removing --component filter")
        sys.exit(0)

    # Step 3: Display candidates
    if args.show_top > 1:
        display_task_ranking(scored_tasks, limit=args.show_top, verbose=args.verbose)
    elif args.dry_run:
        # In dry-run with show-top=1, show full details of top task
        display_task_ranking(scored_tasks, limit=1, verbose=True)

    # Select task
    if args.task:
        # Find specified task
        selected = None
        for task in scored_tasks:
            if task.task_id == args.task:
                selected = task
                break
        if not selected:
            print(f"ERROR: Task '{args.task}' not found or below threshold", file=sys.stderr)
            sys.exit(1)
    else:
        # Select highest-scoring task
        selected = scored_tasks[0]

    # Display selected task
    if not (args.show_top > 1 or args.dry_run):
        # Only show if not already displayed in ranking
        display_selected_task(selected)
        predict_impact(selected, current_scores)

    if args.dry_run:
        print("\n(Dry run mode - not executing)")
        sys.exit(0)

    # Step 4: Confirmation
    if not args.auto:
        print("\n" + "=" * 80)
        response = input("Execute this task? [Y/n] ").strip().lower()
        if response and response not in ["y", "yes"]:
            print("Cancelled.")
            sys.exit(0)

    # Step 5: Execute task
    print("\n" + "=" * 80)
    print(f"Step 3: Executing task {selected.task_id}...")
    print("=" * 80)
    print("\nThis step requires manual implementation by the agent.")
    print("The agent should:")
    print(f"  1. Read task details: {selected.task_id}")
    print("  2. Implement required changes")
    print("  3. Run quality checks (ruff, pyright, pytest)")
    print("  4. Commit changes")
    print("\nWhen complete, run:")
    print("  python .claude/larsson-metrics-helper.py snapshot --output /tmp/after.json")
    compare_line = (
        "  python .claude/larsson-metrics-helper.py compare "
        "--before /tmp/compliance-baseline.json --after /tmp/after.json"
    )
    print(compare_line)
    print()

    # Note: Actual execution would be done by the agent
    # This script focuses on task selection and metrics

    sys.exit(0)


if __name__ == "__main__":
    main()
