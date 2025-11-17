# Path Explorer Guide

**Date**: 2025-11-17
**Status**: ✅ CURRENT

---

## Overview

The **Path Explorer** is an exhaustive dialogue path analysis tool that uses breadth-first search to explore all possible paths through a scenario up to a configurable depth. Unlike the [Interactive Scenario Explorer](INTERACTIVE_SCENARIO_EXPLORER.md) which lets you choose paths interactively, the Path Explorer automatically discovers and analyzes **all possible trajectories**.

### Use Cases

- **Testing Distractor Behaviors** - Verify all alternative moves work correctly
- **Understanding State Transitions** - See how different choices affect dialogue state
- **Validating Scenario Logic** - Ensure all paths lead to reasonable states
- **Coverage Analysis** - Identify which choices are exercised and how often

---

## Quick Start

### Running the CLI

```bash
# From project root
python -m ibdm.demo.explore_paths
```

### What You'll See

1. **Scenario Selection** - Choose from 12 scenarios (IBiS-2, IBiS-3, IBiS-4)
2. **Depth Configuration** - Set maximum depth (default: 3, recommend ≤5)
3. **Automatic Exploration** - BFS explores all paths
4. **Results & Visualization** - Summary reports and tree visualizations

---

## Features

### Exhaustive Path Exploration

The explorer uses **breadth-first search (BFS)** to systematically explore all possible dialogue paths:

```
Root (Initial State)
  ├─ Choice 1 → State A
  │  ├─ Choice 1.1 → State A1
  │  └─ Choice 1.2 → State A2
  ├─ Choice 2 → State B
  │  ├─ Choice 2.1 → State B1
  │  └─ Choice 2.2 → State B2
  └─ Choice 3 → State C
     └─ ...
```

### Depth Control

**Configurable depth** - Default is 3, but can be set to any positive integer:

```python
# Depth 1: Root + 1 level of choices
# Depth 2: Root + 2 levels of choices
# Depth 3: Root + 3 levels of choices (default)
# Depth 5+: Warning - may generate thousands of paths
```

**Growth is exponential**: If each turn has ~4 choices:
- Depth 3: ~64 paths
- Depth 4: ~256 paths
- Depth 5: ~1,024 paths
- Depth 6: ~4,096 paths

### Path Metrics

The explorer tracks:

1. **Total Paths Explored** - How many dialogue trajectories exist
2. **Unique States Reached** - How many distinct dialogue states
3. **State Convergence** - When different paths lead to the same state
4. **Coverage Metrics**:
   - Unique choices exercised
   - Expected vs. distractor path counts
   - Total choices made across all paths

---

## Using the CLI

### Example Session

```
======================================================================
  IBiS Path Explorer - Exhaustive Dialogue Path Analysis
======================================================================

Available Scenarios:
----------------------------------------------------------------------

IBiS-3 Scenarios (Question Accommodation):
  1. Incremental Questioning
  2. Volunteer Information
  3. Clarification Questions
  4. Dependent Questions
  5. Belief Revision (Reaccommodation)

IBiS-2 Scenarios (Grounding & Feedback):
  6. Optimistic Grounding
  7. Cautious Grounding
  8. Pessimistic Grounding
  9. Mixed Grounding Strategies

IBiS-4 Scenarios (Action-Oriented Dialogue):
  10. Action Confirmation
  11. Negotiation with Alternatives
  12. Action Rollback
----------------------------------------------------------------------

Select scenario (1-12) or 'q' to quit: 1

Maximum depth (default: 3, recommend ≤5): 3

✓ Selected: Incremental Questioning
✓ Max depth: 3

✓ Domain: NDA

Exploring all paths up to depth 3...
This may take a few seconds for depth 3...

✓ Exploration complete!
  - Total paths: 64
  - Unique states: 42

Display Options:
  1. Summary report
  2. Tree visualization (depth 1)
  3. Tree visualization (depth 2)
  4. Tree visualization (full depth)
  5. Exit

Select option: 1
```

### Summary Report

Option 1 shows a comprehensive analysis:

```
======================================================================
  Path Exploration Report: Incremental Questioning
  Max Depth: 3
======================================================================

Summary
----------------------------------------------------------------------
Total paths explored: 64
Unique states reached: 42
State convergence instances: 8

Coverage
----------------------------------------------------------------------
Unique choices exercised: 12
Expected path choices: 3
Distractor choices: 61
Total choices made: 64

Paths by Depth
----------------------------------------------------------------------

Depth 0: 1 path(s)
  [root] commitments: 0, qud: 0

Depth 1: 4 path(s)
  [1] commitments: 1, qud: 0
  [2] commitments: 0, qud: 1
  [3] commitments: 2, qud: 0
  [4] commitments: 1, qud: 1

Depth 2: 16 path(s)
  [1→1] commitments: 2, qud: 0
  [1→2] commitments: 1, qud: 1
  [1→3] commitments: 3, qud: 0
  [1→4] commitments: 2, qud: 1
  ... and 12 more paths

Depth 3: 43 path(s)
  [1→1→1] commitments: 3, qud: 0
  [1→1→2] commitments: 2, qud: 1
  [1→1→3] commitments: 4, qud: 0
  ... and 40 more paths

State Convergence
----------------------------------------------------------------------
Found 8 state(s) reached by multiple paths

State 1: 3 paths converge
  - Path: 1→2→1
  - Path: 3→1→1
  - Path: 4→2→1

State 2: 2 paths converge
  - Path: 1→3→2
  - Path: 2→1→3

...

======================================================================
```

### Tree Visualization

Options 2-4 show tree structure at different depths:

```
Path Tree: Incremental Questioning
======================================================================

root
├── [1] expected: "Acme Corp and Smith Inc" (C:1)
│   ├── [1→1] expected: "Mutual" (C:2)
│   │   └── [1→1→1] expected: "January 1, 2025" (C:3)
│   ├── [1→2] invalid_answer: "blue" (C:1)
│   │   └── [1→2→1] expected: "Mutual" (C:2)
│   ├── [1→3] volunteer_info: "Acme Corp and Smith Inc, effective January 1, 2025" (C:2)
│   │   └── [1→3→1] expected: "Mutual" (C:3)
│   └── [1→4] nested_question: "What format should I use?" (C:1)
│       └── [1→4→1] expected: "Mutual" (C:2)
├── [2] invalid_answer: "blue" (C:0)
│   ├── [2→1] expected: "Acme Corp and Smith Inc" (C:1)
│   └── [2→2] invalid_answer: "red" (C:0)
├── [3] volunteer_info: "Acme Corp and Smith Inc, effective January 1, 2025" (C:2)
│   └── [3→1] expected: "Mutual" (C:3)
└── [4] nested_question: "What is an NDA?" (C:0)
    └── [4→1] expected: "Acme Corp and Smith Inc" (C:1)

======================================================================

Legend:
  C:N = Number of commitments at this state
  [path_id] = Unique path identifier
  category: "utterance" = Choice type and text
```

---

## Python API

### Basic Usage

```python
from ibdm.demo.path_explorer import (
    PathExplorer,
    generate_exploration_report,
    generate_tree_visualization,
)
from ibdm.demo.scenarios import scenario_incremental_questioning
from ibdm.domains.nda_domain import get_nda_domain

# Setup
scenario = scenario_incremental_questioning()
domain = get_nda_domain()

# Create explorer
explorer = PathExplorer(scenario, domain)

# Explore paths (default depth=3)
result = explorer.explore_paths(max_depth=3)

# Generate reports
report = generate_exploration_report(result)
print(report)

tree = generate_tree_visualization(result, max_depth=2)
print(tree)
```

### Advanced Usage

```python
# Explore deeper (warning: exponential growth!)
result = explorer.explore_paths(max_depth=5)

print(f"Total paths: {result.total_paths}")
print(f"Unique states: {len(result.unique_states)}")

# Access paths by depth
for depth, paths in result.paths_by_depth.items():
    print(f"Depth {depth}: {len(paths)} paths")
    for path in paths:
        print(f"  Path {path.path_id}: {len(path.get_path_choices())} choices")

# Find convergent states (multiple paths → same state)
for state_sig, nodes in result.state_convergence.items():
    if len(nodes) > 1:
        print(f"State reached by {len(nodes)} paths:")
        for node in nodes:
            choices = " → ".join(node.get_path_choices())
            print(f"  {node.path_id}: {choices}")

# Check coverage
metrics = result.coverage_metrics
print(f"Unique choices: {metrics['unique_choices']}")
print(f"Expected paths: {metrics['expected_paths']}")
print(f"Distractor paths: {metrics['distractor_paths']}")
```

### API Reference

#### `PathExplorer`

**Constructor**:
```python
PathExplorer(scenario: DemoScenario, domain: Any)
```

**Methods**:
```python
def explore_paths(self, max_depth: int = 3) -> ExplorationResult:
    """Explore all dialogue paths up to specified depth.

    Args:
        max_depth: Maximum depth to explore (default: 3).
            Can be any positive integer. Note that path count grows
            exponentially - depth 5+ may generate thousands of paths.

    Returns:
        ExplorationResult with all explored paths and metrics
    """
```

