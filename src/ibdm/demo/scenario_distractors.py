"""Scenario-specific distractor definitions.

Provides detailed, contextual distractors for each scenario turn.
These are designed to be educational and demonstrate different IBiS mechanisms.
"""

from dataclasses import dataclass

from ibdm.demo.scenario_explorer import ChoiceOption, MoveCategory


@dataclass
class TurnDistractors:
    """Distractors for a specific scenario turn.

    Attributes:
        turn_index: The turn number in the scenario
        expected_utterance: The expected user utterance
        distractors: List of distractor options for this turn
    """

    turn_index: int
    expected_utterance: str
    distractors: list[ChoiceOption]


# Scenario 1: Incremental Questioning Distractors


def get_scenario1_turn1_distractors() -> list[ChoiceOption]:
    """Distractors for Scenario 1, Turn 1: Initial NDA request.

    Expected: "I need to draft an NDA"
    Context: User is initiating the dialogue
    """
    return [
        # Expected move (always option 1)
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="I need to draft an NDA",
            description="[Expected] User initiates NDA drafting task",
            expected_trajectory=(
                "System forms task plan with 4 questions, "
                "accommodates them to private.issues, "
                "raises first question to QUD"
            ),
        ),
        # Distractor 1: Vague request
        ChoiceOption(
            id=2,
            category=MoveCategory.CLARIFICATION_REQUEST,
            utterance="I need some kind of agreement",
            description=(
                "[Distractor] Vague request → System asks for clarification about document type"
            ),
            expected_trajectory=(
                "System cannot determine task from vague request, "
                "asks clarification question: 'What type of agreement?' "
                "User must specify NDA"
            ),
        ),
        # Distractor 2: Request with volunteer info
        ChoiceOption(
            id=3,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="I need to draft an NDA between Acme Corp and Smith Inc",
            description=(
                "[Distractor] Request with volunteer parties → "
                "System extracts and accommodates volunteered info"
            ),
            expected_trajectory=(
                "System forms plan, accommodates questions to issues, "
                "but removes 'parties' from issues (already provided), "
                "raises 'effective_date' as first question"
            ),
        ),
        # Distractor 3: Alternative task
        ChoiceOption(
            id=4,
            category=MoveCategory.EXPECTED,
            utterance="I need to book a flight",
            description=(
                "[Distractor] Different task → "
                "System switches to travel domain and flight booking plan"
            ),
            expected_trajectory=(
                "System recognizes travel task, "
                "forms flight booking plan with different questions "
                "(departure city, destination, dates, etc.)"
            ),
        ),
        # Distractor 4: Meta question
        ChoiceOption(
            id=5,
            category=MoveCategory.NESTED_QUESTION,
            utterance="What information do you need to draft an NDA?",
            description=(
                "[Distractor] Meta question about process → System explains NDA requirements"
            ),
            expected_trajectory=(
                "System pushes user's meta-question to QUD, "
                "provides explanation of NDA information needs, "
                "pops meta-question, "
                "then asks if user wants to proceed"
            ),
        ),
    ]


