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

## Next Steps

1. Read the full [Development Plan](DEVELOPMENT_PLAN.md)
2. Explore the [Project Structure](PROJECT_STRUCTURE.md)
3. Start implementing core data structures in `src/ibdm/core/`
4. Write tests as you go in `tests/unit/`
5. Build simple examples in `examples/`

## Further Reading

- **Larsson (2002)**: The foundational PhD thesis
- **Ginzburg (2012)**: Theoretical background on QUD and dialogue semantics
- **Burr Documentation**: https://burr.dagworks.io/ for understanding the state machine integration
- **GoDiS Papers**: Look for papers on the GoDiS system for implementation insights

Happy building!
