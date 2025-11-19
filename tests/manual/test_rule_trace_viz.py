# Manual test for rule trace visualization in ScenarioExplorer

import os
import sys

# Ensure src is on path
sys.path.insert(0, os.path.join(os.getcwd(), "src"))

from ibdm.core import InformationState
from ibdm.demo.scenario_explorer import ScenarioExplorer
from ibdm.demo.scenarios import get_ibis3_scenarios
from ibdm.domains.travel_domain import get_travel_domain


def test_rule_trace_viz():
    # Setup a simple scenario
    scenarios = get_ibis3_scenarios()
    scenario = scenarios[0]
    state = InformationState(agent_id="system")
    domain = get_travel_domain()
    explorer = ScenarioExplorer(scenario, state, domain)

    # Capture initial snapshot (already done in init)
    explorer.display_state()
    # Simulate a user move (choose first choice)
    choices = explorer.get_current_choices()
    if not choices:
        print("No choices available")
        return
    choice = choices[0]
    explorer.tracker.record_choice(choice)
    # Apply a dummy commitment to change state
    explorer.state.shared.commitments.add("test_commitment")
    explorer.capture_snapshot("After dummy move")
    # Show diff and rule trace
    explorer.display_diff()
    explorer.display_rule_trace()


if __name__ == "__main__":
    test_rule_trace_viz()
