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


# Mapping from scenario and turn to distractors
SCENARIO_DISTRACTORS = {
    "Incremental Questioning": {
        0: get_scenario1_turn1_distractors,  # Turn 0: Initial request
        2: get_scenario1_turn2_distractors,  # Turn 2: Parties answer
        4: get_scenario1_turn2a_distractors,  # Turn 4: NDA type answer (NEW)
        6: get_scenario1_turn3_distractors,  # Turn 6: Effective date answer (moved)
        8: get_scenario1_turn4_distractors,  # Turn 8: Duration answer (NEW)
        10: get_scenario1_turn5_distractors,  # Turn 10: Governing law answer (NEW)
    }
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
