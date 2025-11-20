#!/usr/bin/env python3
"""Trace through _integrate_answer to see where it's failing."""

from ibdm.core.answers import Answer
from ibdm.core.information_state import InformationState
from ibdm.core.moves import DialogueMove
from ibdm.core.questions import AltQuestion
from ibdm.domains.nda_domain import get_nda_domain

# Create state with AltQuestion on QUD
state = InformationState(agent_id="system")
question = AltQuestion(alternatives=["mutual", "one-way"])
state.shared.qud.append(question)

print("Initial state:")
print(f"  QUD: {state.shared.qud}")
print(f"  Top QUD: {state.shared.top_qud()}")

# Create answer
answer = Answer(content="Mutual", question_ref=question)
move = DialogueMove(move_type="answer", content=answer, speaker="user")

# Store move in beliefs (this is what the engine does)
state.private.beliefs["_temp_move"] = move

# Now manually run the integration logic
domain = get_nda_domain()

print("\nChecking preconditions:")
print(f"  isinstance(move.content, Answer): {isinstance(move.content, Answer)}")

# Check volunteer answer handling
volunteer_answer_handled = False
print(f"  private.issues: {state.private.issues}")
for issue in state.private.issues[:]:
    if domain.resolves(answer, issue):
        print(f"    Answer resolves issue: {issue}")
        volunteer_answer_handled = True
        break

print(f"  volunteer_answer_handled: {volunteer_answer_handled}")

if not volunteer_answer_handled:
    print("\nChecking QUD:")
    top_question = state.shared.top_qud()
    print(f"  top_question: {top_question}")
    print(f"  type: {type(top_question)}")

    if top_question:
        resolves_result = domain.resolves(answer, top_question)
        print(f"  domain.resolves(answer, top_question): {resolves_result}")

        if resolves_result:
            print("\n  ✓ Should pop QUD and add commitment")
            print(f"  Before pop: QUD = {state.shared.qud}")
            state.shared.pop_qud()
            print(f"  After pop: QUD = {state.shared.qud}")

            commitment = f"{top_question}: {answer.content}"
            state.shared.commitments.add(commitment)
            print(f"  Added commitment: {commitment}")
        else:
            print("\n  ✗ Invalid answer - would need clarification")

print("\nFinal state:")
print(f"  QUD: {state.shared.qud}")
print(f"  Commitments: {state.shared.commitments}")