def get_scenario1_turn2_distractors() -> list[ChoiceOption]:
    """Distractors for Scenario 1, Turn 2: Answering parties question.

    Expected: "Acme Corp and Smith Inc"
    Context: System asked "What are the parties to the NDA?"
    """
    return [
        # Expected move
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="Acme Corp and Smith Inc",
            description="[Expected] Valid parties answer",
            expected_trajectory=(
                "System validates answer (2 legal entities), "
                "pops 'parties' from QUD, "
                "adds commitment 'parties(Acme Corp, Smith Inc)', "
                "raises next question 'effective_date' to QUD"
            ),
        ),
        # Distractor 1: Invalid answer (nonsensical)
        ChoiceOption(
            id=2,
            category=MoveCategory.INVALID_ANSWER,
            utterance="blue",
            description=(
                "[Distractor] Invalid answer → Domain validation fails, clarification generated"
            ),
            expected_trajectory=(
                "System validates: domain.resolves('blue', Q_parties) → False, "
                "creates clarification question CQ, "
                "pushes CQ to QUD above Q_parties, "
                "asks: 'Please provide valid party names (legal entities)'"
            ),
        ),
        # Distractor 2: Incomplete answer
        ChoiceOption(
            id=3,
            category=MoveCategory.INVALID_ANSWER,
            utterance="Acme Corp",
            description=(
                "[Distractor] Incomplete answer (only one party) → "
                "Validation fails, system asks for second party"
            ),
            expected_trajectory=(
                "System validates: needs TWO parties, only one provided, "
                "generates clarification: "
                "'An NDA requires two parties. Who is the second party?'"
            ),
        ),
        # Distractor 3: Volunteer multiple facts
        ChoiceOption(
            id=4,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="Acme Corp and Smith Inc, effective January 1, 2025",
            description=(
                "[Distractor] Volunteer effective date → "
                "System processes both facts, skips date question"
            ),
            expected_trajectory=(
                "System integrates 'parties' (answers current question), "
                "integrates 'effective_date' (volunteer from issues), "
                "removes Q_effective_date from private.issues, "
                "raises Q_term to QUD (skips date question)"
            ),
        ),
        # Distractor 4: Clarification question
        ChoiceOption(
            id=5,
            category=MoveCategory.NESTED_QUESTION,
            utterance="What format should I use for the party names?",
            description=(
                "[Distractor] User asks for format guidance → Nested question pushed to QUD"
            ),
            expected_trajectory=(
                "System pushes user's question to QUD: [Q_parties, Q_format], "
                "answers format question: "
                "'Use full legal names, e.g., Acme Corp and Smith Inc', "
                "pops Q_format, "
                "returns to Q_parties: 'What are the parties?'"
            ),
        ),
        # Distractor 5: Volunteer ALL remaining info
        ChoiceOption(
            id=6,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance=(
                "Acme Corp and Smith Inc, effective January 1, 2025, "
                "5 year term, governed by California law"
            ),
            description=("[Distractor] Volunteer ALL facts → System processes all, plan complete"),
            expected_trajectory=(
                "System integrates all 4 facts, "
                "removes all questions from issues, "
                "QUD empty, plan complete, "
                "system confirms: "
                "'I have all the information needed to draft the NDA'"
            ),
        ),
    ]


def get_scenario1_turn2a_distractors() -> list[ChoiceOption]:
    """Distractors for Scenario 1, Turn 4: Answering NDA type question.

    Expected: "Mutual"
    Context: System asked "Should this be a mutual or one-way NDA?"
            Previous commitment: parties(Acme Corp, Smith Inc)
    """
    return [
        # Expected move
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="Mutual",
            description="[Expected] Choose mutual NDA",
            expected_trajectory=(
                "System validates answer (valid alternative), "
                "pops 'nda_type' from QUD, "
                "adds commitment 'nda_type(mutual)', "
                "raises next question 'effective_date' to QUD"
            ),
        ),
        # Distractor 1: Alternative choice
        ChoiceOption(
            id=2,
            category=MoveCategory.EXPECTED,
            utterance="One-way",
            description="[Distractor] Choose one-way NDA → Different trajectory",
            expected_trajectory=(
                "System validates answer, "
                "adds commitment 'nda_type(one-way)', "
                "continues with effective_date question"
            ),
        ),
        # Distractor 2: Invalid answer
        ChoiceOption(
            id=3,
            category=MoveCategory.INVALID_ANSWER,
            utterance="Both",
            description=(
                "[Distractor] Invalid answer → Not a valid alternative, clarification requested"
            ),
            expected_trajectory=(
                "System validates: 'Both' not in [mutual, one-way] → False, "
                "generates clarification: "
                "'Please choose either mutual or one-way'"
            ),
        ),
        # Distractor 3: Ask for explanation
        ChoiceOption(
            id=4,
            category=MoveCategory.NESTED_QUESTION,
            utterance="What's the difference between mutual and one-way?",
            description=("[Distractor] User asks for explanation → System explains difference"),
            expected_trajectory=(
                "System pushes user's question to QUD, "
                "explains: 'Mutual means both parties protect info. "
                "One-way means only one party protects.', "
                "pops explanation question, "
                "returns to choice: 'Should this be mutual or one-way?'"
            ),
        ),
    ]


