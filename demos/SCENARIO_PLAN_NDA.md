# Legal Document Generation Scenario Plan
## Demo: IBDM-NLU Integration for NDA Generation

**📋 STATUS: CURRENT** - Scenario design for NDA generation demo. Implementation complete in `03_nlu_integration_*.py` files.

**Document**: Non-Disclosure Agreement (NDA)
**Participants**: Attorney (User) ↔ Legal Document Generation System (Agent)
**Demo Files**:
- `demos/03_nlu_integration_interactive.py` (recommended - interactive)
- `demos/03_nlu_integration_basic.py` (pre-scripted)

---

## Executive Summary

This scenario demonstrates Issue-Based Dialogue Management (IBDM) concepts through a realistic legal document generation dialogue. An attorney interacts with a system to create a Non-Disclosure Agreement by answering structured questions. The demo showcases:

- **Natural Language Understanding**: Transforming legal terminology into structured DialogueMoves with Claude Sonnet 4.5
- **Question Under Discussion (QUD)**: Managing information gathering sequence
- **Entity Tracking**: Extracting and tracking legal entities (organizations, dates, jurisdictions)
- **Task Accommodation**: System infers document requirements from initial request
- **Domain-Driven Planning**: Uses NDA domain model for structured information gathering

---

## Document Domain: Non-Disclosure Agreement

### Why NDA?

NDAs are ideal for demonstration because they:
1. **Have well-defined structure**: Predictable information requirements
2. **Require multiple question types**: Wh-questions, alternatives, confirmations
3. **Involve entity extraction**: Organizations, dates, locations, durations
4. **Show practical value**: Real-world legal use case
5. **Are widely understood**: Familiar to most audiences

### Information Requirements

An NDA requires gathering:
- **Parties**: Disclosing party and receiving party (organizations/persons)
- **NDA Type**: Mutual or one-way
- **Effective Date**: When agreement becomes active
- **Duration**: Confidentiality period (e.g., 3 years)
- **Governing Law**: Jurisdiction (e.g., California, Delaware)
- **Optional**: Permitted disclosures, remedies, etc.

---

## Dialogue Flow (7 Turns)

### Turn 1: Task Initiation & Accommodation

**Attorney**: "I need to draft an NDA"

**NLU Processing**:
- Dialogue Act: `request`
- Intent: `draft_document`
- Document Type: `NDA`
- Strategy: Pattern matching (rule-based) → 0 tokens

**IBDM Processing**:
- Task Accommodation triggered
- System infers plan: `findout(parties, nda_type, effective_date, duration, governing_law)`
- First question pushed onto QUD stack

**System Response**: "I'll help you draft an NDA. What are the names of the parties entering into this agreement?"

**Information State After Turn 1**:
```
Private IS (Agent):
  - document_template: NDA_v1.0
  - plan: findout(parties, nda_type, effective_date, duration, governing_law)
  - current_goal: gather_parties

Shared IS:
  - QUD: [?x.parties]
  - commitments: []
  - dialogue_history: [request(attorney, draft_nda)]
  - gathered_info: {document_type: "NDA"}

Control IS:
  - turn: attorney
  - phase: information_gathering
```

**Visualization**:
- Show task accommodation in action
- Display inferred plan structure
- QUD stack: `[?x.parties]`

---

### Turn 2: WhQuestion - Parties

**System**: "What are the names of the parties entering into this agreement?"
- Move Type: `ask` (WhQuestion)
- Question: `?parties.name[role=disclosing_party,receiving_party]`

**Attorney**: "Between Acme Corporation as disclosing party and TechStart Incorporated"

**NLU Processing**:
- Dialogue Act: `answer`
- Strategy: Haiku 4.5 (entity extraction) → ~150 tokens
- Entity Extraction:
  - "Acme Corporation" → {type: ORG, role: disclosing_party}
  - "TechStart Incorporated" → {type: ORG, role: receiving_party}
