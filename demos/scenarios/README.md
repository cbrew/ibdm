# IBDM Business Demo Scenarios

This directory contains pre-scripted business demonstration scenarios for the IBDM (Issue-Based Dialogue Management) system.

## Overview

Each scenario is a JSON file containing:
- **Complete dialogue transcript** (user and system turns)
- **Business narrative** explaining what's being demonstrated
- **Larsson algorithm references** (which rules fire when)
- **State transitions** showing how the information state evolves
- **Expected metrics** (turns, efficiency, completeness)
- **Business value proposition** for each scenario

## Scenarios

### 1. **nda_basic.json** - Happy Path Demo
- **Purpose**: Demonstrate core IBDM operation with perfect information gathering
- **Duration**: 12 turns
- **Key Features**: QUD management, plan progression, systematic questioning
- **Audience**: First-time viewers, executives wanting quick overview
- **Larsson Fidelity**: 95%

### 2. **nda_volunteer.json** - Volunteered Information Demo
- **Purpose**: Show intelligent handling of "over-answering"
- **Duration**: 5 turns (67% reduction from baseline)
- **Key Features**: Belief accommodation, question skipping, dynamic planning
- **Audience**: Technical audiences, UX researchers
- **Larsson Fidelity**: 98%

### 3. **nda_complex.json** - Clarifications and Dependencies Demo
- **Purpose**: Demonstrate robustness with ambiguous answers and nested questions
- **Duration**: 19 turns (includes 3 clarification sub-dialogues)
- **Key Features**: Local questions, QUD nesting (depth 2), context maintenance
- **Audience**: Systems architects, AI researchers, skeptics
- **Larsson Fidelity**: 92%

### 4. **nda_grounding.json** - ICM and Confidence Demo
- **Purpose**: Show confidence-based grounding strategies and error prevention
- **Duration**: 16 turns (includes 1 confirmation, 1 clarification)
- **Key Features**: ICM moves, confidence thresholds, grounding strategies
- **Audience**: Product managers, quality assurance, risk-averse stakeholders
- **Larsson Fidelity**: 95%

## Usage

### With Business Demo Launcher
```bash
# Run specific scenario
python scripts/run_business_demo.py --scenario nda_basic

# Run all scenarios
python scripts/run_business_demo.py --all

# Run with HTML report generation
python scripts/run_business_demo.py --scenario nda_grounding --report
```

### Programmatic Access
```python
import json
from pathlib import Path

# Load scenario
scenario_path = Path("demos/scenarios/nda_basic.json")
scenario = json.loads(scenario_path.read_text())

# Access turns
for turn in scenario["turns"]:
    print(f"Turn {turn['turn']}: {turn['speaker']}")
    print(f"  {turn['utterance']}")
    print(f"  Larsson: {turn['larsson_rule']}")
```

## Scenario Selection Guide

| Goal | Recommended Scenario | Why |
|------|---------------------|-----|
| Quick overview (5 min) | nda_basic | Shows core value prop efficiently |
| Impress power users | nda_volunteer | Demonstrates intelligence, not just automation |
| Prove robustness | nda_complex | Shows handling of real-world messiness |
| Address quality concerns | nda_grounding | Demonstrates error prevention and transparency |
| Technical deep-dive | All four | Complete picture of IBDM capabilities |

## Metrics Summary

| Scenario | Turns | Efficiency | Completeness | Larsson Fidelity | Special Features |
|----------|-------|------------|--------------|------------------|------------------|
| Basic | 12 | 100% | 100% | 95% | Baseline reference |
| Volunteer | 5 | 240% | 100% | 98% | 3 questions skipped |
| Complex | 19 | 63% | 100% | 92% | 3 clarifications, QUD depth=2 |
| Grounding | 16 | 75% | 100% | 95% | 4 ICM moves, 2 grounding interventions |

## Business Value Highlights

### Traditional Chatbot vs IBDM

| Capability | Traditional Chatbot | IBDM |
|------------|-------------------|------|
| Volunteered Info | Ignored or causes errors | Accommodated intelligently (volunteer scenario) |
| Ambiguous Answers | Guesses silently or fails | Asks for clarification (complex scenario) |
| Nested Questions | Context lost | Perfect context maintenance (complex scenario) |
| Confidence Management | No visibility | Explicit grounding strategies (grounding scenario) |
| Transparency | Black box | Full state visibility (all scenarios) |

## Customization

To create a new scenario:

1. Copy an existing scenario JSON file
2. Modify the `turns` array with your dialogue
3. Update `expected_outcomes` and `metrics`
4. Add relevant `larsson_algorithms` references
5. Write compelling `business_narrative` and `business_value`
6. Test with launcher script

## Related Documentation

- **BUSINESS_DEMO_GUIDE.md** - Quick-start guide for running demos
- **demos/SCENARIO_PLAN_NDA.md** - Original planning document
- **docs/LARSSON_ALGORITHMS.md** - Technical details on Larsson (2002) implementation
- **SYSTEM_ACHIEVEMENTS.md** - What's been implemented

## Questions?

For questions about scenarios or to request custom scenarios:
1. Check BUSINESS_DEMO_GUIDE.md first
2. See examples/ibis4_demo.py for live interactive demos
3. Consult CLAUDE.md for development guidelines
