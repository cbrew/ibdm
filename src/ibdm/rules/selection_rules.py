"""Selection rules for Issue-Based Dialogue Management.

Selection rules choose the next system action based on the information state.
They implement strategies for answering, raising questions, etc.

Based on Larsson (2002) Issue-based Dialogue Management, Chapter 2, Section 2.9.
Implements IBiS1 selection rules and IBiS2 ICM (grounding) selection rules.
"""

from ibdm.core import Answer, DialogueMove, InformationState, WhQuestion
from ibdm.core.grounding import GroundingStrategy, requires_confirmation, select_grounding_strategy
from ibdm.core.moves import (
    create_icm_acceptance_positive,
    create_icm_perception_negative,
    create_icm_understanding_interrogative,
)
from ibdm.rules.update_rules import UpdateRule


def create_selection_rules() -> list[UpdateRule]:
    """Create IBiS1 and IBiS2 selection rules.

    Implements the selection rules from Larsson (2002):

    IBiS1 Rules (Section 2.9):
    1. SelectClarification (Section 3.4) - Request clarification for invalid answer
    2. SelectFromPlan (Section 2.9.1) - Select action from plan
    3. SelectAnswer (Section 2.9.4) - Answer top QUD question
    4. SelectAsk (Section 2.9.2) - Ask top QUD question
    5. SelectGreet (Section 2.9) - Greet at dialogue start
    6. Fallback - Generic response

    IBiS2 ICM Rules (Section 3.6):
    7. SelectPerceptionCheck (Rule 3.6) - Request perception check for low confidence
    8. SelectUnderstandingConfirmation (Rule 3.7) - Request understanding confirmation
    9. SelectAcceptance (Rule 3.8) - Provide acceptance feedback

    Returns:
        List of selection rules
    """
    return [
        # Rule: SelectClarification (Section 3.4 - Accommodation)
        # Pre: Invalid answer received, clarification needed
        # Effect: add(shared.next_moves, icm:clarify(Q))
        UpdateRule(
            name="select_clarification",
            preconditions=_needs_clarification,
            effects=_select_clarification,
            priority=25,  # Highest - must handle invalid input first
            rule_type="selection",
        ),
        # IBiS3 Rule 4.4: DependentIssueAccommodation - push prerequisite questions
        # Pre: top(QUD) depends on unanswered question
        # Effect: push prerequisite question to QUD
        UpdateRule(
            name="accommodate_dependent_question",
            preconditions=_has_unanswered_dependency,
            effects=_accommodate_dependency,
            priority=22,  # Before raise (20) and ask (10)
            rule_type="selection",
        ),
        # IBiS3 Rule 4.2: LocalQuestionAccommodation - raise issues to QUD
        # Pre: private.issues not empty AND QUD is empty
        # Effect: raise first issue to QUD
        UpdateRule(
            name="raise_accommodated_question",
            preconditions=_has_raisable_issue,
            effects=_raise_issue_to_qud,
            priority=20,  # High priority - before other selection
            rule_type="selection",
        ),
        # Rule: SelectFromPlan (Section 2.9.1)
        # Pre: head(private.plan) is a communicative action
        # Effect: add(shared.next_moves, head(private.plan))
        UpdateRule(
            name="select_from_plan",
            preconditions=_has_communicative_plan,
            effects=_select_plan_action,
            priority=20,
            rule_type="selection",
        ),
        # Rule: SelectAnswer (Section 2.9.4)
        # Pre: top(shared.qud) == Q AND system can answer Q
        # Effect: add(shared.next_moves, answer(answer))
        UpdateRule(
            name="select_answer",
            preconditions=_can_answer_qud,
            effects=_select_answer_to_qud,
            priority=15,
            rule_type="selection",
        ),
        # Rule: SelectAsk (Section 2.9.2)
        # Pre: top(shared.qud) == Q AND system needs to ask Q
        # Effect: add(shared.next_moves, ask(Q))
        UpdateRule(
            name="select_ask",
            preconditions=_should_ask_qud,
            effects=_select_ask_qud,
            priority=10,
            rule_type="selection",
        ),
        # Rule: SelectGreet (Section 2.9)
        # Pre: Dialogue start, no greeting yet
        # Effect: add(shared.next_moves, greet())
        UpdateRule(
            name="select_greet",
            preconditions=_should_greet,
            effects=_select_greeting,
            priority=5,
            rule_type="selection",
        ),
        # IBiS2 Rule 3.6: SelectPerceptionCheck
        # Pre: User utterance has very low confidence (pessimistic grounding)
        # Effect: add(shared.next_moves, icm:per*neg) - request repetition
        UpdateRule(
            name="select_perception_check",
            preconditions=_needs_perception_check,
            effects=_select_perception_check,
            priority=18,  # High - perception check before other moves
            rule_type="selection",
        ),
        # IBiS2 Rule 3.7: SelectUnderstandingConfirmation
        # Pre: User utterance has medium confidence (cautious grounding)
        # Effect: add(shared.next_moves, icm:und*int) - request confirmation
        UpdateRule(
            name="select_understanding_confirmation",
            preconditions=_needs_understanding_confirmation,
            effects=_select_understanding_confirmation,
            priority=17,  # High - confirmation before processing answer
            rule_type="selection",
        ),
        # IBiS2 Rule 3.8: SelectAcceptance
        # Pre: User utterance has high confidence (optimistic grounding)
        # Effect: add(shared.next_moves, icm:acc*pos) - acknowledge acceptance
        UpdateRule(
            name="select_acceptance",
            preconditions=_should_give_acceptance,
            effects=_select_acceptance,
            priority=12,  # Medium - acceptance after processing content
            rule_type="selection",
        ),
        # IBiS2 Rule 3.2: SelectIcmOther
        # Pre: ICM move on agenda
        # Effect: Move ICM from agenda to next_moves
        UpdateRule(
            name="select_icm_other",
            preconditions=_has_icm_on_agenda,
            effects=_select_icm_from_agenda,
            priority=16,  # High - ICM should be selected promptly
            rule_type="selection",
        ),
        # IBiS2 Rule 3.3: SelectIcmUndIntAsk
        # Pre: User ask-move with low confidence on last_moves
        # Effect: Select interrogative understanding feedback (icm:und*int)
        UpdateRule(
            name="select_icm_und_int_ask",
            preconditions=_needs_understanding_confirmation_for_ask,
            effects=_select_understanding_confirmation_ask,
            priority=19,  # Very high - confirm before processing
            rule_type="selection",
        ),
        # IBiS2 Rule 3.5: SelectIcmUndIntAnswer
        # Pre: User answer-move with low confidence on last_moves
        # Effect: Select interrogative understanding feedback (icm:und*int)
        UpdateRule(
            name="select_icm_und_int_answer",
            preconditions=_needs_understanding_confirmation_for_answer,
            effects=_select_understanding_confirmation_answer,
            priority=19,  # Very high - confirm before processing
            rule_type="selection",
        ),
        # IBiS2 Rule 3.25: ReraiseIssue
        # Pre: Communication failure, need to re-ask question
        # Effect: Re-raise question to QUD after failure
        UpdateRule(
            name="reraise_issue",
            preconditions=_needs_issue_reraised,
            effects=_reraise_failed_issue,
            priority=13,  # Medium-high - handle failures
            rule_type="selection",
        ),
        # Fallback: Generic response if nothing else applies
        # Only fires when no other rule has selected an action
        UpdateRule(
            name="select_fallback",
            preconditions=lambda state: len(state.private.agenda) == 0,
            effects=_select_fallback_response,
            priority=1,
            rule_type="selection",
        ),
    ]


