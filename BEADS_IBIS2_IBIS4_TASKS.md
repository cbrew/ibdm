# IBiS2 and IBiS4 Beads Task Breakdown

**Created**: 2025-11-16
**Total Tasks**: 47 (21 IBiS2 + 26 IBiS4)

This document provides a comprehensive breakdown of all beads tasks created for IBiS2 and IBiS4 implementation. All tasks are now tracked in `.beads/issues.jsonl` and can be managed using beads commands.

---

## IBiS2: Grounding & Interactive Communication Management

**Epic**: `ibdm-98`
**Total Tasks**: 20
**Duration**: 6-8 weeks
**Priority**: P1 (High)
**Larsson Reference**: Chapter 3

### Week 1-2: Information State Extensions (3 tasks)

| Task ID | Title | Description |
|---------|-------|-------------|
| `ibdm-98.1` | Add grounding fields to SharedIS | Add `moves: list[Move]` and `next_moves: list[Move]` to SharedIS |
| `ibdm-98.2` | Create grounding status tracking module | Create `src/ibdm/core/grounding.py` with GroundingStatus enum |
| `ibdm-98.3` | Update serialization for grounding fields | Update to_dict/from_dict for new fields |

### Week 3-5: ICM Taxonomy Implementation (6 tasks)

| Task ID | Title | Description |
|---------|-------|-------------|
| `ibdm-98.4` | Implement ICM move types | Add all ICM move types to `src/ibdm/core/moves.py` |
| `ibdm-98.5` | Implement ICM Rule 3.1: IntegratePerPos | Positive perception integration rule |
| `ibdm-98.6` | Implement ICM Rule 3.5: IntegrateUndPos | Positive understanding integration rule |
| `ibdm-98.7` | Implement ICM Rule 3.15: Reraising | Reraising rule for grounding failure |
| `ibdm-98.8` | Implement ICM Rule 3.20: Confirmation | Confirmation rule for low-confidence |
| `ibdm-98.9` | Implement remaining 23 ICM update rules | All other ICM rules (3.2-3.4, 3.6-3.14, 3.16-3.19, 3.21-3.27) |

### Week 6: Grounding Strategies (2 tasks)

| Task ID | Title | Description |
|---------|-------|-------------|
| `ibdm-98.10` | Implement grounding strategy selection | Optimistic, Cautious, Pessimistic strategies |
| `ibdm-98.11` | Implement evidence requirements | Define evidence needed per utterance type |

### Week 7: Perception Checking (2 tasks)

| Task ID | Title | Description |
|---------|-------|-------------|
| `ibdm-98.12` | Implement perception checking for low ASR confidence | Trigger icm:per*neg for low confidence |
| `ibdm-98.13` | Implement spelling confirmation | Spelling confirmation for critical entities |

### Week 8: Integration & Testing (7 tasks)

| Task ID | Title | Description |
|---------|-------|-------------|
| `ibdm-98.14` | Create ICM unit tests | Unit tests for all 27 ICM rules |
| `ibdm-98.15` | Create grounding integration tests | Integration tests for grounding scenarios |
| `ibdm-98.16` | Test grounding strategies end-to-end | End-to-end tests for all strategies |
| `ibdm-98.17` | Update SYSTEM_ACHIEVEMENTS.md with IBiS2 completion | Document IBiS2 achievements |
| `ibdm-98.18` | Update LARSSON_PRIORITY_ROADMAP.md with IBiS2 progress | Update roadmap with completion |
| `ibdm-98.19` | Create IBiS2 implementation guide | Comprehensive implementation documentation |
| `ibdm-98.20` | Measure IBiS2 Larsson fidelity | Measure compliance with Chapter 3 |

---

## IBiS4: Actions & Negotiative Dialogue

**Epic**: `ibdm-99`
**Total Tasks**: 25
**Duration**: 8-10 weeks
**Priority**: P2 (Medium)
**Larsson Reference**: Chapter 5

### Week 1-2: Information State Extensions (3 tasks)

| Task ID | Title | Description |
|---------|-------|-------------|
| `ibdm-99.1` | Add action fields to PrivateIS | Add `actions: list[Action]` and `iun: set[Proposition]` |
| `ibdm-99.2` | Create Action and Proposition classes | Create `src/ibdm/core/actions.py` with Action and Proposition |
| `ibdm-99.3` | Update serialization for action fields | Update to_dict/from_dict for action fields |

### Week 3-4: Device Interface & Actions (4 tasks)

| Task ID | Title | Description |
|---------|-------|-------------|
| `ibdm-99.4` | Define device interface protocol | Create `src/ibdm/interfaces/device.py` with DeviceInterface |
| `ibdm-99.5` | Implement postcond() function | Add postcond() to domain.py for action effects |
| `ibdm-99.6` | Implement action precondition checking | Validate preconditions before execution |
| `ibdm-99.7` | Create mock device for testing | Mock device implementing DeviceInterface |

