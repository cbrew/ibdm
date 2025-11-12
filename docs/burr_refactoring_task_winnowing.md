# Beads Task Winnowing Analysis

**Date**: 2025-11-12
**Purpose**: Identify obsolete or conflicting tasks after Burr State Refactoring design

## Analysis Approach

Review all open beads tasks against the new Burr-centric architecture to:
1. Identify tasks made obsolete by the refactoring
2. Identify tasks that conflict with new design principles
3. Identify tasks that need updating for new architecture
4. Recommend actions (close, update, keep as-is)

## Review by Phase

### Phase 2: Burr Integration (ibdm-zfl.*)

| Task ID | Title | Status | Recommendation | Rationale |
|---------|-------|--------|----------------|-----------|
| ibdm-zfl | Phase 2 Epic | closed | ✓ Keep | Historical record |
| ibdm-zfl.1-5 | Core Burr tasks | closed | ✓ Keep | Completed, historical |
| ibdm-zfl.6 | Investigate skipped low-level Burr action tests | open | → **Close as superseded** | These tests will be completely rewritten during ibdm-bsr.21-22 refactoring |
| ibdm-zfl.7 | Fix end-to-end question-answer dialogue test | open | → **Close as superseded** | Will be addressed in ibdm-bsr.22 integration tests with new state architecture |
| ibdm-zfl.8 | Address Burr integration type checking warnings | open | → **Keep, update priority** | Still relevant; type issues may persist. Update to P1 after refactoring completes |
| ibdm-zfl.9 | Verify IBDM_API_KEY configured | closed | ✓ Keep | Completed |

**Actions**:
- Close ibdm-zfl.6 and ibdm-zfl.7 as superseded by refactoring
- Keep ibdm-zfl.8 but defer until after ibdm-bsr completes

### Phase 3.5: LLM-Enhanced NLU (ibdm-64.*)

| Task ID | Title | Status | Recommendation | Rationale |
|---------|-------|--------|----------------|-----------|
| ibdm-64 | Phase 3.5 Epic | open | ✓ Keep | Ongoing work |
| ibdm-64.1-10 | Core NLU tasks | closed | ✓ Keep | Completed |
| ibdm-64.11 | Implement intent recognition | open | ✓ Keep | Not affected by refactoring |
| ibdm-64.12 | Pragmatic understanding | open | ✓ Keep | Not affected by refactoring |
| ibdm-64.13 | Confidence scoring | open | → **Simplify** | Conflicts with "no fallbacks" principle; simplify to basic confidence without cascading |
| ibdm-64.14 | Fallback strategies and hybrid | open | → **Close as obsolete** | Directly contradicts user guidance: "no fallbacks" |
| ibdm-64.15 | Caching and performance | open | ✓ Keep | Still relevant for performance |
| ibdm-64.16 | Error handling and recovery | open | → **Simplify** | Remove retry strategies, fallbacks; keep basic error logging |
| ibdm-64.17 | Integrate NLU with IBDM | closed | ✓ Keep | Completed |
| ibdm-64.18 | NLU test suite | open | → **Update** | Tests will need updating for stateless engine (covered by ibdm-bsr.21) |
| ibdm-64.19 | NLU benchmark | open | ✓ Keep | Still relevant |
| ibdm-64.20 | NLU documentation | open | → **Update** | Docs need updating for new architecture (covered by ibdm-bsr.24) |

**Actions**:
- Close ibdm-64.14 (hybrid fallback) as obsolete per user guidance
- Update ibdm-64.13 to remove cascading logic
- Update ibdm-64.16 to remove retry/circuit breaker complexity
- Note that ibdm-64.18 and ibdm-64.20 will be addressed by ibdm-bsr.21 and ibdm-bsr.24

### Demo Suite (ibdm-dem.*)

