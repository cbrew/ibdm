#!/usr/bin/env python3
"""Generate beads tasks for IBiS2 and IBiS4 implementation."""

import hashlib
import json
from datetime import datetime, timezone

def content_hash(text: str) -> str:
    """Generate SHA256 hash of text."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def now_iso() -> str:
    """Get current time in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

# Current timestamp for all tasks
timestamp = now_iso()

# IBiS2 Tasks
ibis2_tasks = []

# Epic: IBiS2 Implementation
ibis2_epic = {
    "id": "ibdm-98",
    "content_hash": content_hash("IBiS2 - Grounding & Interactive Communication Management"),
    "title": "IBiS2 - Grounding & Interactive Communication Management",
    "description": "Implement IBiS2 variant with grounding, ICM taxonomy, and 27 update rules from Larsson (2002) Chapter 3. Target: 60% → 100% completion (6-8 weeks)",
    "status": "open",
    "priority": 1,
    "issue_type": "epic",
    "created_at": timestamp,
    "updated_at": timestamp,
    "source_repo": ".",
    "labels": ["ibis2", "grounding", "icm", "larsson-ch3"]
}
ibis2_tasks.append(ibis2_epic)

# Week 1-2: Information State Extensions
tasks_week1_2 = [
    {
        "id": "ibdm-98.1",
        "title": "Add grounding fields to SharedIS",
        "description": "Update src/ibdm/core/information_state.py to add moves: list[Move] and next_moves: list[Move] fields for tracking complete move history with grounding status and pending system moves. Larsson Figure 3.1.",
        "priority": 1,
        "labels": ["ibis2", "week1-2", "information-state", "grounding"]
    },
    {
        "id": "ibdm-98.2",
        "title": "Create grounding status tracking module",
        "description": "Create src/ibdm/core/grounding.py with GroundingStatus enum (ungrounded, pending, grounded), evidence requirements per move type, and grounding strategy selection. Larsson Section 3.5.",
        "priority": 1,
        "labels": ["ibis2", "week1-2", "grounding", "core"]
    },
    {
        "id": "ibdm-98.3",
        "title": "Update serialization for grounding fields",
        "description": "Update to_dict/from_dict methods in information_state.py to handle new grounding fields (moves, next_moves). Add type safety and validation.",
        "priority": 1,
        "labels": ["ibis2", "week1-2", "serialization", "infrastructure"]
    },
]

# Week 3-5: ICM Taxonomy Implementation
tasks_week3_5 = [
    {
        "id": "ibdm-98.4",
        "title": "Implement ICM move types",
        "description": "Extend src/ibdm/core/moves.py to add ICM move types: icm:per*pos (positive perception), icm:per*neg (negative perception), icm:und*pos (positive understanding), icm:und*neg (negative understanding), icm:und*int:USR*NUM (understanding confirmation). Larsson Section 3.4.",
        "priority": 1,
        "labels": ["ibis2", "week3-5", "icm", "moves", "taxonomy"]
    },
    {
        "id": "ibdm-98.5",
        "title": "Implement ICM Rule 3.1: IntegratePerPos",
        "description": "Implement integration rule for positive perception ICM (user indicates they heard system). Add to integration_rules.py. Larsson Section 3.6.1.",
        "priority": 1,
        "labels": ["ibis2", "week3-5", "icm", "rules", "perception"]
    },
    {
        "id": "ibdm-98.6",
        "title": "Implement ICM Rule 3.5: IntegrateUndPos",
        "description": "Implement integration rule for positive understanding ICM (user indicates they understood system). Add to integration_rules.py. Larsson Section 3.6.5.",
        "priority": 1,
        "labels": ["ibis2", "week3-5", "icm", "rules", "understanding"]
    },
    {
        "id": "ibdm-98.7",
        "title": "Implement ICM Rule 3.15: Reraising",
        "description": "Implement reraising rule for grounding failure (push failed utterance back to QUD). Add to integration_rules.py. Larsson Section 3.6.15.",
        "priority": 1,
        "labels": ["ibis2", "week3-5", "icm", "rules", "reraising"]
    },
    {
        "id": "ibdm-98.8",
        "title": "Implement ICM Rule 3.20: Confirmation",
        "description": "Implement confirmation rule for low-confidence utterances. Add to selection_rules.py. Larsson Section 3.6.20.",
        "priority": 1,
        "labels": ["ibis2", "week3-5", "icm", "rules", "confirmation"]
    },
    {
        "id": "ibdm-98.9",
        "title": "Implement remaining 23 ICM update rules",
        "description": "Implement all remaining ICM update rules (3.2-3.4, 3.6-3.14, 3.16-3.19, 3.21-3.27) from Larsson Section 3.6. Each rule handles specific grounding situations.",
        "priority": 1,
        "labels": ["ibis2", "week3-5", "icm", "rules", "comprehensive"]
    },
]