- Semantic Parse: Answer resolving `?x.parties`

**IBDM Processing**:
- Answer integrates into shared IS
- Resolves `?x.parties` question
- Pops question from QUD
- Pushes next question: `?x.nda_type`

**System Response**: "Should this be a mutual NDA or one-way?"

**Information State Updates**:
```
Shared IS Changes:
  - QUD: [] → [?x.nda_type]
  - commitments: [parties(acme_corp, techstart_inc)]
  - gathered_info: {
      document_type: "NDA",
      parties: {
        disclosing: "Acme Corporation",
        receiving: "TechStart Incorporated"
      }
    }
  - entities: [
      {id: "ent1", text: "Acme Corporation", type: ORG, role: disclosing_party},
      {id: "ent2", text: "TechStart Incorporated", type: ORG, role: receiving_party}
    ]
```

**Visualization**:
- Entity extraction table showing organizations and roles
- QUD evolution: `[?x.parties]` → `[?x.nda_type]`
- Information checklist: ✓ Parties (2/6 gathered)

---

### Turn 3: AltQuestion - NDA Type

**System**: "Should this be a mutual NDA or one-way?"
- Move Type: `ask` (AltQuestion)
- Question: `?nda_type.value[alternatives=[mutual, one_way]]`
- Alternatives: `{mutual, one_way}`

**Attorney**: "Mutual NDA"

**NLU Processing**:
- Dialogue Act: `answer`
- Strategy: Pattern matching (keyword: "mutual") → 0 tokens
- Answer Type: Alternative selection
- Selected: `mutual`

**IBDM Processing**:
- Answer resolves `?x.nda_type` with value `mutual`
- Pops question from QUD
- Pushes next question: `?x.effective_date`

**System Response**: "What should the effective date be?"

**Information State Updates**:
```
Shared IS Changes:
  - QUD: [?x.nda_type] → [?x.effective_date]
  - gathered_info: {
      document_type: "NDA",
      nda_type: "mutual",
      parties: {...}
    }
```

**Visualization**:
- Alternative question display with choices highlighted
- QUD: `[?x.nda_type]` → `[?x.effective_date]`
- Information checklist: ✓ Parties, ✓ NDA Type (3/6 gathered)
- Strategy badge: GREEN (pattern matching, no cost)

---

### Turn 4: WhQuestion - Effective Date

**System**: "What should the effective date be?"
- Move Type: `ask` (WhQuestion)
- Question: `?effective_date.value[type=date]`

**Attorney**: "January 1st, 2025"

**NLU Processing**:
- Dialogue Act: `answer`
- Strategy: Haiku 4.5 (temporal parsing) → ~100 tokens
- Temporal Entity Extraction:
  - Raw: "January 1st, 2025"
  - Normalized: `2025-01-01`
  - Type: DATE
- Semantic Parse: Answer resolving `?x.effective_date`

**IBDM Processing**:
- Answer resolves `?x.effective_date` with value `2025-01-01`
- Pops question from QUD
- Pushes next question: `?x.duration`

**System Response**: "What should the confidentiality period be?"

**Information State Updates**:
```
Shared IS Changes:
  - QUD: [?x.effective_date] → [?x.duration]
  - gathered_info: {
      document_type: "NDA",
      nda_type: "mutual",
      parties: {...},
      effective_date: "2025-01-01"
    }
  - entities: [...,
      {id: "ent3", text: "January 1st, 2025", type: DATE, normalized: "2025-01-01"}
    ]
```

**Visualization**:
- Temporal normalization: "January 1st, 2025" → `2025-01-01`
- Entity table showing date parsing
- Information checklist: ✓ Parties, ✓ Type, ✓ Effective Date (4/6)
- Strategy badge: YELLOW (Haiku, low cost)

---

### Turn 5: WhQuestion - Duration

