"""Integration rules for Issue-Based Dialogue Management.

Integration rules update the information state based on dialogue moves.
They manage the QUD stack, commitments, and agenda.

Task plan formation (creating plans for user tasks) happens here in the
integration phase, NOT in interpretation. This is the correct phase per
Larsson (2002).

Based on Larsson (2002) Issue-based Dialogue Management.
"""

from ibdm.core import Answer, DialogueMove, InformationState, Question
from ibdm.rules.icm_integration_rules import create_icm_integration_rules
from ibdm.rules.update_rules import UpdateRule
from ibdm.utils.skip_detection import is_skip_request


def create_integration_rules() -> list[UpdateRule]:
    """Create standard integration rules including IBiS2 ICM rules.

    Returns IBiS1, IBiS2, and IBiS3 integration rules:
    - IBiS2 ICM integration rules (grounding feedback processing)
    - IBiS1 basic integration rules (questions, answers, assertions)
    - IBiS3 accommodation rules (issue accommodation, reaccommodation)

    Returns:
        List of integration rules
    """
    # Start with IBiS2 ICM integration rules
    # These have priority 15 (high) and 5 (low) to bookend other rules
    rules = create_icm_integration_rules()

    # Add IBiS1 and IBiS3 integration rules
    rules.extend(
        [
            # Task plan formation - create plans for command/request moves
            # This is THE RIGHT PLACE for task plan formation per Larsson (2002)
            # Renamed from "accommodate_command" to clarify this is task plan formation,
            # not Larsson's presupposition accommodation
            # MUST RUN FIRST - creates the plan that Rule 4.1 will accommodate
            UpdateRule(
                name="form_task_plan",
                preconditions=_is_task_request_move,
                effects=_form_task_plan,
                priority=14,  # Highest - must create plan before accommodation
                rule_type="integration",
            ),
            # IBiS3 Rule 4.1: IssueAccommodation - accommodate findout subplans to private.issues
            # This must run AFTER form_task_plan to accommodate newly created plan's questions
            UpdateRule(
                name="accommodate_issue_from_plan",
                preconditions=_plan_has_findout_subplan,
                effects=_accommodate_findout_to_issues,
                priority=13,  # After form_task_plan (14)
                rule_type="integration",
            ),
            # Command integration - treat commands like requests
            UpdateRule(
                name="integrate_command",
                preconditions=_is_command_move,
                effects=_integrate_command,
                priority=12,
                rule_type="integration",
            ),
            # Request integration - task accommodation (no QUD change needed, plan already created)
            UpdateRule(
                name="integrate_request",
                preconditions=_is_request_move,
                effects=_integrate_request,
                priority=11,
                rule_type="integration",
            ),
            # IBiS3 Rule 4.3: IssueClarification - accommodate clarification questions to QUD
            # This must run BEFORE answer integration to handle unclear/invalid answers
            UpdateRule(
                name="accommodate_clarification_question",
                preconditions=_needs_clarification_question,
                effects=_accommodate_clarification,
                priority=10,  # Before integrate_answer (8)
                rule_type="integration",
            ),
            # IBiS3 Rule 4.8: DependentQuestionReaccommodation
            # When a question is reaccommodated, also reaccommodate dependent questions
            # Must run BEFORE reaccommodate_question (priority 10)
            UpdateRule(
                name="reaccommodate_dependent_questions",
                preconditions=_has_dependent_questions_to_reaccommodate,
                effects=_reaccommodate_dependent_questions,
                priority=11,  # Before reaccommodate_question (10)
                rule_type="integration",
            ),
            # IBiS3 Rule 4.6: QuestionReaccommodation (accommodate Com 2Issues)
            # Re-raise question when user provides conflicting answer
            # Must run BEFORE retract (priority 9) and integrate_answer (priority 8)
            UpdateRule(
                name="reaccommodate_question_from_commitment",
                preconditions=_needs_question_reaccommodation,
                effects=_reaccommodate_question,
                priority=10,  # Before retract (9) and integrate_answer (8)
                rule_type="integration",
            ),
            # IBiS3 Rule 4.7: Retract incompatible commitment
            # Remove old incompatible commitment before integrating new answer
            # Must run BEFORE integrate_answer (priority 8)
            UpdateRule(
                name="retract_incompatible_commitment",
                preconditions=_has_incompatible_commitment,
                effects=_retract_commitment,
                priority=9,  # Before integrate_answer (8)
                rule_type="integration",
            ),
            # Skip question handling - allow users to override optional questions
            # When user says "skip that", "I don't have that info", etc.
            # Must run BEFORE integrate_answer (priority 8)
            UpdateRule(
                name="accommodate_skip_question",
                preconditions=_is_skip_request_move,
                effects=_accommodate_skip_question,
                priority=9,  # Before integrate_answer (8)
                rule_type="integration",
            ),
            # Question integration - push to QUD
            UpdateRule(
                name="integrate_question",
                preconditions=_is_ask_move,
                effects=_integrate_question,
                priority=7,  # After reaccommodation rules
                rule_type="integration",
            ),
            # Answer integration - resolve QUD and add commitment
            UpdateRule(
                name="integrate_answer",
                preconditions=_is_answer_move,
                effects=_integrate_answer,
                priority=8,  # After reaccommodation and retract
                rule_type="integration",
            ),
            # Assertion integration - add to commitments
            UpdateRule(
                name="integrate_assertion",
                preconditions=_is_assert_move,
                effects=_integrate_assertion,
                priority=7,
                rule_type="integration",
            ),
            # Greet integration - update control
            UpdateRule(
                name="integrate_greet",
                preconditions=_is_greet_move,
                effects=_integrate_greet,
                priority=6,
                rule_type="integration",
            ),
            # Quit integration - end dialogue
            UpdateRule(
                name="integrate_quit",
                preconditions=_is_quit_move,
                effects=_integrate_quit,
                priority=6,
                rule_type="integration",
            ),
        ]
    )

    return rules