# Week 6: Grounding Strategies
tasks_week6 = [
    {
        "id": "ibdm-98.10",
        "title": "Implement grounding strategy selection",
        "description": "Implement strategy-based grounding: Optimistic (confidence > 0.9), Cautious (confidence > 0.6), Pessimistic (confidence <= 0.6). Add to src/ibdm/core/grounding.py. Larsson Section 3.5.",
        "priority": 1,
        "labels": ["ibis2", "week6", "grounding", "strategies"]
    },
    {
        "id": "ibdm-98.11",
        "title": "Implement evidence requirements",
        "description": "Define evidence requirements per utterance type: Questions need understanding confirmation, Answers need acceptance/rejection, Commands need acknowledgment + execution confirmation. Larsson Section 3.3.",
        "priority": 1,
        "labels": ["ibis2", "week6", "grounding", "evidence"]
    },
]

# Week 7: Perception Checking
tasks_week7 = [
    {
        "id": "ibdm-98.12",
        "title": "Implement perception checking for low ASR confidence",
        "description": "Add perception checking: trigger icm:per*neg when ASR confidence < threshold. Generate 'Sorry, I didn\\'t hear that clearly' responses. Larsson Section 3.7.1.",
        "priority": 1,
        "labels": ["ibis2", "week7", "perception", "asr", "confidence"]
    },
    {
        "id": "ibdm-98.13",
        "title": "Implement spelling confirmation",
        "description": "Add spelling confirmation for critical entities (names, legal terms). Generate icm:und*int:USR*NUM moves. Larsson Section 3.7.2.",
        "priority": 1,
        "labels": ["ibis2", "week7", "understanding", "entities", "confirmation"]
    },
]

# Week 8: Integration & Testing
tasks_week8 = [
    {
        "id": "ibdm-98.14",
        "title": "Create ICM unit tests",
        "description": "Create unit tests for all 27 ICM rules. Verify correct preconditions, effects, and rule priorities. Target: 100% rule coverage.",
        "priority": 1,
        "labels": ["ibis2", "week8", "testing", "icm", "unit-tests"]
    },
    {
        "id": "ibdm-98.15",
        "title": "Create grounding integration tests",
        "description": "Create integration tests for complete grounding scenarios: low confidence detection, perception failure, understanding confirmation, reraising after failure.",
        "priority": 1,
        "labels": ["ibis2", "week8", "testing", "grounding", "integration-tests"]
    },
    {
        "id": "ibdm-98.16",
        "title": "Test grounding strategies end-to-end",
        "description": "Create end-to-end tests for all three grounding strategies (Optimistic, Cautious, Pessimistic) across multi-turn dialogues.",
        "priority": 1,
        "labels": ["ibis2", "week8", "testing", "strategies", "end-to-end"]
    },
    {
        "id": "ibdm-98.17",
        "title": "Update SYSTEM_ACHIEVEMENTS.md with IBiS2 completion",
        "description": "Document IBiS2 implementation: 27 ICM rules, grounding strategies, test coverage, and Larsson fidelity metrics.",
        "priority": 1,
        "labels": ["ibis2", "week8", "documentation", "achievements"]
    },
    {
        "id": "ibdm-98.18",
        "title": "Update LARSSON_PRIORITY_ROADMAP.md with IBiS2 progress",
        "description": "Update roadmap with IBiS2 completion status (60% → 100%). Document all implemented rules and strategies.",
        "priority": 1,
        "labels": ["ibis2", "week8", "documentation", "roadmap"]
    },
    {
        "id": "ibdm-98.19",
        "title": "Create IBiS2 implementation guide",
        "description": "Create comprehensive guide documenting IBiS2 architecture, all 27 ICM rules, grounding strategies, testing patterns, and common pitfalls.",
        "priority": 1,
        "labels": ["ibis2", "week8", "documentation", "guide"]
    },
    {
        "id": "ibdm-98.20",
        "title": "Measure IBiS2 Larsson fidelity",
        "description": "Run Larsson fidelity measurement for IBiS2 implementation. Target: 100% compliance with Chapter 3 algorithms. Generate report.",
        "priority": 1,
        "labels": ["ibis2", "week8", "metrics", "larsson", "fidelity"]
    },
]

