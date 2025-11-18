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
        # Distractor 1: Alternative choice (incomplete)
        ChoiceOption(
            id=2,
            category=MoveCategory.INVALID_ANSWER,
            utterance="One-way",
            description="[Distractor] Choose one-way (incomplete) → Triggers clarification",
            expected_trajectory=(
                "System detects incomplete answer (one-way NDA needs disclosing party), "
                "generates clarification question: 'Who is the disclosing party?'"
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
    """Distractors for Negotiation Turn 0 (Hotel search request).

    Expected: "Find me a hotel in Paris"
    Context: User initiates search that will trigger negotiation with alternatives
    """
    return [
        # Expected move (always option 1)
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="Find me a hotel in Paris",
            description="[Expected] Initiates search → alternatives to IUN",
            expected_trajectory=(
                "System performs hotel search for Paris, "
                "finds multiple options, "
                "adds alternatives to private.iun: [Hotel Expensive, Hotel Budget], "
                "presents both options to user for negotiation"
            ),
        ),
        # Distractor 1: Search with price constraint
        ChoiceOption(
            id=2,
            category=MoveCategory.CLARIFICATION_REQUEST,
            utterance="Find me the cheapest hotel in Paris",
            description=(
                "[Distractor] Price constraint → May skip negotiation if single best match"
            ),
            expected_trajectory=(
                "System applies price filter (minimum price), "
                "searches for cheapest hotel, "
                "if single match: skips IUN, presents single option, "
                "if multiple matches: adds to IUN for negotiation"
            ),
        ),
        # Distractor 2: Search with multiple constraints
        ChoiceOption(
            id=3,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="Find me a hotel in Paris under $150 with free breakfast",
            description=("[Distractor] Multiple constraints → Narrowed search space, targeted IUN"),
            expected_trajectory=(
                "System extracts constraints: max_price(150), amenities(breakfast), "
                "filters search results, "
                "adds matching options to IUN, "
                "presents filtered alternatives for negotiation"
            ),
        ),
        # Distractor 3: Missing location parameter
        ChoiceOption(
            id=4,
            category=MoveCategory.INVALID_ANSWER,
            utterance="What hotels are there?",
            description=("[Distractor] Missing location → Clarification required before search"),
            expected_trajectory=(
                "System detects missing required parameter (location), "
                "forms clarification question: 'Which city are you looking for hotels in?', "
                "pushes to QUD, "
                "after answer, performs search"
            ),
        ),
        # Distractor 4: Search with date range
        ChoiceOption(
            id=5,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="Find me a hotel in Paris for January 5-10, 2025",
            description=("[Distractor] Volunteer dates → Search with availability constraint"),
            expected_trajectory=(
                "System extracts location + dates, "
                "searches for hotels available for specified dates, "
                "filters by availability, "
                "adds available options to IUN"
            ),
        ),
        # Distractor 5: Specific hotel request (no search needed)
        ChoiceOption(
            id=6,
            category=MoveCategory.EXPECTED,
            utterance="Is Hotel de Paris available?",
            description=("[Distractor] Specific hotel query → Direct lookup, no IUN negotiation"),
            expected_trajectory=(
                "System recognizes specific hotel request, "
                "performs direct availability check (not search), "
                "skips IUN negotiation, "
                "provides yes/no answer with details"
            ),
        ),
        # Distractor 6: Comparative search
        ChoiceOption(
            id=7,
            category=MoveCategory.NESTED_QUESTION,
            utterance="Compare hotels in Paris by price",
            description=("[Distractor] Comparison request → Structured presentation, may use IUN"),
            expected_trajectory=(
                "System performs search, "
                "sorts results by price, "
                "presents ranked comparison (may use IUN for selection), "
                "user can select from ranked list"
            ),
        ),
        # Distractor 7: Search with preference expression
        ChoiceOption(
            id=8,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="I prefer boutique hotels in Paris near the Eiffel Tower",
            description=("[Distractor] Volunteer preferences → Soft constraints in search"),
            expected_trajectory=(
                "System extracts preferences: style(boutique), location(near Eiffel Tower), "
                "uses as soft constraints in search ranking, "
                "presents best matches via IUN, "
                "negotiates based on preference satisfaction"
            ),
        ),
        # Distractor 8: Request with explicit alternative limit
        ChoiceOption(
            id=9,
            category=MoveCategory.CLARIFICATION_REQUEST,
            utterance="Show me 3 hotel options in Paris",
            description=("[Distractor] Explicit alternative limit → Constrained IUN size"),
            expected_trajectory=(
                "System notes user preference for 3 options, "
                "performs search, "
                "selects top 3 matches (by ranking), "
                "adds exactly 3 to IUN, "
                "presents for negotiation"
            ),
        ),
        # Distractor 9: Meta-question about hotels
        ChoiceOption(
            id=10,
            category=MoveCategory.NESTED_QUESTION,
            utterance="What's the average hotel price in Paris?",
            description=("[Distractor] Information request → QUD push, provide info, then search"),
            expected_trajectory=(
                "System pushes information question to QUD, "
                "provides answer: 'Average price is $180/night', "
                "pops question, "
                "asks if user wants to search for hotels"
            ),
        ),
    ]


def get_negotiation_turn2_distractors() -> list[ChoiceOption]:
    """Distractors for Negotiation Turn 2 (Rejection of expensive option).

    Expected: "No, Hotel Expensive is too expensive"
    Context: System presented two hotels (Expensive $200, Budget $120)
            Both in IUN, user must respond to first option
    """
    return [
        # Expected move (always option 1)
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="No, Hotel Expensive is too expensive",
            description="[Expected] Rejection with reason → IUN update, next option",
            expected_trajectory=(
                "System removes Hotel Expensive from IUN, "
                "IUN now contains: [Hotel Budget], "
                "proposes next alternative: 'How about Hotel Budget at $120/night?', "
                "continues negotiation"
            ),
        ),
        # Distractor 1: Simple rejection without reason
        ChoiceOption(
            id=2,
            category=MoveCategory.EXPECTED,
            utterance="No",
            description=("[Distractor] Simple rejection → IUN update, may ask for reason"),
            expected_trajectory=(
                "System removes Hotel Expensive from IUN, "
                "no explicit reason given, "
                "may ask clarification: 'Why not?', "
                "or proceeds to next option: Hotel Budget"
            ),
        ),
        # Distractor 2: Accept first option
        ChoiceOption(
            id=3,
            category=MoveCategory.EXPECTED,
            utterance="Yes, I'll take Hotel Expensive",
            description=("[Distractor] Accept first → Negotiation ends, commitment made"),
            expected_trajectory=(
                "System clears IUN (negotiation resolved), "
                "makes commitment: hotel_selected(Hotel Expensive), "
                "ends negotiation, "
                "confirms: 'Great! I'll proceed with Hotel Expensive'"
            ),
        ),
        # Distractor 3: Request more options
        ChoiceOption(
            id=4,
            category=MoveCategory.NESTED_QUESTION,
            utterance="Show me more hotels",
            description=("[Distractor] Search expansion → More alternatives added to IUN"),
            expected_trajectory=(
                "System keeps current IUN: [Hotel Expensive, Hotel Budget], "
                "performs additional search, "
                "finds more options, "
                "adds to IUN: [Hotel Expensive, Hotel Budget, Hotel Moderate, ...], "
                "presents expanded alternatives"
            ),
        ),
        # Distractor 4: Ask about specific hotel details
        ChoiceOption(
            id=5,
            category=MoveCategory.NESTED_QUESTION,
            utterance="What amenities does Hotel Expensive have?",
            description=(
                "[Distractor] Information request → QUD push, provide details, "
                "return to negotiation"
            ),
            expected_trajectory=(
                "System pushes amenity question to QUD, "
                "provides hotel details: 'Pool, spa, gym, breakfast, WiFi', "
                "pops question, "
                "returns to IUN negotiation: 'Would you like Hotel Expensive?'"
            ),
        ),
        # Distractor 5: Counter-proposal with price negotiation
        ChoiceOption(
            id=6,
            category=MoveCategory.CLARIFICATION_REQUEST,
            utterance="I'll take Hotel Expensive if you can get it for $150",
            description=("[Distractor] Counter-proposal → Price negotiation sub-dialogue"),
            expected_trajectory=(
                "System extracts counter-offer: max_price(150) for Hotel Expensive, "
                "attempts price negotiation with hotel, "
                "if successful: commits to hotel at negotiated price, "
                "if failed: returns to IUN with original options"
            ),
        ),
        # Distractor 6: Reject with different constraint
        ChoiceOption(
            id=7,
            category=MoveCategory.REJECTION,
            utterance="No, I need something with a pool",
            description=("[Distractor] Rejection with new constraint → Filtered search"),
            expected_trajectory=(
                "System extracts constraint: amenities(pool), "
                "filters current IUN by constraint, "
                "if Hotel Budget has pool: keeps in IUN, "
                "if not: expands search with pool constraint, "
                "presents filtered alternatives"
            ),
        ),
        # Distractor 7: Request comparison
        ChoiceOption(
            id=8,
            category=MoveCategory.NESTED_QUESTION,
            utterance="What's the difference between these two hotels?",
            description=(
                "[Distractor] Comparison request → QUD push, provide comparison, return to IUN"
            ),
            expected_trajectory=(
                "System pushes comparison question to QUD, "
                "generates comparison: price, amenities, location, ratings, "
                "presents side-by-side comparison, "
                "pops question, "
                "returns to negotiation"
            ),
        ),
        # Distractor 8: Partial acceptance with condition
        ChoiceOption(
            id=9,
            category=MoveCategory.CLARIFICATION_REQUEST,
            utterance="Hotel Expensive is okay if it includes breakfast",
            description=("[Distractor] Conditional acceptance → Constraint verification"),
            expected_trajectory=(
                "System extracts condition: must_include(breakfast), "
                "checks if Hotel Expensive includes breakfast, "
                "if YES: commits to hotel, "
                "if NO: keeps in IUN but marks as conditional, "
                "proceeds to next alternative"
            ),
        ),
        # Distractor 9: Reject both, request new search
        ChoiceOption(
            id=10,
            category=MoveCategory.REJECTION,
            utterance="Neither of these work. Can you find hotels near the Louvre instead?",
            description=("[Distractor] Reject all + new constraint → Clear IUN, new search"),
            expected_trajectory=(
                "System clears IUN: [], "
                "extracts new constraint: location(near Louvre), "
                "performs new search with location constraint, "
                "populates IUN with new results, "
                "presents new alternatives"
            ),
        ),
        # Distractor 10: Ask about policy/terms
        ChoiceOption(
            id=11,
            category=MoveCategory.NESTED_QUESTION,
            utterance="What's the cancellation policy for Hotel Expensive?",
            description=("[Distractor] Policy question → QUD push, provide policy, return to IUN"),
            expected_trajectory=(
                "System pushes policy question to QUD, "
                "provides cancellation terms: 'Free cancellation 24hrs before', "
                "pops question, "
                "returns to negotiation: 'Would you like Hotel Expensive?'"
            ),
        ),
        # Distractor 11: Defer decision
        ChoiceOption(
            id=12,
            category=MoveCategory.REJECTION,
            utterance="Let me think about these options",
            description=("[Distractor] Defer decision → IUN preserved, dialogue paused"),
            expected_trajectory=(
                "System keeps IUN unchanged: [Hotel Expensive, Hotel Budget], "
                "pauses negotiation, "
                "acknowledges: 'Take your time. Let me know when you're ready', "
                "dialogue enters waiting state"
            ),
        ),
    ]