def get_scenario1_turn3_distractors() -> list[ChoiceOption]:
    """Distractors for Scenario 1, Turn 3: Answering effective date question.

    Expected: "January 1, 2025"
    Context: System asked "What is the effective date?"
            Previous commitment: parties(Acme Corp, Smith Inc)
    """
    return [
        # Expected move
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="January 1, 2025",
            description="[Expected] Valid date answer",
            expected_trajectory=(
                "System validates date format, "
                "pops 'effective_date' from QUD, "
                "adds commitment 'effective_date(January 1, 2025)', "
                "raises next question 'term' to QUD"
            ),
        ),
        # Distractor 1: Invalid date format
        ChoiceOption(
            id=2,
            category=MoveCategory.INVALID_ANSWER,
            utterance="yesterday",
            description=("[Distractor] Invalid date → System asks for proper date format"),
            expected_trajectory=(
                "System validates: 'yesterday' not valid date format, "
                "generates clarification: "
                "'Please provide a specific date (e.g., January 1, 2025)'"
            ),
        ),
        # Distractor 2: Correction of previous answer
        ChoiceOption(
            id=3,
            category=MoveCategory.CORRECTION,
            utterance=("Wait, I need to correct the parties. It should be XYZ Corp and Smith Inc"),
            description=(
                "[Distractor] User corrects previous answer → Belief revision (Rules 4.6-4.8)"
            ),
            expected_trajectory=(
                "System detects correction of 'parties' commitment, "
                "retracts old commitment: parties(Acme Corp, Smith Inc), "
                "re-accommodates Q_parties to private.issues, "
                "integrates new answer: parties(XYZ Corp, Smith Inc), "
                "checks dependent questions (none for parties), "
                "returns to current question: 'What is the effective date?'"
            ),
        ),
        # Distractor 3: Question about previous answer
        ChoiceOption(
            id=4,
            category=MoveCategory.NESTED_QUESTION,
            utterance="Can I change the parties I mentioned earlier?",
            description=(
                "[Distractor] Meta-question about revision → System explains revision capability"
            ),
            expected_trajectory=(
                "System pushes user's meta-question to QUD, "
                "answers: 'Yes, you can correct any information. Just say so.', "
                "pops meta-question, "
                "returns to current question: 'What is the effective date?'"
            ),
        ),
        # Distractor 4: Volunteer next answer
        ChoiceOption(
            id=5,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="January 1, 2025, with a 5 year term",
            description=(
                "[Distractor] Volunteer term duration → System processes both, skips term question"
            ),
            expected_trajectory=(
                "System integrates 'effective_date' (current question), "
                "integrates 'term' (volunteer from issues), "
                "removes Q_term from private.issues, "
                "raises Q_governing_law to QUD"
            ),
        ),
        # Distractor 5: Reject entire task
        ChoiceOption(
            id=6,
            category=MoveCategory.REJECTION,
            utterance="Actually, I don't want to draft an NDA anymore",
            description=("[Distractor] User cancels task → System retracts plan and commitments"),
            expected_trajectory=(
                "System detects task cancellation, "
                "clears private.plan, "
                "clears private.issues, "
                "clears shared.commitments, "
                "clears shared.qud, "
                "returns to idle: 'Okay. How can I help you?'"
            ),
        ),
        # Distractor 6: Ask about dependencies
        ChoiceOption(
            id=7,
            category=MoveCategory.NESTED_QUESTION,
            utterance="Does the effective date affect the term length?",
            description=("[Distractor] Question about dependencies → System explains relationship"),
            expected_trajectory=(
                "System pushes user's question to QUD, "
                "explains: 'The term is independent of effective date. "
                "Effective date is when NDA starts, "
                "term is how long it lasts.', "
                "pops explanation question, "
                "returns: 'What is the effective date?'"
            ),
        ),
    ]


def get_scenario1_turn4_distractors() -> list[ChoiceOption]:
    """Distractors for Scenario 1, Turn 8: Answering duration question.

    Expected: "5 years"
    Context: System asked "What is the duration of confidentiality obligations?"
            Previous commitments: parties, nda_type, effective_date
    """
    return [
        # Expected move
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="5 years",
            description="[Expected] Valid duration",
            expected_trajectory=(
                "System validates duration, "
                "pops 'duration' from QUD, "
                "adds commitment 'duration(5 years)', "
                "raises final question 'governing_law' to QUD"
            ),
        ),
        # Distractor 1: Invalid format
        ChoiceOption(
            id=2,
            category=MoveCategory.INVALID_ANSWER,
            utterance="a long time",
            description="[Distractor] Vague duration → Clarification requested",
            expected_trajectory=(
                "System validates: vague duration not acceptable, "
                "generates clarification: "
                "'Please specify duration in years (e.g., 5 years)'"
            ),
        ),
        # Distractor 2: Volunteer governing law
        ChoiceOption(
            id=3,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="5 years, governed by California law",
            description=(
                "[Distractor] Volunteer governing law → System processes both, completes plan"
            ),
            expected_trajectory=(
                "System integrates 'duration(5 years)', "
                "integrates 'governing_law(California)' (volunteer), "
                "all plan questions answered, "
                "QUD empty, plan complete, "
                "confirms: 'I have all the information needed'"
            ),
        ),
        # Distractor 3: Question about term
        ChoiceOption(
            id=4,
            category=MoveCategory.NESTED_QUESTION,
            utterance="Is 5 years typical for NDAs?",
            description=(
                "[Distractor] Meta question about typical duration → System provides guidance"
            ),
            expected_trajectory=(
                "System pushes user's question to QUD, "
                "explains: 'Typical NDAs range from 1-5 years. "
                "5 years is common for sensitive information.', "
                "pops meta-question, "
                "returns: 'What is the duration?'"
            ),
        ),
        # Distractor 4: Perpetual duration
        ChoiceOption(
            id=5,
            category=MoveCategory.EXPECTED,
            utterance="Perpetual",
            description="[Distractor] Perpetual duration → Valid alternative",
            expected_trajectory=(
                "System validates 'perpetual' as valid duration, "
                "adds commitment 'duration(perpetual)', "
                "continues to governing_law question"
            ),
        ),
    ]


