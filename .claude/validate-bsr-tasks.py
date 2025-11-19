#!/usr/bin/env python3
"""
Validate Burr State Refactoring (BSR) tasks.

Checks which BSR tasks are actually complete vs. still open.
This helps identify stale task metadata in the beads database.

Author: Claude Code
Date: 2025-11-14
"""

import inspect
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import actions module directly (not from __init__) to avoid circular import
import ibdm.burr_integration.actions as actions
from ibdm.burr_integration.nlu_context import NLUContext
from ibdm.core import InformationState
from ibdm.engine import DialogueMoveEngine


def validate_bsr_1() -> tuple[bool, str]:
    """ibdm-bsr.1: Extract InformationState from engine to Burr State."""
    try:
        # Check 1: No self.state in DialogueMoveEngine.__init__
        init_source = inspect.getsource(DialogueMoveEngine.__init__)
        if "self.state = " in init_source:
            return False, "DialogueMoveEngine still has self.state"

        # Check 2: Engine is stateless (no state attribute)
        engine = DialogueMoveEngine("test")
        if hasattr(engine, "state"):
            return False, "Engine instance has state attribute"

        return True, "InformationState successfully extracted from engine"
    except Exception as e:
        return False, f"Validation error: {e}"


def validate_bsr_2() -> tuple[bool, str]:
    """ibdm-bsr.2: Update initialize action to create InformationState in Burr."""
    try:
        # Check initialize action source
        init_source = inspect.getsource(actions.initialize)

        # Check 1: Creates InformationState
        if "InformationState(" not in init_source:
            return False, "initialize doesn't create InformationState"

        # Check 2: Writes to Burr state
        if "information_state" not in init_source or "to_dict()" not in init_source:
            return False, "initialize doesn't write information_state to Burr State"

        # Check 3: Returns information_state in state.update()
        if "state.update(" not in init_source:
            return False, "initialize doesn't update Burr state"

        return True, "initialize action creates and stores InformationState in Burr"
    except Exception as e:
        return False, f"Validation error: {e}"


def validate_bsr_3() -> tuple[bool, str]:
    """ibdm-bsr.3: Convert interpret() to accept and return state."""
    try:
        # Check method signature
        sig = inspect.signature(DialogueMoveEngine.interpret)

        # Check 1: Has state parameter
        if "state" not in sig.parameters:
            return False, "interpret() doesn't accept state parameter"

        # Check 2: Type hint is InformationState
        state_param = sig.parameters["state"]
        if state_param.annotation != InformationState:
            return False, f"state parameter has wrong type: {state_param.annotation}"

        # Check 3: Returns list of moves (not tuple with state)
        # This is intentional - interpret is read-only for state
        if sig.return_annotation != list[DialogueMoveEngine.__annotations__.get("interpret", list)]:
            pass  # Return type varies, don't enforce strictly

        return True, "interpret() accepts state parameter"
    except Exception as e:
        return False, f"Validation error: {e}"


def validate_bsr_4() -> tuple[bool, str]:
    """ibdm-bsr.4: Convert integrate() to pure function."""
    try:
        # Check method signature
        sig = inspect.signature(DialogueMoveEngine.integrate)

        # Check 1: Has state parameter
        if "state" not in sig.parameters:
            return False, "integrate() doesn't accept state parameter"

        # Check 2: Returns InformationState
        if sig.return_annotation != InformationState:
            return False, f"integrate() doesn't return InformationState: {sig.return_annotation}"

        # Check 3: Method source doesn't mutate self.state
        source = inspect.getsource(DialogueMoveEngine.integrate)
        if "self.state" in source:
            return False, "integrate() still references self.state"

        return True, "integrate() is a pure function (accepts and returns state)"
    except Exception as e:
        return False, f"Validation error: {e}"


