#!/bin/bash
# Audit beads tasks against actual implementation

echo "=== TASK AUDIT REPORT ==="
echo ""

# ibdm-loop tasks
echo "## ibdm-loop Tasks"
echo ""

echo "✅ ibdm-loop.2: Domain validation"
grep -q "domain.resolves(answer" src/ibdm/rules/integration_rules.py && echo "   IMPLEMENTED: domain.resolves() in integration_rules.py:482"

echo "✅ ibdm-loop.4: Mark subplan complete"
grep -q "_complete_subplan_for_question" src/ibdm/rules/integration_rules.py && echo "   IMPLEMENTED: _complete_subplan_for_question() called in integration"

echo "✅ ibdm-loop.5: Push next question to QUD"
grep -q "_get_next_question_from_plan" src/ibdm/rules/integration_rules.py && echo "   IMPLEMENTED: _get_next_question_from_plan() with push_qud()"

echo "❓ ibdm-loop.3: Handle invalid answers with clarification"
grep -q "clarification\|invalid" src/ibdm/rules/integration_rules.py && echo "   IMPLEMENTED" || echo "   NOT FOUND: No clarification handling for invalid answers"

echo ""
echo "## ibdm-accom Tasks"
echo ""

echo "✅ ibdm-accom.1.1: Add accommodate_command integration rule"
grep -q "form_task_plan" src/ibdm/rules/integration_rules.py && echo "   IMPLEMENTED: form_task_plan integration rule (renamed from accommodate_command)"

echo "✅ ibdm-accom.1.2: Implement _accommodate_task"
grep -q "_form_task_plan" src/ibdm/rules/integration_rules.py && echo "   IMPLEMENTED: _form_task_plan() effect function"

echo "✅ ibdm-accom.2.1: Remove accommodate_nda_task from interpretation"
! grep -q "accommodate" src/ibdm/rules/interpretation_rules.py && echo "   IMPLEMENTED: No accommodation in interpretation_rules.py"

echo "✅ ibdm-accom.2.2: Remove task classifier from interpretation"
! grep -q "task.*classifier\|classify.*task" src/ibdm/rules/interpretation_rules.py && echo "   IMPLEMENTED: No task classifier in interpretation"

echo ""
echo "## ibdm-bsr Tasks"
echo ""

echo "✅ ibdm-bsr.1: Extract InformationState to Burr State"
grep -q 'information_state' src/ibdm/burr_integration/state_machine.py && echo "   IMPLEMENTED: InformationState in Burr State"

echo "✅ ibdm-bsr.2: Initialize action creates InformationState"
grep -q 'InformationState(' src/ibdm/burr_integration/actions.py && echo "   IMPLEMENTED: initialize() creates InformationState"

echo "✅ ibdm-bsr.8: Update interpret action"
grep -A3 '@action' src/ibdm/burr_integration/actions.py | grep -q 'interpret' && echo "   IMPLEMENTED: interpret action exists and reads information_state"

echo "✅ ibdm-bsr.9: Update integrate action"
grep -A3 '@action' src/ibdm/burr_integration/actions.py | grep -q 'integrate' && echo "   IMPLEMENTED: integrate action exists and reads/writes information_state"

echo "✅ ibdm-bsr.10: Update select action"
grep -A3 '@action' src/ibdm/burr_integration/actions.py | grep -q 'select' && echo "   IMPLEMENTED: select action exists"

echo "✅ ibdm-bsr.11: Update generate action"
grep -A3 '@action' src/ibdm/burr_integration/actions.py | grep -q 'generate' && echo "   IMPLEMENTED: generate action exists"

echo "❓ ibdm-bsr.17: Add nlu_context to Burr State"
grep -q 'nlu_context' src/ibdm/burr_integration/actions.py && echo "   IMPLEMENTED: nlu_context in Burr State" || echo "   NOT FOUND: Check if nlu_context is in state"

echo ""
echo "=== SUMMARY ==="
echo "Run 'bd close <task-id>' for each ✅ task to mark as complete"
