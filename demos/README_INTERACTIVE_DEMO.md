# IBDM-NLU Interactive Demo

An interactive demonstration of the IBDM-NLU integration for legal document generation (NDA drafting).

## Overview

This demo showcases:
- **Natural Language Understanding**: LLM-based interpretation of user utterances
- **Dialogue Management**: IBDM question-under-discussion (QUD) stack and dialogue moves
- **Entity Extraction**: Recognition of legal entities (organizations, dates, jurisdictions)
- **Task Accommodation**: System infers document requirements from conversation
- **Real-time Metrics**: Token usage, costs, and latency tracking

## Prerequisites

1. **Python 3.10+** with the IBDM package installed
2. **IBDM_API_KEY** environment variable set with your Anthropic Claude API key
3. **Dependencies**: The demo requires the `rich` library for terminal UI

## Installation

```bash
# Install IBDM with development dependencies
uv pip install --system -e ".[dev]"

# Or if using regular pip
pip install -e ".[dev]"
```

## Running the Demo

### Basic Usage

```bash
python demos/03_nlu_integration_interactive.py
```

### With Options

```bash
# Verbose mode (shows detailed NLU processing)
python demos/03_nlu_integration_interactive.py --verbose

# Without colors (for plain terminals)
python demos/03_nlu_integration_interactive.py --no-color

# Help
python demos/03_nlu_integration_interactive.py --help
```

## Sample Conversation

Here's a complete example conversation showing the system in action:

```
╭───────────────────────────────────────────────────────╮
│                                                       │
│  IBDM-NLU Interactive Demo                           │
│  Legal Document Generation: Non-Disclosure Agreement │
│                                                       │
│  Type your messages to interact with the legal       │
│  document system                                     │
│  Type 'quit' or 'exit' to end the session           │
│                                                       │
╰───────────────────────────────────────────────────────╯

✓ API key found

Validating configuration...
  ✓ All modules available
  ✓ Loaded 16 IBDM rules
  ✓ Configuration validated

Configuration:
  • Model: claude-sonnet-4-5-20250929
  • Rules: 16 IBDM rules loaded
  • API Key: IBDM_API_KEY (✓ set)

✓ Burr state machine initialized with NLU engine

Starting Interactive Session

╭────────────────────────────── Legal System ───────────────────────────────╮
│                                                                            │
│  System: Hello! I'm here to help you draft a Non-Disclosure Agreement.    │
│  What would you like to do?                                               │
│                                                                            │
╰────────────────────────────────────────────────────────────────────────────╯


You: I need to draft an NDA

================================================================================
Turn 1
================================================================================

╭───────────────────────────── You (Turn 1) ─────────────────────────────────╮
│                                                                             │
│  I need to draft an NDA                                                    │
│                                                                             │
╰─────────────────────────────────────────────────────────────────────────────╯

 Strategy:  🔴 sonnet
 Tokens:    1234 (617 in / 617 out)
 Cost:      $0.011085
 Latency:   2.145s

✓ Interpreted 1 dialogue move(s)

╭─────────────────────────── Dialogue Move ──────────────────────────────╮
│                                                                         │
│  Move Type: command                                                    │
│  Speaker: user                                                         │
│  Content: I need to draft an NDA                                       │
│                                                                         │
╰─────────────────────────────────────────────────────────────────────────╯

╭────────────────────────────── QUD Stack ───────────────────────────────╮
│                                                                         │
│  QUD Stack (bottom → top)                                              │
│  ❓ WhQuestion(variable='x', predicate='draft_nda_task') (0)          │
│  ❓ WhQuestion(variable='parties', predicate='nda_parties') (TOP)     │
│                                                                         │
╰─────────────────────────────────────────────────────────────────────────╯

╭────────────────────────────── Legal System ────────────────────────────╮
│                                                                         │
│  I'll help you draft an NDA. What are the names of the parties        │
│  entering into this agreement?                                         │
│                                                                         │
╰─────────────────────────────────────────────────────────────────────────╯


You: Between Acme Corporation and TechStart Inc

================================================================================
Turn 2
================================================================================

╭───────────────────────────── You (Turn 2) ─────────────────────────────────╮
│                                                                             │
│  Between Acme Corporation and TechStart Inc                                │
│                                                                             │
╰─────────────────────────────────────────────────────────────────────────────╯

 Strategy:  🔴 sonnet
 Tokens:    1456 (728 in / 728 out)
 Cost:      $0.013104
 Latency:   2.567s

✓ Interpreted 1 dialogue move(s)

╭─────────────────────────── Dialogue Move ──────────────────────────────╮
│                                                                         │
│  Move Type: answer                                                     │
│  Speaker: user                                                         │
│  Content: Answer(content='Between Acme Corporation and TechStart Inc', │
│           addresses_question=WhQuestion(...))                           │
│                                                                         │
╰─────────────────────────────────────────────────────────────────────────╯

╭────────────────────────────── QUD Stack ───────────────────────────────╮
│                                                                         │
│  QUD Stack (bottom → top)                                              │
│  ❓ WhQuestion(variable='x', predicate='draft_nda_task') (0)          │
│  ⚡ AltQuestion(alternatives=['mutual', 'one-way']) (TOP)             │
│                                                                         │
╰─────────────────────────────────────────────────────────────────────────╯

╭────────────────────────────── Legal System ────────────────────────────╮
│                                                                         │
│  Thank you. Should this be a mutual NDA or a one-way NDA?             │
│                                                                         │
╰─────────────────────────────────────────────────────────────────────────╯


You: Make it mutual

================================================================================
Turn 3
================================================================================

╭───────────────────────────── You (Turn 3) ─────────────────────────────────╮
│                                                                             │
│  Make it mutual                                                            │
│                                                                             │
╰─────────────────────────────────────────────────────────────────────────────╯

 Strategy:  🔴 sonnet
 Tokens:    892 (446 in / 446 out)
 Cost:      $0.008028
 Latency:   1.834s

✓ Interpreted 1 dialogue move(s)

╭─────────────────────────── Dialogue Move ──────────────────────────────╮
│                                                                         │
│  Move Type: answer                                                     │
│  Speaker: user                                                         │
│  Content: Answer(content='Make it mutual', addresses_question=...)     │
│                                                                         │
╰─────────────────────────────────────────────────────────────────────────╯

╭────────────────────────────── QUD Stack ───────────────────────────────╮
│                                                                         │
│  QUD Stack (bottom → top)                                              │
│  ❓ WhQuestion(variable='x', predicate='draft_nda_task') (0)          │
│  ❓ WhQuestion(variable='date', predicate='effective_date') (TOP)     │
│                                                                         │
╰─────────────────────────────────────────────────────────────────────────╯

╭────────────────────────────── Legal System ────────────────────────────╮
│                                                                         │
│  Got it. What should the effective date be?                            │
│                                                                         │
╰─────────────────────────────────────────────────────────────────────────╯


You: quit

Ending session...

================================================================================
Session Summary
================================================================================

╭────────────────────────────────────────────────────────────────────────╮
│                                                                        │
│                          Session Metrics                               │
│  ──────────────────────────────────────────────────────────────────  │
│  Metric                                               Value            │
│  ──────────────────────────────────────────────────────────────────  │
│                                                                        │
│  Total Turns                                              3            │
│  Total Tokens                                         3,582            │
│  Total Cost                                      $0.032217            │
│  Avg Latency                                         2.182s            │
│  Total Latency                                       6.546s            │
│                                                                        │
│  Strategy Distribution                                                 │
│    🔴 sonnet                                     3 (100.0%)           │
│                                                                        │
╰────────────────────────────────────────────────────────────────────────╯

✓ Interactive session completed!
Processed 3 turns using claude-sonnet-4-5-20250929
```

