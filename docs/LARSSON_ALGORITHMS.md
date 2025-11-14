# Larsson (2002) - IBDM Algorithmic Reference

**Source**: Larsson, S. (2002). Issue-Based Dialogue Management. Doctoral dissertation.
**Purpose**: Authoritative algorithmic reference for IBDM implementation
**Status**: Extracted from `docs/larsson_thesis/` (OCR-corrected chapters)

---

## Table of Contents

1. [Core Architecture](#core-architecture)
2. [Control Algorithm](#control-algorithm)
3. [Information State Structures](#information-state-structures)
4. [Semantic Operations](#semantic-operations)
5. [Update Rules by System](#update-rules-by-system)
6. [Selection Rules by System](#selection-rules-by-system)
7. [Implementation Checklists](#implementation-checklists)

---

## Core Architecture

### Four-Phase Dialogue Processing

Larsson's IBDM uses a **four-phase architecture** (Section 2.3.1):

```
┌─────────────────────────────────────────────────────────┐
│                    CONTROL LOOP                          │
│                                                          │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌─────┐ │
│  │  INPUT   │──>│ INTERPRET│──>│  UPDATE  │──>│ ... │ │
│  └──────────┘   └──────────┘   └──────────┘   └─────┘ │
│                                                          │
│  ┌─────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐ │
│  │ ... │──>│  SELECT  │──>│ GENERATE │──>│  OUTPUT  │ │
│  └─────┘   └──────────┘   └──────────┘   └──────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Phase Descriptions:**

1. **INTERPRET** (Interpretation Phase)
   - Parse utterance to dialogue moves
   - Syntactic/semantic processing only
   - No state updates
   - **Output**: List of DialogueMove objects

2. **UPDATE** (Integration Phase)
   - Apply dialogue moves to information state
   - Pragmatic processing
   - Task plan formation
   - Question accommodation
   - **Output**: Updated InformationState

3. **SELECT** (Selection Phase)
   - Choose next system action
   - Apply selection rules
   - Plan-based and reactive selection
   - **Output**: List of DialogueMove objects

4. **GENERATE** (Generation Phase)
   - Convert dialogue moves to natural language
   - Surface realization
   - **Output**: String utterance

### Dialogue Move Engine (DME)

The DME consists of two modules (Section 2.3.1):

- **Update Module**: Applies update rules to modify information state
- **Select Module**: Applies selection rules to choose next moves

**Key Principle**: Domain-independent rules + domain-specific resources

---

## Control Algorithm

### Algorithm 2.2: Main Control Loop (Section 2.3.1)

```
repeat {
    select                           // Choose next system move(s)
    if not isEmpty($nextMoves) {
        generate                     // Convert moves to strings
        output                       // Output to user
        update                       // Update state after output
    }
    test($programState == run)       // Check if continuing
    input                            // Get user input
    interpret                        // Parse to moves
    update                           // Integrate user moves
}
```

**Turn-Taking Principle** (Section 2.3.1, line 227-231):
- If select finds a move to perform → system takes turn
- If select finds no move → turn handed to user
- One update cycle per turn

**Critical Rules**:
1. Select runs BEFORE system output
2. Update runs AFTER each output and input
3. Single rule application per update cycle
4. First-applicable-rule selection

---

## Information State Structures

### IBiS1 Information State (Figure 2.2, Chapter 2)

```
record [
    private : record [
        agenda : oset(Action)
        plan   : list(Plan)
        bel    : set(Proposition)
    ]
    shared : record [
        com     : set(Proposition)    // Commitments/common ground
        qud     : stack(Question)     // Questions Under Discussion
        lu      : Move                // Latest utterance/move
    ]
]
```

**Key Fields**:
- `private.plan`: Task plans containing questions to ask
- `shared.qud`: Stack of active questions (LIFO)
- `shared.com`: Common ground (agreed propositions)
- `shared.lu`: Latest move for sequencing rules

### IBiS2 Information State (Figure 3.1, Chapter 3)

**Extensions for Grounding**:

```
record [
    private : record [
        agenda : oset(Action)
        plan   : list(Plan)
        bel    : set(Proposition)
    ]
    shared : record [
        com     : set(Proposition)
        qud     : stack(Question)
        lu      : LatestMove
        // NEW FIELDS:
        moves   : stack(Move)         // Move history
        next_moves : oset(Move)       // Pending system moves
    ]
]
```

**Grounding Extensions**:
- `shared.moves`: History of all moves for grounding tracking
- `shared.next_moves`: System moves awaiting execution

### IBiS3 Information State (Figure 4.1, Chapter 4)

**Extensions for Accommodation**:

```
record [
    private : record [
        agenda : oset(Action)
        plan   : list(Plan)
        bel    : set(Proposition)
        // NEW FIELD:
        issues : oset(Question)       // Accommodated but not yet raised
    ]
    shared : record [
        com     : set(Proposition)
        qud     : stack(Question)
        lu      : LatestMove
        moves   : stack(Move)
        next_moves : oset(Move)
    ]
]
```

**Accommodation Flow**:
1. Questions enter `private.issues` (accommodation)
2. Questions move to `shared.qud` (explicit raising)
3. Separation enables incremental questioning

### IBiS4 Information State (Figure 5.1, Chapter 5)

**Extensions for Action-Oriented Dialogue**:

```
record [
    private : record [
        agenda : oset(Action)
        plan   : list(Plan)
        bel    : set(Proposition)
        issues : oset(Question)
        // NEW FIELDS:
        actions : oset(Action)        // Pending device actions
        iun     : oset(Proposition)   // Issues Under Negotiation
    ]
    shared : record [
        com     : set(Proposition)
        qud     : stack(Question)
        lu      : LatestMove
        moves   : stack(Move)
        next_moves : oset(Move)
    ]
]
```

**Action Extensions**:
- `private.actions`: Device actions to execute
- `private.iun`: Propositions under negotiation (alternatives)

---

## Semantic Operations

### Core Relations (Chapter 2, Sections 2.4.6-2.4.7)

#### 1. **resolves(Answer, Question) → Boolean**

**Definition**: Answer A resolves Question Q if A provides the information requested by Q.

**Examples** (Table 2.1):
```
resolves(yes, ?P)           = true   // Yes/no answer
resolves(paris, ?X.city(X)) = true   // Wh-answer
resolves(no, ?P)            = true   // Negative answer
resolves(monday, ?X.day(X)) = true   // Short answer
```

**Not Resolving** (Table 2.2):
```
resolves(paris, ?X.country(X)) = false  // Wrong sort
resolves(maybe, ?P)            = false  // Not definitive
```

#### 2. **combines(Question, Answer) → Proposition**

**Definition**: Combines question and short answer into full proposition.

**Examples** (Table 2.3):
```
combines(?X.city(X), paris)    = city(paris)
combines(?X.day(X), monday)    = day(monday)
combines(?P, yes)              = P
combines(?P, no)               = not(P)
```

#### 3. **relevant(Answer, Question) → Boolean**

**Definition**: Answer is relevant to Question even if not resolving.

**Examples**:
```
relevant(paris, ?X.city(X))     = true   // Resolves
relevant(dontknow, ?X.city(X))  = true   // Relevant non-answer
relevant(france, ?X.city(X))    = true   // Related but wrong sort
```

#### 4. **depends(Question1, Question2) → Boolean**

**Definition**: Q1 depends on Q2 if answering Q2 is prerequisite to answering Q1.

**Examples** (Section 4.6.4):
```
depends(?price, ?departure_city)  = true   // Need city to find price
depends(?price, ?day)             = true   // Need day for price
depends(?X.city(X), ?P)           = false  // Independent
```

**Implementation**: Defined in domain model via plan structure or dependency graph.

#### 5. **postcond(Action) → Proposition**

**Definition**: Returns the postcondition (effect) of an action.

**Examples** (Section 5.4.3):
```
postcond(findout(?X.city(X)))    = city(X)      // Finding out makes it known
postcond(action(playVCR))        = playing(vcr) // Action effect
```

#### 6. **dominates(Proposition1, Proposition2) → Boolean**

**Definition**: P1 dominates P2 if P1 is more specific or preferred than P2 in negotiation.

**Examples** (Section 5.7.3):
```
dominates(paris_hotel_X, paris_hotel_Y) = true   // Better rated
dominates(price_100, price_200)         = true   // Cheaper
```

---

## Update Rules by System

### IBiS1 Update Rules (Chapter 2, Section 2.8)

#### Rule: GetLatestUtterance
**Pre**: Latest move available from interpretation
**Effect**: `shared.lu := latestMove`
**Section**: 2.8.1

#### Rule: IntegrateAsk
**Pre**: `shared.lu.type == ask` AND `shared.lu.content == Q`
**Effect**:
- `push(shared.qud, Q)`
- Clear `shared.lu`

**Section**: 2.8.2
**Description**: User asks question → push to QUD

#### Rule: IntegrateAnswer (Resolving)
**Pre**:
- `shared.lu.type == answer`
- `shared.lu.content == A`
- `top(shared.qud) == Q`
- `resolves(A, Q)`

**Effect**:
- `P := combines(Q, A)`
- `add(shared.com, P)`
- `pop(shared.qud)`
- Clear `shared.lu`

**Section**: 2.8.3
**Description**: Resolving answer → add to common ground, pop question

#### Rule: IntegrateAnswer (NonResolving)
**Pre**:
- `shared.lu.type == answer`
- `shared.lu.content == A`
- `top(shared.qud) == Q`
- `NOT resolves(A, Q)` BUT `relevant(A, Q)`

**Effect**:
- Record non-resolving answer (strategy-dependent)
- Keep Q on QUD
- Clear `shared.lu`

**Section**: 2.8.3
**Description**: Non-resolving answer → keep question active

#### Rule: DowndateQUD
**Pre**: `top(shared.qud)` is resolved but still on stack
**Effect**: `pop(shared.qud)`
**Section**: 2.8.4
**Description**: Remove resolved questions from QUD

#### Rule: IntegrateGreet
**Pre**: `shared.lu.type == greet`
**Effect**:
- Load initial plan into `private.plan`
- Clear `shared.lu`

**Section**: 2.8.5

#### Rule: IntegrateQuit
**Pre**: `shared.lu.type == quit`
**Effect**: `programState := stop`
**Section**: 2.8.5

#### Rule: FindPlan
**Pre**:
- `isEmpty(private.plan)`
- User has expressed task request

**Effect**:
- `plan := domain.getPlan(taskType)`
- `append(private.plan, plan)`

**Section**: 2.8.6
**Description**: Form task plan in response to user request

#### Rule: ExecFindout
**Pre**:
- `head(private.plan).type == findout`
- `head(private.plan).content == Q`

**Effect**:
- `push(private.issues, Q)` OR `push(shared.qud, Q)`
- `pop(private.plan)`

**Section**: 2.8.6
**Description**: Execute findout action from plan

#### Rule: ExecRaise
**Pre**:
- `head(private.plan).type == raise`
- `head(private.plan).content == Q`

**Effect**:
- `push(shared.qud, Q)`
- `pop(private.plan)`

**Section**: 2.8.6
**Description**: Explicitly raise question to QUD

#### Rule: ExecBind
**Pre**:
- `head(private.plan).type == bind`
- `head(private.plan).variable == V`
- Database query result available

**Effect**:
- Bind V to query result
- `pop(private.plan)`

**Section**: 2.8.6

---

### IBiS2 Additional Update Rules (Chapter 3, Section 3.6)

**Note**: IBiS2 extends IBiS1 with 27 named grounding rules (3.1-3.27). Key rules:

#### Rule 3.1: IntegrateICM_Perception
**Pre**: `shared.lu.type == icm:per*pos`
**Effect**: Mark utterance as perceived
**Description**: Positive perception feedback

#### Rule 3.2: IntegrateICM_Understanding
**Pre**: `shared.lu.type == icm:und*pos`
**Effect**: Mark utterance as understood
**Description**: Positive understanding feedback

#### Rule 3.6: RequestPerceptionFeedback
**Pre**: System utterance needs grounding
**Effect**: Add `icm:per*?` to `shared.next_moves`
**Description**: Request "did you hear me?"

#### Rule 3.15: ReraiseIssue
**Pre**:
- Grounding failed
- Question Q needs re-asking

**Effect**:
- `push(shared.qud, Q)`
- Reformulate question

**Section**: 3.6.9
**Description**: Re-raise question after communication failure

---

### IBiS3 Additional Update Rules (Chapter 4, Section 4.7)

#### Rule 4.1: IssueAccommodation (from Plan)
**Pre**:
- `head(private.plan).type == findout(Q)`
- Q not in shared.qud

**Effect**:
- `push(private.issues, Q)`
- `pop(private.plan)`

**Section**: 4.6.1
**Description**: Accommodate question from plan into private issues

#### Rule 4.2: LocalQuestionAccommodation
**Pre**:
- `head(private.issues) == Q`
- Conditions appropriate for raising Q

**Effect**:
- `pop(private.issues)`
- `push(shared.qud, Q)`

**Section**: 4.6.2
**Description**: Move question from issues to QUD (explicit raising)

#### Rule 4.3: IssueClarification
**Pre**:
- User utterance unclear
- Clarification question CQ needed

**Effect**:
- `push(shared.qud, CQ)`
- Suspend original question

**Section**: 4.6.3
**Description**: Ask clarification question

#### Rule 4.4: DependentIssueAccommodation
**Pre**:
- `top(shared.qud) == Q1`
- `depends(Q1, Q2)`
- Q2 not answered

**Effect**:
- `push(shared.qud, Q2)`
- Keep Q1 below Q2 on stack

**Section**: 4.6.4
**Description**: Accommodate dependent question from domain knowledge

#### Rule 4.5: QuestionReaccommodation
**Pre**:
- Question Q previously asked
- Answer was non-resolving
- Q needs re-asking

**Effect**:
- `push(shared.qud, Q)`

**Section**: 4.6.6
**Description**: Re-accommodate question after non-resolving answer

---

### IBiS4 Additional Update Rules (Chapter 5, Section 5.6)

#### Rule 5.1: IntegrateRequest
**Pre**:
- `shared.lu.type == request`
- `shared.lu.content == action(A)`

**Effect**:
- `add(private.actions, A)`
- Clear `shared.lu`

**Section**: 5.6.1
**Description**: User requests action

#### Rule 5.2: RejectRequest
**Pre**:
- `shared.lu.type == request`
- `shared.lu.content == action(A)`
- Action A not feasible

**Effect**:
- Add rejection move to `shared.next_moves`
- Clear `shared.lu`

**Section**: 5.6.1
**Description**: Reject infeasible action request

#### Rule 5.3: ExecuteAction
**Pre**: `head(private.actions) == A`
**Effect**:
- Execute A on device
- `pop(private.actions)`
- Add `postcond(A)` to `shared.com`

**Section**: 5.6.2
**Description**: Execute device action and update common ground

#### Rule 5.4: ActionAccommodation
**Pre**:
- User mentions action A implicitly
- A not in private.actions

**Effect**:
- `add(private.actions, A)`

**Section**: 5.6.5
**Description**: Accommodate implicit action request

#### Rule 5.5: IntroduceAlternative
**Pre**:
- Proposition P under discussion
- Alternative P' available

**Effect**:
- `add(private.iun, P')`

**Section**: 5.7.3
**Description**: Introduce alternative for negotiation

---

## Selection Rules by System

### IBiS1 Selection Rules (Chapter 2, Section 2.9)

#### Rule: SelectFromPlan
**Pre**: `head(private.plan)` is a communicative action
**Effect**: `add(shared.next_moves, head(private.plan))`
**Section**: 2.9.1
**Description**: Select action from plan

#### Rule: SelectAsk
**Pre**: `top(shared.qud) == Q` AND system needs to ask Q
**Effect**: `add(shared.next_moves, ask(Q))`
**Section**: 2.9.2
**Description**: Select ask move for top QUD question

#### Rule: SelectAnswer
**Pre**:
- `top(shared.qud) == Q`
- System can answer Q
- `answer := findAnswer(Q)`

**Effect**: `add(shared.next_moves, answer(answer))`
**Section**: 2.9.4
**Description**: Select answer move to top QUD question

#### Rule: SelectGreet
**Pre**: Dialogue start, no greeting yet
**Effect**: `add(shared.next_moves, greet())`
**Section**: 2.9 (implicit)

---

### IBiS2 Additional Selection Rules (Chapter 3, Section 3.7.2)

#### Rule: SelectRequestFeedback
**Pre**: System utterance needs grounding verification
**Effect**: `add(shared.next_moves, icm:per*?)`
**Section**: 3.7.2

#### Rule: SelectConfirm
**Pre**: System needs to confirm understanding of user utterance
**Effect**: `add(shared.next_moves, icm:und*int:USR*NUM)`
**Section**: 3.7.2

---

### IBiS3 Additional Selection Rules (Chapter 4, Section 4.7.3)

#### Rule: SelectClarificationQuestion
**Pre**:
- Utterance ambiguous or unclear
- Clarification question CQ formulated

**Effect**: `add(shared.next_moves, ask(CQ))`
**Section**: 4.7.3

---

### IBiS4 Additional Selection Rules (Chapter 5, Section 5.6.3)

#### Rule: SelectConfirmAction
**Pre**: Action A about to be executed
**Effect**: `add(shared.next_moves, confirm(action(A)))`
**Section**: 5.6.3

#### Rule: SelectProposeAlternative
**Pre**: Alternative proposition P' in IUN
**Effect**: `add(shared.next_moves, propose(P'))`
**Section**: 5.7.3

---

## Implementation Checklists

### IBiS1 Implementation Checklist

**Information State**:
- [ ] Define `InformationState` with `private` and `shared` fields
- [ ] Implement `private.plan` as list of Plan objects
- [ ] Implement `shared.qud` as stack (LIFO) of Questions
- [ ] Implement `shared.com` as set of Propositions
- [ ] Implement `shared.lu` for latest move

**Semantic Operations**:
- [ ] Implement `resolves(answer, question)` logic
- [ ] Implement `combines(question, answer)` logic
- [ ] Define domain-specific sorts and predicates

**Update Rules**:
- [ ] GetLatestUtterance
- [ ] IntegrateAsk
- [ ] IntegrateAnswer (resolving)
- [ ] IntegrateAnswer (non-resolving)
- [ ] DowndateQUD
- [ ] IntegrateGreet / IntegrateQuit
- [ ] FindPlan (task plan formation)
- [ ] ExecFindout, ExecRaise, ExecBind

**Selection Rules**:
- [ ] SelectFromPlan
- [ ] SelectAsk (from QUD top)
- [ ] SelectAnswer (to QUD top)
- [ ] SelectGreet

**Control Flow**:
- [ ] Implement main control loop (Algorithm 2.2)
- [ ] Single-rule-per-cycle execution
- [ ] First-applicable-rule selection
- [ ] Separate update/select modules

### IBiS2 Implementation Checklist (Grounding)

**Additional State Fields**:
- [ ] `shared.moves` - move history
- [ ] `shared.next_moves` - pending system moves

**Additional Rules**:
- [ ] IntegrateICM_Perception (Rule 3.1)
- [ ] IntegrateICM_Understanding (Rule 3.2)
- [ ] RequestPerceptionFeedback (Rule 3.6)
- [ ] ReraiseIssue (Rule 3.15)
- [ ] SelectRequestFeedback
- [ ] SelectConfirm

**Grounding Strategy**:
- [ ] Define evidence requirements per utterance type
- [ ] Implement grounding status tracking
- [ ] Implement feedback move generation

### IBiS3 Implementation Checklist (Accommodation)

**Additional State Fields**:
- [ ] `private.issues` - accommodated questions

**Additional Rules**:
- [ ] IssueAccommodation (Rule 4.1)
- [ ] LocalQuestionAccommodation (Rule 4.2)
- [ ] IssueClarification (Rule 4.3)
- [ ] DependentIssueAccommodation (Rule 4.4)
- [ ] QuestionReaccommodation (Rule 4.5)
- [ ] SelectClarificationQuestion

**Domain Model**:
- [ ] Implement `depends(Q1, Q2)` relation
- [ ] Define dependency graph or plan structure

### IBiS4 Implementation Checklist (Actions)

**Additional State Fields**:
- [ ] `private.actions` - pending device actions
- [ ] `private.iun` - issues under negotiation

**Additional Rules**:
- [ ] IntegrateRequest (Rule 5.1)
- [ ] RejectRequest (Rule 5.2)
- [ ] ExecuteAction (Rule 5.3)
- [ ] ActionAccommodation (Rule 5.4)
- [ ] IntroduceAlternative (Rule 5.5)
- [ ] SelectConfirmAction
- [ ] SelectProposeAlternative

**Device Integration**:
- [ ] Define device interface
- [ ] Implement `postcond(action)` function
- [ ] Connect menu structures to plans

---

## Cross-System Evolution Summary

| Feature | IBiS1 | IBiS2 | IBiS3 | IBiS4 |
|---------|-------|-------|-------|-------|
| Basic QUD | ✓ | ✓ | ✓ | ✓ |
| Plans | ✓ | ✓ | ✓ | ✓ |
| Grounding | - | ✓ | ✓ | ✓ |
| Accommodation | - | - | ✓ | ✓ |
| Actions | - | - | - | ✓ |
| Negotiation | - | - | - | ✓ |
| Issues field | - | - | ✓ | ✓ |
| IUN field | - | - | - | ✓ |

**Backward Compatibility**: Each system extends the previous without breaking changes.

---

## Key Design Principles (Extracted)

### 1. Single Rule Application Per Cycle
"The update algorithm applies rules one at a time, selecting the first applicable rule" (Section 2.8.7)

### 2. Explicit State, No Hidden Mutations
"All dialogue state is visible in the Information State" (Section 2.7.1)

### 3. Domain Independence via Resources
"Rules are domain-independent; domain knowledge in separate resources" (Section 2.3.1)

### 4. Questions as First-Class Objects
"Questions are irreducible objects, not reduced to knowledge preconditions" (Section 2.12.7)

### 5. QUD as Stack (LIFO)
"QUD is a stack with top element being maximal question" (Section 2.2.3)

### 6. Plan-Based + Reactive Selection
"Selection combines plan-based actions with reactive responses" (Section 2.9)

### 7. Task Plan Formation in Integration
"Plan formation happens in integration phase, not interpretation" (Section 2.8.6)

### 8. Accommodation Before Raising
"Questions enter private.issues, then move to shared.qud" (Section 4.6.1-4.6.2)

### 9. Grounding as Explicit Feedback
"Grounding tracked via ICM moves in move history" (Section 3.6)

### 10. Separation of Update/Select
"Update and Select are distinct modules with distinct rule sets" (Section 2.3.1)

---

## Section References for Deep Dive

- **IBiS1 Core**: Chapter 2, Sections 2.8-2.9
- **IBiS2 Grounding**: Chapter 3, Sections 3.6-3.7
- **IBiS3 Accommodation**: Chapter 4, Sections 4.6-4.7
- **IBiS4 Actions**: Chapter 5, Sections 5.6-5.7
- **Information States**: Figures 2.2, 3.1, 4.1, 5.1
- **Semantic Operations**: Chapter 2, Section 2.4
- **Control Algorithm**: Chapter 2, Section 2.3.1, Algorithm 2.2

---

*This document is the authoritative algorithmic reference for IBDM implementation. All rule names, structures, and algorithms are extracted directly from Larsson (2002).*
