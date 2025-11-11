# Issue-Based Dialogue Management - Project Structure

## Directory Layout

```
ibdm/
├── README.md
├── DEVELOPMENT_PLAN.md
├── PROJECT_STRUCTURE.md
├── pyproject.toml
├── setup.py
├── requirements.txt
├── requirements-dev.txt
│
├── src/
│   └── ibdm/
│       ├── __init__.py
│       │
│       ├── core/                    # Core IBDM concepts
│       │   ├── __init__.py
│       │   ├── questions.py         # Question types (Wh, YN, Alt)
│       │   ├── answers.py           # Answer representations
│       │   ├── moves.py             # Dialogue move types
│       │   ├── plans.py             # Plan and goal structures
│       │   └── information_state.py # IS, PrivateIS, SharedIS, ControlIS
│       │
│       ├── rules/                   # Update rule system
│       │   ├── __init__.py
│       │   ├── base.py              # UpdateRule, RuleSet base classes
│       │   ├── interpretation.py    # Interpretation rules
│       │   ├── integration.py       # Integration rules
│       │   ├── selection.py         # Selection rules
│       │   ├── generation.py        # Generation rules
│       │   └── accommodation.py     # Accommodation rules
│       │
│       ├── engine/                  # Dialogue processing engine
│       │   ├── __init__.py
│       │   ├── dialogue_move_engine.py  # Core DME
│       │   ├── interpreter.py       # Utterance → Move
│       │   ├── integrator.py        # Move → IS update
│       │   ├── selector.py          # IS → Action selection
│       │   └── generator.py         # Move → Utterance
│       │
│       ├── burr_integration/        # Burr state machine
│       │   ├── __init__.py
│       │   ├── actions.py           # Burr action definitions
│       │   ├── states.py            # State representations
│       │   ├── transitions.py       # Transition logic
│       │   └── application.py       # Application builder
│       │
│       ├── multi_agent/             # Multi-agent system
│       │   ├── __init__.py
│       │   ├── agent.py             # Base Agent class
│       │   ├── roles.py             # Specialized agent roles
│       │   ├── coordination.py      # Agent coordination
│       │   ├── arbitration.py       # Turn-taking, response selection
│       │   └── system.py            # MultiAgentDialogueSystem
│       │
│       ├── grounding/               # Grounding and ICM
│       │   ├── __init__.py
│       │   ├── icm.py               # Interactive communication management
│       │   ├── feedback.py          # Feedback mechanisms
│       │   └── repair.py            # Error handling and repair
│       │
│       ├── nlu/                     # Natural language understanding
│       │   ├── __init__.py
│       │   ├── parser.py            # Utterance parsing
│       │   ├── semantic_interpreter.py  # Semantic interpretation
│       │   └── intent_recognition.py    # Intent/move type recognition
│       │
│       ├── nlg/                     # Natural language generation
│       │   ├── __init__.py
│       │   ├── templates.py         # Template-based generation
│       │   ├── realizer.py          # Surface realization
│       │   └── aggregation.py       # Content aggregation
│       │
│       ├── persistence/             # State persistence
│       │   ├── __init__.py
│       │   ├── serialization.py     # IS serialization
│       │   ├── storage.py           # Storage backends
│       │   └── session.py           # Session management
│       │
│       └── utils/                   # Utilities
│           ├── __init__.py
│           ├── logging.py           # Logging configuration
│           ├── validation.py        # Data validation
│           └── visualization.py     # Dialogue visualization
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   │
│   ├── unit/
│   │   ├── test_questions.py
│   │   ├── test_answers.py
│   │   ├── test_moves.py
│   │   ├── test_information_state.py
│   │   ├── test_rules.py
│   │   └── test_engine.py
│   │
│   ├── integration/
│   │   ├── test_dialogue_scenarios.py
│   │   ├── test_multi_agent.py
│   │   ├── test_accommodation.py
│   │   └── test_grounding.py
│   │
│   └── property/
│       ├── test_qud_invariants.py
│       └── test_state_consistency.py
│
├── examples/
│   ├── simple_qa.py                 # Simple Q&A dialogue
│   ├── task_oriented.py             # Task-oriented dialogue
│   ├── multi_agent_travel.py        # Multi-agent travel booking
│   └── accommodation_demo.py        # Accommodation examples
│
├── docs/
│   ├── theory.md                    # Theoretical background
│   ├── api.md                       # API documentation
│   ├── tutorial.md                  # Getting started tutorial
│   └── examples.md                  # Example walkthrough
│
└── notebooks/
    ├── 01_core_concepts.ipynb       # Interactive exploration
    ├── 02_rule_development.ipynb
    ├── 03_multi_agent.ipynb
    └── 04_custom_domain.ipynb
```

## Module Descriptions

### Core (`src/ibdm/core/`)
Fundamental data structures representing questions, answers, dialogue moves, plans, and information states. These are the building blocks of the IBDM system.