# Precondition functions (IBiS1)


def _has_unanswered_dependency(state: InformationState) -> bool:
    """Check if top QUD question has unanswered dependencies.

    IBiS3 Rule 4.4 (DependentIssueAccommodation):
    If the question on top of QUD depends on other questions that haven't
    been answered yet, we need to ask those prerequisite questions first.

    Preconditions:
    - There's a question on QUD
    - That question depends on at least one other question (domain knowledge)
    - The prerequisite question hasn't been answered yet (not in commitments)

    Larsson (2002) Section 4.6.4 - DependentIssueAccommodation rule.
    """
    # Don't trigger if there's already something on the agenda
    if state.private.agenda:
        return False

    # Need a question on QUD
    top_question = state.shared.top_qud()
    if not top_question:
        return False

    # Check if this question has dependencies via domain model
    # We need to get the domain model from somewhere - let's check beliefs
    domain = state.private.beliefs.get("_domain")
    if not domain:
        return False  # No domain model available

    # Get dependencies for this question
    dependency_predicates = domain.get_dependencies(top_question)
    if not dependency_predicates:
        return False  # No dependencies

    # Check if any dependency is unanswered
    for dep_predicate in dependency_predicates:
        # Check if we have this predicate in commitments or beliefs
        answered = False
        for key in state.private.beliefs:
            if dep_predicate in key.lower() and state.private.beliefs[key]:
                answered = True
                break

        # If any dependency is unanswered, we need to accommodate it
        if not answered:
            return True

    return False


