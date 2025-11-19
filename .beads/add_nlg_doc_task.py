#!/usr/bin/env python3
"""Add documentation task for NLG demo."""

import hashlib
import json
from datetime import datetime, timezone

def content_hash(text: str) -> str:
    """Generate SHA256 hash of text."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def now_iso() -> str:
    """Get current time in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

timestamp = now_iso()

# New documentation task
doc_task = {
    "id": "ibdm-nlg-demo.9",
    "title": "Update documentation for NLG integration (Phase 5)",
    "description": (
        "Update documentation to explain NLG integration: "
        "Update demos/scenarios/README.md with --nlg-mode flag documentation. "
        "Document three modes: off (default), compare, replace. "
        "Add usage examples showing compare mode output. "
        "Update relevant docs to reference docs/nlg_business_demo_integration.md design. "
        "Document benefits: live NLG demonstration, quality assessment, backward compatibility."
    ),
    "status": "blocked",
    "priority": 2,
    "issue_type": "task",
    "created_at": timestamp,
    "updated_at": timestamp,
    "source_repo": ".",
    "labels": ["nlg", "demo", "documentation"]
}

doc_task["content_hash"] = content_hash(doc_task["title"] + doc_task["description"])

# Append to issues.jsonl
with open('/home/user/ibdm/.beads/issues.jsonl', 'a') as f:
    f.write(json.dumps(doc_task) + '\n')

print(f"✓ Added task ibdm-nlg-demo.9: {doc_task['title']}")
