#!/usr/bin/env python3
"""
Demo 1: Core IBDM Concepts

This demo introduces the fundamental concepts of IBDM:
- Questions as semantic objects
- Information State
- Dialogue Moves
- Question resolution

Run: python demos/01_core_concepts.py
"""

from ibdm.core import (
    WhQuestion,
    YNQuestion,
    AltQuestion,
    Answer,
    DialogueMove,
    InformationState,
    PrivateIS,
    SharedIS,
    ControlIS,
    Plan,
)


def demo_questions():
    """Demonstrate semantic question representation"""
    print("=" * 60)
    print("DEMO 1.1: Semantic Question Representation")
    print("=" * 60)

    # Create different question types
    wh_q = WhQuestion(
        variable="weather", predicate="in_location", constraints={"location": "Stockholm"}
    )

    yn_q = YNQuestion(proposition="will_rain", parameters={"location": "Stockholm"})

    alt_q = AltQuestion(alternatives=["business", "economy"])

    print("\n1. Wh-Question: 'What's the weather in Stockholm?'")
    print(f"   Representation: {wh_q}")
    print(f"   Variable: {wh_q.variable}")
    print(f"   Predicate: {wh_q.predicate}")
    print(f"   Constraints: {wh_q.constraints}")

    print("\n2. Y/N Question: 'Will it rain in Stockholm?'")
    print(f"   Representation: {yn_q}")
    print(f"   Proposition: {yn_q.proposition}")

    print("\n3. Alternative Question: 'Business or economy class?'")
    print(f"   Representation: {alt_q}")
    print(f"   Alternatives: {alt_q.alternatives}")

    print("\n✓ Questions are semantic objects, not strings!")


def demo_question_resolution():
    """Demonstrate how answers resolve questions"""
    print("\n" + "=" * 60)
    print("DEMO 1.2: Question Resolution")
    print("=" * 60)

    # Create a question
    question = WhQuestion(
        variable="weather", predicate="in_location", constraints={"location": "Stockholm"}
    )

    # Create matching answer
    answer = Answer(content={"weather": "sunny, 18°C"}, question_ref=question)

    print(f"\nQuestion: {question}")
    print(f"Answer: {answer.content}")
    print(f"\nDoes answer resolve question? {question.resolves_with(answer)}")

    # Create non-matching answer
    other_question = WhQuestion(
        variable="temperature", predicate="in_location", constraints={"location": "Paris"}
    )
    other_answer = Answer(content={"temperature": "15°C"}, question_ref=other_question)

    print(f"\nOther question: {other_question}")
    print(f"Does this answer resolve first question? {question.resolves_with(other_answer)}")

    print("\n✓ System can determine if answers resolve questions!")


def demo_information_state():
    """Demonstrate Information State structure"""
    print("\n" + "=" * 60)
    print("DEMO 1.3: Information State")
    print("=" * 60)

    # Create a question for the QUD
    weather_q = WhQuestion(
        variable="weather", predicate="in_location", constraints={"location": "Stockholm"}
    )

    # Create Information State
    state = InformationState(
        private=PrivateIS(
            beliefs={"weather_data": {"Stockholm": "sunny, 18°C", "Paris": "rainy, 15°C"}},
            agenda=[],
            plan=[
                Plan(
                    plan_type="respond",
                    content=weather_q,
                    subplans=[],
                )
            ],
            last_utterance=None,
        ),
        shared=SharedIS(
            qud=[weather_q],
            commitments={"location": "Stockholm"},
            last_moves=[],
        ),
        control=ControlIS(
            speaker="user",
            next_speaker="system",
        ),
    )

    print("\nInformation State has three parts:")
    print("\n1. PRIVATE (what only this agent knows):")
    print(f"   Beliefs: {state.private.beliefs}")
    print(f"   Plan: {[str(p) for p in state.private.plan]}")

    print("\n2. SHARED (mutually believed information):")
    print(f"   QUD (Questions Under Discussion): {[str(q) for q in state.shared.qud]}")
    print(f"   Commitments: {state.shared.commitments}")

    print("\n3. CONTROL (dialogue management):")
    print(f"   Current speaker: {state.control.speaker}")
    print(f"   Next speaker: {state.control.next_speaker}")

    print("\n✓ Complete dialogue context captured in structured state!")