def get_negotiation_turn4_distractors() -> list[ChoiceOption]:
    """Distractors for Negotiation Turn 4 (Acceptance of budget option).

    Expected: "Yes, that works!"
    Context: System asked "How about Hotel Budget at $120/night?"
            Hotel Expensive was rejected, IUN contains: [Hotel Budget]
    """
    return [
        # Expected move (always option 1)
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="Yes, that works!",
            description="[Expected] Accept → IUN cleared, commitment added, negotiation ends",
            expected_trajectory=(
                "System clears IUN: [], "
                "makes commitment: hotel_selected(Hotel Budget), "
                "ends negotiation, "
                "confirms: 'Great! I'll proceed with Hotel Budget'"
            ),
        ),
        # Distractor 1: Enthusiastic acceptance
        ChoiceOption(
            id=2,
            category=MoveCategory.EXPECTED,
            utterance="Perfect! That's exactly what I need",
            description=("[Distractor] Enthusiastic acceptance → Same as standard acceptance"),
            expected_trajectory=("System clears IUN, commits to Hotel Budget, ends negotiation"),
        ),
        # Distractor 2: Reject and request more options
        ChoiceOption(
            id=3,
            category=MoveCategory.REJECTION,
            utterance="No, show me more options",
            description=("[Distractor] Rejection → Search expansion, more alternatives to IUN"),
            expected_trajectory=(
                "System removes Hotel Budget from IUN, "
                "IUN now: [], "
                "performs expanded search, "
                "adds new options to IUN, "
                "presents new alternatives for negotiation"
            ),
        ),
        # Distractor 3: Defer decision
        ChoiceOption(
            id=4,
            category=MoveCategory.REJECTION,
            utterance="Actually, let me think about it",
            description=("[Distractor] Soft rejection → IUN preserved, dialogue paused"),
            expected_trajectory=(
                "System keeps Hotel Budget in IUN, "
                "pauses negotiation, "
                "acknowledges: 'Take your time. Let me know when you decide', "
                "dialogue enters waiting state"
            ),
        ),
        # Distractor 4: Accept with booking action
        ChoiceOption(
            id=5,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="Yes, and book it for January 5-10, 2025",
            description=("[Distractor] Volunteer dates + booking → Commitment + action queued"),
            expected_trajectory=(
                "System clears IUN, "
                "makes commitment: hotel_selected(Hotel Budget), "
                "extracts dates: 2025-01-05 to 2025-01-10, "
                "forms booking action: book_hotel(Hotel Budget, 2025-01-05, 2025-01-10), "
                "adds to action queue, "
                "requests confirmation for booking"
            ),
        ),
        # Distractor 5: Ask for more details before deciding
        ChoiceOption(
            id=6,
            category=MoveCategory.NESTED_QUESTION,
            utterance="What are the check-in and check-out times?",
            description=(
                "[Distractor] Information request → QUD push, provide info, return to negotiation"
            ),
            expected_trajectory=(
                "System pushes hotel policy question to QUD, "
                "provides answer: 'Check-in 3pm, check-out 11am', "
                "pops question, "
                "returns to negotiation: 'Would you like Hotel Budget?'"
            ),
        ),
        # Distractor 6: Reject with new constraint
        ChoiceOption(
            id=7,
            category=MoveCategory.REJECTION,
            utterance="No, I need a hotel with free parking",
            description=("[Distractor] Rejection with constraint → Filtered new search"),
            expected_trajectory=(
                "System removes Hotel Budget from IUN, "
                "extracts constraint: amenities(parking), "
                "performs new search with parking constraint, "
                "adds matching options to IUN, "
                "presents new alternatives"
            ),
        ),
        # Distractor 7: Counter-proposal on budget option
        ChoiceOption(
            id=8,
            category=MoveCategory.CLARIFICATION_REQUEST,
            utterance="I'll take it if it includes breakfast",
            description=("[Distractor] Conditional acceptance → Constraint verification"),
            expected_trajectory=(
                "System extracts condition: must_include(breakfast), "
                "checks if Hotel Budget includes breakfast, "
                "if YES: clears IUN, commits to hotel, "
                "if NO: asks if user still wants it or search for alternatives with breakfast"
            ),
        ),
        # Distractor 8: Ask to compare with rejected option
        ChoiceOption(
            id=9,
            category=MoveCategory.NESTED_QUESTION,
            utterance="Can you remind me how this compares to Hotel Expensive?",
            description=("[Distractor] Comparison request → QUD push, compare, return to IUN"),
            expected_trajectory=(
                "System pushes comparison question to QUD, "
                "compares Hotel Budget vs Hotel Expensive: "
                "price ($120 vs $200), amenities, location, "
                "pops question, "
                "returns to negotiation: 'Would you like Hotel Budget?'"
            ),
        ),
        # Distractor 9: Accept and volunteer additional preferences
        ChoiceOption(
            id=10,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="Yes, and I'd also like to book a rental car",
            description=("[Distractor] Accept + volunteer new task → Sequential task handling"),
            expected_trajectory=(
                "System clears IUN, commits to Hotel Budget, "
                "extracts new task: book_rental_car, "
                "ends hotel negotiation, "
                "initiates rental car dialogue: 'What type of car do you need?'"
            ),
        ),
        # Distractor 10: Request to reconsider previous option
        ChoiceOption(
            id=11,
            category=MoveCategory.CORRECTION,
            utterance="Actually, maybe Hotel Expensive wasn't so bad. Can I reconsider?",
            description=("[Distractor] Reconsider rejected option → Re-add to IUN"),
            expected_trajectory=(
                "System re-adds Hotel Expensive to IUN, "
                "IUN now: [Hotel Budget, Hotel Expensive], "
                "presents both options again for reconsideration, "
                "restarts negotiation with both alternatives"
            ),
        ),
        # Distractor 11: Reject and ask for different location
        ChoiceOption(
            id=12,
            category=MoveCategory.REJECTION,
            utterance="No, I'd rather look for hotels in a different area",
            description=("[Distractor] Location change → Clear IUN, new search with new location"),
            expected_trajectory=(
                "System clears IUN, "
                "asks clarification: 'Which area would you prefer?', "
                "after answer, performs new location-based search, "
                "populates IUN with new results"
            ),
        ),
    ]


