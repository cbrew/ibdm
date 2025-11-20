# NLG Integration Design for BusinessDemo

**Status:** ✅ CURRENT
**Task:** ibdm-nlg-demo.1
**Date:** 2025-11-19

## Overview

This document describes the design for integrating the NLG engine into the BusinessDemo class to generate natural language utterances dynamically from dialogue moves, while maintaining the ability to compare against pre-scripted gold standard utterances.

## Current Architecture

### BusinessDemo (`scripts/run_business_demo.py`)
- Reads scenario JSON files with pre-scripted dialogues
- Each turn contains: `speaker`, `utterance`, `move_type`, `state_changes`
- Currently displays pre-scripted utterances directly (line 128)
- Has simplified state tracking via dictionary (lines 737-743)

### NLG Engine (`src/ibdm/nlg/nlg_engine.py`)
- Stateless engine: `generate(move: DialogueMove, state: InformationState) → NLGResult`
- Supports multiple strategies: template, plan_aware, llm
- Already has NDA-specific generation logic
- Works with proper DialogueMove objects (WhQuestion, Answer, etc.)

### Scenario JSON Structure
```json
{
  "turn": 2,
  "speaker": "system",
  "utterance": "What are the parties to the NDA?",
  "move_type": "ask",
  "state_changes": {
    "qud_pushed": "?x.legal_entities(x)"
  }
}
```

## Design Decisions

### 1. DialogueMove Construction from JSON

**Problem:** Scenario JSON contains simple move_type strings, but NLG engine needs properly structured DialogueMove objects with Question/Answer content.

**Solution:** Add a move factory method to parse JSON turn data into DialogueMove objects.

```python
def _create_dialogue_move_from_turn(self, turn_data: dict[str, Any]) -> DialogueMove:
    """Create DialogueMove from scenario turn data.

    Parses move_type and state_changes to construct proper content
    (WhQuestion, YNQuestion, AltQuestion, Answer, etc.)
    """
    move_type = turn_data["move_type"]
    speaker = turn_data["speaker"]
    state_changes = turn_data.get("state_changes", {})

    # Construct content based on move_type and state_changes
    if move_type == "ask":
        content = self._parse_question_from_state_changes(state_changes)
    elif move_type == "answer":
        content = self._parse_answer_from_turn(turn_data, state_changes)
    elif move_type == "request":
        content = turn_data.get("utterance")  # Simple command
    else:
        content = turn_data.get("utterance")

    return DialogueMove(
        move_type=move_type,
        content=content,
        speaker=speaker
    )
```

**Question Parsing:**
- `"qud_pushed": "?x.legal_entities(x)"` → `WhQuestion(variable="x", predicate="legal_entities")`
- `"qud_pushed": "?nda_type"` → Detect from context if it's YN or Alt question
- Use heuristics: if state_changes mention alternatives → AltQuestion

**Answer Parsing:**
- Extract answer content from `turn_data["utterance"]`
- Link to previous question (top of QUD stack in state)
- `Answer(content="Acme Corporation and TechStart Inc", question_ref=last_question)`

### 2. State Reconstruction from state_changes

**Problem:** NLG engine needs full InformationState for context, but JSON only has state_changes deltas. Currently the demo creates a real `InformationState` object (line 99) but never uses it - instead using a plain dictionary for display.

**Solution:** Use the existing `self.state` InformationState and apply changes incrementally.

**Implementation:**
1. Use existing `self.state` InformationState (already initialized at line 99)
2. Upgrade `_update_cumulative_state()` to work with actual InformationState objects instead of plain dictionary
3. Apply state_changes to real state structures:
   - `qud_pushed` → `state.shared.qud.append(question)`
   - `commitment_added` → `state.shared.com.add(proposition)`
   - `issues_added` → `state.private.issues.extend(issues)`
   - `plan_created` → Create and add Plan object

**State Operations Mapping:**
```python
def _apply_state_changes(self, state: InformationState, changes: dict) -> None:
    """Apply state_changes from JSON to InformationState."""

    # QUD operations
    if "qud_pushed" in changes:
        question = self._parse_question_from_state_changes(changes)
        state.shared.qud.append(question)

    if "qud_popped" in changes:
        if state.shared.qud:
            state.shared.qud.pop()

    # Commitments
    if "commitment_added" in changes:
        proposition = changes["commitment_added"]
        state.shared.com.add(proposition)

    # Plans
    if "plan_created" in changes:
        # Create actual Plan object from description
        plan = self._create_plan_from_description(changes["plan_created"])
        state.private.plan.append(plan)
```

### 3. Pre-scripted Utterance Handling

**Problem:** Pre-scripted utterances are valuable as gold standard for comparison, but we want to demonstrate live NLG.

**Solution:** Keep pre-scripted utterances and add comparison capability.

**Modes:**
1. **Scripted Mode (default):** Display pre-scripted utterances only
   - Preserves current behavior
   - Fast, no NLG overhead
   - Good for demos focused on dialogue structure

2. **Compare Mode:** Display both side-by-side
   - Show pre-scripted (gold standard)
   - Show NLG-generated (live generation)
   - Highlight differences
   - Good for NLG quality assessment

3. **NLG Mode:** Display only NLG-generated
   - Pure live generation
   - No pre-scripted fallback
   - Demonstrates full NLG capability

**Output Format (Compare Mode):**
```
─────────────────────────────────────────────────────────────────────
Turn 2: 🤖 SYSTEM [ask]
─────────────────────────────────────────────────────────────────────

📜 SCRIPTED (Gold Standard):
   "What are the parties to the NDA?"

🤖 NLG GENERATED (plan_aware):
   "[Step 1 of 5] What are the names of the parties entering into this NDA?"

💡 Business Context: System asks the first question from its plan...
```