def demo_dialogue_moves():
    """Demonstrate dialogue moves"""
    print("\n" + "=" * 60)
    print("DEMO 1.4: Dialogue Moves")
    print("=" * 60)

    weather_q = WhQuestion(
        variable="weather", predicate="in_location", constraints={"location": "Stockholm"}
    )

    # Create different move types
    ask_move = DialogueMove(
        move_type="ask",
        content=weather_q,
        speaker="user",
    )

    answer_move = DialogueMove(
        move_type="answer",
        content="The weather in Stockholm is sunny, 18°C",
        speaker="system",
    )

    assert_move = DialogueMove(
        move_type="assert",
        content={"fact": "Stockholm is the capital of Sweden"},
        speaker="system",
    )

    print("\nDialogue Moves are structured communication acts:")
    print(f"\n1. ASK: {ask_move}")
    print(f"   Type: {ask_move.move_type}")
    print(f"   Content: {ask_move.content}")
    print(f"   Speaker: {ask_move.speaker}")

    print(f"\n2. ANSWER: {answer_move}")
    print(f"   Type: {answer_move.move_type}")
    print(f"   Content: {answer_move.content}")

    print(f"\n3. ASSERT: {assert_move}")
    print(f"   Type: {assert_move.move_type}")
    print(f"   Content: {assert_move.content}")

    print("\n✓ Moves enable reasoning about dialogue structure!")


def demo_qud_stack():
    """Demonstrate QUD stack evolution"""
    print("\n" + "=" * 60)
    print("DEMO 1.5: Questions Under Discussion (QUD) Stack")
    print("=" * 60)

    print("\nSimulating a booking dialogue:")
    print("\nUser: 'I want to book a flight to Paris'")

    # Initial QUD
    qud = [WhQuestion(variable="flight", predicate="book", constraints={"destination": "Paris"})]
    print(f"QUD: {[str(q) for q in qud]}")

    print("\nSystem: 'When would you like to travel?'")
    # System raises sub-question
    qud.append(WhQuestion(variable="date", predicate="travel", constraints={}))
    print(f"QUD: {[str(q) for q in qud]}")

    print("\nUser: 'June 15th'")
    # Answer resolves top question
    qud.pop()
    print(f"QUD: {[str(q) for q in qud]} ← Date resolved")

    print("\nSystem: 'What class? Business or economy?'")
    # Another sub-question
    qud.append(AltQuestion(alternatives=["business", "economy"]))
    print(f"QUD: {[str(q) for q in qud]}")

    print("\nUser: 'Economy'")
    # Answer resolves class question
    qud.pop()
    print(f"QUD: {[str(q) for q in qud]} ← Class resolved")

    print("\nSystem: 'Booked! Economy flight to Paris on June 15th.'")
    # Main question resolved
    qud.pop()
    print(f"QUD: {qud} ← All resolved!")

    print("\n✓ QUD stack drives dialogue flow naturally!")


def main():
    """Run all demos"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "IBDM Core Concepts Demo" + " " * 25 + "║")
    print("╚" + "=" * 58 + "╝")

    demo_questions()
    demo_question_resolution()
    demo_information_state()
    demo_dialogue_moves()
    demo_qud_stack()

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("\nKey Concepts:")
    print("  1. Questions are semantic objects (not strings)")
    print("  2. Information State captures complete dialogue context")
    print("  3. Dialogue Moves are structured communication acts")
    print("  4. QUD stack drives natural dialogue flow")
    print("  5. System can reason about questions and answers")
    print("\nThis theoretical foundation enables:")
    print("  • Context-aware dialogue")
    print("  • Intelligent question matching")
    print("  • Natural conversation flow")
    print("  • Multi-turn coherence")
    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
