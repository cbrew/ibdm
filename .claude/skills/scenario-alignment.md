# Scenario Alignment Skill

**Purpose**: Systematically align scenario documentation with actual dialogue engine behavior using a structured, incremental approach.

**When to use**: When aligning scenario `state_changes` with actual implementation behavior (Policy #16 - Scenario Alignment).

---

## Overview

This skill breaks down scenario alignment into small, manageable steps to avoid API errors and make progress trackable. It follows the principle: **scenarios document actual behavior, not prescriptive specifications**.

## Step-by-Step Process

### Step 1: Capture Actual State

**Run scenario with tracing**:
```bash
python scripts/run_scenario.py <scenario_id> --replay --trace /tmp/<scenario>_trace.jsonl
```

This creates a JSONL file with actual state after each turn.

**Output**: `/tmp/<scenario>_trace.jsonl` containing actual QUD, commitments, plan, etc.

### Step 2: Document Actual Formats

**Read the trace file** and document the actual formats used:

```bash
head -3 /tmp/<scenario>_trace.jsonl
```

**Create a reference doc** like `/tmp/actual_state_formats.md`:

```markdown
# Actual State Formats

## QUD Format
- Basic: `?parties.legal_entities` (NOT `?x.legal_entities(x)`)
- Clarification: `?x.clarify [utterance=..., topic=...]`

## Commitment Format
- Volunteer info: `predicate(value=args)`
- Direct answers: `?{options}: full answer text`

## Key Observations
- QUD may grow without popping (check actual behavior)
- Commitments vary by move type
```

**Mark TODO complete**: "Document actual formats"

### Step 3: Create TODO List for Fixes

**Break scenario into chunks**:
```bash
# Example for 21-turn scenario
TODO 1: Fix Turn 1 state_changes
TODO 2: Fix Turn 2 state_changes
TODO 3: Fix Turn 3 state_changes
TODO 4: Fix Turns 4-5 state_changes
TODO 5: Fix Turns 6-10 state_changes
TODO 6: Fix Turns 11-16 state_changes
TODO 7: Verify alignment
TODO 8: Commit changes
```

**Why small batches?** Prevents API errors, makes progress visible, allows checkpoints.

### Step 4: Fix Each Batch Incrementally

**For each batch** (e.g., Turns 1-3):

1. **Read trace entry**:
   ```bash
   # Get turn 1 from trace
   head -1 /tmp/<scenario>_trace.jsonl | jq .
   ```

2. **Note actual state**:
   - `qud_top`: What's on top of QUD?
   - `commitments`: What was added?
   - `qud_stack`: Full stack depth?

3. **Edit scenario JSON**:
   ```bash
   vim demos/scenarios/<scenario>.json
   # Update turn's state_changes to match actual
   ```

4. **Common fixes**:
   - QUD format: Use actual repr (e.g., `?parties.legal_entities`)
   - Commitment format: Match actual (`value=` for volunteer info)
   - Remove expectations that don't happen (e.g., `qud_popped` if it doesn't pop)
   - Add `note` field to explain surprising behavior

5. **Mark TODO complete**: "Fix Turns X-Y"

**Example edit**:
```json
"state_changes": {
  "qud_pushed": "?parties.legal_entities",
  "commitments_added": [
    "date(value=2025-02-01)",
    "legal_entities(value=current_company, Global Industries)"
  ],
  "note": "Volunteer info creates structured commitments"
}
```

### Step 5: Verify Alignment

**Run scenario again**:
```bash
python scripts/run_scenario.py <scenario_id> --replay 2>&1 | grep "State mismatch"
```

**Check results**:
- Goal: Zero mismatches (or only minor validator timing issues)
- If mismatches remain: Compare with trace, update state_changes
- Document remaining mismatches if they're validator issues

**Mark TODO complete**: "Verify alignment"

### Step 6: Commit Changes

**Write descriptive commit**:
```bash
git add demos/scenarios/<scenario>.json
git commit -m "docs(scenarios): align <scenario> with actual implementation behavior

- Update QUD format to match actual representation
- Fix commitment format (value= for volunteer info)
- Remove incorrect expectations (qud_popped where it doesn't pop)
- Add notes explaining actual behavior
- Reduce mismatches from X to Y

Aligned per Policy #16 (Scenario Alignment Guide)."
```

**Mark TODO complete**: "Commit changes"

---

## Common Patterns

### Pattern 1: QUD Never Pops

**Observation**: QUD stack keeps growing, never pops.

**Fix**: Replace all `qud_popped` with `qud_unchanged` and track depth.

```json
// Before
"state_changes": {
  "qud_popped": "?nda_type"
}

// After
"state_changes": {
  "qud_unchanged": "?x.clarify [...",
  "qud_depth": 3,
  "note": "QUD not popped in this scenario"
}
```

### Pattern 2: Volunteer Info vs Direct Answers

**Observation**: Different commitment formats for different move types.

**Volunteer info** (assert moves):
```json
"commitments_added": [
  "nda_type(value=mutual)",
  "time_period(value=3 years)"
]
```

**Direct answers** (answer moves):
```json
"commitment_added": "?{mutual, one-way}: I think mutual makes sense..."
```

### Pattern 3: Clarification Questions

**Observation**: Clarification questions include full utterance and topic.

**Fix**:
```json
// Before
"qud_pushed": "?clarify(mutual_nda)"

// After
"qud_pushed": "?x.clarify [utterance=What does mutual mean exactly?, topic=mutual_nda]"
```

---

## Tips for Success

1. **Work in small batches** (1-3 turns at a time)
2. **Use TODOs** to track progress and avoid losing place
3. **Mark TODOs complete** immediately after finishing each step
4. **Compare trace vs scenario** side-by-side for each turn
5. **Add notes** to explain surprising or non-obvious behavior
6. **Verify frequently** - run scenario after every 3-5 turn fixes
7. **Commit often** - don't wait until all turns are fixed

## Anti-Patterns to Avoid

❌ **Don't** try to fix all turns at once (causes API errors)
❌ **Don't** guess state changes without checking trace
❌ **Don't** change implementation to match scenario expectations
❌ **Don't** skip verification step
❌ **Don't** batch commit without incremental verification

## Success Criteria

✅ Scenario runs without state mismatches (or only minor validator issues)
✅ All `state_changes` reflect actual observed behavior
✅ Added notes explain any surprising behavior
✅ Commit message documents changes made
✅ Changes follow Policy #16 (scenarios follow implementation)

---

## Quick Reference

```bash
# 1. Trace
python scripts/run_scenario.py <scenario> --replay --trace /tmp/trace.jsonl

# 2. Document formats
head -3 /tmp/trace.jsonl | jq . > /tmp/formats.txt

# 3. Fix in batches (update JSON)
vim demos/scenarios/<scenario>.json

# 4. Verify after each batch
python scripts/run_scenario.py <scenario> --replay 2>&1 | grep mismatch

# 5. Commit
git add demos/scenarios/<scenario>.json
git commit -m "docs(scenarios): align <scenario> with implementation"
```

## See Also

- `docs/SCENARIO_ALIGNMENT.md` - Full alignment philosophy and procedures
- Policy #16 - Scenario Alignment Guide
- `.claude/beads-helpers.sh` - Task tracking for AI assistants
