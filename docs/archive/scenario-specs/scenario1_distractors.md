# Scenario 1: Incremental Questioning - Complete Distractor Map

**Date**: 2025-11-17
**Status**: ✅ COMPLETE
**Scenario**: Incremental Questioning (NDA Drafting)

This document details all dialogue options available at each turn in Scenario 1.

---

## Scenario Overview

**Name**: Incremental Questioning
**Domain**: NDA (Non-Disclosure Agreement)
**Features**: Rule 4.1 (IssueAccommodation), Rule 4.2 (LocalQuestionAccommodation)

**Goal**: Demonstrate how IBDM asks questions one at a time from a task plan, rather than overwhelming the user with all questions at once.

**Expected Flow**:
1. User requests NDA drafting
2. System asks for parties
3. User provides parties
4. System asks for effective date
5. User provides effective date
6. System asks for term
7. ... (continues through all plan questions)

---

## Turn 1: Initial Request

**Context**: Dialogue start, user initiates task
**System State**: Empty (no plan, no QUD, no commitments)

### Option 1: [Expected] ✓
**Utterance**: "I need to draft an NDA"
**Category**: Expected
**Description**: User initiates NDA drafting task

**What Happens**:
- System forms task plan with 4 questions
- Accommodates all questions to `private.issues`
- Raises first question (parties) to QUD
- System asks: "What are the parties to the NDA?"

**State Changes**:
```diff
Private:
+ plan: [nda_plan with 4 actions]
+ issues: [Q_effective_date, Q_term, Q_governing_law] (3 questions)

Shared:
+ qud: [Q_parties] (1 question)
  commitments: (empty)
```

---

### Option 2: [Distractor] - Vague Request
**Utterance**: "I need some kind of agreement"
**Category**: Clarification Request
**Description**: Vague request → System asks for clarification about document type

**What Happens**:
- System cannot determine specific task from vague request
- Generates clarification question
- Asks: "What type of agreement? (e.g., NDA, contract, MOU)"
- User must provide more specific information

**State Changes**:
```diff
Private:
+ issues: [Q_agreement_type] (clarification needed)

Shared:
+ qud: [Q_agreement_type]
  commitments: (empty)
```

**Educational Value**: Shows how system handles ambiguous requests

---

### Option 3: [Distractor] - Request with Volunteer Info
**Utterance**: "I need to draft an NDA between Acme Corp and Smith Inc"
**Category**: Volunteer Info
**Description**: Request with volunteer parties → System extracts and accommodates volunteered info

**What Happens**:
- System forms NDA plan
- Extracts volunteer info: "parties(Acme Corp, Smith Inc)"
- Accommodates questions to issues BUT removes Q_parties (already answered)
- Adds commitment for parties
- Raises SECOND question (effective_date) to QUD instead

**State Changes**:
```diff
Private:
+ plan: [nda_plan with 4 actions]
+ issues: [Q_term, Q_governing_law] (2 questions - parties skipped!)

Shared:
+ qud: [Q_effective_date] (skipped parties question)
+ commitments: {parties(Acme Corp, Smith Inc)}
```

**Educational Value**: Demonstrates volunteer information handling, question skipping

---

### Option 4: [Distractor] - Different Task
**Utterance**: "I need to book a flight"
**Category**: Expected (but different domain)
**Description**: Different task → System switches to travel domain

**What Happens**:
- System recognizes travel task (not NDA)
- Forms DIFFERENT plan: flight booking
- Different questions: departure city, destination, dates, etc.
- Completely different dialogue trajectory

**State Changes**:
```diff
Private:
+ plan: [flight_booking_plan with different actions]
+ issues: [Q_depart_city, Q_dest_city, Q_depart_date, Q_return_date]
+ beliefs: {domain: TravelDomain}

Shared:
+ qud: [Q_depart_city]
  commitments: (empty)
```

**Educational Value**: Shows domain switching, different task plans

---

### Option 5: [Distractor] - Meta Question
**Utterance**: "What information do you need to draft an NDA?"
**Category**: Nested Question
**Description**: Meta question about process → System explains NDA requirements

**What Happens**:
- System pushes user's meta-question to QUD
- Provides explanation: "I need parties, effective date, term, and governing law"
- Pops meta-question
- Asks: "Would you like to proceed with drafting an NDA?"

**State Changes**:
```diff
Private:
  plan: (empty - not formed yet)

Shared:
+ qud: [Q_nda_requirements] (meta-question)
  commitments: (empty)

After answering meta-question:
qud: []
```

**Educational Value**: Shows system handling of process questions, delayed plan formation

---