#### `ExplorationResult`

**Attributes**:
```python
@dataclass
class ExplorationResult:
    scenario_name: str                                      # Name of explored scenario
    max_depth: int                                          # Maximum depth explored
    total_paths: int                                        # Total number of paths
    paths_by_depth: dict[int, list[PathNode]]              # Paths organized by depth
    unique_states: set[frozenset[tuple[str, Any]]]         # Unique state signatures
    state_convergence: dict[frozenset, list[PathNode]]     # Paths that converged
    coverage_metrics: dict[str, Any]                       # Coverage statistics
```

#### `PathNode`

**Attributes**:
```python
@dataclass
class PathNode:
    depth: int                           # How many user choices deep (0 = initial)
    step_index: int                      # Current position in scenario
    choice_made: ChoiceOption | None     # The choice that led to this node
    state_snapshot: dict[str, Any]       # Snapshot of dialogue state
    parent: PathNode | None              # Parent node in tree
    path_id: str                         # String representation (e.g., "1→3→2")
    children: list[PathNode]             # Child nodes
```

**Methods**:
```python
def get_path_choices(self) -> list[str]:
    """Get the sequence of choices that led to this node."""

def get_state_signature(self) -> frozenset[tuple[str, Any]]:
    """Get a hashable signature of the dialogue state."""
```

#### Utility Functions

```python
def generate_exploration_report(result: ExplorationResult) -> str:
    """Generate a human-readable exploration report."""

def generate_tree_visualization(result: ExplorationResult, max_depth: int = 2) -> str:
    """Generate a tree visualization of explored paths."""
```

---

## Understanding the Results

### Path Identification

Each path has a unique ID showing the sequence of choices:
- `"root"` - Initial state (no choices yet)
- `"1"` - First choice from root
- `"1→3"` - First choice, then third choice
- `"1→3→2"` - First, third, then second choice

### State Snapshots

Each node captures dialogue state:
```python
state_snapshot = {
    "commitments": {"parties(Acme Corp, Smith Inc)", "effective_date(Jan 1, 2025)"},
    "qud_size": 1,      # How many questions on QUD
    "issues_size": 2,   # How many questions in private.issues
}
```

### State Convergence

**Important concept**: Different dialogue paths can lead to the **same dialogue state**.

Example:
```
Path A: Expected answer → Expected answer
Path B: Invalid answer → Clarification → Valid answer

Both paths may converge to:
  commitments: {parties(...), effective_date(...)}
  qud_size: 1
  issues_size: 2
```

This is **normal and expected** - it shows the system's robustness. Multiple dialogue trajectories can achieve the same informational state.

### Coverage Metrics

- **unique_choices**: How many distinct user utterances were exercised
- **expected_paths**: Paths that followed the original scenario
- **distractor_paths**: Paths that explored alternatives
- **total_choices**: Total number of choices made across all paths

High distractor coverage indicates thorough testing of edge cases and alternative behaviors.

---

## Available Scenarios

### IBiS-3 Scenarios (5 scenarios)

1. **Incremental Questioning** - One question at a time (Rule 4.2)
2. **Volunteer Information** - User provides extra facts
3. **Clarification Questions** - Handle unclear answers (Rule 4.3)
4. **Dependent Questions** - Prerequisite ordering (Rule 4.4)
5. **Belief Revision** - User changes previous answer (Rules 4.6-4.8)

### IBiS-2 Scenarios (4 scenarios)

6. **Optimistic Grounding** - High confidence → immediate acceptance
7. **Cautious Grounding** - Medium confidence → confirmation
8. **Pessimistic Grounding** - Low confidence → re-utterance
9. **Mixed Grounding** - Adaptive strategies throughout dialogue

### IBiS-4 Scenarios (3 scenarios)

10. **Action Confirmation** - System requests confirmation before executing
11. **Negotiation with Alternatives** - Present alternatives, handle acceptance/rejection
12. **Action Rollback** - Handle action failures and rollback

---

## Comparison: Path Explorer vs. Interactive Explorer

| Feature | Path Explorer | Interactive Explorer |
|---------|---------------|---------------------|
| **Exploration Mode** | Automatic (BFS) | Manual (user-driven) |
| **Coverage** | Exhaustive (all paths) | Single path per run |
| **Depth** | Configurable (1-∞) | Full scenario length |
| **Output** | Reports + visualizations | Step-by-step choices |
| **Use Case** | Testing & analysis | Learning & demonstration |
| **Time** | Seconds to minutes | Minutes (interactive) |
| **Paths Generated** | 10s to 1000s | 1 per session |

