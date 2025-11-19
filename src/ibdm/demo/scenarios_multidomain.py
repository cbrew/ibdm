from ibdm.demo.scenarios import DemoScenario, ScenarioStep


def scenario_multi_domain() -> DemoScenario:
    """Showcase scenario demonstrating multi-domain dialogue (Travel + NDA).

    Shows how the system can switch between different domains and tasks
    seamlessly, maintaining context and handling task boundaries.
    """
    return DemoScenario(
        name="Multi-Domain Travel & Legal",
        description="Showcase: Seamless switching between Travel (booking) and Legal (NDA) domains",
        features=[
            "Domain switching",
            "Context maintenance",
            "Task boundary management",
            "Multi-intent handling",
        ],
        confidence_mode="optimistic",
        steps=[
            # 1. Start with Travel Task
            ScenarioStep(
                speaker="user",
                utterance="I need to book a flight to Paris for a business meeting",
                description="User initiates Travel task",
                expected_state={"plan": "book_flight", "domain": "travel"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What is your departure city?",
                description="System starts Travel plan",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="San Francisco",
                description="User provides departure city",
                expected_state={"commitments": "+1"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What is your departure date?",
                description="System continues Travel plan",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Next Monday",
                description="User provides date",
                expected_state={"commitments": "+1"},
            ),

            # 2. Switch to Legal Task (Interrupt)
            ScenarioStep(
                speaker="user",
                utterance="Oh wait, before I go, I need to draft an NDA for this meeting",
                description="User interrupts with Legal task (NDA)",
                expected_state={
                    "plan": "draft_nda (pushed on top)",
                    "domain": "legal",
                    "prev_plan": "book_flight (paused)"
                },
            ),
            ScenarioStep(
                speaker="system",
                utterance="I can help with that. What are the parties to the NDA?",
                description="System switches to Legal domain, starts NDA plan",
                expected_state={"qud": "1 question (parties)", "domain": "legal"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="My Company and French Corp",
                description="User answers NDA question",
                expected_state={"commitments": "+1"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="What is the effective date?",
                description="System continues NDA plan",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="The same day I arrive in Paris",
                description="User refers to information from Travel task (cross-domain context)",
                expected_state={"commitments": "+1"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="Understood (Next Monday). What is the duration?",
                description="System resolves context from previous task",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="1 year, mutual NDA, California law",
                description="User volunteers remaining NDA info",
                expected_state={"plan": "complete (NDA)", "commitments": "+3"},
            ),

            # 3. Complete Legal Task
            ScenarioStep(
                speaker="system",
                utterance="""NDA generated successfully for My Company and French Corp.

Now back to your flight booking to Paris. I still need to confirm the return date.""",
                description="System completes NDA, pops plan, resumes Travel task",
                expected_state={
                    "plan": "book_flight (resumed)",
                    "domain": "travel",
                    "qud": "1 question (return_date)"
                },
            ),

            # 4. Resume Travel Task
            ScenarioStep(
                speaker="user",
                utterance="I'll return the following Friday",
                description="User provides return date",
                expected_state={"commitments": "+1"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="Flight booked: SFO to Paris, Mon-Fri. Confirmation #FLT123.",
                description="System completes Travel plan",
                expected_state={"plan": "complete (Travel)", "actions": "booked"},
                is_payoff=True,
            ),
        ],
    )
