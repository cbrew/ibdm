# Validate Scenario JSON Skill

**Purpose**: Check JSON formatting and structure of all scenario files to catch syntax errors and missing required fields.

**When to use**:
- After editing scenario files
- Before committing scenario changes
- When investigating scenario loading errors
- As part of quality checks

---

## Overview

This skill validates all scenario JSON files in `demos/scenarios/` for:
1. **JSON Syntax**: Valid JSON with no trailing commas, missing brackets, etc.
2. **Required Fields**: Presence of essential scenario structure
3. **Turn Structure**: Valid turn format and required turn fields
4. **Consistency**: Turn numbers sequential, speakers valid, etc.

## Quick Validation

**Run existing validator**:
```bash
python -m ibdm.demo.validate_scenarios
```

This uses the built-in validator that checks:
- JSON syntax errors
- Required top-level fields
- Turn structure and numbering
- Valid speaker values
- Move types present

## Step-by-Step Manual Check

### Step 1: Find All Scenarios

```bash
find demos/scenarios -name "*.json" -type f | sort
```

### Step 2: Check JSON Syntax

For each scenario, try to load the JSON:

```bash
python -c "import json; json.load(open('demos/scenarios/nda_comprehensive.json'))" && echo "✓ Valid JSON" || echo "✗ Invalid JSON"
```

### Step 3: Check Required Fields

**Required top-level fields**:
- `scenario_id`
- `title`
- `turns` (array)

**Required turn fields**:
- `turn` (number)
- `speaker` ("user" or "system")
- `utterance` (string)
- `move_type` (string)

**Python check**:
```python
import json
from pathlib import Path

required_top = {"scenario_id", "title", "turns"}
required_turn = {"turn", "speaker", "utterance", "move_type"}

for scenario_file in Path("demos/scenarios").glob("*.json"):
    try:
        data = json.loads(scenario_file.read_text())
        missing_top = required_top - set(data.keys())
        if missing_top:
            print(f"✗ {scenario_file.name}: Missing {missing_top}")
        else:
            for i, turn in enumerate(data["turns"]):
                missing_turn = required_turn - set(turn.keys())
                if missing_turn:
                    print(f"✗ {scenario_file.name} turn {i+1}: Missing {missing_turn}")
            print(f"✓ {scenario_file.name}: Valid structure")
    except json.JSONDecodeError as e:
        print(f"✗ {scenario_file.name}: JSON error at line {e.lineno}: {e.msg}")
    except Exception as e:
        print(f"✗ {scenario_file.name}: {e}")
```

### Step 4: Check Turn Consistency

**Validate**:
- Turn numbers are sequential (1, 2, 3, ...)
- Speakers alternate or follow valid pattern
- No duplicate turn numbers

```python
for turn in data["turns"]:
    expected_turn = turns_seen + 1
    if turn["turn"] != expected_turn:
        print(f"✗ Turn number mismatch: expected {expected_turn}, got {turn['turn']}")
    turns_seen += 1
```

## Common JSON Errors

### 1. Trailing Commas

**Error**:
```json
{
    "field": "value",  ← trailing comma before }
}
```

**Fix**: Remove trailing comma

### 2. Missing Quotes

**Error**:
```json
{
    field: "value"  ← unquoted key
}
```

**Fix**: Quote all keys: `"field": "value"`

### 3. Single Quotes

**Error**:
```json
{
    'field': 'value'  ← single quotes
}
```

**Fix**: Use double quotes: `"field": "value"`

### 4. Unclosed Brackets/Braces

**Error**:
```json
{
    "turns": [
        {"turn": 1}
        ← missing ]
}
```

**Fix**: Close all brackets/braces

## Automated Fix

**Use ruff to format JSON** (if enabled):
```bash
ruff format demos/scenarios/*.json
```

Or use `jq` to reformat:
```bash
jq . demos/scenarios/nda_comprehensive.json > /tmp/formatted.json
mv /tmp/formatted.json demos/scenarios/nda_comprehensive.json
```

## Validation Script

Create a reusable validation script:

```bash
# Save as scripts/check_scenarios.sh
#!/bin/bash
set -e

echo "Validating scenario JSON files..."

for file in demos/scenarios/*.json; do
    echo -n "Checking $(basename "$file")... "
    if python -c "import json; json.load(open('$file'))" 2>/dev/null; then
        echo "✓"
    else
        echo "✗ FAILED"
        python -c "import json; json.load(open('$file'))" 2>&1 | head -5
    fi
done

echo -e "\nRunning built-in validator..."
python -m ibdm.demo.validate_scenarios
```

Make executable:
```bash
chmod +x scripts/check_scenarios.sh
```

Run anytime:
```bash
./scripts/check_scenarios.sh
```

## Integration with Git

**Add pre-commit hook** to validate scenarios automatically:

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Check if any scenario files are being committed
if git diff --cached --name-only | grep -q "demos/scenarios/.*\.json"; then
    echo "Validating scenario JSON files..."
    python -m ibdm.demo.validate_scenarios || exit 1
fi
```

## Troubleshooting

### Python JSONDecodeError

Error shows line number and position:
```
JSONDecodeError: Expecting ',' delimiter: line 47 column 51
```

**Fix**: Go to that line, look for missing comma or extra comma

### File Not Found

```
FileNotFoundError: demos/scenarios/...
```

**Fix**: Check working directory, run from repo root

### Import Error

```
ModuleNotFoundError: No module named 'ibdm'
```

**Fix**: Install project in editable mode:
```bash
uv pip install --system -e .
```

## Best Practices

1. **Always validate** after editing scenario JSON files
2. **Use built-in validator** (`python -m ibdm.demo.validate_scenarios`) as first check
3. **Format with ruff** to maintain consistent style
4. **Test loading** the scenario with `run_scenario.py` before committing
5. **Commit validation fixes separately** from content changes

## Quick Reference

```bash
# Quick check all scenarios
python -m ibdm.demo.validate_scenarios

# Format all scenarios
ruff format demos/scenarios/*.json

# Test specific scenario
python scripts/run_scenario.py <scenario_id>

# Check single file syntax
python -c "import json; json.load(open('demos/scenarios/nda_basic.json'))"
```
