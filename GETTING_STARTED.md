# Getting Started with IBDM

## Core Concepts Explained

### 1. Questions Under Discussion (QUD)

The **QUD** is the heart of issue-based dialogue management. Think of it as a stack of questions that drive the conversation forward.

**Example dialogue:**
```
User: "I want to book a flight to Paris"
  → System infers: QUD = [?flight_to_paris]

System: "When would you like to travel?"
  → System raises sub-question: QUD = [?flight_to_paris, ?travel_date]

User: "Next Tuesday"
  → Answer resolves top question
  → QUD = [?flight_to_paris]

System: "What class? Business or economy?"
  → QUD = [?flight_to_paris, ?class]
```

**Key principles:**
- Questions are pushed onto the QUD stack when raised
- Questions are popped when answered/resolved
- The top question represents the current dialogue focus
- Sub-questions can be raised to gather information needed for parent questions

### 2. Information State

The **Information State (IS)** is a complete snapshot of everything known about the dialogue at any moment. It has three main parts:

#### Private Information State
What only this agent knows:
- **plan**: What the agent is trying to achieve
- **agenda**: Immediate actions to perform
- **beliefs**: What the agent believes about the world
- **last_utterance**: What the agent last said

#### Shared Information State
What all participants mutually believe:
- **qud**: Questions under discussion (shared focus)
- **commitments**: Facts/propositions everyone has agreed to
- **last_moves**: Recent dialogue moves from other participants

#### Control Information State
Meta-information about the dialogue:
- **speaker**: Who is currently speaking
- **next_speaker**: Who should speak next
- **initiative**: Who is driving the dialogue

### 3. Dialogue Moves

**Dialogue moves** are the atomic units of communication. Instead of treating utterances as raw text, we interpret them as structured actions:

**Common move types:**
- `ask(Q)`: Raise question Q (adds to QUD)
- `answer(A)`: Provide answer A (may resolve QUD)
- `assert(P)`: Commit to proposition P
- `request(A)`: Request action A
- `greet()`, `quit()`: Social moves
- `icm:*`: Interactive communication management (feedback, clarification)

**Example:**
```python
Utterance: "What's the weather in Stockholm?"
↓
Interpreted as: DialogueMove(
    move_type="ask",
    content=WhQuestion(
        variable="weather",
        predicate="in_location",
        constraints={"location": "Stockholm"}
    ),
    speaker="user"
)
```

### 4. Plans

**Plans** represent dialogue goals and strategies for achieving them:

**Plan types:**
- `findout(Q)`: Goal to find the answer to question Q
- `raise(Q)`: Goal to get Q into the QUD
- `respond(Q)`: Goal to provide an answer to Q
- `perform(A)`: Goal to execute action A

**Plans can have sub-plans:**
```python
Plan(
    type="findout",
    content=?complete_booking,
    subplans=[
        Plan(type="findout", content=?destination),
        Plan(type="findout", content=?dates),
        Plan(type="findout", content=?passengers),
        Plan(type="perform", content=book_flight)
    ]
)
```

### 5. Update Rules

**Update rules** are condition-action pairs that modify the information state:

**Structure:**
```python
IF <conditions on current IS>
THEN <changes to IS>
```

**Four types:**

1. **Interpretation Rules**: Utterance → Dialogue Move
   ```python
   IF utterance contains "what is"
   THEN create WhQuestion move
   ```

2. **Integration Rules**: Dialogue Move → IS Update
   ```python
   IF move is ask(Q)
   THEN push Q onto shared.qud
   ```

3. **Selection Rules**: IS → Action Selection
   ```python
   IF shared.qud is not empty AND can_answer(top_qud)
   THEN agenda.add(answer_move)
   ```

4. **Generation Rules**: Dialogue Move → Utterance
   ```python
   IF move is ask(WhQuestion(var="X", pred="P"))
   THEN utterance = f"What {var} {pred}?"
   ```

### 6. The Control Loop

The dialogue engine runs a continuous cycle:

```
1. OBSERVE: Get user input
2. INTERPRET: Apply interpretation rules → get dialogue moves
3. INTEGRATE: Apply integration rules → update IS with moves
4. SELECT: Apply selection rules → choose system's next action
5. GENERATE: Apply generation rules → produce utterance
6. INTEGRATE: Update IS with system's move
7. REPEAT
```

