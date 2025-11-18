"""Demo scenarios showcasing IBiS3 and IBiS2 features.

Pre-scripted dialogue scenarios that demonstrate different IBDM capabilities.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ScenarioStep:
    """A single step in a demo scenario.

    Attributes:
        speaker: Who speaks (user or system)
        utterance: What they say
        description: What this demonstrates
        expected_state: Expected internal state changes
        is_payoff: True if this step represents a high-value final product/output
    """

    speaker: str
    utterance: str
    description: str | None = None
    expected_state: dict[str, str] | None = None
    is_payoff: bool = False


@dataclass
class DemoScenario:
    """A complete demo scenario.

    Attributes:
        name: Scenario name
        description: What this scenario demonstrates
        features: List of IBiS3/IBiS2 features showcased
        steps: Dialogue steps
        confidence_mode: Recommended confidence mode for this scenario
    """

    name: str
    description: str
    features: list[str]
    steps: list[ScenarioStep]
    confidence_mode: str = "heuristic"


# IBiS3 Scenarios


def scenario_incremental_questioning() -> DemoScenario:
    """Scenario demonstrating incremental questioning (Rule 4.2).

    Shows how the system asks one question at a time from a plan,
    rather than overwhelming the user with all questions at once.
    """
    return DemoScenario(
        name="Incremental Questioning",
        description="Demonstrates how IBDM asks questions one at a time (Rule 4.2)",
        features=["Rule 4.1 (IssueAccommodation)", "Rule 4.2 (LocalQuestionAccommodation)"],
        confidence_mode="optimistic",
        steps=[
            ScenarioStep(
                speaker="user",
                utterance="I need to draft an NDA",
                description="User initiates task - system forms plan with 5 questions",
                expected_state={"plan": "active", "private.issues": "5 questions"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What are the parties to the NDA?",
                description="System asks FIRST question (not all 5 at once)",
                expected_state={"qud": "1 question", "private.issues": "4 questions"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Acme Corp and Smith Inc",
                description="User answers first question",
                expected_state={"commitments": "+1", "qud": "0"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="Should this be a mutual or one-way NDA?",
                description="System asks SECOND question (NDA type)",
                expected_state={"qud": "1 question", "private.issues": "3 questions"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Mutual",
                description="User answers NDA type question",
                expected_state={"commitments": "+1", "qud": "0"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What is the effective date?",
                description="System asks THIRD question (incrementally)",
                expected_state={"qud": "1 question", "private.issues": "2 questions"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="January 1, 2025",
                description="User answers effective date question",
                expected_state={"commitments": "+1", "qud": "0"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What is the duration of confidentiality obligations?",
                description="System asks FOURTH question (duration)",
                expected_state={"qud": "1 question", "private.issues": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="5 years",
                description="User answers duration question",
                expected_state={"commitments": "+1", "qud": "0"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="Which state law should govern this agreement?",
                description="System asks FIFTH and FINAL question (governing law)",
                expected_state={"qud": "1 question", "private.issues": "0 questions"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="California",
                description="User answers final question - plan complete",
                expected_state={"commitments": "+1", "qud": "0", "plan": "complete"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="I have all the information needed to draft your NDA.",
                description="System confirms plan completion",
                expected_state={"qud": "0", "private.issues": "0"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="""Here is your Non-Disclosure Agreement:

═══════════════════════════════════════════════════════════════════════
                    MUTUAL NON-DISCLOSURE AGREEMENT
═══════════════════════════════════════════════════════════════════════

This Mutual Non-Disclosure Agreement (the "Agreement") is entered into
as of January 1, 2025 (the "Effective Date") by and between:

    Acme Corp ("First Party")
    and
    Smith Inc ("Second Party")

(collectively, the "Parties")

WHEREAS, the Parties wish to explore a business relationship and may
disclose certain confidential information to each other;

NOW, THEREFORE, in consideration of the mutual covenants and agreements
contained herein, the Parties agree as follows:

1. CONFIDENTIAL INFORMATION
   Each Party agrees to hold in strict confidence any information marked
   as confidential or that would reasonably be considered confidential.

2. OBLIGATIONS
   Each Party shall:
   (a) Not disclose Confidential Information to third parties
   (b) Use Confidential Information only for the intended purpose
   (c) Protect such information with the same care as its own confidential
       information

3. TERM
   This Agreement shall remain in effect for a period of 5 years from
   the Effective Date.

4. GOVERNING LAW
   This Agreement shall be governed by and construed in accordance with
   the laws of the State of California, without regard to its conflict
   of law provisions.

5. ENTIRE AGREEMENT
   This Agreement constitutes the entire agreement between the Parties
   concerning the subject matter hereof.

IN WITNESS WHEREOF, the Parties have executed this Agreement as of the
Effective Date.

_____________________________          _____________________________
Acme Corp                             Smith Inc
Authorized Signature                  Authorized Signature

═══════════════════════════════════════════════════════════════════════
                    [End of Document]
═══════════════════════════════════════════════════════════════════════

✓ NDA successfully generated using your specifications
✓ Ready for review and execution""",
                description=(
                    "System generates complete NDA document using all collected information"
                ),
                expected_state={
                    "qud": "0",
                    "private.issues": "0",
                    "document_generated": "true",
                },
                is_payoff=True,  # PAYOFF: High-value NDA document generated
            ),
        ],
    )


def scenario_volunteer_information() -> DemoScenario:
    """Scenario demonstrating volunteer information handling.

    Shows how the system handles extra information provided by the user
    before it's asked for.
    """
    return DemoScenario(
        name="Volunteer Information",
        description="Demonstrates handling of unsolicited information",
        features=["Rule 4.1 (IssueAccommodation)", "Volunteer information integration"],
        confidence_mode="optimistic",
        steps=[
            ScenarioStep(
                speaker="user",
                utterance="I need to draft an NDA",
                description="User initiates task",
                expected_state={"plan": "active", "private.issues": "4 questions"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What are the parties to the NDA?",
                description="System asks for parties",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Acme Corp and Smith Inc, effective January 1, 2025",
                description="User provides parties AND effective date (volunteer info)",
                expected_state={"commitments": "+2", "qud": "0", "private.issues": "-1"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What is the duration of confidentiality obligations?",
                description="System SKIPS date question (already answered) - asks next",
                expected_state={"qud": "1 question", "private.issues": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="3 years, mutual NDA, California law",
                description="User volunteers remaining information efficiently",
                expected_state={"commitments": "+3", "qud": "0", "plan": "complete"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="""Perfect! I have all the details. Here's your NDA:

╔══════════════════════════════════════════════════════════════╗
║          MUTUAL NON-DISCLOSURE AGREEMENT                     ║
╚══════════════════════════════════════════════════════════════╝

Parties:     Acme Corp and Smith Inc
Effective:   January 1, 2025
Term:        3 years
Type:        Mutual (both parties bound)

✓ Document ready for execution
✓ Efficiently gathered via volunteer information""",
                description="System generates NDA using volunteered information",
                expected_state={"document_generated": "true"},
                is_payoff=True,  # PAYOFF: Efficient NDA generation
            ),
        ],
    )


def scenario_clarification() -> DemoScenario:
    """Scenario demonstrating clarification questions (Rule 4.3).

    Shows how the system asks for clarification when it doesn't
    understand an answer.
    """
    return DemoScenario(
        name="Clarification Questions",
        description="Demonstrates clarification when answers are unclear (Rule 4.3)",
        features=["Rule 4.3 (IssueClarification)", "Invalid answer handling"],
        confidence_mode="optimistic",
        steps=[
            ScenarioStep(
                speaker="user",
                utterance="I need to draft an NDA",
                description="User initiates task",
                expected_state={"plan": "active"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What are the parties to the NDA?",
                description="System asks for parties",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="blue",
                description="User provides invalid/unclear answer",
                expected_state={"qud": "2 questions"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What is a valid parties?",
                description="System asks clarification question (Rule 4.3)",
                expected_state={"qud": "2 questions"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Acme Corp and Smith Inc",
                description="User provides valid answer to clarification",
                expected_state={"commitments": "+1", "qud": "1 question"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What is the effective date?",
                description="System returns to normal question sequence",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="January 1, 2025",
                description="User provides date",
                expected_state={"commitments": "+1", "qud": "0"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="""