def get_rollback_turn0_distractors() -> list[ChoiceOption]:
    """Distractors for Rollback Turn 0 (Booking request).

    Expected: "Book Hotel de Paris for January 5-10, 2025"
    Context: User initiates booking with optimistic execution
            This will trigger rollback scenario when payment fails
    """
    return [
        # Expected move (always option 1)
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="Book Hotel de Paris for January 5-10, 2025",
            description="[Expected] Action queued → Optimistic execution, will fail and rollback",
            expected_trajectory=(
                "System forms booking action: book_hotel(Hotel de Paris, 2025-01-05, 2025-01-10), "
                "adds to action queue, "
                "executes optimistically (no confirmation in optimistic mode), "
                "makes optimistic commitment: hotel_booked(...), "
                "execution fails: payment declined, "
                "performs rollback: removes commitment, "
                "offers recovery: 'Would you like to try a different payment method?'"
            ),
        ),
        # Distractor 1: Missing dates parameter
        ChoiceOption(
            id=2,
            category=MoveCategory.INVALID_ANSWER,
            utterance="Book Hotel de Paris",
            description=("[Distractor] Missing dates → Clarification dialogue before action"),
            expected_trajectory=(
                "System detects incomplete action (missing dates), "
                "forms clarification questions: 'When is check-in?', 'When is check-out?', "
                "after collecting dates, queues action, "
                "executes optimistically"
            ),
        ),
        # Distractor 2: Multiple actions volunteered
        ChoiceOption(
            id=3,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance=(
                "Book Hotel de Paris for January 5-10, 2025, and send confirmation to my email"
            ),
            description=(
                "[Distractor] Multiple actions → "
                "Sequential execution, both may need rollback if booking fails"
            ),
            expected_trajectory=(
                "System forms two actions: book_hotel(...), send_email(confirmation), "
                "adds both to queue (FIFO), "
                "executes booking optimistically, "
                "if booking fails: rolls back, skips email action, "
                "if booking succeeds: proceeds with email action"
            ),
        ),
        # Distractor 3: Tentative/conditional request
        ChoiceOption(
            id=4,
            category=MoveCategory.CLARIFICATION_REQUEST,
            utterance="Try to book Hotel de Paris for January 5-10, but don't worry if it fails",
            description=(
                "[Distractor] Tentative action → Softer error handling, no recovery offered"
            ),
            expected_trajectory=(
                "System detects tentative mode ('try', 'don't worry'), "
                "forms action with tentative flag, "
                "executes optimistically, "
                "if fails: performs rollback, "
                "reports failure but doesn't offer recovery (user said not to worry)"
            ),
        ),
        # Distractor 4: Request with payment method specified
        ChoiceOption(
            id=5,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance=(
                "Book Hotel de Paris for January 5-10, 2025, using my credit card ending in 1234"
            ),
            description=(
                "[Distractor] Volunteer payment method → "
                "Explicit payment, may prevent failure or provide different error"
            ),
            expected_trajectory=(
                "System extracts payment method: credit_card(1234), "
                "forms action with payment method, "
                "executes optimistically with specified payment, "
                "may still fail for different reason (insufficient funds), "
                "rollback and recovery with payment context"
            ),
        ),
        # Distractor 5: Request with cancellation insurance
        ChoiceOption(
            id=6,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance=("Book Hotel de Paris for January 5-10, 2025, with cancellation insurance"),
            description=(
                "[Distractor] Volunteer add-on → More complex action, more to rollback on failure"
            ),
            expected_trajectory=(
                "System forms action with add-on: book_hotel(..., insurance=True), "
                "executes optimistically, "
                "if fails: rolls back both booking AND insurance, "
                "recovery offer includes option to try without insurance"
            ),
        ),
        # Distractor 6: Cautious request (wants confirmation)
        ChoiceOption(
            id=7,
            category=MoveCategory.CLARIFICATION_REQUEST,
            utterance="Please confirm before booking Hotel de Paris for January 5-10, 2025",
            description=(
                "[Distractor] Request confirmation → "
                "Switches to cautious mode, no optimistic execution, no rollback needed"
            ),
            expected_trajectory=(
                "System detects confirmation request ('please confirm'), "
                "overrides optimistic mode → cautious mode, "
                "forms action but doesn't execute immediately, "
                "asks confirmation: 'Should I book Hotel de Paris?', "
                "waits for user approval before execution"
            ),
        ),
        # Distractor 7: Request with specific room type
        ChoiceOption(
            id=8,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="Book a deluxe suite at Hotel de Paris for January 5-10, 2025",
            description=(
                "[Distractor] Volunteer room type → "
                "Constraint in booking, may fail due to unavailability"
            ),
            expected_trajectory=(
                "System forms action with room constraint: "
                "book_hotel(Hotel de Paris, room_type=deluxe_suite, ...), "
                "executes optimistically, "
                "if fails (unavailable or payment): performs rollback, "
                "recovery may offer alternative room types"
            ),
        ),
        # Distractor 8: Request check availability first
        ChoiceOption(
            id=9,
            category=MoveCategory.NESTED_QUESTION,
            utterance="Is Hotel de Paris available January 5-10, 2025? If so, book it",
            description=(
                "[Distractor] Check before booking → Two-step process, verification then action"
            ),
            expected_trajectory=(
                "System forms availability check question, "
                "pushes to QUD, "
                "performs availability lookup, "
                "if available: forms booking action, executes optimistically, "
                "if not available: reports unavailability, skips booking"
            ),
        ),
        # Distractor 9: Request with price constraint
        ChoiceOption(
            id=10,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="Book Hotel de Paris for January 5-10, 2025, if it's under $200/night",
            description=(
                "[Distractor] Conditional with price → "
                "Pre-execution check, may prevent action entirely"
            ),
            expected_trajectory=(
                "System extracts price constraint: max_price(200), "
                "checks Hotel de Paris price, "
                "if under $200: executes booking optimistically, "
                "if over $200: skips action, "
                "reports: 'Hotel de Paris is $250/night, exceeds your budget'"
            ),
        ),
        # Distractor 10: Request immediate booking with urgency
        ChoiceOption(
            id=11,
            category=MoveCategory.CLARIFICATION_REQUEST,
            utterance="Book Hotel de Paris for January 5-10, 2025, ASAP! It's urgent",
            description=(
                "[Distractor] Urgent request → "
                "Optimistic execution emphasized, same rollback but urgency noted"
            ),
            expected_trajectory=(
                "System detects urgency markers ('ASAP', 'urgent'), "
                "prioritizes action execution, "
                "executes optimistically without delay, "
                "if fails: performs rollback, "
                "recovery offers expedited alternatives"
            ),
        ),
    ]


# IBiS-3 Additional Scenario Distractors


def get_volunteer_info_turn0_distractors() -> list[ChoiceOption]:
    """Distractors for Volunteer Information Turn 0 (NDA request).

    Expected: "I need to draft an NDA"
    Context: User initiates NDA drafting task
    """
    return [
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="I need to draft an NDA",
            description="[Expected] Clear task initiation",
            expected_trajectory=(
                "System forms NDA drafting plan, "
                "accommodates questions to private.issues: [parties, type, date, duration, law], "
                "raises first question to QUD"
            ),
        ),
        ChoiceOption(
            id=2,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="I need to draft an NDA between Acme Corp and Smith Inc",
            description="[Distractor] Volunteer parties immediately → Skip first question",
            expected_trajectory=(
                "System forms plan, "
                "accommodates parties answer to shared.commitments, "
                "removes parties question from private.issues, "
                "raises next question (NDA type) to QUD"
            ),
        ),
        ChoiceOption(
            id=3,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="I need a mutual NDA effective January 1, 2025",
            description="[Distractor] Volunteer type and date → Skip multiple questions",
            expected_trajectory=(
                "System forms plan, "
                "accommodates type and date to commitments, "
                "removes both questions from issues, "
                "raises next unanswered question to QUD"
            ),
        ),
        ChoiceOption(
            id=4,
            category=MoveCategory.CLARIFICATION_REQUEST,
            utterance="Help me create an NDA",
            description="[Distractor] Vague request → System provides guidance",
            expected_trajectory=(
                "System recognizes help request, "
                "provides NDA explanation/guidance, "
                "then initiates NDA plan with first question"
            ),
        ),
        ChoiceOption(
            id=5,
            category=MoveCategory.NESTED_QUESTION,
            utterance="What is an NDA?",
            description="[Distractor] Definition question → QUD push before task",
            expected_trajectory=(
                "System pushes definition question to QUD, "
                "provides explanation, "
                "pops question, "
                "asks if user wants to proceed with NDA drafting"
            ),
        ),
        ChoiceOption(
            id=6,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance=(
                "I need an NDA between Acme and Smith, mutual, "
                "5 years, California law, effective now"
            ),
            description="[Distractor] Volunteer ALL info → Direct to generation",
            expected_trajectory=(
                "System extracts all parameters, "
                "accommodates all to commitments, "
                "plan immediately complete, "
                "skips all questions, "
                "generates NDA document directly"
            ),
        ),
    ]