**When to use each**:
- **Path Explorer**: Testing, validation, coverage analysis, discovering edge cases
- **Interactive Explorer**: Learning, teaching, demonstrating features, exploring specific scenarios

---

## Best Practices

### Depth Selection

**Recommended depths by scenario**:
- **IBiS-2 scenarios**: Depth 2-3 (grounding is usually shallow)
- **IBiS-3 scenarios**: Depth 3-4 (question sequences are moderate)
- **IBiS-4 scenarios**: Depth 2-3 (action sequences are typically short)

**Warning signs you're going too deep**:
- Exploration takes more than 10 seconds
- Path count exceeds 1,000
- Memory usage increases significantly

### Performance Optimization

```python
# Start with depth 1 to understand scenario structure
result = explorer.explore_paths(max_depth=1)
print(f"Depth 1: {result.total_paths} paths")

# Incrementally increase depth
result = explorer.explore_paths(max_depth=2)
print(f"Depth 2: {result.total_paths} paths")

# If reasonable, go to depth 3
if result.total_paths < 100:
    result = explorer.explore_paths(max_depth=3)
    print(f"Depth 3: {result.total_paths} paths")
```

### Analyzing Results

**Key questions to ask**:

1. **Path Count**: Is the number reasonable? Explosive growth suggests too many distractors.

2. **State Convergence**: Do different paths converge to same states? This indicates robustness.

3. **Coverage**: Are all expected paths present? Are distractors well-distributed?

4. **Unique States**: Do we reach substantially different states? Or are most paths redundant?

---

## Implementation Details

### Algorithm

**Breadth-First Search (BFS)**:
1. Start with root node (initial state)
2. For each node at current depth:
   - Get available choices at that node
   - For each choice:
     - Simulate applying the choice
     - Create child node with new state
     - Add child to queue
3. Continue until max depth reached

**Why BFS, not DFS?**
- Explores level by level (easier to visualize)
- Finds all paths at each depth
- Can stop at any depth
- More intuitive path identification

### State Simulation

