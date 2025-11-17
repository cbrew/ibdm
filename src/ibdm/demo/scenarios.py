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
    previous answers.
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
                utterance="I need to book a flight",
                description="User initiates task",
                expected_state={"plan": "active"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What's your departure date?",
                description="System asks for date",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="April 5th",
                description="User provides initial answer",
                expected_state={"commitments": "+1", "qud": "0"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What's your departure city?",
                description="System continues with plan",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Actually, I meant April 4th for the departure date",
                description="User changes mind about previous answer",
                expected_state={
                    "commitments": "retracted old, added new",
                    "private.issues": "+1 (question re-raised)",
                },
            ),
            ScenarioStep(
                speaker="system",
                utterance="What's your departure city?",
                description="System continues (handles correction gracefully)",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="London",
                description="User answers departure city",
                expected_state={"commitments": "+1", "qud": "0"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What's your destination?",
                description="System asks next question",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Paris",
                description="User answers destination",
                expected_state={"commitments": "+1", "qud": "0"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="""
╔══════════════════════════════════════════════════════════════╗
║         BELIEF REVISION TRACKING REPORT                      ║
╚══════════════════════════════════════════════════════════════╝

Flight Booking Summary - WITH REVISION HISTORY

Final Commitments:
  Departure Date:  April 4, 2025
  Departure City:  London
  Destination:     Paris
  Status:          ✓ Ready to proceed

Revision History:
  1. Initial: departure_date = April 5th
     → Retracted by user during dialogue

  2. Revised: departure_date = April 4th
     → Current commitment (Rule 4.6)

  3. Question re-accommodation:
     → Original Q_departure_date answered
     → Then retracted and re-raised to private.issues
     → Then answered again with new value
     → Demonstrates Rules 4.6, 4.7, 4.8

System Behavior:
  ✓ Gracefully handled mid-dialogue correction
  ✓ Retracted incompatible commitment (Rule 4.7)
  ✓ Re-accommodated corrected question (Rule 4.6)
  ✓ No dependent questions needed re-accommodation (Rule 4.8)
  ✓ Continued dialogue flow seamlessly

Belief Revision Demonstration:
  This dialogue showcases the system's ability to handle
  users changing their mind about previous answers without
  disrupting the conversation flow. The system maintains
  consistency by retracting outdated commitments and
  re-validating dependent information.

Ready to proceed with flight search:
  London → Paris, departing April 4, 2025""",
                description="System generates revision tracking report",
                expected_state={"revision_report": "generated"},
                is_payoff=True,  # PAYOFF: Belief revision analysis
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
                utterance="""
╔══════════════════════════════════════════════════════════════╗
║         OPTIMISTIC GROUNDING ANALYSIS REPORT                 ║
╚══════════════════════════════════════════════════════════════╝

Dialogue Completion Summary:
  Task:            NDA Drafting
  Grounding Mode:  OPTIMISTIC
  Status:          ✓ Successfully Grounded

Information Collected:
  Parties:         Acme Corp and Smith Inc
  Effective Date:  January 1, 2025

Grounding Analysis:

Turn-by-Turn Grounding:
  1. "I need to draft an NDA"
     Confidence: HIGH (0.9)
     Strategy:   Optimistic (immediate acceptance)
     ICM:        [icm:acc*pos] "Okay"
     Result:     ✓ Grounded without confirmation

  2. "Acme Corp and Smith Inc"
     Confidence: HIGH (0.85)
     Strategy:   Optimistic (immediate acceptance)
     ICM:        Implicit acceptance
     Result:     ✓ Grounded, proceed to next question

  3. "January 1, 2025"
     Confidence: HIGH (0.9)
     Strategy:   Optimistic (immediate acceptance)
     ICM:        Implicit acceptance
     Result:     ✓ Grounded, ready for next step

Efficiency Metrics:
  Total Turns:          3 user utterances
  Confirmation Turns:   0 (optimistic strategy)
  Clarification Turns:  0 (high confidence throughout)
  Efficiency Gain:      100% (no overhead for grounding)

Strategy Benefits:
  ✓ Fastest dialogue completion
  ✓ Natural conversational flow
  ✓ No unnecessary confirmations
  ✓ User not interrupted by system doubts

Risk Assessment:
  ⚠ Assumes high confidence = correct interpretation
  ⚠ No safety net for misunderstandings
  ✓ Appropriate when confidence is consistently high
  ✓ Best for clear, unambiguous utterances

Recommendation:
  Optimistic grounding successfully applied. High confidence
  scores justified immediate acceptance. No errors detected.
  Dialogue progressed efficiently without grounding overhead.""",
                description="System generates optimistic grounding analysis",
                expected_state={"grounding_report": "generated"},
                is_payoff=True,  # PAYOFF: Grounding analysis report
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
                utterance="""
╔══════════════════════════════════════════════════════════════╗
║         CAUTIOUS GROUNDING ANALYSIS REPORT                   ║
╚══════════════════════════════════════════════════════════════╝

Dialogue Completion Summary:
  Task:            NDA Drafting
  Grounding Mode:  CAUTIOUS
  Status:          ✓ Successfully Grounded via Confirmation

Information Collected:
  Task Intent:     Draft NDA (confirmed)
  Parties:         Acme Corp and Smith Inc

Grounding Analysis:

Turn-by-Turn Grounding:
  1. "Need NDA draft"
     Confidence: MEDIUM (0.65)
     Strategy:   Cautious (understanding check required)
     ICM:        [icm:und*int] "Do you want to draft an NDA?"
     Result:     ⚠ Required confirmation before grounding

  2. "Yes" (confirmation)
     Confidence: HIGH (0.95)
     Strategy:   Optimistic (confirmation accepted)
     ICM:        Implicit acceptance
     Result:     ✓ Intent now grounded, proceed with task

  3. "Acme Corp and Smith Inc"
     Confidence: HIGH (0.85)
     Strategy:   Optimistic (clear answer)
     ICM:        Implicit acceptance
     Result:     ✓ Grounded, ready for next step

Efficiency Metrics:
  Total Turns:          3 user utterances
  Confirmation Turns:   1 (understanding check)
  Clarification Turns:  0 (no misunderstandings)
  Efficiency:           Good (1 extra turn for safety)

Strategy Benefits:
  ✓ Balanced approach (speed vs. accuracy)
  ✓ Caught ambiguous initial utterance
  ✓ Prevented potential misunderstanding
  ✓ Low overhead (single confirmation)

Risk Mitigation:
  ⚠ Initial utterance ambiguous: "Need NDA draft"
  ✓ System requested understanding confirmation
  ✓ User clarified intent with "Yes"
  ✓ Misunderstanding avoided through cautious strategy

Grounding Ladder:
  Perception:    ✓ System perceived utterance
  Understanding: ✓ System confirmed understanding (ICM check)
  Acceptance:    ✓ User confirmed system's interpretation
  → Full grounding achieved

Recommendation:
  Cautious grounding appropriately applied. Medium confidence
  utterance required understanding check. One confirmation turn
  prevented potential misunderstanding. Good balance between
  efficiency and accuracy.""",
                description="System generates cautious grounding analysis",
                expected_state={"grounding_report": "generated"},
                is_payoff=True,  # PAYOFF: Grounding analysis report
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
                utterance="""
╔══════════════════════════════════════════════════════════════╗
║        PESSIMISTIC GROUNDING ANALYSIS REPORT                 ║
╚══════════════════════════════════════════════════════════════╝

Dialogue Completion Summary:
  Task:            NDA Drafting
  Grounding Mode:  PESSIMISTIC
  Status:          ✓ Successfully Grounded via Repetition

Information Collected:
  Task Intent:     Draft NDA (clarified after repetition)
  Parties:         Acme Corp and Smith Inc

Grounding Analysis:

Turn-by-Turn Grounding:
  1. "NDA"
     Confidence: LOW (0.4)
     Strategy:   Pessimistic (perception failure)
     ICM:        [icm:per*neg] "Sorry, I didn't catch that. Could you repeat?"
     Result:     ✗ Failed perception, repetition required

  2. "I need to draft a Non-Disclosure Agreement" (repetition)
     Confidence: HIGH (0.9)
     Strategy:   Optimistic (clear after repetition)
     ICM:        Implicit acceptance
     Result:     ✓ Perception successful, understanding achieved

  3. "Acme Corp and Smith Inc"
     Confidence: HIGH (0.85)
     Strategy:   Optimistic (clear answer)
     ICM:        Implicit acceptance
     Result:     ✓ Grounded, ready for next step

Efficiency Metrics:
  Total Turns:          3 user utterances
  Repetition Requests:  1 (perception failure recovery)
  Clarification Turns:  0 (after perception, understanding was clear)
  Efficiency:           Moderate (1 extra turn for perception)

Strategy Benefits:
  ✓ Prevented acting on misunderstood input
  ✓ Safely handled very low confidence utterance
  ✓ Requested clarification before proceeding
  ✓ Avoided potential catastrophic misunderstanding

Risk Mitigation:
  ⚠ Initial utterance too brief: "NDA" (LOW confidence 0.4)
  ✗ Perception deemed unreliable
  ✓ System requested repetition for safety
  ✓ User provided expanded utterance
  ✓ Grounding achieved after repetition

Grounding Ladder Recovery:
  Perception (Attempt 1):  ✗ Failed (confidence too low)
  → Repetition Request:     [icm:per*neg]
  Perception (Attempt 2):  ✓ Successful (clear utterance)
  Understanding:           ✓ Achieved (full sentence context)
  Acceptance:              ✓ System proceeded with task
  → Full grounding achieved after recovery

Comparison with Other Strategies:
  Optimistic: Would have guessed "NDA" meaning → High risk
  Cautious:   Would have confirmed "Did you mean NDA?" → Moderate risk
  Pessimistic: Requested repetition → Safest approach ✓

Recommendation:
  Pessimistic grounding correctly applied. Very low confidence
  utterance warranted perception check. Repetition provided
  clearer input, enabling confident task understanding.
  Extra turn cost justified by safety improvement.""",
                description="System generates pessimistic grounding analysis",
                expected_state={"grounding_report": "generated"},
                is_payoff=True,  # PAYOFF: Grounding analysis report
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
                utterance="""
╔══════════════════════════════════════════════════════════════╗
║          MIXED GROUNDING STRATEGIES REPORT                   ║
╚══════════════════════════════════════════════════════════════╝

Dialogue Completion Summary:
  Task:            NDA Drafting
  Grounding Mode:  ADAPTIVE (Mixed Strategies)
  Status:          ✓ Successfully Grounded with Strategy Adaptation

Information Collected:
  Task Intent:     Draft NDA
  Parties:         Acme Corp and Smith Inc (confirmed)
  Effective Date:  January 1, 2025

Grounding Analysis - Adaptive Strategy Selection:

Turn-by-Turn Grounding with Strategy Adaptation:
  1. "I need to draft an NDA"
     Confidence: HIGH (0.9)
     Strategy:   OPTIMISTIC → Immediate acceptance
     ICM:        Implicit acceptance
     Result:     ✓ Grounded without confirmation
     Reason:     High confidence justified optimistic approach

  2. "Acme and Smith"
     Confidence: MEDIUM (0.6) - Abbreviated, informal
     Strategy:   CAUTIOUS → Understanding check required
     ICM:        [icm:und*int] "Did you mean 'Acme Corp and Smith Inc'?"
     Result:     ⚠ Required confirmation before grounding
     Reason:     Medium confidence + informal names → safety check

  3. "Yes, exactly" (confirmation)
     Confidence: HIGH (0.95)
     Strategy:   OPTIMISTIC → Accept confirmation
     ICM:        Implicit acceptance
     Result:     ✓ Parties grounded after confirmation
     Reason:     Clear affirmation, confidence restored

  4. "January 1, 2025"
     Confidence: HIGH (0.9)
     Strategy:   OPTIMISTIC → Immediate acceptance
     ICM:        Implicit acceptance
     Result:     ✓ Grounded, task progressing
     Reason:     Clear, unambiguous date format

Strategy Adaptation Summary:
  Optimistic used:  3/4 turns (75% - high confidence utterances)
  Cautious used:    1/4 turns (25% - medium confidence utterance)
  Pessimistic used: 0/4 turns (0% - no low confidence utterances)

Efficiency Metrics:
  Total Turns:          4 user utterances
  Confirmation Turns:   1 (understanding check for informal names)
  Repetition Requests:  0 (no perception failures)
  Adaptation Events:    2 (optimistic→cautious, cautious→optimistic)
  Overall Efficiency:   Good (minimal overhead, targeted safety)

Adaptive Grounding Benefits:
  ✓ Matched strategy to confidence level dynamically
  ✓ Fast when possible (optimistic for clear utterances)
  ✓ Safe when needed (cautious for ambiguous input)
  ✓ No unnecessary confirmations on high-confidence turns
  ✓ Prevented misunderstanding on medium-confidence turn

Confidence-Based Decision Making:
  HIGH (>0.8):    → Optimistic (3 instances)
  MEDIUM (0.5-0.8): → Cautious (1 instance)
  LOW (<0.5):     → Pessimistic (0 instances)

Risk vs. Efficiency Trade-off:
  ✓ Optimized for both speed and accuracy
  ✓ Safety overhead only where needed (1 extra turn)
  ✓ 75% of dialogue proceeded without grounding overhead
  ✓ 25% had targeted safety confirmation

Grounding Strategy Evolution:
  Turn 1: OPTIMISTIC (conf=0.9) → Direct
  Turn 2: CAUTIOUS (conf=0.6)   → Adaptation triggered
  Turn 3: OPTIMISTIC (conf=0.95) → Back to fast mode
  Turn 4: OPTIMISTIC (conf=0.9)  → Maintained fast mode

Recommendation:
  Mixed/adaptive grounding successfully balanced efficiency
  and accuracy. System dynamically adjusted strategy based
  on real-time confidence assessment. This approach provides
  optimal user experience: fast when possible, safe when needed.
  Ideal for real-world deployment with variable input quality.""",
                description="System generates adaptive grounding analysis",
                expected_state={"grounding_report": "generated"},
                is_payoff=True,  # PAYOFF: Adaptive grounding strategy report
            ),
        ],
    )


# IBiS4 Scenarios (Action-Oriented Dialogue)


def scenario_action_confirmation() -> DemoScenario:
    """Scenario demonstrating action execution with confirmation.

    Shows how the system requests confirmation before executing
    critical actions (booking, payment, etc.).
    """
    return DemoScenario(
        name="Action Confirmation",
        description="Demonstrates action execution with user confirmation (IBiS-4)",
        features=["Action execution", "Confirmation requests", "Device interface"],
        confidence_mode="cautious",
        steps=[
            ScenarioStep(
                speaker="user",
                utterance="Book a hotel in Paris from January 5 to January 10, 2025",
                description="User requests action - system forms booking plan",
                expected_state={"actions": "1 queued", "plan": "active"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="Should I book Hotel de Paris for January 5-10, 2025?",
                description="System requests confirmation before executing action",
                expected_state={"qud": "1 question (confirmation)"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Yes",
                description="User confirms action",
                expected_state={"qud": "0"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="Booking confirmed. Hotel de Paris reserved for January 5-10, 2025.",
                description="System executes action and reports success",
                expected_state={
                    "actions": "0 remaining",
                    "commitments": "+1 (hotel_booked)",
                    "action_result": "success",
                },
            ),
            ScenarioStep(
                speaker="system",
                utterance="""
╔══════════════════════════════════════════════════════════════╗
║            BOOKING CONFIRMATION                              ║
╚══════════════════════════════════════════════════════════════╝

Confirmation #: HDP-2025-00142
Status:         ✓ CONFIRMED

Hotel:          Hotel de Paris
Location:       Paris, France
Check-in:       January 5, 2025 (3:00 PM)
Check-out:      January 10, 2025 (11:00 AM)
Duration:       5 nights

Room Type:      Standard Double
Rate:           $180/night
Total:          $900

✓ Reservation confirmed
✓ Confirmation email sent
✓ Mobile check-in available""",
                description="System generates booking confirmation",
                expected_state={"confirmation_generated": "true"},
                is_payoff=True,  # PAYOFF: Professional booking confirmation
            ),
        ],
    )


def scenario_negotiation_alternatives() -> DemoScenario:
    """Scenario demonstrating negotiation with alternatives.

    Shows how the system presents alternatives and handles
    acceptance/rejection using Issues Under Negotiation (IUN).
    """
    return DemoScenario(
        name="Negotiation with Alternatives",
        description="Demonstrates negotiation and alternative selection (IBiS-4)",
        features=["IUN (Issues Under Negotiation)", "Alternative proposals", "Rejection handling"],
        confidence_mode="optimistic",
        steps=[
            ScenarioStep(
                speaker="user",
                utterance="Find me a hotel in Paris",
                description="User requests hotel search",
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
                utterance="Yes, that works!",
                description="User accepts alternative",
                expected_state={
                    "iun": "0",
                    "commitments": "+1 (hotel selected)",
                    "qud": "0",
                },
            ),
            ScenarioStep(
                speaker="system",
                utterance="Great! I'll proceed with Hotel Budget.",
                description="System confirms negotiation resolution",
                expected_state={"plan": "progressing"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="""
╔══════════════════════════════════════════════════════════════╗
║           HOTEL SELECTION SUMMARY                            ║
╚══════════════════════════════════════════════════════════════╝

Selected Hotel:  Hotel Budget
Location:        Paris, France
Rate:            $120/night
Rating:          ⭐⭐⭐⭐ (4.2/5)

Amenities:
  ✓ Free WiFi
  ✓ Breakfast included
  ✓ 24-hour reception

Negotiation Summary:
  • Alternatives presented: 2 options
  • Hotel Expensive ($200/night) - Rejected (too expensive)
  • Hotel Budget ($120/night) - Accepted
  • Savings: $80/night vs. expensive option

✓ Selection finalized via negotiation
✓ Ready to proceed with booking""",
                description="System generates selection summary",
                expected_state={"selection_summary": "generated"},
                is_payoff=True,  # PAYOFF: Negotiation result summary
            ),
        ],
    )


def scenario_action_rollback() -> DemoScenario:
    """Scenario demonstrating action rollback on failure.

    Shows how the system handles action failures and rolls back
    optimistic commitments when execution fails.
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
                speaker="system",
                utterance="""
╔══════════════════════════════════════════════════════════════╗
║         ERROR RECOVERY REPORT                                ║
╚══════════════════════════════════════════════════════════════╝

Transaction ID: HDP-2025-FAIL-142
Status:         ✗ FAILED → ✓ RECOVERED

Original Request:
  Hotel:        Hotel de Paris
  Dates:        January 5-10, 2025
  Status:       Attempted (optimistic)

Error Details:
  Type:         Payment declined
  Code:         PAY-001
  Detected:     During execution
  Impact:       Booking not completed

Recovery Actions Taken:
  ✓ Optimistic commitment rolled back
  ✓ No charges applied
  ✓ System state restored to pre-booking
  ✓ Alternative payment options offered

System Integrity:
  ✓ Clean rollback performed
  ✓ No inconsistent state
  ✓ User informed of failure
  ✓ Recovery path provided

Ready for retry with alternative payment method.""",
                description="System generates error recovery report",
                expected_state={"recovery_report": "generated"},
                is_payoff=True,  # PAYOFF: Error handling and recovery report
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