def _has_raisable_issue(state: InformationState) -> bool:
    """Check if there are issues that can be raised to QUD.

    An issue can be raised if:
    - There are issues in private.issues
    - QUD is empty or current QUD is not blocking
    - Context is appropriate for asking a new question

    Larsson (2002) Section 4.6.2 - LocalQuestionAccommodation rule.
    """
    # Need at least one issue to raise
    if not state.private.issues:
        return False

    # For now, simple strategy: raise if QUD is empty
    # Future: more sophisticated context checking
    if not state.shared.qud:
        return True

    return False


def _needs_clarification(state: InformationState) -> bool:
    """Check if clarification is needed for invalid answer.

    IBiS2 Rule: SelectClarification (Section 3.4 - Accommodation)
    Pre: Invalid answer received, needs clarification

    Note: If Rule 4.3 (IssueClarification) has already pushed a clarification
    question to QUD, don't use this ICM-based clarification. Let SelectAsk
    handle asking the clarification question from QUD instead.
    """
    # Don't trigger if there's already something on the agenda
    if state.private.agenda:
        return False

    # Don't trigger if Rule 4.3 has already pushed clarification question to QUD
    top_qud = state.shared.top_qud()
    if top_qud:
        constraints = getattr(top_qud, "constraints", {})
        if constraints.get("is_clarification"):
            # Clarification question already on QUD - let SelectAsk handle it
            return False

    # Check if clarification marker is set
    return state.private.beliefs.get("_needs_clarification", False)


def _has_communicative_plan(state: InformationState) -> bool:
    """Check if head of private.plan is a communicative action.

    IBiS1 Rule: SelectFromPlan (Section 2.9.1)
    Pre: head(private.plan) is a communicative action
    """
    # Don't trigger if there's already something on the agenda
    if state.private.agenda:
        return False

    # Check if there's a plan at the head
    if not state.private.plan:
        return False

    # Get the head (first) plan
    head_plan = state.private.plan[0]

    # Check if it's active and is a communicative action
    # Communicative actions include: findout, raise, inform, greet
    if not head_plan.is_active():
        return False

    communicative_types = ["findout", "raise", "inform", "greet", "ask", "answer"]
    return head_plan.plan_type in communicative_types


def _can_answer_qud(state: InformationState) -> bool:
    """Check if system can answer the top QUD from beliefs.

    IBiS1 Rule: SelectAnswer (Section 2.9.4)
    Pre: top(shared.qud) == Q AND system can answer Q
    """
    # Don't trigger if there's already something on the agenda
    if state.private.agenda:
        return False

    if not state.shared.qud:
        return False

    top_question = state.shared.top_qud()

    # Check if we have an answer in our beliefs
    if isinstance(top_question, WhQuestion):
        # Look for a belief that matches the predicate
        predicate_key = top_question.predicate.lower()
        # Check if any belief key contains relevant words
        for key in state.private.beliefs:
            if predicate_key in key.lower() or key.lower() in predicate_key:
                return True

    # For other question types, check for direct answer
    # (This is where domain knowledge would be integrated)
    return False


