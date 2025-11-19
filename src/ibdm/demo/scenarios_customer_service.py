from ibdm.demo.scenarios import DemoScenario, ScenarioStep


def scenario_customer_service_escalation() -> DemoScenario:
    """Showcase scenario demonstrating customer service escalation.

    Shows how the system attempts to resolve an issue using policy rules,
    but escalates to a human agent (simulated action) when necessary.
    """
    return DemoScenario(
        name="Customer Service Escalation",
        description=(
            "Showcase: Customer service troubleshooting, policy application, and escalation logic"
        ),
        features=[
            "Troubleshooting workflow",
            "Policy-based decision making",
            "Sentiment/Frustration handling",
            "Escalation action",
        ],
        confidence_mode="optimistic",
        steps=[
            # 1. Issue Identification
            ScenarioStep(
                speaker="user",
                utterance="My order arrived damaged and I want a refund",
                description="User reports issue with clear intent",
                expected_state={"plan": "process_return", "domain": "customer_service"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="I'm sorry to hear that. What is your order number?",
                description="System starts return process",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="ORD-99283",
                description="User provides order number",
                expected_state={"commitments": "+1"},
            ),

            # 2. Information Gathering (Troubleshooting/Verification)
            ScenarioStep(
                speaker="system",
                utterance="Can you describe the damage?",
                description="System gathers details for policy check",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="The box was crushed and the screen is cracked",
                description="User provides damage details",
                expected_state={"commitments": "+1"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="Do you have photos of the damage?",
                description="System asks for evidence (required by policy)",
                expected_state={"qud": "1 question"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Yes, I have them",
                description="User confirms evidence",
                expected_state={"commitments": "+1"},
            ),

            # 3. Policy Application (Attempt 1)
            ScenarioStep(
                speaker="system",
                utterance=(
                    "Based on the damage, I can offer a replacement unit shipped immediately. "
                    "Would you accept a replacement?"
                ),
                description="System proposes solution based on policy (Replacement > Refund)",
                expected_state={"iun": "1 option (replacement)"},
            ),

            # 4. Rejection & Escalation Trigger
            ScenarioStep(
                speaker="user",
                utterance="No! I told you I want a refund! This is taking too long!",
                description="User rejects proposal with frustration",
                expected_state={"iun": "0", "sentiment": "frustrated"},
            ),

            # 5. Escalation Action
            ScenarioStep(
                speaker="system",
                utterance=(
                    "I understand your frustration. Since you prefer a refund, I need to "
                    "escalate this to a specialist for approval. Should I connect you now?"
                ),
                description="System detects rejection + frustration -> Triggers escalation action",
                expected_state={"qud": "1 question (confirmation)", "actions": "escalate_ticket"},
            ),
            ScenarioStep(
                speaker="user",
                utterance="Yes, connect me",
                description="User confirms escalation",
                expected_state={"actions": "1 executing"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="Escalating Ticket #TKT-8821 to Senior Support Team...",
                description="System executes escalation action",
                expected_state={"action_result": "success"},
            ),
            ScenarioStep(
                speaker="system",
                utterance="""
═══════════════════════════════════════════════════════════════════════
                    ESCALATION CONFIRMED
═══════════════════════════════════════════════════════════════════════
Ticket ID:         TKT-8821
Status:            ✓ ESCALATED to Tier 2 Support
Priority:          HIGH (Customer Frustration detected)

Case Details:
  Order:           ORD-99283
  Issue:           Damaged Item (Crushed box, cracked screen)
  Evidence:        Photos available
  Customer Ask:    Refund
  System Offer:    Replacement (Rejected)

Transferring context to human agent...
Current Wait Time: < 1 minute
═══════════════════════════════════════════════════════════════════════""",
                description="System confirms escalation and hands off context",
                expected_state={"plan": "complete (escalated)"},
                is_payoff=True,
            ),
        ],
    )