## Turn 2: Answering Parties Question

**Context**: System asked "What are the parties to the NDA?"
**System State**:
- `private.plan`: NDA plan with 4 actions
- `private.issues`: [Q_effective_date, Q_term, Q_governing_law]
- `shared.qud`: [Q_parties]
- `shared.commitments`: (empty)

### Option 1: [Expected] ✓
**Utterance**: "Acme Corp and Smith Inc"
**Category**: Expected
**Description**: Valid parties answer

**What Happens**:
- System validates: 2 legal entities → True
- Pops Q_parties from QUD
- Adds commitment: "parties(Acme Corp, Smith Inc)"
- Raises next question (Q_effective_date) to QUD
- System asks: "What is the effective date?"

**State Changes**:
```diff
Private:
  plan: [nda_plan, action 1 marked complete]
- issues: [Q_effective_date, Q_term, Q_governing_law]
+ issues: [Q_term, Q_governing_law] (effective_date raised)

Shared:
- qud: [Q_parties]
+ qud: [Q_effective_date]
- commitments: (empty)
+ commitments: {parties(Acme Corp, Smith Inc)}
```

---

### Option 2: [Distractor] - Invalid Answer (Nonsensical)
**Utterance**: "blue"
**Category**: Invalid Answer
**Description**: Invalid answer → Domain validation fails, clarification generated

**What Happens**:
- System validates: `domain.resolves('blue', Q_parties)` → False
- Creates clarification question CQ
- Pushes CQ to QUD ABOVE Q_parties: [Q_parties, CQ]
- Q_parties suspended temporarily
- System asks: "Please provide valid party names (legal entities)"

**State Changes**:
```diff
Private:
  plan: [nda_plan]
  issues: [Q_effective_date, Q_term, Q_governing_law]
+ beliefs: {failed_answer: "blue"}

Shared:
- qud: [Q_parties]
+ qud: [Q_parties, CQ_parties] (clarification pushed on top)
  commitments: (empty)
```

**After User Provides Valid Answer**:
- Both CQ and Q_parties popped
- Commitment added
- Continue to next question

**Educational Value**: Shows Rule 4.3 (IssueClarification), QUD stack management

---

### Option 3: [Distractor] - Incomplete Answer
**Utterance**: "Acme Corp"
**Category**: Invalid Answer
**Description**: Incomplete answer (only one party) → Validation fails

**What Happens**:
- System validates: needs TWO parties, only one provided → False
- Generates clarification: "An NDA requires two parties. Who is the second party?"
- Similar to Option 2 but with different clarification text

**State Changes**:
```diff
Shared:
- qud: [Q_parties]
+ qud: [Q_parties, CQ_second_party]
```

