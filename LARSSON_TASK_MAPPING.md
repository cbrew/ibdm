# LARSSON TASK MAPPING

**Status**: ✅ CURRENT
**Purpose**: Authoritative mapping of IBDM project tasks to Larsson (2002) thesis chapters
**Last Updated**: 2025-11-15
**For**: AI agents and developers working on IBDM implementation

---

## Overview

This document maps all IBDM beads tasks to the corresponding chapters and sections of Larsson's doctoral thesis. Understanding this mapping is critical for:

1. **Prioritization**: Tasks build incrementally following Larsson's IBiS1 → IBiS2 → IBiS3 → IBiS4 progression
2. **Implementation Fidelity**: Each task relates to specific algorithms, rules, or structures in the thesis
3. **Validation**: Metrics and tests verify compliance with Larsson's specifications

## Thesis Structure

Larsson's thesis presents four incremental dialogue systems:

- **IBiS1** (Chapter 2): Basic issue-based dialogue management (QUD, Plans, Update/Select)
- **IBiS2** (Chapter 3): Grounding issues (ICM, feedback, evidence requirements)
- **IBiS3** (Chapter 4): Addressing unraised issues (accommodation, private.issues)
- **IBiS4** (Chapter 5): Action-oriented and negotiative dialogue (device actions, IUN)

**Implementation Strategy**: Build IBiS1 and IBiS3 core features first (current focus), then add IBiS2 grounding and IBiS4 actions.

---

## Chapter 1: Introduction & TrindiKit Architecture

**Thesis Coverage**: Foundation, motivation, TrindiKit framework
**IBDM Equivalent**: Burr state machine + modern Python architecture

### Infrastructure Tasks

**Burr-Centric State Refactoring** (Modern TrindiKit):
- `ibdm-bsr` (P3): Phase 2.5: Burr-Centric State Refactoring
  - **Maps to**: TrindiKit Total Information State (Section 1.5)
  - **Purpose**: Pure functional engines, all state in Burr (no hidden mutations)

**Subtasks**:
- `ibdm-bsr.3-7`: Convert engines to pure functions (interpret, integrate, select, generate)
- `ibdm-bsr.14-16`: Refactor NLU context to use Burr state
- `ibdm-bsr.18-20`: Remove hybrid fallbacks, simplify configuration
- `ibdm-bsr.21-24`: Update tests and documentation

### Documentation Tasks

- `ibdm-accom.2.3` (P0): Update interpretation docstrings
- `ibdm-accom.5` (P1): Documentation updates
- `ibdm-loop.21-25` (P2): Documentation, user guides, CLAUDE.md updates

---

## Chapter 2: Basic Issue-Based Dialogue Management (IBiS1)

**Thesis Coverage**: Core IBDM architecture, QUD, plans, semantic operations, update/selection rules
**Implementation Status**: HIGHEST PRIORITY - Foundation for all other features

### 2.1 Core Architecture & Fidelity (Section 2.3)

**Demonstration & Validation**:
- `ibdm-82` (P0): Demo Goal 1: Larsson-Faithful IBDM
  - **Maps to**: Complete IBiS1 implementation demonstration
  - **Success Criteria**: All Section 2.8-2.9 rules demonstrated

**Metrics Framework**:
- `ibdm-metrics` (P3): Larsson Fidelity Metrics and Comprehensive Test Suite
- `ibdm-metrics.1` (P0): Q1: Define Larsson Fidelity Metrics Framework
  - **Maps to**: Quantifiable measurement of thesis compliance

**Specific Metrics**:
- `ibdm-metrics.1.1` (P0): Architectural compliance metrics
  - **Maps to**: Section 2.3.1 (four-phase architecture)
- `ibdm-metrics.1.2` (P0): Information state structure metrics
  - **Maps to**: Figure 2.2, Section 2.7.1
- `ibdm-metrics.1.3` (P0): Semantic operations coverage metrics
  - **Maps to**: Section 2.4.6-2.4.7 (resolves, combines, relevant, depends)
- `ibdm-metrics.1.4` (P0): Update rules coverage metrics
  - **Maps to**: Section 2.8 (all update rules)
- `ibdm-metrics.1.5` (P0): Selection rules coverage metrics
  - **Maps to**: Section 2.9 (all selection rules)
- `ibdm-metrics.1.6` (P0): Domain independence metrics
  - **Maps to**: Section 2.3.1 (rules vs. resources separation)
