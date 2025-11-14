# Larsson-First Priority Roadmap

**Goal**: Achieve Larsson-compliant IBDM dialogue management + Modern LLM NLU/NLG

**Date**: 2025-11-14
**Basis**: Larsson (2002) thesis, CLAUDE.md policies, current implementation analysis

---

## Priority Framework

Tasks are prioritized based on:
1. **Larsson Compliance**: Does it implement core Larsson algorithms/structures?
2. **Architectural Correctness**: Does it fix phase separation violations?
3. **Foundation vs. Feature**: Foundation first (core loop, state management, semantic operations)
4. **Blocking Dependencies**: Critical infrastructure that blocks other work

---

## TIER 0: INFRASTRUCTURE (Resolved)

### ~~1. ibdm-zfl.9 - Configure IBDM_API_KEY~~ ✅ RESOLVED
**Status**: CLOSED - IBDM_API_KEY is available in container environment
**Note**: Per CLAUDE.md, IBDM_API_KEY is configured and accessible via `os.getenv("IBDM_API_KEY")`

---

## TIER 1: CORE LARSSON ARCHITECTURE (Foundation)

These tasks implement the fundamental Larsson algorithms and structures from docs/LARSSON_ALGORITHMS.md.

### 2. ibdm-loop - Complete Interactive Dialogue Loop (EPIC)
**Priority**: P0 → **TIER 1A - HIGHEST**
**Why**: Implements Larsson Algorithm 2.2 (Main Control Loop)
**Larsson Compliance**: Direct implementation of thesis Section 2.3.1
**CLAUDE.md**: Policy #12 (Larsson Algorithmic Principles)

**Critical Subtasks** (in order):

#### 2.1. ibdm-loop.2 - Add domain validation to answer integration
**Priority**: P0
**Why**: Implements `domain.resolves(answer, question)` semantic operation
**Larsson**: Section 2.4.3 - resolves/combines operations
**Impact**: Without this, answers are accepted without semantic validation

#### 2.2. ibdm-loop.3 - Handle invalid answers with clarification
**Priority**: P0
**Why**: Implements accommodation mechanism for failed validation
**Larsson**: IBiS3 accommodation (Section 3.4)
**Impact**: Enables robust error handling

#### 2.3. ibdm-loop.4 - Mark subplan complete after valid answer
**Priority**: P0
**Why**: Implements plan progression mechanism
**Larsson**: Plan execution (Section 2.6)
**Impact**: Task plans actually progress

#### 2.4. ibdm-loop.5 - Push next question to QUD after answer
**Priority**: P0
**Why**: Implements QUD stack management (LIFO)
**Larsson**: Algorithm 2.3 - QUD operations
**Impact**: Question flow and dialogue progression

#### 2.5. ibdm-loop.11 - Verify QUD management across turns
**Priority**: P0
**Why**: Validates QUD stack (core IBDM structure)
**Larsson**: QUD must be stack (LIFO), not set
**Impact**: Ensures proper question resolution order

#### 2.6. ibdm-loop.12 - Verify plan progress tracking
**Priority**: P0
**Why**: Validates plan execution mechanism
**Larsson**: Task plan completion tracking
**Impact**: Ensures tasks complete properly

### 3. ibdm-accom - Move Accommodation to Integration Phase (EPIC)
**Priority**: P0 → **TIER 1B - ARCHITECTURAL**
**Why**: Fixes fundamental phase separation violation
**Larsson Compliance**: Aligns with four-phase architecture (INTERPRET ≠ INTEGRATE)
**CLAUDE.md**: Policy #11 (Task Plan Formation in Integration Phase)

**Rationale**:
- Current: Accommodation in INTERPRETATION (wrong phase)
- Larsson: Interpretation = syntactic, Integration = pragmatic (plan formation)
- Problem: NLU engine bypasses interpretation rules → no accommodation

**Critical Subtasks** (in order):

#### 3.1. ibdm-accom.1.1 - Add accommodate_command integration rule
**Priority**: P0
**Why**: Moves plan creation to correct phase
**Impact**: Enables both rule-based and NLU paths to create task plans

#### 3.2. ibdm-accom.2.1 - Remove accommodate_nda_task from interpretation
**Priority**: P0
**Why**: Cleans up architectural violation
**Impact**: Clear phase separation

#### 3.3. ibdm-accom.2.2 - Remove task classifier from interpretation
**Priority**: P0
**Why**: Removes expensive LLM call from wrong phase
**Impact**: Cleaner architecture, better performance

