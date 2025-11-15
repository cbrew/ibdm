# Fine-Grained Burr Pipeline: NLU/NLG Substages

**Author**: Claude (AI Analysis)
**Date**: 2025-11-15
**Status**: Architectural Exploration
**Related**: `docs/NLU_NLG_BURR_REFACTORING.md`, `docs/SYSTEM_DESIGN_AND_LARSSON_ALIGNMENT.md`

## Executive Summary

**Question**: Should NLU and NLG be further decomposed into substages in the Burr loop?

**Answer**: **Yes, with careful design** - A two-level decomposition provides optimal granularity:
- **NLU**: 2 substages (classify + enrich)
- **NLG**: 2 substages (plan + realize)

**Result**: 8-stage pipeline that balances visibility with comprehensibility:
```
utterance → nlu_classify → nlu_enrich → interpret → integrate → select → nlg_plan → nlg_realize → output
```

**Benefits**:
- ✅ **Conditional execution** - Only run expensive substages when needed
- ✅ **Parallel processing** - Some substages can run concurrently
- ✅ **Targeted debugging** - Pinpoint exact failure point in NLU/NLG
- ✅ **Component swapping** - Replace individual substages
- ✅ **Performance tracking** - Measure each substage separately
- ⚠️ **Complexity trade-off** - More nodes, but better organized

---

## Table of Contents