### Rules (`src/ibdm/rules/`)
The update rule system that drives information state changes. Includes:
- **Interpretation**: Map utterances to dialogue moves
- **Integration**: Update IS based on moves
- **Selection**: Choose next action
- **Generation**: Produce utterances
- **Accommodation**: Handle implicit information

### Engine (`src/ibdm/engine/`)
The Dialogue Move Engine implements the core control loop:
```
Observe → Interpret → Integrate → Select → Generate
```

### Burr Integration (`src/ibdm/burr_integration/`)
Wraps the IBDM engine in Burr's state machine framework for:
- State tracking and persistence
- Transition visualization
- Action observability
- State history

### Multi-Agent (`src/ibdm/multi_agent/`)
Multi-agent dialogue capabilities:
- **Agent**: Individual dialogue participant
- **Roles**: Specialized agent behaviors (info-seeker, info-provider, etc.)
- **Coordination**: Agent communication protocols
- **Arbitration**: Turn-taking and response selection
- **System**: Manages multiple agents

### Grounding (`src/ibdm/grounding/`)
Interactive Communication Management for:
- Perception checking
- Understanding confirmation
- Acceptance feedback
- Clarification requests
- Error repair

### NLU/NLG (`src/ibdm/nlu/`, `src/ibdm/nlg/`)
Natural language interfaces (initially simple, can be extended):
- Parsing and semantic interpretation
- Template-based generation
- Intent recognition
- Surface realization

### Persistence (`src/ibdm/persistence/`)
State management:
- Serialization/deserialization of IS
- Storage backends (memory, file, database)
- Session management
- State history

## Development Workflow

### 1. Initial Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install in development mode
pip install -e ".[dev]"
```

### 2. Development Cycle
```bash
# Run tests
pytest tests/

# Type checking
mypy src/ibdm

# Linting
ruff check src/ibdm
black --check src/ibdm

# Format
black src/ibdm
ruff check --fix src/ibdm
```

### 3. Testing Strategy
- **Unit tests**: Individual components in isolation
- **Integration tests**: Multi-component scenarios
- **Property tests**: Invariant checking with Hypothesis
- **Example tests**: End-to-end dialogue scenarios

## Key Files to Create First

### Phase 1: Core Foundation
1. `src/ibdm/core/questions.py` - Question types
2. `src/ibdm/core/answers.py` - Answer representations
3. `src/ibdm/core/moves.py` - Dialogue moves
4. `src/ibdm/core/information_state.py` - IS structures
5. `tests/unit/test_questions.py` - Question tests
6. `tests/unit/test_information_state.py` - IS tests

### Phase 2: Rules
1. `src/ibdm/rules/base.py` - UpdateRule, RuleSet
2. `src/ibdm/rules/integration.py` - Basic integration rules
3. `tests/unit/test_rules.py` - Rule tests

### Phase 3: Engine
1. `src/ibdm/engine/dialogue_move_engine.py` - Core engine
2. `src/ibdm/engine/integrator.py` - Integration component
3. `tests/integration/test_engine.py` - Engine tests

### Phase 4: Burr
1. `src/ibdm/burr_integration/actions.py` - Burr actions
2. `src/ibdm/burr_integration/application.py` - App builder
3. `examples/simple_qa.py` - First working example

## Configuration Files

### `pyproject.toml`
```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "ibdm"
version = "0.1.0"
description = "Issue-Based Dialogue Management system"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]

dependencies = [
    "burr[cli]>=0.20.0",
    "pydantic>=2.0",
    "typing-extensions>=4.8",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4",
    "pytest-asyncio>=0.21",
    "pytest-cov>=4.1",
    "hypothesis>=6.82",
    "mypy>=1.5",
    "black>=23.7",
    "ruff>=0.0.285",
    "ipython>=8.14",
    "jupyter>=1.0",
]

nlu = [
    "transformers>=4.30",
    "torch>=2.0",
    "spacy>=3.6",
]

storage = [
    "sqlalchemy>=2.0",
    "redis>=4.5",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
addopts = "-v --cov=ibdm --cov-report=term-missing"

[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.black]
line-length = 100
target-version = ['py310']

[tool.ruff]
line-length = 100
target-version = "py310"
select = ["E", "F", "I", "N", "W", "UP"]
ignore = []
```

## Git Workflow

### Branch Strategy
- `main`: Stable releases
- `develop`: Integration branch
- `feature/*`: Feature development
- `bugfix/*`: Bug fixes

### Commit Convention
```
type(scope): description

Types: feat, fix, docs, refactor, test, chore
Scopes: core, rules, engine, burr, agent, etc.

Examples:
feat(core): add WhQuestion and YNQuestion classes
fix(rules): correct QUD pop logic in answer integration
docs(tutorial): add getting started guide
test(engine): add dialogue scenario tests
```

## Next Steps

1. Create basic package structure
2. Implement core data structures with tests
3. Build simple rule system
4. Create minimal DialogueMoveEngine
5. Integrate with Burr
6. Develop first example
7. Iterate and expand

This structure provides a clean, modular architecture that supports incremental development while maintaining the theoretical integrity of Larsson's IBDM framework.