### 4. ibdm-bsr - Burr-Centric State Refactoring (EPIC)
**Priority**: P0 → **TIER 1C - STATE MANAGEMENT**
**Why**: Implements "explicit state, pure functions" principle
**Larsson Compliance**: Engine methods must be pure (Section 2.3)
**CLAUDE.md**: Policy #12.8 (Explicit State, Pure Functions), Policy #0 (Architectural Clarity)

**Rationale**:
- Current: Engine has hidden internal state (self.state)
- Larsson: All state explicit, passed to functions
- Problem: State mutations invisible to Burr, can't restore/rollback

**Critical Subtasks** (Phase 1 - Foundation):

#### 4.1. ibdm-bsr.1 - Extract InformationState from engine to Burr State
**Priority**: P0
**Why**: Moves state out of engine into Burr
**Impact**: Foundation for stateless engine

#### 4.2. ibdm-bsr.2 - Update initialize action to create InformationState in Burr
**Priority**: P0
**Why**: Burr owns state creation
**Impact**: Burr becomes single source of truth

**Critical Subtasks** (Phase 2 - Stateless Engine):

#### 4.3. ibdm-bsr.3 - Convert interpret() to accept and return state
**Priority**: P0
**Why**: Makes interpret() pure function
**Larsson**: `interpret(utterance, state) → DialogueMoves`
**Impact**: Stateless interpretation

#### 4.4. ibdm-bsr.4 - Convert integrate() to pure function
**Priority**: P0
**Why**: Makes integrate() pure function
**Larsson**: `integrate(move, state) → InformationState`
**Impact**: Immutable state updates

#### 4.5. ibdm-bsr.5 - Convert select_action() to accept state parameter
**Priority**: P0
**Why**: Makes select() pure function
**Larsson**: `select(state) → DialogueMoves`
**Impact**: Stateless selection

#### 4.6. ibdm-bsr.6 - Convert generate() to accept state parameter
**Priority**: P0
**Why**: Makes generate() pure function
**Larsson**: `generate(move, state) → String`
**Impact**: Stateless generation

#### 4.7. ibdm-bsr.7 - Remove self.state completely from DialogueMoveEngine
**Priority**: P0
**Why**: Completes stateless transformation
**Impact**: Engine is now pure transformation library

---

## TIER 2: MODERN LLM INTEGRATION (NLU/NLG)

These tasks integrate modern LLMs while preserving Larsson dialogue management.

### 5. ibdm-64 - LLM-Enhanced NLU (EPIC)
**Priority**: P1 → **TIER 2A - NLU**
**Why**: Provides modern natural language understanding
**Larsson Compatibility**: LLM does INTERPRET phase, produces DialogueMoves
**CLAUDE.md**: Policy #9 (LiteLLM, Claude 4.5 models)

**Critical Subtasks**:

#### 5.1. ibdm-64.1 - Design LLM adapter interface
**Priority**: P0
**Why**: Foundation for all LLM usage
**Larsson**: Must produce IBDM structures (DialogueMoves, Questions)
**Impact**: Unified LLM access

#### 5.2. ibdm-64.2 - Implement prompt template system
**Priority**: P0
**Why**: Structured prompts for IBDM-compliant output
**Larsson**: Templates must guide LLM to produce Questions, not just text
**Impact**: Quality NLU output

#### 5.3. ibdm-64.4 - Implement semantic parsing
**Priority**: P1
**Why**: Utterance → DialogueMove transformation
**Larsson**: Core INTERPRET phase functionality
**Impact**: Natural language understanding

#### 5.4. ibdm-64.5 - Implement dialogue act classification
**Priority**: P1
**Why**: Recognize move types (ask, answer, request, greet)
**Larsson**: DialogueMove.type classification
**Impact**: Correct move interpretation

#### 5.5. ibdm-64.6 - Implement deep question understanding
**Priority**: P1
**Why**: Parse questions → WhQuestion/YNQuestion/AltQuestion
**Larsson**: Questions as first-class objects (Section 2.4)
**Impact**: Proper question representation

#### 5.6. ibdm-64.7 - Implement answer parsing and QUD matching
**Priority**: P1
**Why**: Parse answers, check relevance to QUD
**Larsson**: `relevant(answer, question)` operation
**Impact**: Answer validation

#### 5.7. ibdm-64.8 - Implement entity extraction
**Priority**: P1
**Why**: Extract ORGANIZATION, DATE, etc. from utterances
**Larsson**: Populate Answer.content with entities
**Impact**: Structured data from natural language