def validate_bsr_5() -> tuple[bool, str]:
    """ibdm-bsr.5: Convert select_action() to accept state parameter."""
    try:
        # Check method signature
        sig = inspect.signature(DialogueMoveEngine.select_action)

        # Check 1: Has state parameter
        if "state" not in sig.parameters:
            return False, "select_action() doesn't accept state parameter"

        # Check 2: Returns tuple (move, state)
        # Return type should be tuple[DialogueMove | None, InformationState]
        # Don't enforce strictly as annotation may vary

        # Check 3: Method source doesn't mutate self.state
        source = inspect.getsource(DialogueMoveEngine.select_action)
        if "self.state" in source:
            return False, "select_action() still references self.state"

        return True, "select_action() accepts state parameter"
    except Exception as e:
        return False, f"Validation error: {e}"


def validate_bsr_6() -> tuple[bool, str]:
    """ibdm-bsr.6: Convert generate() to accept state parameter."""
    try:
        # Check method signature
        sig = inspect.signature(DialogueMoveEngine.generate)

        # Check 1: Has state parameter
        if "state" not in sig.parameters:
            return False, "generate() doesn't accept state parameter"

        # Check 2: Returns str (not tuple)
        if sig.return_annotation is not str:
            return False, f"generate() should return str: {sig.return_annotation}"

        # Check 3: Method source doesn't mutate self.state
        source = inspect.getsource(DialogueMoveEngine.generate)
        if "self.state" in source:
            return False, "generate() still references self.state"

        return True, "generate() accepts state parameter"
    except Exception as e:
        return False, f"Validation error: {e}"


def validate_bsr_7() -> tuple[bool, str]:
    """ibdm-bsr.7: Remove self.state completely from DialogueMoveEngine."""
    try:
        # Check 1: No self.state in entire class
        source = inspect.getsource(DialogueMoveEngine)
        if "self.state" in source:
            return False, "DialogueMoveEngine still has references to self.state"

        # Check 2: __init__ doesn't create state
        init_source = inspect.getsource(DialogueMoveEngine.__init__)
        if "self.state" in init_source:
            return False, "__init__ still creates self.state"

        # Check 3: Instance doesn't have state attribute
        engine = DialogueMoveEngine("test")
        if hasattr(engine, "state"):
            return False, "Engine instance has state attribute"

        return True, "self.state completely removed from DialogueMoveEngine"
    except Exception as e:
        return False, f"Validation error: {e}"


def validate_bsr_8() -> tuple[bool, str]:
    """ibdm-bsr.8: Update interpret action to read/write InformationState."""
    try:
        # Check action reads/writes
        source = inspect.getsource(actions.interpret)

        # Check 1: Reads information_state from Burr state
        if "information_state" not in source:
            return False, "interpret action doesn't read information_state"

        # Check 2: Reads from state["information_state"]
        if (
            'state["information_state"]' not in source
            and 'state.get("information_state")' not in source
        ):
            return False, "interpret action doesn't access information_state from Burr state"

        # Check 3: Converts from dict to InformationState
        if "InformationState.from_dict" not in source:
            return False, "interpret action doesn't deserialize InformationState"

        return True, "interpret action reads InformationState from Burr state"
    except Exception as e:
        return False, f"Validation error: {e}"


def validate_bsr_9() -> tuple[bool, str]:
    """ibdm-bsr.9: Update integrate action to read/write InformationState."""
    try:
        # Check action reads/writes
        source = inspect.getsource(actions.integrate)

        # Check 1: Reads information_state
        if "information_state" not in source:
            return False, "integrate action doesn't read information_state"

        # Check 2: Writes information_state back
        if "state.update(" not in source or "information_state=" not in source:
            return False, "integrate action doesn't write information_state back"

        # Check 3: Converts to dict for storage
        if "to_dict()" not in source:
            return False, "integrate action doesn't serialize InformationState"

        return True, "integrate action reads/writes InformationState in Burr state"
    except Exception as e:
        return False, f"Validation error: {e}"


