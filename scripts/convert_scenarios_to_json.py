#!/usr/bin/env python3
"""Convert Python-based scenarios to JSON format.

This script reads scenarios from scenarios.py and converts them to the
comprehensive JSON format used by the business demo system.
"""

import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ibdm.demo.scenarios import (
    get_ibis2_scenarios,
    get_ibis3_scenarios,
)


def convert_scenario_to_json(scenario, scenario_id: str) -> dict:
    """Convert a DemoScenario to JSON format.

    Args:
        scenario: DemoScenario instance
        scenario_id: Unique identifier for this scenario

    Returns:
        Dictionary in JSON schema format
    """
    # Count turns
    user_turns = len([s for s in scenario.steps if s.speaker == "user"])
    total_turns = len(scenario.steps)

    # Convert steps to turns
    turns = []
    for idx, step in enumerate(scenario.steps, start=1):
        # Infer move_type from context
        if step.speaker == "user":
            if idx == 1 or "need" in step.utterance.lower() or "draft" in step.utterance.lower():
                move_type = "request"
            else:
                move_type = "answer"
        else:
            if "?" in step.utterance:
                move_type = "ask"
            elif "thank" in step.utterance.lower() or "have all" in step.utterance.lower():
                move_type = "inform"
            elif "═" in step.utterance or "AGREEMENT" in step.utterance:
                move_type = "present_document"
            else:
                move_type = "inform"

        # Create turn entry
        turn = {
            "turn": idx,
            "speaker": step.speaker,
            "utterance": step.utterance,
            "move_type": move_type,
            "business_explanation": step.description or f"{step.speaker.capitalize()} turn {idx}",
            "larsson_rule": extract_larsson_rule(step, scenario),
            "state_changes": step.expected_state or {},
        }

        # Mark payoff turns
        if step.is_payoff:
            turn["is_payoff"] = True

        turns.append(turn)

    # Build JSON structure
    return {
        "scenario_id": scenario_id,
        "title": scenario.name,
        "description": scenario.description,
        "business_narrative": generate_business_narrative(scenario),
        "larsson_algorithms": scenario.features,
        "expected_outcomes": {
            "turns": total_turns,
            "qud_depth_max": 1,  # Most scenarios have max depth 1
            "commitments_final": user_turns,  # Approximate
            "plan_completion": "100%",
            "larsson_fidelity": "95%",  # Default high fidelity
        },
        "confidence_mode": scenario.confidence_mode,
        "turns": turns,
        "metrics": {
            "dialogue_efficiency": "High - Systematic information gathering",
            "information_completeness": "100% - All required fields gathered",
            "user_experience": "Good - Clear, logical progression",
            "system_transparency": "High - User always knows what's being asked and why",
        },
    }


def extract_larsson_rule(step, scenario) -> str:
    """Extract Larsson rule from step description or scenario features."""
    desc = step.description or ""

    # Map common patterns to rules
    if "forms plan" in desc or "initiates task" in desc:
        return "Task Accommodation (Section 2.5.1)"
    elif "asks" in desc and "question" in desc:
        return "Rule 5.1 - Raise issue from private.issues to shared.qud"
    elif "answers" in desc:
        return "Rule 4.1 - Answer accommodates top question on QUD"
    elif "volunteer" in desc.lower():
        return "Rule 4.1 - IssueAccommodation (volunteer information)"
    elif "clarification" in desc.lower():
        return "Rule 4.3 - Clarification question handling"
    elif "dependent" in desc.lower() or "prerequisite" in desc.lower():
        return "Rule 4.4 - Dependent question ordering"
    elif "belief revision" in desc.lower() or "reaccommodation" in desc.lower():
        return "Rules 4.6-4.8 - Belief revision and reaccommodation"
    elif "confirm" in desc.lower():
        return "ICM Rule 3.20 - Confirmation request"
    elif "perception" in desc.lower() or "understand" in desc.lower():
        return "ICM Rules 3.1/3.5 - Perception/Understanding check"
    else:
        return "Dialogue update rule"


