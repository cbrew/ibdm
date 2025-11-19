# IBDM State Visualization System

The IBDM visualization system provides powerful tools for inspecting, debugging, and understanding the dialogue state during development and demonstration. It offers multiple ways to view the Information State, from beautiful terminal output to rich HTML reports and real-time monitoring.

## Overview

The system consists of three main components:

1.  **Terminal Visualizer**: Beautiful console output using the `rich` library.
2.  **HTML/SVG Exporter**: High-fidelity static reports with state diffs and diagrams.
3.  **Real-Time Monitor**: Live state tracking in a separate process.

## 1. Terminal Visualizer

The `TerminalVisualizer` renders the Information State directly to the console with color-coding and layout organization.

### Usage

```python
from ibdm.visualization.terminal import TerminalVisualizer
from ibdm.visualization.state_snapshot import StateSnapshot

# Create visualizer
visualizer = TerminalVisualizer()

# Render current state
snapshot = StateSnapshot.from_state(state, timestamp=1, label="Turn 1")
visualizer.render_snapshot(snapshot)

# Render diff between states
diff = compute_diff(prev_snapshot, curr_snapshot)
visualizer.render_diff(diff)
```

### Features
- **Rich Panels**: Organized layout separating Shared vs. Private state.
- **QUD Stack**: Visual representation of Questions Under Discussion.
- **Plan Tree**: Hierarchical view of active plans and subplans.
- **Color-Coded Diffs**: Green for additions, red for removals, yellow for modifications.

## 2. HTML & SVG Export

For deeper analysis and documentation, the system can generate standalone HTML reports containing SVGs for complex structures.

### Usage

```python
from ibdm.visualization.html_export import HtmlExporter

exporter = HtmlExporter()

# Export single snapshot
html = exporter.export_snapshot(snapshot)
with open("snapshot.html", "w") as f:
    f.write(html)

# Export timeline (sequence of states)
html = exporter.export_timeline(history_snapshots)
with open("timeline.html", "w") as f:
    f.write(html)
```

### Capabilities
- **State Snapshots**: Full view of all state components.
- **Diff Visualization**: Highlighted changes between turns.
- **Collapsible Timeline**: View the entire dialogue history in a single file.
- **SVG Diagrams**:
    - **Plan Trees**: Graphviz visualizations of plan hierarchy.
    - **QUD Stacks**: Visual stack representation.

## 3. Real-Time Monitor

The monitor allows you to watch the dialogue state evolve in real-time in a separate terminal window, keeping your main interaction clean.

### How to Use

**1. Start the Monitor** (in a separate terminal):
```bash
python scripts/live_monitor.py
```

**2. Run your Application**:
Your application must publish state updates. The `ScenarioExplorer` does this automatically.

```bash
python examples/demo_scenario_explorer.py
```

### Programmatic Usage

To add monitoring to your own application:

```python
from ibdm.visualization.monitor import StatePublisher
from ibdm.visualization.state_snapshot import StateSnapshot

publisher = StatePublisher()

# In your loop:
snapshot = StateSnapshot.from_state(state, timestamp, label)
publisher.publish(snapshot)
```

### Architecture
- **File-Based Pub/Sub**: Uses an atomic file write (`.ibdm_monitor_state.json`) to pass data between processes.
- **Decoupled**: The monitor process is completely independent of the main application.
- **Safe**: Failures in monitoring do not affect the main application.

## 4. State Diff Engine

Underlying the visualization is a powerful `DiffEngine` that computes semantic differences between states.

```python
from ibdm.visualization.diff_engine import compute_diff

diff = compute_diff(state_before, state_after)

if diff.has_changes():
    print(diff.summary)  # e.g. "3 changes: qud +1, beliefs ~1"
    print(diff.get_changed_field("qud").added_items)
```

This engine powers the "changed fields" highlighting in both Terminal and HTML views.