def _should_ask_qud(state: InformationState) -> bool:
    """Check if system should ask the top QUD question.

    IBiS1 Rule: SelectAsk (Section 2.9.2)
    Pre: top(shared.qud) == Q AND system needs to ask Q

    System asks a question when:
    - There's a question on QUD
    - System doesn't have the answer
    - Question hasn't been asked yet
    """
    # Don't trigger if there's already something on the agenda
    if state.private.agenda:
        return False

    if not state.shared.qud:
        return False

    # If we can answer, SelectAnswer should fire instead
    if _can_answer_qud(state):
        return False

    # System should ask the question
    return True


def _should_greet(state: InformationState) -> bool:
    """Check if system should greet at dialogue start.

    IBiS1 Rule: SelectGreet (Section 2.9)
    Pre: Dialogue start, no greeting yet
    """
    # Don't trigger if there's already something on the agenda
    if state.private.agenda:
        return False

    # Check if dialogue is just starting
    if state.control.dialogue_state != "active":
        return False

    # Check if no moves have been made yet or only user greeting
    if not state.shared.last_moves:
        return True

    # Check if last move was a user greeting and system hasn't responded
    if state.shared.last_moves:
        last_move = state.shared.last_moves[-1]
        if last_move.move_type == "greet" and last_move.speaker != state.agent_id:
            # Check if system has already greeted back
            for move in state.shared.last_moves:
                if move.speaker == state.agent_id and move.move_type == "greet":
                    return False
            return True

    return False


# Effect functions (IBiS1)


def _accommodate_dependency(state: InformationState) -> InformationState:
    """Accommodate prerequisite question to QUD.

    IBiS3 Rule 4.4 (DependentIssueAccommodation):
    When the top QUD question depends on unanswered questions, push the
    first prerequisite question to QUD. This suspends the dependent question
    until the prerequisite is answered.

    Args:
        state: Current information state

    Returns:
        New state with prerequisite question on QUD

    Larsson (2002) Section 4.6.4 - DependentIssueAccommodation rule.
    """
    from ibdm.core import WhQuestion

    new_state = state.clone()

    # Get top question
    top_question = new_state.shared.top_qud()
    if not top_question:
        return new_state

    # Get domain model
    domain = new_state.private.beliefs.get("_domain")
    if not domain:
        return new_state

    # Get dependencies
    dependency_predicates = domain.get_dependencies(top_question)
    if not dependency_predicates:
        return new_state

    # Find first unanswered dependency
    for dep_predicate in dependency_predicates:
        # Check if answered
        answered = False
        for key in new_state.private.beliefs:
            if dep_predicate in key.lower() and new_state.private.beliefs[key]:
                answered = True
                break

        # If unanswered, create and push question for it
        if not answered:
            # Create WhQuestion for the dependency
            prerequisite_question = WhQuestion(
                variable="X",
                predicate=dep_predicate,
                constraints={
                    "is_prerequisite": True,
                    "for_question": str(top_question),
                },
            )

            # Push prerequisite to QUD (suspends dependent question below)
            new_state.shared.push_qud(prerequisite_question)

            # Only accommodate one dependency at a time
            break

    return new_state


def _raise_issue_to_qud(state: InformationState) -> InformationState:
    """Raise first issue from private.issues to shared.qud.

    IBiS3 Rule 4.2 (LocalQuestionAccommodation):
    When context is appropriate, raise accommodated questions
    to QUD so they can be asked. This implements incremental
    questioning - we don't dump all questions at once.

    Args:
        state: Current information state

    Returns:
        New state with first issue raised to QUD

    Larsson (2002) Section 4.6.2 - LocalQuestionAccommodation rule.
    """
    new_state = state.clone()

    # Pop first issue from private.issues
    if new_state.private.issues:
        question = new_state.private.issues.pop(0)

        # Push to QUD
        new_state.shared.push_qud(question)

    return new_state


