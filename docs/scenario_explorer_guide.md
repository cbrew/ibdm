# Interactive Scenario Explorer Guide

**Date**: 2025-11-17
**Status**: ✅ READY TO USE

---

## Overview

The Interactive Scenario Explorer is a choice-based navigation tool that lets you explore IBiS dialogue scenarios interactively. At each dialogue turn, you choose between:

- **Expected move** - Follows the original scenario path
- **Distractors** - Alternative moves that explore different dialogue trajectories

## Quick Start

### Running the Explorer

```bash
# From project root
python -m ibdm.demo.interactive_explorer
```

### What You'll See

1. **Scenario Selection** - Choose from 9 pre-defined scenarios (IBiS-2 and IBiS-3)
2. **Choice Points** - At each user turn, see multiple dialogue options
3. **Trajectory Tracking** - See how your choices diverge from the expected path
4. **State Visualization** - View QUD, issues, and commitments as they change

---

## Features

### Choice Types

At each user turn, you'll see options like:

#### Option 1: [Expected]
- Follows the original scenario path
- ✓ Marked with checkmark
- Completes the scenario as designed

#### Option 2-5: [Distractors]
- Explore alternative dialogue behaviors
- ↻ Marked with loop symbol
- Demonstrate different IBiS rules and mechanisms

### Distractor Categories

The explorer generates these types of distractors:

1. **Invalid Answer** - Triggers clarification mechanism (Rule 4.3)
   - Example: "blue" when asked for parties
   - → System detects invalid, asks for clarification

2. **Nested Question** - User asks for more information
   - Example: "What cities do you fly to?"
   - → Pushes question to QUD stack, answers it, returns

3. **Volunteer Info** - User provides extra facts
   - Example: "Acme Corp and Smith Inc, effective January 1, 2025"
   - → System processes both, skips already-answered questions

4. **Correction** - User changes previous answer
   - Example: "Actually, the effective date should be April 1"
   - → Triggers belief revision (Rules 4.6-4.8)

### Commands

While exploring, you can use these commands:

- `/state` - View current dialogue state (QUD, issues, commitments)
- `/path` - Show trajectory (expected vs. actual path)
- `/help` - Display help information
- `/quit` - Exit explorer

---

## Example Session

```
╔══════════════════════════════════════════════════════════════════════╗
║          IBiS Interactive Scenario Explorer                          ║
╚══════════════════════════════════════════════════════════════════════╝

Available Scenarios:
======================================================================

IBiS-3 Scenarios (Question Accommodation):
  1. Incremental Questioning
     Demonstrates how IBDM asks questions one at a time (Rule 4.2)
  2. Volunteer Information
     Demonstrates multi-fact extraction and question skipping
  ...

Select scenario (1-9) or 'q' to quit: 1

✓ Selected: Incremental Questioning
  Features: Rule 4.1 (IssueAccommodation), Rule 4.2 (LocalQuestionAccommodation)

✓ Domain initialized: NDADomain

======================================================================
Starting Scenario Exploration
======================================================================

──────────────────────────────────────────────────────────────────────
Turn 0 [System]
──────────────────────────────────────────────────────────────────────
system: What are the parties to the NDA?
  (System asks FIRST question (not all 4 at once))

──────────────────────────────────────────────────────────────────────
Turn 1 [User]
──────────────────────────────────────────────────────────────────────
======================================================================
Your dialogue options:
======================================================================

1. [Expected] User answers current question
   Say: "Acme Corp and Smith Inc"
   → Scenario continues as expected

2. [Distractor] Invalid answer → System asks for clarification
   Say: "blue"
   → System detects invalid answer, generates clarification question (Rule 4.3)

3. [Distractor] User asks clarifying question → Pushed to QUD above current question
   Say: "What format should I use for the parties?"
   → System pushes user's question to QUD (stack), answers it, then returns to original question

4. [Distractor] Volunteer info for effective_date → System removes it from issues, skips asking
   Say: "Acme Corp and Smith Inc, effective January 1, 2025"
   → System integrates both answers, removes effective_date from private.issues, skips that question

======================================================================
Choose option (1-4) or type 'custom' for your own response
Commands: /state, /path, /help, /quit
======================================================================

Your choice: 4

✓ You chose: Acme Corp and Smith Inc, effective January 1, 2025
→ System integrates both answers, removes effective_date from private.issues, skips that question

[Simulating move: volunteer_info]
  → Processing volunteer information

Press Enter to continue...
```

---

## Available Scenarios

### IBiS-3 Scenarios (Question Accommodation)

1. **Incremental Questioning**
   - Features: Rule 4.1, Rule 4.2
   - Shows one-question-at-a-time behavior

2. **Volunteer Information**
   - Features: Multi-fact extraction, question skipping
   - Shows how system handles extra information

3. **Clarification Questions**
   - Features: Rule 4.3
   - Shows invalid answer handling

4. **Dependent Questions**
   - Features: Rule 4.4
   - Shows prerequisite ordering

5. **Belief Revision**
   - Features: Rules 4.6-4.8
   - Shows correction handling

### IBiS-2 Scenarios (Grounding)

6. **Optimistic Grounding**
   - High confidence → immediate acceptance
   - No confirmation needed

7. **Cautious Grounding**
   - Medium confidence → confirmation request
   - "Paris, is that correct?"

8. **Pessimistic Grounding**
   - Low confidence → re-utterance
   - "I didn't catch that"

9. **Mixed Grounding**
   - Adaptive strategies throughout dialogue
   - Shows confidence-based selection

---

## Trajectory Tracking

The explorer tracks your path through the scenario:

### Path Display