# Precondition functions


def _plan_has_findout_subplan(state: InformationState) -> bool:
    """Check if there's an active plan with findout subplans to accommodate.

    This checks if we've just created a task plan that contains findout
    subplans. These should be accommodated to private.issues first,
    not pushed directly to shared.qud.

    Larsson (2002) Section 4.6.1 - IssueAccommodation rule.
    """
    # Check if we have active plans with findout subplans
    for plan in state.private.plan:
        if not plan.is_active():
            continue

        # Check if plan has unaccommodated findout subplans
        for subplan in plan.subplans:
            if subplan.plan_type == "findout" and subplan.is_active():
                # Check if this question is already in issues or QUD
                question = subplan.content
                if isinstance(question, Question):
                    if question not in state.private.issues and question not in state.shared.qud:
                        return True

    return False


def _is_task_request_move(state: InformationState) -> bool:
    """Check if move is a command/request that requires task plan formation.

    This checks for command or request moves that indicate the user wants
    the system to perform a task (e.g., "I need to draft an NDA").
    """
    move = state.private.beliefs.get("_temp_move")
    if not isinstance(move, DialogueMove):
        return False

    # Check if it's a command or request move
    if move.move_type not in ["command", "request"]:
        return False

    # Check if it looks like a task request (has task metadata or keywords)
    metadata = move.metadata or {}
    task_type = metadata.get("task_type")
    intent = metadata.get("intent", "")

    # Check for explicit task type or draft-related intent
    if task_type or "draft" in intent.lower():
        return True

    # Check content for task keywords
    content_str = str(move.content).lower()
    task_keywords = [
        "draft",
        "create",
        "prepare",
        "need",
        "help",
        "book",
        "travel",
        "flight",
        "train",
        "trip",
    ]
    return any(keyword in content_str for keyword in task_keywords)


def _is_command_move(state: InformationState) -> bool:
    """Check if the temporary move is a 'command' move."""
    move = state.private.beliefs.get("_temp_move")
    return isinstance(move, DialogueMove) and move.move_type == "command"


def _is_request_move(state: InformationState) -> bool:
    """Check if the temporary move is a 'request' move."""
    move = state.private.beliefs.get("_temp_move")
    return isinstance(move, DialogueMove) and move.move_type == "request"


def _is_ask_move(state: InformationState) -> bool:
    """Check if the temporary move is an 'ask' move."""
    move = state.private.beliefs.get("_temp_move")
    return isinstance(move, DialogueMove) and move.move_type == "ask"


def _is_answer_move(state: InformationState) -> bool:
    """Check if the temporary move is an 'answer' move."""
    move = state.private.beliefs.get("_temp_move")
    return isinstance(move, DialogueMove) and move.move_type == "answer"


def _is_assert_move(state: InformationState) -> bool:
    """Check if the temporary move is an 'assert' move."""
    move = state.private.beliefs.get("_temp_move")
    return isinstance(move, DialogueMove) and move.move_type == "assert"