def validate_bsr_13() -> tuple[bool, str]:
    """ibdm-bsr.13: Create NLUContext dataclass for NLU state."""
    try:
        # Check if NLUContext exists
        if not hasattr(NLUContext, "__dataclass_fields__"):
            return False, "NLUContext is not a dataclass"

        # Check required fields
        fields = NLUContext.__dataclass_fields__
        required = {"entities", "entity_mentions", "reference_chains"}

        missing = required - set(fields.keys())
        if missing:
            return False, f"NLUContext missing fields: {missing}"

        # Check if it has to_dict/from_dict methods
        if not hasattr(NLUContext, "to_dict"):
            return False, "NLUContext doesn't have to_dict method"
        if not hasattr(NLUContext, "from_dict"):
            return False, "NLUContext doesn't have from_dict method"

        return True, "NLUContext dataclass exists with required fields"
    except Exception as e:
        return False, f"Validation error: {e}"


def validate_bsr_17() -> tuple[bool, str]:
    """ibdm-bsr.17: Add nlu_context to Burr State schema."""
    try:
        # Check initialize action creates NLUContext
        source = inspect.getsource(actions.initialize)

        if "NLUContext" not in source:
            return False, "initialize doesn't create NLUContext"

        if "nlu_context" not in source:
            return False, "initialize doesn't add nlu_context to state"

        return True, "nlu_context added to Burr State schema in initialize"
    except Exception as e:
        return False, f"Validation error: {e}"


# Validator registry
VALIDATORS = {
    "ibdm-bsr.1": validate_bsr_1,
    "ibdm-bsr.2": validate_bsr_2,
    "ibdm-bsr.3": validate_bsr_3,
    "ibdm-bsr.4": validate_bsr_4,
    "ibdm-bsr.5": validate_bsr_5,
    "ibdm-bsr.6": validate_bsr_6,
    "ibdm-bsr.7": validate_bsr_7,
    "ibdm-bsr.8": validate_bsr_8,
    "ibdm-bsr.9": validate_bsr_9,
    "ibdm-bsr.13": validate_bsr_13,
    "ibdm-bsr.17": validate_bsr_17,
}


def main():
    """Run all BSR task validators."""
    print("=" * 80)
    print("BSR TASK VALIDATION REPORT")
    print("=" * 80)
    print()

    completed = []
    incomplete = []
    no_validator = []

    # Get all BSR tasks from beads
    import json

    tasks = []
    with open(".beads/issues.jsonl") as f:
        for line in f:
            task = json.loads(line)
            if task["id"].startswith("ibdm-bsr.") and len(task["id"].split(".")) == 2:
                tasks.append(task)

    # Sort by task ID
    tasks.sort(key=lambda t: t["id"])

    for task in tasks:
        task_id = task["id"]
        title = task["title"]

        if task_id in VALIDATORS:
            validator = VALIDATORS[task_id]
            is_complete, reason = validator()

            if is_complete:
                completed.append((task_id, title, reason))
                status = "✓ COMPLETE"
                color = "\033[92m"  # Green
            else:
                incomplete.append((task_id, title, reason))
                status = "✗ INCOMPLETE"
                color = "\033[91m"  # Red
            reset = "\033[0m"

            print(f"{color}{status:15}{reset} {task_id:15} {title[:50]}")
            print(f"                                 → {reason}")
            print()
        else:
            no_validator.append((task_id, title))
            print(f"{'? NO VALIDATOR':15} {task_id:15} {title[:50]}")
            print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✓ Complete:     {len(completed):3} tasks")
    print(f"✗ Incomplete:   {len(incomplete):3} tasks")
    print(f"? No Validator: {len(no_validator):3} tasks")
    print(f"  Total:        {len(tasks):3} BSR tasks")
    print()

    if completed:
        print("=" * 80)
        print("COMPLETED TASKS (should be marked 'done' in beads)")
        print("=" * 80)
        for task_id, title, reason in completed:
            print(f"  {task_id}: {title}")
        print()

    if incomplete:
        print("=" * 80)
        print("INCOMPLETE TASKS (ready to work on)")
        print("=" * 80)
        for task_id, title, reason in incomplete:
            print(f"  {task_id}: {title}")
            print(f"    Status: {reason}")
        print()

    # Exit code: 0 if all validated tasks are complete
    if incomplete:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