def _select_clarification(state: InformationState) -> InformationState:
    """Select clarification request for invalid answer.

    IBiS3 Rule: SelectClarification (Section 3.4 - Accommodation)
    Effect: add(shared.next_moves, icm:clarify(Q))

    Creates an ICM (Interactive Communication Management) move requesting
    clarification about the invalid answer.
    """
    new_state = state.clone()

    # Get the question that needs clarification
    question = new_state.private.beliefs.get("_clarification_question")
    invalid_answer = new_state.private.beliefs.get("_invalid_answer")

    # Create ICM clarification move
    # ICM moves have format "icm:<subtype>" for move_type
    # Content is a dict with clarification details
    clarification_content = {
        "icm_type": "clarify",
        "question": question,
        "invalid_answer": invalid_answer,
        "message": "I didn't understand that answer. Could you please provide a valid response?",
    }

    move = DialogueMove(
        move_type="icm",
        content=clarification_content,
        speaker=new_state.agent_id,
        metadata={"icm_subtype": "clarify"},
    )
    new_state.private.agenda.append(move)

    # Clear the clarification markers
    new_state.private.beliefs["_needs_clarification"] = False
    new_state.private.beliefs.pop("_invalid_answer", None)
    new_state.private.beliefs.pop("_clarification_question", None)

    return new_state


def _select_plan_action(state: InformationState) -> InformationState:
    """Select action from head of plan.

    IBiS1 Rule: SelectFromPlan (Section 2.9.1)
    Effect: add(shared.next_moves, head(private.plan))

    Converts the head plan into a dialogue move and adds to agenda.
    """
    new_state = state.clone()

    if not new_state.private.plan:
        return new_state

    # Get the head (first) plan
    head_plan = new_state.private.plan[0]

    # Convert plan to dialogue move based on plan type
    if head_plan.plan_type == "findout":
        # Findout plan: create ask move with question
        move = DialogueMove(
            move_type="ask",
            content=head_plan.content,
            speaker=new_state.agent_id,
        )
    elif head_plan.plan_type == "inform":
        # Inform plan: create assert move
        move = DialogueMove(
            move_type="assert",
            content=head_plan.content,
            speaker=new_state.agent_id,
        )
    elif head_plan.plan_type == "greet":
        # Greet plan: create greet move
        move = DialogueMove(
            move_type="greet",
            content="greeting",
            speaker=new_state.agent_id,
        )
    else:
        # Default: treat as assertion
        move = DialogueMove(
            move_type="assert",
            content=head_plan.content,
            speaker=new_state.agent_id,
        )

    # Add to agenda
    new_state.private.agenda.append(move)

    # Mark head plan as completed
    head_plan.complete()

    return new_state


def _select_answer_to_qud(state: InformationState) -> InformationState:
    """Select answer to top QUD question.

    IBiS1 Rule: SelectAnswer (Section 2.9.4)
    Effect: add(shared.next_moves, answer(answer))
    """
    new_state = state.clone()

    top_question = new_state.shared.top_qud()
    if not top_question:
        return new_state

    # Retrieve answer from beliefs
    answer_content = None
    if isinstance(top_question, WhQuestion):
        predicate_key = top_question.predicate.lower()
        for key, value in new_state.private.beliefs.items():
            if predicate_key in key.lower() or key.lower() in predicate_key:
                answer_content = value
                break

    if answer_content is not None:
        answer = Answer(content=answer_content, question_ref=top_question)
        move = DialogueMove(
            move_type="answer",
            content=answer,
            speaker=new_state.agent_id,
        )
        new_state.private.agenda.append(move)

    return new_state


def _select_ask_qud(state: InformationState) -> InformationState:
    """Select ask move for top QUD question.

    IBiS1 Rule: SelectAsk (Section 2.9.2)
    Effect: add(shared.next_moves, ask(Q))
    """
    new_state = state.clone()

    top_question = new_state.shared.top_qud()
    if not top_question:
        return new_state

    # Create ask move with the question
    move = DialogueMove(
        move_type="ask",
        content=top_question,
        speaker=new_state.agent_id,
    )
    new_state.private.agenda.append(move)

    return new_state


def _select_greeting(state: InformationState) -> InformationState:
    """Select greeting move.

    IBiS1 Rule: SelectGreet (Section 2.9)
    Effect: add(shared.next_moves, greet())
    """
    new_state = state.clone()

    # Create greeting move
    move = DialogueMove(
        move_type="greet",
        content="greeting_response",
        speaker=new_state.agent_id,
    )
    new_state.private.agenda.append(move)

    return new_state