**System**: "What should the confidentiality period be?"
- Move Type: `ask` (WhQuestion)
- Question: `?duration.value[type=time_period]`

**Attorney**: "Three years"

**NLU Processing**:
- Dialogue Act: `answer`
- Strategy: Haiku 4.5 (duration parsing) → ~80 tokens
- Duration Entity Extraction:
  - Raw: "Three years"
  - Normalized: `{value: 3, unit: "years"}`
  - Type: DURATION
- Semantic Parse: Answer resolving `?x.duration`

**IBDM Processing**:
- Answer resolves `?x.duration` with value `{3, years}`
- Pops question from QUD
- Pushes next question: `?x.governing_law`

**System Response**: "Which state law should govern this agreement - California or Delaware?"

**Information State Updates**:
```
Shared IS Changes:
  - QUD: [?x.duration] → [?x.governing_law]
  - gathered_info: {
      document_type: "NDA",
      nda_type: "mutual",
      parties: {...},
      effective_date: "2025-01-01",
      duration: {value: 3, unit: "years"}
    }
  - entities: [...,
      {id: "ent4", text: "Three years", type: DURATION, normalized: {value: 3, unit: "years"}}
    ]
```

**Visualization**:
- Duration normalization display
- Information checklist: ✓ Parties, ✓ Type, ✓ Date, ✓ Duration (5/6)
- QUD: `[?x.duration]` → `[?x.governing_law]`

---

### Turn 6: AltQuestion - Governing Law

**System**: "Which state law should govern this agreement - California or Delaware?"
- Move Type: `ask` (AltQuestion)
- Question: `?governing_law.value[alternatives=[California, Delaware]]`
- Alternatives: `{California, Delaware}`

**Attorney**: "California law"

**NLU Processing**:
- Dialogue Act: `answer`
- Strategy: Pattern matching (state name recognition) → 0 tokens
- Location Entity Extraction:
  - "California" → {type: LOCATION, context: governing_law}
- Answer Type: Alternative selection
- Selected: `California`

**IBDM Processing**:
- Answer resolves `?x.governing_law` with value `California`
- Pops question from QUD
- All required information gathered
- Transitions to confirmation phase
- Pushes confirmation question: `?x.confirm_generation`

**System Response**: "I have all the information needed. Should I generate the NDA now?"

**Information State Updates**:
```
Shared IS Changes:
  - QUD: [?x.governing_law] → [?x.confirm_generation]
  - gathered_info: {
      document_type: "NDA",
      nda_type: "mutual",
      parties: {
        disclosing: "Acme Corporation",
        receiving: "TechStart Incorporated"
      },
      effective_date: "2025-01-01",
      duration: {value: 3, unit: "years"},
      governing_law: "California"
    }
  - entities: [...,
      {id: "ent5", text: "California", type: LOCATION, context: "governing_law"}
    ]

Control IS Changes:
  - phase: information_gathering → confirmation
```

**Visualization**:
- Information checklist: ALL COMPLETE ✓ (6/6)
- QUD empty (information gathering complete)
- Phase transition indicator
- Strategy badge: GREEN (pattern matching)

---

### Turn 7: YNQuestion - Confirmation

**System**: "I have all the information needed. Should I generate the NDA now?"
- Move Type: `ask` (YNQuestion)
- Question: `?confirm.generate_document`

**Attorney**: "Yes, generate it"

**NLU Processing**:
- Dialogue Act: `answer`
- Strategy: Pattern matching (affirmative keyword) → 0 tokens
- Answer Type: Affirmative (`yes`)

**IBDM Processing**:
- Answer resolves `?x.confirm_generation` with value `true`
- Pops question from QUD (now empty)
- Executes action: prepare document summary

**System Response**: [Displays gathered information summary]

