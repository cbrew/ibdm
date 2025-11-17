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
    """

    speaker: str
    utterance: str
    description: str | None = None
    expected_state: dict[str, str] | None = None


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
                description="System generates complete NDA document using all collected information",
                expected_state={
                    "qud": "0",
                    "private.issues": "0",
                    "document_generated": "true",
                },
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