- `ibdm-metrics.1.7` (P0): Create Larsson fidelity scoring aggregator
  - **Purpose**: Overall compliance score

### 2.2 QUD & Information State (Sections 2.2, 2.7)

**Key Principle**: QUD is a stack (LIFO), not a set

**QUD Management**:
- `ibdm-loop.11` (P0): Verify QUD management across turns
  - **Maps to**: Section 2.2.3, Algorithm 2.2
  - **Validates**: Stack operations (push, pop), maximal question at top

**Information State Structure**:
- `ibdm-metrics.1.2` (P0): Define information state structure metrics
  - **Maps to**: Figure 2.2 (private.plan, private.bel, shared.qud, shared.com, shared.lu)

**Shared Context**:
- `ibdm-metrics.2.2` (P0): Define shared context metrics
  - **Maps to**: Section 2.2 (common ground, shared.com)

### 2.3 Plans (Section 2.6, 2.8.6)

**Key Principle**: Task plan formation happens in INTEGRATION phase, not interpretation

**Plan Tracking**:
- `ibdm-loop.12` (P0): Verify plan progress tracking
  - **Maps to**: Section 2.8.6 (FindPlan, ExecFindout, ExecRaise, ExecBind rules)
  - **Validates**: Plan execution, question accommodation from plans

**Plan-Aware Generation**:
- `ibdm-accom.3.1` (P1): Add plan-aware question generation helper
  - **Maps to**: Section 2.9 (plan-based selection)
- `ibdm-accom.3.2` (P1): Implement NDA-specific question templates
  - **Maps to**: Section 2.10 (domain adaptation)
- `ibdm-accom.3.3` (P2): Add plan progress feedback
  - **Purpose**: User visibility into task progress

**Complete Plan Enhancement**:
- `ibdm-accom.3` (P1): Phase 3: Enhance NLG with plan context
  - **Purpose**: Generate contextually appropriate questions from plans

### 2.4 Update Rules (Section 2.8)

**Key Principle**: Single rule application per cycle, first-applicable-rule selection

**Answer Integration**:
- `ibdm-loop.1` (P0): Review current answer integration rule
  - **Maps to**: Section 2.8.3 (IntegrateAnswer resolving/non-resolving)
  - **Critical**: Rule distinguishes resolves(A,Q) vs. relevant(A,Q)

**Clarification Handling**:
- `ibdm-loop.3` (P0): Handle invalid answers with clarification
  - **Maps to**: Section 2.8.3 (non-resolving answers keep Q on QUD)
  - **Related**: Also connects to Chapter 4 (accommodation)

**Multi-Turn Integration**:
- `ibdm-loop.10` (P0): Create multi-turn integration test
  - **Maps to**: Algorithm 2.2 (main control loop)
  - **Validates**: State updates across multiple turns

**Metrics**:
- `ibdm-metrics.1.4` (P0): Define update rules coverage metrics
  - **Validates**: GetLatestUtterance, IntegrateAsk, IntegrateAnswer, DowndateQUD, IntegrateGreet/Quit, FindPlan, ExecFindout, ExecRaise, ExecBind

### 2.5 Selection Rules (Section 2.9)

**Key Principle**: Plan-based + reactive selection

**Metrics**:
- `ibdm-metrics.1.5` (P0): Define selection rules coverage metrics
  - **Validates**: SelectFromPlan, SelectAsk, SelectAnswer, SelectGreet

### 2.6 Semantic Operations (Section 2.4)

**Core Relations**: resolves, combines, relevant, depends, postcond, dominates

**Metrics**:
- `ibdm-metrics.1.3` (P0): Define semantic operations coverage metrics
  - **Maps to**: Section 2.4.6-2.4.7
  - **Validates**: Domain-specific implementations in Travel/NDA domains

**Implementation**: See domain-specific tasks below

### 2.7 Domain Independence (Section 2.3.1, 2.10)

**Key Principle**: Domain-independent rules + domain-specific resources

**Code Organization**:
- `ibdm-66` (P0): Separate NLU/NLG domain-independent from domain-specific code
  - **Maps to**: Section 2.3.1 (DME rules vs. domain resources)
  - **Purpose**: Enable multi-domain deployment

**Refactoring Phases**:
- `ibdm-66.1`, `ibdm-67` (P0): Phase 1: Create NLG module infrastructure
- `ibdm-66.1.1`, `ibdm-67.1` (P0): Create template engine and domain generator base class
- `ibdm-68-72` (P2): Phases 2-6: Extract domain-specific code, restructure organization, refactor NLU, refactor generation rules, integration testing

