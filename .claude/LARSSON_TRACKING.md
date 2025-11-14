# Larsson Fidelity Tracking System

Automated measurement and review of IBDM's alignment with Larsson (2002) algorithms.

## Overview

This system automatically measures Larsson fidelity before and after beads tasks, prompts for predictions, and generates comparison reviews.

## Quick Start

```bash
# Start a task with baseline measurement
.claude/beads-larsson.sh start ibdm-123
# → Generates baseline report
# → Prompts: "How will this task affect Larsson alignment?"
# → Records prediction

# Work on the task normally...
# ... make changes, commit ...

# Complete task with final measurement
.claude/beads-larsson.sh complete ibdm-123 "Implemented rules"
# → Generates final report
# → Compares baseline vs final
# → Reviews prediction vs actual
```

## Components

### 1. Enhanced Beads Wrapper (`.claude/beads-larsson.sh`)

**Commands:**
- `start <task-id>` - Start task with baseline + prediction
- `complete <task-id> [msg]` - Complete task with review
- `measure [label]` - Quick fidelity measurement
- All other commands delegated to `beads-helpers.sh`

**What Happens:**

**On Start:**
1. Generates baseline fidelity report (text + JSON)
2. Shows current score
3. Prompts for prediction about impact on 5 components
4. Records prediction with timestamp + git hash
5. Starts beads task

**On Complete:**
1. Generates final fidelity report (text + JSON)
2. Compares baseline vs final scores (overall + per-component)
3. Shows prediction vs actual changes
4. Generates review report
5. Completes beads task

### 2. Fidelity Report Generator (`scripts/generate_fidelity_report.py`)

Evaluates 5 components:
1. **Architectural Compliance** (25%) - Control loop, four phases, state passing
2. **Information State Structure** (25%) - Private/shared, QUD stack, fields
3. **Semantic Operations Coverage** (20%) - resolves(), combines(), depends()
4. **Rules Coverage** (20%) - Integration rules, selection rules
5. **Domain Independence** (10%) - No hardcoded predicates, domain model usage

**Outputs:**
- Text report: Human-readable summary with issues/recommendations
- JSON report: Structured data for programmatic analysis

### 3. Report Storage

**Directory Structure:**
```
reports/
├── {task-id}_baseline_{timestamp}_{hash}.txt
├── {task-id}_baseline_{timestamp}_{hash}.json
├── {task-id}_final_{timestamp}_{hash}.txt
├── {task-id}_final_{timestamp}_{hash}.json
├── {task-id}_review_{timestamp}_{hash}.txt
└── predictions/
    ├── {task-id}_prediction_{timestamp}_{hash}.txt
    └── {task-id}_state.txt  (temporary)
```

**Naming Convention:**
- Timestamp: `YYYY-MM-DD_HHMMSS`
- Hash: Short git commit hash (7 chars)
- Example: `ibdm-123_baseline_2025-11-14_153045_a3f7b2c.txt`

## Workflow Integration

### For AI Agents (Claude Code)

When user asks to work on a beads task:

```bash
# 1. Check ready tasks
.claude/beads-helpers.sh ready

# 2. Start with Larsson tracking
.claude/beads-larsson.sh start ibdm-123

# 3. When prompted for prediction, consider:
#    - Will this change rules? → Rules Coverage ↑
#    - Will this add semantic operations? → Semantic Operations ↑
#    - Will this refactor engines? → Architectural Compliance ↑/↓
#    - Will this modify IS structure? → Information State ↑/↓
#    - Will this hardcode domain logic? → Domain Independence ↓

# 4. Complete with review
.claude/beads-larsson.sh complete ibdm-123 "message"
```

### For Manual Use

```bash
# Optional: Load aliases for convenience
source .claude/beads-alias.sh

# Then use short commands
bd-start ibdm-123
bd-complete ibdm-123
bd-measure before-refactor
```

## Prediction Guidelines

When prompted for prediction, consider:

1. **What code will change?**
   - Rules files → Rules Coverage
   - Engine files → Architectural Compliance
   - Domain files → Domain Independence
   - IS/Question files → Information State, Semantic Operations

2. **Will it increase or decrease fidelity?**
   - Adding Larsson rules/features → Increase
   - Refactoring to match algorithms → Increase
   - Quick hacks or shortcuts → Decrease
   - Hardcoding domain logic → Decrease (Domain Independence)

3. **Expected magnitude**
   - Small changes: ±1-3 points
   - Medium changes: ±3-7 points
   - Large refactors: ±7-15 points

**Example Prediction:**
```
This task implements IntegrateAnswer rule (ibdm-rules.4).

Expected changes:
- Rules Coverage: +5 points (adding IBiS1 integration rule)
- Architectural Compliance: +2 points (better algorithm 2.2 match)
- Other components: No change expected

Overall: Should increase from ~85 → ~90
```

## Review Process

After completion, the review report shows:

```
SCORE SUMMARY:
  Baseline: 85.2/100
  Final:    89.7/100
  Delta:    +4.5

PREDICTION:
[Your prediction text]

Component Changes:
  ↑ Rules Coverage                20.0 → 25.0 (+5.0)
  ↑ Architectural Compliance      75.0 → 77.0 (+2.0)
  → Information State             90.0 → 90.0 (+0.0)
  ...
```

**Key:**
- `↑` Increased
- `↓` Decreased
- `→` No change

## Troubleshooting

**Error: "Failed to generate report"**
- Check that IBDM_API_KEY is set
- Verify uv environment is activated
- Try manual run: `python scripts/generate_fidelity_report.py`

**No baseline found warning:**
- Task was started with standard `beads-helpers.sh start`
- Falls back to final report only (no comparison)

**Prediction prompt not showing:**
- Check script has execute permission: `chmod +x .claude/beads-larsson.sh`
- Run directly: `.claude/beads-larsson.sh start <task-id>`

## Integration with Global Policy

From `~/.claude/CLAUDE.md`:
> Before and after every task, run the tools that produce the files in the reports directory. tag each report file with timestamp and git hash

This system implements that policy automatically:
- ✓ Before task: Baseline report generated
- ✓ After task: Final report generated
- ✓ Timestamp: Included in filename
- ✓ Git hash: Included in filename
- ✓ Stored in reports directory

## Advanced Usage

### Measure Without Task Context

```bash
# Quick measurement for ad-hoc checks
.claude/beads-larsson.sh measure before-refactor
.claude/beads-larsson.sh measure after-fix
```

### Manual Report Generation

```bash
# Text report to stdout
python scripts/generate_fidelity_report.py

# Save to file
python scripts/generate_fidelity_report.py -o reports/custom.txt

# JSON output
python scripts/generate_fidelity_report.py --json -o reports/custom.json

# With visualizations (requires matplotlib)
python scripts/generate_fidelity_report.py --plot reports/charts/
```

### Comparing Historical Reports

```bash
# Find all reports for a task
ls reports/ibdm-123_*

# Compare JSON programmatically
python -c "
import json
baseline = json.load(open('reports/ibdm-123_baseline_*.json'))
final = json.load(open('reports/ibdm-123_final_*.json'))
print(f\"Delta: {final['overall_score'] - baseline['overall_score']:.1f}\")
"
```

## See Also

- `docs/LARSSON_ALGORITHMS.md` - Larsson compliance requirements
- `src/ibdm/metrics/larsson_fidelity.py` - Metrics implementation
- `CLAUDE.md` - Project development guide (Policy #6)
