#!/usr/bin/env python3
"""Audit scenarios for structured move compatibility (ibdm-239).

This script identifies:
1. ICM moves that need feedback_level and polarity fields
2. Yes/no answers that need polarity field
3. Understanding questions (icm:und*int) that need WhQuestion.constraints
"""

import json
import re
from pathlib import Path
from typing import TypedDict


class Issue(TypedDict):
    """Type for scenario issues."""

    type: str
    turn: int
    speaker: str
    current: str
    needed: str
    task: str
    icm_signature: str | None
    utterance: str | None


class AuditResult(TypedDict):
    """Type for audit results."""

    scenario_id: str
    title: str
    total_turns: int
    issues: list[Issue]
    needs_update: bool


# ICM pattern in utterances: [icm:LEVEL*POLARITY]
ICM_PATTERN = re.compile(r"\[icm:(\w+)\*(\w+)\]")

# Yes/no patterns
YESNO_PATTERNS = ["yes", "no", "yeah", "nope", "correct", "that's right", "that is right"]


def audit_scenario(scenario_path: Path) -> AuditResult:
    """Audit a single scenario file."""

    with open(scenario_path) as f:
        scenario = json.load(f)

    issues: list[Issue] = []

    for turn in scenario.get("turns", []):
        turn_num = turn.get("turn", 0)
        speaker = turn.get("speaker", "")
        utterance = turn.get("utterance", "").lower()
        move_type = turn.get("move_type", "")

        # Check for ICM notation in utterance
        icm_matches = ICM_PATTERN.findall(turn.get("utterance", ""))
        if icm_matches:
            for level, polarity in icm_matches:
                issue: Issue = {
                    "type": "ICM_MOVE",
                    "turn": turn_num,
                    "speaker": speaker,
                    "icm_signature": f"{level}*{polarity}",
                    "utterance": None,
                    "current": f"Text notation only: [icm:{level}*{polarity}]",
                    "needed": 'Add "move" field with feedback_level and polarity',
                    "task": "ibdm-240",
                }
                issues.append(issue)

        # Check for yes/no answers
        if move_type == "answer" and speaker == "user":
            if any(pattern in utterance for pattern in YESNO_PATTERNS):
                issue: Issue = {
                    "type": "YESNO_ANSWER",
                    "turn": turn_num,
                    "speaker": speaker,
                    "icm_signature": None,
                    "utterance": turn.get("utterance", ""),
                    "current": "No polarity field",
                    "needed": 'Add "move" field with Answer.polarity',
                    "task": "ibdm-241",
                }
                issues.append(issue)

        # Check for understanding questions (icm:und*int)
        if "und*int" in turn.get("utterance", "").lower():
            issue: Issue = {
                "type": "UNDERSTANDING_QUESTION",
                "turn": turn_num,
                "speaker": speaker,
                "icm_signature": None,
                "utterance": turn.get("utterance", ""),
                "current": "No structured Question with constraints",
                "needed": (
                    'Add "move" field with WhQuestion.constraints '
                    "storing confirmed content"
                ),
                "task": "ibdm-242",
            }
            issues.append(issue)

    result: AuditResult = {
        "scenario_id": scenario.get("scenario_id", scenario_path.stem),
        "title": scenario.get("title", ""),
        "total_turns": len(scenario.get("turns", [])),
        "issues": issues,
        "needs_update": len(issues) > 0,
    }
    return result


