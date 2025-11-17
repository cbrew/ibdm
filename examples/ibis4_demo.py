"""IBiS-4 Demo: Action-Oriented Dialogue with Negotiation.

Demonstrates:
- Action execution with device interface
- Action confirmation for critical operations
- Negotiation with Issues Under Negotiation (IUN)
- Counter-proposals based on dominance
- Action rollback on failure

Based on Larsson (2002) Chapter 5.
"""

from ibdm.core.actions import Action, ActionType, Proposition
from ibdm.core.domain import DomainModel
from ibdm.core.information_state import InformationState
from ibdm.core.moves import DialogueMove
from ibdm.domains.travel_domain import get_travel_domain
from ibdm.interfaces.device import ActionResult, ActionStatus
from ibdm.rules.action_rules import (
    _execute_action,
    _process_action_result,
    _request_action_confirmation,
)
from ibdm.rules.negotiation_rules import (
    _accept_proposal,
    _accommodate_alternative,
    _reject_proposal,
)
from tests.mocks.mock_device import MockDevice


def print_header(text: str) -> None:
    """Print a formatted header."""
    print(f"\n{'=' * 70}")
    print(f"  {text}")
    print(f"{'=' * 70}\n")


def print_state(state: InformationState, label: str = "State") -> None:
    """Print current dialogue state."""
    print(f"\n--- {label} ---")
    print(f"Commitments: {state.shared.commitments}")
    print(f"IUN: {state.private.iun}")
    print(f"Actions queue: {[a.name for a in state.private.actions]}")
    print(f"Agenda: {len(state.private.agenda)} items")


def demo_action_execution() -> None:
    """Demo 1: Basic action execution with confirmation."""
    print_header("Demo 1: Action Execution with Confirmation")

    # Setup
    state = InformationState()
    domain = get_travel_domain()
    device = MockDevice()
    device.configure(should_fail=False)

    state.private.beliefs["domain"] = domain
    state.private.beliefs["device_interface"] = device

    # Add action to queue
    action = Action(
        action_type=ActionType.BOOK,
        name="book_hotel",
        parameters={
            "hotel_id": "HOTEL_PARIS_001",
            "city": "Paris",
            "check_in": "2025-01-05",
            "check_out": "2025-01-10",
        },
    )
    state.private.actions.append(action)

    print("📋 Action queued: book_hotel")
    print(f"   Parameters: {action.parameters}")
    print_state(state, "Initial State")

    # Step 1: System requests confirmation
    print("\n🤖 System: Requesting confirmation...")
    state = _request_action_confirmation(state)

    if state.private.agenda:
        confirmation_move = state.private.agenda[-1]
        print(f"   Question: {confirmation_move.content}")

    # Step 2: User confirms
    print("\n👤 User: Yes")
    from ibdm.core.answers import Answer

    answer = Answer(content="yes", question_ref=None)
    confirm_move = DialogueMove(speaker="user", move_type="answer", content=answer)
    state.private.last_utterance = confirm_move

    # Step 3: Execute action
    print("\n⚙️  Executing action...")
    state = _execute_action(state)

    # Step 4: Process result
    state = _process_action_result(state)

    print_state(state, "Final State")

    # Check postconditions
    postconditions = [
        c for c in state.shared.commitments if "hotel_booked" in c
    ]
    if postconditions:
        print(f"\n✅ Success! Postconditions added: {postconditions}")

    feedback = state.private.beliefs.get("action_feedback", {})
    if feedback:
        print(f"📬 Feedback: {feedback['message']}")