╔══════════════════════════════════════════════════════════════╗
║        CLARIFICATION HANDLING ANALYSIS REPORT                ║
╚══════════════════════════════════════════════════════════════╝

NDA Drafting Progress - WITH CLARIFICATION RECOVERY

Information Collected:
  Task:            Draft NDA
  Parties:         Acme Corp and Smith Inc (after clarification)
  Effective Date:  January 1, 2025
  Status:          ✓ Proceeding after successful clarification

Clarification Analysis (Rule 4.3 - IssueClarification):

Dialogue Flow with Clarification:
  1. System asks: "What are the parties to the NDA?"
     User answers: "blue"
     Validation:   domain.resolves("blue", Q_parties) → FALSE
     Result:       ✗ Invalid answer detected

  2. System generates clarification question (Rule 4.3)
     Clarification: "What is a valid parties?"
     QUD state:     [Q_parties, CQ_valid_parties] (nested)
     Strategy:      Push clarification above original question
     Result:        User prompted for valid response

  3. User answers clarification: "Acme Corp and Smith Inc"
     Validation:    domain.resolves("Acme Corp and Smith Inc", Q_parties) → TRUE
     Resolution:    Pops CQ_valid_parties, resolves Q_parties
     QUD state:     [] (both questions resolved)
     Result:        ✓ Valid parties established

  4. System continues: "What is the effective date?"
     Behavior:      Normal flow resumed after clarification
     Result:        ✓ Dialogue progressing smoothly

Clarification Handling Metrics:
  Invalid Answers:         1 ("blue")
  Clarifications Needed:   1 (Rule 4.3 applied once)
  Recovery Success:        ✓ 100% (user provided valid response)
  Dialogue Continuity:     ✓ Maintained (no disruption)
  Extra Turns:             2 (1 invalid + 1 clarification response)

Rule 4.3 Demonstration:
  ✓ Detected invalid answer through domain validation
  ✓ Generated appropriate clarification question
  ✓ Maintained question stack (QUD) correctly
  ✓ Nested clarification above original question
  ✓ Resolved both questions when valid answer provided
  ✓ Continued dialogue flow seamlessly

System Behavior - Error Recovery:
  ⚠ User provided nonsensical answer: "blue"
  ✓ System did NOT accept invalid input
  ✓ System did NOT proceed with bad data
  ✓ System requested clarification politely
  ✓ System handled corrected input properly
  ✓ Dialogue recovered gracefully

Comparison: With vs. Without Clarification:
  Without Rule 4.3:
    → Accept "blue" as parties
    → Generate invalid NDA
    → User discovers error later
    → Must restart dialogue

  With Rule 4.3 (this dialogue):
    → Detect "blue" is invalid
    → Request clarification immediately
    → Get valid input "Acme Corp and Smith Inc"
    → Continue successfully ✓

User Experience Benefits:
  ✓ Prevented proceeding with bad data
  ✓ Provided clear recovery path
  ✓ Maintained conversational flow
  ✓ No need to restart dialogue
  ✓ Minimal overhead (2 extra turns)

Recommendation:
  Rule 4.3 (IssueClarification) successfully prevented invalid
  data from corrupting the dialogue state. The system detected
  the validation failure, generated an appropriate clarification
  question, and recovered when the user provided valid input.
  Essential for robust dialogue management.""",
                description="System generates clarification analysis report",
                expected_state={"clarification_report": "generated"},
                is_payoff=True,  # PAYOFF: Clarification handling analysis
            ),
        ],
    )


def scenario_dependent_questions() -> DemoScenario:
    """Scenario demonstrating dependent question handling (Rule 4.4).

    Shows how the system ensures prerequisite questions are asked
    before dependent questions.
    """
    return DemoScenario(
        name="Dependent Questions",
        description="Demonstrates prerequisite question ordering (Rule 4.4)",
        features=["Rule 4.4 (DependentIssueAccommodation)", "Question dependencies"],
        confidence_mode="optimistic",
        steps=[
            ScenarioStep(
                speaker="user",
                utterance="I need to book a flight",
                description="User initiates task with dependent questions",
                expected_state={"plan": "active", "private.issues": "5+ questions"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What's your departure city?",
                description="System asks prerequisite question first",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="London",
                description="User answers prerequisite",
                expected_state={"commitments": "+1"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What's your destination city?",
                description="System continues with other prerequisites",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="New York",
                description="User answers",
                expected_state={"commitments": "+1"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What's the price?",
                description="System can NOW ask dependent question (after prerequisites answered)",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Under $500",
                description="User provides price constraint",
                expected_state={"commitments": "+1", "qud": "0"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="""
╔══════════════════════════════════════════════════════════════╗
║      DEPENDENT QUESTION HANDLING ANALYSIS REPORT             ║
╚══════════════════════════════════════════════════════════════╝

Flight Search Summary - WITH DEPENDENCY MANAGEMENT

Search Parameters:
  Departure:       London
  Destination:     New York
  Price Constraint: Under $500
  Status:          ✓ All prerequisites satisfied

Dependency Analysis (Rule 4.4 - DependentIssueAccommodation):

Question Dependency Structure:
  Prerequisites (must be asked first):
    ✓ Q_departure_city  → Answered: London
    ✓ Q_destination     → Answered: New York

  Dependent Questions (blocked until prerequisites satisfied):
    ⏸ Q_price          → BLOCKED initially (needs route info)
    ✓ Q_price          → UNBLOCKED after both cities known
    ✓ Q_price          → Answered: Under $500