def get_scenario1_turn5_distractors() -> list[ChoiceOption]:
    """Distractors for Scenario 1, Turn 10: Answering governing law question.

    Expected: "California"
    Context: System asked "Which state law should govern this agreement?"
            Previous commitments: parties, nda_type, effective_date, duration
            This is the FINAL question in the plan
    """
    return [
        # Expected move
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="California",
            description="[Expected] Choose California law → Plan complete",
            expected_trajectory=(
                "System validates answer (valid alternative), "
                "pops 'governing_law' from QUD, "
                "adds commitment 'governing_law(California)', "
                "all plan questions answered, QUD empty, "
                "confirms: 'I have all the information needed to draft your NDA'"
            ),
        ),
        # Distractor 1: Alternative state
        ChoiceOption(
            id=2,
            category=MoveCategory.EXPECTED,
            utterance="Delaware",
            description="[Distractor] Choose Delaware law → Valid alternative",
            expected_trajectory=(
                "System validates answer, adds commitment 'governing_law(Delaware)', plan complete"
            ),
        ),
        # Distractor 2: Invalid jurisdiction
        ChoiceOption(
            id=3,
            category=MoveCategory.INVALID_ANSWER,
            utterance="International law",
            description=(
                "[Distractor] Invalid jurisdiction → Not in alternatives, clarification requested"
            ),
            expected_trajectory=(
                "System validates: not in [California, Delaware, New York], "
                "generates clarification: "
                "'Please choose California, Delaware, or New York'"
            ),
        ),
        # Distractor 3: Correct previous answer
        ChoiceOption(
            id=4,
            category=MoveCategory.CORRECTION,
            utterance="Wait, I want to change the duration to 3 years instead of 5",
            description=(
                "[Distractor] Correction before final answer → Belief revision on duration"
            ),
            expected_trajectory=(
                "System detects correction of 'duration' commitment, "
                "retracts old: duration(5 years), "
                "integrates new: duration(3 years), "
                "returns to current question: 'Which state law?'"
            ),
        ),
        # Distractor 4: Ask about implications
        ChoiceOption(
            id=5,
            category=MoveCategory.NESTED_QUESTION,
            utterance="What are the differences between California and Delaware law?",
            description=(
                "[Distractor] User asks for legal comparison → System provides information"
            ),
            expected_trajectory=(
                "System pushes user's question to QUD, "
                "explains differences between state laws, "
                "pops explanation question, "
                "returns: 'Which state law should govern?'"
            ),
        ),
        # Distractor 5: Review before committing
        ChoiceOption(
            id=6,
            category=MoveCategory.NESTED_QUESTION,
            utterance="Can you review all the information we've collected?",
            description=("[Distractor] Request summary → System lists all commitments"),
            expected_trajectory=(
                "System pushes review request to QUD, "
                "lists all commitments: parties, nda_type, date, duration, "
                "pops review question, "
                "returns: 'Which state law?'"
            ),
        ),
    ]


# IBiS-4 Distractors


