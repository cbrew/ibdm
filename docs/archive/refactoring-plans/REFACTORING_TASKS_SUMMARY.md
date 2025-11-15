# Accommodation Refactoring: Beads Tasks Summary

**Epic**: `ibdm-accom` - Move Task Accommodation from Interpretation to Integration Phase
**Total Tasks**: 35 (1 epic + 7 phase epics + 27 subtasks)
**Estimated Time**: 12 hours
**Priority**: P0 (Critical architectural fix)

---

## Task Hierarchy

### Epic: ibdm-accom
Refactor: Move Task Accommodation from Interpretation to Integration Phase

#### Phase 1: ibdm-accom.1 - Refactor Interpretation Rules
**Priority**: P0 | **Tasks**: 3 | **Time**: 2 hours

- `ibdm-accom.1.1` [P0] Add simple request detection rule with keyword matching
- `ibdm-accom.1.2` [P1] Deprecate NDA accommodation rule in interpretation
- `ibdm-accom.1.3` [P1] Update interpretation tests for new behavior

**Deliverable**: Request detection works, creates moves, no plans yet

---

#### Phase 2: ibdm-accom.2 - Add Accommodation to Integration
**Priority**: P0 | **Tasks**: 6 | **Time**: 3 hours

- `ibdm-accom.2.1` [P0] Add accommodate_request integration rule infrastructure
- `ibdm-accom.2.2` [P0] Implement task classification in integration
- `ibdm-accom.2.3` [P0] Move NDA accommodation logic to integration
- `ibdm-accom.2.4` [P1] Handle both request and command move types
- `ibdm-accom.2.5` [P1] Update existing integrate_request for new flow
- `ibdm-accom.2.6` [P1] Add integration tests for accommodation workflow

**Deliverable**: Request moves trigger plan creation in integration phase

---

#### Phase 3: ibdm-accom.3 - Clean Up Deprecated Code
**Priority**: P1 | **Tasks**: 3 | **Time**: 1 hour

- `ibdm-accom.3.1` [P1] Remove deprecated NDA accommodation from interpretation_rules.py
- `ibdm-accom.3.2` [P1] Remove task classifier from interpretation
- `ibdm-accom.3.3` [P2] Update interpretation docstrings for syntactic-only

**Deliverable**: Clean codebase with clear separation of concerns

---

#### Phase 4: ibdm-accom.4 - Enhance NLG with Plan Context
**Priority**: P1 | **Tasks**: 4 | **Time**: 2 hours

- `ibdm-accom.4.1` [P1] Add plan-aware question generation helper
- `ibdm-accom.4.2` [P1] Implement NDA-specific question templates
- `ibdm-accom.4.3` [P2] Add plan progress feedback in responses
- `ibdm-accom.4.4` [P2] Add fallback to generic generation

**Deliverable**: Natural, context-aware dialogue for NDA workflow

---

#### Phase 5: ibdm-accom.5 - Verify NLU Engine Integration
**Priority**: P1 | **Tasks**: 3 | **Time**: 1 hour

- `ibdm-accom.5.1` [P1] Verify NLU engine creates correct move types
- `ibdm-accom.5.2` [P1] Test NLU → integration → accommodation path
- `ibdm-accom.5.3` [P2] Add logging for accommodation debugging

**Deliverable**: NLU engine triggers accommodation correctly

---

#### Phase 6: ibdm-accom.6 - End-to-End Integration Testing
**Priority**: P1 | **Tasks**: 4 | **Time**: 2 hours

- `ibdm-accom.6.1` [P1] Create comprehensive NDA workflow integration test
- `ibdm-accom.6.2` [P1] Test with both rule-based and NLU interpretation
- `ibdm-accom.6.3` [P1] Manual testing with interactive demo
- `ibdm-accom.6.4` [P2] Performance testing and benchmarking

**Deliverable**: Fully working NDA workflow with natural conversation

---

#### Phase 7: ibdm-accom.7 - Update Documentation
**Priority**: P2 | **Tasks**: 4 | **Time**: 1 hour

