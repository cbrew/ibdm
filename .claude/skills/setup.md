# Setup Skill

**Purpose**: Initialize the IBDM development environment properly before any work begins.

**When to use**:
- At the start of every session
- After any dependency changes
- When encountering import errors

## Setup Steps

1. **Install all dependencies**:
   ```bash
   uv pip install --system -e .
   ```

   This installs the project in editable mode with all dependencies from `pyproject.toml`.

2. **Verify core imports work**:
   ```bash
   python -c "import sys; sys.path.insert(0, 'src'); from ibdm.core import InformationState; print('✓ Core imports working')"
   ```

3. **Verify tools are available**:
   ```bash
   python -m pytest --version
   python -m ruff --version
   python -m pyright --version
   ```

4. **Check API key is set** (for LLM features):
   ```bash
   python -c "import os; assert os.getenv('IBDM_API_KEY'), 'Missing IBDM_API_KEY'; print('✓ API key configured')" || echo "⚠️  IBDM_API_KEY not set (LLM features will not work)"
   ```

5. **Report status**:
   ```bash
   echo "✅ IBDM environment ready"
   ```

## What this fixes

- **No more "module not found" errors**: All dependencies installed properly
- **No more flailing with imports**: Environment is verified before work starts
- **No more tool failures**: pytest, ruff, pyright are guaranteed available
- **Clear status**: You know the environment is ready before coding

## Usage in CLAUDE.md

Add this to the top of your workflow section:

```bash
# 0. Setup environment (run at start of every session)
# Use the setup skill to ensure environment is ready
```

Then in your instructions, tell Claude to run this skill before doing anything else.
