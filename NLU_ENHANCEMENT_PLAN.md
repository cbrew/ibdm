# LLM-Enhanced Natural Language Understanding Plan

## Overview

This plan enhances the IBDM system with sophisticated natural language understanding capabilities using modern LLMs (GPT-4, Claude, Llama, etc.). The current rule-based interpretation system will be augmented with deep semantic understanding.

## Current State

- **Existing**: Pattern-based rules using regex and keyword matching (`src/ibdm/rules/interpretation_rules.py`)
- **Limitations**:
  - Simple heuristics for question/answer classification
  - No entity extraction or tracking
  - Limited reference resolution
  - No semantic parsing
  - Cannot handle complex or ambiguous utterances

## Proposed Enhancement: Phase 3.5

### Epic: LLM-Enhanced Natural Language Understanding
**ID**: ibdm-64
**Priority**: 1
**Labels**: phase-3.5, nlu, llm

---

## Task Breakdown

### 1. Core Architecture & Infrastructure (Priority 0-1)

#### Task 1.1: Design LLM Adapter Interface and Abstraction Layer
**ID**: ibdm-64.1 (created)
**Priority**: 0
**Description**:
- Create IBDM-specific wrapper around LiteLLM for unified LLM access
- Support multiple providers through LiteLLM:
  - Google/Gemini (gemini-1.5-pro, gemini-1.5-flash) - Primary
  - OpenAI (gpt-4o, gpt-4o-mini) - Secondary
  - Local models via Ollama - Fallback
- Support async operations for parallel processing (litellm.acompletion)
- Implement batching for efficiency
- Provider-specific configuration (temperature, max_tokens, etc.)
- Rate limiting and quota management via LiteLLM
- Error handling with graceful fallback between providers
- Use environment variables for API keys (GEMINI_API_KEY, OPENAI_API_KEY)

**Deliverables**:
- `src/ibdm/nlu/llm_adapter.py` - LiteLLM wrapper for IBDM
- Configuration schema for LLM settings
- Provider fallback logic

---

#### Task 1.2: Implement Prompt Template System
**Priority**: 0
**Description**:
- Design composable prompt templates using Jinja2 or similar
- Templates for different NLU tasks:
  - Semantic parsing
  - Dialogue act classification
  - Entity extraction
  - Reference resolution
  - Question understanding
- Include few-shot examples for each task
- Chain-of-thought prompting for complex reasoning
- Dynamic example selection based on similarity
- Version control for prompts

**Deliverables**:
- `src/ibdm/nlu/prompts/` - Template directory
- `src/ibdm/nlu/prompt_manager.py` - Template loader and renderer
- Prompt versioning system

---

#### Task 1.3: Build LLM Response Parsing and Validation Framework
**Priority**: 1
**Description**:
- Parse structured outputs from LLMs:
  - JSON parsing with schema validation
  - XML/S-expression parsing for semantic representations
  - Fallback to text extraction if structured parsing fails
- Schema validation using Pydantic models
- Handle malformed responses gracefully
- Retry logic with corrective prompts
- Confidence scoring based on response quality

**Deliverables**:
- `src/ibdm/nlu/response_parser.py`
- Pydantic schemas for all NLU outputs
- Validation and retry logic

---

### 2. Core Understanding Capabilities (Priority 1)

#### Task 2.1: Implement Semantic Parsing
**Priority**: 1
**Description**:
- Parse natural language utterances into structured semantic representations
- Extract predicate-argument structures
- Identify semantic roles (agent, patient, theme, etc.)
- Map to IBDM DialogueMove format
- Handle complex compositional semantics
- Support multiple semantic frameworks:
  - First-order logic
  - Dependency-based semantics
  - Frame semantics

**Deliverables**:
- `src/ibdm/nlu/semantic_parser.py`
- Semantic representation data structures
- Integration with DialogueMove classes

---

#### Task 2.2: Implement Dialogue Act Classification
**Priority**: 1
**Description**:
- Classify utterances into dialogue acts using LLM
- Support ISO 24617-2 dialogue act taxonomy:
  - Information-seeking: question, set-question, choice-question
  - Information-providing: inform, answer, confirm, disconfirm
  - Commissives: offer, promise, threat
  - Directives: request, instruct, suggest
  - Social: greeting, apology, thanking, goodbye
- Handle multi-functional utterances (composite acts)
- Map dialogue acts to IBDM move types
- Confidence scoring per dialogue act

**Deliverables**:
- `src/ibdm/nlu/dialogue_act_classifier.py`
- Dialogue act taxonomy definitions
- Mapping to IBDM DialogueMove types

---

#### Task 2.3: Implement Deep Question Understanding
**Priority**: 1
**Description**:
- Go beyond simple question type classification:
  - Question types: wh-, yes/no, alternative, tag, rhetorical
  - Question focus and topic identification
  - Presuppositions extraction
  - Implicit constraints and scope
  - Polar vs. alternative readings