def main() -> None:
    """Run audit on all scenarios."""
    scenarios_dir = Path("demos/scenarios")

    print("=" * 80)
    print("SCENARIO STRUCTURED MOVE AUDIT (ibdm-239)")
    print("=" * 80)
    print()

    all_results: list[AuditResult] = []

    for scenario_file in sorted(scenarios_dir.glob("*.json")):
        result = audit_scenario(scenario_file)
        all_results.append(result)

    # Group by task
    icm_scenarios: list[AuditResult] = []
    yesno_scenarios: list[AuditResult] = []
    understanding_scenarios: list[AuditResult] = []
    clean_scenarios: list[AuditResult] = []

    for result in all_results:
        if result["needs_update"]:
            has_icm = any(i["type"] == "ICM_MOVE" for i in result["issues"])
            has_yesno = any(i["type"] == "YESNO_ANSWER" for i in result["issues"])
            has_und = any(i["type"] == "UNDERSTANDING_QUESTION" for i in result["issues"])

            if has_icm:
                icm_scenarios.append(result)
            if has_yesno:
                yesno_scenarios.append(result)
            if has_und:
                understanding_scenarios.append(result)
        else:
            clean_scenarios.append(result)

    # Print summary
    print("SUMMARY")
    print("-------")
    print(f"Total scenarios: {len(all_results)}")
    print(f"Clean (no updates needed): {len(clean_scenarios)}")
    print(f"Need ICM move updates (ibdm-240): {len(icm_scenarios)}")
    print(f"Need Answer.polarity updates (ibdm-241): {len(yesno_scenarios)}")
    print(f"Need WhQuestion.constraints updates (ibdm-242): {len(understanding_scenarios)}")
    print()

    # Print detailed findings for ibdm-240
    print("=" * 80)
    print("TASK ibdm-240: IBiS2 Grounding Scenarios Need Structured ICM Moves")
    print("=" * 80)
    print()
    for result in icm_scenarios:
        icm_issues = [i for i in result["issues"] if i["type"] == "ICM_MOVE"]
        print(f"📄 {result['scenario_id']}")
        print(f"   {len(icm_issues)} ICM moves need structure:")
        for issue in icm_issues:
            print(f"   - Turn {issue['turn']}: {issue['icm_signature']}")
        print()

    # Print detailed findings for ibdm-241
    print("=" * 80)
    print("TASK ibdm-241: Scenarios Need Answer.polarity for Yes/No Answers")
    print("=" * 80)
    print()
    for result in yesno_scenarios:
        yesno_issues = [i for i in result["issues"] if i["type"] == "YESNO_ANSWER"]
        print(f"📄 {result['scenario_id']}")
        print(f"   {len(yesno_issues)} yes/no answers need polarity:")
        for issue in yesno_issues:
            print(f'   - Turn {issue["turn"]}: "{issue["utterance"]}"')
        print()

    # Print detailed findings for ibdm-242
    print("=" * 80)
    print("TASK ibdm-242: Scenarios Need WhQuestion.constraints for Understanding Questions")
    print("=" * 80)
    print()
    for result in understanding_scenarios:
        und_issues = [i for i in result["issues"] if i["type"] == "UNDERSTANDING_QUESTION"]
        print(f"📄 {result['scenario_id']}")
        print(f"   {len(und_issues)} understanding questions need constraints:")
        for issue in und_issues:
            utterance = issue['utterance'] or ''
            print(f"   - Turn {issue['turn']}: {utterance[:60]}...")
        print()

    # Print clean scenarios
    print("=" * 80)
    print("CLEAN SCENARIOS (No Updates Needed)")
    print("=" * 80)
    print()
    for result in clean_scenarios:
        print(f"✅ {result['scenario_id']}")
    print()

    # Save detailed report
    report_path = Path("reports/scenario_move_audit_ibdm-239.json")
    report_path.parent.mkdir(exist_ok=True)

    with open(report_path, "w") as f:
        json.dump(
            {
                "audit_date": "2025-11-22",
                "task": "ibdm-239",
                "summary": {
                    "total_scenarios": len(all_results),
                    "clean_scenarios": len(clean_scenarios),
                    "icm_scenarios": len(icm_scenarios),
                    "yesno_scenarios": len(yesno_scenarios),
                    "understanding_scenarios": len(understanding_scenarios),
                },
                "results": all_results,
            },
            f,
            indent=2,
        )

    print(f"Detailed report saved to: {report_path}")
    print()

    # Print action items
    print("=" * 80)
    print("ACTION ITEMS")
    print("=" * 80)
    print()
    print("ibdm-240: Update these scenarios with structured ICM moves:")
    for result in icm_scenarios:
        print(f"  - {result['scenario_id']}")
    print()
    print("ibdm-241: Update these scenarios with Answer.polarity:")
    for result in yesno_scenarios:
        print(f"  - {result['scenario_id']}")
    print()
    print("ibdm-242: Update these scenarios with WhQuestion.constraints:")
    for result in understanding_scenarios:
        print(f"  - {result['scenario_id']}")
    print()


if __name__ == "__main__":
    main()
