#!/usr/bin/env python3
"""Create beads tasks for the accommodation refactoring plan."""

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
    id="ibdm-accom",
    title="Refactor: Move Task Accommodation from Interpretation to Integration Phase",
    description="""
Architectural refactoring to align implementation with Larsson's IBDM framework.

Current problem:
- Task accommodation (plan creation) is in INTERPRETATION phase
- Should be in INTEGRATION phase per Larsson (2002)
- NLU engine bypasses interpretation rules, making accommodation unreachable

Goal:
- Move accommodation logic to integration rules
- Enable both rule-based and NLU interpretation to trigger accommodation
- Improve conversational behavior in NDA demo

See: docs/REFACTORING_PLAN_accommodation.md
""".strip(),
    issue_type="epic",
    priority=0,
    labels=["architecture", "refactoring", "accommodation"],
)

# Phase 1: Refactor Interpretation Rules
phase1 = create_issue(
    id="ibdm-accom.1",
    title="Phase 1: Refactor interpretation rules (remove accommodation)",
    description="""
Make interpretation lightweight and syntactic-only.

Steps:
1. Add simple request detection rule with keyword matching
2. Deprecate NDA accommodation rule (lower priority to 0)
3. Update tests for new interpretation behavior

Deliverable: Request detection works, creates moves, no plans yet

See: docs/REFACTORING_PLAN_accommodation.md (Phase 1)
""".strip(),
    priority=0,
    labels=["architecture", "refactoring", "interpretation", "phase-1"],
)

# Phase 1 subtasks
phase1_tasks = [
    create_issue(
        id="ibdm-accom.1.1",
        title="Add simple request detection rule with keyword matching",
        description="""
Add interpret_request rule to interpretation_rules.py:
- Precondition: _is_request() checks keywords: "need", "want", "draft", "create"
- Effect: _create_request_move() creates basic request move
- Priority: 11 (high, but below greetings)
- No LLM calls, no plan creation

Test: Request utterances create request moves without plans
""".strip(),
        priority=0,
        labels=["interpretation", "phase-1"],
    ),
    create_issue(
        id="ibdm-accom.1.2",
        title="Deprecate NDA accommodation rule in interpretation",
        description="""
Deprecate accommodate_nda_task rule:
- Rename to accommodate_nda_task_DEPRECATED
- Lower priority to 0 (effectively disabled)
- Add deprecation comment
- Keep code for reference during migration

Test: Verify rule doesn't execute (priority 0)
""".strip(),
        priority=1,
        labels=["interpretation", "phase-1"],
    ),
    create_issue(
        id="ibdm-accom.1.3",
        title="Update interpretation tests for new behavior",
        description="""
Update tests in tests/unit/test_interpretation_rules.py:
- Add test_interpret_request
- Update tests expecting plan creation
- Verify request moves created without plans

Run: pytest tests/unit/test_interpretation_rules.py -v
""".strip(),
        priority=1,
        labels=["testing", "phase-1"],
    ),
]

# Phase 2: Add Accommodation to Integration
phase2 = create_issue(
    id="ibdm-accom.2",
    title="Phase 2: Add accommodation to integration rules",
    description="""
Implement task accommodation in the correct phase (integration).

Steps:
1. Add accommodate_request integration rule
2. Implement task classification in integration
3. Move NDA accommodation logic from interpretation
4. Handle both request and command move types
5. Update integration for request moves

Deliverable: Request moves trigger plan creation in integration phase

See: docs/REFACTORING_PLAN_accommodation.md (Phase 2)
""".strip(),
    priority=0,
    labels=["architecture", "refactoring", "integration", "phase-2"],
)

