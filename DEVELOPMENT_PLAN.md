# Issue-Based Dialogue Management: Development Plan

## Overview

This document outlines the implementation of Staffan Larsson's Issue-Based Dialogue Management (IBDM) system in Python, using Burr for finite state control and designed for multi-agent dialogue from the outset.

**Reference**: Larsson, S. (2002). Issue-based Dialogue Management. PhD thesis, Göteborg University.

---

## 1. Theoretical Foundation

### 1.1 Core Concept: Questions Under Discussion (QUD)

The central idea of IBDM is that dialogue is driven by **issues** (modeled as questions) that participants collaboratively address. The Questions Under Discussion (QUD) stack represents the current focus of the dialogue.

**Key Principles:**
- Issues are raised explicitly or implicitly through dialogue moves
- Issues can be addressed through answers or actions
- Issues can be resolved (answered) or abandoned
- QUD forms a stack structure (LIFO) representing dialogue focus
- Sub-issues can be raised to address prerequisites for resolving parent issues

### 1.2 Information State Approach

The Information State (IS) represents all relevant information about the dialogue at any point. It is updated through **update rules** triggered by **dialogue moves**.

**Information State Update Pattern:**
```
Observation → Interpretation → Update → Selection → Generation
```

---

## 2. Data Structures

### 2.1 Information State Record (ISR)

The ISR is a structured record containing multiple components:

#### Core Components:

1. **PRIVATE** - Information private to one agent
   - `plan`: Stack of dialogue plans/goals
   - `agenda`: Ordered list of immediate actions to perform
   - `bel`: Private beliefs about the world
   - `lu`: Latest utterance (what agent last said)

2. **SHARED** - Information mutually believed to be shared
   - `qud`: Stack of Questions Under Discussion
   - `com`: Shared commitments (propositions agreed upon)
   - `lu`: Latest move from dialogue partner

3. **CONTROL** - Dialogue management state
   - `speaker`: Current speaker
   - `next_speaker`: Who should speak next
   - `initiative`: Who has dialogue initiative

#### Question Representation:

Questions in QUD are represented semantically, not as strings:

```python
Question types:
- Wh-questions: ?x.P(x)  # "What is X such that P(X)?"
- Y/N questions: ?P      # "Is P true?"
- Alt-questions: ?{P1, P2, ..., Pn}  # "Which of these is true?"
```

### 2.2 Dialogue Moves

Dialogue moves are the atomic units of communication:

**Move Types:**
- `ask(Q)`: Raise question Q
- `answer(A)`: Provide answer A to top QUD
- `assert(P)`: Commit to proposition P
- `request(A)`: Request action A
- `greet`, `quit`: Social/structural moves
- `icm`: Interactive communication management (feedback, grounding)

### 2.3 Plans and Actions

Plans represent dialogue goals and the actions needed to achieve them:

```python
Plan types:
- findout(Q): Goal to find answer to Q
- raise(Q): Goal to raise Q in dialogue
- respond(Q): Goal to respond to Q
- perform(A): Goal to execute action A
```

### 2.4 Accommodation

Accommodation allows the system to handle implicit information and adapt to user needs:

**Types:**
1. **Question Accommodation**: Understanding questions not explicitly in domain
2. **Task Accommodation**: Inferring user's task from their questions
3. **Answer Accommodation**: Interpreting elliptical or partial answers

---

## 3. Control Mechanisms

### 3.1 Update Rules

Update rules are condition-action pairs that modify the information state:

```
IF <preconditions on IS>
THEN <effects on IS>
```

**Rule Categories:**

1. **Interpretation Rules**: Map utterances → dialogue moves
   - Input: Recognized utterance + context
   - Output: Interpreted dialogue move

2. **Integration Rules**: Update IS based on moves
   - `ask(Q)` → push Q onto QUD
   - `answer(A)` → integrate A, potentially pop QUD
   - `assert(P)` → add P to shared commitments

