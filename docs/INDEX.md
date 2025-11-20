# IBDM Documentation Index

**Last Updated**: 2025-11-20

Clean, focused documentation for the Issue-Based Dialogue Management system.

---

## 🚀 Essential Documentation

| Document | Purpose |
|----------|---------|
| [README.md](../README.md) | Project overview and quick start |
| [CLAUDE.md](../CLAUDE.md) | **Development guide** - Policies, workflow, tooling |
| [GETTING_STARTED.md](../GETTING_STARTED.md) | Tutorial on IBDM concepts |
| [SYSTEM_ACHIEVEMENTS.md](../SYSTEM_ACHIEVEMENTS.md) | What's been built |

---

## 🏗️ Architecture

| Document | Purpose |
|----------|---------|
| [architecture_principles.md](architecture_principles.md) | **Policy #0** - Clarity, simplicity, no fallbacks |
| [LARSSON_ALGORITHMS.md](LARSSON_ALGORITHMS.md) | **Authoritative reference** - IBiS1-4 algorithms, rules, state structures |
| [burr_state_refactoring.md](burr_state_refactoring.md) | Stateless engine design |
| [execution_controller_design.md](execution_controller_design.md) | Execution flow control (step/auto/replay modes) |

---

## ⚙️ Configuration

| Document | Purpose |
|----------|---------|
| [environment_setup.md](environment_setup.md) | Environment variables, IBDM_API_KEY setup |
| [llm_configuration.md](llm_configuration.md) | LiteLLM setup, Claude 4.5 Sonnet/Haiku |

---

## 🎮 Demo & Scenarios

### Running Scenarios

```bash
# List available scenarios
python scripts/run_scenario.py --list

# Run a scenario in auto mode
python scripts/run_scenario.py nda_basic

# Run in step mode (manual advancement)
python scripts/run_scenario.py nda_basic --step

# Search scenarios
python scripts/run_scenario.py --search grounding
```

**See**: `demos/scenarios/*.json` for all scenario definitions

---

## 📖 Reference Material

| Document | Purpose |
|----------|---------|
| [ZFC.md](ZFC.md) | Zero Framework Cognition principles (philosophical) |
| [visualization.md](visualization.md) | Visualization system documentation |
| [larsson_thesis/](larsson_thesis/) | Larsson thesis chapters (reference) |
| [Larsson_Tesis_nopages.md](Larsson_Tesis_nopages.md) | Full thesis (single file) |

---

## 🗄️ Archive

Historical and superseded documentation: [archive/README.md](archive/README.md)

**Major archival (2025-11-20)**:
- Old scenario specs (replaced by JSON)
- Deprecated tool guides (replaced by `run_scenario.py`)
- Historical roadmaps
- Completed implementation docs

---

## 💡 Quick Reference

**I want to...**

| Task | Start Here |
|------|------------|
| Start development | [CLAUDE.md](../CLAUDE.md) |
| Run a demo | `python scripts/run_scenario.py --list` |
| Understand architecture | [architecture_principles.md](architecture_principles.md) |
| Set up environment | [environment_setup.md](environment_setup.md) |
| Learn IBDM concepts | [GETTING_STARTED.md](../GETTING_STARTED.md) |
| Understand Larsson algorithms | [LARSSON_ALGORITHMS.md](LARSSON_ALGORITHMS.md) |

---

## 🔗 External Resources

- [Burr Documentation](https://burr.dagworks.io/)
- [LiteLLM Documentation](https://docs.litellm.ai/)
- [Anthropic Claude Documentation](https://docs.anthropic.com/)

---

**Documentation too verbose or outdated?** File an issue or submit a PR!