def _select_fallback_response(state: InformationState) -> InformationState:
    """Select fallback response when no other rule applies.

    This is not part of IBiS1 but provides a safety net.
    """
    new_state = state.clone()

    # Create a simple acknowledgment
    move = DialogueMove(
        move_type="assert",
        content="I understand.",
        speaker=new_state.agent_id,
    )
    new_state.private.agenda.append(move)

    return new_state


# IBiS2 ICM Selection - Precondition functions


def _needs_perception_check(state: InformationState) -> bool:
    """Check if perception check is needed for low confidence utterance.

    IBiS2 Rule 3.6: SelectPerceptionCheck
    Pre: User utterance has very low confidence (< 0.5)
         Grounding strategy is PESSIMISTIC

    Args:
        state: Current information state

    Returns:
        True if perception check should be requested
    """
    # Don't trigger if there's already something on the agenda
    if state.private.agenda:
        return False

    # Check if last move has low confidence
    if not state.shared.last_moves:
        return False

    last_move = state.shared.last_moves[-1]

    # Only check user moves
    if last_move.speaker == state.agent_id:
        return False

    # Check confidence score in metadata
    confidence = last_move.metadata.get("confidence", 1.0)

    # Determine if we need perception check
    strategy = select_grounding_strategy(last_move.move_type, confidence)

    return strategy == GroundingStrategy.PESSIMISTIC


def _needs_understanding_confirmation(state: InformationState) -> bool:
    """Check if understanding confirmation is needed for medium confidence utterance.

    IBiS2 Rule 3.7: SelectUnderstandingConfirmation
    Pre: User utterance has medium confidence (0.5-0.7)
         OR requires confirmation (e.g., quit, request)
         Grounding strategy is CAUTIOUS

    Args:
        state: Current information state

    Returns:
        True if understanding confirmation should be requested
    """
    # Don't trigger if there's already something on the agenda
    if state.private.agenda:
        return False

    # Check if last move needs confirmation
    if not state.shared.last_moves:
        return False

    last_move = state.shared.last_moves[-1]

    # Only check user moves
    if last_move.speaker == state.agent_id:
        return False

    # Check confidence score
    confidence = last_move.metadata.get("confidence", 1.0)

    # Check if move type requires confirmation or has medium confidence
    needs_confirm = requires_confirmation(last_move.move_type, confidence)
    strategy = select_grounding_strategy(last_move.move_type, confidence)

    return needs_confirm or strategy == GroundingStrategy.CAUTIOUS


def _should_give_acceptance(state: InformationState) -> bool:
    """Check if acceptance feedback should be given for high confidence utterance.

    IBiS2 Rule 3.8: SelectAcceptance
    Pre: User utterance has high confidence (>= 0.7)
         Grounding strategy is OPTIMISTIC
         Content has been successfully integrated

    Args:
        state: Current information state

    Returns:
        True if acceptance feedback should be provided
    """
    # Don't trigger if there's already something on the agenda
    if state.private.agenda:
        return False

    # Check if last move has high confidence
    if not state.shared.last_moves:
        return False

    last_move = state.shared.last_moves[-1]

    # Only check user moves
    if last_move.speaker == state.agent_id:
        return False

    # Don't give acceptance for greetings (handled by greet rule)
    if last_move.move_type == "greet":
        return False

    # Check confidence score
    confidence = last_move.metadata.get("confidence", 1.0)

    # Determine if we should give acceptance
    strategy = select_grounding_strategy(last_move.move_type, confidence)

    # Only give acceptance for optimistic grounding and substantive moves
    return strategy == GroundingStrategy.OPTIMISTIC and last_move.move_type in [
        "answer",
        "assert",
        "request",
    ]


# IBiS2 ICM Selection - Effect functions


def _select_perception_check(state: InformationState) -> InformationState:
    """Select perception check ICM move (icm:per*neg).

    IBiS2 Rule 3.6: SelectPerceptionCheck
    Effect: add(shared.next_moves, icm:per*neg)

    Request the user to repeat their utterance due to low confidence.

    Args:
        state: Current information state

    Returns:
        Updated state with perception check move on agenda
    """
    new_state = state.clone()

    # Get index of last move for target reference
    target_index = len(new_state.shared.moves) - 1 if new_state.shared.moves else None

    # Create perception negative ICM move
    move = create_icm_perception_negative(
        content="Pardon? I didn't quite catch that.",
        speaker=new_state.agent_id,
        target_move_index=target_index,
    )

    new_state.private.agenda.append(move)

    return new_state


