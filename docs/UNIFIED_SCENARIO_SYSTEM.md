# Unified Scenario System

**Status**: ✅ CURRENT (2025-11-20)

Complete guide to the unified JSON-based scenario system for IBDM demonstrations.

---

## Overview

The unified scenario system provides a clean, consistent way to define, load, and execute dialogue scenarios. All scenarios are stored as JSON files in `demos/scenarios/` and can be run with a simple CLI tool.

**Key Components**:
- **JSON Scenarios** (`demos/scenarios/*.json`) - Scenario definitions
- **ScenarioLoader** (`src/ibdm/demo/scenario_loader.py`) - Loads and validates scenarios
- **ScenarioRunner** (`src/ibdm/demo/scenario_runner.py`) - Executes scenarios with rich formatting
- **CLI Tool** (`scripts/run_scenario.py`) - Command-line interface

---

## Quick Start

```bash
# List all available scenarios
python scripts/run_scenario.py --list

# Run a scenario in auto mode (default)
python scripts/run_scenario.py nda_basic

# Run in step mode (press Enter to advance)
python scripts/run_scenario.py nda_basic --step

# Search for scenarios
python scripts/run_scenario.py --search grounding

# Run with custom delay
python scripts/run_scenario.py nda_basic --delay 1.0

# Run with minimal output
python scripts/run_scenario.py nda_basic --minimal
```

---

## JSON Scenario Format

### Complete Example

```json
{
  "scenario_id": "nda_basic",
  "title": "NDA Basic - Happy Path Demo",
  "description": "Demonstrates incremental question-answer dialogue",
  "business_narrative": "Shows how IBDM efficiently gathers all required information...",
  "larsson_algorithms": [
    "Task Accommodation (Section 2.5.1)",
    "Question Accommodation (Rule 4.1)",
    "QUD Stack Management (Section 2.4.2)"
  ],
  "expected_outcomes": {
    "turns": 6,
    "qud_depth_max": 1,
    "commitments_final": 5,
    "plan_completion": "100%",
    "larsson_fidelity": "95%"
  },
  "confidence_mode": "heuristic",
  "metrics": {
    "dialogue_efficiency": "100% - No wasted turns",
    "information_completeness": "100% - All 5 required fields gathered"
  },
  "turns": [
    {
      "turn": 1,
      "speaker": "user",
      "utterance": "I need to draft an NDA",
      "move_type": "request",
      "business_explanation": "User initiates the task with a simple command",
      "larsson_rule": "Task Accommodation - System infers a plan",
      "state_changes": {
        "plan_created": "nda_drafting with 5 subplans",
        "issues_added": ["legal_entities", "nda_type", "date", "time_period", "jurisdiction"]
      },
      "is_payoff": false
    },
    {
      "turn": 2,
      "speaker": "system",
      "utterance": "What are the parties to the NDA?",
      "move_type": "ask",
      "business_explanation": "System asks the first question from its plan",
      "larsson_rule": "Rule 5.1 - Raise issue from private.issues to shared.qud",
      "state_changes": {
        "qud_pushed": "?x.legal_entities(x)"
      }
    }
  ]
}
```

### Required Fields

**Metadata** (top-level):
- `scenario_id` (string) - Unique identifier
- `title` (string) - Human-readable title
- `description` (string) - Brief description
- `business_narrative` (string) - Business value explanation
- `larsson_algorithms` (array of strings) - Larsson rules/algorithms used
- `expected_outcomes` (object) - Expected metrics
- `turns` (array of turn objects) - Dialogue turns

**Optional Metadata**:
- `confidence_mode` (string) - Grounding strategy (default: "heuristic")
- `metrics` (object) - Quality metrics

**Turn Fields** (required):
- `turn` (number) - Turn number (1-indexed)
- `speaker` (string) - "user" or "system"
- `utterance` (string) - What they say
- `move_type` (string) - Type of dialogue move

**Turn Fields** (optional but recommended):
- `business_explanation` (string) - What this demonstrates
- `larsson_rule` (string) - Which Larsson rule applies
- `state_changes` (object) - Expected state changes
- `is_payoff` (boolean) - Whether this is a high-value output turn (default: false)

---

## Using ScenarioLoader

### Basic Usage

```python
from ibdm.demo import ScenarioLoader, load_scenario

# Method 1: Use convenience function
scenario = load_scenario("nda_basic")

# Method 2: Create loader instance
loader = ScenarioLoader()
scenario = loader.load_scenario("nda_basic")

# List all scenarios
scenarios = loader.list_scenarios()
print(f"Available scenarios: {scenarios}")

# List by category
categories = loader.list_scenarios_by_category()
for category, scenario_ids in categories.items():
    print(f"{category}:")
    for sid in scenario_ids:
        print(f"  - {sid}")

# Search scenarios
matches = loader.search_scenarios("grounding")
print(f"Grounding scenarios: {matches}")
```

