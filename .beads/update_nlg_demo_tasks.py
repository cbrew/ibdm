#!/usr/bin/env python3
"""Update NLG demo tasks based on completed design (ibdm-nlg-demo.1)."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

def content_hash(text: str) -> str:
    """Generate SHA256 hash of text."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def now_iso() -> str:
    """Get current time in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

# Read existing issues
issues_file = Path('/home/user/ibdm/.beads/issues.jsonl')
all_issues = []
with open(issues_file, 'r') as f:
    for line in f:
        if line.strip():
            all_issues.append(json.loads(line))

# Find and update NLG demo tasks
timestamp = now_iso()
updated_count = 0

for issue in all_issues:
    issue_id = issue.get('id', '')

    # Update task .1 (design) - mark as completed
    if issue_id == 'ibdm-nlg-demo.1':
        issue['status'] = 'completed'
        issue['updated_at'] = timestamp
        updated_count += 1
        print(f"✓ Marked {issue_id} as completed (design done)")

    # Update task .2 - align with Phase 2 (State Management)
    elif issue_id == 'ibdm-nlg-demo.2':
        issue['title'] = 'Implement state management with real InformationState'
        issue['description'] = (
            'Use existing self.state (InformationState) instead of cumulative_state dictionary. '
            'Refactor _update_cumulative_state() to apply state_changes to real InformationState objects. '
            'Implement proper state operations: qud_pushed/popped → state.shared.qud, '
            'commitment_added → state.shared.com, plan_created → state.private.plan. '
            'Test state reconstruction matches expected state in scenarios.'
        )
        issue['status'] = 'ready'
        issue['labels'] = ['nlg', 'demo', 'state-management']
        issue['content_hash'] = content_hash(issue['title'] + issue['description'])
        issue['updated_at'] = timestamp
        updated_count += 1
        print(f"✓ Updated {issue_id} → Phase 2: State Management")

    # Update task .3 - align with Phase 3 (Move Construction)
    elif issue_id == 'ibdm-nlg-demo.3':
        issue['title'] = 'Implement DialogueMove construction from JSON'
        issue['description'] = (
            'Implement _create_dialogue_move_from_turn() to construct DialogueMove objects from scenario JSON. '
            'Parse questions from state_changes: "?x.predicate(x)" → WhQuestion, detect AltQuestion from alternatives. '
            'Parse answers from utterances with question references. '
            'Handle all move types: request, ask, answer, inform, greet. '
            'Test move construction produces valid DialogueMove objects with proper content types.'
        )
        issue['status'] = 'blocked'
        issue['labels'] = ['nlg', 'demo', 'move-construction']
        issue['content_hash'] = content_hash(issue['title'] + issue['description'])
        issue['updated_at'] = timestamp
        updated_count += 1
        print(f"✓ Updated {issue_id} → Phase 3: Move Construction")

    # Update task .4 - align with Phase 4 (NLG Integration)
    elif issue_id == 'ibdm-nlg-demo.4':
        issue['title'] = 'Integrate NLG engine with three modes'
        issue['description'] = (
            'Add --nlg-mode flag with three options: "off" (default, scripted only), '
            '"compare" (show both scripted and NLG side-by-side), "replace" (NLG only). '
            'Initialize NLG engine conditionally (only when mode != "off"). '
            'For system turns: construct DialogueMove, call nlg_engine.generate(move, state), '
            'display based on mode. In compare mode, show scripted (gold standard) and NLG-generated with differences highlighted.'
        )
        issue['status'] = 'blocked'
        issue['labels'] = ['nlg', 'demo', 'integration']
        issue['content_hash'] = content_hash(issue['title'] + issue['description'])
        issue['updated_at'] = timestamp
        updated_count += 1
        print(f"✓ Updated {issue_id} → Phase 4: NLG Integration")

    # Rename task .5 to focus on comparison mode (part of Phase 4)
    elif issue_id == 'ibdm-nlg-demo.5':
        issue['title'] = 'Add comparison display and metrics'
        issue['description'] = (
            'Implement compare mode display: show scripted (📜 Gold Standard) and NLG-generated (🤖 Generated) '
            'side-by-side with color coding. Highlight differences between utterances. '
            'Add similarity metrics: exact match, word overlap, semantic similarity (optional). '
            'Update print_turn() to handle all three display modes (off, compare, replace).'
        )
        issue['status'] = 'blocked'
        issue['priority'] = 1
        issue['labels'] = ['nlg', 'demo', 'comparison']
        issue['content_hash'] = content_hash(issue['title'] + issue['description'])
        issue['updated_at'] = timestamp
        updated_count += 1
        print(f"✓ Updated {issue_id} → Comparison display")

    # Update task .6 - LLM mode is lower priority
    elif issue_id == 'ibdm-nlg-demo.6':
        issue['title'] = 'Add LLM-based NLG strategy (future)'
        issue['description'] = (
            'Extend NLG engine to support LLM-based generation using Claude 4.5 Haiku. '
            'Add strategy parameter to NLGEngineConfig. Update business demo to pass strategy. '
            'This is a future enhancement - current implementation uses template/plan_aware strategies. '
            'Demonstrates full ZFC-compliant NLG for language generation.'
        )
        issue['status'] = 'blocked'
        issue['priority'] = 3
        issue['labels'] = ['nlg', 'demo', 'llm', 'future']
        issue['content_hash'] = content_hash(issue['title'] + issue['description'])
        issue['updated_at'] = timestamp
        updated_count += 1
        print(f"✓ Updated {issue_id} → LLM mode (future)")

    # Update task .7 - engineer report updates
    elif issue_id == 'ibdm-nlg-demo.7':
        issue['title'] = 'Update HTML reports with NLG metadata'
        issue['description'] = (
            'Enhance engineer report to show NLG metadata when --nlg-mode != "off": '
            'strategy used (template/plan_aware/llm), generation rule applied, latency, tokens (for LLM). '
            'Show in turn-by-turn analysis alongside existing state changes. '
            'Update business report to mention NLG mode if enabled.'
        )
        issue['status'] = 'blocked'
        issue['priority'] = 2
        issue['labels'] = ['nlg', 'demo', 'reporting']
        issue['content_hash'] = content_hash(issue['title'] + issue['description'])
        issue['updated_at'] = timestamp
        updated_count += 1
        print(f"✓ Updated {issue_id} → HTML reports")

    # Task .8 - tests (Phase 5)
    elif issue_id == 'ibdm-nlg-demo.8':
        issue['title'] = 'Add tests for NLG integration (Phase 5)'
        issue['description'] = (
            'Write comprehensive tests: '
            '(1) Test state reconstruction from state_changes, '
            '(2) Test DialogueMove construction from JSON turns, '
            '(3) Test NLG generation for each move type, '
            '(4) Test all three modes (off, compare, replace), '
            '(5) Integration test: run full scenario with NLG, verify output quality. '
            'Tests in tests/integration/test_business_demo_nlg.py'
        )
        issue['status'] = 'blocked'
        issue['priority'] = 2
        issue['labels'] = ['nlg', 'demo', 'testing']
        issue['content_hash'] = content_hash(issue['title'] + issue['description'])
        issue['updated_at'] = timestamp
        updated_count += 1
        print(f"✓ Updated {issue_id} → Phase 5: Testing")

    # Rename old task .8 to .9 - documentation
    elif issue_id == 'ibdm-nlg-demo.9':
        # This was previously ibdm-nlg-demo.8 in the old scheme
        # Check if we need to update it
        if 'Update business demo documentation' in issue.get('title', ''):
            issue['title'] = 'Update documentation for NLG integration (Phase 5)'
            issue['description'] = (
                'Update documentation to explain NLG integration: '
                'Update demos/scenarios/README.md with --nlg-mode flag documentation. '
                'Document three modes: off (default), compare, replace. '
                'Update CLAUDE.md or relevant docs with NLG design reference. '
                'Add examples showing compare mode output.'
            )
            issue['status'] = 'blocked'
            issue['priority'] = 2
            issue['labels'] = ['nlg', 'demo', 'documentation']
            issue['content_hash'] = content_hash(issue['title'] + issue['description'])
            issue['updated_at'] = timestamp
            updated_count += 1
            print(f"✓ Updated {issue_id} → Phase 5: Documentation")

# Write updated issues back
with open(issues_file, 'w') as f:
    for issue in all_issues:
        f.write(json.dumps(issue) + '\n')

print(f"\n✓ Updated {updated_count} NLG demo tasks based on design")
print("\nTask Status:")
print("  ✅ ibdm-nlg-demo.1: Completed (design document)")
print("  📋 ibdm-nlg-demo.2: Ready (Phase 2: State Management)")
print("  🔒 ibdm-nlg-demo.3: Blocked (Phase 3: Move Construction)")
print("  🔒 ibdm-nlg-demo.4: Blocked (Phase 4: NLG Integration)")
print("  🔒 ibdm-nlg-demo.5: Blocked (Comparison display)")
print("  🔒 ibdm-nlg-demo.6: Blocked (LLM mode - future)")
print("  🔒 ibdm-nlg-demo.7: Blocked (HTML reports)")
print("  🔒 ibdm-nlg-demo.8: Blocked (Phase 5: Testing)")
print("  🔒 ibdm-nlg-demo.9: Blocked (Phase 5: Documentation)")
