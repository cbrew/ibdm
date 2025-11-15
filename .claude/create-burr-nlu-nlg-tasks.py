#!/usr/bin/env python3
"""Create beads tasks for NLU/NLG Burr integration refactoring."""

import hashlib
import json
from datetime import datetime, timezone


def content_hash(title: str, description: str = "") -> str:
    """Generate content hash for beads issue."""
    content = f"{title}\n{description}"
    return hashlib.sha256(content.encode()).hexdigest()


def create_issue(
    id: str,
    title: str,
    description: str = "",
    status: str = "open",
    priority: int = 1,
    issue_type: str = "task",
    labels: list = None,
    parent: str = None,
):
    """Create a beads issue dict."""
    now = datetime.now(timezone.utc).isoformat()

    issue = {
        "id": id,
        "content_hash": content_hash(title, description),
        "title": title,
        "description": description,
        "status": status,
        "priority": priority,
        "issue_type": issue_type,
        "created_at": now,
        "updated_at": now,
        "source_repo": ".",
        "labels": labels or [],
    }

    if status == "closed":
        issue["closed_at"] = now

    if parent:
        issue["parent"] = parent

    return issue


# Epic for the refactoring
epic = create_issue(
    id="ibdm-burr-nlu-nlg",
    title="Refactor: Move NLU/NLG to Explicit Burr Actions",
    description="""
Architectural refactoring to make NLU and NLG explicit stages in the Burr control loop.

Current problem:
- NLU processing hidden inside engine.interpret()
- NLG processing hidden inside engine.generate()
- Can't inspect intermediate results in Burr State
- Can't swap NLU/NLG strategies easily
- Violates architectural clarity principle (Policy #0)

Goal:
- Phase 1: 6-stage pipeline (nlu → interpret → integrate → select → nlg → output)
- Phase 2: 8-stage pipeline (nlu_classify → nlu_enrich → interpret → integrate → select → nlg_plan → nlg_realize → output)
- Improve debuggability, testability, flexibility
- Strengthen Larsson fidelity (93% → 95%)

See:
- docs/NLU_NLG_BURR_REFACTORING.md (6-stage proposal)
- docs/FINE_GRAINED_BURR_PIPELINE.md (8-stage exploration)
- docs/SYSTEM_DESIGN_AND_LARSSON_ALIGNMENT.md (current architecture)
""".strip(),
    issue_type="epic",
    priority=0,
    labels=["architecture", "refactoring", "burr", "nlu", "nlg", "clarity"],
)

# ============================================================================
# Phase 1: 6-Stage Pipeline (NLU/NLG Explicit)
# ============================================================================

phase1 = create_issue(
    id="ibdm-burr-nlu-nlg.1",
    title="Phase 1: Implement 6-stage pipeline (NLU/NLG explicit)",
    description="""
Move NLU and NLG from hidden engine internals to explicit Burr actions.

Pipeline: utterance → nlu → interpret → integrate → select → nlg → output

Steps:
1. Create NLUEngine and NLGEngine components
2. Create nlu() and nlg() Burr actions
3. Simplify DialogueMoveEngine (remove NLU/NLG logic)
4. Update Burr action graph
5. Add integration tests

Deliverable: 6-stage pipeline working with same behavior as current 4-stage

Success criteria:
- NLU results visible in Burr State (nlu_result field)
- NLG results visible in Burr State (nlg_result field)
- DialogueMoveEngine simplified (~50% code reduction)
- All existing tests pass
- Burr UI shows 6 distinct stages

See: docs/NLU_NLG_BURR_REFACTORING.md
""".strip(),
    parent="ibdm-burr-nlu-nlg",
    priority=0,
    labels=["architecture", "refactoring", "burr", "nlu", "nlg", "phase-1"],
)