| Task ID | Title | Status | Recommendation | Rationale |
|---------|-------|--------|----------------|-----------|
| ibdm-dem | Demo Suite Epic | open | ✓ Keep, update | Demos showcase capabilities; update to reflect new architecture |
| ibdm-dem.1 | Stage 1: Foundation demo | open | → **Update** | Update to show stateless engine, Burr state visibility |
| ibdm-dem.2 | Stage 2: Context demo | open | → **Update** | Update to show NLUContext in Burr state |
| ibdm-dem.3 | Stage 3: Hybrid strategy demo | open | → **Close as obsolete** | Hybrid strategy removed per user guidance |
| ibdm-dem.1.1-1.7 | Stage 1 subtasks | open | → **Update** | Update for new architecture |
| ibdm-dem.1.4 | Pre-scripted dialogue scenarios | open | → **Update priority to P0** | Good scenarios; update for new architecture |

**Actions**:
- Close ibdm-dem.3 (hybrid strategy showcase) as obsolete
- Update ibdm-dem.1 and ibdm-dem.2 descriptions to mention new Burr-centric architecture
- Consider adding ibdm-dem.4: "Stage 3: Burr State Visualization Demo" to showcase state inspection

### Phase 5: Multi-Agent (ibdm-tty.*)

| Task ID | Title | Status | Recommendation | Rationale |
|---------|-------|--------|----------------|-----------|
| ibdm-tty | Phase 5 Epic | open | ✓ Keep | Still planned |
| ibdm-tty.1-6 | Multi-agent tasks | open | ✓ Keep, note dependency | These tasks will be **easier** with Burr-centric state; mark as blocked by ibdm-bsr |

**Actions**:
- Add note to ibdm-tty.* tasks: "Blocked by ibdm-bsr completion; new architecture will simplify multi-agent state management"

### Phase 6: Grounding/ICM (ibdm-okw.*)

| Task ID | Title | Status | Recommendation | Rationale |
|---------|-------|--------|----------------|-----------|
| ibdm-okw | Phase 6 Epic | open | ✓ Keep | Still planned |
| ibdm-okw.1-4 | Grounding tasks | open | ✓ Keep | Not affected by refactoring |

**Actions**:
- No changes needed

### Phase 7: Integration/Testing (ibdm-dus.*)

| Task ID | Title | Status | Recommendation | Rationale |
|---------|-------|--------|----------------|-----------|
| ibdm-dus | Phase 7 Epic | open | ✓ Keep | Still planned |
| ibdm-dus.1 | End-to-end integration tests | open | → **Note overlap** | Will overlap with ibdm-bsr.22 |
| ibdm-dus.2-5 | Other phase 7 tasks | open | ✓ Keep | Still relevant |

**Actions**:
- Add note to ibdm-dus.1: "Coordinate with ibdm-bsr.22 to avoid duplication"

### Phase 8: Advanced Features (ibdm-xeh.*)

| Task ID | Title | Status | Recommendation | Rationale |
|---------|-------|--------|----------------|-----------|
| ibdm-xeh | Phase 8 Epic | open | ✓ Keep | Future work |
| ibdm-xeh.1-5 | Advanced features | open | ✓ Keep | Not affected by refactoring |

**Actions**:
- No changes needed

### Standalone Tasks

| Task ID | Title | Status | Recommendation | Rationale |
|---------|-------|--------|----------------|-----------|
| ibdm-65 | Verify Gemini API key | open | → **Close as obsolete** | Project using Claude (IBDM_API_KEY) only per CLAUDE.md |

**Actions**:
- Close ibdm-65 as obsolete (using Claude only)

## Summary of Actions

### Tasks to Close (Obsolete/Superseded)

1. **ibdm-zfl.6**: Skipped Burr action tests → Superseded by ibdm-bsr.21-22
2. **ibdm-zfl.7**: Fix question-answer dialogue test → Superseded by ibdm-bsr.22
3. **ibdm-64.14**: Hybrid fallback strategies → Obsolete per user guidance (no fallbacks)
4. **ibdm-dem.3**: Hybrid strategy demo → Obsolete (no hybrid strategy)
5. **ibdm-65**: Verify Gemini API key → Obsolete (using Claude only)

