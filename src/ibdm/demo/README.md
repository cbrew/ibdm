# IBDM Interactive Demo

Interactive CLI demonstration of the Issue-Based Dialogue Management (IBDM) system, showcasing IBiS3 question accommodation and IBiS2 grounding features.

## Quick Start

```bash
# Run the demo
python -m ibdm.demo.interactive_demo

# Or from Python
from ibdm.demo import InteractiveDemo

demo = InteractiveDemo()
demo.run()
```

## Features

### IBiS3: Question Accommodation

- **Incremental Questioning (Rule 4.2)**: System asks one question at a time instead of overwhelming the user
- **Volunteer Information Handling**: Processes extra information provided before it's asked for
- **Clarification Questions (Rule 4.3)**: Asks for clarification when answers are unclear
- **Dependent Questions (Rule 4.4)**: Ensures prerequisite questions are answered before dependent ones
- **Belief Revision (Rules 4.6-4.8)**: Handles users changing their mind about previous answers

### IBiS2: Grounding & ICM

- **Confidence-Based Grounding**: Adapts strategy based on confidence scores
- **Optimistic Grounding**: High confidence (0.9+) → immediate acceptance
- **Cautious Grounding**: Medium confidence (0.5-0.7) → understanding confirmation
- **Pessimistic Grounding**: Low confidence (<0.5) → perception check (repetition request)
- **ICM Feedback**: Grounding status tracking through dialogue

### Visualization & Export

- **Dialogue History Tracking**: Complete session recording with metadata
- **State Snapshots**: QUD depth, issues count, commitments, active plans per turn
- **Multiple Export Formats**:
  - JSON: Full dialogue history with all metadata
  - Markdown: Formatted dialogue documentation
  - CSV: Tabular format for data analysis
- **Session Persistence**: Save and load dialogue sessions

## Commands

| Command      | Description                               |
|--------------|-------------------------------------------|
| `/help`      | Show help message                         |
| `/state`     | Toggle internal state display             |
| `/history`   | Show dialogue history                     |
| `/export`    | Export dialogue to JSON/Markdown/CSV      |
| `/load`      | Load and replay a saved dialogue          |
| `/confidence`| Change confidence simulation mode         |
| `/reset`     | Reset the dialogue                        |
| `/quit`      | Exit the demo                             |

## Example Session

```
======================================================================
IBDM Interactive Demo - Issue-Based Dialogue Management
======================================================================

Showcasing:
  - IBiS3: Question Accommodation (incremental questioning, volunteer info)
  - IBiS2: Grounding & ICM (confidence-based grounding strategies)

Commands:
  /help       - Show this help
  /state      - Toggle state display
  /history    - Show dialogue history
  /export     - Export dialogue history
  /load       - Load and replay a saved dialogue
  /confidence - Change confidence mode
  /reset      - Reset the dialogue
  /quit       - Exit the demo

Type your message and press Enter to interact.
======================================================================

system: Hello! I can help you draft an NDA. Just say 'I need to draft an NDA' to get started.

user> I need to draft an NDA

======================================================================
Turn 1
======================================================================
user: I need to draft an NDA
[Confidence: 0.90, Strategy: optimistic]

----------------------------------------------------------------------
Internal State:
----------------------------------------------------------------------
QUD (1 questions):
  1. legal_entities = ?

Private Issues (3 questions pending):
  1. date = ?
  2. time_period = ?
  3. jurisdiction = ?

Commitments: (empty)

Active Plans (1):
  - find_out_nda_details (4 subplans)

Recent Moves (1):
  - user:command [unknown]
----------------------------------------------------------------------

system: What are the parties to the NDA?

user> Acme Corp and Smith Inc, effective January 1, 2025

======================================================================
Turn 2
======================================================================
user: Acme Corp and Smith Inc, effective January 1, 2025
[Confidence: 0.90, Strategy: optimistic]

----------------------------------------------------------------------
Internal State:
----------------------------------------------------------------------
QUD (1 questions):
  1. time_period = ?

Private Issues (1 questions pending):
  1. jurisdiction = ?

Commitments (2 facts):
  - legal_entities: Acme Corp and Smith Inc
  - date: January 1, 2025

Active Plans (1):
  - find_out_nda_details (4 subplans)
----------------------------------------------------------------------

system: What is the duration of confidentiality obligations?
```

