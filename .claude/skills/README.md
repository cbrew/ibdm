# Claude Skills

This directory contains skills - reusable procedures that Claude can execute to handle common tasks.

## Available Skills

### setup.md
**Purpose**: Initialize the IBDM development environment
**When**: At the start of every session
**Usage**: Referenced in CLAUDE.md Policy #0

Ensures all dependencies are installed and the environment is ready for work.

### scenario-alignment.md
**Purpose**: Align scenario documentation with actual dialogue engine behavior
**When**: Working on Policy #16 scenario alignment tasks
**Usage**: Referenced in CLAUDE.md Policy #16 and `docs/SCENARIO_ALIGNMENT.md`

Provides step-by-step procedure for aligning scenarios incrementally in small batches to avoid API errors. Uses trace files to capture actual state and updates scenario JSON systematically.

### beads-planning.md
**Purpose**: Use beads issue tracker for task management
**When**: Planning development phases, tracking work, managing dependencies
**Usage**: For AI agents to create and manage beads tasks

Provides commands and best practices for using beads (git-backed issue tracker) to organize work hierarchically.

### larsson-compliance-task-executor.md
**Purpose**: Execute Larsson compliance validation tasks
**When**: Verifying implementation fidelity to Larsson (2002) algorithms
**Usage**: For measuring and improving Larsson compliance scores

### larsson-compliance-metrics.md
**Purpose**: Measure Larsson compliance with automated metrics
**When**: Generating compliance reports and fidelity scores
**Usage**: For quantitative validation of Larsson algorithm implementation

### larsson-delta-advisor.md
**Purpose**: Analyze implementation differences from Larsson specification
**When**: Investigating deviations and planning alignment work
**Usage**: For understanding where and why implementation differs from Larsson (2002)

## How Skills Work

Skills are markdown files that contain step-by-step instructions for common procedures. They serve as:

1. **Documentation**: Clear procedures that are always up-to-date
2. **Consistency**: Same process every time, no variation
3. **Training**: Help new AI agents understand project setup
4. **Debugging**: When something goes wrong, the skill shows what should happen

## Creating New Skills

To create a new skill:

1. Create a markdown file in `.claude/skills/`
2. Give it a clear name (e.g., `deploy.md`, `test.md`)
3. Document the purpose, when to use it, and step-by-step instructions
4. Add it to CLAUDE.md if it should be used automatically

## Why This Matters

Before skills, we had:
- ❌ Dependency flailing every session
- ❌ Import errors wasting time
- ❌ Inconsistent setup procedures

With skills:
- ✅ One command gets everything ready
- ✅ Predictable, reliable setup
- ✅ Focus on work, not environment debugging
