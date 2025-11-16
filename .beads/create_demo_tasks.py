#!/usr/bin/env python3
"""Generate beads tasks for Interactive Demo Application."""

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

demo_tasks = []

# Epic: Interactive Demo Application
demo_epic = {
    "id": "ibdm-100",
    "content_hash": content_hash("Interactive Demo Application - Showcase IBDM with IBiS3 + IBiS2"),
    "title": "Interactive Demo Application - Showcase IBDM with IBiS3 + IBiS2",
    "description": "Create interactive CLI demo application showcasing complete IBDM system with IBiS3 question accommodation and IBiS2 grounding working together. Demonstrates incremental questioning, volunteer information, clarification, dependencies, belief revision, and confidence-based grounding.",
    "status": "open",
    "priority": 0,  # P0 - Highest priority
    "issue_type": "epic",
    "created_at": timestamp,
    "updated_at": timestamp,
    "source_repo": ".",
    "labels": ["demo", "ibis3", "ibis2", "showcase", "interactive"]
}
demo_tasks.append(demo_epic)

# Demo Application Tasks
demo_subtasks = [
    {
        "id": "ibdm-100.1",
        "title": "Create interactive CLI demo framework",
        "description": "Create src/ibdm/demo/interactive_demo.py with CLI framework for running interactive dialogues. Support: user input, system output, dialogue history display, session persistence, help commands. Use simple input/print (not Textual).",
        "priority": 0,
        "labels": ["demo", "cli", "framework", "interactive"]
    },
    {
        "id": "ibdm-100.2",
        "title": "Integrate NDA domain for demo",
        "description": "Configure demo to use NDA domain with complete question set (parties, effective_date, governing_law, confidential_info, term, return_materials). Show incremental questioning through all fields.",
        "priority": 0,
        "labels": ["demo", "nda", "domain", "integration"]
    },
    {
        "id": "ibdm-100.3",
        "title": "Add confidence simulation for grounding demo",
        "description": "Add confidence score simulation to demo: random/configured confidence scores for user inputs to trigger different grounding strategies (optimistic >0.7, cautious 0.5-0.7, pessimistic <0.5). Show ICM moves in action.",
        "priority": 0,
        "labels": ["demo", "grounding", "icm", "confidence", "simulation"]
    },
    {
        "id": "ibdm-100.4",
        "title": "Create demo scenarios showcasing IBiS3 features",
        "description": "Create 5 pre-configured demo scenarios: (1) Happy path with incremental questioning, (2) Volunteer information handling, (3) Clarification questions, (4) Prerequisite ordering (dependencies), (5) Belief revision (reaccommodation). Each scenario shows different IBiS3 rules.",
        "priority": 0,
        "labels": ["demo", "ibis3", "scenarios", "showcase"]
    },
    {
        "id": "ibdm-100.5",
        "title": "Create demo scenarios showcasing IBiS2 grounding",
        "description": "Create 3 grounding demo scenarios: (1) Pessimistic strategy (low confidence, perception checks), (2) Cautious strategy (medium confidence, understanding confirmations), (3) Optimistic strategy (high confidence, acceptance feedback). Show complete grounding flows.",
        "priority": 0,
        "labels": ["demo", "ibis2", "grounding", "scenarios"]
    },
    {
        "id": "ibdm-100.6",
        "title": "Add dialogue visualization and history",
        "description": "Add rich dialogue visualization: color-coded output (system/user/ICM), dialogue move annotations, QUD stack display, private.issues display, grounding status indicators. Show internal state for educational purposes.",
        "priority": 0,
        "labels": ["demo", "visualization", "history", "debugging"]
    },
    {
        "id": "ibdm-100.7",
        "title": "Create session persistence and replay",
        "description": "Add session save/load: persist dialogue state to JSON, reload previous sessions, replay dialogues step-by-step. Enable debugging and demonstration of complex multi-turn scenarios.",
        "priority": 0,
        "labels": ["demo", "persistence", "replay", "debugging"]
    },
    {
        "id": "ibdm-100.8",
        "title": "Write demo user guide and documentation",
        "description": "Create docs/demo_guide.md: how to run demo, available commands, scenario descriptions, what each scenario demonstrates, interpreting output, understanding internal state display.",
        "priority": 0,
        "labels": ["demo", "documentation", "guide", "user-guide"]
    },
    {
        "id": "ibdm-100.9",
        "title": "Create README for demo with example outputs",
        "description": "Create src/ibdm/demo/README.md with: quick start, example dialogue outputs (transcripts), screenshots/examples of each scenario, explanation of demonstrated features, links to documentation.",
        "priority": 0,
        "labels": ["demo", "documentation", "readme", "examples"]
    },
    {
        "id": "ibdm-100.10",
        "title": "Add comprehensive demo test suite",
        "description": "Create tests/integration/test_demo.py: test all demo scenarios run without errors, verify IBiS3 rules fire correctly, verify IBiS2 grounding strategies work, test session persistence, test CLI commands.",
        "priority": 0,
        "labels": ["demo", "testing", "integration", "validation"]
    },
]

# Add all subtasks to demo_tasks
for task in demo_subtasks:
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
    demo_tasks.append(task_entry)

# Append to existing issues.jsonl
with open('/home/user/ibdm/.beads/issues.jsonl', 'a') as f:
    for task in demo_tasks:
        f.write(json.dumps(task) + '\n')

print(f"Created {len(demo_tasks)} demo tasks (1 epic + {len(demo_subtasks)} subtasks)")
print()
print("Demo Epic: ibdm-100")
print("Demo Tasks: ibdm-100.1 through ibdm-100.10")
print()
print("Tasks created:")
for task in demo_subtasks:
    print(f"  - {task['id']}: {task['title']}")
