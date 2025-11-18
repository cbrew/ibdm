"""Automated scenario validation for all demo scenarios.

Validates that all scenarios reach their payoff states using expected-path-only mode.
Generates comprehensive validation report.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ibdm.demo.path_explorer import PathExplorer, PathNode
from ibdm.demo.scenarios import (
    DemoScenario,
    get_ibis2_scenarios,
    get_ibis3_scenarios,
    get_ibis4_scenarios,
)
from ibdm.domains.nda_domain import get_nda_domain
from ibdm.domains.travel_domain import get_travel_domain


@dataclass
class ScenarioTestResult:
    """Results from testing a single scenario."""

    scenario_name: str
    category: str  # IBiS-2, IBiS-3, or IBiS-4
    has_distractors: bool
    has_payoff: bool
    reaches_payoff: bool  # Does expected path reach payoff?
    total_paths: int
    payoff_paths: int
    max_score: float
    issues: list[str]
    demo_quality: str  # "Excellent", "Good", "Fair", "Poor"


def get_domain_for_scenario(scenario: DemoScenario) -> Any:
    """Get appropriate domain for a scenario.

    Args:
        scenario: Demo scenario

    Returns:
        Domain instance (NDA or Travel)
    """
    if "nda" in scenario.name.lower() or "clarification" in scenario.name.lower():
        return get_nda_domain()
    return get_travel_domain()


def validate_scenario(
    scenario: DemoScenario,
    category: str,
    max_depth: int = 20,
    expected_only: bool = True,
) -> ScenarioTestResult:
    """Validate a single scenario.

    Args:
        scenario: Scenario to validate
        category: IBiS category (IBiS-2, IBiS-3, IBiS-4)
        max_depth: Maximum exploration depth
        expected_only: Use expected-path-only mode

    Returns:
        Test results for the scenario
    """
    # Get domain
    domain = get_domain_for_scenario(scenario)

    # Check scenario properties
    has_distractors = False  # TODO: Could check SCENARIO_DISTRACTORS
    has_payoff = any(step.is_payoff for step in scenario.steps)

    issues: list[str] = []

    # Run exploration
    explorer = PathExplorer(
        scenario,
        domain,
        beam_size=200,
        turn_penalty=5.0,
        expected_only=expected_only,
    )

    try:
        result = explorer.explore_paths(max_depth=max_depth)
    except Exception as e:
        issues.append(f"Exploration failed: {e}")
        return ScenarioTestResult(
            scenario_name=scenario.name,
            category=category,
            has_distractors=has_distractors,
            has_payoff=has_payoff,
            reaches_payoff=False,
            total_paths=0,
            payoff_paths=0,
            max_score=0.0,
            issues=issues,
            demo_quality="Poor",
        )

    # Check if any paths reach payoff
    payoff_paths: list[PathNode] = []
    for depth_paths in result.paths_by_depth.values():
        for node in depth_paths:
            # Check current step and upcoming system turns
            for step_idx in range(node.step_index, min(node.step_index + 5, len(scenario.steps))):
                step = scenario.steps[step_idx]
                if step.is_payoff:
                    payoff_paths.append(node)
                    break

    reaches_payoff = len(payoff_paths) > 0
    max_score = max((n.score for n in payoff_paths), default=0.0)

    # Assess demo quality
    if not has_payoff:
        demo_quality = "Poor"
        issues.append("No payoff state defined")
    elif not reaches_payoff:
        demo_quality = "Poor"
        issues.append("Expected path does not reach payoff")
    elif max_score < 400:
        demo_quality = "Fair"
        issues.append(f"Low score ({max_score:.1f}), may have scoring issues")
    elif len(scenario.steps) < 5:
        demo_quality = "Fair"
        issues.append("Very short scenario, limited educational value")
    elif len(scenario.steps) > 15:
        demo_quality = "Good"
    else:
        demo_quality = "Excellent"

    return ScenarioTestResult(
        scenario_name=scenario.name,
        category=category,
        has_distractors=has_distractors,
        has_payoff=has_payoff,
        reaches_payoff=reaches_payoff,
        total_paths=result.total_paths,
        payoff_paths=len(payoff_paths),
        max_score=max_score,
        issues=issues,
        demo_quality=demo_quality,
    )


def validate_all_scenarios() -> list[ScenarioTestResult]:
    """Validate all demo scenarios.

    Returns:
        List of test results for all scenarios
    """
    results: list[ScenarioTestResult] = []

    # IBiS-3 scenarios
    for scenario in get_ibis3_scenarios():
        print(f"Testing {scenario.name}...")
        result = validate_scenario(scenario, "IBiS-3")
        results.append(result)
        status = "✓" if result.reaches_payoff else "✗"
        print(f"  {status} {result.demo_quality} - Score: {result.max_score:.1f}")

    # IBiS-2 scenarios
    for scenario in get_ibis2_scenarios():
        print(f"Testing {scenario.name}...")
        result = validate_scenario(scenario, "IBiS-2")
        results.append(result)
        status = "✓" if result.reaches_payoff else "✗"
        print(f"  {status} {result.demo_quality} - Score: {result.max_score:.1f}")

    # IBiS-4 scenarios
    for scenario in get_ibis4_scenarios():
        print(f"Testing {scenario.name}...")
        result = validate_scenario(scenario, "IBiS-4")
        results.append(result)
        status = "✓" if result.reaches_payoff else "✗"
        print(f"  {status} {result.demo_quality} - Score: {result.max_score:.1f}")

    return results


def generate_validation_report(results: list[ScenarioTestResult]) -> str:
    """Generate comprehensive validation report.

    Args:
        results: Test results for all scenarios

    Returns:
        Formatted report string
    """
    # Get git hash and timestamp
    try:
        git_hash = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], text=True
        ).strip()
    except Exception:
        git_hash = "unknown"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines: list[str] = []
    lines.append("=" * 80)
    lines.append("SCENARIO VALIDATION REPORT")
    lines.append("=" * 80)
    lines.append(f"Timestamp: {timestamp}")
    lines.append(f"Git Hash:  {git_hash}")
    lines.append("Mode:      Expected-path-only (no distractors)")
    lines.append("")

    # Summary statistics
    total = len(results)
    passing = sum(1 for r in results if r.reaches_payoff)
    excellent = sum(1 for r in results if r.demo_quality == "Excellent")
    good = sum(1 for r in results if r.demo_quality == "Good")
    fair = sum(1 for r in results if r.demo_quality == "Fair")
    poor = sum(1 for r in results if r.demo_quality == "Poor")

    lines.append("SUMMARY")
    lines.append("-" * 80)
    lines.append(f"Total Scenarios:      {total}")
    lines.append(f"Reaching Payoff:      {passing}/{total} ({passing * 100 // total}%)")
    lines.append("")
    lines.append("Demo Quality Distribution:")
    lines.append(f"  Excellent: {excellent}")
    lines.append(f"  Good:      {good}")
    lines.append(f"  Fair:      {fair}")
    lines.append(f"  Poor:      {poor}")
    lines.append("")

    # Group by category
    for category in ["IBiS-3", "IBiS-2", "IBiS-4"]:
        category_results = [r for r in results if r.category == category]
        if not category_results:
            continue

        lines.append(f"{category} SCENARIOS ({len(category_results)} total)")
        lines.append("-" * 80)

        for result in category_results:
            status = "✓" if result.reaches_payoff else "✗"
            lines.append(f"{status} {result.scenario_name}")
            lines.append(f"   Quality: {result.demo_quality}")
            lines.append(f"   Score:   {result.max_score:.1f}")
            lines.append(f"   Paths:   {result.payoff_paths}/{result.total_paths} reach payoff")

            if result.issues:
                lines.append("   Issues:")
                for issue in result.issues:
                    lines.append(f"     - {issue}")

            lines.append("")

    # Recommendations
    lines.append("RECOMMENDATIONS")
    lines.append("-" * 80)

    failing = [r for r in results if not r.reaches_payoff]
    if failing:
        lines.append("Scenarios NOT reaching payoff (CRITICAL):")
        for r in failing:
            lines.append(f"  - {r.scenario_name} ({r.category})")
            for issue in r.issues:
                lines.append(f"      {issue}")
        lines.append("")

    top_demos = sorted(
        [r for r in results if r.reaches_payoff],
        key=lambda r: (
            {"Excellent": 4, "Good": 3, "Fair": 2, "Poor": 1}[r.demo_quality],
            r.max_score,
        ),
        reverse=True,
    )[:5]

    if top_demos:
        lines.append("Top 5 Demo Scenarios (Recommended for Showcase):")
        for i, r in enumerate(top_demos, 1):
            lines.append(f"  {i}. {r.scenario_name} ({r.category})")
            lines.append(f"     Quality: {r.demo_quality}, Score: {r.max_score:.1f}")
        lines.append("")

    lines.append("=" * 80)

    return "\n".join(lines)


def main() -> None:
    """Main entry point for automated validation."""
    print("\n" + "=" * 80)
    print("  AUTOMATED SCENARIO VALIDATION")
    print("=" * 80)
    print()

    # Run validation
    results = validate_all_scenarios()

    # Generate report
    print("\n" + "=" * 80)
    print("  GENERATING REPORT")
    print("=" * 80)
    print()

    report = generate_validation_report(results)
    print(report)

    # Save to file
    try:
        git_hash = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], text=True
        ).strip()
    except Exception:
        git_hash = "unknown"

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"reports/scenario-validation-{timestamp}-{git_hash}.txt"

    # Ensure reports directory exists
    import os

    os.makedirs("reports", exist_ok=True)

    with open(filename, "w") as f:
        f.write(report)

    print(f"\n✓ Report saved to: {filename}")
    print()


if __name__ == "__main__":
    main()