def _select_understanding_confirmation(state: InformationState) -> InformationState:
    """Select understanding confirmation ICM move (icm:und*int).

    IBiS2 Rule 3.7: SelectUnderstandingConfirmation
    Effect: add(shared.next_moves, icm:und*int)

    Request confirmation of understanding for medium confidence utterance.

    Args:
        state: Current information state

    Returns:
        Updated state with understanding confirmation move on agenda
    """
    new_state = state.clone()

    if not new_state.shared.last_moves:
        return new_state

    last_move = new_state.shared.last_moves[-1]

    # Get index of last move for target reference
    target_index = len(new_state.shared.moves) - 1 if new_state.shared.moves else None

    # Create understanding interrogative ICM move
    # Content should be reformulation of what was understood
    content_str = str(last_move.content) if last_move.content else "that"
    confirmation_text = f"{content_str}, is that correct?"

    move = create_icm_understanding_interrogative(
        content=confirmation_text,
        speaker=new_state.agent_id,
        target_move_index=target_index,
    )

    new_state.private.agenda.append(move)

    return new_state


def _select_acceptance(state: InformationState) -> InformationState:
    """Select acceptance ICM move (icm:acc*pos).

    IBiS2 Rule 3.8: SelectAcceptance
    Effect: add(shared.next_moves, icm:acc*pos)

    Provide acceptance feedback for high confidence utterance.

    Args:
        state: Current information state

    Returns:
        Updated state with acceptance move on agenda
    """
    new_state = state.clone()

    # Get index of last move for target reference
    target_index = len(new_state.shared.moves) - 1 if new_state.shared.moves else None

    # Create acceptance positive ICM move
    move = create_icm_acceptance_positive(
        content="Okay",
        speaker=new_state.agent_id,
        target_move_index=target_index,
    )

    new_state.private.agenda.append(move)

    return new_state


# IBiS2 Rule 3.2, 3.3, 3.5 functions


def _has_icm_on_agenda(state: InformationState) -> bool:
    """Check if there's an ICM move on the agenda.

    IBiS2 Rule 3.2: SelectIcmOther
    Pre: ICM move on agenda that hasn't been selected yet

    Args:
        state: Current information state

    Returns:
        True if agenda has ICM move
    """
    return any(move.is_icm() for move in state.private.agenda)


def _select_icm_from_agenda(state: InformationState) -> InformationState:
    """Move ICM from agenda to next_moves.

    IBiS2 Rule 3.2: SelectIcmOther
    Effect: push(nextmoves, icm:A), del(/private/agenda, icm:A)

    Args:
        state: Current information state

    Returns:
        Updated state with ICM moved from agenda to next_moves
    """
    new_state = state.clone()

    # Find first ICM move on agenda
    for i, move in enumerate(new_state.private.agenda):
        if move.is_icm():
            # Remove from agenda and add to next_moves
            icm_move = new_state.private.agenda.pop(i)
            new_state.private.agenda.insert(0, icm_move)  # Move to front for selection
            break

    return new_state


def _needs_understanding_confirmation_for_ask(state: InformationState) -> bool:
    """Check if user ask-move needs understanding confirmation.

    IBiS2 Rule 3.3: SelectIcmUndIntAsk
    Pre: User ask-move with low/medium confidence AND no agenda

    Args:
        state: Current information state

    Returns:
        True if last move is ask with low confidence
    """
    # Don't apply if there's already something on the agenda
    if state.private.agenda:
        return False

    if not state.shared.last_moves:
        return False

    last_move = state.shared.last_moves[-1]

    # Check if it's a user ask move
    if last_move.move_type != "ask" or last_move.speaker == state.agent_id:
        return False

    # Check confidence (if available)
    confidence = last_move.metadata.get("confidence", 0.8)  # Default medium-high
    # Request confirmation if confidence is low/medium (< 0.7)
    return confidence < 0.7