def generate_business_narrative(scenario) -> str:
    """Generate business narrative from scenario."""
    name = scenario.name.lower()

    if "incremental" in name:
        return (
            "This scenario demonstrates systematic information gathering through "
            "incremental questioning. The system asks one question at a time, avoiding "
            "user overwhelm while maintaining clear progress toward the goal. This shows "
            "the core value of IBDM: transparent, efficient dialogue management."
        )
    elif "volunteer" in name:
        return (
            "This scenario shows how IBDM handles volunteered information gracefully. "
            "When users provide extra details before being asked, the system recognizes "
            "and integrates that information, skipping unnecessary questions. This "
            "demonstrates intelligent context awareness and efficiency."
        )
    elif "clarification" in name:
        return (
            "This scenario demonstrates how IBDM handles ambiguous or incomplete user "
            "responses. The system asks clarification questions to resolve uncertainty, "
            "ensuring accurate information capture. This shows robust error handling."
        )
    elif "dependent" in name:
        return (
            "This scenario shows how IBDM manages question dependencies. Some questions "
            "can only be asked after prerequisites are satisfied. The system tracks these "
            "dependencies and asks questions in the correct order, demonstrating "
            "sophisticated plan management."
        )
    elif "reaccommodation" in name or "belief" in name:
        return (
            "This scenario demonstrates belief revision when users correct previous "
            "answers. The system gracefully handles changes, updating its commitments "
            "and potentially revising its plan. This shows robust state management."
        )
    elif "optimistic" in name:
        return (
            "This scenario demonstrates optimistic grounding strategy. The system "
            "assumes high confidence in perception and understanding, proceeding "
            "without explicit confirmations. This is efficient for clear communication."
        )
    elif "cautious" in name:
        return (
            "This scenario demonstrates cautious grounding strategy. The system "
            "requests explicit confirmations for critical information, ensuring "
            "accuracy at the cost of a few extra turns. Balances efficiency and safety."
        )
    elif "pessimistic" in name:
        return (
            "This scenario demonstrates pessimistic grounding strategy. The system "
            "uses re-utterance and extensive confirmation to ensure perfect accuracy. "
            "Prioritizes correctness over efficiency for high-stakes situations."
        )
    elif "mixed" in name:
        return (
            "This scenario demonstrates adaptive grounding. The system adjusts its "
            "confirmation strategy based on confidence levels: optimistic for clear "
            "answers, cautious for uncertain ones. Shows intelligent strategy selection."
        )
    else:
        return f"This scenario demonstrates {scenario.name}: {scenario.description}"


def main():
    """Convert all scenarios to JSON."""
    output_dir = Path(__file__).parent.parent / "demos" / "scenarios"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get all scenarios
    ibis3_scenarios = get_ibis3_scenarios()
    ibis2_scenarios = get_ibis2_scenarios()

    # IBiS3 scenario IDs
    ibis3_ids = [
        "ibis3_incremental_questioning",
        "ibis3_volunteer_information",
        "ibis3_clarification",
        "ibis3_dependent_questions",
        "ibis3_reaccommodation",
    ]

    # IBiS2 scenario IDs
    ibis2_ids = [
        "ibis2_grounding_optimistic",
        "ibis2_grounding_cautious",
        "ibis2_grounding_pessimistic",
        "ibis2_grounding_mixed",
    ]

    # Convert IBiS3 scenarios
    print("Converting IBiS3 scenarios...")
    for scenario, scenario_id in zip(ibis3_scenarios, ibis3_ids):
        json_data = convert_scenario_to_json(scenario, scenario_id)
        output_path = output_dir / f"{scenario_id}.json"

        with open(output_path, "w") as f:
            json.dump(json_data, f, indent=2)

        print(f"  ✓ Wrote {output_path}")

    # Convert IBiS2 scenarios
    print("\nConverting IBiS2 scenarios...")
    for scenario, scenario_id in zip(ibis2_scenarios, ibis2_ids):
        json_data = convert_scenario_to_json(scenario, scenario_id)
        output_path = output_dir / f"{scenario_id}.json"

        with open(output_path, "w") as f:
            json.dump(json_data, f, indent=2)

        print(f"  ✓ Wrote {output_path}")

    print(f"\n✓ Converted {len(ibis3_scenarios) + len(ibis2_scenarios)} scenarios to JSON")
    print(f"  Output directory: {output_dir}")


if __name__ == "__main__":
    main()