def _is_greet_move(state: InformationState) -> bool:
    """Check if the temporary move is a 'greet' move."""
    move = state.private.beliefs.get("_temp_move")
    return isinstance(move, DialogueMove) and move.move_type == "greet"


def _is_quit_move(state: InformationState) -> bool:
    """Check if the temporary move is a 'quit' move."""
    move = state.private.beliefs.get("_temp_move")
    return isinstance(move, DialogueMove) and move.move_type == "quit"


def _is_skip_request_move(state: InformationState) -> bool:
    """Check if user wants to skip the current question.

    Detects patterns like:
    - "skip that"
    - "I don't have that information"
    - "move on without it"
    - "proceed anyway"
    - "don't know"

    This only triggers if:
    1. User utterance matches skip patterns
    2. There's a question on QUD
    3. The question has required=False (optional)
    """
    move = state.private.beliefs.get("_temp_move")
    if not isinstance(move, DialogueMove):
        return False

    # Check if utterance matches skip patterns
    utterance = str(move.content) if move.content else ""
    if not is_skip_request(utterance):
        return False

    # Only allow skipping if there's a question on QUD
    top_qud = state.shared.top_qud()
    if not top_qud:
        return False

    # Only allow skipping if question is optional (required=False)
    if getattr(top_qud, "required", True):
        return False

    return True


def _needs_clarification_question(state: InformationState) -> bool:
    """Check if clarification question should be accommodated to QUD.

    IBiS3 Rule 4.3 (IssueClarification):
    When user utterance is unclear or ambiguous, we need to push
    a clarification question to QUD to resolve the ambiguity before
    continuing with the original question.

    Preconditions:
    - Clarification is needed (flag set during previous processing)
    - There's a question that needs clarification
    - Clarification question hasn't already been raised

    Larsson (2002) Section 4.6.3 - IssueClarification rule.
    """
    # Check if clarification marker is set (from previous turn or NLU)
    if not state.private.beliefs.get("_needs_clarification", False):
        return False

    # Check if we have information about what needs clarification
    clarification_question = state.private.beliefs.get("_clarification_question")
    if not clarification_question:
        return False

    # Don't re-raise if QUD top is already a clarification question
    # (Check constraints dict to see if it's a clarification question)
    top_qud = state.shared.top_qud()
    if top_qud:
        # WhQuestion has constraints dict, check if it's marked as clarification
        constraints = getattr(top_qud, "constraints", {})
        if constraints.get("is_clarification"):
            return False

    return True


def _needs_question_reaccommodation(state: InformationState) -> bool:
    """Check if question needs reaccommodation due to conflicting answer.

    IBiS3 Rule 4.6 (QuestionReaccommodation / accommodate Com 2Issues):
    When user provides an answer that conflicts with an existing commitment,
    the question should be re-raised to private.issues for re-resolution.

    Preconditions:
    - User provided an answer move
    - Answer is relevant to a question
    - There's an existing commitment for that question
    - New answer is incompatible with old commitment

    Larsson (2002) Section 4.6.6 - QuestionReaccommodation.
    """
    move = state.private.beliefs.get("_temp_move")
    if not isinstance(move, DialogueMove) or move.move_type != "answer":
        return False

    if not isinstance(move.content, Answer):
        return False

    answer = move.content
    domain = _get_active_domain(state)

    # Reaccommodation requires knowing what question the answer is for
    # In real NLU scenarios, this would be set by the interpretation phase
    if not hasattr(answer, "question_ref") or answer.question_ref is None:
        return False

    # Check each commitment to see if this answer is incompatible
    for commitment in state.shared.commitments:
        # Try to extract question from commitment
        question = domain.get_question_from_commitment(commitment)
        if not question:
            continue

        # Only check commitments for the same question as the answer
        if question != answer.question_ref:
            continue

        # Check if answer resolves this question (using domain semantic matching)
        if not domain.resolves(answer, question):
            continue

        # Construct new commitment string for this answer
        # Use predicate name (not full question object string representation)
        predicate = getattr(question, "predicate", str(question))
        new_commitment = f"{predicate}: {answer.content}"

        # Check if incompatible with existing commitment
        if domain.incompatible(new_commitment, commitment):
            # Store the question and old commitment for effect function
            state.private.beliefs["_reaccommodate_question"] = question
            state.private.beliefs["_reaccommodate_old_commitment"] = commitment
            return True

    return False


