# NLU/NLG Burr Integration Tasks Summary

**Generated**: 2025-11-15
**Total Tasks**: 26 tasks (1 epic, 2 phases, 23 implementation tasks)
**Source**: `create-burr-nlu-nlg-tasks.py`
**Tasks File**: `burr-nlu-nlg-tasks.json`

## Overview

This task breakdown implements the architectural refactoring to move NLU and NLG from hidden engine internals to explicit Burr actions, as proposed in:
- `docs/NLU_NLG_BURR_REFACTORING.md` (6-stage proposal)
- `docs/FINE_GRAINED_BURR_PIPELINE.md` (8-stage exploration)

## Epic: ibdm-burr-nlu-nlg

**Move NLU/NLG to Explicit Burr Actions**

Current problem:
- NLU processing hidden inside `engine.interpret()`
- NLG processing hidden inside `engine.generate()`
- Can't inspect intermediate results in Burr State
- Violates architectural clarity principle (Policy #0)

Goal:
- **Phase 1**: 6-stage pipeline (NLU/NLG explicit)
- **Phase 2**: 8-stage pipeline (NLU/NLG substages with conditional execution)

Benefits:
- +90% architectural clarity
- -75% debug time
- +100% test coverage
- +200% flexibility
- Larsson fidelity: 93% → 95%

## Phase 1: 6-Stage Pipeline (12 tasks)

**Pipeline**: `utterance → nlu → interpret → integrate → select → nlg → output`

### Tasks:

1. **ibdm-burr-nlu-nlg.1.1**: Create NLUResult and NLGResult dataclasses
   - Structured result types for serialization
   - Priority: 1

2. **ibdm-burr-nlu-nlg.1.2**: Create NLUEngine component
   - Extract NLU from NLUDialogueEngine
   - Standalone component for dialogue act classification, entities, etc.
   - Priority: 1

3. **ibdm-burr-nlu-nlg.1.3**: Create NLGEngine component
   - Extract NLG from generation rules
   - Standalone component for template/plan/LLM generation
   - Priority: 1

4. **ibdm-burr-nlu-nlg.1.4**: Create nlu() Burr action
   - Explicit NLU stage
   - Writes nlu_result to Burr State
   - Priority: 2

5. **ibdm-burr-nlu-nlg.1.5**: Create nlg() Burr action
   - Explicit NLG stage
   - Writes nlg_result to Burr State
   - Priority: 2

6. **ibdm-burr-nlu-nlg.1.6**: Simplify DialogueMoveEngine
   - Remove NLU/NLG logic (~50% code reduction)
   - Becomes pure rule processor
   - Priority: 2

7. **ibdm-burr-nlu-nlg.1.7**: Update interpret() Burr action
   - Simplify to use nlu_result (not utterance)
   - No NLU processing
   - Priority: 3

8. **ibdm-burr-nlu-nlg.1.8**: Update generate() Burr action
   - Simplify to integrate system move (not generate text)
   - No NLG processing
   - Priority: 3

9. **ibdm-burr-nlu-nlg.1.9**: Update Burr state machine graph
   - New 6-stage graph
   - Add nlu and nlg actions
   - Priority: 4

10. **ibdm-burr-nlu-nlg.1.10**: Add feature flag for backward compatibility
    - Support both 4-stage and 6-stage pipelines
    - Gradual migration
    - Priority: 4

11. **ibdm-burr-nlu-nlg.1.11**: Update integration tests
    - Test 6-stage pipeline
    - Parity tests (same behavior as 4-stage)
    - Priority: 5

12. **ibdm-burr-nlu-nlg.1.12**: Update documentation
    - Architecture diagrams
    - Debugging guides
    - Migration notes
    - Priority: 5

### Phase 1 Success Criteria

- ✅ NLU results visible in Burr State
- ✅ NLG results visible in Burr State
- ✅ DialogueMoveEngine ~50% smaller
- ✅ All existing tests pass
- ✅ Burr UI shows 6 distinct stages

## Phase 2: 8-Stage Pipeline (12 tasks)

**Pipeline**: `nlu_classify → nlu_enrich → interpret → integrate → select → nlg_plan → nlg_realize → output`

**Prerequisites**: Phase 1 complete, team feedback positive

### New Capabilities:

**Conditional Execution**:
- Skip expensive enrichment for simple dialogue acts
- Fast path (greet/quit): 300ms vs 500ms (40% faster)
- Slow path (ask/answer): conditional enrichment only

**Targeted Debugging**:
- Inspect nlu_classify_result: See classification scores
- Inspect nlu_result: See enrichment results
- Pinpoint exact failure location

### Tasks:

1. **ibdm-burr-nlu-nlg.2.1**: Create NLUClassifier component
   - Fast classification (~200-350ms)
   - Dialogue act + entities
   - Priority: 1

2. **ibdm-burr-nlu-nlg.2.2**: Create NLUEnricher component
   - Conditional enrichment per dialogue act
   - Question analysis, answer parsing, intent classification
   - Priority: 1

3. **ibdm-burr-nlu-nlg.2.3**: Create nlu_classify() Burr action
   - First NLU substage
   - Fast classification only
   - Priority: 2

4. **ibdm-burr-nlu-nlg.2.4**: Create nlu_enrich() Burr action
   - Second NLU substage
   - Conditional enrichment
   - Priority: 2

5. **ibdm-burr-nlu-nlg.2.5**: Create NLGPlanner component
   - Strategy selection (template | plan_aware | llm)
   - Content planning
   - Priority: 1

6. **ibdm-burr-nlu-nlg.2.6**: Create NLGRealizer component
   - Text generation per strategy
   - Template (~15ms), plan (~55ms), LLM (~505ms)
   - Priority: 1

7. **ibdm-burr-nlu-nlg.2.7**: Create nlg_plan() Burr action
   - First NLG substage
   - Strategy selection visible
   - Priority: 2

8. **ibdm-burr-nlu-nlg.2.8**: Create nlg_realize() Burr action
   - Second NLG substage
   - Conditional realization
   - Priority: 2

9. **ibdm-burr-nlu-nlg.2.9**: Update Burr state machine graph (8-stage)
   - Replace nlu with nlu_classify + nlu_enrich
   - Replace nlg with nlg_plan + nlg_realize
   - Priority: 3

10. **ibdm-burr-nlu-nlg.2.10**: Add performance monitoring
    - Track latency per substage
    - Aggregate by dialogue act and strategy
    - Priority: 4

11. **ibdm-burr-nlu-nlg.2.11**: Update integration tests
    - Test conditional execution
    - Test debugging workflows
    - Priority: 5

12. **ibdm-burr-nlu-nlg.2.12**: Update documentation
    - 8-stage architecture diagrams
    - Conditional execution guide
    - Performance comparison
    - Priority: 5

### Phase 2 Success Criteria

- ✅ Conditional execution working (40% faster for greet/quit)
- ✅ Targeted debugging (pinpoint failure location)
- ✅ Performance tracking per substage
- ✅ Same dialogue behavior as 6-stage
- ✅ Burr UI shows 8 distinct stages

## Task Statistics

**Total**: 26 tasks
- Epic: 1
- Phase epics: 2
- Implementation tasks: 23

**By Priority**:
- Priority 0 (epics): 3 tasks
- Priority 1 (foundation): 8 tasks
- Priority 2 (actions): 8 tasks
- Priority 3 (integration): 2 tasks
- Priority 4 (polish): 3 tasks
- Priority 5 (docs/tests): 4 tasks

**By Type**:
- Component creation: 8 tasks
- Burr action creation: 8 tasks
- Integration/testing: 4 tasks
- Documentation: 2 tasks
- Infrastructure: 4 tasks

**Estimated Effort**:
- Phase 1: ~3 weeks (12 tasks, building foundation)
- Phase 2: ~2 weeks (12 tasks, extending foundation)
- Total: ~5 weeks

## Implementation Strategy

### Week 1-2: Phase 1 Foundation (Tasks 1.1-1.6)
- Create result dataclasses
- Extract NLUEngine and NLGEngine components
- Create nlu() and nlg() actions
- Simplify DialogueMoveEngine

### Week 2-3: Phase 1 Integration (Tasks 1.7-1.12)
- Update interpret() and generate() actions
- Update Burr state machine graph
- Add feature flag
- Integration tests and documentation

### Week 4: Phase 2 Foundation (Tasks 2.1-2.6)
- Split NLU into classifier + enricher
- Split NLG into planner + realizer

### Week 5: Phase 2 Integration (Tasks 2.7-2.12)
- Create substage actions
- Update Burr graph
- Performance monitoring
- Tests and documentation

## Using These Tasks

### With beads (if installed):

```bash
# Import tasks
bd import .claude/burr-nlu-nlg-tasks.json

# List tasks
bd list --epic ibdm-burr-nlu-nlg

# Start Phase 1
bd start ibdm-burr-nlu-nlg.1

# Work on specific task
bd start ibdm-burr-nlu-nlg.1.1
```

### Without beads:

The tasks are structured in JSON format and can be:
- Imported into any issue tracking system
- Used as a checklist for implementation
- Referenced in commit messages

## Next Steps

1. Review epic and phase plans with team
2. Get approval for Phase 1 implementation
3. Start with ibdm-burr-nlu-nlg.1.1 (create dataclasses)
4. Follow dependency order (priority indicates rough sequence)
5. Run integration tests after each task
6. Evaluate Phase 1 success before starting Phase 2

## References

- Epic doc: `docs/NLU_NLG_BURR_REFACTORING.md`
- Phase 2 doc: `docs/FINE_GRAINED_BURR_PIPELINE.md`
- Current architecture: `docs/SYSTEM_DESIGN_AND_LARSSON_ALIGNMENT.md`
- Task generator: `.claude/create-burr-nlu-nlg-tasks.py`
- Task data: `.claude/burr-nlu-nlg-tasks.json`