def get_action_confirmation_turn0_distractors() -> list[ChoiceOption]:
    """Distractors for Action Confirmation Turn 0 (Initial request).

    Expected: "Book a hotel in Paris from January 5 to January 10, 2025"
    Context: User is initiating an action-oriented dialogue
    """
    return [
        # Expected move (always option 1)
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="Book a hotel in Paris from January 5 to January 10, 2025",
            description="[Expected] Complete action request with all parameters",
            expected_trajectory=(
                "System forms booking plan with action: book_hotel(Paris, 2025-01-05, 2025-01-10), "
                "adds action to private.actions queue, "
                "generates confirmation question, "
                "raises confirmation to QUD"
            ),
        ),
        # Distractor 1: Missing critical parameters
        ChoiceOption(
            id=2,
            category=MoveCategory.INVALID_ANSWER,
            utterance="Book a hotel in Paris",
            description=(
                "[Distractor] Missing dates → "
                "System must ask follow-up questions for required parameters"
            ),
            expected_trajectory=(
                "System detects incomplete action (missing check_in, check_out), "
                "forms clarification plan with questions: "
                "'When is check-in?', 'When is check-out?', "
                "accommodates questions to private.issues, "
                "raises first question to QUD"
            ),
        ),
        # Distractor 2: Ambiguous parameters
        ChoiceOption(
            id=3,
            category=MoveCategory.CLARIFICATION_REQUEST,
            utterance="Book a hotel for next week",
            description=("[Distractor] Ambiguous time reference → System asks for specific dates"),
            expected_trajectory=(
                "System detects ambiguous temporal reference 'next week', "
                "generates clarification: 'What are the specific check-in and check-out dates?', "
                "pushes clarification to QUD"
            ),
        ),
        # Distractor 3: Volunteer multiple actions
        ChoiceOption(
            id=4,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance=(
                "Book a hotel in Paris from January 5 to January 10, 2025, "
                "and cancel my existing Paris booking"
            ),
            description=("[Distractor] Multiple actions → System queues both actions in sequence"),
            expected_trajectory=(
                "System forms two actions: cancel_booking(), book_hotel(Paris, ...), "
                "adds both to private.actions queue (FIFO), "
                "processes first action (cancel) with confirmation request"
            ),
        ),
        # Distractor 4: Nested question before action
        ChoiceOption(
            id=5,
            category=MoveCategory.NESTED_QUESTION,
            utterance="What hotels are available in Paris for January 5-10?",
            description=(
                "[Distractor] Information request before action → QUD stack, search dialogue"
            ),
            expected_trajectory=(
                "System pushes search question to QUD, "
                "performs hotel search, "
                "presents alternatives (may trigger negotiation via IUN), "
                "after selection, may lead to booking action"
            ),
        ),
        # Distractor 5: Request specific hotel
        ChoiceOption(
            id=6,
            category=MoveCategory.EXPECTED,
            utterance="Book Hotel de Paris from January 5 to January 10, 2025",
            description=(
                "[Distractor] Specific hotel named → System forms booking with exact hotel"
            ),
            expected_trajectory=(
                "System forms action: book_hotel(Hotel de Paris, Paris, 2025-01-05, 2025-01-10), "
                "queues action, "
                "raises confirmation to QUD with specific hotel name"
            ),
        ),
        # Distractor 6: Request without confirmation
        ChoiceOption(
            id=7,
            category=MoveCategory.CLARIFICATION_REQUEST,
            utterance="Book a hotel in Paris from January 5-10 without asking me to confirm",
            description=(
                "[Distractor] User requests optimistic execution → System bypasses confirmation"
            ),
            expected_trajectory=(
                "System detects user preference for optimistic mode, "
                "forms booking action, "
                "executes action IMMEDIATELY without confirmation, "
                "makes optimistic commitment, "
                "reports result (may need rollback if fails)"
            ),
        ),
        # Distractor 7: Volunteer preferences/constraints
        ChoiceOption(
            id=8,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance=(
                "Book a hotel in Paris from January 5 to January 10, 2025, "
                "with free breakfast and under $150 per night"
            ),
            description=("[Distractor] Volunteer constraints → System adds constraints to action"),
            expected_trajectory=(
                "System forms action with constraints: "
                "book_hotel(Paris, 2025-01-05, 2025-01-10, amenities=[breakfast], max_price=150), "
                "may need to search for hotels matching constraints, "
                "then raise confirmation with specific hotel meeting criteria"
            ),
        ),
        # Distractor 8: Meta-question about process
        ChoiceOption(
            id=9,
            category=MoveCategory.NESTED_QUESTION,
            utterance="How do I book a hotel?",
            description=(
                "[Distractor] Meta-question about booking process → System explains procedure"
            ),
            expected_trajectory=(
                "System pushes meta-question to QUD, "
                "provides explanation: "
                "'Provide city, check-in/out dates, I'll find options and confirm', "
                "pops meta-question, "
                "asks if user wants to proceed with booking"
            ),
        ),
    ]