def _has_incompatible_commitment(state: InformationState) -> bool:
    """Check if there's an incompatible commitment to retract.

    IBiS3 Rule 4.7 (Retract):
    Before integrating a new answer, retract any incompatible old commitments.

    Preconditions:
    - Reaccommodation has been triggered (Rule 4.6 has marked the old commitment)

    Larsson (2002) Section 4.6.6 - part of reaccommodation process.
    """
    # Check if Rule 4.6 has identified an incompatible commitment
    return state.private.beliefs.get("_reaccommodate_old_commitment") is not None


def _has_dependent_questions_to_reaccommodate(state: InformationState) -> bool:
    """Check if dependent questions need reaccommodation.

    IBiS3 Rule 4.8 (DependentQuestionReaccommodation / accommodate Com 2Issues Dependent):
    When a question is reaccommodated, also reaccommodate questions that depend on it.

    Preconditions:
    - A question has been marked for reaccommodation (by Rule 4.6)
    - That question has dependent questions in the domain
    - The dependent questions have been answered (have commitments)

    Larsson (2002) Section 4.6.6 - dependent question reaccommodation.
    """
    reaccommodate_question = state.private.beliefs.get("_reaccommodate_question")
    if not reaccommodate_question:
        return False

    domain = _get_active_domain(state)

    # Check if any questions depend on the reaccommodated question
    # We need to check all questions in the domain and see if they depend on this one
    for commitment in state.shared.commitments:
        question = domain.get_question_from_commitment(commitment)
        if not question:
            continue

        # Check if this question depends on the reaccommodated question
        # domain.depends(Q1, Q2) returns True if Q1 depends on Q2
        # We want to find questions that depend on the reaccommodated question
        # So we check: does this question depend on the reaccommodated question?
        if domain.depends(question, reaccommodate_question):
            return True

    return False


# Effect functions


def _accommodate_findout_to_issues(state: InformationState) -> InformationState:
    """Accommodate findout subplans to private.issues.

    IBiS3 Rule 4.1 (IssueAccommodation):
    Instead of pushing questions directly to QUD, accommodate them
    to private.issues first. They'll be raised to QUD later by
    Rule 4.2 (LocalQuestionAccommodation) when contextually appropriate.

    Args:
        state: Current information state

    Returns:
        New state with findout questions accommodated to private.issues

    Larsson (2002) Section 4.6.1 - IssueAccommodation rule.
    """
    new_state = state.clone()

    # Find active plans with findout subplans
    for plan in new_state.private.plan:
        if not plan.is_active():
            continue

        # Accommodate each findout subplan to private.issues
        for subplan in plan.subplans:
            if subplan.plan_type == "findout" and subplan.is_active():
                question = subplan.content
                if isinstance(question, Question):
                    # Only accommodate if not already in issues or QUD
                    if (
                        question not in new_state.private.issues
                        and question not in new_state.shared.qud
                    ):
                        new_state.private.issues.append(question)

    return new_state


def _accommodate_clarification(state: InformationState) -> InformationState:
    """Accommodate clarification question to QUD.

    IBiS3 Rule 4.3 (IssueClarification):
    When user utterance is unclear or invalid, push a clarification
    question to QUD. This suspends the original question (it stays
    on the stack below the clarification question).

    The clarification question becomes the new top of QUD, and must
    be answered before the original question can be addressed.

    Args:
        state: Current information state

    Returns:
        New state with clarification question on QUD

    Larsson (2002) Section 4.6.3 - IssueClarification rule.
    """
    from ibdm.core import WhQuestion

    new_state = state.clone()

    # Get the invalid answer and original question
    invalid_answer = new_state.private.beliefs.get("_invalid_answer")
    original_question = new_state.private.beliefs.get("_clarification_question")

    # Generate clarification question
    # The clarification question asks the user to provide a valid answer
    # for the original question's expected type
    if isinstance(original_question, WhQuestion):
        predicate_for_clarification = f"clarification_for_{original_question.predicate}"
    else:
        predicate_for_clarification = "clarification"

    clarification_question = WhQuestion(
        predicate=predicate_for_clarification,
        variable="X",
        constraints={
            "is_clarification": True,
            "for_question": str(original_question),
            "invalid_answer": str(invalid_answer) if invalid_answer else None,
        },
    )

    # Push clarification question to QUD
    # This suspends the original question (it stays on stack below)
    new_state.shared.push_qud(clarification_question)

    # Clear the clarification flag (it's been handled)
    new_state.private.beliefs["_needs_clarification"] = False

    # Keep the invalid answer in beliefs for context
    # (Selection/generation can use this to provide helpful feedback)

    return new_state