def demo_negotiation() -> None:
    """Demo 2: Negotiation with multiple alternatives."""
    print_header("Demo 2: Negotiation with Hotel Alternatives")

    state = InformationState()
    domain = get_travel_domain()
    state.private.beliefs["domain"] = domain

    # System proposes two hotels
    hotel1 = Proposition(
        predicate="hotel",
        arguments={"id": "H1", "name": "Hotel Expensive", "price": "200"},
    )
    hotel2 = Proposition(
        predicate="hotel",
        arguments={"id": "H2", "name": "Hotel Budget", "price": "120"},
    )

    print("🤖 System: I found two hotels in Paris:")
    print(f"   Option A: {hotel1.arguments['name']} - ${hotel1.arguments['price']}/night")
    print(f"   Option B: {hotel2.arguments['name']} - ${hotel2.arguments['price']}/night")

    # Accommodate alternatives to IUN
    move = DialogueMove(
        speaker="system",
        move_type="assert",
        content=hotel1,
        metadata={"alternatives": [hotel1, hotel2]},
    )
    state.private.last_utterance = move

    state = _accommodate_alternative(state)
    print_state(state, "After Accommodation")

    # User rejects expensive option
    print("\n👤 User: No, Hotel Expensive is too expensive")
    reject_move = DialogueMove(
        speaker="user", move_type="answer", content=Answer(content="no", question_ref=None)
    )
    state.private.last_utterance = reject_move

    state = _reject_proposal(state)
    print(f"\n🗑️  IUN cleared (user rejected)")
    print_state(state, "After Rejection")

    # System proposes better alternative
    print("\n🤖 System: How about Hotel Budget at $120/night?")
    state.private.iun.add(hotel2)

    # User accepts
    print("\n👤 User: Yes, that works!")
    accept_move = DialogueMove(
        speaker="user",
        move_type="answer",
        content=Answer(content="yes", question_ref=None),
    )
    state.private.last_utterance = accept_move

    state = _accept_proposal(state)
    print_state(state, "Final State")

    # Check commitment
    commitment = [c for c in state.shared.commitments if "hotel" in c]
    if commitment:
        print(f"\n✅ Negotiation resolved! Committed to: {commitment[0]}")


def demo_dominance() -> None:
    """Demo 3: Dominance-based counter-proposals."""
    print_header("Demo 3: Dominance-Based Counter-Proposals")

    domain = get_travel_domain()

    # Test dominance function
    expensive_hotel = Proposition(
        predicate="hotel", arguments={"price": "250"}
    )
    cheap_hotel = Proposition(predicate="hotel", arguments={"price": "150"})
    mid_hotel = Proposition(predicate="hotel", arguments={"price": "180"})

    print("🏨 Hotels available:")
    print(f"   Hotel A: ${expensive_hotel.arguments['price']}")
    print(f"   Hotel B: ${cheap_hotel.arguments['price']}")
    print(f"   Hotel C: ${mid_hotel.arguments['price']}")

    print("\n📊 Dominance checks:")
    print(
        f"   Hotel B dominates Hotel A? {domain.dominates(cheap_hotel, expensive_hotel)}"
    )
    print(
        f"   Hotel B dominates Hotel C? {domain.dominates(cheap_hotel, mid_hotel)}"
    )
    print(f"   Hotel A dominates Hotel B? {domain.dominates(expensive_hotel, cheap_hotel)}")

    # Find better alternative
    print(f"\n🔍 User rejected Hotel A (${expensive_hotel.arguments['price']})")
    alternatives = {cheap_hotel, mid_hotel}

    better = domain.get_better_alternative(expensive_hotel, alternatives)
    if better:
        print(
            f"✨ System suggests: Hotel at ${better.arguments['price']} (dominates rejected option)"
        )
    else:
        print("❌ No better alternative found")