# Add all week tasks to ibis2_tasks
for task_list in [tasks_week1_2, tasks_week3_5, tasks_week6, tasks_week7, tasks_week8]:
    for task in task_list:
        task_entry = {
            "id": task["id"],
            "content_hash": content_hash(task["title"] + task["description"]),
            "title": task["title"],
            "description": task["description"],
            "status": "open",
            "priority": task["priority"],
            "issue_type": "task",
            "created_at": timestamp,
            "updated_at": timestamp,
            "source_repo": ".",
            "labels": task["labels"]
        }
        ibis2_tasks.append(task_entry)

# IBiS4 Tasks
ibis4_tasks = []

# Epic: IBiS4 Implementation
ibis4_epic = {
    "id": "ibdm-99",
    "content_hash": content_hash("IBiS4 - Actions & Negotiative Dialogue"),
    "title": "IBiS4 - Actions & Negotiative Dialogue",
    "description": "Implement IBiS4 variant with action execution, device interfaces, and negotiation from Larsson (2002) Chapter 5. Target: 10% → 100% completion (8-10 weeks)",
    "status": "open",
    "priority": 2,
    "issue_type": "epic",
    "created_at": timestamp,
    "updated_at": timestamp,
    "source_repo": ".",
    "labels": ["ibis4", "actions", "negotiation", "larsson-ch5"]
}
ibis4_tasks.append(ibis4_epic)

# Week 1-2: Information State Extensions
ibis4_week1_2 = [
    {
        "id": "ibdm-99.1",
        "title": "Add action fields to PrivateIS",
        "description": "Update src/ibdm/core/information_state.py to add actions: list[Action] and iun: set[Proposition] fields for tracking pending device actions and Issues Under Negotiation. Larsson Figure 5.1.",
        "priority": 2,
        "labels": ["ibis4", "week1-2", "information-state", "actions"]
    },
    {
        "id": "ibdm-99.2",
        "title": "Create Action and Proposition classes",
        "description": "Create src/ibdm/core/actions.py with Action class (action_type, parameters, preconditions, postconditions), Proposition class (predicate, arguments, truth_value), and ActionStatus enum. Larsson Section 5.2.",
        "priority": 2,
        "labels": ["ibis4", "week1-2", "actions", "core", "data-structures"]
    },
    {
        "id": "ibdm-99.3",
        "title": "Update serialization for action fields",
        "description": "Update to_dict/from_dict methods to handle new action fields (actions, iun). Add type safety and validation for Action and Proposition objects.",
        "priority": 2,
        "labels": ["ibis4", "week1-2", "serialization", "infrastructure"]
    },
]

# Week 3-4: Device Interface & Actions
ibis4_week3_4 = [
    {
        "id": "ibdm-99.4",
        "title": "Define device interface protocol",
        "description": "Create src/ibdm/interfaces/device.py with DeviceInterface protocol: execute_action(), check_preconditions(), get_postconditions(). Larsson Section 5.4.1.",
        "priority": 2,
        "labels": ["ibis4", "week3-4", "device", "interface", "protocol"]
    },
    {
        "id": "ibdm-99.5",
        "title": "Implement postcond() function",
        "description": "Add postcond() function to src/ibdm/core/domain.py for getting action postconditions. Used by update rules to determine action effects. Larsson Section 5.3.",
        "priority": 2,
        "labels": ["ibis4", "week3-4", "domain", "actions", "postconditions"]
    },
    {
        "id": "ibdm-99.6",
        "title": "Implement action precondition checking",
        "description": "Add precondition validation to action execution. Check domain constraints before executing actions. Generate clarification if preconditions not met.",
        "priority": 2,
        "labels": ["ibis4", "week3-4", "actions", "preconditions", "validation"]
    },
    {
        "id": "ibdm-99.7",
        "title": "Create mock device for testing",
        "description": "Create tests/mocks/mock_device.py implementing DeviceInterface for testing without real hardware. Support common actions: send_email, create_document, book_travel.",
        "priority": 2,
        "labels": ["ibis4", "week3-4", "testing", "mocks", "device"]
    },
]