```
Trajectory Path:
==================================================
✓ 1. [expected] Acme Corp and Smith Inc
↻ 2. [volunteer_info] Acme Corp and Smith Inc, effective January 1, 2025 [DIVERGED]
✓ 3. [expected] 5 years
==================================================
Divergences: 1
Completion: 67% of expected scenario
```

### Status Metrics

- **Total moves** - How many dialogue turns taken
- **Expected moves** - How many followed the expected path
- **Divergences** - How many times you chose a distractor
- **Completion** - Percentage of scenario completed

---

## Understanding the Output

### State Visualization

When you type `/state`, you'll see:

```
======================================================================
Current Dialogue State:
======================================================================
QUD: 1 questions
  1. term = ?

Private Issues: 1 pending
  1. governing_law = ?

Commitments: 2 facts
  - parties(Acme Corp, Smith Inc)
  - effective_date(January 1, 2025)
======================================================================
```

This shows:
- **QUD** - Questions currently being addressed (LIFO stack)
- **Private Issues** - Questions waiting to be raised
- **Commitments** - Facts that have been established

### Move Simulation

When you choose an option, you'll see:

```
[Simulating move: volunteer_info]
  → Processing volunteer information
```

This indicates what IBiS mechanism is being triggered.

---

## Educational Use

The explorer is designed for:

1. **Learning IBiS Algorithms**
   - See how rules apply in real scenarios
   - Understand QUD stack operations
   - Observe belief revision mechanisms

2. **Testing Edge Cases**
   - What happens with invalid answers?
   - How does nested questioning work?
   - When are questions skipped?

3. **Comparing Strategies**
   - Optimistic vs. cautious vs. pessimistic grounding
   - Incremental vs. batch questioning
   - Different error recovery paths

4. **Demonstrating Capabilities**
   - Show IBiS features to stakeholders
   - Explain dialogue management concepts
   - Illustrate Larsson (2002) algorithms

---

## Limitations

### Current Version

This is a **visualization tool**, not a full dialogue engine:

- ✅ Shows scenario structure
- ✅ Generates plausible distractors
- ✅ Tracks trajectory
- ✅ Visualizes state conceptually

- ⚠️ Does NOT actually run dialogue engine
- ⚠️ Does NOT apply full rule sets
- ⚠️ Does NOT execute NLU/NLG

### Future Enhancements

Planned improvements:

1. **Full Engine Integration**
   - Actually run DialogueMoveEngine
   - Apply integration and selection rules
   - Real state updates

2. **Custom Responses**
   - Allow typing arbitrary utterances
   - NLU interpretation
   - Dynamic distractor generation

3. **Branching Visualization**
   - Show tree of possible paths
   - Visualize state differences
   - Compare outcomes

4. **Scenario Authoring**
   - Create custom scenarios
   - Define expected behaviors
   - Test new domains

---

## Tips for Exploration

### For Learning

1. **Start with Expected Path**
   - Run through scenario once with all expected moves
   - Understand the "happy path" behavior

2. **Explore One Distractor at a Time**
   - Try each distractor type separately
   - See how system handles each case

3. **Use /state Frequently**
   - Check QUD, issues, commitments at each turn
   - Understand state transformations

4. **Compare Trajectories**
   - Run same scenario with different choices
   - See how paths diverge

### For Teaching

1. **Use Incremental Questioning First**
   - Shows core IBiS3 concept clearly
   - Easy to understand

2. **Demonstrate Volunteer Info Next**
   - Impressive user experience improvement
   - Clear before/after comparison

3. **Show Grounding Strategies**
   - Different confidence levels
   - Adaptation in action

4. **Advanced: Belief Revision**
   - Shows sophisticated capability
   - Demonstrates robustness

---

## Troubleshooting

### Import Errors

```bash
# Make sure you're in the project root
cd /path/to/ibdm

# Reinstall if needed
uv pip install --system -e ".[dev]"
```

### Scenario Not Displaying Correctly

- Check that all scenario files are present
- Verify domains are properly configured
- Try restarting Python interpreter

### Type Errors

```bash
# Run type checking
pyright src/ibdm/demo/
```

---

## Technical Details

### Architecture

**Files**:
- `src/ibdm/demo/scenario_explorer.py` - Core explorer classes
- `src/ibdm/demo/interactive_explorer.py` - CLI implementation
- `src/ibdm/demo/scenarios.py` - Scenario definitions

**Key Classes**:
- `ScenarioExplorer` - Main explorer logic
- `DistractorGenerator` - Creates alternative moves
- `TrajectoryTracker` - Tracks path through scenario
- `InteractiveExplorerCLI` - User interface

### Design Philosophy

**Visualization Over Execution**:
- Focus on understanding scenario structure
- Show what WOULD happen, not execute full engine
- Educational tool, not production system

**Extensible**:
- Easy to add new distractor types
- Simple to create new scenarios
- Clear integration points for full engine

---

## Related Documentation

- **Scenario Documentation**:
  - `docs/ibis1_demo_scenarios.md`
  - `docs/ibis2_demo_scenarios.md`
  - `docs/ibis3_demo_scenarios.md`

- **Scenario Execution**: `docs/SCENARIO_EXECUTION_GUIDE.md`

- **IBiS Implementation**:
  - `IBIS_PROGRESSION_GUIDE.md`
  - `docs/ibis3_implementation.md`

---

## Contributing

To add new scenarios or distractor types:

1. **New Scenarios**: Add to `src/ibdm/demo/scenarios.py`
2. **New Distractors**: Extend `DistractorGenerator` class
3. **New Features**: Update `ChoiceOption` and `MoveCategory`

---

**Enjoy exploring the scenarios! 🚀**

For questions or issues, create a task with beads:
```bash
bd create "Scenario Explorer: [your question]"
```