- Identify Question Under Discussion (QUD) candidates
- Extract question variables and their constraints
- Detect complex/nested questions
- Handle indirect questions

**Deliverables**:
- `src/ibdm/nlu/question_understander.py`
- Enhanced Question data structures with semantic annotations
- QUD candidate ranking

---

#### Task 2.4: Implement Answer Parsing and QUD Matching
**Priority**: 1
**Description**:
- Parse answers and match to questions on QUD stack
- Handle different answer types:
  - Direct answers
  - Partial answers
  - Over-informative answers
  - Indirect answers
  - Evasive responses
- Extract propositional content from answers
- Match answer content to question variables
- Identify new vs. confirmed information
- Handle answer ellipsis and fragments

**Deliverables**:
- `src/ibdm/nlu/answer_parser.py`
- Answer-question matching logic
- Integration with QUD stack

---

### 3. Advanced NLU Features (Priority 1-2)

#### Task 3.1: Implement Entity Extraction and Tracking
**Priority**: 1
**Description**:
- Extract named entities using LLM:
  - Persons, organizations, locations
  - Temporal expressions
  - Numerical values and measurements
  - Domain-specific entities
- Track entities across dialogue turns
- Maintain entity coreference chains
- Build discourse entity database
- Link entities to information state

**Deliverables**:
- `src/ibdm/nlu/entity_extractor.py`
- Entity tracking system
- Integration with InformationState

---

#### Task 3.2: Implement Reference Resolution
**Priority**: 1
**Description**:
- Resolve pronouns and definite references:
  - Personal pronouns (he, she, they, it)
  - Demonstratives (this, that, these, those)
  - Definite descriptions (the X)
  - One-anaphora
- Use discourse context from InformationState
- Leverage salience and recency heuristics
- Handle ambiguous references
- Integrate with entity tracking

**Deliverables**:
- `src/ibdm/nlu/reference_resolver.py`
- Salience-based ranking
- Integration with entity tracking

---

#### Task 3.3: Implement Context-Aware Interpretation Pipeline
**Priority**: 1
**Description**:
- Build end-to-end NLU pipeline that uses dialogue context:
  - Access to full InformationState
  - QUD stack context
  - Commitment store context
  - Recent dialogue history
- Context-sensitive semantic parsing
- Pragmatic interpretation using Gricean maxims
- Conversational implicature detection
- Topic tracking and shift detection

**Deliverables**:
- `src/ibdm/nlu/context_interpreter.py`
- Pipeline orchestration
- Context integration logic

---

#### Task 3.4: Implement Intent Recognition and Task Extraction
**Priority**: 2
**Description**:
- Identify user intents beyond dialogue acts:
  - Information-seeking intent
  - Task completion intent
  - Clarification intent
  - Negotiation intent
- Extract task parameters and constraints
- Identify user goals and plans
- Multi-intent detection
- Intent confidence scoring

**Deliverables**:
- `src/ibdm/nlu/intent_recognizer.py`
- Intent taxonomy
- Task parameter extraction

---

#### Task 3.5: Implement Pragmatic Understanding
**Priority**: 2
**Description**:
- Detect indirect speech acts:
  - Requests phrased as questions ("Can you...?")
  - Suggestions as statements
  - Refusals and acceptances
- Identify politeness strategies
- Detect sarcasm and irony (if needed)
- Handle figurative language
- Cultural and social context awareness

**Deliverables**:
- `src/ibdm/nlu/pragmatics.py`
- Indirect speech act detection
- Politeness feature extraction

---

### 4. Optimization & Robustness (Priority 1-2)

#### Task 4.1: Implement Confidence Scoring and Uncertainty Modeling
**Priority**: 1
**Description**:
- Confidence scores for all NLU outputs:
  - Semantic parses
  - Dialogue acts
  - Entity extractions
  - Reference resolutions
- Calibrate confidence scores
- Uncertainty propagation through pipeline
- Decision thresholds for triggering clarification
- Confidence-based selection between interpretations

**Deliverables**:
- `src/ibdm/nlu/confidence.py`
- Calibration methodology
- Integration with selection rules

---

#### Task 4.2: Implement Fallback Strategies and Hybrid Approach
**Priority**: 1
**Description**:
- Integrate LLM-based NLU with existing rule-based system:
  - Use rules as fast path for simple cases
  - LLM for complex/ambiguous cases
  - Fallback to rules if LLM fails
  - Ensemble methods combining both approaches
- Graceful degradation when LLM unavailable
- Cost-aware processing (use cheaper models when possible)
- Latency optimization

**Deliverables**:
- `src/ibdm/nlu/hybrid_interpreter.py`
- Fallback logic
- Cost and latency monitoring