def get_volunteer_info_turn2_distractors() -> list[ChoiceOption]:
    """Distractors for Volunteer Information Turn 2 (Parties + date).

    Expected: "Acme Corp and Smith Inc, effective January 1, 2025"
    Context: System asked "What are the parties to the NDA?"
            User volunteers parties AND effective date
    """
    return [
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="Acme Corp and Smith Inc, effective January 1, 2025",
            description=("[Expected] Answer parties + volunteer date → Skip date question"),
            expected_trajectory=(
                "System accommodates both commitments, "
                "pops parties question from QUD, "
                "removes date question from private.issues, "
                "raises next question (duration) to QUD"
            ),
        ),
        ChoiceOption(
            id=2,
            category=MoveCategory.EXPECTED,
            utterance="Acme Corp and Smith Inc",
            description="[Distractor] Answer only what's asked → Normal flow",
            expected_trajectory=(
                "System accommodates parties to commitments, "
                "pops question from QUD, "
                "raises next question (NDA type) to QUD"
            ),
        ),
        ChoiceOption(
            id=3,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance=(
                "Acme Corp and Smith Inc, mutual NDA, 3 years, "
                "California law, effective January 1, 2025"
            ),
            description="[Distractor] Volunteer ALL remaining → Complete plan",
            expected_trajectory=(
                "System accommodates all commitments, "
                "clears all private.issues, "
                "plan complete, "
                "proceeds to NDA generation"
            ),
        ),
        ChoiceOption(
            id=4,
            category=MoveCategory.INVALID_ANSWER,
            utterance="Acme and Smith",
            description="[Distractor] Ambiguous/incomplete → Clarification needed",
            expected_trajectory=(
                "System detects ambiguity (informal names), "
                "asks clarification: 'Do you mean Acme Corp and Smith Inc?', "
                "raises clarification to QUD"
            ),
        ),
        ChoiceOption(
            id=5,
            category=MoveCategory.CORRECTION,
            utterance="Actually, it's between Acme Corp and Jones LLC, not Smith",
            description="[Distractor] Self-correction → Update belief",
            expected_trajectory=(
                "System accommodates corrected parties, "
                "if prior commitment existed: revises it, "
                "pops question, "
                "continues with next question"
            ),
        ),
        ChoiceOption(
            id=6,
            category=MoveCategory.NESTED_QUESTION,
            utterance="Can the NDA have three parties instead of two?",
            description="[Distractor] Question about constraints → QUD push",
            expected_trajectory=(
                "System pushes constraint question to QUD, "
                "answers: 'Yes, multi-party NDAs are supported', "
                "pops question, "
                "returns to parties question"
            ),
        ),
    ]


def get_volunteer_info_turn4_distractors() -> list[ChoiceOption]:
    """Distractors for Volunteer Information Turn 4 (Duration + type + law).

    Expected: "3 years, mutual NDA, California law"
    Context: System asked "What is the duration of confidentiality obligations?"
            User volunteers duration, type, AND governing law
    """
    return [
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="3 years, mutual NDA, California law",
            description="[Expected] Volunteer all remaining → Plan complete",
            expected_trajectory=(
                "System accommodates all three commitments, "
                "clears all private.issues, "
                "plan complete, "
                "generates NDA document"
            ),
        ),
        ChoiceOption(
            id=2,
            category=MoveCategory.EXPECTED,
            utterance="3 years",
            description="[Distractor] Answer only duration → Continue questioning",
            expected_trajectory=(
                "System accommodates duration, "
                "pops question, "
                "raises next question (NDA type) to QUD"
            ),
        ),
        ChoiceOption(
            id=3,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="3 years, one-way NDA protecting Acme Corp",
            description="[Distractor] Duration + type + specifics → Partial volunteer",
            expected_trajectory=(
                "System accommodates duration and type, "
                "notes protecting party detail, "
                "raises governing law question"
            ),
        ),
        ChoiceOption(
            id=4,
            category=MoveCategory.INVALID_ANSWER,
            utterance="Perpetual",
            description="[Distractor] Just duration (unusual) → May ask confirmation",
            expected_trajectory=(
                "System accommodates perpetual duration, "
                "may ask confirmation: 'Perpetual NDAs are uncommon. Is this correct?', "
                "then continues with next question"
            ),
        ),
        ChoiceOption(
            id=5,
            category=MoveCategory.CLARIFICATION_REQUEST,
            utterance="What's the difference between mutual and one-way NDAs?",
            description="[Distractor] Question instead of answer → QUD push",
            expected_trajectory=(
                "System pushes definition question to QUD, "
                "explains difference, "
                "pops question, "
                "returns to duration question"
            ),
        ),
        ChoiceOption(
            id=6,
            category=MoveCategory.CORRECTION,
            utterance="Wait, make it 5 years instead of 3",
            description="[Distractor] Correction without initial answer → Assumes 3",
            expected_trajectory=(
                "System infers correction relates to unstated 3-year duration, "
                "accommodates 5 years, "
                "pops question, "
                "continues"
            ),
        ),
        ChoiceOption(
            id=7,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="5 years, mutual, governed by Delaware law",
            description="[Distractor] Different values volunteered → Completes plan",
            expected_trajectory=(
                "System accommodates all commitments, "
                "plan complete, "
                "generates NDA with volunteered parameters"
            ),
        ),
    ]


# IBiS-3 Clarification Scenario Distractors


def get_clarification_turn0_distractors() -> list[ChoiceOption]:
    """Distractors for Clarification Turn 0 (NDA request).

    Expected: "I need to draft an NDA"
    Context: User initiates NDA drafting, scenario will test clarification on Turn 2
    """
    return [
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="I need to draft an NDA",
            description="[Expected] Clear task initiation",
            expected_trajectory=(
                "System forms NDA drafting plan, "
                "accommodates questions to private.issues, "
                "raises 'parties' question to QUD"
            ),
        ),
        ChoiceOption(
            id=2,
            category=MoveCategory.CLARIFICATION_REQUEST,
            utterance="I need help with an agreement",
            description="[Distractor] Vague request → System asks for clarification",
            expected_trajectory=(
                "System detects vague request, "
                "asks clarification: 'What type of agreement?', "
                "user must specify NDA"
            ),
        ),
        ChoiceOption(
            id=3,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="I need to draft an NDA for Acme Corp and Smith Inc",
            description="[Distractor] Volunteer parties → Skip first question",
            expected_trajectory=(
                "System forms plan with parties pre-filled, "
                "removes parties from private.issues, "
                "raises next question (NDA type) to QUD"
            ),
        ),
        ChoiceOption(
            id=4,
            category=MoveCategory.NESTED_QUESTION,
            utterance="What is an NDA and when do I need one?",
            description="[Distractor] Information request → QUD push before task",
            expected_trajectory=(
                "System pushes explanation question to QUD, "
                "provides NDA explanation, "
                "pops question, "
                "asks if user wants to proceed with drafting"
            ),
        ),
        ChoiceOption(
            id=5,
            category=MoveCategory.EXPECTED,
            utterance="Draft a confidentiality agreement",
            description="[Distractor] Alternative terminology → Same as NDA",
            expected_trajectory=(
                "System recognizes 'confidentiality agreement' as NDA synonym, "
                "forms NDA plan, "
                "proceeds with parties question"
            ),
        ),
    ]


def get_clarification_turn2_distractors() -> list[ChoiceOption]:
    """Distractors for Clarification Turn 2 (Invalid parties answer).

    Expected: "blue"
    Context: System asked "What are the parties to the NDA?"
            This turn demonstrates Rule 4.3 (IssueClarification)
    """
    return [
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="blue",
            description="[Expected] Invalid answer → Triggers clarification (Rule 4.3)",
            expected_trajectory=(
                "System validates: domain.resolves('blue', Q_parties) → False, "
                "creates clarification question: 'What is a valid parties?', "
                "pushes CQ to QUD above Q_parties, "
                "QUD now: [Q_parties, CQ_valid_parties]"
            ),
        ),
        ChoiceOption(
            id=2,
            category=MoveCategory.EXPECTED,
            utterance="Acme Corp and Smith Inc",
            description="[Distractor] Valid answer → Normal flow, no clarification",
            expected_trajectory=(
                "System validates: domain.resolves() → True, "
                "accommodates parties commitment, "
                "pops Q_parties from QUD, "
                "raises next question to QUD"
            ),
        ),
        ChoiceOption(
            id=3,
            category=MoveCategory.INVALID_ANSWER,
            utterance="42",
            description="[Distractor] Numeric nonsense → Clarification needed",
            expected_trajectory=(
                "System validates: number is not valid parties, "
                "creates clarification: 'Please provide party names (legal entities)', "
                "pushes CQ to QUD"
            ),
        ),
        ChoiceOption(
            id=4,
            category=MoveCategory.INVALID_ANSWER,
            utterance="Just one company",
            description="[Distractor] Incomplete/vague → Clarification for specifics",
            expected_trajectory=(
                "System detects vague/incomplete answer, "
                "creates clarification: 'What is the name of the company? And the second party?', "
                "pushes CQ to QUD"
            ),
        ),
        ChoiceOption(
            id=5,
            category=MoveCategory.INVALID_ANSWER,
            utterance="Me and my friend",
            description="[Distractor] Informal reference → Clarification for legal names",
            expected_trajectory=(
                "System detects informal references, "
                "creates clarification: 'Please provide full legal names of both parties', "
                "pushes CQ to QUD"
            ),
        ),
        ChoiceOption(
            id=6,
            category=MoveCategory.NESTED_QUESTION,
            utterance="Can an NDA have more than two parties?",
            description="[Distractor] Question instead of answer → QUD push",
            expected_trajectory=(
                "System pushes user's question to QUD: [Q_parties, Q_multi_party], "
                "answers: 'Yes, multi-party NDAs are supported', "
                "pops Q_multi_party, "
                "returns to Q_parties: 'What are the parties?'"
            ),
        ),
        ChoiceOption(
            id=7,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="Acme Corp and Smith Inc, effective January 1, 2025",
            description="[Distractor] Valid answer + volunteer date → Skip date question",
            expected_trajectory=(
                "System validates and accommodates both commitments, "
                "pops Q_parties, "
                "removes Q_effective_date from private.issues, "
                "raises next question"
            ),
        ),
        ChoiceOption(
            id=8,
            category=MoveCategory.REJECTION,
            utterance="Actually, I don't want to do this anymore",
            description="[Distractor] Task abandonment → Clear plan",
            expected_trajectory=(
                "System detects task cancellation, "
                "clears private.plan, private.issues, shared.qud, "
                "returns to idle: 'Okay. How can I help you?'"
            ),
        ),
    ]