def _accommodate_skip_question(state: InformationState) -> InformationState:
    """Handle user request to skip the current optional question.

    When user says "skip that", "I don't have that info", etc. for an
    optional question (required=False), this rule:
    1. Removes the question from QUD
    2. Adds it to private.overridden_questions for tracking
    3. Allows dialogue to proceed without that information

    Args:
        state: Current information state

    Returns:
        New state with question overridden and removed from QUD
    """
    new_state = state.clone()

    # Get the question from top of QUD
    question = new_state.shared.top_qud()
    if not question:
        return new_state

    # Only proceed if question is optional
    if getattr(question, "required", True):
        return new_state

    # Remove question from QUD
    new_state.shared.pop_qud()

    # Track that this question was overridden
    if question not in new_state.private.overridden_questions:
        new_state.private.overridden_questions.append(question)

    return new_state


def _form_task_plan(state: InformationState) -> InformationState:
    """Form execution plan for user's task.

    RENAMED from _accommodate_task to clarify this is task plan formation,
    not Larsson's presupposition accommodation.

    Uses domain model to get appropriate plan via domain.get_plan().
    This replaces hardcoded plan creation with domain-driven approach.

    Args:
        state: Current information state

    Returns:
        New state with plan added and first question on QUD
    """
    move = state.private.beliefs.get("_temp_move")
    new_state = state.clone()

    if not isinstance(move, DialogueMove):
        return new_state

    # Extract task type from metadata or content
    metadata = move.metadata or {}
    task_type = metadata.get("task_type")
    intent = metadata.get("intent", "")

    # Determine which task this is
    # For now, check for NDA-related requests
    if (
        task_type == "DRAFT_DOCUMENT"
        or "draft" in intent.lower()
        or "NDA" in str(move.content).upper()
        or "nda" in str(move.content).lower()
        or "confidentiality" in str(move.content).lower()
    ):
        # Get NDA domain and create plan using domain model
        from ibdm.domains.nda_domain import get_nda_domain

        domain = get_nda_domain()

        # Use domain to get plan (not hardcoded!)
        context = _extract_context(move, state)
        plan = domain.get_plan("nda_drafting", context)

        # Add plan to state
        new_state.private.plan.append(plan)

        # IBiS3: Do NOT push to QUD here - Rule 4.1 will accommodate to private.issues
        # Rule 4.2 will then raise to QUD when appropriate

    # Check for travel booking requests (Larsson 2002 travel agency domain)
    elif (
        task_type == "BOOK_TRAVEL"
        or "travel" in intent.lower()
        or "book" in str(move.content).lower()
        or "flight" in str(move.content).lower()
        or "train" in str(move.content).lower()
        or "trip" in str(move.content).lower()
    ):
        # Get travel domain and create plan using domain model
        from ibdm.domains.travel_domain import get_travel_domain

        domain = get_travel_domain()

        # Use domain to get plan (not hardcoded!)
        context = _extract_context(move, state)
        plan = domain.get_plan("travel_booking", context)

        # Add plan to state
        new_state.private.plan.append(plan)

        # IBiS3: Do NOT push to QUD here - Rule 4.1 will accommodate to private.issues
        # Rule 4.2 will then raise to QUD when appropriate

    # Add move to history
    new_state.shared.last_moves.append(move)

    # System should respond
    new_state.control.next_speaker = new_state.agent_id

    return new_state


def _extract_context(move: DialogueMove, state: InformationState) -> dict[str, str]:
    """Extract context from move for plan building.

    Args:
        move: The dialogue move
        state: Current information state

    Returns:
        Context dictionary for plan builder

    Note:
        Currently returns empty dict. Future enhancements could extract
        entities, intent details, etc. from move metadata.
    """
    # Can extract entities, intent details, etc.
    # For now, return empty context
    return {}


def _get_active_domain(state: InformationState):
    """Determine which domain is active based on the plan.

    Args:
        state: Current information state

    Returns:
        The active domain model, or NDA domain as default

    Note:
        Inspects active plans to determine which domain is in use.
        Falls back to NDA domain if unable to determine.
    """
    from ibdm.domains.nda_domain import get_nda_domain
    from ibdm.domains.travel_domain import get_travel_domain

    # Check active plans for domain hints
    for plan in state.private.plan:
        if plan.plan_type == "travel_booking":
            return get_travel_domain()
        elif plan.plan_type == "nda_drafting":
            return get_nda_domain()

    # Default to NDA domain for backward compatibility
    return get_nda_domain()


