# Issue-Based Dialogue Management (IBDM)

A Python implementation of Staffan Larsson's Issue-Based Dialogue Management framework, using Burr for finite state control and designed for multi-agent dialogue from the ground up.

## Overview

This project implements the Information State approach to dialogue management, where dialogue is driven by **Questions Under Discussion (QUD)** that participants collaboratively raise, address, and resolve.

### Key Features

- **Issue-Based Architecture**: Dialogue managed through a stack of questions under discussion
- **Information State**: Comprehensive state tracking including private beliefs, shared commitments, and dialogue plans
- **Update Rules**: Modular rule system for interpretation, integration, selection, and generation
- **Burr Integration**: Finite state machine control with state persistence and visualization
- **Multi-Agent**: Built-in support for multiple dialogue agents with different roles
- **Accommodation**: Flexible handling of implicit information and user adaptability
- **Grounding**: Interactive communication management for robust dialogue

## Theoretical Foundation

Based on:
- **Larsson, S. (2002)**. *Issue-based Dialogue Management*. PhD thesis, Göteborg University
- **Larsson, S., & Traum, D. R. (2000)**. Information state and dialogue management in the TRINDI dialogue move engine toolkit
- **Ginzburg, J. (2012)**. *The Interactive Stance: Meaning for Conversation*

Inspired by @heatherleaf's PyTrindikit

## Quick Start

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install in development mode
pip install -e ".[dev]"
```

### Basic Example

```python
from ibdm.core import InformationState, WhQuestion
from ibdm.engine import DialogueMoveEngine
from ibdm.rules import RuleSet

# Create dialogue engine
rules = RuleSet()
# ... add rules
engine = DialogueMoveEngine(agent_id="system", rules=rules)

# Process user input
response = engine.process_input("What's the weather in Stockholm?", speaker="user")
```

## Architecture

The system follows the IBDM control loop:

```
┌─────────────┐
│  Interpret  │ ← Parse utterance to dialogue move
└──────┬──────┘
       │
       v
┌──────────────┐
│  Integrate   │ ← Update information state
└──────┬───────┘
       │
       v
┌──────────────┐
│   Select     │ ← Choose next action
└──────┬───────┘
       │
       v
┌──────────────┐
│  Generate    │ ← Produce utterance
└──────────────┘
```

### Core Components

- **Information State**: Complete dialogue context (QUD, plans, commitments, beliefs)
- **Questions**: Semantic representations (Wh-questions, Y/N questions, alternatives)
- **Dialogue Moves**: Atomic communication acts (ask, answer, assert, request, etc.)
- **Plans**: Dialogue goals and strategies (findout, raise, respond, perform)
- **Update Rules**: Condition-action pairs that modify the information state
- **Dialogue Move Engine**: Orchestrates the interpretation-integration-selection-generation cycle

### Multi-Agent System

```python
from ibdm.multi_agent import MultiAgentDialogueSystem, Agent, AgentRole

# Create multi-agent system
system = MultiAgentDialogueSystem()

# Add specialized agents
info_agent = Agent("info_provider", role=AgentRole.INFO_PROVIDER)
seeker_agent = Agent("info_seeker", role=AgentRole.INFO_SEEKER)

system.add_agent(info_agent)
system.add_agent(seeker_agent)

# Agents coordinate through shared QUD and commitments
```

## Documentation

- [Development Plan](DEVELOPMENT_PLAN.md) - Comprehensive implementation roadmap
- [Project Structure](PROJECT_STRUCTURE.md) - Code organization and architecture
- [Theory Guide](docs/theory.md) - Theoretical background and concepts (coming soon)
- [API Documentation](docs/api.md) - Detailed API reference (coming soon)
- [Tutorial](docs/tutorial.md) - Step-by-step tutorial (coming soon)

## Development Status

**Current Phase**: Foundation (Phase 1)

- [x] Project structure
- [x] Development plan
- [ ] Core data structures
- [ ] Update rule system
- [ ] Dialogue Move Engine
- [ ] Burr integration
- [ ] Multi-agent system
- [ ] Accommodation mechanisms
- [ ] Grounding and ICM

See [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md) for the complete roadmap.

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ibdm --cov-report=html

# Run specific test categories
pytest tests/unit
pytest tests/integration
pytest tests/property
```

## Examples

See the `examples/` directory for complete examples:

- `simple_qa.py` - Basic question-answering dialogue
- `task_oriented.py` - Task-oriented dialogue with plans
- `multi_agent_travel.py` - Multi-agent travel booking scenario
- `accommodation_demo.py` - Question and task accommodation

## Contributing

This is a research implementation. Contributions are welcome, especially:

- Additional update rules for different dialogue phenomena
- Domain-specific dialogue applications
- Integration with NLU/NLG systems
- Performance optimizations
- Documentation and examples

## License

MIT License

## References

### Primary Literature

1. Larsson, S. (2002). *Issue-based Dialogue Management*. PhD thesis, Göteborg University.
2. Larsson, S., & Traum, D. R. (2000). Information state and dialogue management in the TRINDI dialogue move engine toolkit. *Natural Language Engineering*, 6(3-4), 323-340.
3. Ginzburg, J. (2012). *The Interactive Stance: Meaning for Conversation*. Oxford University Press.

### Related Systems

- **TrindiKit**: Original toolkit for information state dialogue systems
- **GoDiS**: Göteborg Dialogue System implementing IBDM
- **PyTrindikit**: @heatherleaf's Python implementation
- **Burr**: Modern state machine framework for LLM applications

## Citation

If you use this implementation in your research, please cite:

```bibtex
@software{ibdm2024,
  title = {IBDM: Issue-Based Dialogue Management},
  year = {2024},
  note = {Python implementation of Larsson's framework}
}

@phdthesis{larsson2002issue,
  title={Issue-based dialogue management},
  author={Larsson, Staffan},
  year={2002},
  school={Göteborg University}
}
```

## Contact

For questions, issues, or discussions, please open an issue on GitHub.