```
═══════════════════════════════════════════════
         NDA DOCUMENT INFORMATION SUMMARY
═══════════════════════════════════════════════

Document Type: Non-Disclosure Agreement (NDA)
NDA Type:      Mutual (reciprocal confidentiality)

Parties:
  Disclosing Party:  Acme Corporation
  Receiving Party:   TechStart Incorporated

Terms:
  Effective Date:    January 1, 2025
  Duration:          3 years
  Governing Law:     California

Status: ✓ All information gathered
        ✓ Ready for document generation

═══════════════════════════════════════════════
```

**Final Information State**:
```
Shared IS Final:
  - QUD: []
  - gathered_info: {complete: true, ...all fields...}
  - entities: [5 total entities]
  - commitments: [all answers committed]
  - dialogue_history: [7 turns complete]

Control IS Final:
  - phase: confirmation → complete
  - status: ready_for_generation
```

**Visualization**:
- Document summary display (formatted table)
- Complete entity tracking table
- Final QUD state: EMPTY ✓
- Dialogue flow diagram showing all 7 turns
- Success indicator

---

## IBDM Concepts Demonstrated

### 1. Task Accommodation
- **Turn 1**: Attorney's request "draft an NDA" triggers plan inference
- System automatically determines required information fields
- Creates structured `findout` plan with sub-questions
- Demonstrates proactive dialogue management

### 2. Question Under Discussion (QUD) Stack
- **Dynamic management**: Questions pushed/popped as dialogue progresses
- **Ordering**: System controls information gathering sequence
- **Resolution**: Each answer resolves top question on stack
- **Visualization**: Tree/stack display showing evolution

```
Turn 1: [?x.parties]
Turn 2: [?x.nda_type]
Turn 3: [?x.effective_date]
Turn 4: [?x.duration]
Turn 5: [?x.governing_law]
Turn 6: [?x.confirm_generation]
Turn 7: []  ← Complete
```

### 3. Question Types
- **WhQuestion** (3 instances): Open-ended information gathering
  - Parties names
  - Effective date
  - Duration
- **AltQuestion** (2 instances): Constrained choice questions
  - NDA type (mutual vs. one-way)
  - Governing law (California vs. Delaware)
- **YNQuestion** (1 instance): Binary confirmation
  - Final generation confirmation

### 4. Entity Extraction & Tracking
Entities extracted and tracked across dialogue:
- **Organizations**: Acme Corporation, TechStart Incorporated
- **Dates**: January 1, 2025
- **Durations**: 3 years
- **Locations**: California

Each entity maintains:
- Raw text
- Normalized form
- Entity type
- Contextual role/attributes
- Cross-turn references

### 5. Information State Management

**Private IS (Agent)**:
- Document templates
- Validation rules
- Domain knowledge
- Generation capabilities
- Plan structure

**Shared IS**:
- QUD stack
- Gathered document parameters
- Commitments (agreed-upon facts)
- Entity tracking
- Dialogue history

**Control IS**:
- Turn-taking
- Dialogue phase (gathering → confirmation → complete)
- Error handling state

### 6. Hybrid Fallback Strategy

Strategy selection per turn:
- **Turn 1**: Pattern (keyword: "draft", "NDA") → 0 tokens
- **Turn 2**: Haiku (entity extraction) → ~150 tokens
- **Turn 3**: Pattern (keyword: "mutual") → 0 tokens
- **Turn 4**: Haiku (temporal parsing) → ~100 tokens
- **Turn 5**: Haiku (duration parsing) → ~80 tokens
- **Turn 6**: Pattern (state name) → 0 tokens
- **Turn 7**: Pattern (affirmative) → 0 tokens

**Total**: ~330 tokens vs. ~1,500 tokens if always using Sonnet
**Savings**: ~78% token reduction

### 7. Accommodation Mechanisms

**Task Accommodation**: Inferring document requirements from initial request

**Answer Accommodation**: Understanding implicit information
- "Between X and Y" → X is disclosing, Y is receiving
- "Mutual NDA" → reciprocal confidentiality obligations
- "Three years" → duration in temporal units