**Notice how**:
1. System asks ONE question at a time (incremental questioning)
2. User provides parties AND date (volunteer information)
3. System skips asking for date (already answered)
4. System tracks all state internally (QUD, issues, commitments)

## Confidence Modes

Change confidence simulation mode with `/confidence`:

| Mode         | Confidence | Strategy      | Use Case                    |
|--------------|------------|---------------|-----------------------------|
| heuristic    | Length-based | Varies      | Default, realistic          |
| random       | 0.3-1.0    | Varies        | Testing grounding behavior  |
| optimistic   | 0.9        | Optimistic    | High ASR confidence         |
| cautious     | 0.65       | Cautious      | Medium ASR confidence       |
| pessimistic  | 0.4        | Pessimistic   | Low ASR confidence / noisy  |

## Export Examples

### JSON Export
```json
{
  "session_id": "demo-abc123",
  "start_time": "2025-11-16T10:30:00",
  "end_time": null,
  "turns": [
    {
      "turn_number": 1,
      "timestamp": "2025-11-16T10:30:05",
      "speaker": "user",
      "utterance": "I need to draft an NDA",
      "move_type": "command",
      "confidence": 0.9,
      "grounding_strategy": "optimistic",
      "state_snapshot": {
        "qud_depth": 1,
        "issues_count": 3,
        "commitments_count": 0,
        "active_plans": 1
      }
    }
  ],
  "metadata": {
    "agent_id": "system",
    "user_id": "user",
    "confidence_mode": "heuristic"
  }
}
```

### Markdown Export
```markdown
# Dialogue Session: demo-abc123

**Started:** 2025-11-16T10:30:00

## Session Metadata

- **agent_id:** system
- **user_id:** user
- **confidence_mode:** heuristic

## Dialogue

### Turn 1

**user:** I need to draft an NDA

**Metadata:**
- Move Type: `command`
- Confidence: 0.90
- Grounding: `optimistic`

### Turn 2

**system:** What are the parties to the NDA?

**Metadata:**
- Move Type: `ask`

## Summary

- Total turns: 2
```

### CSV Export
```csv
turn,timestamp,speaker,utterance,move_type,confidence,grounding_strategy
1,2025-11-16T10:30:05,user,"I need to draft an NDA",command,0.90,optimistic
2,2025-11-16T10:30:08,system,"What are the parties to the NDA?",ask,,
```

## Pre-Scripted Scenarios

Use the scenario module to explore specific features:

```python
from ibdm.demo import get_ibis3_scenarios, get_ibis2_scenarios

# Get all IBiS3 scenarios
ibis3_scenarios = get_ibis3_scenarios()

# Get specific scenario
from ibdm.demo import get_scenario
scenario = get_scenario("incremental")

# List all scenarios
from ibdm.demo import list_scenarios
all_scenarios = list_scenarios()
```

Available scenarios:
- `incremental`: Incremental questioning demo
- `volunteer`: Volunteer information handling
- `clarification`: Clarification questions
- `dependent`: Dependent question ordering
- `reaccommodation`: Belief revision
- `grounding-optimistic`: High confidence grounding
- `grounding-cautious`: Medium confidence grounding
- `grounding-pessimistic`: Low confidence grounding
- `grounding-mixed`: Adaptive grounding

## Architecture