**Educational Value**: Shows context-aware clarification (knows what's missing)

---

### Option 4: [Distractor] - Volunteer Effective Date
**Utterance**: "Acme Corp and Smith Inc, effective January 1, 2025"
**Category**: Volunteer Info
**Description**: Volunteer effective date → System processes both facts

**What Happens**:
- System integrates "parties" (answers current question on QUD)
- System detects "effective_date" volunteer info
- Checks `private.issues` → finds Q_effective_date
- Integrates volunteer answer
- Removes Q_effective_date from issues
- Pops Q_parties from QUD
- Raises NEXT question (Q_term) to QUD (skips effective_date!)

**State Changes**:
```diff
Private:
  plan: [nda_plan, actions 1+2 marked complete]
- issues: [Q_effective_date, Q_term, Q_governing_law]
+ issues: [Q_governing_law] (both parties and date answered)

Shared:
- qud: [Q_parties]
+ qud: [Q_term] (skipped effective_date question!)
- commitments: (empty)
+ commitments: {
+   parties(Acme Corp, Smith Inc),
+   effective_date(January 1, 2025)
+ }
```

**Educational Value**: Core IBiS3 capability - volunteer info processing, question skipping

---

### Option 5: [Distractor] - Clarification Question
**Utterance**: "What format should I use for the party names?"
**Category**: Nested Question
**Description**: User asks for format guidance → Nested question pushed to QUD

**What Happens**:
- System pushes user's question to QUD: [Q_parties, Q_format]
- Q_parties suspended (below Q_format on stack)
- System answers format question: "Use full legal names, e.g., Acme Corp and Smith Inc"
- Pops Q_format
- Returns to Q_parties: "What are the parties?"
- User must now provide actual answer

**State Changes**:
```diff
Shared:
- qud: [Q_parties]
+ qud: [Q_parties, Q_format] (user's question on top)

After answering format question:
qud: [Q_parties] (back to original)
```

**Educational Value**: Shows user-initiated nested questions, QUD stack LIFO operations

---

### Option 6: [Distractor] - Volunteer ALL Facts
**Utterance**: "Acme Corp and Smith Inc, effective January 1, 2025, 5 year term, governed by California law"
**Category**: Volunteer Info
**Description**: Volunteer ALL facts → System processes all, plan complete

**What Happens**:
- System extracts 4 facts from single utterance
- Integrates ALL facts:
  - parties (current question)
  - effective_date (from issues)
  - term (from issues)
  - governing_law (from issues)
- Removes ALL questions from issues (empty)
- Marks all plan actions complete
- QUD becomes empty
- System confirms: "I have all the information needed to draft the NDA"

**State Changes**:
```diff
Private:
  plan: [nda_plan, ALL 4 actions marked complete]
- issues: [Q_effective_date, Q_term, Q_governing_law]
+ issues: [] (all answered!)

Shared:
- qud: [Q_parties]
+ qud: [] (all questions answered!)
- commitments: (empty)
+ commitments: {
+   parties(Acme Corp, Smith Inc),
+   effective_date(January 1, 2025),
+   term(5 years),
+   governing_law(California)
+ }
```

**Educational Value**: Shows extreme volunteer info case, plan completion

---

## Turn 3: Answering Effective Date Question

**Context**: System asked "What is the effective date?"
**System State**:
- `private.plan`: NDA plan (action 1 complete)
- `private.issues`: [Q_term, Q_governing_law]
- `shared.qud`: [Q_effective_date]
- `shared.commitments`: {parties(Acme Corp, Smith Inc)}

### Option 1: [Expected] ✓
**Utterance**: "January 1, 2025"
**Category**: Expected
**Description**: Valid date answer

**What Happens**:
- System validates date format → True
- Pops Q_effective_date from QUD
- Adds commitment: "effective_date(January 1, 2025)"
- Raises next question (Q_term) to QUD
- System asks: "What is the term?"

**State Changes**:
```diff
Private:
  plan: [nda_plan, actions 1+2 complete]
- issues: [Q_term, Q_governing_law]
+ issues: [Q_governing_law]

Shared:
- qud: [Q_effective_date]
+ qud: [Q_term]
- commitments: {parties(...)}
+ commitments: {
+   parties(Acme Corp, Smith Inc),
+   effective_date(January 1, 2025)
+ }
```

---

### Option 2: [Distractor] - Invalid Date Format
**Utterance**: "yesterday"
**Category**: Invalid Answer
**Description**: Invalid date → System asks for proper date format

**What Happens**:
- System validates: "yesterday" not a valid date format → False
- Generates clarification: "Please provide a specific date (e.g., January 1, 2025)"
- Pushes CQ to QUD

**State Changes**:
```diff
Shared:
- qud: [Q_effective_date]
+ qud: [Q_effective_date, CQ_date_format]
```

**Educational Value**: Shows date validation, format guidance

---

### Option 3: [Distractor] - Correction of Previous Answer
**Utterance**: "Wait, I need to correct the parties. It should be XYZ Corp and Smith Inc"
**Category**: Correction
**Description**: User corrects previous answer → Belief revision (Rules 4.6-4.8)

**What Happens**:
- System detects correction of "parties" commitment
- Retracts old commitment: `parties(Acme Corp, Smith Inc)` removed
- Re-accommodates Q_parties to `private.issues`
- Integrates new answer: `parties(XYZ Corp, Smith Inc)`
- Checks dependent questions (none for parties in NDA domain)
- Returns to current question: "What is the effective date?"

**State Changes**:
```diff
Private:
  plan: [nda_plan]
+ issues: [Q_term, Q_governing_law] (Q_parties NOT re-added because corrected immediately)

Shared:
  qud: [Q_effective_date] (unchanged - returns here)
- commitments: {parties(Acme Corp, Smith Inc)}
+ commitments: {parties(XYZ Corp, Smith Inc)} (updated!)
```

**Educational Value**: Shows Rules 4.6-4.8 (QuestionReaccommodation, RetractIncompatibleCommitment), belief revision

---

### Option 4: [Distractor] - Meta Question About Revision
**Utterance**: "Can I change the parties I mentioned earlier?"
**Category**: Nested Question
**Description**: Meta-question about revision → System explains capability

**What Happens**:
- System pushes user's meta-question to QUD
- Answers: "Yes, you can correct any information. Just say so."
- Pops meta-question
- Returns to current question: "What is the effective date?"

**State Changes**:
```diff
Shared:
- qud: [Q_effective_date]
+ qud: [Q_effective_date, Q_can_revise]

After answering:
qud: [Q_effective_date]
```

**Educational Value**: Shows system explaining its own capabilities

---

### Option 5: [Distractor] - Volunteer Term
**Utterance**: "January 1, 2025, with a 5 year term"
**Category**: Volunteer Info
**Description**: Volunteer term duration → System processes both

**What Happens**:
- System integrates "effective_date" (current question)
- System integrates "term" (volunteer from issues)
- Removes Q_term from issues
- Raises Q_governing_law to QUD

**State Changes**:
```diff
Private:
  plan: [nda_plan, actions 1+2+3 complete]
- issues: [Q_term, Q_governing_law]
+ issues: [] (only governing_law remains, will be raised)

Shared:
- qud: [Q_effective_date]
+ qud: [Q_governing_law] (skipped term question)
+ commitments: {
+   parties(Acme Corp, Smith Inc),
+   effective_date(January 1, 2025),
+   term(5 years)
+ }
```

**Educational Value**: Shows continued volunteer info handling across multiple turns

---

### Option 6: [Distractor] - Task Cancellation
**Utterance**: "Actually, I don't want to draft an NDA anymore"
**Category**: Rejection
**Description**: User cancels task → System retracts plan and commitments

**What Happens**:
- System detects task cancellation
- Clears `private.plan` (empty)
- Clears `private.issues` (empty)
- Clears `shared.commitments` (empty)
- Clears `shared.qud` (empty)
- Returns to idle state
- System: "Okay. How can I help you?"

**State Changes**:
```diff
Private:
- plan: [nda_plan]
+ plan: []
- issues: [Q_term, Q_governing_law]
+ issues: []

Shared:
- qud: [Q_effective_date]
+ qud: []
- commitments: {parties(Acme Corp, Smith Inc)}
+ commitments: {}
```

**Educational Value**: Shows task abandonment, full state reset

---

### Option 7: [Distractor] - Question About Dependencies
**Utterance**: "Does the effective date affect the term length?"
**Category**: Nested Question
**Description**: Question about dependencies → System explains relationship

**What Happens**:
- System pushes user's question to QUD
- Explains: "The term is independent of effective date. Effective date is when NDA starts, term is how long it lasts."
- Pops explanation question
- Returns: "What is the effective date?"

**State Changes**:
```diff
Shared:
- qud: [Q_effective_date]
+ qud: [Q_effective_date, Q_date_term_dependency]

After explanation:
qud: [Q_effective_date]
```

**Educational Value**: Shows domain knowledge explanation, independence of predicates

---

## Summary Statistics

**Total Dialogue Options Across All Turns**: 18 options (5 + 6 + 7)

**Breakdown by Category**:
- Expected moves: 3 (one per turn)
- Invalid answers: 4 (validation/clarification triggers)
- Volunteer info: 5 (multi-fact extraction)
- Nested questions: 5 (user-initiated clarifications)
- Corrections: 1 (belief revision)
- Rejections: 1 (task cancellation)
- Clarification requests: 1 (vague input)
- Domain switches: 1 (different task)

**IBiS Rules Demonstrated**:
- ✅ Rule 4.1: IssueAccommodation (all turns)
- ✅ Rule 4.2: LocalQuestionAccommodation (all turns)
- ✅ Rule 4.3: IssueClarification (options 2.2, 2.3, 3.2)
- ✅ Rules 4.6-4.8: QuestionReaccommodation, belief revision (option 3.3)
- ✅ QUD Stack Management (all nested question options)
- ✅ Domain Validation (all invalid answer options)
- ✅ Volunteer Information Handling (options 1.3, 2.4, 2.6, 3.5)

**Educational Path Recommendations**:

1. **First-Time Users**: Follow expected path (options 1.1 → 2.1 → 3.1)
2. **Learning Volunteer Info**: Try 1.1 → 2.4 → observe question skipping
3. **Learning Clarification**: Try 1.1 → 2.2 → see Rule 4.3 in action
4. **Learning Belief Revision**: Try 1.1 → 2.1 → 3.3 → see correction handling
5. **Advanced**: Try 1.3 → volunteer all info → see complete plan execution

---

## Implementation Notes

These distractors are defined in:
- File: `src/ibdm/demo/scenario_distractors.py`
- Functions:
  - `get_scenario1_turn1_distractors()`
  - `get_scenario1_turn2_distractors()`
  - `get_scenario1_turn3_distractors()`

Used by `ScenarioExplorer` when `scenario.name == "Incremental Questioning"`.

---

**Last Updated**: 2025-11-17
**Maintained By**: IBDM Development Team