3. **Selection Rules**: Choose next system action
   - Based on: agenda, plans, QUD, obligations
   - Output: Selected dialogue move to perform

4. **Generation Rules**: Produce utterance from move
   - Input: Dialogue move
   - Output: Surface form (text/speech)

### 3.2 Control Algorithm (Dialogue Move Engine)

```
REPEAT:
  1. Observe input (user utterance/action)
  2. Apply interpretation rules → get dialogue move(s)
  3. Apply integration rules → update IS
  4. Apply selection rules → choose next action
  5. Apply generation rules → produce output
  6. Update IS with system's move
UNTIL dialogue ends
```

### 3.3 Grounding and Feedback

Interactive Communication Management (ICM) handles:
- Perception: "I didn't hear that"
- Understanding: "Did you say X?"
- Acceptance: "OK", "I see"
- Clarification: "What do you mean?"

---

## 4. Python Implementation Design

### 4.1 Core Data Structure Classes

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set
from enum import Enum
from abc import ABC, abstractmethod

@dataclass
class Question(ABC):
    """Base class for semantic question representations"""
    @abstractmethod
    def resolves_with(self, answer: 'Answer') -> bool:
        """Check if answer resolves this question"""
        pass

@dataclass
class WhQuestion(Question):
    """Wh-question: ?x.P(x) - What is x such that P(x)?"""
    variable: str
    predicate: str
    constraints: Dict[str, Any] = field(default_factory=dict)

@dataclass
class YNQuestion(Question):
    """Yes/No question: ?P - Is P true?"""
    proposition: str
    parameters: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AltQuestion(Question):
    """Alternative question: ?{P1, P2, ...}"""
    alternatives: List[str]

@dataclass
class Answer:
    """Answer to a question"""
    content: Any  # The actual answer value
    question_ref: Optional[Question] = None  # Which question it answers
    certainty: float = 1.0  # Confidence level

@dataclass
class DialogueMove:
    """Abstract dialogue move"""
    move_type: str
    content: Any
    speaker: str
    timestamp: float = field(default_factory=lambda: time.time())

@dataclass
class Plan:
    """Dialogue plan/goal"""
    plan_type: str  # 'findout', 'raise', 'respond', 'perform'
    content: Any
    status: str = 'active'  # 'active', 'completed', 'abandoned'
    subplans: List['Plan'] = field(default_factory=list)

@dataclass
class PrivateIS:
    """Private information state"""
    plan: List[Plan] = field(default_factory=list)
    agenda: List[DialogueMove] = field(default_factory=list)
    beliefs: Dict[str, Any] = field(default_factory=dict)
    last_utterance: Optional[DialogueMove] = None

@dataclass
class SharedIS:
    """Shared information state"""
    qud: List[Question] = field(default_factory=list)  # Stack (last = top)
    commitments: Set[str] = field(default_factory=set)
    last_moves: List[DialogueMove] = field(default_factory=list)

@dataclass
class ControlIS:
    """Control information"""
    speaker: str = "user"
    next_speaker: str = "system"
    initiative: str = "mixed"
    dialogue_state: str = "active"

@dataclass
class InformationState:
    """Complete information state record"""
    private: PrivateIS = field(default_factory=PrivateIS)
    shared: SharedIS = field(default_factory=SharedIS)
    control: ControlIS = field(default_factory=ControlIS)
    agent_id: str = "system"

    def clone(self) -> 'InformationState':
        """Deep copy of IS for state transitions"""
        import copy
        return copy.deepcopy(self)
```

### 4.2 Update Rule System

```python
from typing import Callable, List, Tuple
from dataclasses import dataclass

@dataclass
class UpdateRule:
    """Information state update rule"""
    name: str
    preconditions: Callable[[InformationState], bool]
    effects: Callable[[InformationState], InformationState]
    priority: int = 0
    rule_type: str = "integration"  # interpretation, integration, selection, generation