def _select_understanding_confirmation_ask(state: InformationState) -> InformationState:
    """Select interrogative understanding feedback for ask.

    IBiS2 Rule 3.3: SelectIcmUndIntAsk
    Effect: push(nextmoves, icm:und*int:usr*issue(Q))

    Args:
        state: Current information state

    Returns:
        Updated state with understanding confirmation on agenda
    """
    new_state = state.clone()
    last_move = new_state.shared.last_moves[-1]

    # Get index for target reference
    target_index = len(new_state.shared.moves) - 1 if new_state.shared.moves else None

    # Create understanding interrogative ICM move
    question_content = str(last_move.content) if last_move.content else "that question"
    confirmation_text = f"{question_content}, is that what you're asking?"

    move = create_icm_understanding_interrogative(
        content=confirmation_text,
        speaker=new_state.agent_id,
        target_move_index=target_index,
    )

    new_state.private.agenda.append(move)

    return new_state


def _needs_understanding_confirmation_for_answer(state: InformationState) -> bool:
    """Check if user answer-move needs understanding confirmation.

    IBiS2 Rule 3.5: SelectIcmUndIntAnswer
    Pre: User answer-move with low/medium confidence AND no agenda

    Args:
        state: Current information state

    Returns:
        True if last move is answer with low confidence
    """
    # Don't apply if there's already something on the agenda
    if state.private.agenda:
        return False

    if not state.shared.last_moves:
        return False

    last_move = state.shared.last_moves[-1]

    # Check if it's a user answer move
    if last_move.move_type != "answer" or last_move.speaker == state.agent_id:
        return False

    # Check confidence (if available)
    confidence = last_move.metadata.get("confidence", 0.8)  # Default medium-high
    # Request confirmation if confidence is low/medium (< 0.7)
    return confidence < 0.7


def _select_understanding_confirmation_answer(state: InformationState) -> InformationState:
    """Select interrogative understanding feedback for answer.

    IBiS2 Rule 3.5: SelectIcmUndIntAnswer
    Effect: push(nextmoves, icm:und*int:usr*C)

    Args:
        state: Current information state

    Returns:
        Updated state with understanding confirmation on agenda
    """
    new_state = state.clone()
    last_move = new_state.shared.last_moves[-1]

    # Get index for target reference
    target_index = len(new_state.shared.moves) - 1 if new_state.shared.moves else None

    # Create understanding interrogative ICM move
    answer_content = str(last_move.content) if last_move.content else "that"
    confirmation_text = f"{answer_content}, is that correct?"

    move = create_icm_understanding_interrogative(
        content=confirmation_text,
        speaker=new_state.agent_id,
        target_move_index=target_index,
    )

    new_state.private.agenda.append(move)

    return new_state


# IBiS2 Rule 3.25 functions


def _needs_issue_reraised(state: InformationState) -> bool:
    """Check if an issue needs to be re-raised after failure.

    IBiS2 Rule 3.25: ReraiseIssue
    Pre: Communication failure for a question, need to re-ask

    Args:
        state: Current information state

    Returns:
        True if issue needs to be re-raised
    """
    # Check if beliefs indicate a failed question that needs re-raising
    if "needs_reutterance" in state.private.beliefs and state.private.beliefs["needs_reutterance"]:
        # Check if there's a rejected interpretation
        if "rejected_interpretation" in state.private.beliefs:
            return True

    return False


def _reraise_failed_issue(state: InformationState) -> InformationState:
    """Re-raise question after communication failure.

    IBiS2 Rule 3.25: ReraiseIssue
    Effect: Re-ask the question that failed

    Args:
        state: Current information state

    Returns:
        Updated state with question re-raised
    """
    new_state = state.clone()

    # Get the rejected interpretation
    rejected_content = new_state.private.beliefs.get("rejected_interpretation", "")

    # Clear the failure flags
    new_state.private.beliefs["needs_reutterance"] = False
    new_state.private.beliefs.pop("rejected_interpretation", None)

    # Try to create a clarification question
    from ibdm.core import WhQuestion
    from ibdm.core.moves import DialogueMove

    # Create a clarification request
    clarification = DialogueMove(
        move_type="ask",
        content=WhQuestion(variable="x", predicate=f"clarify_{rejected_content}"),
        speaker=new_state.agent_id,
    )

    new_state.private.agenda.append(clarification)

    return new_state