def get_action_confirmation_turn2_distractors() -> list[ChoiceOption]:
    """Distractors for Action Confirmation Turn 2 (Confirmation response).

    Expected: "Yes"
    Context: System asked "Should I book Hotel de Paris for January 5-10, 2025?"
            Action is queued: book_hotel(Hotel de Paris, Paris, 2025-01-05, 2025-01-10)
    """
    return [
        # Expected move (always option 1)
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="Yes",
            description="[Expected] User confirms → action executes",
            expected_trajectory=(
                "System pops confirmation question from QUD, "
                "executes action from queue: book_hotel(...), "
                "makes commitment: hotel_booked(Hotel de Paris, 2025-01-05, 2025-01-10), "
                "removes action from queue, "
                "reports success: 'Booking confirmed. Hotel de Paris reserved.'"
            ),
        ),
        # Distractor 1: Explicit rejection
        ChoiceOption(
            id=2,
            category=MoveCategory.REJECTION,
            utterance="No",
            description=("[Distractor] Rejection → Action cancelled, queue cleared, plan aborted"),
            expected_trajectory=(
                "System pops confirmation question from QUD, "
                "removes action from queue WITHOUT executing, "
                "no commitment made, "
                "reports cancellation: 'Okay, I won't book the hotel', "
                "clears private.actions, "
                "returns to idle or asks if user wants different hotel"
            ),
        ),
        # Distractor 2: Rejection with reason
        ChoiceOption(
            id=3,
            category=MoveCategory.REJECTION,
            utterance="No, that hotel is too expensive",
            description=(
                "[Distractor] Rejection with constraint → System searches for alternatives"
            ),
            expected_trajectory=(
                "System pops confirmation, removes action from queue, "
                "extracts constraint: price_constraint(lower), "
                "initiates new search with constraint, "
                "may trigger negotiation dialogue with cheaper alternatives"
            ),
        ),
        # Distractor 3: Correction of dates
        ChoiceOption(
            id=4,
            category=MoveCategory.CORRECTION,
            utterance="Wait, change the dates to January 6-11 instead",
            description=(
                "[Distractor] Date correction → Parameter revision, new confirmation cycle"
            ),
            expected_trajectory=(
                "System detects correction, "
                "updates action parameters: "
                "book_hotel(Hotel de Paris, Paris, 2025-01-06, 2025-01-11), "
                "keeps action in queue, "
                "generates NEW confirmation question with updated dates, "
                "raises to QUD: 'Should I book Hotel de Paris for January 6-11, 2025?'"
            ),
        ),
        # Distractor 4: Correction of hotel
        ChoiceOption(
            id=5,
            category=MoveCategory.CORRECTION,
            utterance="Actually, I want a different hotel",
            description=("[Distractor] Hotel correction → Restarts search/selection process"),
            expected_trajectory=(
                "System removes current action from queue, "
                "asks clarification: 'Which hotel would you prefer?', "
                "may trigger search dialogue or negotiation with alternatives"
            ),
        ),
        # Distractor 5: Nested question - cancellation policy
        ChoiceOption(
            id=6,
            category=MoveCategory.NESTED_QUESTION,
            utterance="What are the cancellation terms for this hotel?",
            description=("[Distractor] Policy question → QUD push, answer, return to confirmation"),
            expected_trajectory=(
                "System pushes user's question to QUD: [Q_confirm, Q_cancellation], "
                "provides answer: 'Free cancellation up to 24 hours before check-in', "
                "pops Q_cancellation, "
                "returns to Q_confirm: 'Should I book Hotel de Paris for January 5-10?'"
            ),
        ),
        # Distractor 6: Nested question - hotel details
        ChoiceOption(
            id=7,
            category=MoveCategory.NESTED_QUESTION,
            utterance="What amenities does Hotel de Paris have?",
            description=(
                "[Distractor] Information request → "
                "QUD push, provide details, return to confirmation"
            ),
            expected_trajectory=(
                "System pushes amenities question to QUD, "
                "provides hotel details: 'Free WiFi, breakfast, gym, pool', "
                "pops amenities question, "
                "returns to confirmation: 'Should I book this hotel?'"
            ),
        ),
        # Distractor 7: Conditional acceptance
        ChoiceOption(
            id=8,
            category=MoveCategory.CLARIFICATION_REQUEST,
            utterance="Yes, but only if the price is under $200 per night",
            description=(
                "[Distractor] Conditional acceptance → System checks constraint before executing"
            ),
            expected_trajectory=(
                "System extracts constraint: max_price(200), "
                "checks if hotel meets constraint, "
                "if YES: executes action and confirms, "
                "if NO: rejects and searches for alternatives meeting constraint"
            ),
        ),
        # Distractor 8: Volunteer additional action
        ChoiceOption(
            id=9,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="Yes, and also book a flight to Paris for January 5",
            description=("[Distractor] Volunteer new action → Sequential action execution"),
            expected_trajectory=(
                "System confirms hotel booking (executes first action), "
                "forms second action: book_flight(Paris, 2025-01-05), "
                "adds to queue, "
                "after hotel confirmation, raises flight confirmation: "
                "'Should I book a flight to Paris for January 5?'"
            ),
        ),
        # Distractor 9: Request modification and confirmation
        ChoiceOption(
            id=10,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="Yes, and send me a confirmation email",
            description=(
                "[Distractor] Volunteer follow-up action → Action with chained sub-action"
            ),
            expected_trajectory=(
                "System confirms hotel booking (executes), "
                "forms follow-up action: send_confirmation_email(), "
                "adds to queue, "
                "executes email action (may or may not confirm), "
                "reports: 'Booking confirmed. Confirmation email sent.'"
            ),
        ),
        # Distractor 10: Ask for summary before confirming
        ChoiceOption(
            id=11,
            category=MoveCategory.NESTED_QUESTION,
            utterance="Can you summarize all the booking details first?",
            description=(
                "[Distractor] Request summary → QUD push, provide details, return to confirmation"
            ),
            expected_trajectory=(
                "System pushes summary request to QUD, "
                "provides full booking details: hotel, dates, price, location, "
                "pops summary question, "
                "returns to confirmation: 'Should I proceed with this booking?'"
            ),
        ),
        # Distractor 11: Defer decision
        ChoiceOption(
            id=12,
            category=MoveCategory.REJECTION,
            utterance="Let me think about it",
            description=("[Distractor] Soft rejection → Action remains queued, dialogue paused"),
            expected_trajectory=(
                "System keeps action in queue (doesn't remove), "
                "keeps confirmation in QUD or moves to pending state, "
                "acknowledges: 'Okay, let me know when you're ready', "
                "dialogue enters waiting state"
            ),
        ),
    ]