### Week 5-6: Negotiation (4 tasks)

| Task ID | Title | Description |
|---------|-------|-------------|
| `ibdm-99.8` | Implement Issues Under Negotiation (IUN) | IUN state management and conflict detection |
| `ibdm-99.9` | Implement negotiation accommodation rules | Rules for accommodating proposals to IUN |
| `ibdm-99.10` | Implement accept/reject negotiation moves | Handle acceptance/rejection in negotiation |
| `ibdm-99.11` | Implement counter-proposal generation | Generate counter-proposals on rejection |

### Week 7-8: Action Execution (4 tasks)

| Task ID | Title | Description |
|---------|-------|-------------|
| `ibdm-99.12` | Implement action execution integration rule | Execute actions when preconditions met |
| `ibdm-99.13` | Implement action confirmation selection rule | Request user confirmation before execution |
| `ibdm-99.14` | Implement action result handling | Handle success, failure, partial results |
| `ibdm-99.15` | Implement action rollback on failure | Rollback mechanism for failed actions |

### Week 9-10: Domain Integration & Testing (10 tasks)

| Task ID | Title | Description |
|---------|-------|-------------|
| `ibdm-99.16` | Add actions to NDA domain | Extend NDA domain with document actions |
| `ibdm-99.17` | Add actions to travel domain | Extend travel domain with booking actions |
| `ibdm-99.18` | Create action execution unit tests | Unit tests for action system |
| `ibdm-99.19` | Create negotiation integration tests | Integration tests for negotiation |
| `ibdm-99.20` | Create end-to-end action tests | End-to-end action workflow tests |
| `ibdm-99.21` | Update SYSTEM_ACHIEVEMENTS.md with IBiS4 completion | Document IBiS4 achievements |
| `ibdm-99.22` | Update LARSSON_PRIORITY_ROADMAP.md with IBiS4 progress | Update roadmap with completion |
| `ibdm-99.23` | Create IBiS4 implementation guide | Comprehensive implementation documentation |
| `ibdm-99.24` | Measure IBiS4 Larsson fidelity | Measure compliance with Chapter 5 |
| `ibdm-99.25` | Create IBiS4 demo application | Demo showing action planning and negotiation |

---

## Task Management Commands

Once beads is installed, use these commands to manage tasks:

```bash
# View all IBiS2 tasks
bd list 'ibdm-98*'

# View all IBiS4 tasks
bd list 'ibdm-99*'

# Show details of a specific task
bd show ibdm-98.1

# Start working on a task
bd start ibdm-98.1

# Mark task as complete
bd close ibdm-98.1 "Implemented grounding fields"

# View ready tasks (those you can start)
bd ready

# View current in-progress tasks
bd current
```

## Installation

To install beads (if not already installed):

```bash
GOTOOLCHAIN=auto go install github.com/steveyegge/beads/cmd/bd@latest
# Ensure $HOME/go/bin is in your PATH
export PATH="$HOME/go/bin:$PATH"
```

---

## Implementation Order Recommendation

### Phase 1: IBiS2 First (Recommended)
**Why**: Grounding and robustness are foundation for production systems

1. Start with `ibdm-98.1` - `ibdm-98.3` (Information State)
2. Proceed week by week through ICM implementation
3. Complete with testing and documentation

**After IBiS2**: System will have production-ready error handling and grounding

### Phase 2: IBiS4 After IBiS2
**Why**: Actions build on robust grounding from IBiS2

1. Start with `ibdm-99.1` - `ibdm-99.3` (Information State)
2. Build device interface and action system
3. Add negotiation capabilities
4. Complete with domain integration and testing

**After IBiS4**: System will have full action execution and negotiation

---

## Progress Tracking

Update `NEXT-TASK.md` as you complete tasks:

- Mark weeks complete as you finish them
- Update progress percentages (IBiS2: 60% → 100%, IBiS4: 10% → 100%)
- Document key achievements and learnings
- Measure Larsson fidelity at completion

---

## References

- **IBIS_VARIANTS_PRIORITY.md**: Detailed rationale for IBiS2 and IBiS4
- **LARSSON_PRIORITY_ROADMAP.md**: Overall project roadmap
- **Larsson (2002) Thesis**: Chapter 3 (IBiS2), Chapter 5 (IBiS4)
- **CLAUDE.md**: Development policies and workflow

---

**Status**: ✅ All tasks created and ready for implementation
**Next Step**: Install beads and start with `ibdm-98.1` (Add grounding fields to SharedIS)
