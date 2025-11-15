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
# Install dependencies using uv (recommended)
uv pip install --system -e ".[dev]"

# Or using regular pip
pip install -e ".[dev]"
```

See [docs/environment_setup.md](docs/environment_setup.md) for API key configuration.

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

**Note**: Multi-agent system is planned but not yet implemented. See [LARSSON_PRIORITY_ROADMAP.md](LARSSON_PRIORITY_ROADMAP.md) for status.

Planned features:
- Specialized agents with different roles
- Shared QUD and commitment tracking
- Turn-taking and arbitration
- Agent coordination protocols

## Documentation

**Quick Reference**:
- [CLAUDE.md](CLAUDE.md) - **Development guide** (start here for development)
- [GETTING_STARTED.md](GETTING_STARTED.md) - Tutorial and concepts
- [docs/INDEX.md](docs/INDEX.md) - Complete documentation index

**Status & Planning**:
- [SYSTEM_ACHIEVEMENTS.md](SYSTEM_ACHIEVEMENTS.md) - Current implementation status
- [LARSSON_PRIORITY_ROADMAP.md](LARSSON_PRIORITY_ROADMAP.md) - Active roadmap

**Architecture**:
- [docs/architecture_principles.md](docs/architecture_principles.md) - Design principles
- [docs/LARSSON_ALGORITHMS.md](docs/LARSSON_ALGORITHMS.md) - Authoritative algorithms reference

**Historical**:
- [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md) - Original 8-phase plan (historical)
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Ideal structure (historical)

## Development Status

**Current Phase**: Phase 3.5 Complete (LLM-NLU Integration)

- [x] Project structure and core data structures
- [x] Update rule system (interpretation, integration, selection, generation)
- [x] Dialogue Move Engine with Burr integration
- [x] Domain semantic layer (NDA domain)
- [x] LLM-based NLU with Claude 4.5 Sonnet/Haiku
- [x] Entity extraction and reference resolution
- [x] Task plan formation and accommodation
- [ ] Stateless engine refactoring (in progress)
- [ ] Multi-agent system (planned)
- [ ] Grounding and ICM (planned)

**Stats**: 10,893 LOC, 527 tests, 88% test coverage

See [SYSTEM_ACHIEVEMENTS.md](SYSTEM_ACHIEVEMENTS.md) for detailed status and [LARSSON_PRIORITY_ROADMAP.md](LARSSON_PRIORITY_ROADMAP.md) for current priorities.

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

## Demos & Examples

### Interactive Demos (`demos/`)

Comprehensive demonstrations of IBDM features:

- `01_core_concepts.py` - Fundamental IBDM concepts (no API key needed)
- `02_cost_analysis.py` - LLM cost comparison (no API key needed)
- `03_nlu_integration_interactive.py` - Interactive NDA dialogue (requires IBDM_API_KEY)
- `03_nlu_integration_basic.py` - Pre-scripted NDA demo (requires IBDM_API_KEY)

See [demos/README.md](demos/README.md) for detailed usage instructions.

### LLM Examples (`examples/`)

Simple examples of LiteLLM integration:

- `simple_llm_demo.py` - Claude 4.5 Sonnet/Haiku usage (requires IBDM_API_KEY)

See [examples/README.md](examples/README.md) for configuration details.

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