# Phase 2 subtasks
phase2_tasks = [
    create_issue(
        id="ibdm-accom.2.1",
        title="Add accommodate_request integration rule infrastructure",
        description="""
Add to integration_rules.py:
- accommodate_request rule
- Precondition: _is_request_move() or _is_command_move()
- Effect: _accommodate_request_task() (stub for now)
- Priority: 13 (highest - before other integrations)

Test: Rule is registered and triggers for request moves
""".strip(),
        priority=0,
        labels=["integration", "phase-2"],
    ),
    create_issue(
        id="ibdm-accom.2.2",
        title="Implement task classification in integration",
        description="""
Implement _accommodate_request_task():
- Import task classifier
- Classify utterance content
- Dispatch to task-specific handlers
- Add caching to avoid re-classification

Test: Task classification works for NDA requests
""".strip(),
        priority=0,
        labels=["integration", "phase-2"],
    ),
    create_issue(
        id="ibdm-accom.2.3",
        title="Move NDA accommodation logic to integration",
        description="""
Copy and adapt _create_nda_plan() from interpretation_rules.py:
- Rename to _accommodate_nda_task()
- Update to work with request move instead of utterance
- Add plan to state.private.plan
- Push first question to state.shared.qud

Test: NDA plan created correctly in integration phase
""".strip(),
        priority=0,
        labels=["integration", "phase-2", "nda"],
    ),
    create_issue(
        id="ibdm-accom.2.4",
        title="Handle both request and command move types",
        description="""
Ensure both move types trigger accommodation:
- Update preconditions to check for both
- Unified logic path for NLU (command) and rules (request)

Test: Both request and command moves create plans
""".strip(),
        priority=1,
        labels=["integration", "phase-2"],
    ),
    create_issue(
        id="ibdm-accom.2.5",
        title="Update existing integrate_request for new flow",
        description="""
Modify _integrate_request():
- Check if plan already created by accommodation
- Set next_speaker appropriately
- Track move in history

Test: Integration works with accommodated plans
""".strip(),
        priority=1,
        labels=["integration", "phase-2"],
    ),
    create_issue(
        id="ibdm-accom.2.6",
        title="Add integration tests for accommodation workflow",
        description="""
Create tests/unit/test_integration_rules.py tests:
- test_accommodate_request
- test_accommodate_nda
- test_nda_plan_creation
- test_qud_pushed_after_accommodation

Run: pytest tests/unit/test_integration_rules.py -v
""".strip(),
        priority=1,
        labels=["testing", "phase-2"],
    ),
]

# Phase 3: Clean Up
phase3 = create_issue(
    id="ibdm-accom.3",
    title="Phase 3: Remove deprecated accommodation code from interpretation",
    description="""
Clean up old accommodation code after migration complete.

Steps:
1. Remove deprecated NDA accommodation rule
2. Remove task classifier from interpretation
3. Update documentation

Deliverable: Clean codebase with clear separation of concerns

See: docs/REFACTORING_PLAN_accommodation.md (Phase 3)
""".strip(),
    priority=1,
    labels=["architecture", "refactoring", "cleanup", "phase-3"],
)

# Phase 3 subtasks
phase3_tasks = [
    create_issue(
        id="ibdm-accom.3.1",
        title="Remove deprecated NDA accommodation from interpretation_rules.py",
        description="""
Delete deprecated code:
- accommodate_nda_task_DEPRECATED rule
- _is_nda_request() function
- _create_nda_plan() function

Verify: pytest tests/unit/test_interpretation_rules.py -v
""".strip(),
        priority=1,
        labels=["cleanup", "phase-3"],
    ),
    create_issue(
        id="ibdm-accom.3.2",
        title="Remove task classifier from interpretation",
        description="""
Remove from interpretation_rules.py:
- _task_classifier global
- _get_task_classifier() function
- Task classifier imports

Verify: No unused imports, code compiles
""".strip(),
        priority=1,
        labels=["cleanup", "phase-3"],
    ),
    create_issue(
        id="ibdm-accom.3.3",
        title="Update interpretation docstrings for syntactic-only",
        description="""
Update documentation:
- Docstrings reflect interpretation is syntactic only
- Add references to integration rules for accommodation
- Update module-level docs

Verify: Documentation is accurate
""".strip(),
        priority=2,
        labels=["documentation", "phase-3"],
    ),
]

# Phase 4: Enhance NLG
phase4 = create_issue(
    id="ibdm-accom.4",
    title="Phase 4: Enhance NLG with plan context",
    description="""
Generate context-aware responses based on active plans.

Steps:
1. Add plan-aware question generation
2. Implement NDA question templates
3. Add plan progress feedback
4. Fallback to generic generation

Deliverable: Natural, context-aware dialogue for NDA workflow

See: docs/REFACTORING_PLAN_accommodation.md (Phase 4)
""".strip(),
    priority=1,
    labels=["nlg", "generation", "phase-4"],
)