**Visualization:**
```
User utterance → [Interpret] → Moves
                              ↓
                         [Integrate]
                              ↓
                      Information State
                              ↓
                          [Select]
                              ↓
                      System action
                              ↓
                        [Generate]
                              ↓
                      System utterance
```

### 7. Accommodation

**Accommodation** is how the system handles implicit information:

**Question Accommodation:**
```
User: "When does it close?"
System: [What closes? Check context...]
       [Assume: "the library" from previous context]
       "The library closes at 8 PM"
```

**Task Accommodation:**
```
User: "I need the address"
System: [Infer: user wants ?address(library)]
       [Activate plan: provide_info(?address(library))]
```

**Answer Accommodation (Ellipsis):**
```
System: "Do you want business or economy class?"
User: "Economy"  [Elliptical answer]
System: [Interpret as: answer(?class, economy)]
       [Resolve top QUD]
```

## Practical Example: Building a Weather Dialogue

### Step 1: Define Question Types

```python
from ibdm.core import WhQuestion, YNQuestion

# "What's the weather in X?"
weather_question = WhQuestion(
    variable="weather",
    predicate="in_location",
    constraints={"location": "Stockholm"}
)

# "Will it rain?"
rain_question = YNQuestion(
    proposition="will_rain",
    parameters={}
)
```

### Step 2: Create Information State

```python
from ibdm.core import InformationState, PrivateIS, SharedIS, Plan

state = InformationState(
    private=PrivateIS(
        plan=[
            Plan(type="respond", content=weather_question)
        ],
        beliefs={"current_weather": {"Stockholm": "sunny, 18°C"}}
    ),
    shared=SharedIS(
        qud=[weather_question],
        commitments=set()
    )
)
```

### Step 3: Define Update Rules

```python
from ibdm.rules import UpdateRule, RuleSet

rules = RuleSet()

# Integration rule: When ask(Q), add to QUD
def integrate_ask(state):
    if state.last_move.type == "ask":
        state.shared.qud.append(state.last_move.content)
    return state

rules.add_rule(UpdateRule(
    name="integrate_ask",
    preconditions=lambda s: s.last_move and s.last_move.type == "ask",
    effects=integrate_ask,
    rule_type="integration"
))

# Selection rule: If can answer top QUD, do it
def select_answer(state):
    if state.shared.qud:
        q = state.shared.qud[-1]
        if q.variable == "weather" and q.constraints["location"] in state.private.beliefs["current_weather"]:
            answer = state.private.beliefs["current_weather"][q.constraints["location"]]
            state.private.agenda.append(
                DialogueMove(type="answer", content=answer)
            )
    return state

rules.add_rule(UpdateRule(
    name="select_weather_answer",
    preconditions=lambda s: len(s.shared.qud) > 0,
    effects=select_answer,
    rule_type="selection"
))
```

### Step 4: Create Engine and Process

```python
from ibdm.engine import DialogueMoveEngine

engine = DialogueMoveEngine(agent_id="weather_bot", rules=rules)

# Process user input
response = engine.process_input(
    "What's the weather in Stockholm?",
    speaker="user"
)

# Response: "The weather in Stockholm is sunny, 18°C"
```

## Multi-Agent Example

**Note**: Multi-agent system is planned but not yet implemented. See [LARSSON_PRIORITY_ROADMAP.md](LARSSON_PRIORITY_ROADMAP.md) for status (ibdm-tty epic).

**Planned API** (conceptual):

```python
from ibdm.multi_agent import MultiAgentDialogueSystem, Agent, AgentRole

# Create system
system = MultiAgentDialogueSystem()

# Add travel agent
travel_agent = Agent("travel_agent", role=AgentRole.INFO_PROVIDER)
travel_agent.engine.state.private.beliefs = {
    "flights": [...],
    "hotels": [...]
}

# Add budget advisor
budget_agent = Agent("budget_advisor", role=AgentRole.INFO_PROVIDER)
budget_agent.engine.state.private.beliefs = {
    "user_budget": 1000,
    "price_recommendations": [...]
}

system.add_agent(travel_agent)
system.add_agent(budget_agent)

# User asks question
user_move = DialogueMove(
    type="ask",
    content=WhQuestion(variable="flight", predicate="to_paris"),
    speaker="user"
)

# Both agents process in parallel
# System arbitrates who should respond
response = await system.broadcast_move(user_move)
```