def get_clarification_turn4_distractors() -> list[ChoiceOption]:
    """Distractors for Clarification Turn 4 (Response to clarification).

    Expected: "Acme Corp and Smith Inc"
    Context: System asked "What is a valid parties?" (clarification question)
            QUD: [Q_parties, CQ_valid_parties]
            User previously said "blue" (invalid)
    """
    return [
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="Acme Corp and Smith Inc",
            description="[Expected] Valid clarification response → Resolve both questions",
            expected_trajectory=(
                "System validates answer as valid parties, "
                "pops CQ_valid_parties from QUD, "
                "uses answer to resolve original Q_parties, "
                "pops Q_parties from QUD, "
                "accommodates commitment: parties(Acme Corp, Smith Inc), "
                "raises next question to QUD"
            ),
        ),
        ChoiceOption(
            id=2,
            category=MoveCategory.INVALID_ANSWER,
            utterance="red",
            description="[Distractor] Still invalid → Additional clarification layer",
            expected_trajectory=(
                "System validates: still not valid parties, "
                "may create nested clarification or provide examples: "
                "'Please provide company names like Acme Corp and Smith Inc', "
                "keeps CQ in QUD"
            ),
        ),
        ChoiceOption(
            id=3,
            category=MoveCategory.INVALID_ANSWER,
            utterance="I don't know",
            description="[Distractor] Explicit confusion → System provides help",
            expected_trajectory=(
                "System detects user confusion, "
                "provides guidance/examples: "
                "'Parties are the legal entities entering the NDA, like companies or individuals', "
                "may offer to help formulate answer"
            ),
        ),
        ChoiceOption(
            id=4,
            category=MoveCategory.NESTED_QUESTION,
            utterance="What do you mean by valid parties?",
            description="[Distractor] Meta-question about clarification → Further QUD nesting",
            expected_trajectory=(
                "System pushes meta-question to QUD: "
                "[Q_parties, CQ_valid_parties, Q_what_is_valid], "
                "explains validation criteria: 'Valid parties are legal entity names', "
                "pops Q_what_is_valid, "
                "returns to CQ_valid_parties"
            ),
        ),
        ChoiceOption(
            id=5,
            category=MoveCategory.EXPECTED,
            utterance="TechCorp and InnovateLLC",
            description="[Distractor] Different valid parties → Resolves clarification",
            expected_trajectory=(
                "System validates as valid parties, "
                "resolves clarification and original question, "
                "accommodates: parties(TechCorp, InnovateLLC), "
                "continues with next question"
            ),
        ),
        ChoiceOption(
            id=6,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="Acme Corp and Smith Inc, mutual NDA, effective now",
            description="[Distractor] Valid + volunteer extras → Resolve + skip questions",
            expected_trajectory=(
                "System resolves clarification with valid parties, "
                "accommodates additional volunteered info (type, date), "
                "removes corresponding questions from private.issues, "
                "continues with remaining questions"
            ),
        ),
        ChoiceOption(
            id=7,
            category=MoveCategory.CORRECTION,
            utterance="Sorry, I meant to say Acme Corp and Smith Inc earlier",
            description="[Distractor] Explicit correction acknowledgment → Valid resolution",
            expected_trajectory=(
                "System recognizes correction acknowledgment, "
                "validates new answer, "
                "resolves both clarification and original question, "
                "accommodates valid parties"
            ),
        ),
        ChoiceOption(
            id=8,
            category=MoveCategory.REJECTION,
            utterance="Never mind, I'll draft it myself",
            description="[Distractor] Task abandonment during clarification → Clear all",
            expected_trajectory=(
                "System detects abandonment, "
                "clears QUD (all questions including clarification), "
                "clears plan and issues, "
                "returns to idle"
            ),
        ),
    ]


# IBiS-3 Dependent Questions Scenario Distractors


def get_dependent_questions_turn0_distractors() -> list[ChoiceOption]:
    """Distractors for Dependent Questions Turn 0 (Flight booking request).

    Expected: "I need to book a flight"
    Context: User initiates flight booking with dependent questions (price depends on route)
    """
    return [
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="I need to book a flight",
            description="[Expected] Clear flight booking request",
            expected_trajectory=(
                "System forms flight booking plan with dependent questions, "
                "accommodates to private.issues: [departure, destination, dates, price, ...], "
                "dependencies: price depends on [departure, destination], "
                "raises first prerequisite question (departure) to QUD"
            ),
        ),
        ChoiceOption(
            id=2,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="I need to book a flight from London to New York",
            description="[Distractor] Volunteer departure and destination → Skip prerequisites",
            expected_trajectory=(
                "System forms plan, "
                "accommodates departure(London) and destination(New York) to commitments, "
                "removes both from private.issues, "
                "dependent question 'price' now has prerequisites satisfied, "
                "can raise price or other questions to QUD"
            ),
        ),
        ChoiceOption(
            id=3,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="Book a flight from London to New York on January 15, 2025",
            description="[Distractor] Volunteer route and date → Skip multiple prerequisites",
            expected_trajectory=(
                "System extracts departure, destination, date, "
                "accommodates all to commitments, "
                "dependent questions can now be asked (prerequisites met), "
                "raises next question (return date, class, etc.)"
            ),
        ),
        ChoiceOption(
            id=4,
            category=MoveCategory.INVALID_ANSWER,
            utterance="Book a flight",
            description="[Distractor] Missing parameters → Asks prerequisites in order",
            expected_trajectory=(
                "System forms flight plan, "
                "all parameters missing, "
                "follows dependency order: asks prerequisite questions first, "
                "then dependent questions"
            ),
        ),
        ChoiceOption(
            id=5,
            category=MoveCategory.NESTED_QUESTION,
            utterance="What information do you need to book a flight?",
            description="[Distractor] Meta-question about requirements → QUD push",
            expected_trajectory=(
                "System pushes meta-question to QUD, "
                "explains flight booking requirements and dependencies: "
                "'I need departure, destination, dates, then I can find prices', "
                "pops question, "
                "asks if user wants to proceed"
            ),
        ),
        ChoiceOption(
            id=6,
            category=MoveCategory.CLARIFICATION_REQUEST,
            utterance="Help me find a flight",
            description="[Distractor] Help request → System provides guidance then proceeds",
            expected_trajectory=(
                "System provides guidance about flight booking, "
                "then initiates plan with first question"
            ),
        ),
    ]


def get_dependent_questions_turn2_distractors() -> list[ChoiceOption]:
    """Distractors for Dependent Questions Turn 2 (Departure city answer).

    Expected: "London"
    Context: System asked "What's your departure city?"
            This is a prerequisite for price question
    """
    return [
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="London",
            description="[Expected] Answer prerequisite question",
            expected_trajectory=(
                "System accommodates departure(London) to commitments, "
                "pops departure question from QUD, "
                "prerequisite satisfied but price still needs destination, "
                "raises next prerequisite question (destination) to QUD"
            ),
        ),
        ChoiceOption(
            id=2,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="London to New York",
            description="[Distractor] Volunteer destination too → Satisfy multiple prerequisites",
            expected_trajectory=(
                "System extracts both departure(London) and destination(New York), "
                "accommodates both to commitments, "
                "both prerequisites for price now satisfied, "
                "can raise price or other questions to QUD"
            ),
        ),
        ChoiceOption(
            id=3,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="London, flying out January 15, 2025",
            description="[Distractor] Volunteer departure date → Partial skip",
            expected_trajectory=(
                "System accommodates departure(London) and date(Jan 15), "
                "pops departure question, "
                "skips date question from issues, "
                "raises destination question (still prerequisite for price)"
            ),
        ),
        ChoiceOption(
            id=4,
            category=MoveCategory.INVALID_ANSWER,
            utterance="I'm not sure, somewhere in Europe",
            description="[Distractor] Vague answer → Clarification needed",
            expected_trajectory=(
                "System detects vague/incomplete answer, "
                "creates clarification: 'Which specific city in Europe?', "
                "pushes CQ to QUD"
            ),
        ),
        ChoiceOption(
            id=5,
            category=MoveCategory.NESTED_QUESTION,
            utterance="Which cities do you fly from?",
            description="[Distractor] Information request → QUD push",
            expected_trajectory=(
                "System pushes question to QUD, "
                "provides list of available departure cities, "
                "pops question, "
                "returns to departure question"
            ),
        ),
        ChoiceOption(
            id=6,
            category=MoveCategory.INVALID_ANSWER,
            utterance="The airport near me",
            description="[Distractor] Ambiguous reference → Clarification required",
            expected_trajectory=(
                "System cannot resolve 'airport near me', "
                "asks clarification: 'Which airport is that?', "
                "pushes CQ to QUD"
            ),
        ),
        ChoiceOption(
            id=7,
            category=MoveCategory.EXPECTED,
            utterance="Heathrow",
            description="[Distractor] Specific airport → Valid answer",
            expected_trajectory=(
                "System resolves Heathrow to London, "
                "accommodates departure(London/Heathrow), "
                "continues with destination question"
            ),
        ),
    ]