# Phase 4 subtasks
phase4_tasks = [
    create_issue(
        id="ibdm-accom.4.1",
        title="Add plan-aware question generation helper",
        description="""
Update generation_rules.py:
- Add _get_active_plan(state) helper
- Update _generate_question_text() to check for active plans
- Add logic to select templates based on plan type

Test: Plan-aware generation triggers when plan exists
""".strip(),
        priority=1,
        labels=["nlg", "phase-4"],
    ),
    create_issue(
        id="ibdm-accom.4.2",
        title="Implement NDA-specific question templates",
        description="""
Add templates for each NDA question:
- Parties: "Let's start with the parties..."
- NDA type: "Will this be mutual or one-way?"
- Effective date: "What effective date..."
- Duration: "How long should obligations last?"
- Governing law: "California or Delaware?"

Test: Each question generates appropriate template
""".strip(),
        priority=1,
        labels=["nlg", "nda", "phase-4"],
    ),
    create_issue(
        id="ibdm-accom.4.3",
        title="Add plan progress feedback in responses",
        description="""
Add progress indicators:
- "Great! That's 2 of 5 requirements."
- "I have all the information needed. Generate NDA?"

Test: Progress shown correctly at each step
""".strip(),
        priority=2,
        labels=["nlg", "phase-4"],
    ),
    create_issue(
        id="ibdm-accom.4.4",
        title="Add fallback to generic generation",
        description="""
Ensure backward compatibility:
- If no active plan, use generic templates
- Maintain existing behavior for non-plan scenarios

Test: Generic generation still works
""".strip(),
        priority=2,
        labels=["nlg", "phase-4"],
    ),
]

# Phase 5: NLU Integration
phase5 = create_issue(
    id="ibdm-accom.5",
    title="Phase 5: Verify NLU engine integration",
    description="""
Ensure NLU engine works seamlessly with new accommodation.

Steps:
1. Verify NLU creates appropriate move types
2. Test integration path (NLU → integrate → accommodate)
3. Add logging for debugging

Deliverable: NLU engine triggers accommodation correctly

See: docs/REFACTORING_PLAN_accommodation.md (Phase 5)
""".strip(),
    priority=1,
    labels=["nlu", "integration", "phase-5"],
)

# Phase 5 subtasks
phase5_tasks = [
    create_issue(
        id="ibdm-accom.5.1",
        title="Verify NLU engine creates correct move types",
        description="""
Check nlu_engine.py:
- NLU creates "command" or "request" moves for task requests
- Move content includes full utterance text
- Metadata populated with confidence scores

Test: NLU interpretation produces correct moves
""".strip(),
        priority=1,
        labels=["nlu", "phase-5"],
    ),
    create_issue(
        id="ibdm-accom.5.2",
        title="Test NLU → integration → accommodation path",
        description="""
Integration test:
- NLU interpret → creates move
- Base class integrate → applies accommodation rules
- Verify plan is created correctly

Test: pytest tests/integration/test_nlu_accommodation.py -v
""".strip(),
        priority=1,
        labels=["nlu", "testing", "phase-5"],
    ),
    create_issue(
        id="ibdm-accom.5.3",
        title="Add logging for accommodation debugging",
        description="""
Add logging:
- Log when NLU creates request/command moves
- Log when accommodation is triggered
- Log plan creation and QUD updates

Test: Run demo with logging, verify output
""".strip(),
        priority=2,
        labels=["nlu", "logging", "phase-5"],
    ),
]

# Phase 6: Integration Testing
phase6 = create_issue(
    id="ibdm-accom.6",
    title="Phase 6: End-to-end integration testing",
    description="""
Verify complete workflow end-to-end.

Steps:
1. Create comprehensive integration test
2. Test with both interpretation methods
3. Manual testing with interactive demo
4. Performance testing

Deliverable: Fully working NDA workflow with natural conversation

See: docs/REFACTORING_PLAN_accommodation.md (Phase 6)
""".strip(),
    priority=1,
    labels=["testing", "integration", "phase-6"],
)