**Domain Portability Demonstration**:
- `ibdm-84` (P0): Demo Goal 3: Domain Portability
  - **Maps to**: Section 2.10 (domain adaptation methodology)
  - **Success Criteria**: Same core engine works for Travel and NDA domains

**Domain Validation**:
- `ibdm-84.1` (P0): Verify NDA domain completeness
- `ibdm-85` (P0): Verify Travel domain completeness
- `ibdm-86` (P0): Domain switching in interactive demo
- `ibdm-87` (P0): NDA end-to-end validation
- `ibdm-88` (P0): Travel end-to-end validation

**Metrics**:
- `ibdm-metrics.1.6` (P0): Define domain independence metrics
  - **Validates**: Rules work across domains without modification

---

## Chapter 3: Grounding Issues (IBiS2)

**Thesis Coverage**: Interactive Communication Management (ICM), feedback, evidence requirements
**Implementation Status**: P1 priority (after IBiS1 and IBiS3 core)

### 3.1 Grounding Mechanisms (Section 3.6)

**Information State Extensions**: shared.moves, shared.next_moves (Figure 3.1)

**Grounding & ICM Implementation**:
- `ibdm-okw` (P1): Phase 6: Grounding and ICM
  - **Maps to**: Chapter 3 complete implementation

**Subtasks**:
- `ibdm-okw.1` (P1): Implement grounding mechanisms
  - **Maps to**: Section 3.6.3 (issue-based grounding)