**Question Accommodation**: Adapting to context
- Alternative questions when choices are constrained
- Open questions when information is unconstrained

---

## Metrics to Track

### Per-Turn Metrics
- Strategy used (pattern/Haiku/Sonnet)
- Tokens: input + output
- Cost: based on strategy and tokens
- Latency: processing time
- Entity count: entities extracted this turn

### Cumulative Metrics
- Total tokens used
- Total cost
- Average latency per turn
- Strategy distribution (% each tier)
- Information gathering progress (N/6 fields)

### Final Summary Metrics
- Total turns: 7
- Questions asked: 6
- Questions resolved: 6
- Entities extracted: 5
- Total cost: ~$0.002 (with hybrid) vs ~$0.012 (always-Sonnet)
- Cost savings: ~83%
- Average latency: <500ms per turn

---

## Visualization Design

### Per-Turn Display

```
╔═══════════════════════════════════════════════════════════════╗
║  Turn 2 │ Attorney                                            ║
╚═══════════════════════════════════════════════════════════════╝

  "Between Acme Corporation as disclosing party and
   TechStart Incorporated"

┌─────────────────────────────────────────────────────────────┐
│ NLU Interpretation                                          │
├─────────────────────────────────────────────────────────────┤
│ Dialogue Act:    answer                                     │
│ Strategy:        Haiku 4.5 🟡                               │
│ Confidence:      0.95                                       │
│ Processing Time: 245ms                                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Entities Extracted                                          │
├─────────────────────────────────────────────────────────────┤
│ 🏢 Acme Corporation                                         │
│    Type: ORG | Role: disclosing_party                      │
│ 🏢 TechStart Incorporated                                   │
│    Type: ORG | Role: receiving_party                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ QUD Stack                                                   │
├─────────────────────────────────────────────────────────────┤
│ ✓ ?x.parties [RESOLVED]                                    │
│ ↓                                                           │
│ ▶ ?x.nda_type [CURRENT]                                    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Turn Metrics                                                │
├─────────────────────────────────────────────────────────────┤
│ Tokens: 120 in / 30 out │ Cost: $0.0004 │ Latency: 245ms │
└─────────────────────────────────────────────────────────────┘

╔═══════════════════════════════════════════════════════════════╗
║  System                                                       ║
╚═══════════════════════════════════════════════════════════════╝

  "Should this be a mutual NDA or one-way?"
```

### Final Dashboard