1. [NLU Substages Analysis](#nlu-substages-analysis)
2. [NLG Substages Analysis](#nlg-substages-analysis)
3. [Proposed 8-Stage Pipeline](#proposed-8-stage-pipeline)
4. [Conditional Execution Patterns](#conditional-execution-patterns)
5. [Parallel Processing Opportunities](#parallel-processing-opportunities)
6. [Granularity Trade-offs](#granularity-trade-offs)
7. [Implementation Design](#implementation-design)
8. [Comparison of Architectures](#comparison-of-architectures)

---

## NLU Substages Analysis

### Current NLU Process (Hidden in One Action)

Looking at what happens inside `nlu()`:

```python
def nlu(utterance, context):
    # Stage 1: Core classification (always runs)
    dialogue_act = classify_dialogue_act(utterance)        # ~200ms
    entities = extract_entities(utterance)                 # ~150ms

    # Stage 2: Conditional enrichment (depends on dialogue_act)
    if dialogue_act == "ask":
        question_type = analyze_question(utterance)        # ~300ms
        question_details = parse_question_structure(...)   # ~200ms
    elif dialogue_act == "answer":
        answer_content = parse_answer(utterance, context)  # ~250ms
    elif dialogue_act in ["command", "request"]:
        intent = classify_intent(utterance)                # ~200ms

    # Stage 3: Cross-cutting enrichment (always runs)
    resolved_entities = resolve_references(entities, context)  # ~100ms

    return NLUResult(...)
```

**Total time**: ~350-1200ms depending on dialogue act

### Identified Substages

#### Option A: Fully Granular (7 substages)

```
1. nlu_classify_act      (dialogue act classification)
2. nlu_extract_entities  (entity extraction)
3. nlu_analyze_question  (question analysis - conditional)
4. nlu_parse_answer      (answer parsing - conditional)
5. nlu_classify_intent   (intent classification - conditional)
6. nlu_resolve_refs      (reference resolution)
7. nlu_assemble          (assemble final NLU result)
```

**Pros**: Maximum visibility, fine-grained swapping
**Cons**: Too many nodes (14 total in full pipeline), cluttered graph

#### Option B: Two-Stage Decomposition (2 substages) ✓ RECOMMENDED

```
1. nlu_classify   (dialogue act + entities + basic parsing)
2. nlu_enrich     (conditional enrichment based on dialogue act)
```

**Pros**: Clean graph, meaningful breakpoint, conditional execution
**Cons**: Less granular than Option A

#### Option C: Three-Stage Decomposition (3 substages)

```
1. nlu_classify   (dialogue act classification)
2. nlu_extract    (entity extraction + specialized parsing)
3. nlu_resolve    (reference resolution + final assembly)
```

**Pros**: Balanced granularity
**Cons**: Middle ground without clear benefits over Option B

### Recommendation: Option B (Two-Stage)

**Stage 1: `nlu_classify`** - Fast, always runs
- Dialogue act classification
- Basic entity extraction
- Confidence scoring

**Stage 2: `nlu_enrich`** - Conditional, dialogue-act-specific
- Question analysis (if ask)
- Answer parsing (if answer)
- Intent classification (if command/request)
- Reference resolution

**Benefits**:
- Clear separation: classification vs. enrichment
- Conditional execution: Skip expensive enrichment if not needed
- Debugging: Can see if failure is in classification vs. enrichment
- Performance: Can track fast path (classify only) vs. slow path (classify + enrich)

---

## NLG Substages Analysis

### Current NLG Process (Hidden in One Action)

Looking at what happens inside `nlg()`:

```python
def nlg(move, state):
    # Stage 1: Planning (decide what to say)
    strategy = select_strategy(move, state)        # template | plan | llm
    content_plan = plan_content(move, state)       # What info to include

    # Stage 2: Realization (convert plan to text)
    if strategy == "template":
        text = fill_template(content_plan)         # ~10ms
    elif strategy == "plan_aware":
        text = generate_from_plan(content_plan)    # ~50ms
    else:  # llm
        text = llm_generate(content_plan)          # ~500ms

    # Stage 3: Post-processing
    text = apply_formatting(text)                  # ~5ms

    return NLGResult(text, strategy, ...)
```

**Total time**: ~15-555ms depending on strategy

### Identified Substages

#### Option A: Fully Granular (4 substages)

```
1. nlg_select_strategy    (choose template vs plan vs LLM)
2. nlg_plan_content       (decide what info to include)
3. nlg_realize            (convert to text)
4. nlg_postprocess        (formatting, cleanup)
```

**Pros**: Very fine-grained control
**Cons**: Overkill - planning substages are trivial (~1ms each)

#### Option B: Two-Stage Decomposition (2 substages) ✓ RECOMMENDED

```
1. nlg_plan      (strategy selection + content planning)
2. nlg_realize   (text generation + post-processing)
```

**Pros**: Clean separation, conditional execution potential
**Cons**: None significant

#### Option C: Single Stage (1 stage)

```
1. nlg           (all-in-one)
```

**Pros**: Simplest
**Cons**: Can't swap realization strategies easily

### Recommendation: Option B (Two-Stage)

**Stage 1: `nlg_plan`** - Fast decision making
- Select generation strategy (template | plan_aware | llm)
- Plan content (what info to include)
- Prepare context for realization

**Stage 2: `nlg_realize`** - Conditional on strategy
- Template filling (if strategy == template)
- Plan-aware generation (if strategy == plan_aware)
- LLM generation (if strategy == llm)
- Post-processing

**Benefits**:
- Can swap realization strategies without changing planning
- Can test planning independently
- Can measure time spent on planning vs. realization
- Clear separation of concerns

---

## Proposed 8-Stage Pipeline

### Complete Pipeline

```
┌────────────────┐
│  receive_input │  utterance, speaker
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  nlu_classify  │  dialogue_act, entities, confidence
└───────┬────────┘
        │
        ▼
┌────────────────┐
│   nlu_enrich   │  question_details | answer_content | intent
└───────┬────────┘
        │
        ▼
┌────────────────┐
│   interpret    │  moves
└───────┬────────┘
        │
        ▼
┌────────────────┐
│   integrate    │  information_state'
└───────┬────────┘
        │
        ▼
┌────────────────┐
│     select     │  response_move
└───────┬────────┘
        │
        ▼
┌────────────────┐
│    nlg_plan    │  generation_strategy, content_plan
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  nlg_realize   │  utterance_text
└───────┬────────┘
        │
        ▼
┌────────────────┐
│     output     │
└────────────────┘
```

### State at Each Stage

```python
# After receive_input
{
    "utterance": "Draft an NDA for Acme Corp and Beta Inc",
    "speaker": "user"
}

# After nlu_classify
{
    "nlu_classify_result": {
        "dialogue_act": "command",
        "confidence": 0.87,
        "entities": [
            {"type": "ORGANIZATION", "text": "Acme Corp", "start": 18, "end": 27},
            {"type": "ORGANIZATION", "text": "Beta Inc", "start": 32, "end": 40}
        ],
        "raw_classification": {...}
    }
}

# After nlu_enrich
{
    "nlu_result": {
        "dialogue_act": "command",
        "confidence": 0.87,
        "entities": [
            {"type": "ORGANIZATION", "text": "Acme Corp", ...},
            {"type": "ORGANIZATION", "text": "Beta Inc", ...}
        ],
        "intent": "DRAFT_DOCUMENT",
        "task_type": "nda_drafting",
        "question_details": null,  # Not a question
        "answer_content": null,    # Not an answer
        "resolved_entities": [...]  # After reference resolution
    }
}

# After interpret
{
    "moves": [
        {
            "move_type": "command",
            "content": "draft_nda",
            "speaker": "user",
            "metadata": {
                "intent": "DRAFT_DOCUMENT",
                "task_type": "nda_drafting",
                "entities": [...]
            }
        }
    ]
}

# ... (integrate, select as before) ...

# After nlg_plan
{
    "nlg_plan_result": {
        "strategy": "plan_aware",
        "content_items": [
            {"type": "acknowledgment", "content": "I'll help you draft an NDA"},
            {"type": "question", "content": state.shared.qud[0]},
            {"type": "context", "content": "parties: Acme Corp, Beta Inc"}
        ],
        "template": null,           # Not using template
        "llm_prompt": null,         # Not using LLM
        "plan_context": {...}
    }
}

# After nlg_realize
{
    "utterance_text": "I'll help you draft an NDA for Acme Corp and Beta Inc. First, what type of NDA do you need - mutual or one-way?",
    "nlg_result": {
        "utterance_text": "...",
        "strategy": "plan_aware",
        "generation_rule": "generate_from_question",
        "tokens_used": 0,
        "latency": 0.045
    }
}
```

---

## Conditional Execution Patterns

### NLU Enrichment Conditions

**Pattern**: `nlu_enrich` performs different operations based on `dialogue_act`

```python
@action(reads=["nlu_classify_result"], writes=["nlu_result"])
def nlu_enrich(state: State) -> tuple[dict, State]:
    """Conditionally enrich NLU results based on dialogue act."""

    classify_result = state["nlu_classify_result"]
    dialogue_act = classify_result["dialogue_act"]

    # Start with classification results
    nlu_result = {**classify_result}

    # Conditional enrichment
    if dialogue_act == "ask":
        # Question-specific analysis
        nlu_result.update({
            "question_type": analyze_question_type(utterance),
            "question_details": parse_question_structure(utterance)
        })

    elif dialogue_act == "answer":
        # Answer-specific parsing
        nlu_result.update({
            "answer_content": parse_answer(utterance, context),
            "resolves_qud": check_qud_resolution(answer, state)
        })

    elif dialogue_act in ["command", "request"]:
        # Intent classification for tasks
        nlu_result.update({
            "intent": classify_intent(utterance),
            "task_type": infer_task_type(utterance, entities)
        })

    # Always do reference resolution
    nlu_result["resolved_entities"] = resolve_references(
        nlu_result["entities"],
        state["nlu_context"]
    )

    return {"nlu_result": nlu_result}, state.update(nlu_result=nlu_result)
```

**Benefit**: Only run expensive operations when needed
- Question analysis: ~500ms (only for asks)
- Answer parsing: ~250ms (only for answers)
- Intent classification: ~200ms (only for commands/requests)

**Performance Impact**:
- Greet/Quit: Skip enrichment entirely (fast path)
- Questions: Only run question analysis
- Answers: Only run answer parsing
- Commands: Only run intent classification

### NLG Realization Conditions

**Pattern**: `nlg_realize` chooses realization strategy based on `nlg_plan`

```python
@action(reads=["nlg_plan_result", "response_move"], writes=["utterance_text"])
def nlg_realize(state: State) -> tuple[dict, State]:
    """Realize NLG plan into text using selected strategy."""

    plan = state["nlg_plan_result"]
    strategy = plan["strategy"]

    if strategy == "template":
        # Fast template filling (~10ms)
        text = fill_template(plan["template"], plan["content_items"])

    elif strategy == "plan_aware":
        # Moderate plan-based generation (~50ms)
        text = generate_from_plan(plan["content_items"], state)

    else:  # llm
        # Slow LLM generation (~500ms)
        text = llm_generate(plan["llm_prompt"])

    # Post-processing (always)
    text = apply_formatting(text)

    return {"utterance_text": text}, state.update(utterance_text=text)
```

**Benefit**: Strategy selection visible in state
- Can see why LLM was chosen vs. template
- Can track performance by strategy
- Can override strategy for testing

---

## Parallel Processing Opportunities

### Concurrent NLU Operations

Some NLU substages could run in parallel:

```python
# Sequential (current)
classify_result = nlu_classify(utterance)      # 200ms
enrich_result = nlu_enrich(classify_result)    # 300ms
# Total: 500ms

# Parallel (potential)
async {
    dialogue_act = classify_dialogue_act(utterance)  # 200ms
    entities = extract_entities(utterance)           # 150ms
}
# Total: 200ms (limited by slowest)

async {
    question_details = analyze_question(utterance)   # 300ms (if ask)
    resolved_entities = resolve_refs(entities)       # 100ms
}
# Total: 300ms
```

**Potential speedup**: ~40% for question processing

**Burr Support**: Burr doesn't natively support parallel actions, but could be simulated:

```python
# Pseudo-code for parallel execution
@action(reads=["utterance"], writes=["dialogue_act", "entities"])
def nlu_classify_parallel(state: State):
    """Run classification and entity extraction in parallel."""

    with ThreadPoolExecutor() as executor:
        # Submit both tasks
        act_future = executor.submit(classify_dialogue_act, utterance)
        ent_future = executor.submit(extract_entities, utterance)

        # Wait for both
        dialogue_act = act_future.result()
        entities = ent_future.result()

    return {...}, state.update(dialogue_act=dialogue_act, entities=entities)
```

**Trade-off**: Complexity vs. performance gain
- Benefit: ~200-300ms faster per turn
- Cost: More complex action code, harder to debug
- Recommendation: Profile first, optimize if needed

### Fork-Join Pattern for Multi-Model NLU

Could run multiple NLU models in parallel and combine results:

```
                    ┌─→ llm_nlu_sonnet ─┐
utterance ─────────→├─→ llm_nlu_haiku  ─┤─→ nlu_ensemble → nlu_result
                    └─→ template_nlu   ─┘
```

**Use case**: Ensemble NLU for high-confidence classification
- Run fast template matcher + LLM in parallel
- If both agree → high confidence
- If disagree → use LLM result with lower confidence

**Implementation**: Would need custom Burr action or external orchestration

---

## Granularity Trade-offs

### Comparison of Options

| Pipeline | Stages | Pros | Cons | Recommendation |
|----------|--------|------|------|----------------|
| **Minimal** (4 stages) | interpret, integrate, select, generate | Simple graph | NLU/NLG hidden | ❌ Too opaque |
| **6-stage** | nlu, interpret, integrate, select, nlg, output | Good balance | NLU/NLG still monolithic | ⚠️ Good but can improve |
| **8-stage** | nlu_classify, nlu_enrich, interpret, integrate, select, nlg_plan, nlg_realize, output | Conditional execution, targeted debugging | More nodes | ✅ **RECOMMENDED** |
| **14-stage** | Fully granular NLU/NLG substages | Maximum visibility | Graph too cluttered, tight coupling | ❌ Too granular |

### 8-Stage Sweet Spot

**Why 8 stages is optimal**:

1. **Meaningful Breakpoints**
   - Classification failures vs. enrichment failures (NLU)
   - Planning failures vs. realization failures (NLG)

2. **Conditional Execution**
   - Skip expensive enrichment for simple dialogue acts
   - Skip expensive LLM generation for templates

3. **Performance Tracking**
   - Measure fast path (classify + template) vs. slow path (enrich + LLM)
   - Identify bottlenecks precisely

4. **Comprehensible Graph**
   - 8 nodes is still easy to visualize
   - Clear main flow with conditional branches

5. **Component Swapping**
   - Swap classifier without changing enrichment
   - Swap realization strategy without changing planning

### Visual Complexity Comparison

**4-stage graph** (current):
```
[interpret] → [integrate] → [select] → [generate]
```
**Clarity**: ⭐⭐ (NLU/NLG hidden)

**6-stage graph** (NLU/NLG explicit):
```
[nlu] → [interpret] → [integrate] → [select] → [nlg] → [output]
```
**Clarity**: ⭐⭐⭐⭐ (Good visibility)

**8-stage graph** (NLU/NLG substages):
```
[nlu_classify] → [nlu_enrich] → [interpret] → [integrate] → [select] → [nlg_plan] → [nlg_realize] → [output]
```
**Clarity**: ⭐⭐⭐⭐⭐ (Optimal visibility)

**14-stage graph** (fully granular):
```
[nlu_act] → [nlu_entity] → [nlu_question?] → [nlu_answer?] → [nlu_intent?] → [nlu_resolve] → [nlu_assemble] →
[interpret] → [integrate] → [select] →
[nlg_strategy] → [nlg_plan] → [nlg_realize] → [nlg_post]
```
**Clarity**: ⭐⭐ (Too cluttered)

---

## Implementation Design

### Action Definitions

#### 1. nlu_classify Action

```python
@dataclass
class NLUClassifyResult:
    """Result of NLU classification stage."""
    dialogue_act: str          # ask | answer | command | assert | greet | quit
    confidence: float
    entities: list[dict]       # Raw entities extracted
    raw_scores: dict          # Classification scores for all acts

    def to_dict(self) -> dict:
        return {
            "dialogue_act": self.dialogue_act,
            "confidence": self.confidence,
            "entities": self.entities,
            "raw_scores": self.raw_scores
        }


@action(
    reads=["utterance", "speaker", "nlu_context", "nlu_classifier"],
    writes=["nlu_classify_result"]
)
def nlu_classify(state: State) -> tuple[dict, State]:
    """Classify dialogue act and extract basic entities.

    Fast stage (~200-350ms) that always runs.
    Provides basic classification needed for conditional enrichment.
    """
    utterance = state["utterance"]
    speaker = state["speaker"]
    nlu_classifier = state["nlu_classifier"]

    # Core classification
    dialogue_act, confidence, raw_scores = nlu_classifier.classify(utterance)

    # Basic entity extraction (fast, always useful)
    entities = nlu_classifier.extract_entities(utterance)

    result = NLUClassifyResult(
        dialogue_act=dialogue_act,
        confidence=confidence,
        entities=entities,
        raw_scores=raw_scores
    )

    return {
        "dialogue_act": dialogue_act,
        "confidence": confidence
    }, state.update(nlu_classify_result=result.to_dict())
```

#### 2. nlu_enrich Action

```python
@dataclass
class NLUResult:
    """Complete NLU result after enrichment."""
    dialogue_act: str
    confidence: float
    entities: list[dict]
    resolved_entities: list[dict]     # After reference resolution

    # Conditional fields (populated based on dialogue_act)
    question_type: str | None = None
    question_details: dict | None = None
    answer_content: Any | None = None
    intent: str | None = None
    task_type: str | None = None

    def to_dict(self) -> dict:
        return {
            "dialogue_act": self.dialogue_act,
            "confidence": self.confidence,
            "entities": self.entities,
            "resolved_entities": self.resolved_entities,
            "question_type": self.question_type,
            "question_details": self.question_details,
            "answer_content": self.answer_content,
            "intent": self.intent,
            "task_type": self.task_type
        }


@action(
    reads=["utterance", "nlu_classify_result", "nlu_context", "nlu_enricher"],
    writes=["nlu_result", "nlu_context"]
)
def nlu_enrich(state: State) -> tuple[dict, State]:
    """Conditionally enrich NLU classification based on dialogue act.

    Expensive stage (~200-500ms) with conditional execution.
    Only runs enrichment needed for the specific dialogue act.
    """
    utterance = state["utterance"]
    classify_result = NLUClassifyResult(**state["nlu_classify_result"])
    nlu_context = NLUContext.from_dict(state["nlu_context"])
    enricher = state["nlu_enricher"]

    # Start with classification results
    nlu_result = NLUResult(
        dialogue_act=classify_result.dialogue_act,
        confidence=classify_result.confidence,
        entities=classify_result.entities,
        resolved_entities=[]  # Will populate below
    )

    # Conditional enrichment based on dialogue act
    if classify_result.dialogue_act == "ask":
        # Question-specific enrichment (~500ms)
        q_type, q_details = enricher.analyze_question(utterance, nlu_context)
        nlu_result.question_type = q_type
        nlu_result.question_details = q_details

    elif classify_result.dialogue_act == "answer":
        # Answer-specific enrichment (~250ms)
        nlu_result.answer_content = enricher.parse_answer(
            utterance, nlu_context
        )

    elif classify_result.dialogue_act in ["command", "request"]:
        # Task-specific enrichment (~200ms)
        nlu_result.intent = enricher.classify_intent(utterance)
        nlu_result.task_type = enricher.infer_task_type(
            utterance, classify_result.entities
        )

    # Always do reference resolution (~100ms)
    nlu_result.resolved_entities = enricher.resolve_references(
        classify_result.entities, nlu_context
    )

    # Update NLU context with new entities
    updated_nlu_context = nlu_context.add_entities(
        nlu_result.resolved_entities
    )

    return {
        "nlu_result": nlu_result.to_dict()
    }, state.update(
        nlu_result=nlu_result.to_dict(),
        nlu_context=updated_nlu_context.to_dict()
    )
```

#### 3. nlg_plan Action

```python
@dataclass
class NLGPlan:
    """NLG generation plan."""
    strategy: str              # template | plan_aware | llm
    content_items: list[dict]  # What to say
    template_name: str | None = None
    llm_prompt: str | None = None
    plan_context: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "strategy": self.strategy,
            "content_items": self.content_items,
            "template_name": self.template_name,
            "llm_prompt": self.llm_prompt,
            "plan_context": self.plan_context
        }


@action(
    reads=["response_move", "information_state", "nlg_planner"],
    writes=["nlg_plan_result"]
)
def nlg_plan(state: State) -> tuple[dict, State]:
    """Plan what to say and how to say it.

    Fast stage (~10-50ms) that decides generation strategy and content.
    """
    response_move_dict = state["response_move"]
    if not response_move_dict:
        return {"nlg_plan_result": None}, state.update(nlg_plan_result=None)

    response_move = DialogueMove.from_dict(response_move_dict)
    info_state = InformationState.from_dict(state["information_state"])
    planner = state["nlg_planner"]

    # Select generation strategy
    strategy = planner.select_strategy(response_move, info_state)

    # Plan content
    content_items = planner.plan_content(response_move, info_state)

    # Prepare strategy-specific plan details
    plan = NLGPlan(strategy=strategy, content_items=content_items)

    if strategy == "template":
        plan.template_name = planner.select_template(response_move)
    elif strategy == "llm":
        plan.llm_prompt = planner.build_prompt(response_move, content_items)

    return {
        "strategy": strategy
    }, state.update(nlg_plan_result=plan.to_dict())
```

#### 4. nlg_realize Action

```python
@dataclass
class NLGResult:
    """NLG realization result."""
    utterance_text: str
    strategy: str
    tokens_used: int = 0
    latency: float = 0.0
    generation_details: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "utterance_text": self.utterance_text,
            "strategy": self.strategy,
            "tokens_used": self.tokens_used,
            "latency": self.latency,
            "generation_details": self.generation_details
        }


@action(
    reads=["nlg_plan_result", "information_state", "nlg_realizer"],
    writes=["utterance_text", "nlg_result", "information_state"]
)
def nlg_realize(state: State) -> tuple[dict, State]:
    """Realize NLG plan into natural language text.

    Variable latency stage (~10-500ms) depending on strategy.
    """
    plan_dict = state["nlg_plan_result"]
    if not plan_dict:
        return {"utterance_text": ""}, state.update(utterance_text="")

    plan = NLGPlan(**plan_dict)
    info_state = InformationState.from_dict(state["information_state"])
    realizer = state["nlg_realizer"]

    # Conditional realization based on strategy
    start_time = time.time()

    if plan.strategy == "template":
        # Fast template filling
        text = realizer.fill_template(
            plan.template_name, plan.content_items
        )
        tokens_used = 0

    elif plan.strategy == "plan_aware":
        # Moderate plan-based generation
        text = realizer.generate_from_plan(
            plan.content_items, info_state
        )
        tokens_used = 0

    else:  # llm
        # Slow LLM generation
        text, tokens_used = realizer.llm_generate(plan.llm_prompt)

    latency = time.time() - start_time

    # Post-processing
    text = realizer.apply_formatting(text)

    result = NLGResult(
        utterance_text=text,
        strategy=plan.strategy,
        tokens_used=tokens_used,
        latency=latency
    )

    # Integrate system's own move (move content to state)
    # (This could be a separate action, but keeping here for simplicity)

    return {
        "utterance_text": text,
        "tokens_used": tokens_used,
        "latency": latency
    }, state.update(
        utterance_text=text,
        nlg_result=result.to_dict()
    )
```

### Component Architecture

```python
# New component: NLUClassifier
class NLUClassifier:
    """Fast dialogue act classification and entity extraction."""

    def __init__(self, config: NLUConfig):
        self.dialogue_act_classifier = DialogueActClassifier(config)
        self.entity_extractor = EntityExtractor(config)

    def classify(self, utterance: str) -> tuple[str, float, dict]:
        """Classify dialogue act with confidence scores."""
        ...

    def extract_entities(self, utterance: str) -> list[dict]:
        """Extract basic entities."""
        ...

# New component: NLUEnricher
class NLUEnricher:
    """Conditional NLU enrichment based on dialogue act."""

    def __init__(self, config: NLUConfig):
        self.question_analyzer = QuestionAnalyzer(config)
        self.answer_parser = AnswerParser(config)
        self.intent_classifier = IntentClassifier(config)
        self.reference_resolver = ReferenceResolver(config)

    def analyze_question(self, utterance: str, context: NLUContext):
        """Analyze question structure (only for ask moves)."""
        ...

    def parse_answer(self, utterance: str, context: NLUContext):
        """Parse answer content (only for answer moves)."""
        ...

    def classify_intent(self, utterance: str):
        """Classify intent (only for command/request moves)."""
        ...

    def resolve_references(self, entities: list, context: NLUContext):
        """Resolve entity references (always runs)."""
        ...

# New component: NLGPlanner
class NLGPlanner:
    """NLG strategy selection and content planning."""

    def select_strategy(self, move: DialogueMove, state: InformationState) -> str:
        """Select generation strategy (template | plan_aware | llm)."""
        ...

    def plan_content(self, move: DialogueMove, state: InformationState) -> list:
        """Plan what information to include."""
        ...

    def select_template(self, move: DialogueMove) -> str:
        """Select template (if strategy == template)."""
        ...

    def build_prompt(self, move: DialogueMove, content: list) -> str:
        """Build LLM prompt (if strategy == llm)."""
        ...

# New component: NLGRealizer
class NLGRealizer:
    """NLG text realization from plans."""

    def fill_template(self, template_name: str, content: list) -> str:
        """Fill template with content."""
        ...

    def generate_from_plan(self, content: list, state: InformationState) -> str:
        """Generate from plan structure."""
        ...

    def llm_generate(self, prompt: str) -> tuple[str, int]:
        """Generate using LLM (returns text, tokens)."""
        ...

    def apply_formatting(self, text: str) -> str:
        """Post-process text."""
        ...
```

---

## Comparison of Architectures

### Side-by-Side Comparison

#### Current (4-stage):
```
utterance → [interpret with hidden NLU] → integrate → select → [generate with hidden NLG] → output
```
**State captured**: moves, information_state, response_move, utterance_text
**Visibility**: ⭐⭐ (Poor - NLU/NLG hidden)
**Debuggability**: ⭐⭐ (Poor - must add logging)
**Flexibility**: ⭐⭐ (Poor - must modify engine)

#### 6-Stage (NLU/NLG Explicit):
```
utterance → [nlu] → interpret → integrate → select → [nlg] → output
```
**State captured**: +nlu_result, +nlg_result
**Visibility**: ⭐⭐⭐⭐ (Good - NLU/NLG visible)
**Debuggability**: ⭐⭐⭐⭐ (Good - inspect NLU/NLG results)
**Flexibility**: ⭐⭐⭐⭐ (Good - swap NLU/NLG engines)

#### 8-Stage (NLU/NLG Substages): ✓ RECOMMENDED
```
utterance → [nlu_classify] → [nlu_enrich] → interpret → integrate → select → [nlg_plan] → [nlg_realize] → output
```
**State captured**: +nlu_classify_result, +nlu_result, +nlg_plan_result, +nlg_result
**Visibility**: ⭐⭐⭐⭐⭐ (Excellent - all substages visible)
**Debuggability**: ⭐⭐⭐⭐⭐ (Excellent - pinpoint failure location)
**Flexibility**: ⭐⭐⭐⭐⭐ (Excellent - swap individual substages)
**Conditional Execution**: ✅ (Skip enrichment for simple acts)
**Performance Tracking**: ✅ (Measure each substage)

#### 14-Stage (Fully Granular):
```
utterance → [nlu_act] → [nlu_entity] → [nlu_question?] → [nlu_answer?] → [nlu_intent?] →
[nlu_resolve] → [nlu_assemble] → interpret → integrate → select →
[nlg_strategy] → [nlg_plan] → [nlg_realize] → [nlg_post] → output
```
**State captured**: Very granular
**Visibility**: ⭐⭐⭐⭐⭐ (Maximum)
**Debuggability**: ⭐⭐⭐ (Overwhelming - too many stages)
**Flexibility**: ⭐⭐⭐⭐⭐ (Maximum)
**Complexity**: ⭐ (Too complex - graph is cluttered)

### Performance Comparison

**Scenario**: User says "What type of NDA?" (ask move)

| Architecture | NLU Time | NLG Time | Total | Inspectable Stages |
|--------------|----------|----------|-------|--------------------|
| 4-stage      | 500ms (hidden) | 50ms (hidden) | 550ms | 4 |
| 6-stage      | 500ms (visible) | 50ms (visible) | 550ms | 6 |
| 8-stage      | 200ms (classify) + 300ms (enrich) | 10ms (plan) + 40ms (realize) | 550ms | 8 |
| 14-stage     | 200ms + 150ms + 300ms + ... | 5ms + 5ms + 40ms + ... | 550ms | 14 |

**Key Insight**: 8-stage has same total time but better visibility into *where* time is spent.

### Debugging Comparison

**Scenario**: System misinterprets "Draft an NDA" as a question instead of command

#### 4-stage debugging:
1. Notice wrong response
2. Add logging to `engine.interpret()`
3. Re-run, grep logs
4. Find: dialogue act classifier returned "ask" with 0.51 confidence
5. Hypothesis: Classification threshold too low OR training data issue
6. Can't easily test - must modify engine

#### 6-stage debugging:
1. Notice wrong response
2. Inspect `state["nlu_result"]`:
   ```
   {"dialogue_act": "ask", "confidence": 0.51, ...}
   ```
3. Hypothesis: Classification confidence too low
4. Can test classifier independently

#### 8-stage debugging:
1. Notice wrong response
2. Inspect `state["nlu_classify_result"]`:
   ```
   {"dialogue_act": "ask", "confidence": 0.51,
    "raw_scores": {"ask": 0.51, "command": 0.49, ...}}
   ```
3. **AHA!** Very close scores (0.51 vs 0.49)
4. Inspect `state["nlu_enrich_result"]`:
   ```
   {"question_type": null, "question_details": null, ...}
   ```
5. **AHA!** Enrichment failed to find question structure
6. **Root cause**: Classifier marginally wrong, enrichment revealed error
7. **Fix**: Adjust classification prompt or add ensemble voting

**Winner**: 8-stage provides most diagnostic information

---

## Recommendation

### Adopt 8-Stage Pipeline

**Rationale**:
1. **Optimal granularity** - Not too coarse (4), not too fine (14)
2. **Conditional execution** - Skip expensive substages when not needed
3. **Targeted debugging** - Pinpoint exact failure location
4. **Component swapping** - Replace individual substages
5. **Performance tracking** - Measure each substage
6. **Still comprehensible** - 8 nodes is manageable in Burr UI

### Implementation Priority

**Phase 1** (Recommended): 6-stage pipeline (from `NLU_NLG_BURR_REFACTORING.md`)
- Proves the concept
- Major improvement over current 4-stage
- Lower risk

**Phase 2** (If Phase 1 succeeds): 8-stage pipeline (this document)
- Further decompose NLU/NLG
- Add conditional execution
- Add performance tracking

### Migration Path

```
Current (4-stage)
    ↓
6-stage (NLU/NLG explicit) ← Do this first
    ↓
8-stage (NLU/NLG substages) ← Do this if 6-stage succeeds
    ↓
Optional: Parallel execution for hot paths
```

---

## Conclusion

**Yes, NLU and NLG have meaningful substages** that should be exposed in the Burr loop:

**NLU Substages**:
1. `nlu_classify` - Fast classification + entity extraction
2. `nlu_enrich` - Conditional enrichment based on dialogue act

**NLG Substages**:
1. `nlg_plan` - Strategy selection + content planning
2. `nlg_realize` - Text generation + post-processing

**Result**: 8-stage pipeline that provides:
- **Conditional execution** (skip expensive enrichment)
- **Targeted debugging** (pinpoint failure location)
- **Component swapping** (replace individual substages)
- **Performance tracking** (measure each substage)
- **Comprehensible graph** (8 nodes still manageable)

**Next Step**: Implement 6-stage pipeline first (lower risk), then evaluate 8-stage based on experience.

---

## References

- `docs/NLU_NLG_BURR_REFACTORING.md` - 6-stage pipeline proposal
- `docs/SYSTEM_DESIGN_AND_LARSSON_ALIGNMENT.md` - Current architecture
- `docs/architecture_principles.md` - Policy #0 (architectural clarity)
- Burr Documentation: https://burr.dagworks.io/

---

**Document Version**: 1.0
**Last Updated**: 2025-11-15
**Authors**: Claude (AI Analysis)
**Status**: Architectural Exploration - Builds on 6-stage proposal