def demo_rollback() -> None:
    """Demo 4: Action rollback on failure."""
    print_header("Demo 4: Action Rollback on Failure")

    state = InformationState()
    domain = get_travel_domain()
    device = MockDevice()

    state.private.beliefs["domain"] = domain
    state.private.beliefs["device_interface"] = device

    # Optimistically commit booking
    print("📋 Optimistic booking (before payment)...")
    state.shared.commitments.add("hotel_booked(hotel_id=HOTEL_001, check_in=2025-01-05, check_out=2025-01-10)")
    print_state(state, "Before Payment")

    # Setup action that will fail
    action = Action(
        action_type=ActionType.BOOK,
        name="book_hotel",
        parameters={
            "hotel_id": "HOTEL_001",
            "check_in": "2025-01-05",
            "check_out": "2025-01-10",
        },
    )
    state.private.actions.append(action)

    # Configure device to fail
    device.configure(should_fail=True, failure_message="Payment declined")

    # Execute and fail
    print("\n💳 Processing payment...")
    state = _execute_action(state)

    # Process failure (triggers rollback)
    print("❌ Payment failed!")
    state = _process_action_result(state)

    print_state(state, "After Rollback")

    # Check rollback
    rollback_info = state.private.beliefs.get("rollback_performed")
    if rollback_info:
        print(f"\n🔄 Rollback performed: {rollback_info['action']}")
        print(f"   Reason: {rollback_info['reason']}")

    # Verify commitment removed
    hotel_commits = [c for c in state.shared.commitments if "hotel_booked" in c]
    if not hotel_commits:
        print("✅ Booking rolled back successfully (commitment removed)")


def demo_multi_step_actions() -> None:
    """Demo 5: Multi-step action sequence."""
    print_header("Demo 5: Multi-Step Action Sequence")

    state = InformationState()
    domain = get_travel_domain()
    device = MockDevice()
    device.configure(should_fail=False)

    state.private.beliefs["domain"] = domain
    state.private.beliefs["device_interface"] = device

    # Queue multiple actions
    actions = [
        Action(
            action_type=ActionType.BOOK,
            name="book_flight",
            parameters={
                "confirmation_number": "FL123",
                "depart_city": "london",
                "dest_city": "paris",
                "depart_day": "2025-01-05",
            },
        ),
        Action(
            action_type=ActionType.BOOK,
            name="book_hotel",
            parameters={
                "hotel_id": "HOTEL_PARIS",
                "city": "paris",
                "check_in": "2025-01-05",
                "check_out": "2025-01-10",
            },
        ),
        Action(
            action_type=ActionType.SET,
            name="reserve_car",
            parameters={
                "confirmation": "CAR456",
                "pickup_location": "airport",
                "pickup_date": "2025-01-05",
                "return_date": "2025-01-10",
            },
        ),
    ]

    print("📋 Travel itinerary:")
    for i, action in enumerate(actions, 1):
        print(f"   {i}. {action.name}")
        state.private.actions.append(action)

    print_state(state, "Initial Queue")

    # Execute each action
    step = 1
    while state.private.actions:
        current_action = state.private.actions[0]
        print(f"\n⚙️  Step {step}: Executing {current_action.name}...")

        state = _execute_action(state)
        state = _process_action_result(state)

        feedback = state.private.beliefs.get("action_feedback", {})
        if feedback.get("status") == "success":
            print(f"   ✅ {feedback['message']}")

        step += 1

    print_state(state, "Final State")

    print("\n📦 Travel package completed!")
    print(f"   Total postconditions: {len(state.shared.commitments)}")
    for commitment in state.shared.commitments:
        print(f"   - {commitment}")


def main() -> None:
    """Run all IBiS-4 demos."""
    print("\n" + "=" * 70)
    print(" " * 15 + "IBiS-4 DEMONSTRATION")
    print(" " * 10 + "Action-Oriented Dialogue System")
    print(" " * 12 + "Based on Larsson (2002)")
    print("=" * 70)

    demos = [
        ("Action Execution", demo_action_execution),
        ("Negotiation", demo_negotiation),
        ("Dominance Relations", demo_dominance),
        ("Action Rollback", demo_rollback),
        ("Multi-Step Actions", demo_multi_step_actions),
    ]

    for name, demo_func in demos:
        try:
            demo_func()
        except Exception as e:
            print(f"\n❌ Demo '{name}' failed: {e}")
            import traceback

            traceback.print_exc()

    print("\n" + "=" * 70)
    print(" " * 20 + "Demo Complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