def get_negotiation_turn0_distractors() -> list[ChoiceOption]:
    """Distractors for Negotiation Turn 0 (Hotel search request)."""
    return [
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="Find me a hotel in Paris",
            description="[Expected] Initiates search → alternatives to IUN",
            expected_trajectory="System searches, presents alternatives in IUN",
        ),
        ChoiceOption(
            id=2,
            category=MoveCategory.CLARIFICATION_REQUEST,
            utterance="Find me the cheapest hotel in Paris",
            description="[Distractor] Constraint → May skip negotiation",
            expected_trajectory="System applies price filter, shows single best option",
        ),
        ChoiceOption(
            id=3,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="Find me a hotel in Paris under $150 with free breakfast",
            description="[Distractor] Volunteer constraints → Narrowed search space",
            expected_trajectory="System filters by price and amenities",
        ),
        ChoiceOption(
            id=4,
            category=MoveCategory.INVALID_ANSWER,
            utterance="What hotels are there?",
            description="[Distractor] Missing parameter → Clarification needed",
            expected_trajectory="System asks for clarification: which city?",
        ),
    ]


def get_negotiation_turn2_distractors() -> list[ChoiceOption]:
    """Distractors for Negotiation Turn 2 (Rejection of expensive option)."""
    return [
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="No, Hotel Expensive is too expensive",
            description="[Expected] Rejection → IUN update, next option",
            expected_trajectory="System removes from IUN, proposes next alternative",
        ),
        ChoiceOption(
            id=2,
            category=MoveCategory.CORRECTION,
            utterance="Yes, I'll take Hotel Expensive",
            description="[Distractor] Accept first → Negotiation ends immediately",
            expected_trajectory="System commits to expensive option, ends negotiation",
        ),
        ChoiceOption(
            id=3,
            category=MoveCategory.NESTED_QUESTION,
            utterance="Show me more hotels",
            description="[Distractor] Search expansion, more alternatives",
            expected_trajectory="System expands search, adds more options to IUN",
        ),
        ChoiceOption(
            id=4,
            category=MoveCategory.NESTED_QUESTION,
            utterance="What amenities does Hotel Expensive have?",
            description="[Distractor] Information request → QUD push, return to IUN",
            expected_trajectory="System provides details, returns to negotiation",
        ),
        ChoiceOption(
            id=5,
            category=MoveCategory.CLARIFICATION_REQUEST,
            utterance="I'll take Hotel Expensive if you can get it for $150",
            description="[Distractor] Counter-proposal → Price negotiation sub-dialogue",
            expected_trajectory="System attempts counter-offer negotiation",
        ),
    ]