- `ibdm-accom.7.1` [P2] Update architecture documentation
- `ibdm-accom.7.2` [P2] Update code comments and docstrings
- `ibdm-accom.7.3` [P2] Update CLAUDE.md with architectural principle
- `ibdm-accom.7.4` [P2] Update demo documentation

**Deliverable**: Complete, accurate documentation

---

## Work Flow

### Starting Work

1. Check ready tasks:
   ```bash
   grep '"status":"open"' .beads/issues.jsonl | grep 'ibdm-accom' | jq -r '"\(.id): \(.title)"'
   ```

2. Work through phases sequentially (Phase 1 → 2 → 3 → ...)

3. Within each phase, work on P0 tasks first, then P1, then P2

### Tracking Progress

Update task status in `.beads/issues.jsonl`:
- `"status": "in_progress"` - Currently working on
- `"status": "closed"` - Completed (add `"closed_at"` timestamp)

### Dependencies

- **Phase 2** depends on **Phase 1** (need basic request detection before accommodation)
- **Phase 3** depends on **Phase 2** (need new accommodation before removing old)
- **Phases 4-7** can be done in parallel after Phase 3

---

## Priority Breakdown

| Priority | Count | Description |
|----------|-------|-------------|
| P0 | 8 | Critical path - core refactoring |
| P1 | 19 | Important - testing and integration |
| P2 | 8 | Nice to have - polish and documentation |

---

## Testing Strategy

Each phase has test requirements:

- **Phase 1**: Unit tests for interpretation rules
- **Phase 2**: Unit tests for integration rules + accommodation
- **Phase 3**: Verify all tests still pass after cleanup
- **Phase 4**: Unit tests for NLG enhancements
- **Phase 5**: Integration tests for NLU engine
- **Phase 6**: End-to-end workflow tests
- **Phase 7**: Documentation review

**Run after each phase**:
```bash
pytest tests/unit/test_interpretation_rules.py -v
pytest tests/unit/test_integration_rules.py -v
pytest tests/unit/test_generation_rules.py -v
pytest tests/integration/ -v
```

---

## Success Metrics

### Phase 1 Complete
- ✅ Request detection rule exists
- ✅ NDA accommodation rule disabled (priority 0)
- ✅ Tests pass

### Phase 2 Complete
- ✅ Accommodation happens in integration phase
- ✅ Plans created for NDA requests
- ✅ First question pushed to QUD
- ✅ Integration tests pass

### Phase 3 Complete
- ✅ Old accommodation code removed
- ✅ No task classifier in interpretation
- ✅ All tests still pass

### Phase 4 Complete
- ✅ NLG generates context-aware questions
- ✅ NDA-specific templates work
- ✅ Plan progress shown to user

### Phase 5 Complete
- ✅ NLU engine creates request/command moves
- ✅ Accommodation triggers for NLU interpretation
- ✅ Logging shows accommodation flow

### Phase 6 Complete
- ✅ Complete NDA workflow test passes
- ✅ Both rule-based and NLU paths work identically
- ✅ Manual demo shows natural conversation
- ✅ No performance regression

### Phase 7 Complete
- ✅ All documentation updated
- ✅ Architecture docs reflect new design
- ✅ CLAUDE.md has architectural principle

---

## Quick Commands

**View all accommodation tasks**:
```bash
grep 'ibdm-accom' .beads/issues.jsonl | jq -r '"\(.id): \(.title) [\(.status)]"'
```

**View Phase 1 tasks**:
```bash
grep 'ibdm-accom.1' .beads/issues.jsonl | jq -r '"\(.id): \(.title) [\(.status)]"'
```

**View P0 tasks**:
```bash
grep 'ibdm-accom' .beads/issues.jsonl | jq 'select(.priority == 0)' | jq -r '"\(.id): \(.title)"'
```

**Count remaining tasks**:
```bash
grep 'ibdm-accom' .beads/issues.jsonl | jq 'select(.status == "open")' | wc -l
```

---

## References

- **Detailed Plan**: `docs/REFACTORING_PLAN_accommodation.md`
- **Architecture Analysis**: `docs/architecture_interpretation_accommodation.md`
- **Quick Summary**: `ARCHITECTURE_ISSUE_SUMMARY.md`
- **Task Generator**: `.claude/create-refactoring-tasks.py`