# Week 5-6: Negotiation
ibis4_week5_6 = [
    {
        "id": "ibdm-99.8",
        "title": "Implement Issues Under Negotiation (IUN)",
        "description": "Add IUN management: track propositions under negotiation, detect conflicts, manage negotiation state. Larsson Section 5.5.",
        "priority": 2,
        "labels": ["ibis4", "week5-6", "negotiation", "iun", "state-management"]
    },
    {
        "id": "ibdm-99.9",
        "title": "Implement negotiation accommodation rules",
        "description": "Add rules for accommodating proposals to IUN, detecting conflicts, and managing negotiation dialogue. Larsson Section 5.6.",
        "priority": 2,
        "labels": ["ibis4", "week5-6", "negotiation", "rules", "accommodation"]
    },
    {
        "id": "ibdm-99.10",
        "title": "Implement accept/reject negotiation moves",
        "description": "Add support for accept and reject moves in negotiation. Update integration rules to handle acceptance/rejection of proposals.",
        "priority": 2,
        "labels": ["ibis4", "week5-6", "negotiation", "moves", "accept-reject"]
    },
    {
        "id": "ibdm-99.11",
        "title": "Implement counter-proposal generation",
        "description": "Add selection rules for generating counter-proposals when user rejects system proposals. Use domain constraints to generate alternatives.",
        "priority": 2,
        "labels": ["ibis4", "week5-6", "negotiation", "counter-proposals", "generation"]
    },
]

# Week 7-8: Action Execution
ibis4_week7_8 = [
    {
        "id": "ibdm-99.12",
        "title": "Implement action execution integration rule",
        "description": "Add integration rule for executing actions when preconditions are met and user has confirmed. Update state with postconditions. Larsson Section 5.7.",
        "priority": 2,
        "labels": ["ibis4", "week7-8", "actions", "execution", "rules"]
    },
    {
        "id": "ibdm-99.13",
        "title": "Implement action confirmation selection rule",
        "description": "Add selection rule for requesting user confirmation before executing actions. Generate natural language descriptions of action effects.",
        "priority": 2,
        "labels": ["ibis4", "week7-8", "actions", "confirmation", "selection"]
    },
    {
        "id": "ibdm-99.14",
        "title": "Implement action result handling",
        "description": "Handle action execution results (success, failure, partial). Update commitments and beliefs based on postconditions. Handle failures gracefully.",
        "priority": 2,
        "labels": ["ibis4", "week7-8", "actions", "results", "error-handling"]
    },
    {
        "id": "ibdm-99.15",
        "title": "Implement action rollback on failure",
        "description": "Add rollback mechanism for failed actions. Restore previous state, remove failed action from plan, generate error explanation to user.",
        "priority": 2,
        "labels": ["ibis4", "week7-8", "actions", "rollback", "recovery"]
    },
]

