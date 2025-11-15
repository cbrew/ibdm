# Demo-Focused Task Reorganization
**Date**: 2025-11-15
**Author**: Claude
**Purpose**: Refocus project on core demonstration goals

## Top-Level Goals

The project has **3 demonstration goals**:

### Goal 1: Larsson-Faithful IBDM (**ibdm-82**)
**Demonstrate** issue-based dialogue management following Larsson (2002):
- QUD stack (LIFO question resolution)
- Four-phase control loop (interpret, integrate, select, generate)
- Task plan execution with subplan progression
- Information state tracking (private, shared, control)
- Clarification handling for invalid answers

**Deliverable**: Interactive demo (`demos/03_nlu_integration_interactive.py`)

### Goal 2: LLM-Powered Natural Language (**ibdm-83**)
**Demonstrate** LLM integration for natural language:
- NLU: Claude interprets utterances → DialogueMoves/Questions
- NLG: Generate natural responses from dialogue moves
- Domain-independent NLU/NLG infrastructure

**Deliverable**: Natural language dialogue using Claude 4.5

### Goal 3: Domain Portability (**ibdm-84**)
**Demonstrate** domain independence:
- Same IBDM core works with multiple domains
- Domain abstraction layer (predicates, sorts, plan builders)
- Easy domain switching (NDA ↔ Travel)

**Deliverable**: Demo working with 2+ domains

## Priority Restructuring

### P0 - ESSENTIAL FOR DEMO (Focus here)
**Epics**:
- ibdm-82: Demo Goal 1 (Larsson-Faithful)
- ibdm-83: Demo Goal 2 (LLM NLU/NLG)
- ibdm-84: Demo Goal 3 (Domain Portability)
- ibdm-loop: Interactive dialogue loop
- ibdm-66: NLU/NLG domain separation
- ibdm-dem: Demo suite
- ibdm-accom: Accommodation (Phases 1-2 complete)

**Critical Tasks** (~20 tasks):
1. **ibdm-loop.3**: Handle invalid answers with clarification
2. **ibdm-loop.11**: Verify QUD management
3. **ibdm-loop.12**: Verify plan progress
4. **ibdm-66.1**: Create NLG module infrastructure
5. **ibdm-67.1**: Create template engine
6. **ibdm-84.1**: Verify NDA domain
7. **ibdm-85**: Verify Travel domain
8. **ibdm-86**: Domain switching demo
9. **ibdm-87-88**: End-to-end domain validation
10. **ibdm-dem.1.x**: Demo infrastructure (7 subtasks)

### P1 - NICE TO HAVE
- ibdm-64: LLM-Enhanced NLU (mostly complete)
- Additional demo stages
- Enhanced NLG features

### P2 - DEFER TO POST-DEMO
- ibdm-dus: Integration and testing infrastructure

### P3 - ARCHIVE (Post-demo quality work)
**Moved from P0/P1** (~140 tasks):
- **ibdm-bsr**: Burr State Refactoring (Phases 2-5)
  - 15 tasks about pure functions, internal refactoring
  - Important but not visible in demo
- **ibdm-metrics**: Larsson Fidelity Metrics
  - 38 tasks for comprehensive metrics framework
  - Validation, not demonstration
- **ibdm-tty**: Multi-Agent System
  - 7 tasks for future multi-agent features
  - Not in scope for initial demo
- **ibdm-okw**: Grounding and ICM
  - 5 tasks for advanced dialogue features
  - Future enhancement
- **ibdm-xeh**: Advanced Features
  - 6 tasks for learning, adaptation, visualization
  - Future enhancement

## Task Count Changes

**Before**:
- P0: 73 tasks
- P1: 76 tasks
- P2: 65 tasks
- P3: 9 tasks
- Total: 223 tasks

**After**:
- P0: ~25 tasks (demo-essential)
- P1: ~10 tasks (nice-to-have)
- P2: ~15 tasks (infrastructure)
- P3: ~173 tasks (post-demo)
- Total: 223 tasks

**Impact**: Focus reduced from 149 tasks to ~25 essential tasks

## New Demo-Specific Tasks Created

