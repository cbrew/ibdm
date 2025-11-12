# Beads Tasks for Rule-Driven Demo Implementation

## Parent Task
ibdm-dem.1.5: Implement main dialogue loop with NLUDialogueEngine [open]

## New Subtasks to Create

### ibdm-dem.1.5.1: Create NDA task accommodation interpretation rule
**Priority**: 0 (blocking other work)
**Type**: task
**Status**: open
**Parent**: ibdm-dem.1.5

**Description**:
Create an interpretation rule that detects "draft NDA" requests and creates a hierarchical Plan for NDA document generation.

**Acceptance Criteria**:
- Rule detects utterances requesting NDA creation (e.g., "I need to draft an NDA")
- Creates Plan with plan_type="findout"
- Plan contains ordered subplans for each NDA requirement:
  1. findout(parties) - WhQuestion
  2. findout(nda_type) - AltQuestion["mutual", "one-way"]
  3. findout(effective_date) - WhQuestion
  4. findout(duration) - WhQuestion
  5. findout(governing_law) - AltQuestion["California", "Delaware"]
  6. confirm(generate_document) - YNQuestion
- Plan is stored in state.private.plan
- Initial gathered_info populated with {document_type: "NDA"}

**Implementation Location**: `src/ibdm/rules/interpretation_rules.py`

**Tests**: Unit tests in `tests/unit/test_interpretation_rules.py`

---

### ibdm-dem.1.5.2: Create plan-based selection rule
**Priority**: 0 (blocking other work)
**Type**: task
**Status**: open
**Parent**: ibdm-dem.1.5
**Blocks**: ibdm-dem.1.5.3

**Description**:
Create selection rule that executes active Plans by converting findout subplans into ask moves.

**Acceptance Criteria**:
- Rule checks for active Plans in state.private.plan
- Takes first active subplan of type "findout"
- Creates DialogueMove(move_type="ask", content=<question from subplan>)
- Adds move to state.private.agenda
- Marks subplan as completed after use
- Has higher priority than generic selection rules
- Only triggers when no other moves are on agenda

**Implementation Location**: `src/ibdm/rules/selection_rules.py`

**Tests**: Unit tests in `tests/unit/test_selection_rules.py`

---

### ibdm-dem.1.5.3: Remove manual question creation from demo
**Priority**: 1
**Type**: task
**Status**: open
**Parent**: ibdm-dem.1.5
**Depends on**: ibdm-dem.1.5.1, ibdm-dem.1.5.2

**Description**:
Update demo to use rule-driven control flow instead of manually creating and integrating system questions.

**Acceptance Criteria**:
- Remove all manual DialogueMove creation for system questions
- Remove direct engine.integrate() calls for system moves
- Let Burr state machine's select/generate actions handle system responses
- Demo only calls state_machine.process_utterance() for user input
- Display system responses from Burr state after generation
- QUD stack evolution shown but not manually manipulated
- Metrics still captured correctly

**Implementation Location**: `demos/03_nlu_integration_basic.py`

**Changes Required**:
- Delete lines 911-938 (manual question creation and integration)
- Display system response from burr_state.get("utterance_text") after processing
- Get response moves from burr_state.get("response_move")

---

### ibdm-dem.1.5.4: Test full rule-driven NDA dialogue flow
**Priority**: 1
**Type**: task
**Status**: open
**Parent**: ibdm-dem.1.5
**Depends on**: ibdm-dem.1.5.3

**Description**:
Verify the complete NDA generation dialogue works with rule-driven control.

**Acceptance Criteria**:
- Demo runs without errors through all 7 turns
- Task accommodation triggers on "I need to draft an NDA"
- System asks appropriate questions via selection rules
- Answers resolve QUDs via integration rules
- QUD stack evolves correctly (push on ask, pop on answer)
- All NDA information gathered: parties, type, date, duration, law
- Metrics accurately captured for all turns
- No manual state manipulation in demo code

**Test Method**: Run `python demos/03_nlu_integration_basic.py` and verify output

**Documentation**: Update demo comments to explain rule-driven architecture

---

### ibdm-dem.1.5.5: Add NDA domain-specific generation rules (optional enhancement)
**Priority**: 2
**Type**: task
**Status**: open
**Parent**: ibdm-dem.1.5
**Depends on**: ibdm-dem.1.5.4

**Description**:
Enhance generation rules to produce more natural legal-domain question text.

**Acceptance Criteria**:
- Generation rule for "parties" question produces legal-appropriate text
- Generation rule for "nda_type" produces clear mutual vs one-way explanation
- Generation rule for "governing_law" includes jurisdiction context
- All generated questions sound natural in legal document context

**Implementation Location**: `src/ibdm/rules/generation_rules.py`

**Example**:
Instead of: "What parties?"
Generate: "What are the names of the parties entering into this agreement?"

**Note**: This is optional - generic generation may be sufficient for demo

---

## Task Dependencies

```
ibdm-dem.1.5: Main dialogue loop
├── ibdm-dem.1.5.1: NDA task accommodation rule (P0)
├── ibdm-dem.1.5.2: Plan-based selection rule (P0)
│   └── blocks → ibdm-dem.1.5.3
├── ibdm-dem.1.5.3: Remove manual control from demo (P1)
│   └── depends on → ibdm-dem.1.5.1, ibdm-dem.1.5.2
│   └── blocks → ibdm-dem.1.5.4
├── ibdm-dem.1.5.4: Test full flow (P1)
│   └── depends on → ibdm-dem.1.5.3
│   └── blocks → ibdm-dem.1.5.5
└── ibdm-dem.1.5.5: Domain-specific generation (P2, optional)
    └── depends on → ibdm-dem.1.5.4
```

## Implementation Order

1. **First**: ibdm-dem.1.5.1 and ibdm-dem.1.5.2 (can be done in parallel)
2. **Second**: ibdm-dem.1.5.3 (after rules are working)
3. **Third**: ibdm-dem.1.5.4 (test and verify)
4. **Optional**: ibdm-dem.1.5.5 (enhancement if needed)
