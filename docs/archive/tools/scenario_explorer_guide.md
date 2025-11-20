# Interactive Scenario Explorer Guide

The Scenario Explorer is an interactive tool for experiencing and analyzing IBDM dialogue behaviors. Unlike the free-form demo, the Explorer guides you through curated scenarios while allowing you to test "what if" deviations.

## Quick Start

Run the explorer:

```bash
python examples/demo_scenario_explorer.py
```

Select a scenario from the menu to begin.

## Available Scenarios

The explorer includes scenarios showcasing various IBDM features:

| Scenario | Focus | Features Demonstrated |
|----------|-------|-----------------------|
| **Incremental Questioning** | IBiS-3 | Rule 4.2 (LocalQuestionAccommodation), incremental QUD raising |
| **Volunteer Information** | IBiS-3 | Rule 4.1 (IssueAccommodation), skipping answered questions |
| **Clarification** | IBiS-3 | Rule 4.3 (IssueClarification), handling invalid/ambiguous input |
| **Dependent Questions** | IBiS-3 | Rule 4.4 (DependentIssueAccommodation), prerequisite ordering |
| **Reaccommodation** | IBiS-3 | Rules 4.6-4.8, belief revision and dependency cascading |
| **Customer Service** | **Showcase** | Policy-based troubleshooting, frustration detection, escalation |
| **Multi-Domain** | **Showcase** | Seamless switching between Travel and Legal domains |
| **Grounding (Various)** | IBiS-2 | Different grounding strategies (optimistic, cautious, pessimistic) |
| **Action Execution** | IBiS-4 | Action confirmation, execution, and rollback |

## How to Use

### 1. Turn-by-Turn Interaction

At each dialogue turn, the system presents you with options:

```
1. [Expected] I need to draft an NDA
   Say: "I need to draft an NDA"
   → Scenario continues as expected

2. [Distractor] Invalid answer → System asks for clarification
   Say: "blue"
   → System detects invalid answer, generates clarification question (Rule 4.3)

3. [Distractor] Volunteer info → System removes from issues
   Say: "I need an NDA for Acme Corp"
   → System integrates parties immediately
```

- **Option 1** always follows the "happy path" of the scenario.
- **Other options** (distractors) let you test the system's robustness and flexibility.
- **Custom Input**: Type `custom` to enter your own text and test unscripted behavior.

### 2. Visualizing State

After each turn, the system displays the **Information State**:

```
Current Dialogue State (Turn 1):
======================================================================
📚 QUD Stack (1 active):
   ► 1. ?x.draft_nda_task(x)

🔒 Private Issues (4 pending):
   • ?parties.nda_parties
   • ?type.nda_type
   • ?date.effective_date
   ... and 1 more

🤝 Shared Commitments (0 facts):
   (None)
======================================================================
```

This shows you exactly what the system is thinking:
- **QUD**: What question is currently under discussion (top of stack).
- **Private Issues**: Questions planned but not yet raised (IBiS-3).
- **Commitments**: Information that has been grounded and agreed upon.

### 3. Live Monitoring (Advanced)

For a deeper view, you can run the **Live Monitor** in a separate terminal window. This provides a real-time, auto-updating view of the full state structure.

**Terminal 1 (Monitor):**
```bash
python scripts/live_monitor.py
```

**Terminal 2 (Explorer):**
```bash
python examples/demo_scenario_explorer.py
```

As you make choices in the Explorer, the Monitor instantly updates to reflect the new state.

### 4. HTML Reports

Every turn generates an HTML report (`state_turn_X.html`) in the current directory. These reports contain:
- Color-coded state diffs (showing exactly what changed from the previous turn)
- Full state snapshots
- Collapsible JSON views of complex objects

Open these in your browser to analyze the dialogue state offline.

## Commands

Inside the explorer, you can use these commands:

- `/state`: Re-display the current state visualization
- `/path`: Show your current trajectory vs. the expected path
- `/help`: Show help message
- `/quit`: Exit the explorer

## Understanding the Logic

The Explorer demonstrates the **IBDM Core Loop**:

1.  **Interpret**: Your choice is converted into a Dialogue Move (e.g., `user:answer("Acme")`).
2.  **Integrate**: The move updates the Information State (e.g., adds "Acme" to commitments, pops QUD).
3.  **Select**: The system selects the next action based on the updated state (e.g., select `ask(?date)`).
4.  **Generate**: The action is converted into natural language (e.g., "What is the effective date?").

By choosing distractors, you can see how the **Integration** and **Selection** rules adapt to unexpected input (e.g., by raising clarification questions or skipping redundant questions).