---

#### Task 4.3: Implement Caching and Performance Optimization
**Priority**: 2
**Description**:
- Cache LLM responses:
  - Semantic caching (similar utterances)
  - Exact match caching
  - Cache invalidation strategies
- Batch processing for multiple utterances
- Async processing with queues
- Prefetching for predictable patterns
- Monitor and optimize token usage
- Streaming responses for real-time feel

**Deliverables**:
- `src/ibdm/nlu/cache.py`
- Performance monitoring
- Optimization strategies

---

#### Task 4.4: Implement Error Handling and Recovery
**Priority**: 1
**Description**:
- Handle LLM failures gracefully:
  - API errors and timeouts
  - Rate limiting
  - Malformed responses
  - Unexpected content
- Retry strategies with exponential backoff
- Circuit breaker pattern for failing providers
- Logging and monitoring
- User-facing error messages

**Deliverables**:
- `src/ibdm/nlu/error_handler.py`
- Retry logic
- Circuit breaker implementation

---

### 5. Integration & Testing (Priority 1-2)

#### Task 5.1: Integrate NLU Pipeline with IBDM Engine
**Priority**: 1
**Description**:
- Replace/augment existing interpretation rules with NLU pipeline
- Maintain backward compatibility
- Configuration for enabling/disabling LLM features
- Performance comparison with rule-based system
- Gradual rollout mechanism

**Deliverables**:
- Modified interpretation rules that call NLU pipeline
- Configuration system
- Feature flags

---

#### Task 5.2: Create Comprehensive NLU Test Suite
**Priority**: 1
**Description**:
- Unit tests for all NLU components
- Integration tests for full pipeline
- Test datasets:
  - Question understanding
  - Answer parsing
  - Reference resolution
  - Entity extraction
  - Dialogue act classification
- Property-based testing for robustness
- Adversarial examples
- Cross-linguistic testing (if applicable)

**Deliverables**:
- `tests/nlu/` - comprehensive test suite
- Test datasets
- Continuous testing framework

---

#### Task 5.3: Create NLU Benchmark and Evaluation Framework
**Priority**: 2
**Description**:
- Benchmark dataset for IBDM-style dialogues
- Evaluation metrics:
  - Semantic parsing accuracy
  - Dialogue act F1 score
  - Entity extraction precision/recall
  - Reference resolution accuracy
  - End-to-end dialogue success rate
- Comparison with baseline rule-based system
- Error analysis tools
- Ablation studies

**Deliverables**:
- `benchmarks/nlu/` - evaluation framework
- Benchmark datasets
- Evaluation scripts and reporting

---

#### Task 5.4: Documentation and Examples
**Priority**: 2
**Description**:
- API documentation for NLU components
- Architecture documentation
- Prompt engineering guide
- Configuration guide
- Example applications demonstrating NLU capabilities
- Best practices and troubleshooting guide

**Deliverables**:
- `docs/nlu/` - comprehensive documentation
- Example applications
- Tutorials

---

## Dependencies

- Phase 1 (Core Foundation): ✅ Complete
- Phase 2 (Burr Integration): ✅ Complete
- Phase 3 (Rule Development): ✅ Complete

## Success Criteria

1. **Accuracy**: NLU pipeline achieves >85% accuracy on benchmark dialogues
2. **Latency**: Average interpretation latency <500ms for common cases
3. **Robustness**: Graceful handling of malformed/unexpected input
4. **Flexibility**: Support for multiple LLM providers
5. **Cost-efficiency**: Optimized token usage through caching and batching

## Timeline Estimate

- Architecture & Infrastructure: 1 week
- Core Understanding: 2 weeks
- Advanced Features: 2 weeks
- Optimization & Integration: 1 week
- Testing & Documentation: 1 week

**Total**: ~7 weeks

## Technology Stack

- **LLM Interface**: LiteLLM (unified API for multiple providers)
- **LLM Providers** (priority order):
  1. Google/Gemini (gemini-1.5-pro, gemini-1.5-flash) - First choice
  2. OpenAI (gpt-4o, gpt-4o-mini) - Second choice
  3. Local models via Ollama - Fallback
- **API Keys**: Available via environment variables (GEMINI_API_KEY, OPENAI_API_KEY)
- **Prompt Engineering**: Jinja2, custom template system
- **Parsing**: Pydantic, JSON Schema
- **Caching**: Redis or in-memory LRU cache
- **Testing**: pytest, hypothesis (property testing)

## Notes

- This enhancement maintains backward compatibility with existing rule-based system
- Designed for gradual adoption - can enable/disable LLM features via configuration
- Cost-aware design with caching and fallbacks to minimize API usage
- Focus on IBDM-specific dialogue patterns (QUD, accommodation, grounding)
