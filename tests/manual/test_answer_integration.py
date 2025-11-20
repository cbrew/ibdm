#!/usr/bin/env python3
"""Quick test to verify Answer integration is working."""

from ibdm.core.information_state import InformationState
from ibdm.core.moves import DialogueMove
from ibdm.core.answers import Answer
from ibdm.core.questions import WhQuestion
from ibdm.engine.dialogue_engine import DialogueMoveEngine
from ibdm.rules import create_integration_rules, create_selection_rules
from ibdm.rules.update_rules import RuleSet

# Create engine
rules = RuleSet()
for rule in create_integration_rules():
    rules.add_rule(rule)
for rule in create_selection_rules():
    rules.add_rule(rule)
engine = DialogueMoveEngine(agent_id="system", rules=rules)

# Create initial state
state = InformationState(agent_id="system")

# Push a question to QUD
question = WhQuestion(predicate="nda_type", variable="x")
state.shared.qud.append(question)

print(f"Initial QUD: {state.shared.qud}")
print(f"Top QUD: {state.shared.top_qud()}")

# Create an answer
answer = Answer(content="mutual", question_ref=question)
answer_move = DialogueMove(move_type="answer", content=answer, speaker="user")

print(f"\nAnswer question_ref: {answer.question_ref}")
print(f"Answer content: {answer.content}")

# Integrate the answer
new_state = engine.integrate(answer_move, state)

print(f"\nAfter integration:")
print(f"QUD: {new_state.shared.qud}")
print(f"Commitments: {new_state.shared.commitments}")
print(f"Top QUD: {new_state.shared.top_qud()}")