class RuleSet:
    """Collection of update rules"""
    def __init__(self):
        self.rules: Dict[str, List[UpdateRule]] = {
            'interpretation': [],
            'integration': [],
            'selection': [],
            'generation': []
        }

    def add_rule(self, rule: UpdateRule):
        self.rules[rule.rule_type].append(rule)
        # Sort by priority
        self.rules[rule.rule_type].sort(key=lambda r: r.priority, reverse=True)

    def apply_rules(self, rule_type: str, state: InformationState) -> InformationState:
        """Apply all applicable rules of given type"""
        current_state = state
        for rule in self.rules[rule_type]:
            if rule.preconditions(current_state):
                current_state = rule.effects(current_state)
        return current_state
```

### 4.3 Dialogue Move Engine

```python
class DialogueMoveEngine:
    """Core dialogue manager implementing IBDM control algorithm"""

    def __init__(self, agent_id: str, rules: RuleSet):
        self.agent_id = agent_id
        self.rules = rules
        self.state = InformationState(agent_id=agent_id)

    def process_input(self, utterance: str, speaker: str) -> Optional[DialogueMove]:
        """Main processing loop"""
        # 1. Interpretation
        moves = self.interpret(utterance, speaker)

        # 2. Integration
        for move in moves:
            self.state = self.integrate(move)

        # 3. Selection
        if self.state.control.next_speaker == self.agent_id:
            response_move = self.select_action()

            # 4. Generation
            if response_move:
                utterance = self.generate(response_move)
                self.state = self.integrate(response_move)
                return response_move

        return None

    def interpret(self, utterance: str, speaker: str) -> List[DialogueMove]:
        """Apply interpretation rules"""
        # This would use NLU + interpretation rules
        # For now, simplified
        pass

    def integrate(self, move: DialogueMove) -> InformationState:
        """Apply integration rules to update state"""
        return self.rules.apply_rules('integration', self.state)

    def select_action(self) -> Optional[DialogueMove]:
        """Apply selection rules to choose next action"""
        # Check agenda first
        if self.state.private.agenda:
            return self.state.private.agenda.pop(0)

        # Then check plans and QUD
        # Apply selection rules
        new_state = self.rules.apply_rules('selection', self.state)
        if new_state.private.agenda:
            return new_state.private.agenda.pop(0)

        return None

    def generate(self, move: DialogueMove) -> str:
        """Apply generation rules to produce utterance"""
        # This would use NLG + generation rules
        pass
```

---

## 5. Burr Integration for Finite State Control

### 5.1 Why Burr?

Burr provides:
- Clear state machine definitions
- State persistence and tracking
- Visualization of dialogue flow
- Composable state transitions
- Built-in action tracking and observability

### 5.2 Burr State Machine Design

```python
from burr.core import State, Action, ApplicationBuilder, when
from burr.core.action import action

# Define states as Burr actions
@action(reads=["information_state", "input"], writes=["information_state", "moves"])
def interpret_input(state: State) -> State:
    """Interpretation action"""
    is_state = state["information_state"]
    utterance = state["input"]

    # Apply interpretation rules
    moves = interpret_utterance(utterance, is_state)

    return state.update(moves=moves)

@action(reads=["information_state", "moves"], writes=["information_state"])
def integrate_moves(state: State) -> State:
    """Integration action"""
    is_state = state["information_state"]
    moves = state["moves"]

    # Apply integration rules
    for move in moves:
        is_state = apply_integration_rules(move, is_state)

    return state.update(information_state=is_state)

@action(reads=["information_state"], writes=["information_state", "selected_move"])
def select_response(state: State) -> State:
    """Selection action"""
    is_state = state["information_state"]

    # Apply selection rules
    move = select_next_move(is_state)

    return state.update(selected_move=move)

@action(reads=["information_state", "selected_move"], writes=["information_state", "output"])
def generate_output(state: State) -> State:
    """Generation action"""
    move = state["selected_move"]

    # Apply generation rules
    utterance = generate_utterance(move)

    return state.update(output=utterance)