**Current implementation** (simplified for demo):
- Extracts commitments from utterances using pattern matching
- Simulates state updates (doesn't run full dialogue engine)
- Captures key state components: commitments, QUD size, issues size

**Future enhancement** (full engine integration):
- Actually run DialogueMoveEngine
- Apply full integration and selection rules
- Use real NLU/NLG for interpretation

### Path Identification

Paths use **arrow notation**:
- `"1→3→2"` means: First choice → Third choice → Second choice
- Compact and human-readable
- Easy to trace back through tree
- Unique identifier for each path

---

## Limitations & Future Work

### Current Limitations

1. **Simplified State Simulation**
   - ⚠️ Does NOT run full dialogue engine
   - ⚠️ Does NOT apply complete rule sets
   - ⚠️ Pattern matching instead of real NLU

2. **Fixed Distractor Generation**
   - Distractors are pre-defined in scenario
   - No dynamic generation based on context
   - Limited distractor types

3. **No Execution Validation**
   - Shows paths, doesn't validate they actually work
   - State updates are simulated, not real

### Planned Enhancements

1. **Full Engine Integration**
   - Run actual DialogueMoveEngine at each step
   - Apply integration and selection rules
   - Real state updates and validation

2. **Dynamic Distractor Generation**
   - Use LLM to generate context-appropriate distractors
   - Automatically discover edge cases
   - Adaptive distractor selection

3. **Execution Validation**
   - Actually execute each path through engine
   - Validate state transitions
   - Detect errors and inconsistencies

4. **Advanced Metrics**
   - Rule coverage (which rules were exercised?)
   - State space analysis (which states are reachable?)
   - Anomaly detection (unexpected states?)

---

## Troubleshooting

### Out of Memory Errors

```bash
# Reduce depth
# Depth 5+ can generate thousands of paths
# Try depth 3 or 4 instead
```

### Exploration Takes Too Long

```bash
# Check path count growth:
python -c "
from ibdm.demo.path_explorer import PathExplorer
from ibdm.demo.scenarios import scenario_incremental_questioning
from ibdm.domains.nda_domain import get_nda_domain

scenario = scenario_incremental_questioning()
domain = get_nda_domain()
explorer = PathExplorer(scenario, domain)

for depth in range(1, 6):
    result = explorer.explore_paths(max_depth=depth)
    print(f'Depth {depth}: {result.total_paths} paths')
    if result.total_paths > 1000:
        print('  → Too many paths, recommend stopping here')
        break
"
```

### Import Errors

```bash
# Make sure you're in project root
cd /path/to/ibdm

# Reinstall if needed
uv pip install --system -e ".[dev]"
```

### Type Errors

```bash
# Run type checking
pyright src/ibdm/demo/path_explorer.py
```

---

## Related Documentation

- **Interactive Explorer**: [INTERACTIVE_SCENARIO_EXPLORER.md](INTERACTIVE_SCENARIO_EXPLORER.md)
- **Scenario Execution**: [SCENARIO_EXECUTION_GUIDE.md](SCENARIO_EXECUTION_GUIDE.md)
- **Scenario Definitions**:
  - [ibis1_demo_scenarios.md](ibis1_demo_scenarios.md)
  - [ibis2_demo_scenarios.md](ibis2_demo_scenarios.md)
  - [ibis3_demo_scenarios.md](ibis3_demo_scenarios.md)
  - [ibis4_demo_scenarios.md](ibis4_demo_scenarios.md)

---

## Technical Reference

### File Locations

**Source**:
- `src/ibdm/demo/path_explorer.py` - Core path exploration engine
- `src/ibdm/demo/explore_paths.py` - CLI implementation
- `src/ibdm/demo/scenarios.py` - Scenario definitions
- `src/ibdm/demo/scenario_explorer.py` - Choice and distractor generation

**Tests**:
- `tests/unit/test_path_explorer.py` - Path explorer tests (if exists)
- `tests/unit/test_demo_scenarios.py` - Scenario definition tests

### Design Philosophy

**Testing Tool Over Production System**:
- Focus on discovering all possible paths
- Emphasis on coverage and analysis
- Educational and validation use cases

**Extensible Architecture**:
- Easy to add new scenarios
- Simple to adjust depth
- Clear integration points for full engine

**Separation of Concerns**:
- Path exploration (this tool)
- Path execution (full engine, separate)
- Path visualization (reports and trees)

---

## Examples

### Example 1: Basic Exploration

```python
from ibdm.demo.path_explorer import PathExplorer, generate_exploration_report
from ibdm.demo.scenarios import scenario_volunteer_information
from ibdm.domains.nda_domain import get_nda_domain

# Setup
scenario = scenario_volunteer_information()
domain = get_nda_domain()
explorer = PathExplorer(scenario, domain)

# Explore
result = explorer.explore_paths(max_depth=3)

# Show report
print(generate_exploration_report(result))
```

### Example 2: Incremental Depth Analysis

```python
from ibdm.demo.path_explorer import PathExplorer
from ibdm.demo.scenarios import scenario_incremental_questioning
from ibdm.domains.nda_domain import get_nda_domain

scenario = scenario_incremental_questioning()
domain = get_nda_domain()
explorer = PathExplorer(scenario, domain)

# Explore incrementally
for depth in range(1, 5):
    result = explorer.explore_paths(max_depth=depth)
    print(f"\nDepth {depth}:")
    print(f"  Paths: {result.total_paths}")
    print(f"  Unique states: {len(result.unique_states)}")
    print(f"  Convergence: {sum(1 for n in result.state_convergence.values() if len(n) > 1)}")
```

### Example 3: Finding Convergent States

```python
from ibdm.demo.path_explorer import PathExplorer
from ibdm.demo.scenarios import scenario_clarification
from ibdm.domains.nda_domain import get_nda_domain

scenario = scenario_clarification()
domain = get_nda_domain()
explorer = PathExplorer(scenario, domain)

result = explorer.explore_paths(max_depth=3)

# Find states reached by multiple paths
print("State Convergence Analysis:")
for state_sig, nodes in result.state_convergence.items():
    if len(nodes) > 1:
        print(f"\n{len(nodes)} paths converge:")
        for node in nodes:
            choices = " → ".join(node.get_path_choices())
            print(f"  [{node.path_id}] {choices}")
```

### Example 4: Coverage Analysis

```python
from ibdm.demo.path_explorer import PathExplorer
from ibdm.demo.scenarios import get_ibis3_scenarios
from ibdm.domains.nda_domain import get_nda_domain

domain = get_nda_domain()

print("IBiS-3 Coverage Analysis:")
print("=" * 70)

for scenario in get_ibis3_scenarios():
    explorer = PathExplorer(scenario, domain)
    result = explorer.explore_paths(max_depth=3)
    metrics = result.coverage_metrics

    print(f"\n{scenario.name}:")
    print(f"  Total paths: {result.total_paths}")
    print(f"  Expected: {metrics['expected_paths']}")
    print(f"  Distractors: {metrics['distractor_paths']}")
    print(f"  Coverage: {metrics['unique_choices']} unique choices")
```

---

**Enjoy exploring! 🚀**

For questions or issues, create a task:
```bash
bd create "Path Explorer: [your question]"
```
