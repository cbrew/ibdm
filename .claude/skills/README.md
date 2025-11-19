# Claude Skills

This directory contains skills - reusable procedures that Claude can execute to handle common tasks.

## Available Skills

### setup.md
**Purpose**: Initialize the IBDM development environment
**When**: At the start of every session
**Usage**: Referenced in CLAUDE.md Policy #0

Ensures all dependencies are installed and the environment is ready for work.

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