def _complete_subplan_for_question(state: InformationState, question: Question) -> None:
    """Mark the subplan corresponding to a question as completed.

    When an answer resolves a question, find the findout subplan that
    contains that question and mark it as completed. This allows plan
    progression.

    Args:
        state: Information state containing plans
        question: The question that was resolved

    Note:
        Implements Larsson (2002) Section 2.6 plan execution mechanism.
        Modifies state in-place.
    """
    # Iterate through active plans
    for plan in state.private.plan:
        if not plan.is_active():
            continue

        # Check subplans for matching findout
        for subplan in plan.subplans:
            if not subplan.is_active():
                continue

            # Check if this is a findout subplan with matching question
            if subplan.plan_type == "findout" and subplan.content == question:
                # Mark subplan as completed
                subplan.complete()
                return  # Found and completed, done


def _get_next_question_from_plan(state: InformationState) -> Question | None:
    """Get the next question from the next active subplan.

    After completing a subplan, find the next active findout subplan
    and return its question. Returns None if no more active subplans.

    Args:
        state: Information state containing plans

    Returns:
        Next question to push to QUD, or None if plan is complete

    Note:
        Implements plan progression per Larsson (2002) Section 2.6.
        Searches through active plans for the next findout subplan.
    """
    # Iterate through active plans
    for plan in state.private.plan:
        if not plan.is_active():
            continue

        # Find first active subplan
        for subplan in plan.subplans:
            if subplan.is_active() and subplan.plan_type == "findout":
                # Found next active findout subplan
                if isinstance(subplan.content, Question):
                    return subplan.content

    # No more active subplans
    return None


def _integrate_command(state: InformationState) -> InformationState:
    """Integrate a 'command' move by treating it like a request.

    Command moves (like "I need to draft an NDA") trigger task accommodation.
    Commands are similar to requests - they express user goals/intentions.
    """
    new_state = state.clone()
    move = new_state.private.beliefs.get("_temp_move")

    if not isinstance(move, DialogueMove):
        return new_state

    # Add to last_moves for history
    new_state.shared.last_moves.append(move)

    # System should respond to the command
    new_state.control.next_speaker = new_state.agent_id

    return new_state


def _integrate_request(state: InformationState) -> InformationState:
    """Integrate a 'request' move by acknowledging task request.

    Request moves (like "I need to draft an NDA") trigger task accommodation.
    The interpretation rule already created the plan, so this just tracks the move.
    """
    new_state = state.clone()
    move = new_state.private.beliefs.get("_temp_move")

    if not isinstance(move, DialogueMove):
        return new_state

    # Add to last_moves for history
    new_state.shared.last_moves.append(move)

    # System should respond with first question from plan
    new_state.control.next_speaker = new_state.agent_id

    return new_state


def _integrate_question(state: InformationState) -> InformationState:
    """Integrate an 'ask' move by pushing question to QUD.

    When a question is asked, it becomes the new top issue under discussion.
    """
    new_state = state.clone()
    move = new_state.private.beliefs.get("_temp_move")

    if not isinstance(move, DialogueMove):
        return new_state

    if isinstance(move.content, Question):
        # Push question to QUD stack
        new_state.shared.push_qud(move.content)

        # Add to last_moves for history
        new_state.shared.last_moves.append(move)

        # Set next speaker to the system (if user asked)
        if move.speaker != new_state.agent_id:
            new_state.control.next_speaker = new_state.agent_id
        else:
            # If system asked, wait for user response
            new_state.control.next_speaker = "user"

    return new_state