```
InteractiveDemo
├── Dialogue Engine
│   ├── Integration Rules (IBiS1, IBiS2, IBiS3)
│   └── Selection Rules
├── Dialogue History
│   ├── Turn Recording
│   ├── State Snapshots
│   └── Metadata Tracking
├── Visualizer
│   ├── Compact Format
│   ├── Detailed Format
│   └── Export (JSON/Markdown/CSV)
└── Domain (NDA)
    ├── Predicates (legal_entities, date, time_period, jurisdiction)
    └── Plans (find_out_nda_details)
```

## API Usage

### Basic Usage

```python
from ibdm.demo import InteractiveDemo

# Create demo instance
demo = InteractiveDemo(
    agent_id="system",
    user_id="user",
    show_state=True,
    show_moves=True,
    confidence_mode="heuristic"
)

# Run interactive loop
demo.run()
```

### Programmatic Usage

```python
from ibdm.demo import InteractiveDemo

# Create demo
demo = InteractiveDemo()

# Process user input
response = demo.process_user_input("I need to draft an NDA")

# Access dialogue history
history = demo.dialogue_history

# Export to file
history.save_to_file("my-dialogue.json")

# Load from file
from ibdm.demo import DialogueHistory
loaded = DialogueHistory.load_from_file("my-dialogue.json")
```

### Visualization

```python
from ibdm.demo import DialogueVisualizer, DialogueHistory

visualizer = DialogueVisualizer(width=70)

# Load dialogue
history = DialogueHistory.load_from_file("dialogue.json")

# Format history
compact = visualizer.format_compact_history(history)
detailed = visualizer.format_history(history, show_metadata=True)
full = visualizer.format_history(history, show_metadata=True, show_state=True)

# Export
markdown = visualizer.export_to_markdown(history)
csv = visualizer.export_to_csv(history)
```

## Troubleshooting

### Issue: Demo doesn't start

**Solution**: Ensure you have all dependencies installed:
```bash
uv pip install --system -e ".[dev]"
```

### Issue: State display shows empty

**Solution**: Toggle state display with `/state` command. It may be turned off.

### Issue: Confidence always shows 0.90

**Solution**: You're in `optimistic` mode. Change with `/confidence` command.

### Issue: Load fails with "File not found"

**Solution**: Check filename is correct. Exported files are named `dialogue-{session_id}.json`.

## Implementation Details

### Confidence Simulation

The demo simulates confidence scores since there's no real ASR system:

- **heuristic**: Length-based (longer = higher confidence)
- **random**: Random between 0.3-1.0
- **optimistic/cautious/pessimistic**: Fixed values for testing

Real deployments would use actual ASR confidence scores.

### Grounding Strategy Selection

Based on `src/ibdm/core/grounding.py`:

```python
def select_grounding_strategy(move_type: str, confidence: float) -> GroundingStrategy:
    """Select grounding strategy based on confidence and move type."""
    evidence_req = get_evidence_requirement(move_type)

    if confidence >= evidence_req.high_threshold:
        return GroundingStrategy.OPTIMISTIC
    elif confidence >= evidence_req.low_threshold:
        return GroundingStrategy.CAUTIOUS
    else:
        return GroundingStrategy.PESSIMISTIC
```

Thresholds vary by move type (e.g., quit=0.9, answer=0.7).

### State Tracking

State snapshots capture:
- **qud_depth**: Number of questions on QUD stack
- **issues_count**: Number of pending questions in private.issues
- **commitments_count**: Number of facts committed to shared state
- **active_plans**: Number of active dialogue plans

## Contributing

To add new demo features:

1. **Add scenarios**: Edit `scenarios.py` to add new DemoScenario instances
2. **Extend visualizer**: Add new format methods to `DialogueVisualizer`
3. **Add commands**: Add new command handlers to `InteractiveDemo.process_command()`

## References

- [Larsson (2002)](../docs/reference/larsson-thesis-2002.pdf): Issue-Based Dialogue Management thesis
- [IBDM Documentation](../README.md): Main IBDM documentation
- [Architecture Principles](../docs/architecture_principles.md): Design philosophy

## License

See [LICENSE](../../../LICENSE) file in repository root.