# Phase 6 subtasks
phase6_tasks = [
    create_issue(
        id="ibdm-accom.6.1",
        title="Create comprehensive NDA workflow integration test",
        description="""
Create tests/integration/test_complete_nda_workflow.py:
- Test complete NDA workflow (all 5 questions)
- Verify plan execution
- Verify QUD management
- Verify final confirmation

Test: pytest tests/integration/test_complete_nda_workflow.py -v
""".strip(),
        priority=1,
        labels=["testing", "integration", "phase-6"],
    ),
    create_issue(
        id="ibdm-accom.6.2",
        title="Test with both rule-based and NLU interpretation",
        description="""
Verify identical behavior:
- Test rule-based interpretation → accommodation
- Test NLU interpretation → accommodation
- Compare results (should be identical)

Test: Both paths produce same plans and QUD state
""".strip(),
        priority=1,
        labels=["testing", "nlu", "phase-6"],
    ),
    create_issue(
        id="ibdm-accom.6.3",
        title="Manual testing with interactive demo",
        description="""
Run interactive demo with real LLM:
- python demos/03_nlu_integration_interactive.py
- Test various phrasings: "need NDA", "draft NDA", etc.
- Verify plan execution and question sequencing
- Verify natural conversation flow

Document: Results in test report
""".strip(),
        priority=1,
        labels=["testing", "demo", "phase-6"],
    ),
    create_issue(
        id="ibdm-accom.6.4",
        title="Performance testing and benchmarking",
        description="""
Measure performance:
- Latency with accommodation in integration
- Compare to baseline (if available)
- Ensure no significant regression

Document: Performance metrics
""".strip(),
        priority=2,
        labels=["testing", "performance", "phase-6"],
    ),
]

# Phase 7: Documentation
phase7 = create_issue(
    id="ibdm-accom.7",
    title="Phase 7: Update documentation",
    description="""
Update all documentation to reflect new architecture.

Steps:
1. Update architecture docs
2. Update code comments
3. Update CLAUDE.md policy
4. Update demo documentation

Deliverable: Complete, accurate documentation

See: docs/REFACTORING_PLAN_accommodation.md (Phase 7)
""".strip(),
    priority=2,
    labels=["documentation", "phase-7"],
)

# Phase 7 subtasks
phase7_tasks = [
    create_issue(
        id="ibdm-accom.7.1",
        title="Update architecture documentation",
        description="""
Update docs:
- docs/burr_state_refactoring.md
- ARCHITECTURE_ISSUE_SUMMARY.md (mark resolved)
- Add resolution notes with date

Verify: Documentation is accurate
""".strip(),
        priority=2,
        labels=["documentation", "phase-7"],
    ),
    create_issue(
        id="ibdm-accom.7.2",
        title="Update code comments and docstrings",
        description="""
Update code:
- Add comments explaining accommodation in integration
- Reference Larsson (2002) in docstrings
- Add examples in docstrings

Verify: Code is well-documented
""".strip(),
        priority=2,
        labels=["documentation", "phase-7"],
    ),
    create_issue(
        id="ibdm-accom.7.3",
        title="Update CLAUDE.md with architectural principle",
        description="""
Add to CLAUDE.md:
- Principle: "Interpretation is syntactic, Integration is semantic"
- Document accommodation belongs in integration
- Reference this refactoring as example

Verify: Policy is clear
""".strip(),
        priority=2,
        labels=["documentation", "policy", "phase-7"],
    ),
    create_issue(
        id="ibdm-accom.7.4",
        title="Update demo documentation",
        description="""
Update demos/README.md:
- New behavior description
- Example conversation showing plan-driven dialogue
- Document architectural improvement

Verify: Demo docs are accurate
""".strip(),
        priority=2,
        labels=["documentation", "demo", "phase-7"],
    ),
]

# Collect all issues
all_issues = [
    epic,
    phase1,
    *phase1_tasks,
    phase2,
    *phase2_tasks,
    phase3,
    *phase3_tasks,
    phase4,
    *phase4_tasks,
    phase5,
    *phase5_tasks,
    phase6,
    *phase6_tasks,
    phase7,
    *phase7_tasks,
]

# Print as JSONL
for issue in all_issues:
    print(json.dumps(issue))
