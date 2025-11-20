# Question Override Feature

## Overview

The question override feature allows users to skip optional questions when they don't have the required information. This is useful for scenarios like report generation where some information may not be available, but the user wants to proceed anyway.

## Usage

### Marking Questions as Optional

Questions can be marked as optional by setting `required=False`:

```python
from ibdm.core import WhQuestion

# Required question (default)
destination = WhQuestion(
    predicate="destination",
    variable="city",
    required=True,  # Explicit, but this is the default
)

# Optional question - can be skipped
seat_preference = WhQuestion(
    predicate="seat_preference",
    variable="seat",
    required=False,  # User can skip this
)
```

### User Skip Patterns

The system recognizes various user utterances that indicate a desire to skip:

- "skip that"
- "skip this question"
- "pass"
- "I don't have that information"
- "I don't know"
- "not available"
- "move on"
- "proceed anyway"
- "proceed without it"
- "can't provide"
- "no info"
- "idk"
- "dunno"

### Example Dialogue

```
System: What is your seat preference? (window or aisle)
User: I don't have a preference, skip that
System: [Skips seat_preference question]
        Proceeding with booking. Destination confirmed as Paris...
```

## Implementation Details

### Rule Flow

1. **Detection** (`_is_skip_request_move`):
   - Checks if user utterance matches skip patterns
   - Verifies a question is on QUD
   - Confirms the question is optional (`required=False`)

2. **Accommodation** (`_accommodate_skip_question`):
   - Removes question from QUD
   - Adds question to `private.overridden_questions` for tracking
   - Dialogue continues without that information

3. **Plan Completion** (`_has_communicative_plan`):
   - Plan can execute if all findout subplans are either:
     - Completed (user answered), OR
     - Overridden (user chose to skip)

### State Tracking

Overridden questions are tracked in the information state:

```python
state.private.overridden_questions: list[Question]
```

This allows:
- Audit trail of skipped questions
- Conditional logic based on what was skipped
- Full serialization/deserialization support

### Required vs Optional Behavior

| Question Type | User Says "skip" | Behavior |
|--------------|------------------|----------|
| `required=True` (default) | System ignores skip request | Continues asking question |
| `required=False` | System accepts skip | Removes from QUD, tracks as overridden |

## Design Rationale

### Why This Feature?

In real-world dialogue systems, users may not always have all requested information. Examples:

- **Report Generation**: "What's the project completion date?" → "We haven't set one yet"
- **Form Filling**: "What's your middle name?" → "I don't have one"
- **Booking**: "What's your seat preference?" → "I don't care"

Without override support, the dialogue would be stuck in a loop asking for unavailable information.

### Why Distinguish Required/Optional?

Some information is critical to task completion:

- **Critical (required=True)**: Destination for a flight booking
- **Optional (required=False)**: Meal preference, seat preference

The system should be flexible on optional details but firm on essentials.

## Usage in Domain Models

When creating domain models, mark questions as optional for non-critical information:

```python
def create_flight_booking_plan():
    return Plan(
        plan_type="book_flight",
        content="Flight booking",
        subplans=[
            # Critical information
            Plan("findout", WhQuestion("destination", "city", required=True)),
            Plan("findout", WhQuestion("departure_date", "date", required=True)),

            # Optional preferences
            Plan("findout", WhQuestion("seat_preference", "seat", required=False)),
            Plan("findout", WhQuestion("meal_preference", "meal", required=False)),
        ]
    )
```

## Testing

Comprehensive tests are available in `tests/unit/test_question_override.py`:

- Skip pattern recognition
- Optional question skipping
- Required question protection
- Plan execution with overrides
- State serialization

Run tests:
```bash
pytest tests/unit/test_question_override.py -v
```

## Larsson Fidelity Impact

This feature extends IBiS dialogue management while maintaining Larsson (2002) principles:

- **Preserves**: QUD stack semantics, explicit state management
- **Extends**: Question semantics to include optionality
- **Adds**: New accommodation rule for skip handling

The implementation follows the established pattern:
1. Integration phase: Detect skip and update state
2. Selection phase: Respect overridden questions in plan execution
