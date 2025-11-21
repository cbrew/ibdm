#!/usr/bin/env python3
"""Test script to verify QUD push/pop operations and logging."""

import os
import logging
os.environ["IBDM_DEBUG"] = "qud"

# Import after setting env var
from ibdm.core.information_state import InformationState, SharedIS
from ibdm.core import WhQuestion

# Ensure logging is configured
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(name)s: %(message)s')
logging.getLogger("ibdm.core.information_state").setLevel(logging.DEBUG)

print("Testing QUD operations...")
print("=" * 60)

# Create a simple information state
state = InformationState()

# Create some test questions
question1 = WhQuestion(predicate="nda_type", variable="X")
question2 = WhQuestion(
    predicate="clarification",
    variable="X",
    constraints={"is_clarification": True}
)

print("\n1. Initial QUD state:")
print(f"   QUD depth: {len(state.shared.qud)}")
print(f"   Top QUD: {state.shared.top_qud()}")

print("\n2. Pushing question1 (nda_type)...")
state.shared.push_qud(question1)
print(f"   QUD depth: {len(state.shared.qud)}")
print(f"   Top QUD: {state.shared.top_qud()}")

print("\n3. Pushing question2 (clarification)...")
state.shared.push_qud(question2)
print(f"   QUD depth: {len(state.shared.qud)}")
print(f"   Top QUD: {state.shared.top_qud()}")

print("\n4. Popping QUD...")
popped = state.shared.pop_qud()
print(f"   Popped: {popped}")
print(f"   QUD depth: {len(state.shared.qud)}")
print(f"   Top QUD: {state.shared.top_qud()}")

print("\n5. Popping QUD again...")
popped = state.shared.pop_qud()
print(f"   Popped: {popped}")
print(f"   QUD depth: {len(state.shared.qud)}")
print(f"   Top QUD: {state.shared.top_qud()}")

print("\n" + "=" * 60)
print("Test complete!")