### Accessing Scenario Data

```python
scenario = load_scenario("nda_basic")

# Metadata
print(scenario.title)
print(scenario.metadata.description)
print(scenario.metadata.business_narrative)
print(scenario.metadata.larsson_algorithms)

# Turns
print(f"Total turns: {scenario.total_turns}")
print(f"User turns: {len(scenario.user_turns)}")
print(f"System turns: {len(scenario.system_turns)}")
print(f"Payoff turns: {len(scenario.payoff_turns)}")

# Access specific turn
turn = scenario.get_turn(1)
if turn:
    print(f"Turn 1: {turn.speaker} says '{turn.utterance}'")

# Iterate through turns
for turn in scenario.turns:
    print(f"[{turn.speaker}] {turn.utterance}")
```

### Validation

```python
loader = ScenarioLoader()
is_valid, issues = loader.validate_scenario("nda_basic")

if is_valid:
    print("Scenario is valid!")
else:
    print("Issues found:")
    for issue in issues:
        print(f"  - {issue}")
```

---

## Using ScenarioRunner

### Basic Usage

```python
from ibdm.demo import ScenarioRunner, ExecutionMode, load_scenario

# Load scenario
scenario = load_scenario("nda_basic")

# Create runner with default settings (auto mode)
runner = ScenarioRunner(scenario)
runner.run()

# Run in step mode
from ibdm.demo import ExecutionController
controller = ExecutionController(mode=ExecutionMode.STEP)
runner = ScenarioRunner(scenario, controller=controller)
runner.run()

# Run with custom options
runner = ScenarioRunner(
    scenario,
    show_explanations=True,
    show_state_changes=True,
    show_larsson_rules=True,
    show_metrics=True
)
runner.run()
```

### Execution Modes

**STEP Mode** - Manual advancement:
```python
controller = ExecutionController(mode=ExecutionMode.STEP)
# User must press Enter to advance each turn
```

**AUTO Mode** - Automatic advancement:
```python
controller = ExecutionController(
    mode=ExecutionMode.AUTO,
    auto_delay=2.0  # 2 seconds between turns
)
```

**REPLAY Mode** - Instant playback:
```python
controller = ExecutionController(mode=ExecutionMode.REPLAY)
# No delays, plays instantly
```

### Customizing Display

```python
# Hide detailed information
runner = ScenarioRunner(
    scenario,
    show_explanations=False,
    show_state_changes=False,
    show_larsson_rules=False,
    show_metrics=False
)

# Minimal output
runner = ScenarioRunner(
    scenario,
    show_explanations=False,
    show_state_changes=False,
    show_larsson_rules=False
)
```

### Convenience Function

```python
from ibdm.demo import run_scenario, ExecutionMode

# Simple usage
run_scenario("nda_basic")

# With options
run_scenario(
    "nda_basic",
    mode=ExecutionMode.STEP,
    auto_delay=1.5,
    show_explanations=True
)
```

---

## CLI Tool Usage

The `run_scenario.py` script provides a complete command-line interface.

### List Scenarios

```bash
# List all scenarios grouped by category
python scripts/run_scenario.py --list

# Output:
# IBiS-3 (Question Accommodation)
#   • ibis3_clarification
#   • ibis3_dependent_questions
#   ...
#
# IBiS-2 (Grounding)
#   • ibis2_grounding_cautious
#   ...
```

### Search Scenarios

```bash
# Search by keyword
python scripts/run_scenario.py --search grounding

# Output:
# Scenarios matching 'grounding':
#   • ibis2_grounding_cautious
#   • ibis2_grounding_mixed
#   ...
```

### Run Scenarios

```bash
# Auto mode (default) - 2 second delays
python scripts/run_scenario.py nda_basic

# Step mode - press Enter to advance
python scripts/run_scenario.py nda_basic --step

# Replay mode - instant playback
python scripts/run_scenario.py nda_basic --replay

# Custom delay
python scripts/run_scenario.py nda_basic --delay 1.0

# Minimal output
python scripts/run_scenario.py nda_basic --minimal
```

### Help

```bash
python scripts/run_scenario.py --help
```

---

## Creating New Scenarios

### 1. Create JSON File

Create `demos/scenarios/my_scenario.json`:

```json
{
  "scenario_id": "my_scenario",
  "title": "My Scenario Title",
  "description": "Brief description",
  "business_narrative": "Business value explanation",
  "larsson_algorithms": [
    "Relevant Larsson rules"
  ],
  "expected_outcomes": {
    "turns": 4,
    "qud_depth_max": 1
  },
  "turns": [
    {
      "turn": 1,
      "speaker": "user",
      "utterance": "User input",
      "move_type": "request",
      "business_explanation": "What this shows",
      "larsson_rule": "Which rule applies",
      "state_changes": {}
    },
    {
      "turn": 2,
      "speaker": "system",
      "utterance": "System response",
      "move_type": "ask",
      "business_explanation": "System asks for info",
      "larsson_rule": "Rule 5.1",
      "state_changes": {
        "qud_pushed": "?x.entity(x)"
      }
    }
  ]
}
```

### 2. Validate Scenario

```python
from ibdm.demo import ScenarioLoader

loader = ScenarioLoader()
is_valid, issues = loader.validate_scenario("my_scenario")

if not is_valid:
    for issue in issues:
        print(f"Issue: {issue}")
```

### 3. Test Scenario

```bash
python scripts/run_scenario.py my_scenario --replay
```

### Best Practices

1. **Use descriptive IDs**: `ibis3_clarification` not `scenario1`
2. **Include business narratives**: Explain why this scenario matters
3. **Document Larsson rules**: Reference specific thesis sections
4. **Mark payoff turns**: Set `is_payoff: true` for high-value outputs
5. **Add state changes**: Show expected state modifications
6. **Test thoroughly**: Run in all execution modes

---

## Scenario Categories

Scenarios are automatically categorized by ID prefix:

| Prefix | Category |
|--------|----------|
| `ibis3_*` | IBiS-3 (Question Accommodation) |
| `ibis2_*` | IBiS-2 (Grounding) |
| `nda_*` or `legal_*` | Business Demos |
| Other | Other |

---

## Architecture

### Component Overview

```
demos/scenarios/*.json  ← Scenario definitions (JSON)
        ↓
ScenarioLoader          ← Loads and validates
        ↓
Scenario object         ← In-memory representation
        ↓
ScenarioRunner          ← Executes with formatting
        ↓
ExecutionController     ← Controls timing/flow
        ↓
Rich Console            ← Professional output
```

### Class Hierarchy

- `ScenarioMetadata` - Scenario metadata
- `ScenarioTurn` - Single dialogue turn
- `Scenario` - Complete scenario with metadata and turns
- `ScenarioLoader` - Loads scenarios from JSON
- `ScenarioRunner` - Executes scenarios with rich output
- `ExecutionController` - Controls execution flow (step/auto/replay)

---

## Testing

Comprehensive test coverage:

- `tests/unit/test_scenario_loader.py` - 18 tests for loading
- `tests/unit/test_scenario_runner.py` - 22 tests for execution

Run tests:

```bash
python -m pytest tests/unit/test_scenario_loader.py -v
python -m pytest tests/unit/test_scenario_runner.py -v
```

---

## Migration from Old System

**Before** (Python-based scenarios):
- Scenarios defined in `src/ibdm/demo/scenarios.py`
- Multiple format variations
- Difficult to create new scenarios

**After** (JSON-based):
- Scenarios defined in `demos/scenarios/*.json`
- Unified format
- Easy to create and modify

**Archived Documentation**:
- `docs/archive/scenario-specs/` - Old scenario specs
- `docs/archive/tools/` - Old execution guides

---

## Troubleshooting

### Scenario Not Found

```
FileNotFoundError: Scenario 'foo' not found.
```

**Solution**: Check available scenarios with `python scripts/run_scenario.py --list`

### Invalid JSON

```
ValueError: Invalid JSON in demos/scenarios/foo.json
```

**Solution**: Validate JSON syntax (use `python -m json.tool < file.json`)

### Missing Required Fields

```
ValueError: Missing required fields: ['turns']
```

**Solution**: Ensure all required fields are present (see JSON Scenario Format section)

---

## References

- **Code**: `src/ibdm/demo/scenario_loader.py`, `src/ibdm/demo/scenario_runner.py`
- **Tests**: `tests/unit/test_scenario_loader.py`, `tests/unit/test_scenario_runner.py`
- **CLI**: `scripts/run_scenario.py`
- **Scenarios**: `demos/scenarios/*.json`
- **Design**: `docs/execution_controller_design.md`

---

**Questions or issues?** File an issue or check `docs/INDEX.md` for more documentation.