# Build application
app = (
    ApplicationBuilder()
    .with_actions(
        interpret=interpret_input,
        integrate=integrate_moves,
        select=select_response,
        generate=generate_output
    )
    .with_transitions(
        ("interpret", "integrate", when(lambda state: state.get("moves"))),
        ("integrate", "select", when(lambda state: state["information_state"].control.next_speaker == "system")),
        ("integrate", "interpret", when(lambda state: state["information_state"].control.next_speaker == "user")),
        ("select", "generate", when(lambda state: state.get("selected_move"))),
        ("generate", "interpret", when(lambda state: True)),
    )
    .with_entrypoint("interpret")
    .with_state(information_state=InformationState())
    .build()
)
```

### 5.3 State Transitions

```
┌─────────────┐
│  interpret  │ ← User input
└──────┬──────┘
       │
       v
┌──────────────┐
│  integrate   │ ← Update IS with moves
└──────┬───────┘
       │
       ├─→ (if user's turn) ─→ interpret
       │
       v
┌──────────────┐
│   select     │ ← Choose system action
└──────┬───────┘
       │
       v
┌──────────────┐
│  generate    │ ← Produce utterance
└──────┬───────┘
       │
       v
    interpret
```

---

## 6. Multi-Agent Architecture

### 6.1 Design Principles

1. **Agent Modularity**: Each agent is an independent dialogue participant
2. **Shared Context**: Agents can access shared QUD and commitments
3. **Private State**: Each agent maintains private beliefs and plans
4. **Coordination**: Agents coordinate through dialogue moves
5. **Roles**: Agents can have specialized roles (info-seeker, info-provider, mediator)

### 6.2 Multi-Agent Structure

```python
from typing import Dict, List
import asyncio

class Agent:
    """Individual dialogue agent"""
    def __init__(self, agent_id: str, role: str):
        self.agent_id = agent_id
        self.role = role
        self.engine = DialogueMoveEngine(agent_id, self._load_rules())

    async def process(self, move: DialogueMove) -> Optional[DialogueMove]:
        """Process incoming move and potentially respond"""
        response = self.engine.process_input(move.content, move.speaker)
        return response

    def _load_rules(self) -> RuleSet:
        """Load role-specific rules"""
        # Different rules based on agent role
        pass

class MultiAgentDialogueSystem:
    """Manages multiple dialogue agents"""

    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.shared_state = SharedIS()
        self.move_queue: asyncio.Queue = asyncio.Queue()

    def add_agent(self, agent: Agent):
        self.agents[agent.agent_id] = agent
        # Link agent to shared state
        agent.engine.state.shared = self.shared_state

    async def broadcast_move(self, move: DialogueMove):
        """Send move to all agents"""
        # Update shared state
        self._update_shared_state(move)

        # Each agent processes the move
        tasks = []
        for agent_id, agent in self.agents.items():
            if agent_id != move.speaker:
                tasks.append(agent.process(move))

        responses = await asyncio.gather(*tasks)

        # Handle responses (may need arbitration)
        return self._arbitrate_responses(responses)

    def _update_shared_state(self, move: DialogueMove):
        """Update shared QUD and commitments based on move"""
        if move.move_type == "ask":
            self.shared_state.qud.append(move.content)
        elif move.move_type == "answer":
            if self.shared_state.qud:
                # Check if answer resolves top QUD
                top_q = self.shared_state.qud[-1]
                if top_q.resolves_with(move.content):
                    self.shared_state.qud.pop()
        # ... more rules

    def _arbitrate_responses(self, responses: List[Optional[DialogueMove]]) -> Optional[DialogueMove]:
        """Decide which agent should respond"""
        # Strategies:
        # - Turn-taking rules
        # - Priority based on role
        # - Relevance to current QUD
        # - Explicit addressing
        valid_responses = [r for r in responses if r is not None]
        if valid_responses:
            return valid_responses[0]  # Simple: first response
        return None
```

### 6.3 Agent Roles and Specialization

```python
class AgentRole(Enum):
    INFO_PROVIDER = "info_provider"
    INFO_SEEKER = "info_seeker"
    TASK_EXECUTOR = "task_executor"
    MEDIATOR = "mediator"
    CLARIFIER = "clarifier"

# Example: Specialized agents
class InfoProviderAgent(Agent):
    """Agent specialized in providing information"""
    def _load_rules(self) -> RuleSet:
        rules = RuleSet()

        # Prioritize answering questions
        rules.add_rule(UpdateRule(
            name="answer_question",
            preconditions=lambda state: len(state.shared.qud) > 0 and self._can_answer(state),
            effects=lambda state: self._generate_answer(state),
            priority=100,
            rule_type="selection"
        ))

        return rules

class InfoSeekerAgent(Agent):
    """Agent specialized in asking questions"""
    def _load_rules(self) -> RuleSet:
        rules = RuleSet()

        # Prioritize asking questions to fulfill plans
        rules.add_rule(UpdateRule(
            name="ask_question",
            preconditions=lambda state: self._has_unanswered_findout(state),
            effects=lambda state: self._raise_question(state),
            priority=100,
            rule_type="selection"
        ))

        return rules
```

---

## 7. Implementation Roadmap

### Phase 1: Core Foundation (Weeks 1-2)
- [ ] Implement basic data structures (Question, Answer, DialogueMove, InformationState)
- [ ] Implement update rule system (UpdateRule, RuleSet)
- [ ] Create basic DialogueMoveEngine
- [ ] Unit tests for data structures
- [ ] Basic serialization/deserialization

### Phase 2: Burr Integration (Week 3)
- [ ] Design Burr state machine for IBDM control loop
- [ ] Implement Burr actions for interpret/integrate/select/generate
- [ ] Define state transitions
- [ ] Add state persistence
- [ ] Visualization of dialogue flow

### Phase 3: Rule Development (Weeks 4-5)
- [ ] Implement interpretation rules
  - Question recognition
  - Answer recognition
  - Command recognition
- [ ] Implement integration rules
  - QUD management (push/pop)
  - Commitment updates
  - Agenda management
- [ ] Implement selection rules
  - Question answering
  - Question raising
  - Clarification
- [ ] Implement generation rules
  - Template-based generation
  - Context-aware generation

### Phase 4: Accommodation (Week 6)
- [ ] Question accommodation mechanisms
- [ ] Task accommodation
- [ ] Answer accommodation (ellipsis handling)
- [ ] Plan inference

### Phase 5: Multi-Agent System (Weeks 7-8)
- [ ] Implement Agent class
- [ ] Implement MultiAgentDialogueSystem
- [ ] Shared state synchronization
- [ ] Turn-taking and arbitration
- [ ] Role-based specialization
- [ ] Agent coordination protocols

### Phase 6: Grounding and ICM (Week 9)
- [ ] Implement grounding mechanisms
- [ ] Interactive communication management
- [ ] Feedback and clarification
- [ ] Error handling and repair

### Phase 7: Integration and Testing (Week 10)
- [ ] End-to-end integration tests
- [ ] Multi-agent dialogue scenarios
- [ ] Performance optimization
- [ ] Documentation
- [ ] Example applications

### Phase 8: Advanced Features (Weeks 11-12)
- [ ] Natural language understanding integration
- [ ] Natural language generation integration
- [ ] Domain-specific knowledge bases
- [ ] Learning and adaptation
- [ ] Dialogue visualization tools

---

## 8. Technology Stack

### Core Dependencies
```
python >= 3.10
burr >= 0.20.0           # State machine and workflow
pydantic >= 2.0          # Data validation
typing-extensions >= 4.8  # Advanced typing
```

### Optional Dependencies
```
# NLU/NLG
transformers >= 4.30     # LLM integration
spacy >= 3.6             # Linguistic processing

# Storage
sqlalchemy >= 2.0        # State persistence
redis >= 4.5             # Session management

# Observability
opentelemetry-api        # Tracing
structlog                # Logging

# Testing
pytest >= 7.4
pytest-asyncio >= 0.21
hypothesis >= 6.82       # Property-based testing
```

---

## 9. Testing Strategy

### Unit Tests
- Data structure validation
- Update rule preconditions and effects
- State transitions
- Question resolution logic

### Integration Tests
- Dialogue move engine processing
- Multi-step conversations
- Accommodation scenarios
- Multi-agent coordination

### Property-Based Tests
- QUD stack invariants
- Information state consistency
- Rule application commutativity (where applicable)

### Dialogue Scenario Tests
- Information seeking dialogues
- Task-oriented dialogues
- Clarification dialogues
- Multi-agent negotiations

---

## 10. Example Use Cases

### 10.1 Information Seeking
```
User: "What's the weather in Stockholm?"
System: [raise ?weather(stockholm) to QUD]
        [plan: findout(?weather(stockholm))]
        "The weather in Stockholm is sunny, 18°C."
        [answer weather(stockholm) = sunny_18c]
        [resolve top QUD]
```

### 10.2 Accommodation
```
User: "When does it close?"
System: [accommodate: what closes? → assume topic from context]
        [raise ?close_time(library) to QUD]
        "The library closes at 8 PM."
```

### 10.3 Multi-Agent Scenario
```
User → System1: "I need to book a flight to Paris"
System1: [specialist: travel agent]
        [raise ?flight(destination=paris) to shared QUD]
        "When would you like to travel?"

User → System1: "Next Tuesday"
System1: [update findout plan with date]
        "Business or economy class?"

System2: [specialist: budget advisor, monitoring]
        [checks user's budget]
        "I notice economy class fits your budget better."

User → System1: "Economy, thanks"
System1: [integrate answer, resolve QUD]
        "I've found flights..."
```

---

## 11. Extension Points

### 11.1 Domain Adaptation
- Custom question types for specific domains
- Domain-specific accommodation rules
- Specialized agent roles

### 11.2 Learning
- Rule learning from dialogue corpora
- Plan adaptation based on success/failure
- User preference learning

### 11.3 Multimodal Extension
- Visual question answering
- Gesture and deixis handling
- Multimodal grounding

### 11.4 Emotion and Social Reasoning
- Politeness strategies
- Emotion recognition and response
- Social commitment tracking

---

## 12. References and Resources

### Primary References
1. Larsson, S. (2002). Issue-based Dialogue Management. PhD thesis, Göteborg University
2. Larsson, S., & Traum, D. R. (2000). Information state and dialogue management in the TRINDI dialogue move engine toolkit
3. Ginzburg, J. (2012). The Interactive Stance: Meaning for Conversation

### Related Work
- Cooper, R., & Larsson, S. (2009). Compositional and distributional models of meaning
- Bos, J., Klein, E., Lemon, O., & Oka, T. (2003). DIPPER: Description and Formalisation of an Information-State Update Dialogue System Architecture

### Tools and Frameworks
- Burr: https://burr.dagworks.io/
- TrindiKit: http://www.ling.gu.se/projekt/trindi/
- GoDiS: https://www.gu.se/en/research/godis-an-accommodating-dialogue-system

---

## Next Steps

1. Set up Python project structure with dependencies
2. Implement core data structures with comprehensive tests
3. Build basic DialogueMoveEngine with simple rules
4. Integrate with Burr for state management
5. Create first multi-agent example
6. Iterate on rule sophistication

This plan provides a solid foundation for implementing a modern, extensible issue-based dialogue management system that honors Larsson's theoretical framework while leveraging contemporary tools like Burr for robust state management.
