#!/usr/bin/env python3
"""
Generate Larsson Fidelity Report.

This script evaluates the IBDM implementation against Larsson (2002)
and generates a comprehensive fidelity report.

Usage:
    python scripts/generate_fidelity_report.py [--output FILENAME] [--json]

Example:
    python scripts/generate_fidelity_report.py --output reports/fidelity_2025-11-14.txt
    python scripts/generate_fidelity_report.py --json --output reports/fidelity.json
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

from ibdm.domains.nda_domain import get_nda_domain
from ibdm.engine.dialogue_engine import DialogueMoveEngine
from ibdm.metrics.larsson_fidelity import evaluate_larsson_fidelity


def generate_text_report(score) -> str:
    """Generate human-readable text report."""
    lines = [
        "=" * 80,
        "IBDM LARSSON FIDELITY REPORT",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 80,
        "",
        score.summary(),
        "",
        "=" * 80,
        "DETAILED BREAKDOWN",
        "=" * 80,
        "",
    ]

    # Add detailed breakdown for each component
    components = [
        ("Architectural Compliance", score.architectural_compliance),
        ("Information State Structure", score.information_state),
        ("Semantic Operations Coverage", score.semantic_operations),
        ("Rules Coverage", score.rules_coverage),
        ("Domain Independence", score.domain_independence),
    ]

    for name, metric in components:
        lines.extend(
            [
                f"\n### {name}",
                f"Score: {metric.score:.1f}/100",
                f"Status: {'✓ PASS' if metric.passed else '✗ FAIL'}",
                "",
                "Details:",
            ]
        )

        for key, value in metric.details.items():
            lines.append(f"  • {key}: {value:.1f}/100")

        if metric.issues:
            lines.extend(["", "Issues:"])
            for issue in metric.issues:
                lines.append(f"  • {issue}")

        if metric.recommendations:
            lines.extend(["", "Recommendations:"])
            for rec in metric.recommendations:
                lines.append(f"  • {rec}")

        lines.append("")

    # Add conclusion
    lines.extend(
        [
            "=" * 80,
            "CONCLUSION",
            "=" * 80,
            "",
        ]
    )

    if score.overall_score >= 90:
        lines.append(
            f"✓ EXCELLENT: Overall fidelity {score.overall_score:.1f}% meets target (≥90%)"
        )
        lines.append("  Implementation is highly faithful to Larsson (2002)")
    elif score.overall_score >= 80:
        lines.append(f"✓ GOOD: Overall fidelity {score.overall_score:.1f}% is strong")
        lines.append("  Minor improvements needed to reach target")
    elif score.overall_score >= 70:
        lines.append(f"⚠ MODERATE: Overall fidelity {score.overall_score:.1f}% needs improvement")
        lines.append("  Several areas require attention")
    else:
        lines.append(f"✗ LOW: Overall fidelity {score.overall_score:.1f}% is insufficient")
        lines.append("  Significant work needed for Larsson compliance")

    lines.extend(
        [
            "",
            "Target: ≥90% (py-trindikit baseline: ~95%)",
            "",
            "=" * 80,
        ]
    )

    return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generate Larsson fidelity report")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)", default=None)
    parser.add_argument("--json", "-j", action="store_true", help="Output in JSON format")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.verbose:
        print("Initializing IBDM components...")

    # Initialize components
    engine = DialogueMoveEngine(agent_id="system")
    domain = get_nda_domain()

    if args.verbose:
        print("Running Larsson fidelity evaluation...")

    # Evaluate fidelity
    score = evaluate_larsson_fidelity(engine=engine, domain=domain)

    if args.verbose:
        print("Generating report...")

    # Generate report
    if args.json:
        report = json.dumps(score.to_dict(), indent=2)
    else:
        report = generate_text_report(score)

    # Output report
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report)
        print(f"Report written to: {output_path}")
    else:
        print(report)

    # Exit with status code based on pass/fail
    return 0 if score.passed else 1


if __name__ == "__main__":
    exit(main())