# Phase 1 subtasks
phase1_tasks = [
    # Task 1.1: Create NLUResult and NLGResult dataclasses
    create_issue(
        id="ibdm-burr-nlu-nlg.1.1",
        title="Create NLUResult and NLGResult dataclasses",
        description="""
Create structured result types for NLU and NLG processing.

Files to create:
- src/ibdm/nlu/nlu_result.py

Classes:
- NLUResult: dialogue_act, confidence, entities, intent, question_details, answer_content
- Methods: to_dict(), from_dict() for Burr State serialization

Testing:
- tests/unit/test_nlu_result.py
- Test serialization round-trip
- Test field validation

Acceptance:
- NLUResult can be serialized to/from dict
- All fields properly typed
- Unit tests pass
""".strip(),
        parent="ibdm-burr-nlu-nlg.1",
        priority=1,
        labels=["nlu", "nlg", "dataclass", "phase-1"],
    ),
    # Task 1.2: Create NLUEngine component
    create_issue(
        id="ibdm-burr-nlu-nlg.1.2",
        title="Create NLUEngine component (extract from NLUDialogueEngine)",
        description="""
Extract NLU processing from NLUDialogueEngine into standalone component.

Files to create:
- src/ibdm/nlu/nlu_engine.py

Class NLUEngine:
- __init__(config: NLUEngineConfig)
- process(utterance, speaker, context) -> NLUResult
- update_context(nlu_result, context) -> NLUContext

Extract from NLUDialogueEngine:
- Dialogue act classification
- Entity extraction
- Question analysis
- Answer parsing
- Intent classification
- Reference resolution

Testing:
- tests/unit/test_nlu_engine.py
- Test each dialogue act type (ask, answer, command, greet, quit)
- Test entity extraction
- Test context updates

Acceptance:
- NLUEngine produces same results as NLUDialogueEngine.interpret()
- All NLU tests pass
- No dependencies on DialogueMoveEngine
""".strip(),
        parent="ibdm-burr-nlu-nlg.1",
        priority=1,
        labels=["nlu", "extraction", "phase-1"],
    ),
    # Task 1.3: Create NLGEngine component
    create_issue(
        id="ibdm-burr-nlu-nlg.1.3",
        title="Create NLGEngine component (extract from generation rules)",
        description="""
Extract NLG processing from generation rules into standalone component.

Files to create:
- src/ibdm/nlg/nlg_engine.py
- src/ibdm/nlg/nlg_result.py

Class NLGEngine:
- __init__(config: NLGEngineConfig)
- generate(move, state) -> NLGResult

Class NLGResult:
- utterance_text: str
- strategy: str (template | plan_aware | llm)
- generation_rule: str | None
- tokens_used: int
- latency: float

Extract from generation rules:
- Template-based generation
- Plan-aware generation
- LLM-based generation
- Strategy selection logic

Testing:
- tests/unit/test_nlg_engine.py
- Test each generation strategy
- Test move types (ask, answer, greet, etc.)
- Test performance tracking (tokens, latency)

Acceptance:
- NLGEngine produces same text as current generation rules
- Strategy selection visible in NLGResult
- Performance metrics captured
- All NLG tests pass
""".strip(),
        parent="ibdm-burr-nlu-nlg.1",
        priority=1,
        labels=["nlg", "extraction", "phase-1"],
    ),
    # Task 1.4: Create nlu() Burr action
    create_issue(
        id="ibdm-burr-nlu-nlg.1.4",
        title="Create nlu() Burr action",
        description="""
Create explicit NLU stage as Burr action.

File: src/ibdm/burr_integration/actions.py

@action(reads=["utterance", "speaker", "nlu_context", "nlu_engine"],
        writes=["nlu_result", "nlu_context"])
def nlu(state: State) -> tuple[dict, State]:
    - Get NLUEngine from state
    - Call engine.process(utterance, speaker, context)
    - Return NLUResult and updated NLUContext
    - Store in Burr State

Testing:
- tests/integration/test_burr_nlu_action.py
- Test NLU action with various dialogue acts
- Test state updates (nlu_result, nlu_context)
- Test error handling

Acceptance:
- NLU action callable from Burr
- nlu_result appears in Burr State
- nlu_context updated correctly
- Integration tests pass
""".strip(),
        parent="ibdm-burr-nlu-nlg.1",
        priority=2,
        labels=["burr", "nlu", "action", "phase-1"],
    ),
    # Task 1.5: Create nlg() Burr action
    create_issue(
        id="ibdm-burr-nlu-nlg.1.5",
        title="Create nlg() Burr action",
        description="""
Create explicit NLG stage as Burr action.

File: src/ibdm/burr_integration/actions.py

@action(reads=["response_move", "information_state", "nlg_engine"],
        writes=["utterance_text", "nlg_result"])
def nlg(state: State) -> tuple[dict, State]:
    - Get NLGEngine from state
    - Call engine.generate(move, state)
    - Return NLGResult
    - Store utterance_text and nlg_result in Burr State

Testing:
- tests/integration/test_burr_nlg_action.py
- Test NLG action with various move types
- Test strategy selection visible in state
- Test performance metrics captured

Acceptance:
- NLG action callable from Burr
- utterance_text generated correctly
- nlg_result appears in Burr State (strategy, tokens, latency)
- Integration tests pass
""".strip(),
        parent="ibdm-burr-nlu-nlg.1",
        priority=2,
        labels=["burr", "nlg", "action", "phase-1"],
    ),
    # Task 1.6: Simplify DialogueMoveEngine
    create_issue(
        id="ibdm-burr-nlu-nlg.1.6",
        title="Simplify DialogueMoveEngine (remove NLU/NLG logic)",
        description="""
Remove NLU and NLG logic from DialogueMoveEngine, make it pure rule processor.

File: src/ibdm/engine/dialogue_engine.py

Changes:
- Remove all NLU components (dialogue_act_classifier, entity_extractor, etc.)
- Remove generate() method (now in NLG action)
- Add interpret_from_nlu(nlu_result, state) -> moves
- Keep integrate(), select_action() unchanged

New signature:
class DialogueMoveEngine:
    def __init__(self, agent_id: str, rules: RuleSet):
        self.agent_id = agent_id
        self.rules = rules
        # No NLU components!
        # No NLG components!

    def interpret_from_nlu(self, nlu_result: NLUResult, state: InformationState) -> list[DialogueMove]:
        # Create moves from NLU results using interpretation rules
        ...

Testing:
- tests/unit/test_dialogue_engine.py (update)
- Test interpret_from_nlu() with various NLU results
- Verify no NLU/NLG code remains
- All engine tests pass

Acceptance:
- DialogueMoveEngine ~50% smaller (LOC reduction)
- No NLU/NLG imports in dialogue_engine.py
- All tests pass
- Engine is now pure rule processor
""".strip(),
        parent="ibdm-burr-nlu-nlg.1",
        priority=2,
        labels=["engine", "simplification", "phase-1"],
    ),
    # Task 1.7: Update interpret() Burr action
    create_issue(
        id="ibdm-burr-nlu-nlg.1.7",
        title="Update interpret() Burr action to use NLU results",
        description="""
Simplify interpret() action to just apply interpretation rules to NLU results.

File: src/ibdm/burr_integration/actions.py

@action(reads=["nlu_result", "information_state", "engine"],
        writes=["moves"])
def interpret(state: State) -> tuple[dict, State]:
    - Get nlu_result from state (not utterance!)
    - Call engine.interpret_from_nlu(nlu_result, info_state)
    - Return moves

Remove:
- Direct utterance processing
- NLU logic (now in nlu() action)

Testing:
- tests/integration/test_burr_interpret_action.py (update)
- Test interpret() reads from nlu_result
- Test various dialogue acts
- Verify no NLU processing in interpret()

Acceptance:
- interpret() action simplified (no NLU calls)
- Reads nlu_result from state
- Produces same moves as before
- Integration tests pass
""".strip(),
        parent="ibdm-burr-nlu-nlg.1",
        priority=3,
        labels=["burr", "interpret", "action", "phase-1"],
    ),
    # Task 1.8: Update generate() Burr action
    create_issue(
        id="ibdm-burr-nlu-nlg.1.8",
        title="Update generate() Burr action to call NLG action",
        description="""
Simplify generate() action to just integrate system move (NLG done in nlg() action).

File: src/ibdm/burr_integration/actions.py

@action(reads=["utterance_text", "response_move", "information_state", "engine"],
        writes=["information_state"])
def integrate_system_move(state: State) -> tuple[dict, State]:
    - Get utterance_text from state (generated by nlg() action)
    - Update response_move.content with utterance_text
    - Integrate system's own move into information_state
    - Return updated information_state

Remove:
- NLG logic (now in nlg() action)
- Text generation (now in nlg() action)

Testing:
- tests/integration/test_burr_generate_action.py (update)
- Test integration of system move
- Verify no NLG processing

Acceptance:
- generate() action simplified (no NLG calls)
- Uses utterance_text from nlg() action
- Integrates system move correctly
- Integration tests pass
""".strip(),
        parent="ibdm-burr-nlu-nlg.1",
        priority=3,
        labels=["burr", "generate", "action", "phase-1"],
    ),
    # Task 1.9: Update Burr state machine graph
    create_issue(
        id="ibdm-burr-nlu-nlg.1.9",
        title="Update Burr state machine graph (6-stage pipeline)",
        description="""
Update Burr application graph to use new 6-stage pipeline.

File: src/ibdm/burr_integration/state_machine.py

Old graph (4 stages):
  interpret → integrate → select → generate

New graph (6 stages):
  nlu → interpret → integrate → select → nlg → integrate_system_move

Changes:
- Add nlu() action before interpret()
- Add nlg() action before integrate_system_move()
- Update transitions
- Add nlu_engine and nlg_engine to initial state

Testing:
- tests/integration/test_burr_state_machine.py
- Test complete dialogue flow through 6 stages
- Verify state at each stage
- Test Burr UI visualization

Acceptance:
- Burr app runs with 6 stages
- All stages visible in Burr UI
- State correctly passed between stages
- Complete dialogue flows work
""".strip(),
        parent="ibdm-burr-nlu-nlg.1",
        priority=4,
        labels=["burr", "graph", "state-machine", "phase-1"],
    ),
    # Task 1.10: Add feature flag for backward compatibility
    create_issue(
        id="ibdm-burr-nlu-nlg.1.10",
        title="Add feature flag for backward compatibility",
        description="""
Add feature flag to enable gradual migration from 4-stage to 6-stage pipeline.

File: src/ibdm/burr_integration/state_machine.py

def create_dialogue_application(
    agent_id: str = "system",
    rules: RuleSet | None = None,
    use_explicit_nlu_nlg: bool = False,  # NEW: Feature flag
    nlu_engine: NLUEngine | None = None,
    nlg_engine: NLGEngine | None = None,
    **kwargs
) -> Application:
    if use_explicit_nlu_nlg:
        return _create_6_stage_pipeline(...)  # New pipeline
    else:
        return _create_4_stage_pipeline(...)  # Legacy pipeline

Testing:
- tests/integration/test_backward_compatibility.py
- Test both pipelines produce same results
- Test feature flag toggle

Acceptance:
- Feature flag works
- Both pipelines coexist
- Parity tests pass (same dialogue behavior)
- Can migrate incrementally
""".strip(),
        parent="ibdm-burr-nlu-nlg.1",
        priority=4,
        labels=["burr", "migration", "compatibility", "phase-1"],
    ),
    # Task 1.11: Update integration tests
    create_issue(
        id="ibdm-burr-nlu-nlg.1.11",
        title="Update integration tests for 6-stage pipeline",
        description="""
Update all integration tests to work with both 4-stage and 6-stage pipelines.

Files:
- tests/integration/test_burr_integration.py (update)
- tests/integration/test_dialogue_flow.py (update)
- tests/integration/test_nlu_nlg_pipeline.py (new)

New tests:
- Test NLU results visible in state
- Test NLG results visible in state
- Test state evolution through 6 stages
- Test debugging workflow (inspect nlu_result)
- Test performance tracking (NLU/NLG latency)

Parity tests:
- Verify 6-stage produces same responses as 4-stage
- Verify dialogue flows unchanged

Acceptance:
- All integration tests pass
- Parity tests pass (same behavior)
- New tests demonstrate visibility improvements
- Test coverage maintained
""".strip(),
        parent="ibdm-burr-nlu-nlg.1",
        priority=5,
        labels=["testing", "integration", "phase-1"],
    ),
    # Task 1.12: Update documentation
    create_issue(
        id="ibdm-burr-nlu-nlg.1.12",
        title="Update documentation for 6-stage pipeline",
        description="""
Update documentation to reflect new 6-stage architecture.

Files to update:
- docs/SYSTEM_DESIGN_AND_LARSSON_ALIGNMENT.md (update section 4)
- README.md (update architecture diagram)
- CLAUDE.md (add migration notes)

New sections:
- Architecture diagram showing 6 stages
- NLU/NLG visibility benefits
- Debugging guide using Burr State inspection
- Performance tracking guide

Examples:
- Inspecting nlu_result in Burr State
- Swapping NLU/NLG engines
- Debugging NLU failures

Acceptance:
- Documentation updated
- Architecture diagram shows 6 stages
- Examples working
- Migration guide clear
""".strip(),
        parent="ibdm-burr-nlu-nlg.1",
        priority=5,
        labels=["documentation", "phase-1"],
    ),
]