### 4. NLG Mode Integration (Flag vs Always-On)

**Decision:** Add `--nlg-mode` flag with three options (not always-on).

**Rationale:**
- Preserves backward compatibility
- Allows gradual rollout and testing
- Supports multiple use cases (demo, QA, development)
- Maintains performance for structure-focused demos

**CLI Interface:**
```bash
# Current behavior (no change)
python scripts/run_business_demo.py --scenario nda_basic

# Show both scripted and NLG
python scripts/run_business_demo.py --scenario nda_basic --nlg-mode compare

# Use only NLG
python scripts/run_business_demo.py --scenario nda_basic --nlg-mode replace

# Explicitly disable (same as default)
python scripts/run_business_demo.py --scenario nda_basic --nlg-mode off
```

**Configuration:**
```python
class BusinessDemo:
    def __init__(
        self,
        scenario_path: Path,
        verbose: bool = True,
        auto_advance: bool = True,
        nlg_mode: str = "off",  # "off", "compare", "replace"
    ):
        ...
        self.nlg_mode = nlg_mode

        # Initialize NLG engine only if needed
        if self.nlg_mode != "off":
            from ibdm.nlg.nlg_engine import NLGEngine, NLGEngineConfig
            config = NLGEngineConfig(
                default_strategy="plan_aware",
                use_plan_awareness=True,
                use_domain_descriptions=True
            )
            self.nlg_engine = NLGEngine(config)
        else:
            self.nlg_engine = None
```

## Implementation Plan

### Phase 1: Foundation (Current Task)
- ✅ Design document (this file)
- Document key decisions and architecture

### Phase 2: State Management
- Use existing `self.state` instead of plain dictionary
- Refactor `_update_cumulative_state()` to update real InformationState
- Implement proper state change application (QUD, commitments, plans)
- Test state reconstruction matches expected state

### Phase 3: Move Construction
- Implement `_create_dialogue_move_from_turn()`
- Implement `_parse_question_from_state_changes()`
- Implement `_parse_answer_from_turn()`
- Test move construction produces valid DialogueMove objects

### Phase 4: NLG Integration
- Add `--nlg-mode` CLI argument
- Initialize NLG engine conditionally
- Implement NLG generation in `print_turn()`
- Add comparison display logic

### Phase 5: Testing & Refinement
- Test all three modes (off, compare, replace)
- Verify NLG output quality
- Update HTML report generation to include NLG metadata
- Document usage in README

## Technical Considerations

### Question Type Detection

Since JSON doesn't explicitly specify question types, we need heuristics:

```python
def _parse_question_from_state_changes(self, changes: dict) -> Question:
    """Parse question from state_changes.

    Heuristics:
    - "?x.predicate(x)" → WhQuestion
    - "?proposition" with no variables → YNQuestion or check alternatives
    - Check for alternative values in changes → AltQuestion
    """
    qud_pushed = changes.get("qud_pushed", "")

    # Wh-question pattern: ?x.predicate(x) or ?x.predicate
    if re.match(r"\?(\w+)\.(\w+)", qud_pushed):
        match = re.match(r"\?(\w+)\.(\w+)(?:\(.*\))?", qud_pushed)
        variable = match.group(1)
        predicate = match.group(2)
        return WhQuestion(variable=variable, predicate=predicate)

    # Alternative question if we see multiple options mentioned
    # (This requires domain knowledge - may need manual annotation)
    elif self._has_alternatives(changes):
        alternatives = self._extract_alternatives(changes)
        return AltQuestion(alternatives=alternatives)

    # Default to simple proposition question
    else:
        proposition = qud_pushed.replace("?", "")
        return YNQuestion(proposition=proposition)
```

### Performance

- NLG generation adds latency (~100-500ms per utterance with templates, more with LLM)
- In compare/replace modes, may want to disable auto-advance delays
- Consider caching generated utterances for replay

### Testing Strategy

1. **Unit tests:** Test move construction, state application individually
2. **Integration tests:** Run scenarios in all three modes, verify output
3. **Manual QA:** Review NLG quality in compare mode
4. **Regression:** Ensure scripted mode unchanged

## Benefits

1. **Demonstrates live NLG:** Shows IBDM can generate natural language dynamically
2. **Quality assessment:** Compare mode enables NLG evaluation
3. **Backward compatible:** Default behavior unchanged
4. **Flexible:** Three modes support different use cases
5. **Educational:** Shows relationship between semantic moves and surface text

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Question type detection ambiguity | Wrong question type → poor NLG | Add explicit type hints to JSON schema |
| State reconstruction errors | Wrong context → irrelevant NLG | Extensive testing, state validation |
| NLG quality below scripted | Demo less impressive | Use compare mode to show both, iterate on NLG |
| Performance degradation | Slower demos | Make NLG opt-in, optimize generation |

## Future Enhancements

1. **LLM-based generation:** Use Claude for system utterances (current: templates)
2. **Scenario validation:** Verify state_changes are valid
3. **Interactive mode:** Allow editing NLG prompts live
4. **Quality metrics:** Automatic comparison scoring (BLEU, etc.)
5. **Multi-language:** Generate in different languages from same moves

## References

- `src/ibdm/nlg/nlg_engine.py` - NLG implementation
- `scripts/run_business_demo.py` - Current BusinessDemo class
- `demos/scenarios/*.json` - Scenario format
- `CLAUDE.md` Policy #14 (ZFC) - Use LLM for language, not dialogue logic

---

**Next Steps:** Proceed to Phase 2 (State Management implementation)