## Key Design Patterns

### 1. Always Think in Terms of Issues

Instead of: "The user wants to book a flight"
Think: "The user has raised the issue ?book_flight which has sub-issues ?destination, ?dates, ?class"

### 2. Make QUD Explicit

Always maintain a clear QUD stack. When confused about what the dialogue is about, check the QUD.

### 3. Use Plans for Proactivity

Don't just react to user input. Maintain plans for what the agent is trying to achieve.

### 4. Accommodate Liberally

When something is unclear, try to infer from context before asking for clarification.

### 5. Track Commitments

Keep track of what's been mutually agreed upon. This prevents redundant questions and enables reference resolution.

## Running the Dialogue State Engine with Scenarios

### Quick Start: Interactive Demo

The easiest way to experience IBDM is through the interactive demo:

```bash
# Basic interactive demo
python -m ibdm.demo.interactive_demo

# With specific confidence mode
python -m ibdm.demo.interactive_demo --confidence optimistic
```

Once running, try:
```
I need to draft an NDA
```

Watch the system demonstrate:
- Task plan formation
- Incremental questioning (one at a time)
- Volunteer information handling
- State visualization

**Available commands in the demo**:
- `/state` - Toggle internal state display
- `/history` - Show complete dialogue history
- `/export json filename.json` - Export session to JSON
- `/export markdown filename.md` - Export to Markdown
- `/confidence optimistic|cautious|pessimistic` - Change grounding mode
- `/quit` - Exit

### Using Pre-Built Scenarios Programmatically

IBDM includes 9+ pre-scripted scenarios demonstrating all capabilities:

```python
from ibdm.demo.scenarios import get_ibis3_scenarios, scenario_incremental_questioning

# List available scenarios
for scenario in get_ibis3_scenarios():
    print(f"- {scenario.name}: {scenario.description}")
    print(f"  Features: {', '.join(scenario.features)}")
    print(f"  Steps: {len(scenario.steps)}")

# Load a specific scenario
scenario = scenario_incremental_questioning()

# View scenario structure
print(f"\nScenario: {scenario.name}")
for i, step in enumerate(scenario.steps, 1):
    print(f"Step {i} [{step.speaker}]: {step.utterance}")
    if step.description:
        print(f"  → {step.description}")
```

### Interactive Scenario Explorer

The **Scenario Explorer** lets you explore scenarios with choice-based navigation:

```python
from ibdm.demo.scenarios import scenario_incremental_questioning
from ibdm.demo.scenario_explorer import ScenarioExplorer
from ibdm.core import InformationState
from ibdm.domains.nda_domain import get_nda_domain

# Load scenario and domain
scenario = scenario_incremental_questioning()
domain = get_nda_domain()

# Create initial state
state = InformationState(agent_id="system")

# Create explorer
explorer = ScenarioExplorer(scenario, state, domain)

# Get available choices for user
choices = explorer.get_current_choices()

# Display choices to user
explorer.display_choices(choices)

# User selects option (e.g., choice 1)
selected = explorer.select_choice("1", choices)
if selected:
    print(f"You chose: {selected.utterance}")
    explorer.tracker.record_choice(selected)

# View current state
explorer.display_state()

# View trajectory (expected vs. actual path)
explorer.display_trajectory()
```

**Choice Types in Explorer**:
- `[Expected]` - Follows the original scenario path
- `[Distractor: Invalid Answer]` - Tests clarification handling
- `[Distractor: Nested Question]` - Tests QUD stack management
- `[Distractor: Volunteer Info]` - Tests multi-fact processing
- `[Distractor: Correction]` - Tests belief revision

### Creating Custom Scenarios

You can create your own scenarios:

```python
from ibdm.demo.scenarios import DemoScenario, ScenarioStep

my_scenario = DemoScenario(
    name="Travel Booking",
    description="Demonstrates incremental information gathering for travel",
    features=["Rule 4.1", "Rule 4.2", "Volunteer information"],
    confidence_mode="optimistic",
    steps=[
        ScenarioStep(
            speaker="user",
            utterance="I want to book a flight",
            description="User initiates travel booking task"
        ),
        ScenarioStep(
            speaker="system",
            utterance="Where would you like to go?",
            description="System asks for destination"
        ),
        ScenarioStep(
            speaker="user",
            utterance="Paris, departing March 15",
            description="User provides destination AND date (volunteer info)"
        ),
        # ... more steps
    ]
)
```

## Visual Monitoring and State Inspection

### Terminal Visualization (In-Process)

For immediate state inspection during development:

```python
from ibdm.visualization.terminal import TerminalVisualizer
from ibdm.visualization.state_snapshot import StateSnapshot

# Create visualizer
visualizer = TerminalVisualizer()

# Capture state snapshot
snapshot = StateSnapshot.from_state(state, timestamp=0, label="Initial State")

# Render to terminal (uses Rich for beautiful output)
visualizer.render_snapshot(snapshot)
```

**What it displays**:
- QUD stack with question details
- Private issues (pending questions)
- Commitments (agreed facts)
- Active plans with subplan hierarchy
- Agenda (next system actions)
- Beliefs (agent's knowledge)

### State Diff Visualization

Compare two states to see what changed:

```python
from ibdm.visualization.diff_engine import compute_diff
from ibdm.visualization.terminal import TerminalVisualizer

# Capture before and after states
before = StateSnapshot.from_state(state_before, 0, "Before")
after = StateSnapshot.from_state(state_after, 1, "After")

# Compute diff
diff = compute_diff(before, after)

# Display diff with color coding
visualizer = TerminalVisualizer()
visualizer.render_diff(diff)
```

**Diff shows**:
- ➕ Added items (green)
- ➖ Removed items (red)
- 🔄 Modified items (yellow)
- ➡️ Unchanged items (dim)

### Real-Time State Monitor (Separate Terminal)

For monitoring a running dialogue session in a separate terminal window:

**Terminal 1 - Run your dialogue**:
```python
from ibdm.demo.scenario_explorer import ScenarioExplorer
from ibdm.visualization.monitor import StatePublisher

explorer = ScenarioExplorer(scenario, state, domain)

# The explorer automatically publishes state updates
# to .ibdm_monitor_state.json
explorer.display_state()  # This triggers publication
```

**Terminal 2 - Monitor state updates**:
```bash
# In a separate terminal window
python scripts/live_monitor.py

# With custom file path
python scripts/live_monitor.py --file /path/to/state.json

# With custom polling interval
python scripts/live_monitor.py --interval 0.5
```

The monitor will:
- Watch the state file for changes
- Auto-refresh when updates occur
- Display full state with Rich formatting
- Show update timestamp

### HTML Report Generation

Generate rich HTML reports for offline analysis:

```python
from ibdm.visualization.html_export import HtmlExporter
from ibdm.visualization.state_snapshot import StateSnapshot

exporter = HtmlExporter()

# Export single snapshot
snapshot = StateSnapshot.from_state(state, 0, "Turn 5")
html = exporter.export_snapshot(snapshot)

with open("state_turn_5.html", "w") as f:
    f.write(html)

# Export rule trace (shows rule evaluation process)
from ibdm.visualization import RuleTrace, RuleEvaluation

trace = RuleTrace(
    phase="integration",
    timestamp=5,
    label="After user answer",
    evaluations=[
        RuleEvaluation("Rule 4.1", priority=1, preconditions_met=True, was_selected=True),
        RuleEvaluation("Rule 4.2", priority=2, preconditions_met=False, was_selected=False),
    ],
    selected_rule="Rule 4.1",
    state_before=before_snapshot,
    state_after=after_snapshot,
    diff=diff
)

trace_html = exporter.export_rule_trace(trace)
with open("trace_turn_5.html", "w") as f:
    f.write(trace_html)
```

**HTML reports include**:
- Formatted state display with syntax highlighting
- Expandable/collapsible sections
- Rule evaluation details with color coding
- Before/after diffs
- Navigation between related snapshots

### Using Visualization in Scenario Explorer

The `ScenarioExplorer` has built-in visualization:

```python
explorer = ScenarioExplorer(scenario, state, domain)

# Commands available during exploration:
# /state  - Show current dialogue state with rich visualization
# /diff   - Show changes from last move
# /trace  - Show rule execution trace
# /path   - Show trajectory (expected vs. actual)
```

The explorer automatically:
- Captures snapshots at each turn
- Generates HTML reports (saved as `state_turn_N.html`)
- Publishes to monitor (if StatePublisher available)
- Tracks rule evaluations

### Quick Visualization Demo

Try the visualization demo:

```bash
# Terminal visualizer demo
python scripts/demo_terminal_viz.py

# HTML export demo
python scripts/demo_html_export.py
```

These create example states and show all visualization capabilities.

## Complete Example: Running and Monitoring a Scenario

Here's a complete example combining scenarios and visualization:

```python
from ibdm.demo.scenarios import scenario_volunteer_information
from ibdm.demo.scenario_explorer import ScenarioExplorer
from ibdm.core import InformationState
from ibdm.domains.nda_domain import get_nda_domain
from ibdm.visualization.terminal import TerminalVisualizer

# 1. Setup
scenario = scenario_volunteer_information()
domain = get_nda_domain()
state = InformationState(agent_id="system")
visualizer = TerminalVisualizer()

# 2. Create explorer
explorer = ScenarioExplorer(scenario, state, domain)

# 3. Main interaction loop
print(f"\nScenario: {scenario.name}")
print(f"Description: {scenario.description}\n")

while not explorer.is_complete():
    # Get user choices
    choices = explorer.get_current_choices()

    if not choices:
        # System turn - advance automatically
        explorer.advance_step()
        continue

    # Display choices
    explorer.display_choices(choices)

    # Get user input
    user_input = input("\nYour choice (or /state, /path, /quit): ").strip()

    # Handle commands
    if user_input == "/state":
        explorer.display_state()
        continue
    elif user_input == "/path":
        explorer.display_trajectory()
        continue
    elif user_input == "/diff":
        explorer.display_diff()
        continue
    elif user_input == "/quit":
        break

    # Process choice
    selected = explorer.select_choice(user_input, choices)
    if selected:
        explorer.tracker.record_choice(selected)
        explorer.capture_snapshot(f"After: {selected.utterance}")
        explorer.advance_step()

# 4. Final summary
print("\n" + "="*70)
print("Scenario Complete!")
print("="*70)
status = explorer.get_trajectory_status()
print(f"Total moves: {status['total_moves']}")
print(f"Expected moves: {status['expected_moves']}")
print(f"Divergences: {status['divergences']}")
print(f"Completion: {status['completion']:.0%}")

# Display final state
print("\nFinal State:")
explorer.display_state()
```

**Start monitoring in another terminal before running**:
```bash
python scripts/live_monitor.py
```

Then run the scenario script and watch the monitor update in real-time!

## Next Steps

**For Understanding the System**:
1. Run the demos in `demos/` to see IBDM in action:
   - `demos/01_core_concepts.py` - See concepts in practice
   - `python -m ibdm.demo.interactive_demo` - Try interactive dialogue
2. Read [SCENARIO_EXECUTION_GUIDE.md](docs/SCENARIO_EXECUTION_GUIDE.md) - Complete scenario guide
3. Read [SYSTEM_ACHIEVEMENTS.md](SYSTEM_ACHIEVEMENTS.md) for current status
4. Review [docs/LARSSON_ALGORITHMS.md](docs/LARSSON_ALGORITHMS.md) for algorithm details

**For Development**:
1. Read [CLAUDE.md](CLAUDE.md) - Development workflow and policies
2. Check [LARSSON_PRIORITY_ROADMAP.md](LARSSON_PRIORITY_ROADMAP.md) for current priorities
3. Explore implemented code in `src/ibdm/`
4. Run tests: `pytest tests/`
5. See [docs/INDEX.md](docs/INDEX.md) for complete documentation

## Further Reading

- **Larsson (2002)**: The foundational PhD thesis
- **Ginzburg (2012)**: Theoretical background on QUD and dialogue semantics
- **Burr Documentation**: https://burr.dagworks.io/ for understanding the state machine integration
- **GoDiS Papers**: Look for papers on the GoDiS system for implementation insights

Happy building!