def get_negotiation_turn4_distractors() -> list[ChoiceOption]:
    """Distractors for Negotiation Turn 4 (Acceptance of budget option)."""
    return [
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="Yes, that works!",
            description="[Expected] Accept → IUN cleared, commitment added",
            expected_trajectory="System clears IUN, commits to hotel, proceeds",
        ),
        ChoiceOption(
            id=2,
            category=MoveCategory.REJECTION,
            utterance="No, show me more options",
            description="[Distractor] Search continues, new options to IUN",
            expected_trajectory="System expands search, presents more alternatives",
        ),
        ChoiceOption(
            id=3,
            category=MoveCategory.REJECTION,
            utterance="Actually, let me think about it",
            description="[Distractor] Rejection (soft) → IUN preserved, dialogue paused",
            expected_trajectory="System keeps options in IUN, pauses negotiation",
        ),
        ChoiceOption(
            id=4,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="Yes, and book it for January 5-10",
            description="[Distractor] Volunteer info → Commitment + action queued",
            expected_trajectory="System commits to hotel AND queues booking action",
        ),
    ]


def get_rollback_turn0_distractors() -> list[ChoiceOption]:
    """Distractors for Rollback Turn 0 (Booking request)."""
    return [
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="Book Hotel de Paris for January 5-10, 2025",
            description="[Expected] Action queued → Optimistic execution attempt",
            expected_trajectory="System queues action, attempts optimistic execution",
        ),
        ChoiceOption(
            id=2,
            category=MoveCategory.INVALID_ANSWER,
            utterance="Book Hotel de Paris",
            description="[Distractor] Missing parameters → Clarification needed",
            expected_trajectory="System asks for missing dates",
        ),
        ChoiceOption(
            id=3,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance=(
                "Book Hotel de Paris for January 5-10, 2025, and send confirmation to my email"
            ),
            description="[Distractor] Volunteer action → Multiple action sequence",
            expected_trajectory="System queues two actions: book + send_email",
        ),
        ChoiceOption(
            id=4,
            category=MoveCategory.CLARIFICATION_REQUEST,
            utterance="Try to book Hotel de Paris, but don't worry if it fails",
            description="[Distractor] Conditional action → Different error handling",
            expected_trajectory="System sets tentative mode, handles failure silently",
        ),
    ]


# Mapping from scenario and turn to distractors
SCENARIO_DISTRACTORS = {
    "Incremental Questioning": {
        0: get_scenario1_turn1_distractors,  # Turn 0: Initial request
        2: get_scenario1_turn2_distractors,  # Turn 2: Parties answer
        4: get_scenario1_turn2a_distractors,  # Turn 4: NDA type answer (NEW)
        6: get_scenario1_turn3_distractors,  # Turn 6: Effective date answer (moved)
        8: get_scenario1_turn4_distractors,  # Turn 8: Duration answer (NEW)
        10: get_scenario1_turn5_distractors,  # Turn 10: Governing law answer (NEW)
    },
    "Action Confirmation": {
        0: get_action_confirmation_turn0_distractors,  # Turn 0: Booking request
        2: get_action_confirmation_turn2_distractors,  # Turn 2: Confirmation response
    },
    "Negotiation with Alternatives": {
        0: get_negotiation_turn0_distractors,  # Turn 0: Hotel search
        2: get_negotiation_turn2_distractors,  # Turn 2: Reject expensive
        4: get_negotiation_turn4_distractors,  # Turn 4: Accept budget
    },
    "Action Rollback": {
        0: get_rollback_turn0_distractors,  # Turn 0: Booking request
    },
}


def get_distractors_for_turn(scenario_name: str, turn_index: int) -> list[ChoiceOption] | None:
    """Get specific distractors for a scenario turn.

    Args:
        scenario_name: Name of the scenario
        turn_index: The turn index in the scenario

    Returns:
        List of choice options or None if no specific distractors defined
    """
    if scenario_name in SCENARIO_DISTRACTORS:
        turn_map = SCENARIO_DISTRACTORS[scenario_name]
        if turn_index in turn_map:
            return turn_map[turn_index]()
    return None
