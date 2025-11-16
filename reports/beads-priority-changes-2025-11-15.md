# Beads Priority Changes - ZFC Alignment
**Date**: 2025-11-15
**Session**: claude/align-beads-with-zfc-01VTe7NhqivT6qiM9D9fXnDB

## Summary

Reprioritized 45 beads tasks to align with ZFC (Zero Framework Cognition) selective compliance principles as defined in CLAUDE.md Policy #14.

## Key Principle

**Higher priority = More important work** (Priority scale: 0-3, where 3 is HIGHEST)

ZFC compliance strategy:
- ✅ **Use ZFC** (delegate to AI): Language processing (NLU/NLG), infrastructure orchestration
- ❌ **Violate ZFC** (explicit algorithms): Dialogue management (Larsson's update rules, QUD operations, semantic reasoning)

## Priority Changes

### Priority 3 (HIGHEST) - Larsson Core Algorithms

**Promoted from Priority 0 → 3:**
- `ibdm-brm` - Phase 1: Core Foundation
  - `ibdm-brm.1` - Data structures (Question, Answer, DialogueMove, InformationState)
  - `ibdm-brm.2` - Update rule system (UpdateRule, RuleSet)
  - `ibdm-brm.3` - DialogueMoveEngine
  - `ibdm-brm.4` - Unit tests

**Promoted from Priority 1 → 3:**
- `ibdm-63p.2` - Integration rules (QUD management, commitments, agenda)
- `ibdm-63p.3` - Selection rules (question answering, raising, clarification)

**Rationale**: These implement Larsson's dialogue algorithms - the core research contribution. This is an **intentional ZFC violation** because we need transparent, inspectable dialogue logic.

### Priority 2 - Infrastructure & Language Interfaces

**Promoted from Priority 1 → 2:**
- `ibdm-zfl` - Phase 2: Burr Integration
  - All Burr tasks except visualization

**Promoted from Priority 1 → 2:**
- `ibdm-63p` - Phase 3: Rule Development (epic)
- `ibdm-63p.1` - Interpretation rules (AI delegation)
- `ibdm-63p.4` - Generation rules (AI delegation)

**Promoted from Priority 0 → 2:**
- `ibdm-brm.5` - Serialization/deserialization

**Rationale**: Burr orchestration (ZFC-compliant) and language processing (ZFC-compliant via AI delegation) form the shell around the Larsson core.

### Priority 1 - Advanced Features

**Demoted from Priority 2 → 1:**
- `ibdm-x1g` - Phase 4: Accommodation
- `ibdm-okw` - Phase 6: Grounding and ICM

**Demoted from Priority 3 → 1:**
- `ibdm-tty` - Phase 5: Multi-Agent System

**Rationale**: These are extensions and advanced features. Important, but require the foundation first.

### Priority 0 (LOWEST) - End-Stage Work

**Demoted from Priority 1 → 0:**
- `ibdm-dus` - Phase 7: Integration and Testing
  - All testing, documentation, example tasks

**Demoted from Priority 3 → 0:**
- `ibdm-xeh` - Phase 8: Advanced Features
  - NLU/NLG integration, knowledge bases, learning, visualization

**Rationale**: Can't do end-to-end testing until foundational components exist. Advanced features are optional enhancements.

## Impact Analysis

### Before (ZFC-misaligned):
```
Priority 3: Advanced features, multi-agent
Priority 2: Accommodation, grounding, integration/testing
Priority 1: Burr, rules, interpretation/generation
Priority 0: Core foundation (Larsson algorithms) ← WRONG!
```

### After (ZFC-aligned):
```
Priority 3: Core foundation (Larsson algorithms) ← CORRECT!
Priority 2: Burr orchestration, language interfaces
Priority 1: Advanced dialogue features
Priority 0: End-to-end testing, optional enhancements
```

## Work Order

Following new priorities, recommended development sequence:

**Weeks 1-2** (Priority 3 - Larsson Core):
1. ✓ Data structures (ibdm-brm.1)
2. ✓ Update rules (ibdm-brm.2)
3. ✓ Integration rules (ibdm-63p.2) - moved from Phase 3
4. ✓ Selection rules (ibdm-63p.3) - moved from Phase 3
5. ✓ DialogueMoveEngine (ibdm-brm.3)
6. ✓ Tests (ibdm-brm.4)

**Week 3** (Priority 2 - Orchestration):
1. Burr state machine (ibdm-zfl.*)
2. Serialization (ibdm-brm.5)

**Week 4** (Priority 2 - Language):
1. Interpretation with AI (ibdm-63p.1)
2. Generation with AI (ibdm-63p.4)

**Weeks 5-8** (Priority 1 - Extensions):
- Accommodation (Phase 4)
- Multi-agent (Phase 5)
- Grounding/ICM (Phase 6)

**Weeks 9-10** (Priority 0 - Polish):
- Integration testing (Phase 7)
- Advanced features (Phase 8)

## Files Changed

- `.beads/issues.jsonl` - Updated 45 task priorities
- `.beads/update_priorities.py` - Script to apply priority updates
- `reports/beads-zfc-alignment-2025-11-15.md` - Detailed analysis
- `reports/beads-priority-changes-2025-11-15.md` - This summary

## Backup

Original beads database backed up to:
`.beads/issues.jsonl.backup-20251115-235842`

## Verification

Epic priorities after update:
- Priority 3: ibdm-brm (Core Foundation) ✓
- Priority 2: ibdm-zfl (Burr Integration) ✓
- Priority 2: ibdm-63p (Rule Development) ✓
- Priority 1: ibdm-x1g (Accommodation) ✓
- Priority 1: ibdm-tty (Multi-Agent) ✓
- Priority 1: ibdm-okw (Grounding/ICM) ✓
- Priority 0: ibdm-dus (Integration/Testing) ✓
- Priority 0: ibdm-xeh (Advanced Features) ✓

## Next Steps

1. Start work on Priority 3 tasks (Larsson core)
2. Build foundational data structures first
3. Implement update rules and engines
4. Wrap in Burr orchestration (Priority 2)
5. Add language interfaces with AI delegation (Priority 2)
6. Extend with advanced features (Priority 1)
7. Integration testing last (Priority 0)

This ordering ensures we build the **intentional ZFC violation zone** (Larsson algorithms) first, then wrap it in **ZFC-compliant** orchestration and language processing.

---

**Philosophy**: "Use AI for what humans are bad at (language). Use explicit algorithms for what we understand (dialogue)." - CLAUDE.md Policy #14
