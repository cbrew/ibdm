#!/usr/bin/env python3
"""Update beads task priorities to align with ZFC principles."""

import json
from pathlib import Path
from datetime import datetime, timezone

# Priority mappings based on ZFC analysis
PRIORITY_UPDATES = {
    # Phase 1: Core Foundation (ibdm-brm) - Promote to Priority 3 (HIGHEST)
    "ibdm-brm": 3,
    "ibdm-brm.1": 3,  # Data structures
    "ibdm-brm.2": 3,  # Update rules
    "ibdm-brm.3": 3,  # DialogueMoveEngine
    "ibdm-brm.4": 3,  # Tests
    "ibdm-brm.5": 2,  # Serialization (infrastructure)

    # Phase 2: Burr Integration (ibdm-zfl) - Keep at Priority 2
    "ibdm-zfl": 2,
    "ibdm-zfl.1": 2,  # Design
    "ibdm-zfl.2": 2,  # Actions
    "ibdm-zfl.3": 2,  # Transitions
    "ibdm-zfl.4": 2,  # Persistence
    "ibdm-zfl.5": 1,  # Visualization (nice-to-have)

    # Phase 3: Rule Development (ibdm-63p) - Split by ZFC compliance
    "ibdm-63p": 2,
    "ibdm-63p.1": 2,  # Interpretation (AI delegation)
    "ibdm-63p.2": 3,  # Integration (Larsson algorithms) - PROMOTE
    "ibdm-63p.3": 3,  # Selection (Larsson algorithms) - PROMOTE
    "ibdm-63p.4": 2,  # Generation (AI delegation)

    # Phase 4: Accommodation (ibdm-x1g) - Keep at Priority 1
    "ibdm-x1g": 1,
    "ibdm-x1g.1": 1,
    "ibdm-x1g.2": 1,
    "ibdm-x1g.3": 1,
    "ibdm-x1g.4": 1,

    # Phase 5: Multi-Agent (ibdm-tty) - Keep at Priority 1
    "ibdm-tty": 1,
    "ibdm-tty.1": 1,
    "ibdm-tty.2": 1,
    "ibdm-tty.3": 1,
    "ibdm-tty.4": 1,
    "ibdm-tty.5": 1,
    "ibdm-tty.6": 1,

    # Phase 6: Grounding/ICM (ibdm-okw) - Keep at Priority 1
    "ibdm-okw": 1,
    "ibdm-okw.1": 1,
    "ibdm-okw.2": 1,
    "ibdm-okw.3": 1,
    "ibdm-okw.4": 1,

    # Phase 7: Integration/Testing (ibdm-dus) - Demote to Priority 0
    "ibdm-dus": 0,
    "ibdm-dus.1": 0,
    "ibdm-dus.2": 0,
    "ibdm-dus.3": 0,
    "ibdm-dus.4": 0,
    "ibdm-dus.5": 0,

    # Phase 8: Advanced Features (ibdm-xeh) - Demote to Priority 0
    "ibdm-xeh": 0,
    "ibdm-xeh.1": 0,
    "ibdm-xeh.2": 0,
    "ibdm-xeh.3": 0,
    "ibdm-xeh.4": 0,
    "ibdm-xeh.5": 0,
}

def update_beads_priorities():
    """Update priorities in issues.jsonl according to ZFC analysis."""
    beads_dir = Path(__file__).parent
    issues_file = beads_dir / "issues.jsonl"
    backup_file = beads_dir / f"issues.jsonl.backup-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"

    # Backup original file
    if issues_file.exists():
        issues_file.rename(backup_file)
        print(f"Created backup: {backup_file}")

    # Read from backup, write updated to issues.jsonl
    updated_count = 0
    unchanged_count = 0

    with open(backup_file, 'r') as infile, open(issues_file, 'w') as outfile:
        for line in infile:
            issue = json.loads(line)
            task_id = issue.get("id")
            old_priority = issue.get("priority")

            if task_id in PRIORITY_UPDATES:
                new_priority = PRIORITY_UPDATES[task_id]
                if old_priority != new_priority:
                    issue["priority"] = new_priority
                    issue["updated_at"] = datetime.now(timezone.utc).isoformat()
                    updated_count += 1
                    print(f"Updated {task_id}: priority {old_priority} → {new_priority}")
                else:
                    unchanged_count += 1
            else:
                unchanged_count += 1

            outfile.write(json.dumps(issue) + '\n')

    print(f"\nSummary:")
    print(f"  Updated: {updated_count} tasks")
    print(f"  Unchanged: {unchanged_count} tasks")
    print(f"  Backup: {backup_file}")

if __name__ == "__main__":
    update_beads_priorities()
