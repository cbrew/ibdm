# Burr State Refactoring: Consistency Check

**Date**: 2025-11-12
**Purpose**: Verify consistency between design document and beads tasks

## Design Document vs Beads Tasks Mapping

### Epic

| Document Section | Beads Task | Status |
|-----------------|------------|--------|
| Burr-Centric State Refactoring | ibdm-bsr | ✓ Created |

### Phase 1: State Extraction

| Design Document Item | Beads Task | Match |
|---------------------|------------|-------|
| Move InformationState from engine to Burr State | ibdm-bsr.1 | ✓ |
| Update initialize action to create IS in Burr | ibdm-bsr.2 | ✓ |

**Coverage**: 2/2 items ✓

### Phase 2: Stateless Engine Methods

| Design Document Item | Beads Task | Match |
|---------------------|------------|-------|
| Convert interpret() to accept state parameter | ibdm-bsr.3 | ✓ |
| Convert integrate() to pure function | ibdm-bsr.4 | ✓ |
| Convert select_action() to accept state | ibdm-bsr.5 | ✓ |
| Convert generate() to accept state | ibdm-bsr.6 | ✓ |
| Remove self.state from DialogueMoveEngine | ibdm-bsr.7 | ✓ |

**Coverage**: 5/5 items ✓

### Phase 3: Burr Actions Refactoring

| Design Document Item | Beads Task | Match |
|---------------------|------------|-------|
| Update interpret action to read/write IS | ibdm-bsr.8 | ✓ |
| Update integrate action to read/write IS | ibdm-bsr.9 | ✓ |
| Update select action to read IS | ibdm-bsr.10 | ✓ |
| Update generate action to read/write IS | ibdm-bsr.11 | ✓ |
| Update DialogueStateMachine wrapper | ibdm-bsr.12 | ✓ |

**Coverage**: 5/5 items ✓

### Phase 4: NLU State Integration

| Design Document Item | Beads Task | Match |
|---------------------|------------|-------|
| Create NLUContext dataclass | ibdm-bsr.13 | ✓ |
| Refactor EntityTracker to use NLUContext | ibdm-bsr.14 | ✓ |
| Refactor ReferenceResolver to use NLUContext | ibdm-bsr.15 | ✓ |
| Update NLUDialogueEngine to use NLUContext | ibdm-bsr.16 | ✓ |
| Add nlu_context to Burr State schema | ibdm-bsr.17 | ✓ |

**Coverage**: 5/5 items ✓

### Phase 5: Configuration Simplification

| Design Document Item | Beads Task | Match |
|---------------------|------------|-------|
| Remove hybrid fallback strategy | ibdm-bsr.18 | ✓ |
| Simplify NLUEngineConfig | ibdm-bsr.19 | ✓ |
| Remove conditional NLU initialization | ibdm-bsr.20 | ✓ |

**Coverage**: 3/3 items ✓

### Testing and Documentation

| Design Document Item | Beads Task | Match |
|---------------------|------------|-------|
| Update unit tests for stateless engine | ibdm-bsr.21 | ✓ |
| Update integration tests for Burr schema | ibdm-bsr.22 | ✓ |
| Add state schema validation | ibdm-bsr.23 | ✓ |
| Update documentation | ibdm-bsr.24 | ✓ |
| Create migration guide | ibdm-bsr.25 | ✓ |

**Coverage**: 5/5 items ✓

## Implementation Checklist Cross-Reference

Checking design document's "Implementation Checklist" against beads tasks:

| Checklist Item | Covered By | Match |
|---------------|------------|-------|
| Create NLUContext dataclass | ibdm-bsr.13 | ✓ |
| Refactor DialogueMoveEngine to stateless | ibdm-bsr.3-7 | ✓ |
| Update interpret() signature | ibdm-bsr.3 | ✓ |
| Update integrate() signature | ibdm-bsr.4 | ✓ |
| Update select_action() signature | ibdm-bsr.5 | ✓ |
| Update generate() signature | ibdm-bsr.6 | ✓ |
| Remove self.state | ibdm-bsr.7 | ✓ |
| Update initialize action | ibdm-bsr.2 | ✓ |
| Update interpret action | ibdm-bsr.8 | ✓ |
| Update integrate action | ibdm-bsr.9 | ✓ |
| Update select action | ibdm-bsr.10 | ✓ |
| Update generate action | ibdm-bsr.11 | ✓ |
| Refactor NLUDialogueEngine | ibdm-bsr.16 | ✓ |
| Remove hybrid fallback | ibdm-bsr.18 | ✓ |
| Simplify NLUEngineConfig | ibdm-bsr.19 | ✓ |
| Update all tests | ibdm-bsr.21, ibdm-bsr.22 | ✓ |
| Update documentation | ibdm-bsr.24 | ✓ |
| Add state schema validation | ibdm-bsr.23 | ✓ |

**Total Coverage**: 100% ✓

## Summary

### Consistency Status: ✓ PASS

- **Total Beads Tasks**: 26 (1 epic + 25 tasks)
- **Design Document Phases**: 5
- **Coverage**: 100%
- **Alignment**: Complete

### Task Organization

Tasks are well-organized with:
- Clear phase grouping (Phase 1-5)
- Logical dependencies
- Appropriate priorities (0 for critical path, 1-2 for supporting)
- Consistent labeling

### Dependencies

Recommended execution order:
1. **Phase 1** (ibdm-bsr.1-2): Foundation - extract state
2. **Phase 2** (ibdm-bsr.3-7): Core refactor - stateless methods
3. **Phase 3** (ibdm-bsr.8-12): Integration - update Burr actions
4. **Phase 4** (ibdm-bsr.13-17): NLU - add NLUContext
5. **Phase 5** (ibdm-bsr.18-20): Cleanup - simplify config
6. **Testing/Docs** (ibdm-bsr.21-25): Validation - tests and docs

### Priorities

Critical path (P0):
- ibdm-bsr (epic)
- ibdm-bsr.1-11 (Phases 1-3 core tasks)
- ibdm-bsr.21-22 (Testing)

Supporting tasks (P1-P2):
- ibdm-bsr.12-20 (NLU and simplification)
- ibdm-bsr.23-25 (Validation and docs)

## Verification Checklist

- [x] All design document phases have corresponding beads tasks
- [x] Implementation checklist items mapped to tasks
- [x] Task priorities set appropriately
- [x] Task labels applied consistently
- [x] Task descriptions are clear and actionable
- [x] Dependencies implicitly clear through phase ordering
- [x] Epic created for tracking
- [x] No duplicate tasks
- [x] No missing critical items

## Notes

1. **Completeness**: Every item from the design document has a corresponding beads task
2. **Granularity**: Tasks are appropriately sized (not too large, not too small)
3. **Actionability**: Each task has clear acceptance criteria in description
4. **Traceability**: Can map from design doc to task and back
5. **Consistency**: Labels, priorities, and structure align with project standards

## Next Steps

1. Review this consistency check ✓
2. Winnow obsolete beads tasks (see next document)
3. Update CLAUDE.md with clarity/simplicity principles
4. Begin implementation starting with Phase 1