**Total**: 5 tasks to close

### Tasks to Update (Description/Priority)

1. **ibdm-zfl.8**: Defer priority to P2, add note "Revisit after ibdm-bsr completion"
2. **ibdm-64.13**: Update description to remove cascading logic, simplify confidence scoring
3. **ibdm-64.16**: Simplify to basic error logging, remove retry/circuit breaker
4. **ibdm-64.18**: Add note "Will be updated as part of ibdm-bsr.21"
5. **ibdm-64.20**: Add note "Will be updated as part of ibdm-bsr.24"
6. **ibdm-dem.1**: Update description to mention Burr-centric architecture
7. **ibdm-dem.2**: Update description to mention NLUContext in Burr state
8. **ibdm-dem.1.4**: Increase priority to P0 (good test scenarios)
9. **ibdm-tty.1-6**: Add note "Blocked by ibdm-bsr; new architecture simplifies multi-agent"
10. **ibdm-dus.1**: Add note "Coordinate with ibdm-bsr.22"

**Total**: 10+ tasks to update

### Tasks to Keep As-Is

- All completed tasks (historical record)
- Phase 5-8 tasks (future work, not affected)
- Most NLU tasks (ibdm-64.11, 64.12, 64.15, 64.19)
- Most demo infrastructure tasks

**Total**: ~50 tasks unchanged

## New Tasks to Consider

Based on the refactoring, consider adding:

1. **ibdm-dem.4**: "Stage 4: Burr State Visualization Demo"
   - Show complete state inspection via Burr UI
   - Demonstrate rollback and time-travel
   - Visualize QUD stack evolution

2. **ibdm-bsr.26**: "Performance benchmarking before/after refactoring"
   - Ensure refactoring doesn't degrade performance
   - Measure state cloning overhead

3. **ibdm-bsr.27**: "Create Burr State schema documentation"
   - Document complete state schema
   - Provide TypedDict or Pydantic model for validation

## Implementation Plan

### Step 1: Close Obsolete Tasks (Immediate)

```bash
# Close tasks that are obsolete or superseded
bd close ibdm-zfl.6 --reason "Superseded by ibdm-bsr.21-22 refactoring"
bd close ibdm-zfl.7 --reason "Superseded by ibdm-bsr.22 integration tests"
bd close ibdm-64.14 --reason "Obsolete: No fallbacks per user guidance on clarity/simplicity"
bd close ibdm-dem.3 --reason "Obsolete: Hybrid strategy removed per user guidance"
bd close ibdm-65 --reason "Obsolete: Using Claude (IBDM_API_KEY) only per CLAUDE.md Policy #9"
```

### Step 2: Update Task Descriptions (Next)

For each task in "Tasks to Update", modify description/labels/priority in .beads/issues.jsonl

### Step 3: Create New Tasks (After refactoring starts)

Create ibdm-dem.4, ibdm-bsr.26-27 once ibdm-bsr work is underway

## Validation Checklist

- [x] Analyzed all open tasks
- [x] Identified conflicts with new design
- [x] Identified obsolete tasks
- [x] Recommended actions for each
- [x] Provided rationale
- [x] Created close commands
- [x] Identified new tasks to consider

## Risk Assessment

### Low Risk Closures
- ibdm-zfl.6, zfl.7: Low-priority test fixes, definitely superseded
- ibdm-64.14: Explicitly contradicts user guidance
- ibdm-dem.3: Demo for removed feature
- ibdm-65: Wrong API provider

### No Risks Identified
All closures are justified by either:
1. User's explicit "no fallbacks" guidance
2. Supersession by comprehensive refactoring tasks
3. Wrong technology choice (Gemini vs Claude)

## Next Steps

1. Execute Step 1 (close obsolete tasks) ✓ Ready
2. Update task descriptions per Step 2
3. Begin ibdm-bsr implementation
4. Create new demo task (ibdm-dem.4) during Phase 4
5. Re-evaluate after refactoring completion