```
╔═════════════════════════════════════════════════════════════════╗
║                    DIALOGUE COMPLETE ✓                          ║
║              NDA Information Successfully Gathered              ║
╚═════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────┐
│ Document Information Checklist                                  │
├─────────────────────────────────────────────────────────────────┤
│ ✓ Parties:        Acme Corporation ↔ TechStart Incorporated   │
│ ✓ NDA Type:       Mutual                                       │
│ ✓ Effective Date: January 1, 2025                              │
│ ✓ Duration:       3 years                                      │
│ ✓ Governing Law:  California                                   │
│ ✓ Confirmation:   Approved                                     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Dialogue Statistics                                             │
├─────────────────────────────────────────────────────────────────┤
│ Total Turns:      7                                             │
│ Questions Asked:  6 (3 Wh, 2 Alt, 1 Y/N)                       │
│ Entities Found:   5 (2 ORG, 1 DATE, 1 DURATION, 1 LOCATION)   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Strategy Performance                                            │
├─────────────────────────────────────────────────────────────────┤
│ 🟢 Pattern Matching:  4 turns (57%) │   0 tokens │ $0.0000    │
│ 🟡 Haiku 4.5:         3 turns (43%) │ 330 tokens │ $0.0020    │
│ 🔴 Sonnet 4.5:        0 turns ( 0%) │   0 tokens │ $0.0000    │
├─────────────────────────────────────────────────────────────────┤
│ Total Cost: $0.0020                                             │
│ vs. Always-Sonnet: $0.0120 → 83% savings 💰                    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Performance                                                     │
├─────────────────────────────────────────────────────────────────┤
│ Average Latency: 420ms                                          │
│ Total Time:      2.94s                                          │
│ Tokens/Turn:     47 avg                                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Implementation Checklist

### Phase 1: Scenario Data Structure ✓
- [ ] Define 7 dialogue turns with utterances
- [ ] Specify expected IBDM structures per turn
- [ ] Map QUD evolution
- [ ] Define entity extraction requirements
- [ ] Create mock system responses

### Phase 2: Visualization Helpers
- [ ] Implement `format_question()` for Question objects
- [ ] Implement `format_dialogue_move()` for DialogueMove objects
- [ ] Implement `format_qud_stack()` for QUD visualization
- [ ] Implement `format_entities()` for entity table
- [ ] Implement `format_information_state()` for IS display
- [ ] Implement `format_turn_metrics()` for per-turn stats

### Phase 3: Main Dialogue Loop
- [ ] Initialize NLUDialogueEngine with hybrid strategy
- [ ] Create InformationState
- [ ] Implement turn-by-turn processing
- [ ] Capture metrics per turn
- [ ] Handle entity tracking across turns
- [ ] Display visualizations per turn

### Phase 4: Final Summary
- [ ] Implement document information checklist
- [ ] Create metrics dashboard
- [ ] Generate strategy performance breakdown
- [ ] Show entity relationship summary
- [ ] Display complete dialogue history

---

## Success Criteria

The demo successfully demonstrates IBDM-NLU integration when:

✅ **Functional Requirements**
- All 7 dialogue turns execute without errors
- All question types demonstrated (Wh, Alt, Y/N)
- Entity extraction works for all 5 entities
- QUD stack properly manages question flow
- Information State correctly updated each turn
- Hybrid strategy routing works as expected

✅ **Visualization Requirements**
- Clear, professional output using rich library
- IBDM structures are human-readable
- QUD evolution is visually obvious
- Entity tracking is clear
- Metrics are accurate and well-formatted

✅ **Educational Value**
- Demonstrates practical IBDM application
- Shows clear connection between NLU and IBDM
- Illustrates cost benefits of hybrid approach
- Provides realistic legal use case

✅ **Technical Quality**
- Code follows project policies (formatting, typing)
- Proper error handling
- Accurate metrics tracking
- Reproducible results

---

## Future Enhancements

Potential extensions for Stage 2 and Stage 3 demos:

1. **Multi-Document Support**: Handle different document types (contracts, agreements, etc.)
2. **Clarification Dialogues**: Add sub-dialogues for ambiguous inputs
3. **Validation**: Check for legal constraints and requirements
4. **Amendment Handling**: Modify previously provided information
5. **Entity Disambiguation**: Handle ambiguous entity references
6. **Multi-Party Scenarios**: More than 2 parties in agreement

---

## Appendix: Sample Code Snippets

### Dialogue Turn Definition

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class DialogueTurn:
    turn: int
    speaker: str  # "attorney" or "system"
    utterance: str
    expected_move_type: str
    expected_question_type: Optional[str]
    entities: list[dict]
    system_response: str
    qud_after: list[str]
```

### Entity Definition

```python
@dataclass
class ExtractedEntity:
    id: str
    text: str
    entity_type: str  # ORG, DATE, DURATION, LOCATION
    normalized: Optional[any]
    role: Optional[str]
    context: Optional[str]
```

### Metrics Tracking

```python
@dataclass
class TurnMetrics:
    turn: int
    strategy: str  # "pattern", "haiku", "sonnet"
    tokens_input: int
    tokens_output: int
    cost: float
    latency_ms: int
    entities_extracted: int
```

---

**Document Version**: 1.0
**Last Updated**: 2025-11-12
**Author**: IBDM Demo Team