def _integrate_answer(state: InformationState) -> InformationState:
    """Integrate an 'answer' move by resolving QUD and updating commitments.

    Modified for IBiS3:
    1. Check if answer resolves question in private.issues (volunteer info)
    2. If yes: remove from issues, add commitment, DON'T raise to QUD
    3. If no: check QUD as normal (original behavior)

    When an answer is provided:
    - Check if it resolves the top QUD (using domain validation)
    - If valid: pop the question from QUD, add commitment, progress plan
    - If invalid: mark as needing clarification (Larsson Section 3.4 accommodation)

    Note:
        Uses domain.resolves() for semantic validation (Larsson Section 2.4.3)
        instead of just Question.resolves_with() to enable domain-level
        type checking and validation.
    """
    new_state = state.clone()
    move = new_state.private.beliefs.get("_temp_move")

    if not isinstance(move, DialogueMove):
        return new_state

    if isinstance(move.content, Answer):
        answer = move.content
        domain = _get_active_domain(new_state)

        # IBiS3: Check private.issues FIRST (volunteer information)
        volunteer_answer_handled = False
        for issue in new_state.private.issues[:]:  # Iterate over copy
            if domain.resolves(answer, issue):
                # User volunteered answer to unasked question!
                new_state.private.issues.remove(issue)

                # Add commitment
                commitment = f"{issue}: {answer.content}"
                new_state.shared.commitments.add(commitment)

                # Mark corresponding subplan as completed
                _complete_subplan_for_question(new_state, issue)

                # DON'T raise this question to QUD - already answered!
                volunteer_answer_handled = True
                break  # Process one volunteer answer per turn

        # If volunteer answer was handled, skip QUD processing
        if not volunteer_answer_handled:
            # No volunteer info - check QUD as normal (original behavior)
            top_question = new_state.shared.top_qud()
            if top_question:
                # Use domain.resolves() for type checking and validation
                # This implements Larsson (2002) Section 2.4.3 semantic operation
                if domain.resolves(answer, top_question):
                    # Valid answer - integrate normally
                    # Pop the resolved question
                    new_state.shared.pop_qud()

                    # Add answer as a commitment (convert to string for simplicity)
                    commitment = f"{top_question}: {answer.content}"
                    new_state.shared.commitments.add(commitment)

                    # Mark corresponding subplan as completed (Larsson Section 2.6)
                    # Find and complete the findout subplan for this question
                    _complete_subplan_for_question(new_state, top_question)

                    # IBiS3: Do NOT push next question to QUD here
                    # Rule 4.2 (LocalQuestionAccommodation) will raise it from private.issues
                    # during the SELECTION phase, implementing incremental questioning
                else:
                    # Invalid answer - needs clarification (Larsson Section 3.4)
                    # Keep question on QUD (don't pop)
                    # Mark that clarification is needed
                    new_state.private.beliefs["_needs_clarification"] = True
                    new_state.private.beliefs["_invalid_answer"] = answer.content
                    new_state.private.beliefs["_clarification_question"] = top_question

        # Add to last_moves
        new_state.shared.last_moves.append(move)

        # Switch turn (if user answered, system's turn next)
        if move.speaker != new_state.agent_id:
            new_state.control.next_speaker = new_state.agent_id
        else:
            # If system answered, check if there are more QUDs
            if new_state.shared.qud:
                new_state.control.next_speaker = new_state.agent_id
            else:
                new_state.control.next_speaker = "user"

    return new_state


def _integrate_assertion(state: InformationState) -> InformationState:
    """Integrate an 'assert' move by adding to commitments.

    Assertions are added to the shared commitment store.
    """
    new_state = state.clone()
    move = new_state.private.beliefs.get("_temp_move")

    if not isinstance(move, DialogueMove):
        return new_state

    # Add assertion to commitments
    if move.content:
        new_state.shared.commitments.add(str(move.content))

    # Add to last_moves
    new_state.shared.last_moves.append(move)

    # Switch turn
    if move.speaker != new_state.agent_id:
        new_state.control.next_speaker = new_state.agent_id
    else:
        new_state.control.next_speaker = "user"

    return new_state


def _integrate_greet(state: InformationState) -> InformationState:
    """Integrate a 'greet' move by updating control state.

    Greetings typically prompt a greeting response.
    """
    new_state = state.clone()
    move = new_state.private.beliefs.get("_temp_move")

    if not isinstance(move, DialogueMove):
        return new_state

    # Add to last_moves
    new_state.shared.last_moves.append(move)

    # Set dialogue to active
    new_state.control.dialogue_state = "active"

    # Switch turn
    if move.speaker != new_state.agent_id:
        # User greeted, system should respond
        new_state.control.next_speaker = new_state.agent_id
        # Add a greeting to agenda
        greeting_move = DialogueMove(
            move_type="greet",
            content="greeting_response",
            speaker=new_state.agent_id,
        )
        new_state.private.agenda.append(greeting_move)
    else:
        new_state.control.next_speaker = "user"

    return new_state