#### 5.8. ibdm-64.17 - Integrate NLU pipeline with IBDM engine
**Priority**: P1
**Why**: Connect NLU to dialogue loop
**Larsson**: NLU becomes INTERPRET phase implementation
**Impact**: End-to-end integration

### 6. NLG Enhancement Tasks
**Priority**: P2 → **TIER 2B - NLG**
**Why**: Natural language generation for responses
**Larsson Compatibility**: LLM does GENERATE phase, consumes DialogueMoves

**Note**: NLG is lower priority than NLU because template-based NLG works adequately. Focus on getting NLU + dialogue loop working first.

---

## TIER 3: VALIDATION & DEMONSTRATION

### 7. ibdm-metrics - Larsson Fidelity Metrics (EPIC)
**Priority**: P0 → **TIER 3A - VALIDATION**
**Why**: Measures Larsson compliance objectively
**Larsson Compliance**: Validates implementation against thesis
**CLAUDE.md**: Policy #12 (Verification Against Larsson)

**Critical Subtasks**:

#### 7.1. ibdm-metrics.1.1 - Define architectural compliance metrics
**Priority**: P0
**Why**: Measures four-phase architecture compliance
**Metrics**: Phase separation, rule organization, control loop structure

#### 7.2. ibdm-metrics.1.2 - Define information state structure metrics
**Priority**: P0
**Why**: Validates InformationState matches Larsson figures
**Metrics**: private/shared separation, QUD as stack, agenda structure

#### 7.3. ibdm-metrics.1.3 - Define semantic operations coverage metrics
**Priority**: P0
**Why**: Ensures resolves, combines, relevant, depends implemented
**Metrics**: Operation coverage, correctness tests

#### 7.4. ibdm-metrics.1.4 - Define update rules coverage metrics
**Priority**: P0
**Why**: Validates update rules match Larsson algorithms
**Metrics**: Rule count, precondition/effect correctness

#### 7.5. ibdm-metrics.1.5 - Define selection rules coverage metrics
**Priority**: P0
**Why**: Validates selection rules match Larsson algorithms
**Metrics**: Rule count, selection strategy correctness

#### 7.6. ibdm-metrics.1.6 - Define domain independence metrics
**Priority**: P0
**Why**: Ensures rules don't hardcode domain knowledge
**Metrics**: No domain predicates in rule code, uses domain resources

### 8. ibdm-dem - Integration Demo Suite (EPIC)
**Priority**: P0 → **TIER 3B - DEMONSTRATION**
**Why**: Validates end-to-end system works
**Larsson Compliance**: Shows all phases working together
**CLAUDE.md**: Demonstrates architectural success

**Critical Subtasks**:

#### 8.1. ibdm-dem.1 - Stage 1: Foundation Demo
**Priority**: P0
**Why**: Shows basic NLU-IBDM integration
**Demonstrates**: Four phases, QUD evolution, domain validation

**Substeps** (after loop + accommodation working):
- ibdm-dem.1.1 - Setup script structure
- ibdm-dem.1.2 - Visualization helpers
- ibdm-dem.1.3 - Metrics tracking
- ibdm-dem.1.4 - Pre-scripted scenarios
- ibdm-dem.1.5 - Main dialogue loop
- ibdm-dem.1.6 - Summary dashboard

---

## TIER 4: ADVANCED FEATURES

These are lower priority - focus on getting Tier 1-3 working first.

### 9. Advanced NLU Features (ibdm-64.*)
**Priority**: P2
**Examples**:
- ibdm-64.9 - Reference resolution
- ibdm-64.10 - Context-aware interpretation
- ibdm-64.11 - Intent recognition
- ibdm-64.12 - Pragmatic understanding

**Why Lower Priority**: Core loop must work first. These enhance UX but aren't critical for Larsson compliance.

### 10. Multi-Party Extensions
**Priority**: P2-P3
**Examples**: Multi-agent conversations, complex turn-taking

**Why Lower Priority**: Start with two-party (user-system) first.

---

## EXECUTION STRATEGY

### Phase A: Core Dialogue Loop (Week 1)
**Goal**: Larsson-compliant dialogue management

1. **ibdm-loop.2-5** - Domain validation and QUD management
   - Add domain.resolves() to answer integration
   - Handle invalid answers
   - Mark subplans complete
   - Push next question to QUD
   - Test with simple scenarios

2. **ibdm-loop.11-12** - Verification
   - Verify QUD stack behavior across turns
   - Verify plan progress tracking
   - Create multi-turn integration tests

### Phase B: Architectural Cleanup (Week 2)
**Goal**: Fix phase separation violations