def get_dependent_questions_turn4_distractors() -> list[ChoiceOption]:
    """Distractors for Dependent Questions Turn 4 (Destination city answer).

    Expected: "New York"
    Context: System asked "What's your destination city?"
            Departure already answered (London)
            This is the FINAL prerequisite for price question
    """
    return [
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="New York",
            description="[Expected] Answer final prerequisite → Price question unlocked",
            expected_trajectory=(
                "System accommodates destination(New York) to commitments, "
                "pops destination question from QUD, "
                "ALL prerequisites for price now satisfied, "
                "price question moves from blocked to available, "
                "raises price question to QUD (demonstrates Rule 4.4)"
            ),
        ),
        ChoiceOption(
            id=2,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="New York, departing January 15, returning January 20",
            description="[Distractor] Volunteer dates → Skip date questions, unlock price",
            expected_trajectory=(
                "System accommodates destination, departure date, return date, "
                "all prerequisites for price satisfied, "
                "removes date questions from issues, "
                "raises price question to QUD"
            ),
        ),
        ChoiceOption(
            id=3,
            category=MoveCategory.CORRECTION,
            utterance="Actually, change departure to Paris instead of London",
            description="[Distractor] Correct previous answer → Updates prerequisite",
            expected_trajectory=(
                "System detects correction of departure commitment, "
                "retracts old: departure(London), "
                "accommodates new: departure(Paris), "
                "prerequisite still satisfied (just different value), "
                "continues with destination question"
            ),
        ),
        ChoiceOption(
            id=4,
            category=MoveCategory.INVALID_ANSWER,
            utterance="Somewhere in the United States",
            description="[Distractor] Vague answer → Clarification before unlocking price",
            expected_trajectory=(
                "System detects vague destination, "
                "creates clarification: 'Which specific city in the US?', "
                "price question remains blocked until specific destination provided"
            ),
        ),
        ChoiceOption(
            id=5,
            category=MoveCategory.NESTED_QUESTION,
            utterance="What destinations are available from London?",
            description="[Distractor] Route options request → QUD push",
            expected_trajectory=(
                "System pushes route query to QUD, "
                "provides list of destinations from London, "
                "pops question, "
                "returns to destination question"
            ),
        ),
        ChoiceOption(
            id=6,
            category=MoveCategory.EXPECTED,
            utterance="JFK Airport, New York",
            description="[Distractor] Specific airport → Resolves to city, unlocks price",
            expected_trajectory=(
                "System resolves JFK to New York, "
                "accommodates destination(New York/JFK), "
                "prerequisites satisfied, "
                "raises price question"
            ),
        ),
        ChoiceOption(
            id=7,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="New York, economy class, under $500",
            description="[Distractor] Volunteer class and price constraint → Skip to search",
            expected_trajectory=(
                "System accommodates destination, class, price constraint, "
                "all prerequisites for search satisfied, "
                "may skip price question (constraint provided), "
                "proceeds to search with constraints"
            ),
        ),
        ChoiceOption(
            id=8,
            category=MoveCategory.NESTED_QUESTION,
            utterance="How much will it cost to fly there?",
            description="[Distractor] Ask dependent question prematurely → Explain dependency",
            expected_trajectory=(
                "System recognizes premature dependent question, "
                "explains: 'I need to know the destination first to check prices', "
                "returns to destination question"
            ),
        ),
    ]


# IBiS-3 Belief Revision Scenario Distractors


def get_belief_revision_turn0_distractors() -> list[ChoiceOption]:
    """Distractors for Belief Revision Turn 0 (Flight booking request).

    Expected: "I need to book a flight from London to Paris"
    Context: User initiates flight booking (will later revise to train)
    """
    return [
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="I need to book a flight from London to Paris",
            description="[Expected] Flight booking request",
            expected_trajectory=(
                "System forms flight booking plan, "
                "accommodates flight questions to private.issues, "
                "raises departure_date question to QUD"
            ),
        ),
        ChoiceOption(
            id=2,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="I need to book a flight from London to Paris on April 4th",
            description="[Distractor] Volunteer departure date → Skip date question",
            expected_trajectory=(
                "System forms flight plan with date pre-filled, "
                "removes date from issues, "
                "raises next question (cabin class) to QUD"
            ),
        ),
        ChoiceOption(
            id=3,
            category=MoveCategory.EXPECTED,
            utterance="I need to book a train from London to Paris",
            description="[Distractor] Request train directly → No revision needed",
            expected_trajectory=(
                "System forms train booking plan, "
                "accommodates train questions to issues, "
                "raises departure_date to QUD"
            ),
        ),
        ChoiceOption(
            id=4,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="I need to travel from London to Paris on April 4th",
            description="[Distractor] Ambiguous mode (flight/train) → System may ask",
            expected_trajectory=(
                "System detects ambiguity (flight or train?), "
                "may ask clarification: 'Would you like to fly or take the train?', "
                "then forms appropriate plan"
            ),
        ),
        ChoiceOption(
            id=5,
            category=MoveCategory.NESTED_QUESTION,
            utterance="What's the fastest way to get from London to Paris?",
            description="[Distractor] Information request → QUD push before task",
            expected_trajectory=(
                "System pushes comparison question to QUD, "
                "provides answer: 'Flight is 1h15m, Eurostar train is 2h15m', "
                "pops question, asks if user wants to proceed with booking"
            ),
        ),
    ]


def get_belief_revision_turn2_distractors() -> list[ChoiceOption]:
    """Distractors for Belief Revision Turn 2 (Date answer).

    Expected: "April 4th"
    Context: System asked "What's your departure date?" for flight
    """
    return [
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="April 4th",
            description="[Expected] Valid date answer",
            expected_trajectory=(
                "System accommodates date commitment, "
                "pops date question from QUD, "
                "raises cabin_class question"
            ),
        ),
        ChoiceOption(
            id=2,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="April 4th, economy class",
            description="[Distractor] Volunteer class → Skip class question",
            expected_trajectory=(
                "System accommodates date and class, "
                "removes class from issues, "
                "plan may be complete, proceeds to booking"
            ),
        ),
        ChoiceOption(
            id=3,
            category=MoveCategory.INVALID_ANSWER,
            utterance="Next week",
            description="[Distractor] Vague date → Clarification needed",
            expected_trajectory=(
                "System detects vague temporal reference, asks clarification: 'What specific date?'"
            ),
        ),
        ChoiceOption(
            id=4,
            category=MoveCategory.NESTED_QUESTION,
            utterance="What dates have the cheapest flights?",
            description="[Distractor] Price-based question → QUD push, search",
            expected_trajectory=(
                "System pushes price query to QUD, "
                "performs flight price search, "
                "provides flexible date pricing, "
                "returns to date question"
            ),
        ),
        ChoiceOption(
            id=5,
            category=MoveCategory.CORRECTION,
            utterance="Actually, I want to take a train instead of flying",
            description="[Distractor] EARLY revision → Plan change before class question",
            expected_trajectory=(
                "System detects plan change (flight → train), "
                "retracts flight plan, forms train plan, "
                "date commitment may be compatible, retained, "
                "raises train-specific questions"
            ),
        ),
    ]