## Understanding the Output

### Dialogue Moves

The system displays the interpreted dialogue move for each utterance:

- **command**: User giving an instruction or expressing a need ("I need to...", "I want to...")
- **question**: User asking for information
- **answer**: User providing information in response to a system question
- **assert**: User making a statement

### QUD Stack

The Question Under Discussion (QUD) stack shows:
- **Current focus**: What question is being addressed (shown at TOP)
- **Stack depth**: Previous questions still pending
- **Question types**:
  - ❓ **WhQuestion**: Open-ended questions (who, what, where, when)
  - ✓ **YNQuestion**: Yes/no questions
  - ⚡ **AltQuestion**: Alternative choice questions (A or B?)

### Metrics

For each turn, you'll see:

- **Strategy**: Which approach was used
  - 🔴 **Sonnet**: Claude Sonnet 4.5 (most capable, higher cost)
  - 🟡 **Haiku**: Claude Haiku 4.5 (fast, lower cost)
  - 🟢 **Rules**: Pattern-based rules (free, instant)

- **Tokens**: Number of tokens consumed
  - Format: `total (input / output)`

- **Cost**: Estimated cost in USD
  - Sonnet: $3/million input, $15/million output
  - Haiku: $1/million input, $5/million output

- **Latency**: Time taken to process the utterance

## Tips for Interaction

1. **Be Natural**: The system handles natural language, so speak naturally
   - ✓ "I need to draft an NDA"
   - ✓ "Between Acme Corp and TechStart"
   - ✓ "Make it mutual"

2. **Provide Context**: Give enough information for the system to understand
   - ✓ "Between Acme Corporation as disclosing party and TechStart Inc"
   - ✗ "Acme" (too vague)

3. **Follow the Flow**: The system guides you through required information
   - It asks for parties, type, dates, etc. in a logical order

4. **Exit Anytime**: Type any of these to end the session:
   - `quit`
   - `exit`
   - `bye`
   - `goodbye`

## Verbose Mode

Use `--verbose` to see detailed NLU processing:

```bash
python demos/03_nlu_integration_interactive.py --verbose
```

This shows:
- Dialogue act classification confidence scores
- Entity extraction details
- Semantic parsing results
- Internal reasoning steps

## Troubleshooting

### "IBDM_API_KEY environment variable not found"

Set your Anthropic API key:

```bash
export IBDM_API_KEY='sk-ant-api03-...'
```

Or add it to your `.env` file in the project root.

### "No module named 'rich'"

Install the required dependency:

```bash
uv pip install --system rich
# or
pip install rich
```

### High latency or costs

The demo uses Claude Sonnet 4.5 for high-quality NLU, which can be expensive for long conversations. For cost-sensitive testing:

1. Keep conversations short (3-5 turns)
2. Consider modifying the config to use Haiku for classification
3. Monitor the session summary metrics

## Architecture

The demo integrates several IBDM components:

1. **NLU Engine** (`NLUDialogueEngine`): Interprets user utterances using Claude
2. **Burr State Machine** (`DialogueStateMachine`): Manages dialogue state
3. **IBDM Rules**: Handle question integration, selection, and response generation
4. **Context Interpreter**: Provides semantic understanding and entity extraction

## Next Steps

- Explore the non-interactive demo: `demos/03_nlu_integration_basic.py`
- Read the IBDM documentation: `docs/`
- Review the NLU components: `src/ibdm/nlu/`
- Examine the integration rules: `src/ibdm/rules/integration_rules.py`

## Related Files

- **Demo script**: `demos/03_nlu_integration_interactive.py`
- **Non-interactive version**: `demos/03_nlu_integration_basic.py`
- **NLU engine**: `src/ibdm/engine/nlu_engine.py`
- **Burr integration**: `src/ibdm/burr_integration/`
