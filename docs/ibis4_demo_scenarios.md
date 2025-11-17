# IBiS4 Demo Scenarios: Detailed Turn-by-Turn Analysis

**Date**: 2025-11-17
**Status**: ✅ CURRENT
**Based on**: `examples/ibis4_demo.py` (task ibdm-99.25)

---

## Table of Contents

1. [Scenario 1: Action Execution with Confirmation](#scenario-1-action-execution-with-confirmation)
2. [Scenario 2: Negotiation with Alternatives](#scenario-2-negotiation-with-alternatives)
3. [Scenario 3: Dominance-Based Counter-Proposals](#scenario-3-dominance-based-counter-proposals)
4. [Scenario 4: Action Rollback on Failure](#scenario-4-action-rollback-on-failure)
5. [Scenario 5: Multi-Step Action Sequence](#scenario-5-multi-step-action-sequence)

---

## Scenario 1: Action Execution with Confirmation

**Domain**: Travel (hotel booking)
**Demonstrates**: User confirmation before critical actions, action execution, postcondition tracking
**Larsson Reference**: Chapter 5, Section 5.6

### Initial State

```python
Private IS:
  actions: []
  iun: set()
  beliefs: {
    "domain": TravelDomain,
    "device_interface": MockDevice(should_fail=False)
  }

Shared IS:
  commitments: set()
  qud: []
```

### Turn 1: System Queues Action

**What Happens**: Hotel booking action added to action queue

**Action**:
```python
action = Action(
    action_type=ActionType.BOOK,
    name="book_hotel",
    parameters={
        "hotel_id": "HOTEL_PARIS_001",
        "city": "Paris",
        "check_in": "2025-01-05",
        "check_out": "2025-01-10"
    }
)
state.private.actions.append(action)
```

**State Change**:
```diff
Private IS:
- actions: []
+ actions: [Action(BOOK, "book_hotel", {...})]
  iun: set()
  beliefs: {...}

Shared IS:
  (no change)
```

**Demonstrates**: Action queuing mechanism

---

### Turn 2: System Requests Confirmation

**System**: "Should I book Hotel Paris from 2025-01-05 to 2025-01-10?"

**Rule Applied**: `_request_action_confirmation(state)` (Action Rule 5.6)

**What Happens**:
- System detects queued action requires confirmation
- Creates confirmation question
- Pushes question to agenda

**State Change**:
```diff
Private IS:
  actions: [Action(BOOK, "book_hotel", {...})]
  iun: set()
+ agenda: [DialogueMove(
+   speaker="system",
+   move_type="ask_yn",
+   content=YesNoQuestion(
+     predicate="confirm_action",
+     question_id="Q1"
+   )
+ )]
  beliefs: {...}

Shared IS:
  (no change)
```

**Demonstrates**:
- Confirmation request generation
- Safety mechanism for critical operations
- YesNo question creation

---

### Turn 3: User Confirms

**User**: "Yes"

**Interpretation**:
```python
answer = Answer(content="yes", question_ref=None)
confirm_move = DialogueMove(
    speaker="user",
    move_type="answer",
    content=answer
)
state.private.last_utterance = confirm_move
```

**State Change**:
```diff
Private IS:
  actions: [Action(BOOK, "book_hotel", {...})]
  iun: set()
- agenda: [DialogueMove(...)]
+ agenda: []
+ last_utterance: DialogueMove(speaker="user", move_type="answer", ...)
  beliefs: {...}

Shared IS:
  (no change)
```

**Demonstrates**:
- User confirmation handling
- Answer accommodation
- Dialogue move interpretation

---

### Turn 4: System Executes Action

**System**: (internal) Executing booking...

**Rule Applied**: `_execute_action(state)` (Action Rule 5.7)

**What Happens**:
1. Pop action from queue
2. Check preconditions (all met)
3. Call device interface: `device.execute_action(action)`
4. Device returns success
5. Store result in beliefs

**Device Interaction**:
```python
result = ActionResult(
    status=ActionStatus.SUCCESS,
    message="Hotel booked successfully",
    data={"confirmation": "BOOKING_CONF_001"}
)
```

**State Change**:
```diff
Private IS:
- actions: [Action(BOOK, "book_hotel", {...})]
+ actions: []
  iun: set()
  last_utterance: ...
  beliefs: {
    "domain": TravelDomain,
    "device_interface": MockDevice,
+   "action_result": ActionResult(status=SUCCESS, ...)
  }

Shared IS:
  (no change yet - postconditions added next)
```

**Demonstrates**:
- Action execution flow
- Device interface protocol
- Precondition checking
- Action queue management

---

### Turn 5: System Processes Result

**System**: "Hotel booked successfully! Confirmation: BOOKING_CONF_001"

**Rule Applied**: `_process_action_result(state)` (Action Rule 5.8)

**What Happens**:
1. Check action result status = SUCCESS
2. Apply postconditions using `domain.postcond(action)`
3. Add postconditions to shared commitments
4. Store user feedback in beliefs

**Postconditions Applied**:
```python
postconditions = domain.postcond(action)
# Returns: {
#   "hotel_booked(hotel_id=HOTEL_PARIS_001, check_in=2025-01-05, check_out=2025-01-10)"
# }
```

**State Change**:
```diff
Private IS:
  actions: []
  iun: set()
  last_utterance: ...
  beliefs: {
    "domain": TravelDomain,
    "device_interface": MockDevice,
    "action_result": ActionResult(...),
+   "action_feedback": {
+     "status": "success",
+     "message": "Hotel booked successfully! Confirmation: BOOKING_CONF_001"
+   }
  }

Shared IS:
- commitments: set()
+ commitments: {
+   "hotel_booked(hotel_id=HOTEL_PARIS_001, check_in=2025-01-05, check_out=2025-01-10)"
+ }
```

**Demonstrates**:
- Postcondition application
- Commitment tracking
- Success feedback generation
- State consistency (action executed → commitment added)

---

### Summary

**Dialogue Flow**:
1. System: Queues action
2. System: "Should I book Hotel Paris?" (confirmation request)
3. User: "Yes"
4. System: (executes booking)
5. System: "Hotel booked successfully!"

**Key State Transitions**:
- `actions: [] → [action] → []` (queued then executed)
- `agenda: [] → [confirmation_question] → []` (asked then answered)
- `commitments: {} → {"hotel_booked(...)"}`  (postcondition applied)

**Features Demonstrated**:
- ✅ Action queuing
- ✅ Confirmation requests for critical operations
- ✅ Device interface integration
- ✅ Precondition checking
- ✅ Postcondition application
- ✅ Commitment tracking

---

## Scenario 2: Negotiation with Alternatives

**Domain**: Travel (hotel selection)
**Demonstrates**: Issues Under Negotiation (IUN), accept/reject, counter-proposals
**Larsson Reference**: Chapter 5, Section 5.7

### Initial State

```python
Private IS:
  actions: []
  iun: set()
  beliefs: {"domain": TravelDomain}

Shared IS:
  commitments: set()
  qud: []
```

---

### Turn 1: System Proposes Alternatives

**System**: "I found two hotels in Paris: Hotel Expensive at $200/night or Hotel Budget at $120/night"

**Propositions**:
```python
hotel1 = Proposition(
    predicate="hotel",
    arguments={"id": "H1", "name": "Hotel Expensive", "price": "200"}
)
hotel2 = Proposition(
    predicate="hotel",
    arguments={"id": "H2", "name": "Hotel Budget", "price": "120"}
)
```

**Dialogue Move**:
```python
move = DialogueMove(
    speaker="system",
    move_type="assert",
    content=hotel1,
    metadata={"alternatives": [hotel1, hotel2]}
)
state.private.last_utterance = move
```

**Rule Applied**: `_accommodate_alternative(state)` (Negotiation Rule 5.15)

**What Happens**:
- System detects multiple alternatives in move metadata
- Adds all alternatives to IUN (Issues Under Negotiation)
- User must now accept or reject

**State Change**:
```diff
Private IS:
  actions: []
- iun: set()
+ iun: {
+   Proposition("hotel", {"id": "H1", "name": "Hotel Expensive", "price": "200"}),
+   Proposition("hotel", {"id": "H2", "name": "Hotel Budget", "price": "120"})
+ }
+ last_utterance: DialogueMove(speaker="system", ...)
  beliefs: {...}

Shared IS:
  commitments: set()
  qud: []
```

**Demonstrates**:
- Alternative accommodation
- IUN initialization
- Proposition representation
- Metadata-driven negotiation triggering

---

### Turn 2: User Rejects Expensive Option

**User**: "No, Hotel Expensive is too expensive"

**Interpretation**:
```python
reject_move = DialogueMove(
    speaker="user",
    move_type="answer",
    content=Answer(content="no", question_ref=None)
)
state.private.last_utterance = reject_move
```

**Rule Applied**: `_reject_proposal(state)` (Negotiation Rule 5.17)

**What Happens**:
1. System detects "no" answer
2. Current proposal (Hotel Expensive) is rejected
3. Clear IUN (remove all alternatives)
4. System can now propose a better alternative

**State Change**:
```diff
Private IS:
  actions: []
- iun: {
-   Proposition("hotel", {"id": "H1", ...}),
-   Proposition("hotel", {"id": "H2", ...})
- }
+ iun: set()
  last_utterance: DialogueMove(speaker="user", move_type="answer", ...)
  beliefs: {...}

Shared IS:
  commitments: set()
  qud: []
```

**Demonstrates**:
- Rejection handling
- IUN clearing on rejection
- Negative answer accommodation
- Preservation of rejection context for counter-proposal

---

### Turn 3: System Proposes Better Alternative

**System**: "How about Hotel Budget at $120/night?"

**What Happens**:
- System uses dominance relation to find better alternative
- Hotel Budget dominates Hotel Expensive (lower price)
- Add new proposal to IUN

**State Change**:
```diff
Private IS:
  actions: []
- iun: set()
+ iun: {
+   Proposition("hotel", {"id": "H2", "name": "Hotel Budget", "price": "120"})
+ }
  beliefs: {...}

Shared IS:
  (no change)
```

**Demonstrates**:
- Counter-proposal generation
- Dominance-based alternative selection
- IUN re-initialization with better option

---

### Turn 4: User Accepts

**User**: "Yes, that works!"

**Interpretation**:
```python
accept_move = DialogueMove(
    speaker="user",
    move_type="answer",
    content=Answer(content="yes", question_ref=None)
)
state.private.last_utterance = accept_move
```

**Rule Applied**: `_accept_proposal(state)` (Negotiation Rule 5.16)

**What Happens**:
1. System detects "yes" answer
2. All propositions in IUN move to shared commitments
3. Clear IUN (negotiation complete)
4. Dialogue can proceed to action execution

**State Change**:
```diff
Private IS:
  actions: []
- iun: {
-   Proposition("hotel", {"id": "H2", "name": "Hotel Budget", "price": "120"})
- }
+ iun: set()
  last_utterance: DialogueMove(speaker="user", move_type="answer", ...)
  beliefs: {...}

Shared IS:
- commitments: set()
+ commitments: {
+   "hotel(id=H2, name=Hotel Budget, price=120)"
+ }
  qud: []
```

**Demonstrates**:
- Acceptance handling
- IUN → Commitments transfer
- Negotiation resolution
- Positive answer accommodation
- Shared commitment establishment

---

### Summary

**Dialogue Flow**:
1. System: "I found Hotel Expensive ($200) or Hotel Budget ($120)"
2. User: "No, Hotel Expensive is too expensive"
3. System: "How about Hotel Budget at $120?"
4. User: "Yes, that works!"

**Key State Transitions**:
- `iun: {} → {H1, H2} → {} → {H2} → {}`
- `commitments: {} → {"hotel(id=H2, ...)"}`

**Negotiation Arc**:
```
Propose Alternatives → IUN: {H1, H2}
     ↓
User Rejects → IUN: {}
     ↓
Counter-Propose → IUN: {H2}
     ↓
User Accepts → Commitments: {H2}, IUN: {}
```

**Features Demonstrated**:
- ✅ Alternative accommodation to IUN
- ✅ Rejection handling
- ✅ Counter-proposal generation
- ✅ Dominance-based selection
- ✅ Acceptance with commitment
- ✅ Complete negotiation cycle

---

## Scenario 3: Dominance-Based Counter-Proposals

**Domain**: Travel (hotel comparison)
**Demonstrates**: Dominance relation computation, preference-based filtering
**Larsson Reference**: Chapter 5, Section 5.7.3

### Setup

**Propositions**:
```python
expensive_hotel = Proposition(
    predicate="hotel",
    arguments={"price": "250"}
)
cheap_hotel = Proposition(
    predicate="hotel",
    arguments={"price": "150"}
)
mid_hotel = Proposition(
    predicate="hotel",
    arguments={"price": "180"}
)
```

---

### Operation 1: Dominance Check (Cheap vs Expensive)

**Query**: `domain.dominates(cheap_hotel, expensive_hotel)`

**Computation**:
```python
def dominates(self, p1: Proposition, p2: Proposition) -> bool:
    """Check if p1 dominates p2 (p1 is better than p2)."""
    # For hotels: lower price dominates higher price
    price1 = int(p1.arguments.get("price", "999"))
    price2 = int(p2.arguments.get("price", "999"))
    return price1 < price2
```

**Result**: `True` (150 < 250)

**State**: (no state change - pure function)

**Demonstrates**:
- Dominance relation definition
- Price-based preference ordering
- Domain-specific preference rules

---

### Operation 2: Dominance Check (Cheap vs Mid)

**Query**: `domain.dominates(cheap_hotel, mid_hotel)`

**Computation**:
```python
price1 = 150
price2 = 180
return 150 < 180  # True
```

**Result**: `True` (150 < 180)

**Demonstrates**:
- Transitive dominance
- Cheap hotel dominates all others in this set

---

### Operation 3: Reverse Dominance Check

**Query**: `domain.dominates(expensive_hotel, cheap_hotel)`

**Computation**:
```python
price1 = 250
price2 = 150
return 250 < 150  # False
```

**Result**: `False`

**Demonstrates**:
- Non-symmetric dominance relation
- Higher price does not dominate lower price

---

### Operation 4: Find Better Alternative

**Context**: User rejected expensive hotel ($250)

**Query**:
```python
alternatives = {cheap_hotel, mid_hotel}
better = domain.get_better_alternative(expensive_hotel, alternatives)
```

**Algorithm**:
```python
def get_better_alternative(
    self,
    rejected: Proposition,
    alternatives: set[Proposition]
) -> Proposition | None:
    """Find alternative that dominates rejected option."""
    for alt in alternatives:
        if self.dominates(alt, rejected):
            return alt
    return None
```

**Execution**:
1. Check `cheap_hotel`: `dominates(cheap_hotel, expensive_hotel)` → `True` ✅
2. Return `cheap_hotel` immediately

**Result**: `cheap_hotel` (price=$150)

**Demonstrates**:
- Counter-proposal selection
- Dominance-based filtering
- First-match selection strategy
- Guaranteed improvement (only returns if dominates)

---

### Alternative Scenario: No Better Option

**Context**: User rejected cheap hotel ($150)

**Query**:
```python
alternatives = {expensive_hotel, mid_hotel}
better = domain.get_better_alternative(cheap_hotel, alternatives)
```

**Execution**:
1. Check `expensive_hotel`: `dominates(expensive_hotel, cheap_hotel)` → `False` (250 > 150) ❌
2. Check `mid_hotel`: `dominates(mid_hotel, cheap_hotel)` → `False` (180 > 150) ❌
3. No alternatives dominate rejected option

**Result**: `None`

**System Response**: "I don't have any cheaper options available"

**Demonstrates**:
- Graceful handling when no better alternative exists
- Prevents proposing worse options
- Truthful system behavior

---

### Summary

**Dominance Properties**:
- **Reflexive**: No (hotel doesn't dominate itself)
- **Symmetric**: No (if A dominates B, B doesn't dominate A)
- **Transitive**: Yes (if A dominates B and B dominates C, then A dominates C)
- **Relation Type**: Partial order over propositions

**Preference Rules** (Travel Domain):
```
Lower price → Better option
cheaper_price dominates expensive_price
```

**Usage in Dialogue**:
```
User rejects option → Find dominating alternative → Propose if exists
```

**Features Demonstrated**:
- ✅ Dominance relation computation
- ✅ Preference-based ordering
- ✅ Counter-proposal selection algorithm
- ✅ Guaranteed improvement property
- ✅ Graceful failure (no worse options proposed)

---

## Scenario 4: Action Rollback on Failure

**Domain**: Travel (hotel booking with payment failure)
**Demonstrates**: Optimistic commitment, action failure handling, rollback mechanism
**Larsson Reference**: Chapter 5, Section 5.8

### Initial State

```python
Private IS:
  actions: []
  iun: set()
  beliefs: {
    "domain": TravelDomain,
    "device_interface": MockDevice(should_fail=True, failure_message="Payment declined")
  }

Shared IS:
  commitments: set()
  qud: []
```

---

### Turn 1: Optimistic Booking Commitment

**System**: (internal) Adding optimistic booking commitment before payment

**What Happens**:
- System assumes booking will succeed
- Adds postcondition to commitments early
- Will rollback if payment fails

**State Change**:
```diff
Private IS:
  actions: []
  iun: set()
  beliefs: {...}

Shared IS:
- commitments: set()
+ commitments: {
+   "hotel_booked(hotel_id=HOTEL_001, check_in=2025-01-05, check_out=2025-01-10)"
+ }
  qud: []
```

**Demonstrates**:
- Optimistic commitment strategy
- Early postcondition application
- Assumption of success (will verify later)

---

### Turn 2: Queue Payment Action

**What Happens**:
```python
action = Action(
    action_type=ActionType.BOOK,
    name="book_hotel",
    parameters={
        "hotel_id": "HOTEL_001",
        "check_in": "2025-01-05",
        "check_out": "2025-01-10"
    }
)
state.private.actions.append(action)
```

**State Change**:
```diff
Private IS:
- actions: []
+ actions: [Action(BOOK, "book_hotel", {...})]
  iun: set()
  beliefs: {...}

Shared IS:
  commitments: {"hotel_booked(...)"}
  qud: []
```

**Demonstrates**: Action queuing with existing commitment

---

### Turn 3: Payment Processing (Fails)

**System**: (internal) Processing payment...

**Rule Applied**: `_execute_action(state)`

**Device Interaction**:
```python
# MockDevice configured with should_fail=True
device.configure(should_fail=True, failure_message="Payment declined")

result = device.execute_action(action)
# Returns: ActionResult(
#   status=ActionStatus.FAILED,
#   message="Payment declined",
#   data={}
# )
```

**State Change**:
```diff
Private IS:
- actions: [Action(BOOK, "book_hotel", {...})]
+ actions: []
  iun: set()
  beliefs: {
    "domain": TravelDomain,
    "device_interface": MockDevice,
+   "action_result": ActionResult(status=FAILED, message="Payment declined")
  }

Shared IS:
  commitments: {"hotel_booked(...)"}  # Still present (will be removed)
  qud: []
```

**Demonstrates**:
- Action execution with failure
- Device failure signaling
- Action removal from queue even on failure

---

### Turn 4: Rollback Processing

**System**: "Payment failed. Your booking has been cancelled."

**Rule Applied**: `_process_action_result(state)` with rollback logic

**What Happens**:
1. Check action result status = FAILED
2. Detect existing commitment for this action
3. Remove postcondition from commitments (ROLLBACK)
4. Store rollback information in beliefs
5. Generate failure feedback

**Rollback Algorithm**:
```python
def _process_action_result(state: InformationState) -> InformationState:
    result = state.private.beliefs.get("action_result")

    if result.status == ActionStatus.FAILED:
        # Find postconditions that were optimistically added
        action_name = "book_hotel"
        postconds_to_remove = [
            c for c in state.shared.commitments
            if action_name in c
        ]

        # ROLLBACK: Remove commitments
        for postcond in postconds_to_remove:
            state.shared.commitments.discard(postcond)

        # Record rollback
        state.private.beliefs["rollback_performed"] = {
            "action": action_name,
            "reason": result.message,
            "removed_commitments": postconds_to_remove
        }

        # User feedback
        state.private.beliefs["action_feedback"] = {
            "status": "failed",
            "message": f"Payment failed: {result.message}"
        }

    return state
```

**State Change**:
```diff
Private IS:
  actions: []
  iun: set()
  beliefs: {
    "domain": TravelDomain,
    "device_interface": MockDevice,
    "action_result": ActionResult(status=FAILED, ...),
+   "rollback_performed": {
+     "action": "book_hotel",
+     "reason": "Payment declined",
+     "removed_commitments": ["hotel_booked(...)"]
+   },
+   "action_feedback": {
+     "status": "failed",
+     "message": "Payment failed: Payment declined"
+   }
  }

Shared IS:
- commitments: {"hotel_booked(hotel_id=HOTEL_001, check_in=2025-01-05, check_out=2025-01-10)"}
+ commitments: set()  # ROLLED BACK
  qud: []
```

**Demonstrates**:
- Rollback detection (failure after optimistic commit)
- Commitment removal (restore previous state)
- Rollback notification to user
- Failure feedback generation
- State consistency restoration

---

### Summary

**Dialogue Flow**:
1. System: (internal) Optimistically commits booking
2. System: (internal) Queues payment action
3. System: (internal) Processes payment → FAILS
4. System: "Payment failed. Your booking has been cancelled."

**Key State Transitions**:
```
Optimistic Commit:
  commitments: {} → {"hotel_booked(...)"}

Payment Failure:
  action_result: None → ActionResult(FAILED)

Rollback:
  commitments: {"hotel_booked(...)"} → {}
  beliefs: + rollback_performed, + action_feedback
```

**Consistency Properties**:
- Before payment: `commitments = {"hotel_booked"}`, `action_result = None`
- After failure: `commitments = {}`, `action_result = FAILED`
- **Result**: Consistent state (no booking commitment without successful payment)

**Features Demonstrated**:
- ✅ Optimistic commitment strategy
- ✅ Action failure detection
- ✅ Automatic rollback mechanism
- ✅ Commitment removal
- ✅ Rollback notification
- ✅ State consistency guarantee
- ✅ Graceful failure handling

---

## Scenario 5: Multi-Step Action Sequence

**Domain**: Travel (complete trip package)
**Demonstrates**: Action queue management, sequential execution, aggregate postconditions
**Larsson Reference**: Chapter 5, Section 5.6

### Initial State

```python
Private IS:
  actions: []
  iun: set()
  beliefs: {
    "domain": TravelDomain,
    "device_interface": MockDevice(should_fail=False)
  }

Shared IS:
  commitments: set()
  qud: []
```

---

### Turn 1: Queue Complete Travel Package

**System**: (internal) Planning travel itinerary

**Actions**:
```python
actions = [
    Action(
        action_type=ActionType.BOOK,
        name="book_flight",
        parameters={
            "confirmation_number": "FL123",
            "depart_city": "london",
            "dest_city": "paris",
            "depart_day": "2025-01-05"
        }
    ),
    Action(
        action_type=ActionType.BOOK,
        name="book_hotel",
        parameters={
            "hotel_id": "HOTEL_PARIS",
            "city": "paris",
            "check_in": "2025-01-05",
            "check_out": "2025-01-10"
        }
    ),
    Action(
        action_type=ActionType.SET,
        name="reserve_car",
        parameters={
            "confirmation": "CAR456",
            "pickup_location": "airport",
            "pickup_date": "2025-01-05",
            "return_date": "2025-01-10"
        }
    )
]

for action in actions:
    state.private.actions.append(action)
```

**State Change**:
```diff
Private IS:
- actions: []
+ actions: [
+   Action(BOOK, "book_flight", {...}),
+   Action(BOOK, "book_hotel", {...}),
+   Action(SET, "reserve_car", {...})
+ ]
  iun: set()
  beliefs: {...}

Shared IS:
  commitments: set()
  qud: []
```

**Demonstrates**:
- Multi-action queuing
- Action sequence planning
- FIFO queue structure

---

### Turn 2: Execute Flight Booking

**System**: (internal) Executing book_flight...

**Rule Applied**: `_execute_action(state)` (processes first action in queue)

**Device Interaction**:
```python
action = state.private.actions[0]  # book_flight
result = device.execute_action(action)
# Returns: ActionResult(
#   status=SUCCESS,
#   message="Flight booked: FL123",
#   data={"confirmation": "FL123"}
# )
```

**State Change**:
```diff
Private IS:
- actions: [
-   Action(BOOK, "book_flight", {...}),
-   Action(BOOK, "book_hotel", {...}),
-   Action(SET, "reserve_car", {...})
- ]
+ actions: [
+   Action(BOOK, "book_hotel", {...}),
+   Action(SET, "reserve_car", {...})
+ ]
  iun: set()
  beliefs: {
    "domain": TravelDomain,
    "device_interface": MockDevice,
+   "action_result": ActionResult(status=SUCCESS, message="Flight booked: FL123")
  }

Shared IS:
  (no change yet)
```

**Demonstrates**:
- FIFO action processing
- Queue advancement
- Action execution isolation

---

### Turn 3: Process Flight Result

**System**: "Flight booked: FL123"

**Rule Applied**: `_process_action_result(state)`

**Postconditions**:
```python
postconds = domain.postcond(book_flight_action)
# Returns: {
#   "flight_booked(confirmation=FL123, depart_city=london, dest_city=paris, depart_day=2025-01-05)"
# }
```

**State Change**:
```diff
Private IS:
  actions: [
    Action(BOOK, "book_hotel", {...}),
    Action(SET, "reserve_car", {...})
  ]
  iun: set()
  beliefs: {
    "domain": TravelDomain,
    "device_interface": MockDevice,
    "action_result": ActionResult(status=SUCCESS, ...),
+   "action_feedback": {
+     "status": "success",
+     "message": "Flight booked: FL123"
+   }
  }

Shared IS:
- commitments: set()
+ commitments: {
+   "flight_booked(confirmation=FL123, depart_city=london, dest_city=paris, depart_day=2025-01-05)"
+ }
  qud: []
```

**Demonstrates**:
- Postcondition application
- Incremental commitment building
- Per-action feedback

---

### Turn 4: Execute Hotel Booking

**System**: (internal) Executing book_hotel...

**Rule Applied**: `_execute_action(state)` (next action in queue)

**Device Interaction**:
```python
action = state.private.actions[0]  # book_hotel
result = device.execute_action(action)
# Returns: ActionResult(
#   status=SUCCESS,
#   message="Hotel booked: HOTEL_PARIS",
#   data={"confirmation": "HOTEL_CONF_789"}
# )
```

**State Change**:
```diff
Private IS:
- actions: [
-   Action(BOOK, "book_hotel", {...}),
-   Action(SET, "reserve_car", {...})
- ]
+ actions: [
+   Action(SET, "reserve_car", {...})
+ ]
  iun: set()
  beliefs: {
    "domain": TravelDomain,
    "device_interface": MockDevice,
-   "action_result": ActionResult(status=SUCCESS, message="Flight booked: FL123"),
+   "action_result": ActionResult(status=SUCCESS, message="Hotel booked: HOTEL_PARIS"),
-   "action_feedback": {"status": "success", "message": "Flight booked: FL123"}
  }

Shared IS:
  commitments: {"flight_booked(...)"}
  qud: []
```

**Demonstrates**:
- Sequential action processing
- Queue consumption
- State update isolation

---

### Turn 5: Process Hotel Result

**System**: "Hotel booked: HOTEL_PARIS"

**Rule Applied**: `_process_action_result(state)`

**Postconditions**:
```python
postconds = domain.postcond(book_hotel_action)
# Returns: {
#   "hotel_booked(hotel_id=HOTEL_PARIS, city=paris, check_in=2025-01-05, check_out=2025-01-10)"
# }
```

**State Change**:
```diff
Private IS:
  actions: [Action(SET, "reserve_car", {...})]
  iun: set()
  beliefs: {
    "domain": TravelDomain,
    "device_interface": MockDevice,
    "action_result": ActionResult(status=SUCCESS, ...),
+   "action_feedback": {
+     "status": "success",
+     "message": "Hotel booked: HOTEL_PARIS"
+   }
  }

Shared IS:
- commitments: {
-   "flight_booked(...)"
- }
+ commitments: {
+   "flight_booked(confirmation=FL123, depart_city=london, dest_city=paris, depart_day=2025-01-05)",
+   "hotel_booked(hotel_id=HOTEL_PARIS, city=paris, check_in=2025-01-05, check_out=2025-01-10)"
+ }
  qud: []
```

**Demonstrates**:
- Commitment accumulation
- Multiple independent commitments
- Progress tracking through commitments

---

### Turn 6: Execute Car Reservation

**System**: (internal) Executing reserve_car...

**Rule Applied**: `_execute_action(state)` (final action)

**Device Interaction**:
```python
action = state.private.actions[0]  # reserve_car
result = device.execute_action(action)
# Returns: ActionResult(
#   status=SUCCESS,
#   message="Car reserved: CAR456",
#   data={"confirmation": "CAR456"}
# )
```

**State Change**:
```diff
Private IS:
- actions: [Action(SET, "reserve_car", {...})]
+ actions: []  # QUEUE EMPTY
  iun: set()
  beliefs: {
    "domain": TravelDomain,
    "device_interface": MockDevice,
-   "action_result": ActionResult(status=SUCCESS, message="Hotel booked: HOTEL_PARIS"),
+   "action_result": ActionResult(status=SUCCESS, message="Car reserved: CAR456"),
  }

Shared IS:
  commitments: {
    "flight_booked(...)",
    "hotel_booked(...)"
  }
  qud: []
```

**Demonstrates**:
- Queue completion detection
- Final action processing

---

### Turn 7: Process Car Result & Complete Package

**System**: "Car reserved: CAR456. Travel package complete!"

**Rule Applied**: `_process_action_result(state)`

**Postconditions**:
```python
postconds = domain.postcond(reserve_car_action)
# Returns: {
#   "car_reserved(confirmation=CAR456, pickup_location=airport, pickup_date=2025-01-05, return_date=2025-01-10)"
# }
```

**State Change**:
```diff
Private IS:
  actions: []
  iun: set()
  beliefs: {
    "domain": TravelDomain,
    "device_interface": MockDevice,
    "action_result": ActionResult(status=SUCCESS, ...),
+   "action_feedback": {
+     "status": "success",
+     "message": "Car reserved: CAR456. Travel package complete!"
+   }
  }

Shared IS:
- commitments: {
-   "flight_booked(confirmation=FL123, depart_city=london, dest_city=paris, depart_day=2025-01-05)",
-   "hotel_booked(hotel_id=HOTEL_PARIS, city=paris, check_in=2025-01-05, check_out=2025-01-10)"
- }
+ commitments: {
+   "flight_booked(confirmation=FL123, depart_city=london, dest_city=paris, depart_day=2025-01-05)",
+   "hotel_booked(hotel_id=HOTEL_PARIS, city=paris, check_in=2025-01-05, check_out=2025-01-10)",
+   "car_reserved(confirmation=CAR456, pickup_location=airport, pickup_date=2025-01-05, return_date=2025-01-10)"
+ }
  qud: []
```

**Demonstrates**:
- Complete package assembly
- All postconditions present
- Queue emptiness as completion signal

---

### Summary

**Dialogue Flow**:
1. System: Queue 3 actions (flight, hotel, car)
2. System: Execute flight → "Flight booked: FL123"
3. System: Execute hotel → "Hotel booked: HOTEL_PARIS"
4. System: Execute car → "Car reserved: CAR456"
5. System: "Travel package complete!"

**Key State Transitions**:

**Action Queue**:
```
[flight, hotel, car] → [hotel, car] → [car] → []
```

**Commitments (Accumulation)**:
```
{}
→ {"flight_booked(...)"}
→ {"flight_booked(...)", "hotel_booked(...)"}
→ {"flight_booked(...)", "hotel_booked(...)", "car_reserved(...)"}
```

**Execution Pattern**:
```
For each action in queue:
  1. Execute action (device call)
  2. Process result (add postconditions)
  3. Move to next action
Until queue empty
```

**Features Demonstrated**:
- ✅ Multi-action queuing (3 actions)
- ✅ FIFO queue processing
- ✅ Sequential execution
- ✅ Per-action postconditions
- ✅ Commitment accumulation
- ✅ Independent action isolation
- ✅ Queue completion detection
- ✅ Aggregate package completion

**Invariants Maintained**:
- Action queue length decreases monotonically
- Commitments set grows monotonically (unless rollback)
- Each action processes exactly once
- Postconditions apply only after success

---

## Cross-Scenario Patterns

### Common State Structures

**Action Queue Pattern**:
```
actions: [] → [a1, a2, ..., an] → [a2, ..., an] → ... → []
```

**IUN Pattern**:
```
iun: {} → {p1, p2, ...} → {} (on accept/reject)
```

**Commitment Pattern**:
```
commitments: {} → {postcond1} → {postcond1, postcond2} → ...
```

### Rule Application Order

1. **Confirmation**: `_request_action_confirmation` (if needed)
2. **Execution**: `_execute_action` (device interaction)
3. **Processing**: `_process_action_result` (postconditions/rollback)
4. **Negotiation**: `_accommodate_alternative`, `_accept_proposal`, `_reject_proposal`

### State Consistency Guarantees

**Invariant 1**: If `action ∈ commitments`, then action was executed successfully
- Ensured by: Rollback on failure

**Invariant 2**: If `proposition ∈ commitments`, then either accepted from IUN or added as postcondition
- Ensured by: Only two paths to commitments

**Invariant 3**: `actions` queue contains only pending actions
- Ensured by: Remove action after execution (success or failure)

**Invariant 4**: `iun` is empty when not negotiating
- Ensured by: Clear IUN on accept/reject

---

## Usage Guide

### How to Read These Scenarios

Each scenario shows:
1. **Initial State**: Starting information state
2. **Turn-by-Turn**: Each dialogue turn with:
   - Speaker and utterance
   - Rule applied
   - State changes (diff format)
   - What is demonstrated
3. **Summary**: Key transitions and features

### State Diff Format

```diff
Field:
- old_value  # Value before turn
+ new_value  # Value after turn
  unchanged  # Value that didn't change
```

### Finding Related Code

- **Action Rules**: `src/ibdm/rules/action_rules.py`
- **Negotiation Rules**: `src/ibdm/rules/negotiation_rules.py`
- **Action Types**: `src/ibdm/core/actions.py`
- **Device Interface**: `src/ibdm/interfaces/device.py`
- **Domain Model**: `src/ibdm/domains/travel_domain.py`
- **Demo Application**: `examples/ibis4_demo.py`

---

## Larsson Fidelity

### Implemented from Chapter 5

- ✅ **Section 5.2**: Device Interface Protocol
- ✅ **Section 5.3**: Action Preconditions & Postconditions
- ✅ **Section 5.6**: Action Execution with Confirmation
- ✅ **Section 5.7**: Negotiative Dialogue
- ✅ **Section 5.7.3**: Dominance Relations
- ✅ **Section 5.8**: Action Rollback

### Compliance Metrics

Based on `reports/larsson-fidelity-ibis4-final.md`:
- **Overall Fidelity**: 96.5%
- **Action Execution**: 100%
- **Negotiation**: 95%
- **Device Interface**: 100%

---

**Document Status**: ✅ CURRENT
**Last Updated**: 2025-11-17
**Maintained By**: IBDM Development Team
