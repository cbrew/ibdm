import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.getcwd(), "src"))

from ibdm.core import InformationState
from ibdm.demo.scenario_explorer import ScenarioExplorer
from ibdm.demo.scenarios import get_ibis3_scenarios
from ibdm.domains.nda_domain import get_nda_domain


def test_viz_integration():
    print("Testing Visualization Integration...")

    # Setup
    scenario = get_ibis3_scenarios()[0]
    domain = get_nda_domain()
    state = InformationState(agent_id="system")
    state.private.beliefs["domain"] = domain

    explorer = ScenarioExplorer(scenario, state, domain)

    # Check initial state
    print("\n1. Initial State:")
    explorer.display_state()

    # Simulate a move
    print("\n2. Simulating Move...")
    # Add a commitment manually
    state.shared.commitments.add("parties(Acme Corp and Smith Inc)")
    explorer.capture_snapshot("After move 1")

    # Check state again
    print("\n3. Updated State:")
    explorer.display_state()

    # Check diff
    print("\n4. State Diff:")
    explorer.display_diff()

    print("\nTest Complete!")


if __name__ == "__main__":
    test_viz_integration()