def get_belief_revision_turn4_distractors() -> list[ChoiceOption]:
    """Distractors for Belief Revision Turn 4 (THE MAJOR REVISION).

    Expected: "Actually, I changed my mind - I want to take a train instead"
    Context: System asked "What cabin class do you prefer?"
            Date already committed (April 4th)
            THIS IS THE KEY DEMONSTRATION OF BELIEF REVISION
    """
    return [
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="Actually, I changed my mind - I want to take a train instead",
            description="[Expected] MAJOR PLAN CHANGE → Demonstrates Rules 4.6-4.8",
            expected_trajectory=(
                "System detects plan revision (flight → train), "
                "Rule 4.7: Retracts cabin_class question (flight-specific), "
                "Rule 4.6: Retains date commitment (compatible), "
                "Forms new train booking plan, "
                "Rule 4.8: Accommodates train questions, "
                "Raises departure_time question"
            ),
        ),
        ChoiceOption(
            id=2,
            category=MoveCategory.EXPECTED,
            utterance="Economy class",
            description="[Distractor] Answer question normally → No revision",
            expected_trajectory=(
                "System accommodates cabin_class(economy), "
                "plan complete, "
                "proceeds with flight booking"
            ),
        ),
        ChoiceOption(
            id=3,
            category=MoveCategory.EXPECTED,
            utterance="Business class",
            description="[Distractor] Different class choice → No revision",
            expected_trajectory=(
                "System accommodates cabin_class(business), "
                "plan complete, "
                "proceeds with flight booking"
            ),
        ),
        ChoiceOption(
            id=4,
            category=MoveCategory.CORRECTION,
            utterance="Wait, change the date to April 5th instead",
            description="[Distractor] Correct previous answer → Minor revision",
            expected_trajectory=(
                "System detects date correction, "
                "retracts old: date(April 4th), "
                "accommodates new: date(April 5th), "
                "returns to cabin_class question"
            ),
        ),
        ChoiceOption(
            id=5,
            category=MoveCategory.NESTED_QUESTION,
            utterance="What's the price difference between economy and business?",
            description="[Distractor] Price comparison → QUD push, return to class",
            expected_trajectory=(
                "System pushes price query to QUD, "
                "provides class price comparison, "
                "pops question, "
                "returns to cabin_class question"
            ),
        ),
        ChoiceOption(
            id=6,
            category=MoveCategory.REJECTION,
            utterance="Actually, I don't want to travel anymore",
            description="[Distractor] Cancel entire task → Clear all",
            expected_trajectory=(
                "System detects task cancellation, "
                "clears plan, issues, QUD, commitments, "
                "returns to idle"
            ),
        ),
        ChoiceOption(
            id=7,
            category=MoveCategory.CORRECTION,
            utterance="Never mind the flight, book me a hotel in Paris instead",
            description="[Distractor] Complete task switch → Different domain",
            expected_trajectory=(
                "System detects new task (hotel booking), "
                "clears flight plan, "
                "forms hotel booking plan, "
                "raises hotel questions"
            ),
        ),
        ChoiceOption(
            id=8,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="Economy class, and I'll also need a hotel",
            description="[Distractor] Answer + new task → Sequential tasks",
            expected_trajectory=(
                "System accommodates cabin_class, "
                "completes flight plan, "
                "notes hotel task for after flight booking"
            ),
        ),
    ]


def get_belief_revision_turn6_distractors() -> list[ChoiceOption]:
    """Distractors for Belief Revision Turn 6 (Time answer after revision).

    Expected: "Morning, around 9 AM"
    Context: System asked "What time would you like to depart?" for TRAIN
            Plan changed from flight to train
            Date (April 4th) was retained
    """
    return [
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="Morning, around 9 AM",
            description="[Expected] Answer train time question",
            expected_trajectory=(
                "System accommodates time(9 AM), pops time question, raises train_class question"
            ),
        ),
        ChoiceOption(
            id=2,
            category=MoveCategory.EXPECTED,
            utterance="Evening, around 6 PM",
            description="[Distractor] Different time → Alternative valid answer",
            expected_trajectory=(
                "System accommodates time(6 PM), continues with train_class question"
            ),
        ),
        ChoiceOption(
            id=3,
            category=MoveCategory.INVALID_ANSWER,
            utterance="As soon as possible",
            description="[Distractor] Vague time → Clarification",
            expected_trajectory=(
                "System detects vague time, asks clarification: 'What specific time?'"
            ),
        ),
        ChoiceOption(
            id=4,
            category=MoveCategory.NESTED_QUESTION,
            utterance="What train times are available?",
            description="[Distractor] Schedule query → QUD push, show options",
            expected_trajectory=(
                "System pushes schedule query to QUD, "
                "provides Eurostar schedule for April 4th, "
                "pops question, returns to time question"
            ),
        ),
        ChoiceOption(
            id=5,
            category=MoveCategory.CORRECTION,
            utterance="Actually, I want to fly after all, not take the train",
            description="[Distractor] REVERSE revision → Change back to flight",
            expected_trajectory=(
                "System detects plan change (train → flight), "
                "retracts train-specific questions/commitments, "
                "re-forms flight plan, "
                "retains compatible commitments (date), "
                "raises cabin_class question"
            ),
        ),
        ChoiceOption(
            id=6,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="9 AM, standard class",
            description="[Distractor] Volunteer class → Skip class question",
            expected_trajectory=(
                "System accommodates time and class, plan complete, proceeds to train booking"
            ),
        ),
    ]


def get_belief_revision_turn8_distractors() -> list[ChoiceOption]:
    """Distractors for Belief Revision Turn 8 (Class answer).

    Expected: "Standard class is fine"
    Context: System asked "Would you like standard or first class?"
            Train booking plan active
            Date and time already committed
    """
    return [
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="Standard class is fine",
            description="[Expected] Choose standard class → Complete train plan",
            expected_trajectory=(
                "System accommodates class(standard), "
                "plan complete, "
                "proceeds to train booking execution"
            ),
        ),
        ChoiceOption(
            id=2,
            category=MoveCategory.EXPECTED,
            utterance="First class please",
            description="[Distractor] Choose first class → Alternative completion",
            expected_trajectory=(
                "System accommodates class(first), "
                "plan complete, "
                "proceeds with first class train booking"
            ),
        ),
        ChoiceOption(
            id=3,
            category=MoveCategory.NESTED_QUESTION,
            utterance="What's included in first class?",
            description="[Distractor] Amenities query → QUD push",
            expected_trajectory=(
                "System pushes amenities question to QUD, "
                "explains first class benefits (meal, lounge, WiFi), "
                "pops question, returns to class selection"
            ),
        ),
        ChoiceOption(
            id=4,
            category=MoveCategory.NESTED_QUESTION,
            utterance="What's the price difference?",
            description="[Distractor] Price query → QUD push",
            expected_trajectory=(
                "System pushes price query to QUD, "
                "provides class price comparison, "
                "pops question, returns to class selection"
            ),
        ),
        ChoiceOption(
            id=5,
            category=MoveCategory.CORRECTION,
            utterance="Actually, change the time to 11 AM instead of 9 AM",
            description="[Distractor] Correct previous answer → Minor revision",
            expected_trajectory=(
                "System retracts time(9 AM), accommodates time(11 AM), returns to class question"
            ),
        ),
        ChoiceOption(
            id=6,
            category=MoveCategory.REJECTION,
            utterance="Never mind, I'll just drive instead",
            description="[Distractor] Cancel booking → Task abandonment",
            expected_trajectory=("System detects cancellation, clears train plan, returns to idle"),
        ),
    ]


# IBiS-4 Complex Contract Negotiation Distractors


def get_contract_negotiation_turn0_distractors() -> list[ChoiceOption]:
    """Distractors for Contract Negotiation Turn 0 (Ambiguous request).

    Expected: "Draft service contract"
    Context: Low confidence (0.4) - triggers pessimistic grounding
    """
    return [
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="Draft service contract",
            description="[Expected] Ambiguous request → Pessimistic grounding (icm:per*neg)",
            expected_trajectory=(
                "System detects low confidence (0.4), "
                "uses pessimistic grounding strategy, "
                "asks clarification: 'Could you be more specific?'"
            ),
        ),
        ChoiceOption(
            id=2,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="Draft a software development services contract",
            description="[Distractor] Clear request → Optimistic grounding, immediate acceptance",
            expected_trajectory=(
                "System detects clear request (high confidence), "
                "uses optimistic grounding, "
                "forms contract plan, "
                "raises first question"
            ),
        ),
        ChoiceOption(
            id=3,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="Create a software development contract for TechCorp and DevStudio",
            description="[Distractor] Volunteer parties → Skip parties question",
            expected_trajectory=(
                "System forms contract plan with parties pre-filled, "
                "skips parties question, "
                "raises duration question"
            ),
        ),
        ChoiceOption(
            id=4,
            category=MoveCategory.NESTED_QUESTION,
            utterance="What types of contracts can you draft?",
            description="[Distractor] Meta-question → QUD push",
            expected_trajectory=(
                "System pushes question to QUD, "
                "explains available contract types, "
                "pops question, asks if user wants to proceed"
            ),
        ),
    ]