- `ibdm-okw.2` (P1): Interactive communication management
  - **Maps to**: Section 3.2.3 (Allwood's ICM framework)
- `ibdm-okw.3` (P1): Feedback and clarification
  - **Maps to**: Section 3.4 (feedback classification), Section 3.6.1-3.6.2
- `ibdm-okw.4` (P1): Error handling and repair
  - **Maps to**: Section 3.6.9 (reraising issues), Section 3.4.8 (repair)

### 3.2 Turn Management (Section 3.5, 3.6.5)

**Metrics**:
- `ibdm-metrics.2.1` (P0): Define turn management metrics
  - **Maps to**: Section 3.6.5 (sequencing dialogue moves)
- `ibdm-metrics.2.4` (P1): Define conversation coherence metrics
  - **Maps to**: Section 3.5 (update strategies)

### 3.3 Multi-Party Conversation (Chapter 3 + Chapter 6)

**Metrics Framework**:
- `ibdm-metrics.2` (P0): Q2: Define Multi-Party Conversation Metrics
  - **Maps to**: Extensions of grounding for multi-agent scenarios
- `ibdm-metrics.2.3` (P0): Define conversation completeness metrics

---

## Chapter 4: Addressing Unraised Issues (IBiS3)

**Thesis Coverage**: Question accommodation (private.issues), clarification, dependent issues
**Implementation Status**: CRITICAL - Core accommodation refactoring in progress

### 4.1 Information State Extension (Section 4.5.1)

**New Field**: private.issues (accommodated but not yet raised questions)

**Figure 4.1**: IBiS3 Information State adds private.issues to IBiS2 state

### 4.2 Issue Accommodation (Sections 4.6.1-4.6.2)

**CRITICAL REFACTORING**:
- `ibdm-accom` (P0): **Refactor: Move Task Accommodation from Interpretation to Integration Phase**
  - **Maps to**: Rule 4.1 (IssueAccommodation) + Rule 4.2 (LocalQuestionAccommodation)
  - **Key Insight**: INTERPRET produces moves, INTEGRATE accommodates to private.issues, SELECT raises to shared.qud
  - **Why Critical**: Architectural fidelity - accommodation is pragmatic processing, not syntactic

**Flow**: Plan → private.issues (Rule 4.1) → shared.qud (Rule 4.2)

**Integration Testing**:
- `ibdm-accom.1.3` (P0): Update integration tests for accommodation
  - **Validates**: Two-phase accommodation flow

**Path Validation**:
- `ibdm-accom.4.1` (P1): Verify NLU engine creates correct move types
- `ibdm-accom.4.2` (P1): Test NLU → integration → accommodation path
- `ibdm-accom.4.3` (P2): Add logging for accommodation debugging
- `ibdm-accom.4.4` (P2): Add fallback to generic generation

**Complete Phase 4**:
- `ibdm-accom.4` (P1): Phase 4: Enhance NLG with plan context

**End-to-End Validation**:
- `ibdm-accom.5.1` (P1): Create comprehensive NDA workflow integration test
  - **Validates**: Complete accommodation flow in NDA domain
- `ibdm-accom.5.2` (P1): Test with both rule-based and NLU interpretation
- `ibdm-accom.5.3` (P1): Manual testing with interactive demo
- `ibdm-accom.5.4` (P2): Performance testing and benchmarking

### 4.3 Clarification (Section 4.6.3)

**Rule 4.3**: IssueClarification

**Implementation**:
- `ibdm-loop.2` (P0): Handle invalid answers with clarification
  - **Same as**: `ibdm-loop.3`
  - **Maps to**: Section 4.6.3 (push clarification question CQ to QUD)

### 4.4 Dependent Issues (Section 4.6.4)

**Rule 4.4**: DependentIssueAccommodation

**Semantic Operation**: depends(Q1, Q2) - Q1 depends on Q2 if answering Q2 is prerequisite

**Future Work**: Implement dependency graphs in domain models

### 4.5 Question Reaccommodation (Section 4.6.6)

**Rule 4.5**: QuestionReaccommodation (re-ask after non-resolving answer)

**Future Work**: Enhanced handling of persistent non-resolution

---

## Chapter 5: Action-Oriented and Negotiative Dialogue (IBiS4)

**Thesis Coverage**: Device actions, menu-based interaction, negotiation
**Implementation Status**: P1 priority (future work)

### 5.1 Information State Extension (Section 5.3.1)

**New Fields**: private.actions (device actions), private.iun (Issues Under Negotiation)

**Figure 5.1**: IBiS4 Information State

### 5.2 Action-Oriented Dialogue (Sections 5.4, 5.6)

**Future Work**: Not yet prioritized

**Would Include**:
- Rule 5.1: IntegrateRequest
- Rule 5.2: RejectRequest
- Rule 5.3: ExecuteAction
- Rule 5.4: ActionAccommodation
- Menu traversal (Section 5.4.2)
- Device integration (Section 5.4.1)

### 5.3 Negotiative Dialogue (Section 5.7)

**Future Work**: Issues Under Negotiation (IUN)

**Would Include**:
- Rule 5.5: IntroduceAlternative
- Dominance relations (Section 5.7.3)
- Alternative proposals

---

## Chapter 6: Conclusions & Advanced Features

**Thesis Coverage**: Dialogue typology, multi-party dialogue, future research
**Implementation Status**: P1-P2 (advanced features)

### 6.1 Multi-Party Dialogue

**Multi-Agent System**:
- `ibdm-tty` (P1): Phase 5: Multi-Agent System
  - **Maps to**: Section 6.5 (future research), extensions of grounding

**Subtasks**:
- `ibdm-tty.1` (P1): Implement Agent class
- `ibdm-tty.2` (P1): Implement MultiAgentDialogueSystem
- `ibdm-tty.3` (P1): Shared state synchronization
  - **Challenge**: Extend shared.com across multiple agents
- `ibdm-tty.4` (P1): Turn-taking and arbitration
  - **Challenge**: Algorithm 2.2 with multiple participants
- `ibdm-tty.5` (P1): Role-based specialization
- `ibdm-tty.6` (P1): Agent coordination protocols

**Metrics**:
- `ibdm-metrics.2` (P0): Q2: Define Multi-Party Conversation Metrics
- `ibdm-metrics.4.2` (P1): Implement multi-party conversation test suite
- `ibdm-metrics.5.2` (P2): Run multi-party conversation test suite

### 6.2 Integration and Testing

**Phase 7**:
- `ibdm-dus` (P0): Phase 7: Integration and Testing

**Subtasks**:
- `ibdm-dus.1` (P0): End-to-end integration tests
- `ibdm-dus.2` (P0): Multi-agent dialogue scenarios
- `ibdm-dus.3` (P0): Performance optimization
- `ibdm-dus.4` (P0): Documentation
- `ibdm-dus.5` (P0): Example applications

### 6.3 Advanced Features

**Phase 8**:
- `ibdm-xeh` (P0): Phase 8: Advanced Features

**Subtasks**:
- `ibdm-xeh.1` (P0): Natural language understanding integration
  - **Maps to**: Section 6.5.5 (NL input/output)
- `ibdm-xeh.2` (P0): Natural language generation integration
- `ibdm-xeh.3` (P0): Domain-specific knowledge bases
  - **Maps to**: Section 6.5.4 (general inference)
- `ibdm-xeh.4` (P0): Learning and adaptation
- `ibdm-xeh.5` (P0): Dialogue visualization tools

---

## Cross-Cutting Themes

### Natural Language Understanding/Generation

**LLM-Enhanced NLU** (relates to all chapters):
- `ibdm-64` (P1): Phase 3.5: LLM-Enhanced Natural Language Understanding
  - **Purpose**: Modern implementation of interpretation phase (Algorithm 2.2)
  - **ZFC Principle**: Delegate language understanding to LLM, keep dialogue management explicit

**Subtasks**:
- `ibdm-64.11` (P2): Implement intent recognition and task extraction
  - **Maps to**: Section 2.8.6 (FindPlan rule)
- `ibdm-64.12` (P2): Implement pragmatic understanding (indirect speech acts)
- `ibdm-64.13` (P1): Implement confidence scoring and uncertainty modeling
- `ibdm-64.15` (P2): Implement caching and performance optimization
- `ibdm-64.16` (P1): Implement error handling and recovery
- `ibdm-64.18` (P1): Create comprehensive NLU test suite
- `ibdm-64.19` (P2): Create NLU benchmark and evaluation framework
- `ibdm-64.20` (P2): NLU documentation and examples

**LLM-Powered Natural Language Demo**:
- `ibdm-83` (P0): Demo Goal 2: LLM-Powered Natural Language
  - **Purpose**: Show LLM interpretation + Larsson dialogue management

**NLU Integration Testing**:
- `ibdm-loop.6` (P0): Create comprehensive NLU engine integration test
- `ibdm-loop.7` (P0): Verify entity extraction integration
- `ibdm-loop.8` (P1): Test NLU + Domain integration
- `ibdm-loop.9` (P1): Test NLU error handling

**NLU Domain Mapping**:
- `ibdm-loop.14` (P1): Review NLUDomainMapper implementation
- `ibdm-loop.15` (P1): Integrate mapper into answer processing
- `ibdm-loop.16` (P1): Test entity mapping for all NDA types
- `ibdm-loop.17` (P2): Handle unmapped entities

**Demo Integration**:
- `ibdm-loop.18` (P1): Update demo configuration
- `ibdm-loop.19` (P1): Add progress display to demo
- `ibdm-loop.20` (P1): Test demo end-to-end

**Complete Loop**:
- `ibdm-loop` (P0): Complete Interactive Dialogue Loop Implementation
- `ibdm-loop.13` (P1): Verify domain validation throughout workflow

### Domain-Specific Implementations

**Travel Domain** (like Section 2.10):
- `ibdm-85` (P0): Verify Travel domain completeness
  - **Maps to**: Section 2.10 (travel information domain)
  - **Validates**: resolves, combines, depends relations for travel
- `ibdm-88` (P0): Travel end-to-end validation

**NDA Domain** (legal domain transfer):
- `ibdm-84.1` (P0): Verify NDA domain completeness
  - **Purpose**: Demonstrate domain portability beyond Larsson's examples
- `ibdm-87` (P0): NDA end-to-end validation

**Legal Domain Transfer Metrics**:
- `ibdm-metrics.3` (P0): Q3: Define Legal Domain Transfer Metrics
  - **Purpose**: Validate domain-independent approach on new domain
- `ibdm-metrics.3.1` (P0): Define NDA domain coverage metrics
- `ibdm-metrics.3.2` (P1): Define legal accuracy metrics
- `ibdm-metrics.3.3` (P0): Define entity recognition metrics
- `ibdm-metrics.3.4` (P0): Define domain-specific validation metrics
- `ibdm-metrics.3.5` (P1): Define NLU performance metrics for legal text

**Legal Domain Testing**:
- `ibdm-metrics.4.3` (P1): Implement legal domain transfer test suite
- `ibdm-metrics.5.3` (P2): Run legal domain transfer test suite
- `ibdm-metrics.5.4` (P2): Analyze results and identify gaps

### Testing & Metrics Framework

**Comprehensive Test Suite**:
- `ibdm-metrics.4` (P1): Implement Comprehensive Test Suite
  - **Purpose**: Automated Larsson fidelity validation

**Test Suite Components**:
- `ibdm-metrics.4.1` (P1): Implement Larsson fidelity test suite
  - **Validates**: All Chapter 2 (IBiS1) rules and structures
- `ibdm-metrics.4.2` (P1): Implement multi-party conversation test suite
  - **Validates**: Chapter 3 extensions for multi-agent
- `ibdm-metrics.4.3` (P1): Implement legal domain transfer test suite
  - **Validates**: Domain independence (Section 2.3.1)
- `ibdm-metrics.4.4` (P1): Create test data generators
- `ibdm-metrics.4.5` (P2): Create metrics reporting dashboard

**Test Execution & Reporting**:
- `ibdm-metrics.5` (P2): Run Test Suite and Generate Results
- `ibdm-metrics.5.1` (P2): Run Larsson fidelity test suite
- `ibdm-metrics.5.2` (P2): Run multi-party conversation test suite
- `ibdm-metrics.5.3` (P2): Run legal domain transfer test suite
- `ibdm-metrics.5.4` (P2): Analyze results and identify gaps
- `ibdm-metrics.5.5` (P2): Generate final comprehensive report
- `ibdm-metrics.5.6` (P2): Create improvement roadmap

**Documentation & Knowledge Transfer**:
- `ibdm-metrics.6` (P2): Documentation and Knowledge Transfer
- `ibdm-metrics.6.1` (P2): Document metrics framework
- `ibdm-metrics.6.2` (P2): Create test suite usage guide
- `ibdm-metrics.6.3` (P2): Update CLAUDE.md with metrics policy
- `ibdm-metrics.6.4` (P2): Set up continuous metrics monitoring

### Demonstration & Validation

**Demo Suite**:
- `ibdm-dem` (P0): IBDM-NLU Integration Demo Suite
  - **Purpose**: Interactive demonstration of Larsson implementation

**Stage 1 - Foundation**:
- `ibdm-dem.1` (P0): Stage 1: Foundation Demo - Basic NLU-IBDM Integration
- `ibdm-dem.1.1` (P0): Set up demo script structure and dependencies
- `ibdm-dem.1.2` (P0): Implement IBDM structure visualization helpers
  - **Shows**: private.plan, private.issues, shared.qud, shared.com (Figures 2.2, 4.1)
- `ibdm-dem.1.3` (P0): Implement metrics tracking and display
- `ibdm-dem.1.4` (P0): Create pre-scripted dialogue scenarios
- `ibdm-dem.1.5` (P0): Implement main dialogue loop with NLUDialogueEngine
- `ibdm-dem.1.6` (P0): Add final summary and metrics dashboard
- `ibdm-dem.1.7` (P1): Add tests and documentation for Stage 1 demo

**Stage 2 - Multi-Turn Context**:
- `ibdm-dem.2` (P0): Stage 2: Multi-Turn Context Demo - Complex Information Seeking
  - **Demonstrates**: QUD stack operations, plan progression, accommodation

---

## Implementation Priority Guidance

### Phase 1: IBiS1 Core (P0 - Current Focus)

**Foundation**:
1. `ibdm-bsr` - Burr state refactoring (TrindiKit equivalent)
2. `ibdm-82` - Larsson-faithful demo
3. `ibdm-metrics.1.*` - Larsson fidelity metrics

**Critical Tasks**:
4. `ibdm-loop.1-3, 10-12` - Answer integration, QUD, plans
5. `ibdm-84-88` - Domain portability validation

### Phase 2: IBiS3 Accommodation (P0 - Critical Refactoring)

**ARCHITECTURAL CHANGE**:
1. `ibdm-accom` - Move accommodation from INTERPRET to INTEGRATE
2. `ibdm-accom.1.3, 4.*, 5.*` - Testing and validation

**Rationale**: Accommodation is pragmatic processing (belongs in UPDATE/INTEGRATE), not syntactic parsing (INTERPRET)

### Phase 3: Domain Independence (P0-P2)

**Code Organization**:
1. `ibdm-66-72` - Separate domain-independent from domain-specific code
2. Domain validation for Travel and NDA

### Phase 4: NLU Integration (P0-P1)

**Modern Language Understanding**:
1. `ibdm-64.*` - LLM-enhanced NLU
2. `ibdm-loop.6-9, 14-17` - NLU integration testing
3. `ibdm-83` - LLM-powered NL demo

### Phase 5: IBiS2 Grounding (P1)

**After IBiS1 + IBiS3 stable**:
1. `ibdm-okw.*` - Grounding and ICM

### Phase 6: Multi-Party & Advanced (P1-P2)

**Extensions**:
1. `ibdm-tty.*` - Multi-agent system
2. `ibdm-dus.*` - Integration and testing
3. `ibdm-xeh.*` - Advanced features

### Phase 7: IBiS4 Actions (Future)

**Not yet prioritized**: Device actions and negotiation

---

## Key Architectural Principles from Larsson

### 1. Four-Phase Processing (Section 2.3.1)
- **INTERPRET**: Utterance → DialogueMove (syntactic/semantic only)
- **UPDATE**: DialogueMove → State changes (pragmatic processing)
- **SELECT**: Choose next system move
- **GENERATE**: Move → Natural language

**Critical**: Accommodation happens in UPDATE, not INTERPRET

### 2. Single Rule Application Per Cycle (Section 2.8.7)
- First-applicable-rule selection
- No parallel rule execution

### 3. QUD as Stack (Section 2.2.3)
- LIFO structure
- Top element is maximal question

### 4. Domain Independence (Section 2.3.1)
- Rules are domain-independent
- Domain knowledge in separate resources (lexicon, database, plans)

### 5. Accommodation Flow (Chapter 4)
- Questions enter private.issues first
- Then move to shared.qud (explicit raising)
- Enables incremental questioning

### 6. Explicit State (Section 2.7.1)
- All state visible in Information State
- No hidden mutations
- Pure functional engines (Burr implementation)

---

## References

### Primary Source
- **Larsson, S. (2002)**. Issue-Based Dialogue Management. Doctoral dissertation, Göteborg University.
  - **Local**: `docs/Larsson_Tesis_nopages.md`
  - **Algorithms**: `docs/LARSSON_ALGORITHMS.md`

### Project Documentation
- **Architecture**: `docs/architecture_principles.md` (Policy #0)
- **Roadmap**: `LARSSON_PRIORITY_ROADMAP.md`
- **Achievements**: `SYSTEM_ACHIEVEMENTS.md`
- **Development**: `CLAUDE.md` (Policies 10-14)

### Beads Tasks
- **View Ready**: `.claude/beads-helpers.sh ready`
- **View Current**: `.claude/beads-helpers.sh current`
- **Summary**: `.claude/beads-helpers.sh summary`

---

## Updates

**Maintenance**: This document should be updated when:
1. New tasks are created that relate to thesis chapters
2. Task priorities shift
3. Major architectural decisions affect thesis alignment
4. New thesis sections are implemented

**Last Major Update**: 2025-11-15 (Initial creation, comprehensive mapping)

---

## Historical Documentation

### Archived Planning Documents
These documents capture the original design and planning phases:

- **Development Plan**: `docs/archive/planning/DEVELOPMENT_PLAN.md` (📋 Original 8-phase implementation roadmap)
- **Demo Plan**: `docs/archive/planning/DEMO_PLAN.md` (✅ Comprehensive demonstration strategy)
- **NLU Enhancement Plan**: `docs/archive/planning/NLU_ENHANCEMENT_PLAN.md` (✅ Phase 3.5 LLM integration plan)
- **Project Structure**: `docs/archive/planning/PROJECT_STRUCTURE.md` (📋 Intended directory organization)

### Analysis & Status Reports
Detailed assessments and snapshots:

- **IBD-1 Completion Analysis**: `reports/ibd-1-completion-analysis.md`
  - Comprehensive analysis of IBD-1 vs. demonstration goals
  - IBiS1-4 alignment assessment
  - Larsson fidelity scoring

- **Project Status (2025-11-16)**: `reports/project-status-2025-11-16.md`
  - Complete status snapshot at IBD-1 completion
  - Technical statistics and metrics
  - Demo readiness assessment

### Archived Reviews
One-time technical reviews and verifications:

- **Hybrid Fallback Review**: `docs/archive/reviews/ibdm-64.14-review.md` (❌ Deprecated approach)
- **API Key Verification**: `docs/archive/reviews/IBDM_API_KEY_VERIFICATION.md` (✅ Initial setup validation)

### Quick References
- **Interpretation/Accommodation Issue**: `docs/interpretation-accommodation-quick-ref.md`
  - Quick reference for understanding task accommodation phase boundaries
  - Links to full analysis at `docs/architecture_interpretation_accommodation.md`