# Week 9-10: Domain Integration & Testing
ibis4_week9_10 = [
    {
        "id": "ibdm-99.16",
        "title": "Add actions to NDA domain",
        "description": "Extend NDA domain with actions: generate_document, send_for_signature, store_document. Define preconditions and postconditions for each.",
        "priority": 2,
        "labels": ["ibis4", "week9-10", "domain", "nda", "actions"]
    },
    {
        "id": "ibdm-99.17",
        "title": "Add actions to travel domain",
        "description": "Extend travel domain with actions: book_ticket, reserve_hotel, send_itinerary. Define preconditions and postconditions for each. Larsson Chapter 5 examples.",
        "priority": 2,
        "labels": ["ibis4", "week9-10", "domain", "travel", "actions"]
    },
    {
        "id": "ibdm-99.18",
        "title": "Create action execution unit tests",
        "description": "Create unit tests for action execution, precondition checking, postcondition application, and error handling. Use MockDevice for testing.",
        "priority": 2,
        "labels": ["ibis4", "week9-10", "testing", "actions", "unit-tests"]
    },
    {
        "id": "ibdm-99.19",
        "title": "Create negotiation integration tests",
        "description": "Create integration tests for negotiation scenarios: proposal-acceptance, proposal-rejection with counter-proposal, multi-round negotiation.",
        "priority": 2,
        "labels": ["ibis4", "week9-10", "testing", "negotiation", "integration-tests"]
    },
    {
        "id": "ibdm-99.20",
        "title": "Create end-to-end action tests",
        "description": "Create end-to-end tests for complete action workflows: information gathering → action proposal → confirmation → execution → result handling.",
        "priority": 2,
        "labels": ["ibis4", "week9-10", "testing", "actions", "end-to-end"]
    },
    {
        "id": "ibdm-99.21",
        "title": "Update SYSTEM_ACHIEVEMENTS.md with IBiS4 completion",
        "description": "Document IBiS4 implementation: action execution, device interface, negotiation, test coverage, and Larsson fidelity metrics.",
        "priority": 2,
        "labels": ["ibis4", "week9-10", "documentation", "achievements"]
    },
    {
        "id": "ibdm-99.22",
        "title": "Update LARSSON_PRIORITY_ROADMAP.md with IBiS4 progress",
        "description": "Update roadmap with IBiS4 completion status (10% → 100%). Document all implemented features and capabilities.",
        "priority": 2,
        "labels": ["ibis4", "week9-10", "documentation", "roadmap"]
    },
    {
        "id": "ibdm-99.23",
        "title": "Create IBiS4 implementation guide",
        "description": "Create comprehensive guide documenting IBiS4 architecture, action system, negotiation, device interface, testing patterns, and examples.",
        "priority": 2,
        "labels": ["ibis4", "week9-10", "documentation", "guide"]
    },
    {
        "id": "ibdm-99.24",
        "title": "Measure IBiS4 Larsson fidelity",
        "description": "Run Larsson fidelity measurement for IBiS4 implementation. Target: 95%+ compliance with Chapter 5 algorithms. Generate report.",
        "priority": 2,
        "labels": ["ibis4", "week9-10", "metrics", "larsson", "fidelity"]
    },
    {
        "id": "ibdm-99.25",
        "title": "Create IBiS4 demo application",
        "description": "Create demo showing IBiS4 capabilities: multi-step action planning, negotiation, action execution with confirmation, error handling and recovery.",
        "priority": 2,
        "labels": ["ibis4", "week9-10", "demo", "showcase"]
    },
]

# Add all week tasks to ibis4_tasks
for task_list in [ibis4_week1_2, ibis4_week3_4, ibis4_week5_6, ibis4_week7_8, ibis4_week9_10]:
    for task in task_list:
        task_entry = {
            "id": task["id"],
            "content_hash": content_hash(task["title"] + task["description"]),
            "title": task["title"],
            "description": task["description"],
            "status": "open",
            "priority": task["priority"],
            "issue_type": "task",
            "created_at": timestamp,
            "updated_at": timestamp,
            "source_repo": ".",
            "labels": task["labels"]
        }
        ibis4_tasks.append(task_entry)

# Write all tasks to JSONL file
all_tasks = ibis2_tasks + ibis4_tasks

# Append to existing issues.jsonl
with open('/home/user/ibdm/.beads/issues.jsonl', 'a') as f:
    for task in all_tasks:
        f.write(json.dumps(task) + '\n')

print(f"Created {len(ibis2_tasks)} IBiS2 tasks (1 epic + {len(ibis2_tasks)-1} subtasks)")
print(f"Created {len(ibis4_tasks)} IBiS4 tasks (1 epic + {len(ibis4_tasks)-1} subtasks)")
print(f"Total: {len(all_tasks)} tasks added to .beads/issues.jsonl")
print()
print("IBiS2 Epic: ibdm-98")
print("IBiS2 Tasks: ibdm-98.1 through ibdm-98.20")
print()
print("IBiS4 Epic: ibdm-99")
print("IBiS4 Tasks: ibdm-99.1 through ibdm-99.25")