# ============================================================================
# Phase 2: 8-Stage Pipeline (NLU/NLG Substages)
# ============================================================================

phase2 = create_issue(
    id="ibdm-burr-nlu-nlg.2",
    title="Phase 2: Implement 8-stage pipeline (NLU/NLG substages)",
    description="""
Further decompose NLU and NLG into substages for conditional execution and targeted debugging.

Pipeline: nlu_classify → nlu_enrich → interpret → integrate → select → nlg_plan → nlg_realize → output

Benefits:
- Conditional execution: Skip expensive enrichment for simple dialogue acts (40% faster for greet/quit)
- Targeted debugging: Pinpoint exact failure location (classification vs enrichment)
- Component swapping: Replace individual substages
- Performance tracking: Measure each substage separately

Prerequisites:
- Phase 1 complete (6-stage pipeline working)
- Team feedback on 6-stage pipeline positive

See: docs/FINE_GRAINED_BURR_PIPELINE.md
""".strip(),
    parent="ibdm-burr-nlu-nlg",
    priority=1,
    labels=["architecture", "refactoring", "burr", "nlu", "nlg", "phase-2"],
)

# Phase 2 subtasks
phase2_tasks = [
    # Task 2.1: Create NLUClassifier component
    create_issue(
        id="ibdm-burr-nlu-nlg.2.1",
        title="Create NLUClassifier component (fast classification)",
        description="""
Split NLUEngine into NLUClassifier (fast) and NLUEnricher (conditional).

File: src/ibdm/nlu/nlu_classifier.py

Class NLUClassifier:
- classify(utterance) -> (dialogue_act, confidence, raw_scores)
- extract_entities(utterance) -> list[Entity]

Fast operations (~200-350ms):
- Dialogue act classification
- Basic entity extraction
- Confidence scoring

Testing:
- tests/unit/test_nlu_classifier.py
- Test all dialogue act types
- Test entity extraction
- Test performance (<400ms)

Acceptance:
- NLUClassifier extracts classification and entities
- Fast (<400ms)
- Same results as NLUEngine.process() classification
- Unit tests pass
""".strip(),
        parent="ibdm-burr-nlu-nlg.2",
        priority=1,
        labels=["nlu", "classification", "phase-2"],
    ),
    # Task 2.2: Create NLUEnricher component
    create_issue(
        id="ibdm-burr-nlu-nlg.2.2",
        title="Create NLUEnricher component (conditional enrichment)",
        description="""
Create NLUEnricher for dialogue-act-specific processing.

File: src/ibdm/nlu/nlu_enricher.py

Class NLUEnricher:
- analyze_question(utterance, context) -> (type, details)  # if ask
- parse_answer(utterance, context) -> content              # if answer
- classify_intent(utterance) -> intent                     # if command/request
- resolve_references(entities, context) -> resolved        # always

Conditional operations:
- Question analysis: ~500ms (only for ask)
- Answer parsing: ~250ms (only for answer)
- Intent classification: ~200ms (only for command/request)
- Reference resolution: ~100ms (always)

Testing:
- tests/unit/test_nlu_enricher.py
- Test conditional execution per dialogue act
- Test skip logic for greet/quit
- Test performance metrics

Acceptance:
- NLUEnricher provides dialogue-act-specific enrichment
- Conditional execution working
- Performance measured per dialogue act
- Unit tests pass
""".strip(),
        parent="ibdm-burr-nlu-nlg.2",
        priority=1,
        labels=["nlu", "enrichment", "phase-2"],
    ),
    # Task 2.3: Create nlu_classify() Burr action
    create_issue(
        id="ibdm-burr-nlu-nlg.2.3",
        title="Create nlu_classify() Burr action",
        description="""
Create first NLU substage for fast classification.

File: src/ibdm/burr_integration/actions.py

@action(reads=["utterance", "speaker", "nlu_classifier"],
        writes=["nlu_classify_result"])
def nlu_classify(state: State) -> tuple[dict, State]:
    - Call nlu_classifier.classify(utterance)
    - Call nlu_classifier.extract_entities(utterance)
    - Store NLUClassifyResult in state

State:
{
    "nlu_classify_result": {
        "dialogue_act": "command",
        "confidence": 0.87,
        "entities": [...],
        "raw_scores": {"ask": 0.13, "command": 0.87, ...}
    }
}

Testing:
- tests/integration/test_nlu_classify_action.py
- Test classification visible in state
- Test performance (<400ms)

Acceptance:
- nlu_classify() action works
- Classification results in Burr State
- Fast (<400ms)
- Integration tests pass
""".strip(),
        parent="ibdm-burr-nlu-nlg.2",
        priority=2,
        labels=["burr", "nlu", "action", "phase-2"],
    ),
    # Task 2.4: Create nlu_enrich() Burr action
    create_issue(
        id="ibdm-burr-nlu-nlg.2.4",
        title="Create nlu_enrich() Burr action (conditional enrichment)",
        description="""
Create second NLU substage for conditional enrichment.

File: src/ibdm/burr_integration/actions.py

@action(reads=["utterance", "nlu_classify_result", "nlu_context", "nlu_enricher"],
        writes=["nlu_result", "nlu_context"])
def nlu_enrich(state: State) -> tuple[dict, State]:
    - Get dialogue_act from nlu_classify_result
    - Conditionally call enricher methods based on dialogue_act
    - If ask: analyze_question()
    - If answer: parse_answer()
    - If command/request: classify_intent()
    - Always: resolve_references()
    - Store complete NLUResult in state

Testing:
- tests/integration/test_nlu_enrich_action.py
- Test conditional execution per dialogue act
- Test fast path (greet/quit skip enrichment)
- Test slow path (ask runs question analysis)
- Test performance varies by dialogue act

Acceptance:
- nlu_enrich() action works
- Conditional execution implemented
- Performance varies correctly:
  * Greet/quit: ~100ms
  * Ask: ~500ms
  * Answer: ~250ms
  * Command: ~200ms
- Integration tests pass
""".strip(),
        parent="ibdm-burr-nlu-nlg.2",
        priority=2,
        labels=["burr", "nlu", "action", "conditional", "phase-2"],
    ),
    # Task 2.5: Create NLGPlanner component
    create_issue(
        id="ibdm-burr-nlu-nlg.2.5",
        title="Create NLGPlanner component (strategy selection)",
        description="""
Split NLGEngine into NLGPlanner (strategy) and NLGRealizer (text generation).

File: src/ibdm/nlg/nlg_planner.py

Class NLGPlanner:
- select_strategy(move, state) -> str  # template | plan_aware | llm
- plan_content(move, state) -> list[ContentItem]
- select_template(move) -> str | None
- build_prompt(move, content) -> str | None

Fast operations (~10-50ms):
- Strategy selection
- Content planning
- Template selection
- Prompt building

Testing:
- tests/unit/test_nlg_planner.py
- Test strategy selection logic
- Test content planning
- Test each strategy path

Acceptance:
- NLGPlanner selects generation strategy
- Content planning works
- Fast (<50ms)
- Unit tests pass
""".strip(),
        parent="ibdm-burr-nlu-nlg.2",
        priority=1,
        labels=["nlg", "planning", "phase-2"],
    ),
    # Task 2.6: Create NLGRealizer component
    create_issue(
        id="ibdm-burr-nlu-nlg.2.6",
        title="Create NLGRealizer component (text generation)",
        description="""
Create NLGRealizer for strategy-specific text generation.

File: src/ibdm/nlg/nlg_realizer.py

Class NLGRealizer:
- fill_template(template, content) -> str        # ~10ms
- generate_from_plan(content, state) -> str      # ~50ms
- llm_generate(prompt) -> (str, tokens)          # ~500ms
- apply_formatting(text) -> str                  # ~5ms

Performance varies by strategy:
- Template: ~15ms
- Plan-aware: ~55ms
- LLM: ~505ms

Testing:
- tests/unit/test_nlg_realizer.py
- Test each realization strategy
- Test performance per strategy
- Test post-processing

Acceptance:
- NLGRealizer generates text from plans
- Performance varies by strategy
- Same output as current NLGEngine
- Unit tests pass
""".strip(),
        parent="ibdm-burr-nlu-nlg.2",
        priority=1,
        labels=["nlg", "realization", "phase-2"],
    ),
    # Task 2.7: Create nlg_plan() Burr action
    create_issue(
        id="ibdm-burr-nlu-nlg.2.7",
        title="Create nlg_plan() Burr action",
        description="""
Create first NLG substage for generation planning.

File: src/ibdm/burr_integration/actions.py

@action(reads=["response_move", "information_state", "nlg_planner"],
        writes=["nlg_plan_result"])
def nlg_plan(state: State) -> tuple[dict, State]:
    - Call planner.select_strategy(move, state)
    - Call planner.plan_content(move, state)
    - Prepare strategy-specific plan details
    - Store NLGPlan in state

State:
{
    "nlg_plan_result": {
        "strategy": "plan_aware",
        "content_items": [...],
        "template_name": null,
        "llm_prompt": null
    }
}

Testing:
- tests/integration/test_nlg_plan_action.py
- Test strategy selection visible
- Test content planning
- Test performance (<50ms)

Acceptance:
- nlg_plan() action works
- Strategy visible in Burr State
- Content plan visible
- Fast (<50ms)
- Integration tests pass
""".strip(),
        parent="ibdm-burr-nlu-nlg.2",
        priority=2,
        labels=["burr", "nlg", "action", "phase-2"],
    ),
    # Task 2.8: Create nlg_realize() Burr action
    create_issue(
        id="ibdm-burr-nlu-nlg.2.8",
        title="Create nlg_realize() Burr action (conditional realization)",
        description="""
Create second NLG substage for strategy-specific text generation.

File: src/ibdm/burr_integration/actions.py

@action(reads=["nlg_plan_result", "nlg_realizer"],
        writes=["utterance_text", "nlg_result"])
def nlg_realize(state: State) -> tuple[dict, State]:
    - Get strategy from nlg_plan_result
    - Conditionally call realizer methods:
      * If template: fill_template()
      * If plan_aware: generate_from_plan()
      * If llm: llm_generate()
    - Apply post-processing
    - Track performance (tokens, latency)
    - Store NLGResult in state

Testing:
- tests/integration/test_nlg_realize_action.py
- Test conditional execution per strategy
- Test performance varies:
  * Template: ~15ms
  * Plan-aware: ~55ms
  * LLM: ~505ms
- Test metrics captured (tokens, latency)

Acceptance:
- nlg_realize() action works
- Conditional realization implemented
- Performance varies by strategy
- Metrics captured in nlg_result
- Integration tests pass
""".strip(),
        parent="ibdm-burr-nlu-nlg.2",
        priority=2,
        labels=["burr", "nlg", "action", "conditional", "phase-2"],
    ),
    # Task 2.9: Update Burr state machine graph (8-stage)
    create_issue(
        id="ibdm-burr-nlu-nlg.2.9",
        title="Update Burr state machine graph (8-stage pipeline)",
        description="""
Update Burr application graph to use new 8-stage pipeline.

File: src/ibdm/burr_integration/state_machine.py

Old graph (6 stages):
  nlu → interpret → integrate → select → nlg → output

New graph (8 stages):
  nlu_classify → nlu_enrich → interpret → integrate →
  select → nlg_plan → nlg_realize → integrate_system_move

Changes:
- Replace nlu() with nlu_classify() + nlu_enrich()
- Replace nlg() with nlg_plan() + nlg_realize()
- Update transitions
- Add components to initial state (nlu_classifier, nlu_enricher, nlg_planner, nlg_realizer)

Testing:
- tests/integration/test_8_stage_pipeline.py
- Test complete dialogue flow through 8 stages
- Test conditional execution paths
- Test Burr UI visualization (8 nodes)

Acceptance:
- Burr app runs with 8 stages
- All stages visible in Burr UI
- Conditional execution working
- Complete dialogue flows work
""".strip(),
        parent="ibdm-burr-nlu-nlg.2",
        priority=3,
        labels=["burr", "graph", "state-machine", "phase-2"],
    ),
    # Task 2.10: Add performance monitoring
    create_issue(
        id="ibdm-burr-nlu-nlg.2.10",
        title="Add performance monitoring for each substage",
        description="""
Add performance tracking to measure time spent in each substage.

Files:
- src/ibdm/burr_integration/performance.py (new)

Metrics to track:
- nlu_classify_latency
- nlu_enrich_latency (varies by dialogue act)
- nlg_plan_latency
- nlg_realize_latency (varies by strategy)
- Total NLU time
- Total NLG time
- Total turn time

Aggregations:
- By dialogue act (greet/quit fast path vs ask/answer slow path)
- By NLG strategy (template fast vs LLM slow)
- Percentiles (p50, p95, p99)

Dashboard:
- Grafana dashboard (optional)
- Simple logging with structured output

Testing:
- tests/unit/test_performance_monitoring.py
- Verify metrics captured
- Verify aggregations correct

Acceptance:
- Performance metrics captured per substage
- Can identify bottlenecks
- Can measure conditional execution benefit
- Monitoring dashboard or logs available
""".strip(),
        parent="ibdm-burr-nlu-nlg.2",
        priority=4,
        labels=["monitoring", "performance", "phase-2"],
    ),
    # Task 2.11: Update integration tests for 8-stage pipeline
    create_issue(
        id="ibdm-burr-nlu-nlg.2.11",
        title="Update integration tests for 8-stage pipeline",
        description="""
Update integration tests to work with 8-stage pipeline.

Files:
- tests/integration/test_burr_integration.py (update)
- tests/integration/test_conditional_execution.py (new)
- tests/integration/test_debugging_workflow.py (new)

New tests:
- Test conditional NLU enrichment (fast path vs slow path)
- Test conditional NLG realization (template vs LLM)
- Test state inspection at each substage
- Test debugging workflow examples
- Test performance tracking

Parity tests:
- Verify 8-stage produces same responses as 6-stage
- Verify dialogue flows unchanged

Acceptance:
- All integration tests pass
- Parity tests pass (same behavior)
- Conditional execution tests pass
- Performance tests demonstrate benefit
- Test coverage maintained
""".strip(),
        parent="ibdm-burr-nlu-nlg.2",
        priority=5,
        labels=["testing", "integration", "phase-2"],
    ),
    # Task 2.12: Update documentation for 8-stage pipeline
    create_issue(
        id="ibdm-burr-nlu-nlg.2.12",
        title="Update documentation for 8-stage pipeline",
        description="""
Update documentation to reflect new 8-stage architecture.

Files to update:
- docs/SYSTEM_DESIGN_AND_LARSSON_ALIGNMENT.md (update)
- docs/FINE_GRAINED_BURR_PIPELINE.md (mark as implemented)
- README.md (update architecture diagram)

New content:
- Architecture diagram showing 8 stages
- Conditional execution explanation
- Performance comparison (6-stage vs 8-stage)
- Debugging guide with substage inspection

Examples:
- Debugging classification failures (inspect nlu_classify_result)
- Debugging enrichment failures (inspect nlu_result)
- Optimizing NLG strategy (inspect nlg_plan_result)
- Performance monitoring

Acceptance:
- Documentation updated
- Architecture diagram shows 8 stages
- Examples working
- Performance benefits documented
""".strip(),
        parent="ibdm-burr-nlu-nlg.2",
        priority=5,
        labels=["documentation", "phase-2"],
    ),
]

# Collect all issues
all_issues = [epic, phase1] + phase1_tasks + [phase2] + phase2_tasks

# Output as JSON
output = {
    "issues": all_issues,
    "metadata": {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source": "NLU/NLG Burr Integration Refactoring",
        "epic": "ibdm-burr-nlu-nlg",
        "total_tasks": len(all_issues),
        "phase_1_tasks": len(phase1_tasks) + 1,  # +1 for phase epic
        "phase_2_tasks": len(phase2_tasks) + 1,  # +1 for phase epic
    },
}

print(json.dumps(output, indent=2))