1. **ibdm-84.1**: Verify NDA domain completeness
2. **ibdm-85**: Verify Travel domain completeness
3. **ibdm-86**: Domain switching in interactive demo
4. **ibdm-87**: NDA end-to-end validation
5. **ibdm-88**: Travel end-to-end validation

## What Changed

### Kept at P0 (Demo-Essential)
✅ ibdm-loop (dialogue loop completion)
✅ ibdm-66 (NLU/NLG domain separation)
✅ ibdm-dem (demo suite)
✅ ibdm-accom Phases 1-2 (already complete)

### Lowered to P3 (Post-Demo)
⬇️ ibdm-bsr Phases 2-5 (stateless engine refactoring)
⬇️ ibdm-metrics (comprehensive metrics)
⬇️ ibdm-tty (multi-agent)
⬇️ ibdm-okw (grounding/ICM)
⬇️ ibdm-xeh (advanced features)

## Demonstration Path

### Phase 1: Core Loop (2-3 weeks)
1. Implement ibdm-loop.3 (clarification)
2. Verify QUD management (ibdm-loop.11)
3. Verify plan progression (ibdm-loop.12)
4. Polish existing demo

**Milestone**: Working NDA demo with LLM, QUD, plans, clarification

### Phase 2: Domain-Independent NLG (1-2 weeks)
1. Create NLG infrastructure (ibdm-66.1)
2. Template engine (ibdm-67.1)
3. Separate domain-specific from generic

**Milestone**: Clean NLU/NLG separation, maintainable

### Phase 3: Domain Portability (1-2 weeks)
1. Complete NDA domain (ibdm-84.1)
2. Complete Travel domain (ibdm-85)
3. Add domain switching (ibdm-86)
4. Validate both domains (ibdm-87, ibdm-88)

**Milestone**: Same demo works with NDA or Travel domain

### Phase 4: Demo Polish (1 week)
1. Complete demo infrastructure (ibdm-dem.1.x)
2. User documentation
3. Demo script and video
4. Performance optimization

**Milestone**: Polished, documented, presentable demo

## Success Criteria

**Demo is complete when:**

1. ✅ User can complete multi-turn task (NDA or Travel)
2. ✅ Natural language input/output (LLM-powered)
3. ✅ QUD stack correctly manages question resolution
4. ✅ Plans progress through subgoals
5. ✅ Invalid answers trigger clarification
6. ✅ Same demo works with 2+ domains
7. ✅ Domain switching at runtime
8. ✅ Information state correctly tracked
9. ✅ All Larsson core algorithms visible

**Then and only then**: Return to quality work (metrics, refactoring, advanced features)

## Rationale

### Why This Refocus?

**Problem**: 223 tasks, no clear path to demonstration
**Solution**: 3 concrete demo goals, ~25 essential tasks

**Benefits**:
1. **Clear objective**: Working demo, not perfect architecture
2. **Measurable progress**: Can demo actually work?
3. **Motivating**: See results, not just refactoring
4. **Validating**: Demo shows if theory works
5. **Presentable**: Something to show, not just code

**Post-Demo Work**:
- After demo validated, return to quality work
- Metrics to measure Larsson fidelity
- Refactoring for maintainability
- Advanced features (multi-agent, grounding)
- Test infrastructure

But **demonstration comes first**.

## Next Steps

1. Start with **ibdm-loop.3** (clarification handling) - highest impact
2. Then **ibdm-66.1** (NLG infrastructure) - enables domain separation
3. Then **ibdm-84.1/85** (domain completeness) - enables portability
4. Polish demo throughout

**Timeline**: 6-8 weeks to working, presentable demo

## Files Modified

- Created 3 new demo goal epics (ibdm-82, ibdm-83, ibdm-84)
- Created 5 new domain portability tasks (ibdm-84.1, ibdm-85-88)
- Lowered priority of 140+ tasks to P3
- Created `/tmp/filter-tasks.sh` for task analysis
- Created this report

## Conclusion

**Before**: 149 open P0/P1 tasks, unclear path
**After**: 25 essential P0 tasks, clear demonstration path

**Focus**: Build a working demo that shows:
1. Larsson's IBDM works
2. LLMs integrate cleanly
3. Domains are portable

**Everything else waits until the demo is validated.**