3. **ibdm-accom.1-2** - Move accommodation to integration
   - Add accommodate_command rule in integration
   - Remove accommodation from interpretation
   - Update tests
   - Verify both rule-based and NLU paths work

### Phase C: Stateless Engine (Week 2-3)
**Goal**: Pure functions, explicit state

4. **ibdm-bsr.1-7** - Burr-centric refactoring
   - Extract InformationState to Burr (Phase 1)
   - Convert all engine methods to pure functions (Phase 2)
   - Update Burr actions (Phase 3)
   - Update tests
   - Verify state persistence/rollback

### Phase D: LLM Integration (Week 3-4)
**Goal**: Modern NLU with Larsson structures

5. **ibdm-64.1-2** - LLM adapter foundation
   - Design adapter interface
   - Implement prompt templates
   - Test with Claude 4.5 Haiku/Sonnet

6. **ibdm-64.4-8** - Core NLU pipeline
   - Semantic parsing (utterance → DialogueMove)
   - Dialogue act classification
   - Question understanding
   - Answer parsing
   - Entity extraction

7. **ibdm-64.17** - Integration
   - Connect NLU pipeline to IBDM engine
   - Test end-to-end

### Phase E: Validation & Demo (Week 4-5)
**Goal**: Prove it works

8. **ibdm-metrics.1** - Larsson fidelity metrics
   - Define all metric categories
   - Implement measurement
   - Generate compliance report

9. **ibdm-dem.1** - Foundation demo
    - Setup and visualization
    - Pre-scripted NDA dialogue
    - Metrics dashboard
    - Document results

---

## SUCCESS CRITERIA

### Larsson Compliance Checklist

- [ ] Four-phase architecture (Interpret → Integrate → Select → Generate)
- [ ] InformationState structure matches Larsson (private/shared/control)
- [ ] QUD is stack (LIFO), not set or unordered list
- [ ] Semantic operations implemented (resolves, combines, relevant)
- [ ] Domain model with predicates, sorts, plan builders
- [ ] Task plan formation in INTEGRATION phase (not interpretation)
- [ ] Update rules match Larsson algorithms
- [ ] Selection rules match Larsson algorithms
- [ ] Single rule application per cycle
- [ ] Engine methods are pure functions (explicit state passing)
- [ ] Domain independence (rules use domain resources, not hardcoded logic)

### Integration Checklist

- [ ] IBDM_API_KEY configured and working
- [ ] LiteLLM adapter with Claude 4.5 Haiku/Sonnet
- [ ] NLU produces IBDM structures (DialogueMoves, Questions)
- [ ] NLG consumes IBDM structures (DialogueMoves → natural language)
- [ ] End-to-end dialogue loop working
- [ ] Multi-turn conversations maintain QUD/plan state
- [ ] Domain validation working (answers validated against domain)
- [ ] Demo shows natural NDA dialogue

### Quality Metrics

- [ ] Larsson fidelity score: ≥95%
- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] Type checking clean (pyright)
- [ ] Code formatted (ruff)
- [ ] Documentation complete

---

## DEFERRED/LOW PRIORITY

The following are NOT critical for initial Larsson compliance:

- **ibdm-64.15** - Caching/performance optimization (P2)
- **ibdm-64.19** - Benchmarking (P2)
- **ibdm-64.20** - Documentation (P2) - do incrementally
- **ibdm-dem.2** - Multi-turn context demo (P2) - after Stage 1 working
- **Advanced NLU** - Reference resolution, pragmatics (P2)
- **Multi-party** - Complex conversations (P3)

Focus: Get core Larsson IBDM working with basic LLM NLU/NLG first!

---

## SUMMARY: TOP 10 TASKS IN ORDER

1. **ibdm-loop.2** - Add domain validation to answer integration
2. **ibdm-loop.3** - Handle invalid answers with clarification
3. **ibdm-loop.4** - Mark subplan complete after valid answer
4. **ibdm-loop.5** - Push next question to QUD after answer
5. **ibdm-loop.11** - Verify QUD management across turns
6. **ibdm-accom.1.1** - Add accommodate_command integration rule
7. **ibdm-accom.2.1** - Remove accommodate_nda_task from interpretation
8. **ibdm-bsr.1** - Extract InformationState from engine to Burr State
9. **ibdm-bsr.3-6** - Convert engine methods to pure functions
10. **ibdm-64.1-2** - LLM adapter and prompt templates

**Start Here**: ibdm-loop.2-5 (core dialogue loop), then ibdm-accom (phase separation), then ibdm-bsr (stateless engine).
