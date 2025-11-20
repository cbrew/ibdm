#!/usr/bin/env python3
"""Debug Answer integration in the demo context."""

from ibdm.core.information_state import InformationState
from ibdm.core.moves import DialogueMove
from ibdm.core.answers import Answer
from ibdm.core.questions import WhQuestion, AltQuestion
from ibdm.engine.dialogue_engine import DialogueMoveEngine
from ibdm.rules import create_integration_rules, create_selection_rules
from ibdm.rules.update_rules import RuleSet
from ibdm.domains.nda_domain import get_nda_domain

# Create engine
rules = RuleSet()
for rule in create_integration_rules():
    rules.add_rule(rule)
for rule in create_selection_rules():
    rules.add_rule(rule)
engine = DialogueMoveEngine(agent_id="system", rules=rules)

# Create initial state
state = InformationState(agent_id="system")

# Simulate the NDA scenario up to Turn 4
# Turn 1: User requests NDA
request_move = DialogueMove(move_type="request", content="I need to draft an NDA", speaker="user")
state = engine.integrate(request_move, state)

print(f"After Turn 1 (request):")
print(f"  QUD: {[str(q) for q in state.shared.qud]}")
print(f"  Issues: {[str(q) for q in state.private.issues]}")
print(f"  Plans: {[p.plan_type for p in state.private.plan]}")

# Turn 2: System asks about parties (simulate by pushing question)
# In reality, selection rules would do this
parties_q = WhQuestion(predicate="legal_entities", variable="x")
state.shared.qud.append(parties_q)

print(f"\nAfter Turn 2 (system asks parties):")
print(f"  Top QUD: {state.shared.top_qud()}")

# Turn 3: User answers parties
parties_answer = Answer(content="Acme Corporation and TechStart Inc", question_ref=state.shared.top_qud())
parties_move = DialogueMove(move_type="answer", content=parties_answer, speaker="user")
state = engine.integrate(parties_move, state)

print(f"\nAfter Turn 3 (user answers parties):")
print(f"  QUD: {[str(q) for q in state.shared.qud]}")
print(f"  Commitments: {state.shared.commitments}")

# Turn 4: System asks about NDA type
# The question should be in private.issues from the plan
print(f"\nIssues available:")
for issue in state.private.issues:
    print(f"  {issue}")

# Find the nda_type question from issues
nda_type_q = None
for issue in state.private.issues:
    if hasattr(issue, 'predicate') and 'nda' in str(issue).lower():
        nda_type_q = issue
        break
    elif hasattr(issue, 'alternatives'):  # AltQuestion
        nda_type_q = issue
        break

if nda_type_q:
    print(f"\nFound nda_type question from issues: {nda_type_q}")
    print(f"  Type: {type(nda_type_q)}")
    state.shared.qud.append(nda_type_q)
else:
    # Fallback
    print("\nUsing fallback WhQuestion")
    nda_type_q = WhQuestion(predicate="nda_type", variable="x")
    state.shared.qud.append(nda_type_q)

print(f"\nAfter Turn 4 (system asks nda_type):")
print(f"  Top QUD: {state.shared.top_qud()}")
print(f"  Top QUD type: {type(state.shared.top_qud())}")

# Turn 5: User answers "Mutual"
top_qud_before = state.shared.top_qud()
print(f"\nBefore Turn 5 integration:")
print(f"  Top QUD: {top_qud_before}")
print(f"  QUD list: {state.shared.qud}")

nda_answer = Answer(content="Mutual", question_ref=top_qud_before)
nda_move = DialogueMove(move_type="answer", content=nda_answer, speaker="user")

print(f"\nAnswer details:")
print(f"  content: {nda_answer.content}")
print(f"  question_ref: {nda_answer.question_ref}")
print(f"  question_ref == top_qud: {nda_answer.question_ref == top_qud_before}")
print(f"  question_ref is top_qud: {nda_answer.question_ref is top_qud_before}")

# Check if domain.resolves would work
domain = get_nda_domain()
print(f"\nDomain resolves check:")
print(f"  domain.resolves(answer, question): {domain.resolves(nda_answer, top_qud_before)}")

state = engine.integrate(nda_move, state)

print(f"\nAfter Turn 5 (user answers Mutual):")
print(f"  QUD: {[str(q) for q in state.shared.qud]}")
print(f"  Top QUD: {state.shared.top_qud()}")
print(f"  Commitments: {state.shared.commitments}")