Dialogue Flow with Dependency Management:
  1. System asks: "What's your departure city?" (Prerequisite #1)
     User answers: "London"
     Dependencies: price still BLOCKED (needs destination too)
     Result:       ✓ First prerequisite satisfied

  2. System asks: "What's your destination city?" (Prerequisite #2)
     User answers: "New York"
     Dependencies: price now UNBLOCKED (route complete!)
     Result:       ✓ All prerequisites satisfied

  3. System asks: "What's the price?" (Dependent Question)
     Dependency Check: Can ask because [London, New York] known
     User answers: "Under $500"
     Result:       ✓ Dependent question answered successfully

Rule 4.4 Demonstration:
  ✓ Identified prerequisite dependencies correctly
  ✓ Asked prerequisite questions BEFORE dependent questions
  ✓ Did NOT ask price before knowing route
  ✓ Unlocked price question after prerequisites satisfied
  ✓ Maintained correct question ordering throughout

Why Dependencies Matter:
  Price depends on Route:
    ❌ Cannot ask "What's the price?" without knowing route
    ❌ Price varies by route: LON→NYC ≠ LON→PAR
    ✓ Must know both cities before price makes sense

  System Behavior:
    ✓ Detected dependency: price depends on [departure, destination]
    ✓ Ensured prerequisites asked first
    ✓ Only raised price question after route established

Prerequisite Satisfaction Timeline:
  Turn 0: price BLOCKED     (no prerequisites satisfied)
  Turn 1: price BLOCKED     (1/2 prerequisites: departure only)
  Turn 2: price UNBLOCKED   (2/2 prerequisites: departure + destination)
  Turn 3: price ANSWERED    (constraint provided)

Comparison: With vs. Without Rule 4.4:
  Without dependency management:
    System: "What's the price?"
    User:   "For which route?"
    System: "What's your departure city?"
    → Confusing, illogical question order

  With Rule 4.4 (this dialogue):
    System: "What's your departure city?"
    User:   "London"
    System: "What's your destination city?"
    User:   "New York"
    System: "What's the price?"
    → Logical, natural question order ✓

Flight Search Results:
  Route:           London (LHR) → New York (JFK)
  Price Filter:    Maximum $500
  Available Flights: 12 options found

  Best Match:
    Flight:        BA117 (British Airways)
    Departure:     10:30 AM from Heathrow
    Arrival:       1:15 PM at JFK
    Price:         $485
    Duration:      7h 45m
    Status:        ✓ Meets all criteria

Recommendation:
  Rule 4.4 (DependentIssueAccommodation) successfully managed
  question dependencies. The system ensured prerequisite questions
  were answered before asking dependent questions, resulting in
  a logical, natural dialogue flow. Essential for complex domains
  with interdependent information requirements.""",
                description="System generates dependency analysis + search results",
                expected_state={"dependency_report": "generated", "search_complete": "true"},
                is_payoff=True,  # PAYOFF: Dependency analysis + flight results
            ),
        ],
    )


def scenario_reaccommodation() -> DemoScenario:
    """Scenario demonstrating question reaccommodation (Rules 4.6-4.8).

    Shows how the system handles users changing their mind about
    previous answers, including dramatic plan changes (flight → train).
    """
    return DemoScenario(
        name="Belief Revision (Reaccommodation)",
        description="Demonstrates handling of changed answers (Rules 4.6-4.8)",
        features=[
            "Rule 4.6 (QuestionReaccommodation)",
            "Rule 4.7 (RetractIncompatibleCommitment)",
            "Rule 4.8 (DependentQuestionReaccommodation)",
        ],
        confidence_mode="optimistic",
        steps=[
            ScenarioStep(
                speaker="user",
                utterance="I need to book a flight from London to Paris",
                description="User initiates flight booking task",
                expected_state={"plan": "flight_booking", "mode": "flight"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What's your departure date?",
                description="System asks flight-specific question",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="April 4th",
                description="User provides date",
                expected_state={"commitments": "+1 (date)", "qud": "0"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What cabin class do you prefer: economy, business, or first class?",
                description="System asks flight-specific question (cabin class)",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Actually, I changed my mind - I want to take a train instead",
                description="MAJOR BELIEF REVISION: User switches from flight to train",
                expected_state={
                    "plan": "retract flight, form train plan",
                    "commitments": "retract flight-specific",
                    "mode": "train",
                },
            ),
            ScenarioStep(
                speaker="system",
                utterance="Understood. I'll help you book a train from London to Paris instead.",
                description="System acknowledges dramatic plan change",
                expected_state={"plan": "train_booking"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="The date April 4th is still valid. What time would you like to depart?",
                description="System retains compatible commitment (date), asks train question",
                expected_state={"qud": "1 question", "commitments": "1 retained"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Morning, around 9 AM",
                description="User answers train-specific question",
                expected_state={"commitments": "+1 (time)", "qud": "0"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="Would you like standard or first class for the Eurostar?",
                description="System asks train-specific class question",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Standard class is fine",
                description="User completes train booking info",
                expected_state={"commitments": "+1 (class)", "qud": "0", "plan": "complete"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="Perfect! Booking your Eurostar train for April 4th at 9:00 AM...",
                description="System executes train booking",
                expected_state={"action": "train_booking", "plan": "executing"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="""
═══════════════════════════════════════════════════════════════════════
                    EUROSTAR TRAIN BOOKING
═══════════════════════════════════════════════════════════════════════
Confirmation #:    ES-2025-47821
Status:            ✓ CONFIRMED

───────────────────────────────────────────────────────────────────────
JOURNEY DETAILS
───────────────────────────────────────────────────────────────────────
Route:             London St Pancras → Paris Gare du Nord
Date:              April 4, 2025
Departure:         9:01 AM (London St Pancras International)
Arrival:           12:17 PM (Paris Gare du Nord) - Local time
Duration:          2h 16min
Train:             Eurostar 9012
Class:             Standard
Seat:              Coach 5, Seat 42A (Window, Forward-facing)

───────────────────────────────────────────────────────────────────────
COST BREAKDOWN
───────────────────────────────────────────────────────────────────────
Standard Class Ticket:                        £89.00
Booking Fee:                                   £5.50
                                              ──────
TOTAL:                                        £94.50

Payment Status:       ✓ Charged to card ending 4567

───────────────────────────────────────────────────────────────────────
BELIEF REVISION CASCADE - COMPLETE ANALYSIS
───────────────────────────────────────────────────────────────────────

ORIGINAL PLAN (Retracted):
  Mode:              Flight booking
  Questions raised:  departure_date, cabin_class
  Commitments:       date=April 4th
  Status:            ✗ ABANDONED after user revision

REVISION EVENT:
  Trigger:           "I want to take a train instead"
  Type:              Major plan change (flight → train)
  Scope:             Complete task reframing

RETRACTION CASCADE (Rule 4.7):
  ✗ Retracted: cabin_class question (flight-specific)
  ✗ Retracted: flight_booking plan
  ✓ Retained: departure_date=April 4th (compatible with trains)

NEW PLAN (Formed):
  Mode:              Train booking
  Questions raised:  departure_time, train_class
  Commitments:       date=April 4th (retained), time=9AM, class=Standard
  Status:            ✓ COMPLETED

RE-ACCOMMODATION (Rules 4.6, 4.8):
  ✓ Compatible commitment retained (date)
  ✓ Incompatible questions retracted (cabin class)
  ✓ New questions accommodated (departure time, train class)
  ✓ New plan successfully completed

───────────────────────────────────────────────────────────────────────
SYSTEM BEHAVIOR DEMONSTRATED
───────────────────────────────────────────────────────────────────────
✓ Handled dramatic mid-dialogue plan change gracefully
✓ Rule 4.6: Re-accommodated compatible questions
✓ Rule 4.7: Retracted incompatible commitments (cabin class)
✓ Rule 4.8: Managed dependent question cascade
✓ Completed alternative task successfully (train booking)
✓ No user confusion or repetition needed
✓ Seamless transition from flight to train domain

Impact: User completely changed transportation mode mid-dialogue,
system adapted without disruption and delivered complete booking.

═══════════════════════════════════════════════════════════════════════

✓ Train booking confirmed despite major plan revision
✓ Belief revision cascade handled automatically
✓ Compatible information retained (date)
✓ Incompatible information gracefully discarded (cabin class)
✓ New task completed successfully
✓ Ready for London → Paris journey!""",
                description="Train booking confirmation with belief revision analysis",
                expected_state={"booking_confirmed": "true"},
                is_payoff=True,  # PAYOFF: Train booking + dramatic revision analysis
            ),
        ],
    )


# IBiS2 Scenarios


def scenario_grounding_optimistic() -> DemoScenario:
    """Scenario demonstrating optimistic grounding strategy.

    Shows high-confidence utterances being accepted immediately
    without confirmation.
    """
    return DemoScenario(
        name="Optimistic Grounding",
        description="Demonstrates immediate acceptance of high-confidence utterances",
        features=["Grounding strategies", "ICM acceptance (icm:acc*pos)"],
        confidence_mode="optimistic",
        steps=[
            ScenarioStep(
                speaker="user",
                utterance="I need to draft an NDA",
                description="User utterance with HIGH confidence (0.9)",
                expected_state={"grounding": "optimistic strategy"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="[icm:acc*pos] Okay",
                description="System accepts immediately (no confirmation needed)",
                expected_state={"grounding_status": "grounded"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What are the parties to the NDA?",
                description="System proceeds with task",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Acme Corp and Smith Inc",
                description="User provides parties (high confidence)",
                expected_state={"commitments": "+1", "grounding": "optimistic"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What is the effective date?",
                description="Accepted immediately, continues",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="January 1, 2025",
                description="User provides date (high confidence)",
                expected_state={"commitments": "+1"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="Should this be a mutual or one-way NDA?",
                description="System continues gathering information",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Mutual",
                description="User provides NDA type (high confidence)",
                expected_state={"commitments": "+1", "grounding": "optimistic"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What is the duration of confidentiality obligations?",
                description="System asks for duration",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="5 years",
                description="User provides duration (high confidence)",
                expected_state={"commitments": "+1"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="Which state law should govern this agreement?",
                description="System asks final question",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="California",
                description="User provides governing law (high confidence) - all info collected",
                expected_state={"commitments": "+1", "plan": "complete"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="""
╔══════════════════════════════════════════════════════════════╗
║         OPTIMISTIC GROUNDING ANALYSIS                        ║
╚══════════════════════════════════════════════════════════════╝

Grounding Performance (5 critical inputs):
  1. "I need to draft an NDA" → Confidence: 0.9 → Optimistic: Accept
  2. "Acme Corp and Smith Inc" → Confidence: 0.85 → Optimistic: Accept
  3. "January 1, 2025" → Confidence: 0.9 → Optimistic: Accept
  4. "Mutual" → Confidence: 0.95 → Optimistic: Accept
  5. "5 years" → Confidence: 0.9 → Optimistic: Accept
  6. "California" → Confidence: 0.9 → Optimistic: Accept

Results: 6/6 inputs grounded immediately (100% efficiency)
Turns saved vs cautious: 6 confirmation turns avoided
Time saved: ~2 minutes (assuming 20sec/turn)

✓ Optimistic grounding enabled fastest possible task completion""",
                description="System provides grounding analysis summary",
                expected_state={"grounding_analysis": "complete"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="""Here is your Non-Disclosure Agreement:

═══════════════════════════════════════════════════════════════════════
                    MUTUAL NON-DISCLOSURE AGREEMENT
═══════════════════════════════════════════════════════════════════════

This Mutual Non-Disclosure Agreement (the "Agreement") is entered into
as of January 1, 2025 (the "Effective Date") by and between:

    Acme Corp ("First Party")
    and
    Smith Inc ("Second Party")

(collectively, the "Parties")

WHEREAS, the Parties wish to explore a business relationship and may
disclose certain confidential information to each other;

NOW, THEREFORE, in consideration of the mutual covenants and agreements
contained herein, the Parties agree as follows:

1. CONFIDENTIAL INFORMATION
   Each Party agrees to hold in strict confidence any information marked
   as confidential or that would reasonably be considered confidential.

2. OBLIGATIONS
   Each Party shall:
   (a) Not disclose Confidential Information to third parties
   (b) Use Confidential Information only for the intended purpose
   (c) Protect such information with the same care as its own confidential
       information

3. TERM
   This Agreement shall remain in effect for a period of 5 years from
   the Effective Date.

4. GOVERNING LAW
   This Agreement shall be governed by and construed in accordance with
   the laws of the State of California, without regard to its conflict
   of law provisions.

5. ENTIRE AGREEMENT
   This Agreement constitutes the entire agreement between the Parties
   concerning the subject matter hereof.

IN WITNESS WHEREOF, the Parties have executed this Agreement as of the
Effective Date.

_____________________________          _____________________________
Acme Corp                             Smith Inc
Authorized Signature                  Authorized Signature

═══════════════════════════════════════════════════════════════════════
                    [End of Document]
═══════════════════════════════════════════════════════════════════════

✓ NDA successfully generated using optimistic grounding strategy
✓ Zero confirmation overhead - maximum efficiency achieved
✓ Task completed in 6 turns (vs 12+ turns with cautious grounding)""",
                description="System generates complete NDA document - BUSINESS VALUE DELIVERED",
                expected_state={
                    "qud": "0",
                    "private.issues": "0",
                    "document_generated": "true",
                },
                is_payoff=True,  # PAYOFF: Complete NDA doc + efficiency demo
            ),
        ],
    )


def scenario_grounding_cautious() -> DemoScenario:
    """Scenario demonstrating cautious grounding strategy.

    Shows medium-confidence utterances requiring understanding
    confirmation.
    """
    return DemoScenario(
        name="Cautious Grounding",
        description="Demonstrates confirmation for medium-confidence utterances",
        features=["Grounding strategies", "ICM understanding (icm:und*int)"],
        confidence_mode="cautious",
        steps=[
            ScenarioStep(
                speaker="user",
                utterance="Need NDA draft",
                description="User utterance with MEDIUM confidence (0.65)",
                expected_state={"grounding": "cautious strategy"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="[icm:und*int] Do you want to draft an NDA?",
                description="System requests confirmation (understanding check)",
                expected_state={"grounding_status": "understood"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Yes",
                description="User confirms understanding",
                expected_state={"grounding_status": "grounded"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What are the parties to the NDA?",
                description="System proceeds after confirmation",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Acme Corp and Smith Inc",
                description="User provides parties (high confidence)",
                expected_state={"commitments": "+1"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="Should this be a mutual or one-way NDA?",
                description="System continues gathering information",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Mutual",
                description="User provides NDA type",
                expected_state={"commitments": "+1"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What is the effective date?",
                description="System asks for effective date",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="January 1, 2025",
                description="User provides date",
                expected_state={"commitments": "+1"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What is the duration of confidentiality obligations?",
                description="System asks for duration",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="3 years",
                description="User provides duration",
                expected_state={"commitments": "+1"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="Which state law should govern this agreement?",
                description="System asks final question",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Delaware",
                description="User provides governing law - all info collected",
                expected_state={"commitments": "+1", "plan": "complete"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="""
╔══════════════════════════════════════════════════════════════╗
║         CAUTIOUS GROUNDING ANALYSIS                          ║
╚══════════════════════════════════════════════════════════════╝

Grounding Performance (7 inputs):
  1. "Need NDA draft" → Confidence: 0.65 (MEDIUM)
     ⚠ Ambiguous → Cautious: Request confirmation
     System: "Do you want to draft an NDA?"
     User: "Yes" → ✓ Misunderstanding prevented

  2. "Acme Corp and Smith Inc" → Confidence: 0.85 → Optimistic: Accept
  3. "Mutual" → Confidence: 0.9 → Optimistic: Accept
  4. "January 1, 2025" → Confidence: 0.9 → Optimistic: Accept
  5. "3 years" → Confidence: 0.85 → Optimistic: Accept
  6. "Delaware" → Confidence: 0.9 → Optimistic: Accept

Results: 1 confirmation needed, 5 immediately grounded
Safety overhead: 1 extra turn (vs optimistic)
Trade-off: Prevented potential task mismatch

✓ Cautious grounding balanced speed and accuracy effectively""",
                description="System provides grounding analysis summary",
                expected_state={"grounding_analysis": "complete"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="""Here is your Non-Disclosure Agreement:

═══════════════════════════════════════════════════════════════════════
                    MUTUAL NON-DISCLOSURE AGREEMENT
═══════════════════════════════════════════════════════════════════════

This Mutual Non-Disclosure Agreement (the "Agreement") is entered into
as of January 1, 2025 (the "Effective Date") by and between:

    Acme Corp ("First Party")
    and
    Smith Inc ("Second Party")

(collectively, the "Parties")

WHEREAS, the Parties wish to explore a business relationship and may
disclose certain confidential information to each other;

NOW, THEREFORE, in consideration of the mutual covenants and agreements
contained herein, the Parties agree as follows:

1. CONFIDENTIAL INFORMATION
   Each Party agrees to hold in strict confidence any information marked
   as confidential or that would reasonably be considered confidential.

2. OBLIGATIONS
   Each Party shall:
   (a) Not disclose Confidential Information to third parties
   (b) Use Confidential Information only for the intended purpose
   (c) Protect such information with the same care as its own confidential
       information

3. TERM
   This Agreement shall remain in effect for a period of 3 years from
   the Effective Date.

4. GOVERNING LAW
   This Agreement shall be governed by and construed in accordance with
   the laws of the State of Delaware, without regard to its conflict
   of law provisions.

5. ENTIRE AGREEMENT
   This Agreement constitutes the entire agreement between the Parties
   concerning the subject matter hereof.

IN WITNESS WHEREOF, the Parties have executed this Agreement as of the
Effective Date.

_____________________________          _____________________________
Acme Corp                             Smith Inc
Authorized Signature                  Authorized Signature

═══════════════════════════════════════════════════════════════════════
                    [End of Document]
═══════════════════════════════════════════════════════════════════════

✓ NDA successfully generated using cautious grounding strategy
✓ Task correctly identified through confirmation (prevented mismatch)
✓ Balanced efficiency: 1 safety check avoided potential rework""",
                description="System generates complete NDA document - BUSINESS VALUE DELIVERED",
                expected_state={
                    "qud": "0",
                    "private.issues": "0",
                    "document_generated": "true",
                },
                is_payoff=True,  # PAYOFF: Complete NDA doc + safety demo
            ),
        ],
    )


def scenario_grounding_pessimistic() -> DemoScenario:
    """Scenario demonstrating pessimistic grounding strategy.

    Shows low-confidence utterances requiring perception check
    (repetition request).
    """
    return DemoScenario(
        name="Pessimistic Grounding",
        description="Demonstrates perception check for low-confidence utterances",
        features=["Grounding strategies", "ICM perception (icm:per*neg)"],
        confidence_mode="pessimistic",
        steps=[
            ScenarioStep(
                speaker="user",
                utterance="NDA",
                description="User utterance with LOW confidence (0.4)",
                expected_state={"grounding": "pessimistic strategy"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="[icm:per*neg] Sorry, I didn't catch that. Could you repeat?",
                description="System requests repetition (perception failure)",
                expected_state={"grounding_status": "perception_failed"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="I need to draft a Non-Disclosure Agreement",
                description="User provides clearer utterance",
                expected_state={"grounding_status": "perceived"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What are the parties to the NDA?",
                description="System proceeds after successful perception",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Acme Corp and Smith Inc",
                description="User provides parties (clear utterance)",
                expected_state={"commitments": "+1"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="Should this be a mutual or one-way NDA?",
                description="System continues gathering information",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Mutual",
                description="User provides NDA type",
                expected_state={"commitments": "+1"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What is the effective date?",
                description="System asks for effective date",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="January 1, 2025",
                description="User provides date",
                expected_state={"commitments": "+1"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What is the duration of confidentiality obligations?",
                description="System asks for duration",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="5 years",
                description="User provides duration",
                expected_state={"commitments": "+1"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="Which state law should govern this agreement?",
                description="System asks final question",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="New York",
                description="User provides governing law - all info collected",
                expected_state={"commitments": "+1", "plan": "complete"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="""
╔══════════════════════════════════════════════════════════════╗
║        PESSIMISTIC GROUNDING ANALYSIS                        ║
╚══════════════════════════════════════════════════════════════╝

Grounding Performance (7 inputs):
  1. "NDA" → Confidence: 0.4 (LOW)
     ✗ Too ambiguous → Pessimistic: Request repetition
     System: "Sorry, I didn't catch that. Could you repeat?"
     User: "I need to draft a Non-Disclosure Agreement"
     ✓ Clear input obtained, catastrophic misunderstanding prevented

  2. "Acme Corp and Smith Inc" → Confidence: 0.85 → Optimistic: Accept
  3. "Mutual" → Confidence: 0.9 → Optimistic: Accept
  4. "January 1, 2025" → Confidence: 0.9 → Optimistic: Accept
  5. "5 years" → Confidence: 0.85 → Optimistic: Accept
  6. "New York" → Confidence: 0.9 → Optimistic: Accept

Results: 1 repetition needed, 5 immediately grounded
Safety overhead: 1 extra turn (vs optimistic)
Trade-off: Prevented potential major task mismatch

✓ Pessimistic grounding prevented acting on unreliable input""",
                description="System provides grounding analysis summary",
                expected_state={"grounding_analysis": "complete"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="""Here is your Non-Disclosure Agreement:

═══════════════════════════════════════════════════════════════════════
                    MUTUAL NON-DISCLOSURE AGREEMENT
═══════════════════════════════════════════════════════════════════════

This Mutual Non-Disclosure Agreement (the "Agreement") is entered into
as of January 1, 2025 (the "Effective Date") by and between:

    Acme Corp ("First Party")
    and
    Smith Inc ("Second Party")

(collectively, the "Parties")

WHEREAS, the Parties wish to explore a business relationship and may
disclose certain confidential information to each other;

NOW, THEREFORE, in consideration of the mutual covenants and agreements
contained herein, the Parties agree as follows:

1. CONFIDENTIAL INFORMATION
   Each Party agrees to hold in strict confidence any information marked
   as confidential or that would reasonably be considered confidential.

2. OBLIGATIONS
   Each Party shall:
   (a) Not disclose Confidential Information to third parties
   (b) Use Confidential Information only for the intended purpose
   (c) Protect such information with the same care as its own confidential
       information

3. TERM
   This Agreement shall remain in effect for a period of 5 years from
   the Effective Date.

4. GOVERNING LAW
   This Agreement shall be governed by and construed in accordance with
   the laws of the State of New York, without regard to its conflict
   of law provisions.

5. ENTIRE AGREEMENT
   This Agreement constitutes the entire agreement between the Parties
   concerning the subject matter hereof.

IN WITNESS WHEREOF, the Parties have executed this Agreement as of the
Effective Date.

_____________________________          _____________________________
Acme Corp                             Smith Inc
Authorized Signature                  Authorized Signature

═══════════════════════════════════════════════════════════════════════
                    [End of Document]
═══════════════════════════════════════════════════════════════════════

✓ NDA successfully generated using pessimistic grounding strategy
✓ Repetition request ensured task was correctly understood
✓ Safety-first approach: 1 extra turn prevented potential major error""",
                description="System generates complete NDA document - BUSINESS VALUE DELIVERED",
                expected_state={
                    "qud": "0",
                    "private.issues": "0",
                    "document_generated": "true",
                },
                is_payoff=True,  # PAYOFF: Complete NDA doc + safety-first demo
            ),
        ],
    )


def scenario_grounding_mixed() -> DemoScenario:
    """Scenario demonstrating mixed grounding strategies.

    Shows how grounding strategy adapts to confidence levels
    throughout the dialogue.
    """
    return DemoScenario(
        name="Mixed Grounding Strategies",
        description="Demonstrates adaptive grounding based on confidence",
        features=[
            "Grounding strategies",
            "ICM perception/understanding/acceptance",
            "Confidence-based adaptation",
        ],
        confidence_mode="random",
        steps=[
            ScenarioStep(
                speaker="user",
                utterance="I need to draft an NDA",
                description="High confidence utterance",
                expected_state={"grounding": "optimistic"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What are the parties to the NDA?",
                description="Accepted immediately, proceeds with question",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Acme and Smith",
                description="Low/medium confidence answer (short)",
                expected_state={"grounding": "cautious/pessimistic"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="[icm:und*int] Did you mean 'Acme Corp and Smith Inc'?",
                description="System confirms understanding (medium confidence)",
                expected_state={"grounding_status": "understood"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Yes, exactly",
                description="User confirms",
                expected_state={"commitments": "+1", "grounding_status": "grounded"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What is the effective date?",
                description="System continues with next question",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="January 1, 2025",
                description="User provides date (high confidence)",
                expected_state={"commitments": "+1"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="Should this be a mutual or one-way NDA?",
                description="System continues gathering information",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Mutual",
                description="User provides NDA type",
                expected_state={"commitments": "+1"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What is the duration of confidentiality obligations?",
                description="System asks for duration",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="3 years",
                description="User provides duration",
                expected_state={"commitments": "+1"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="Which state law should govern this agreement?",
                description="System asks final question",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="California",
                description="User provides governing law - all info collected",
                expected_state={"commitments": "+1", "plan": "complete"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="""
╔══════════════════════════════════════════════════════════════╗
║          ADAPTIVE GROUNDING ANALYSIS                         ║
╚══════════════════════════════════════════════════════════════╝

Grounding Performance (8 inputs with strategy adaptation):
  1. "I need to draft an NDA" → Confidence: 0.9 (HIGH)
     Strategy: OPTIMISTIC → Immediate acceptance

  2. "Acme and Smith" → Confidence: 0.6 (MEDIUM)
     ⚠ Informal/ambiguous → Strategy switch: CAUTIOUS
     System: "Did you mean 'Acme Corp and Smith Inc'?"
     User: "Yes, exactly" → ✓ Misunderstanding prevented via adaptation

  3-7. All remaining inputs → Confidence: 0.85-0.95 (HIGH)
     Strategy: OPTIMISTIC → All immediately accepted

Strategy Distribution:
  - OPTIMISTIC: 6/7 inputs (86%)
  - CAUTIOUS: 1/7 inputs (14%)
  - PESSIMISTIC: 0/7 inputs (0%)

Adaptation Events: 2
  Turn 2: HIGH→CAUTIOUS (confidence drop triggered safety check)
  Turn 3: CAUTIOUS→HIGH (confidence restored, returned to fast mode)

Results: Optimal balance of speed and safety
✓ Fast grounding when confidence permits
✓ Safety checks only when needed
✓ Dynamic adaptation to input quality""",
                description="System provides adaptive grounding analysis summary",
                expected_state={"grounding_analysis": "complete"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="""Here is your Non-Disclosure Agreement:

═══════════════════════════════════════════════════════════════════════
                    MUTUAL NON-DISCLOSURE AGREEMENT
═══════════════════════════════════════════════════════════════════════

This Mutual Non-Disclosure Agreement (the "Agreement") is entered into
as of January 1, 2025 (the "Effective Date") by and between:

    Acme Corp ("First Party")
    and
    Smith Inc ("Second Party")

(collectively, the "Parties")

WHEREAS, the Parties wish to explore a business relationship and may
disclose certain confidential information to each other;

NOW, THEREFORE, in consideration of the mutual covenants and agreements
contained herein, the Parties agree as follows:

1. CONFIDENTIAL INFORMATION
   Each Party agrees to hold in strict confidence any information marked
   as confidential or that would reasonably be considered confidential.

2. OBLIGATIONS
   Each Party shall:
   (a) Not disclose Confidential Information to third parties
   (b) Use Confidential Information only for the intended purpose
   (c) Protect such information with the same care as its own confidential
       information

3. TERM
   This Agreement shall remain in effect for a period of 3 years from
   the Effective Date.

4. GOVERNING LAW
   This Agreement shall be governed by and construed in accordance with
   the laws of the State of California, without regard to its conflict
   of law provisions.

5. ENTIRE AGREEMENT
   This Agreement constitutes the entire agreement between the Parties
   concerning the subject matter hereof.

IN WITNESS WHEREOF, the Parties have executed this Agreement as of the
Effective Date.

_____________________________          _____________________________
Acme Corp                             Smith Inc
Authorized Signature                  Authorized Signature

═══════════════════════════════════════════════════════════════════════
                    [End of Document]
═══════════════════════════════════════════════════════════════════════

✓ NDA successfully generated using adaptive grounding strategy
✓ Strategy adapted dynamically based on confidence (1 safety check)
✓ Optimal balance: Fast completion with targeted safety where needed""",
                description="System generates complete NDA document - BUSINESS VALUE DELIVERED",
                expected_state={
                    "qud": "0",
                    "private.issues": "0",
                    "document_generated": "true",
                },
                is_payoff=True,  # PAYOFF: Complete NDA doc + adaptive strategy demo
            ),
        ],
    )


# IBiS4 Scenarios (Action-Oriented Dialogue)


def scenario_action_confirmation() -> DemoScenario:
    """Scenario demonstrating action execution with confirmation.

    Shows how the system requests confirmation before executing
    critical actions (booking, payment, etc.). Extended to show
    complete travel package with multiple action confirmations.
    """
    return DemoScenario(
        name="Action Confirmation",
        description="Demonstrates action execution with user confirmation (IBiS-4)",
        features=["Action execution", "Confirmation requests", "Device interface"],
        confidence_mode="cautious",
        steps=[
            ScenarioStep(
                speaker="user",
                utterance="Book a complete trip to Paris from January 5 to January 10, 2025",
                description="User requests comprehensive travel booking",
                expected_state={"actions": "3 queued", "plan": "active"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="Should I book flight AF 1234 departing JFK at 6:30 PM on January 5?",
                description="System requests confirmation for first action (flight)",
                expected_state={"qud": "1 question (confirmation)"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Yes",
                description="User confirms flight",
                expected_state={"qud": "0", "commitments": "+1"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="Flight confirmed. Should I book Hotel de Paris for January 5-10?",
                description="System confirms flight, requests hotel confirmation",
                expected_state={"qud": "1 question (confirmation)", "actions": "2 queued"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Yes",
                description="User confirms hotel",
                expected_state={"qud": "0", "commitments": "+1"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="Hotel reserved. Should I book a rental car (compact)?",
                description="System confirms hotel, requests car rental confirmation",
                expected_state={"qud": "1 question (confirmation)", "actions": "1 queued"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Yes, book the car",
                description="User confirms car rental - all actions confirmed",
                expected_state={"qud": "0", "commitments": "+1", "plan": "complete"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="Perfect! All bookings confirmed. Generating your complete itinerary...",
                description="System executes all actions successfully",
                expected_state={
                    "actions": "0 remaining",
                    "commitments": "3 (flight, hotel, car)",
                    "action_result": "success",
                },
            ),
            ScenarioStep(
                speaker="system",
                utterance="""
═══════════════════════════════════════════════════════════════════════
                    COMPLETE TRAVEL ITINERARY
═══════════════════════════════════════════════════════════════════════
Booking Reference: PARIS-2025-00142
Status:            ✓ ALL CONFIRMED
Traveler:          Customer
Destination:       Paris, France
Travel Dates:      January 5-10, 2025 (5 nights)

───────────────────────────────────────────────────────────────────────
OUTBOUND FLIGHT
───────────────────────────────────────────────────────────────────────
Confirmation:      AF-1234-5JAN25
Airline:           Air France
Flight:            AF 1234
Departure:         JFK Terminal 1, New York → 6:30 PM, Jan 5
Arrival:           CDG Terminal 2E, Paris → 8:15 AM, Jan 6 (+1 day)
Duration:          7h 45min
Seat:              23A (Window, Economy)
Baggage:           1 checked bag included
Status:            ✓ CONFIRMED

───────────────────────────────────────────────────────────────────────
ACCOMMODATION
───────────────────────────────────────────────────────────────────────
Confirmation:      HDP-2025-00142
Hotel:             Hotel de Paris ⭐⭐⭐⭐
Location:          8 Rue de la Paix, 75002 Paris
Check-in:          January 6, 2025 at 3:00 PM
Check-out:         January 10, 2025 at 11:00 AM
Duration:          4 nights
Room:              Superior Double Room with City View
Rate:              $220/night
Amenities:         • Free WiFi • Breakfast included • Spa access
Total:             $880
Status:            ✓ CONFIRMED

───────────────────────────────────────────────────────────────────────
GROUND TRANSPORTATION
───────────────────────────────────────────────────────────────────────
Confirmation:      HERTZ-FR-789456
Provider:          Hertz France
Vehicle:           Compact Car (Renault Clio or similar)
Pickup:            CDG Airport, January 6 at 9:00 AM
Return:            CDG Airport, January 10 at 5:00 PM
Duration:          4 days
Rate:              $45/day
Insurance:         Basic coverage included
Total:             $180
Status:            ✓ CONFIRMED

───────────────────────────────────────────────────────────────────────
RETURN FLIGHT
───────────────────────────────────────────────────────────────────────
Confirmation:      AF-1235-10JAN25
Airline:           Air France
Flight:            AF 1235
Departure:         CDG Terminal 2E, Paris → 7:45 PM, Jan 10
Arrival:           JFK Terminal 1, New York → 10:30 PM, Jan 10
Duration:          8h 45min
Seat:              24B (Middle, Economy)
Baggage:           1 checked bag included
Status:            ✓ CONFIRMED

═══════════════════════════════════════════════════════════════════════
COST SUMMARY
═══════════════════════════════════════════════════════════════════════
Flights (roundtrip):    $650
Hotel (4 nights):       $880
Car rental (4 days):    $180
                        ─────
TOTAL PACKAGE:          $1,710

Payment Status:         ✓ Processed
Confirmation Email:     ✓ Sent to customer@email.com
Mobile Boarding Pass:   ✓ Available 24hrs before departure

═══════════════════════════════════════════════════════════════════════

✓ Complete Paris travel package confirmed
✓ All 3 components booked with user confirmation at each step
✓ Action confirmation workflow demonstrated successfully
✓ Ready for travel!""",
                description="Complete travel itinerary with all confirmations",
                expected_state={"confirmation_generated": "true"},
                is_payoff=True,  # PAYOFF: Complete professional travel itinerary
            ),
        ],
    )


def scenario_negotiation_alternatives() -> DemoScenario:
    """Scenario demonstrating negotiation with alternatives.

    Shows how the system presents alternatives and handles
    acceptance/rejection using Issues Under Negotiation (IUN).
    Extended to complete booking after successful negotiation.
    """
    return DemoScenario(
        name="Negotiation with Alternatives",
        description="Demonstrates negotiation and alternative selection (IBiS-4)",
        features=["IUN (Issues Under Negotiation)", "Alternative proposals", "Rejection handling"],
        confidence_mode="optimistic",
        steps=[
            ScenarioStep(
                speaker="user",
                utterance="Find me a hotel in Paris for January 10-15",
                description="User requests hotel search with dates",
                expected_state={"plan": "active"},
            ),
            ScenarioStep(
                speaker="system",
                utterance=(
                    "I found two hotels: Hotel Expensive ($200/night) or Hotel Budget ($120/night)"
                ),
                description="System presents alternatives - both added to IUN",
                expected_state={"iun": "2 options"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="No, Hotel Expensive is too expensive",
                description="User rejects first option",
                expected_state={"iun": "1 option remaining"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="How about Hotel Budget at $120/night?",
                description="System proposes remaining alternative",
                expected_state={"iun": "1 option", "qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Yes, that works! Book it",
                description="User accepts alternative and requests booking",
                expected_state={
                    "iun": "0",
                    "commitments": "+1 (hotel selected)",
                    "qud": "0",
                },
            ),
            ScenarioStep(
                speaker="system",
                utterance="Perfect! Should I confirm Hotel Budget for January 10-15, 2025?",
                description="System requests final booking confirmation",
                expected_state={"qud": "1 question (confirmation)"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Yes, confirm it",
                description="User confirms final booking",
                expected_state={"qud": "0", "actions": "1 executing"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="Booking confirmed! Generating your reservation details...",
                description="System executes booking action successfully",
                expected_state={"action_result": "success", "plan": "complete"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="""
═══════════════════════════════════════════════════════════════════════
                    BOOKING CONFIRMATION
═══════════════════════════════════════════════════════════════════════
Confirmation #:    HB-2025-98765
Status:            ✓ CONFIRMED VIA NEGOTIATION
Booking Method:    Alternative Selection (2 options presented, 1 accepted)

───────────────────────────────────────────────────────────────────────
HOTEL DETAILS
───────────────────────────────────────────────────────────────────────
Hotel:             Hotel Budget ⭐⭐⭐⭐ (4.2/5 - 1,247 reviews)
Location:          45 Rue de Rivoli, 75001 Paris, France
                   • 5 min walk to Louvre Museum
                   • Near Metro: Châtelet (Lines 1, 4, 7, 11, 14)

Check-in:          January 10, 2025 at 2:00 PM
Check-out:         January 15, 2025 at 11:00 AM
Duration:          5 nights

Room Type:         Standard Double Room
Bed:               1 Queen Bed
Max Occupancy:     2 guests
View:              City view

───────────────────────────────────────────────────────────────────────
AMENITIES & SERVICES
───────────────────────────────────────────────────────────────────────
✓ Free high-speed WiFi throughout hotel
✓ Continental breakfast included (7:00 AM - 10:00 AM)
✓ 24-hour front desk and concierge
✓ Luggage storage available
✓ Daily housekeeping
✓ Safe in room
✓ Hair dryer and toiletries

───────────────────────────────────────────────────────────────────────
NEGOTIATION SUMMARY
───────────────────────────────────────────────────────────────────────
Initial Options Presented:
  1. Hotel Expensive - $200/night
     User Response: ✗ Rejected (too expensive)

  2. Hotel Budget - $120/night
     User Response: ✓ Accepted

Negotiation Outcome:
  • User saved: $80/night ($400 total for 5 nights)
  • Alternative successfully negotiated
  • Both parties satisfied with final selection

───────────────────────────────────────────────────────────────────────
COST BREAKDOWN
───────────────────────────────────────────────────────────────────────
Room Rate:            $120/night × 5 nights = $600.00
City Tax:                    $3.50/night × 5 =  $17.50
Service Fee:                                    $12.50
                                                ───────
TOTAL:                                         $630.00

Payment Method:       Credit card ending in 4567
Payment Status:       ✓ Authorized (charged at check-in)

───────────────────────────────────────────────────────────────────────
CONFIRMATION DETAILS
───────────────────────────────────────────────────────────────────────
✓ Confirmation email sent to: customer@email.com
✓ Reservation guaranteed (credit card on file)
✓ Free cancellation until January 3, 2025
✓ Mobile check-in available via hotel app

═══════════════════════════════════════════════════════════════════════

✓ Booking completed successfully via negotiation workflow
✓ Alternative selection process demonstrated (IUN)
✓ User preferences respected (rejected expensive, accepted budget)
✓ $400 saved through negotiation
✓ Ready for Paris trip!""",
                description="Complete booking confirmation after successful negotiation",
                expected_state={"confirmation_generated": "true"},
                is_payoff=True,  # PAYOFF: Complete booking after negotiation
            ),
        ],
    )


def scenario_action_rollback() -> DemoScenario:
    """Scenario demonstrating action rollback on failure.

    Shows how the system handles action failures and rolls back
    optimistic commitments when execution fails. Extended to show
    successful recovery with alternative payment method.
    """
    return DemoScenario(
        name="Action Rollback",
        description="Demonstrates error handling and rollback (IBiS-4)",
        features=["Action failure", "Rollback mechanism", "Error recovery"],
        confidence_mode="optimistic",
        steps=[
            ScenarioStep(
                speaker="user",
                utterance="Book Hotel de Paris for January 5-10, 2025",
                description="User requests booking",
                expected_state={"actions": "1 queued"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="Booking Hotel de Paris...",
                description="System attempts action (optimistic commitment)",
                expected_state={
                    "commitments": "+1 (hotel_booked - optimistic)",
                    "action_status": "executing",
                },
            ),
            ScenarioStep(
                speaker="system",
                utterance="I'm sorry, the booking failed: Payment declined",
                description="System detects action failure",
                expected_state={"action_result": "failure"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="I've rolled back the booking. The hotel was not reserved.",
                description="System performs rollback - removes optimistic commitment",
                expected_state={
                    "commitments": "-1 (hotel_booked removed)",
                    "rollback": "performed",
                },
            ),
            ScenarioStep(
                speaker="system",
                utterance="Would you like to try a different payment method?",
                description="System offers recovery option",
                expected_state={"qud": "1 question (recovery)"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Yes, try my other credit card",
                description="User accepts recovery option with alternative payment",
                expected_state={"qud": "0", "payment_method": "alternative"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="Attempting booking with alternative payment method...",
                description="System retries with new payment method",
                expected_state={"action_status": "retrying"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="Success! Payment accepted. Hotel de Paris is now confirmed.",
                description="System successfully completes booking with alternative payment",
                expected_state={
                    "action_result": "success",
                    "commitments": "+1 (hotel_booked)",
                    "recovery": "successful",
                },
            ),
            ScenarioStep(
                speaker="system",
                utterance="""
═══════════════════════════════════════════════════════════════════════
                    BOOKING CONFIRMATION - RECOVERED
═══════════════════════════════════════════════════════════════════════
Confirmation #:    HDP-2025-REC-142
Status:            ✓ CONFIRMED (after recovery)
Recovery Method:   Alternative payment successful

───────────────────────────────────────────────────────────────────────
BOOKING DETAILS
───────────────────────────────────────────────────────────────────────
Hotel:             Hotel de Paris ⭐⭐⭐⭐⭐
Location:          5 Place Vendôme, 75001 Paris, France
Check-in:          January 5, 2025 at 3:00 PM
Check-out:         January 10, 2025 at 11:00 AM
Duration:          5 nights

Room Type:         Deluxe Double Room
Amenities:         • King bed • City view • Marble bathroom
                   • Complimentary minibar • Nespresso machine
                   • Free WiFi • Daily turndown service

───────────────────────────────────────────────────────────────────────
COST BREAKDOWN
───────────────────────────────────────────────────────────────────────
Room Rate:            $350/night × 5 nights = $1,750.00
City Tax:                    $5.00/night × 5 =    $25.00
Resort Fee:                                        $50.00
                                                   ──────
TOTAL:                                          $1,825.00

Payment Status:       ✓ CHARGED (alternative card ending 9876)

───────────────────────────────────────────────────────────────────────
RECOVERY TIMELINE
───────────────────────────────────────────────────────────────────────
22:15:30  Initial booking attempt started
22:15:45  Payment processing with card ending 1234
22:15:52  ✗ Payment DECLINED (insufficient funds)
22:15:53  ✓ Automatic rollback initiated
22:15:54  ✓ Optimistic commitment removed
22:15:55  ✓ State restored to pre-booking
22:15:56  Alternative payment option offered to user
22:16:10  User provided alternative card ending 9876
22:16:15  Retry attempt started
22:16:22  ✓ Payment APPROVED
22:16:25  ✓ Booking CONFIRMED

Total Recovery Time: 55 seconds
User Impact: Minimal (single retry, no manual intervention needed)

───────────────────────────────────────────────────────────────────────
ERROR RECOVERY ANALYSIS
───────────────────────────────────────────────────────────────────────
Failure Type:          Payment declined (card 1234)
Detection:             Immediate (during transaction)
Rollback:              ✓ Automatic and complete
State Consistency:     ✓ Maintained throughout
User Notification:     ✓ Transparent error communication
Recovery Offered:      ✓ Alternative payment suggested
Retry Success:         ✓ Booking completed with card 9876

Recovery Effectiveness:
  ✓ No data loss or corruption
  ✓ No duplicate charges
  ✓ Clean state transitions (booking → rollback → rebooked)
  ✓ User experience gracefully handled
  ✓ Final outcome: Successful booking despite initial failure

═══════════════════════════════════════════════════════════════════════
CONFIRMATION DETAILS
═══════════════════════════════════════════════════════════════════════
✓ Confirmation email sent to: customer@email.com
✓ Booking reference: HDP-2025-REC-142
✓ Credit card charged: Card ending 9876
✓ Cancellation policy: Free until 24 hours before check-in

═══════════════════════════════════════════════════════════════════════

✓ Booking successfully recovered from payment failure
✓ Rollback mechanism demonstrated (optimistic commitment removed cleanly)
✓ Alternative payment method accepted
✓ Complete end-to-end error recovery workflow shown
✓ System integrity maintained throughout failure and recovery
✓ Hotel reservation confirmed - ready for Paris trip!""",
                description="Complete booking confirmation after successful error recovery",
                expected_state={"confirmation_generated": "true", "plan": "complete"},
                is_payoff=True,  # PAYOFF: Complete recovery + final booking
            ),
        ],
    )


# Scenario registry

ALL_SCENARIOS: dict[str, DemoScenario] = {
    "incremental": scenario_incremental_questioning(),
    "volunteer": scenario_volunteer_information(),
    "clarification": scenario_clarification(),
    "dependent": scenario_dependent_questions(),
    "reaccommodation": scenario_reaccommodation(),
    "grounding-optimistic": scenario_grounding_optimistic(),
    "grounding-cautious": scenario_grounding_cautious(),
    "grounding-pessimistic": scenario_grounding_pessimistic(),
    "grounding-mixed": scenario_grounding_mixed(),
    "action-confirmation": scenario_action_confirmation(),
    "negotiation": scenario_negotiation_alternatives(),
    "rollback": scenario_action_rollback(),
}


def get_scenario(scenario_name: str) -> DemoScenario | None:
    """Get a scenario by name.

    Args:
        scenario_name: Name of the scenario

    Returns:
        DemoScenario if found, None otherwise
    """
    return ALL_SCENARIOS.get(scenario_name)


def list_scenarios() -> list[str]:
    """Get list of all scenario names.

    Returns:
        List of scenario names
    """
    return list(ALL_SCENARIOS.keys())


def get_ibis3_scenarios() -> list[DemoScenario]:
    """Get all IBiS3 scenarios.

    Returns:
        List of IBiS3 scenarios
    """
    return [
        scenario_incremental_questioning(),
        scenario_volunteer_information(),
        scenario_clarification(),
        scenario_dependent_questions(),
        scenario_reaccommodation(),
    ]


def get_ibis2_scenarios() -> list[DemoScenario]:
    """Get all IBiS2 (grounding) scenarios.

    Returns:
        List of IBiS2 scenarios
    """
    return [
        scenario_grounding_optimistic(),
        scenario_grounding_cautious(),
        scenario_grounding_pessimistic(),
        scenario_grounding_mixed(),
    ]


def get_ibis4_scenarios() -> list[DemoScenario]:
    """Get all IBiS4 (action-oriented) scenarios.

    Returns:
        List of IBiS4 scenarios
    """
    return [
        scenario_action_confirmation(),
        scenario_negotiation_alternatives(),
        scenario_action_rollback(),
    ]