def _integrate_quit(state: InformationState) -> InformationState:
    """Integrate a 'quit' move by ending the dialogue.

    Quit moves set the dialogue state to 'ended'.
    """
    new_state = state.clone()
    move = new_state.private.beliefs.get("_temp_move")

    if not isinstance(move, DialogueMove):
        return new_state

    # Add to last_moves
    new_state.shared.last_moves.append(move)

    # End the dialogue
    new_state.control.dialogue_state = "ended"

    # If user quit, system should acknowledge
    if move.speaker != new_state.agent_id:
        new_state.control.next_speaker = new_state.agent_id
        # Add a quit response to agenda
        quit_move = DialogueMove(
            move_type="quit",
            content="quit_response",
            speaker=new_state.agent_id,
        )
        new_state.private.agenda.append(quit_move)
    else:
        new_state.control.next_speaker = "user"

    return new_state


def _reaccommodate_question(state: InformationState) -> InformationState:
    """Re-raise question to private.issues when user provides conflicting answer.

    IBiS3 Rule 4.6 (QuestionReaccommodation / accommodate Com 2Issues):
    When user changes their mind and provides a new answer that conflicts with
    an existing commitment, re-raise the question to private.issues so it can
    be asked again and the new answer can be integrated.

    This implements simple belief revision - the question is reopened for
    discussion when conflicting information is provided.

    Args:
        state: Current information state

    Returns:
        New state with question re-raised to private.issues

    Larsson (2002) Section 4.6.6 - QuestionReaccommodation.
    """
    new_state = state.clone()

    # Get the question that needs reaccommodation (set by precondition)
    question = new_state.private.beliefs.get("_reaccommodate_question")
    if not question:
        return new_state

    # Re-raise question to private.issues
    # Check if not already there (avoid duplicates)
    if question not in new_state.private.issues:
        new_state.private.issues.append(question)

    # Note: The old commitment will be retracted by Rule 4.7
    # The new answer will be integrated by integrate_answer

    return new_state


def _retract_commitment(state: InformationState) -> InformationState:
    """Retract incompatible commitment before integrating new answer.

    IBiS3 Rule 4.7 (Retract):
    When user provides a conflicting answer, remove the old incompatible
    commitment from shared commitments. This implements simple belief revision.

    Args:
        state: Current information state

    Returns:
        New state with old commitment removed

    Larsson (2002) Section 4.6.6 - part of reaccommodation process.
    """
    new_state = state.clone()

    # Get the old commitment to retract (set by Rule 4.6 precondition)
    old_commitment = new_state.private.beliefs.get("_reaccommodate_old_commitment")
    if not old_commitment:
        return new_state

    # Remove the old commitment
    if old_commitment in new_state.shared.commitments:
        new_state.shared.commitments.remove(old_commitment)

    # Clear the marker (commitment has been retracted)
    new_state.private.beliefs["_reaccommodate_old_commitment"] = None

    return new_state


def _reaccommodate_dependent_questions(state: InformationState) -> InformationState:
    """Re-raise dependent questions when base question is reaccommodated.

    IBiS3 Rule 4.8 (DependentQuestionReaccommodation / accommodate Com 2Issues Dependent):
    When a question is reaccommodated due to a changed answer, also reaccommodate
    any questions that depend on it. This ensures dependent information is also
    re-evaluated.

    Example:
        User changes travel class from "economy" to "business"
        → Price question depends on class
        → Both class and price questions are reaccommodated

    Args:
        state: Current information state

    Returns:
        New state with dependent questions re-raised to private.issues

    Larsson (2002) Section 4.6.6 - dependent question reaccommodation.
    """
    new_state = state.clone()

    # Get the question that's being reaccommodated
    reaccommodate_question = new_state.private.beliefs.get("_reaccommodate_question")
    if not reaccommodate_question:
        return new_state

    domain = _get_active_domain(new_state)

    # Find all questions that depend on the reaccommodated question
    # and retract their commitments, then re-raise them
    commitments_to_retract: list[str] = []
    questions_to_reaccommodate: list[Question] = []

    for commitment in new_state.shared.commitments:
        question = domain.get_question_from_commitment(commitment)
        if not question:
            continue

        # Check if this question depends on the reaccommodated question
        if domain.depends(question, reaccommodate_question):
            commitments_to_retract.append(commitment)
            questions_to_reaccommodate.append(question)

    # Retract dependent commitments
    for commitment_to_retract in commitments_to_retract:
        if commitment_to_retract in new_state.shared.commitments:
            new_state.shared.commitments.remove(commitment_to_retract)

    # Re-raise dependent questions to issues
    for question_to_reaccommodate in questions_to_reaccommodate:
        if question_to_reaccommodate not in new_state.private.issues:
            new_state.private.issues.append(question_to_reaccommodate)

    return new_state