def get_contract_negotiation_turn8_distractors() -> list[ChoiceOption]:
    """Distractors for Contract Negotiation Turn 8 (Informal rate).

    Expected: "$15k monthly"
    Context: Medium confidence (0.65) - informal format triggers cautious grounding
    """
    return [
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="$15k monthly",
            description="[Expected] Informal format → Cautious grounding (icm:und*int)",
            expected_trajectory=(
                "System detects medium confidence (0.65), informal format, "
                "uses cautious grounding, "
                "asks confirmation: 'Did you mean $15,000 per month?'"
            ),
        ),
        ChoiceOption(
            id=2,
            category=MoveCategory.EXPECTED,
            utterance="$15,000 per month",
            description="[Distractor] Formal format → Optimistic grounding, accept immediately",
            expected_trajectory=(
                "System detects formal, clear format (high confidence), "
                "uses optimistic grounding, "
                "accepts immediately, continues to payment terms"
            ),
        ),
        ChoiceOption(
            id=3,
            category=MoveCategory.INVALID_ANSWER,
            utterance="A reasonable amount",
            description="[Distractor] Vague amount → Clarification required",
            expected_trajectory=(
                "System detects vague answer, asks clarification: 'What specific monthly rate?'"
            ),
        ),
        ChoiceOption(
            id=4,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="$15,000 per month, Net 60 payment terms",
            description="[Distractor] Volunteer payment terms → Skip negotiation",
            expected_trajectory=(
                "System accommodates rate and payment terms, "
                "skips IUN negotiation (user already decided), "
                "continues to notice period question"
            ),
        ),
        ChoiceOption(
            id=5,
            category=MoveCategory.NESTED_QUESTION,
            utterance="What's the market rate for this type of work?",
            description="[Distractor] Market research query → QUD push",
            expected_trajectory=(
                "System pushes market rate question to QUD, "
                "provides market rate information, "
                "pops question, returns to rate question"
            ),
        ),
    ]


def get_contract_negotiation_turn12_distractors() -> list[ChoiceOption]:
    """Distractors for Contract Negotiation Turn 12 (IUN negotiation).

    Expected: "Net 30 is too tight, we need Net 60"
    Context: IUN with two options (Net 30, Net 60)
    """
    return [
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="Net 30 is too tight, we need Net 60",
            description="[Expected] Reject first, accept second → IUN resolution",
            expected_trajectory=(
                "System removes Net 30 from IUN, "
                "accepts Net 60, "
                "clears IUN, "
                "continues to notice period question"
            ),
        ),
        ChoiceOption(
            id=2,
            category=MoveCategory.EXPECTED,
            utterance="Net 30 works for us",
            description="[Distractor] Accept first option → Different resolution",
            expected_trajectory=(
                "System accepts Net 30, clears IUN, continues to notice period question"
            ),
        ),
        ChoiceOption(
            id=3,
            category=MoveCategory.REJECTION,
            utterance="Neither works. Can we do Net 45?",
            description="[Distractor] Counter-proposal → New option negotiation",
            expected_trajectory=(
                "System considers counter-proposal Net 45, "
                "may accept as compromise, "
                "or explain available options"
            ),
        ),
        ChoiceOption(
            id=4,
            category=MoveCategory.NESTED_QUESTION,
            utterance="What's the difference between Net 30 and Net 60?",
            description="[Distractor] Explanation request → QUD push",
            expected_trajectory=(
                "System pushes explanation to QUD, "
                "explains payment term difference (30 vs 60 days), "
                "pops question, returns to negotiation"
            ),
        ),
        ChoiceOption(
            id=5,
            category=MoveCategory.NESTED_QUESTION,
            utterance="Are there any other payment options available?",
            description="[Distractor] Request more alternatives → Expand IUN",
            expected_trajectory=(
                "System may add more payment options to IUN, "
                "presents expanded alternatives for negotiation"
            ),
        ),
    ]


def get_contract_negotiation_turn16_distractors() -> list[ChoiceOption]:
    """Distractors for Contract Negotiation Turn 16 (Action confirmation).

    Expected: "Yes, generate it"
    Context: System asks "Should I generate the contract?"
    """
    return [
        ChoiceOption(
            id=1,
            category=MoveCategory.EXPECTED,
            utterance="Yes, generate it",
            description="[Expected] Confirm action → Contract generation executes",
            expected_trajectory=(
                "System pops confirmation from QUD, "
                "executes contract generation action, "
                "produces contract document"
            ),
        ),
        ChoiceOption(
            id=2,
            category=MoveCategory.REJECTION,
            utterance="No, wait",
            description="[Distractor] Reject action → Action cancelled",
            expected_trajectory=(
                "System removes action from queue, asks: 'Would you like to make changes?'"
            ),
        ),
        ChoiceOption(
            id=3,
            category=MoveCategory.CORRECTION,
            utterance="Wait, change the duration to 24 months",
            description="[Distractor] Correction before generation → Update parameters",
            expected_trajectory=(
                "System retracts duration(12 months), "
                "accommodates duration(24 months), "
                "re-asks confirmation with updated terms"
            ),
        ),
        ChoiceOption(
            id=4,
            category=MoveCategory.NESTED_QUESTION,
            utterance="Can you review all the terms first?",
            description="[Distractor] Request summary → QUD push",
            expected_trajectory=(
                "System pushes review request to QUD, "
                "summarizes all contract terms, "
                "pops question, returns to confirmation"
            ),
        ),
        ChoiceOption(
            id=5,
            category=MoveCategory.VOLUNTEER_INFO,
            utterance="Yes, and email it to legal@techcorp.com",
            description="[Distractor] Confirmation + additional action → Sequential actions",
            expected_trajectory=(
                "System confirms generation, "
                "adds email action to queue, "
                "executes both actions sequentially"
            ),
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
    "Volunteer Information": {
        0: get_volunteer_info_turn0_distractors,  # Turn 0: NDA request
        2: get_volunteer_info_turn2_distractors,  # Turn 2: Parties + date volunteer
        4: get_volunteer_info_turn4_distractors,  # Turn 4: Duration + type + law volunteer
    },
    "Clarification Questions": {
        0: get_clarification_turn0_distractors,  # Turn 0: NDA request
        2: get_clarification_turn2_distractors,  # Turn 2: Invalid answer ("blue")
        4: get_clarification_turn4_distractors,  # Turn 4: Clarification response
    },
    "Dependent Questions": {
        0: get_dependent_questions_turn0_distractors,  # Turn 0: Flight booking request
        2: get_dependent_questions_turn2_distractors,  # Turn 2: Departure city answer
        4: get_dependent_questions_turn4_distractors,  # Turn 4: Destination city answer
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
    "Belief Revision (Reaccommodation)": {
        0: get_belief_revision_turn0_distractors,  # Turn 0: Flight request
        2: get_belief_revision_turn2_distractors,  # Turn 2: Date answer
        4: get_belief_revision_turn4_distractors,  # Turn 4: MAJOR REVISION (flight → train)
        6: get_belief_revision_turn6_distractors,  # Turn 6: Time answer (after revision)
        8: get_belief_revision_turn8_distractors,  # Turn 8: Class answer
    },
    # IBiS-2 Grounding scenarios reuse Incremental Questioning distractors
    # (same dialogue flow, different confidence/grounding behaviors)
    "Optimistic Grounding": {
        0: get_scenario1_turn1_distractors,  # Turn 0: NDA request (reused)
        2: get_scenario1_turn2_distractors,  # Turn 2: Parties
        4: get_scenario1_turn3_distractors,  # Turn 4: Date
        6: get_scenario1_turn2a_distractors,  # Turn 6: Type
        8: get_scenario1_turn4_distractors,  # Turn 8: Duration
        10: get_scenario1_turn5_distractors,  # Turn 10: Law
    },
    "Cautious Grounding": {
        0: get_scenario1_turn1_distractors,  # Turn 0: NDA request (reused)
        2: get_scenario1_turn2_distractors,  # Turn 2: Parties
        4: get_scenario1_turn3_distractors,  # Turn 4: Date
        6: get_scenario1_turn2a_distractors,  # Turn 6: Type
        8: get_scenario1_turn4_distractors,  # Turn 8: Duration
        10: get_scenario1_turn5_distractors,  # Turn 10: Law
    },
    "Pessimistic Grounding": {
        0: get_scenario1_turn1_distractors,  # Turn 0: NDA request (reused)
        2: get_scenario1_turn2_distractors,  # Turn 2: Parties
        4: get_scenario1_turn3_distractors,  # Turn 4: Date
        6: get_scenario1_turn2a_distractors,  # Turn 6: Type
        8: get_scenario1_turn4_distractors,  # Turn 8: Duration
        10: get_scenario1_turn5_distractors,  # Turn 10: Law
    },
    "Mixed Grounding Strategies": {
        0: get_scenario1_turn1_distractors,  # Turn 0: NDA request (reused)
        2: get_scenario1_turn2_distractors,  # Turn 2: Parties
        4: get_scenario1_turn3_distractors,  # Turn 4: Date
        6: get_scenario1_turn2a_distractors,  # Turn 6: Type
        8: get_scenario1_turn4_distractors,  # Turn 8: Duration
        10: get_scenario1_turn5_distractors,  # Turn 10: Law
    },
    "Complex Contract Negotiation": {
        0: get_contract_negotiation_turn0_distractors,  # Turn 0: Ambiguous request
        8: get_contract_negotiation_turn8_distractors,  # Turn 8: Informal rate
        12: get_contract_negotiation_turn12_distractors,  # Turn 12: IUN negotiation
        16: get_contract_negotiation_turn16_distractors,  # Turn 16: Action confirmation
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
