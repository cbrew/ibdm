"""ICM Integration rules for Issue-Based Dialogue Management.

ICM (Interactive Communication Management) integration rules handle grounding
feedback moves. They update the information state based on perception,
understanding, and acceptance feedback.

Based on Larsson (2002) Section 3.6 - ICM Update Rules.
"""

from ibdm.core import Answer, InformationState, WhQuestion
from ibdm.core.grounding import ActionLevel
from ibdm.core.moves import Polarity
from ibdm.rules.update_rules import UpdateRule


def create_icm_integration_rules() -> list[UpdateRule]:
    """Create ICM integration rules for IBiS2 grounding.

    Implements Rules 3.1-3.8 from Larsson (2002) Section 3.6:
    - Rule 3.1: IntegrateICM_PerceptionPositive (icm:per*pos)
    - Rule 3.2: IntegrateICM_UnderstandingPositive (icm:und*pos)
    - Rule 3.3: IntegrateICM_AcceptancePositive (icm:acc*pos)
    - Rule 3.4: IntegrateICM_PerceptionNegative (icm:per*neg)
    - Rule 3.5: IntegrateICM_UnderstandingNegative (icm:und*neg)
    - Rule 3.6: IntegrateUndIntICM (icm:und*int → raises und question)
    - Rule 3.7: IntegrateNegIcmAnswer (no → understanding question)
    - Rule 3.8: IntegratePosIcmAnswer (yes → understanding question)

    Returns:
        List of ICM integration rules
    """
    return [
        # Rule 3.1: IntegrateICM_PerceptionPositive
        # Pre: last move is icm:per*pos
        # Effect: Mark target move as perceived (update grounding status)
        UpdateRule(
            name="integrate_icm_perception_positive",
            preconditions=_is_perception_positive_icm,
            effects=_integrate_perception_positive,
            priority=15,  # Before general ICM processing
            rule_type="integration",
        ),
        # Rule 3.2: IntegrateICM_UnderstandingPositive
        # Pre: last move is icm:und*pos
        # Effect: Mark target move as understood
        UpdateRule(
            name="integrate_icm_understanding_positive",
            preconditions=_is_understanding_positive_icm,
            effects=_integrate_understanding_positive,
            priority=15,
            rule_type="integration",
        ),
        # Rule 3.3: IntegrateICM_AcceptancePositive
        # Pre: last move is icm:acc*pos
        # Effect: Add content to commitments (full grounding)
        UpdateRule(
            name="integrate_icm_acceptance_positive",
            preconditions=_is_acceptance_positive_icm,
            effects=_integrate_acceptance_positive,
            priority=15,
            rule_type="integration",
        ),
        # Rule 3.4: IntegrateICM_PerceptionNegative
        # Pre: last move is icm:per*neg
        # Effect: Mark for re-utterance (perception failure)
        UpdateRule(
            name="integrate_icm_perception_negative",
            preconditions=_is_perception_negative_icm,
            effects=_integrate_perception_negative,
            priority=15,
            rule_type="integration",
        ),
        # Rule 3.5: IntegrateICM_UnderstandingNegative
        # Pre: last move is icm:und*neg
        # Effect: Mark for clarification (understanding failure)
        UpdateRule(
            name="integrate_icm_understanding_negative",
            preconditions=_is_understanding_negative_icm,
            effects=_integrate_understanding_negative,
            priority=15,
            rule_type="integration",
        ),
        # Rule 3.6: IntegrateUndIntICM
        # Pre: last move is icm:und*int (interrogative understanding feedback)
        # Effect: Push understanding question to QUD
        UpdateRule(
            name="integrate_und_int_icm",
            preconditions=_is_understanding_interrogative_icm,
            effects=_integrate_understanding_interrogative,
            priority=15,
            rule_type="integration",
        ),
        # Rule 3.7: IntegrateNegIcmAnswer
        # Pre: answer(no) AND top(QUD) is understanding question
        # Effect: Pop understanding question, confirm negative interpretation
        UpdateRule(
            name="integrate_neg_icm_answer",
            preconditions=_is_negative_answer_to_understanding_question,
            effects=_integrate_negative_icm_answer,
            priority=16,  # Higher than regular answer integration
            rule_type="integration",
        ),
        # Rule 3.8: IntegratePosIcmAnswer
        # Pre: answer(yes) AND top(QUD) is understanding question
        # Effect: Pop understanding question, integrate confirmed content
        UpdateRule(
            name="integrate_pos_icm_answer",
            preconditions=_is_positive_answer_to_understanding_question,
            effects=_integrate_positive_icm_answer,
            priority=16,  # Higher than regular answer integration
            rule_type="integration",
        ),
        # Rule 3.10: IntegrateOtherICM
        # Pre: Any other ICM move not handled by specific rules
        # Effect: Track in move history
        UpdateRule(
            name="integrate_other_icm",
            preconditions=_is_unhandled_icm,
            effects=_integrate_other_icm,
            priority=6,  # Low priority - catch-all
            rule_type="integration",
        ),
        # Rule 3.20: IntegrateUsrPerNegICM
        # Pre: User says "what?" (perception negative feedback)
        # Effect: Retract last system utterance, prepare to re-utter
        UpdateRule(
            name="integrate_usr_per_neg_icm",
            preconditions=_is_user_perception_negative,
            effects=_integrate_user_perception_negative,
            priority=17,  # High - handle perception failure immediately
            rule_type="integration",
        ),
        # Rule 3.21: IntegrateUsrAccNegICM
        # Pre: User says "no, that's wrong" (acceptance negative feedback)
        # Effect: Retract from commitments, mark for correction
        UpdateRule(
            name="integrate_usr_acc_neg_icm",
            preconditions=_is_user_acceptance_negative,
            effects=_integrate_user_acceptance_negative,
            priority=17,  # High - handle rejection immediately
            rule_type="integration",
        ),
        # Generic ICM move tracking
        # Ensures all ICM moves are added to move history
        UpdateRule(
            name="track_icm_move",
            preconditions=_is_any_icm_move,
            effects=_track_icm_move,
            priority=5,  # Lower priority, runs after specific ICM handlers
            rule_type="integration",
        ),
    ]


# Precondition functions


def _is_perception_positive_icm(state: InformationState) -> bool:
    """Check if last move is icm:per*pos.

    Args:
        state: Current information state

    Returns:
        True if last move is positive perception ICM
    """
    if not state.shared.last_moves:
        return False

    last_move = state.shared.last_moves[-1]
    if not last_move.is_icm():
        return False

    return (
        last_move.feedback_level == ActionLevel.PERCEPTION
        and last_move.polarity == Polarity.POSITIVE
    )


def _is_understanding_positive_icm(state: InformationState) -> bool:
    """Check if last move is icm:und*pos.

    Args:
        state: Current information state

    Returns:
        True if last move is positive understanding ICM
    """
    if not state.shared.last_moves:
        return False

    last_move = state.shared.last_moves[-1]
    if not last_move.is_icm():
        return False

    return (
        last_move.feedback_level == ActionLevel.UNDERSTANDING
        and last_move.polarity == Polarity.POSITIVE
    )


def _is_acceptance_positive_icm(state: InformationState) -> bool:
    """Check if last move is icm:acc*pos.

    Args:
        state: Current information state

    Returns:
        True if last move is positive acceptance ICM
    """
    if not state.shared.last_moves:
        return False

    last_move = state.shared.last_moves[-1]
    if not last_move.is_icm():
        return False

    return (
        last_move.feedback_level == ActionLevel.ACCEPTANCE
        and last_move.polarity == Polarity.POSITIVE
    )


def _is_perception_negative_icm(state: InformationState) -> bool:
    """Check if last move is icm:per*neg.

    Args:
        state: Current information state

    Returns:
        True if last move is negative perception ICM
    """
    if not state.shared.last_moves:
        return False

    last_move = state.shared.last_moves[-1]
    if not last_move.is_icm():
        return False

    return (
        last_move.feedback_level == ActionLevel.PERCEPTION
        and last_move.polarity == Polarity.NEGATIVE
    )


def _is_understanding_negative_icm(state: InformationState) -> bool:
    """Check if last move is icm:und*neg.

    Args:
        state: Current information state

    Returns:
        True if last move is negative understanding ICM
    """
    if not state.shared.last_moves:
        return False

    last_move = state.shared.last_moves[-1]
    if not last_move.is_icm():
        return False

    return (
        last_move.feedback_level == ActionLevel.UNDERSTANDING
        and last_move.polarity == Polarity.NEGATIVE
    )


def _is_any_icm_move(state: InformationState) -> bool:
    """Check if last move is any ICM move.

    Args:
        state: Current information state

    Returns:
        True if last move is an ICM move
    """
    if not state.shared.last_moves:
        return False

    return state.shared.last_moves[-1].is_icm()


def _is_understanding_interrogative_icm(state: InformationState) -> bool:
    """Check if last move is icm:und*int.

    Args:
        state: Current information state

    Returns:
        True if last move is interrogative understanding ICM
    """
    if not state.shared.last_moves:
        return False

    last_move = state.shared.last_moves[-1]
    if not last_move.is_icm():
        return False

    return (
        last_move.feedback_level == ActionLevel.UNDERSTANDING
        and last_move.polarity == Polarity.INTERROGATIVE
    )


def _is_positive_answer_to_understanding_question(state: InformationState) -> bool:
    """Check if last move is answer(yes) to an understanding question.

    Args:
        state: Current information state

    Returns:
        True if last move is yes/positive answer to understanding question
    """
    if not state.shared.last_moves or not state.shared.qud:
        return False

    last_move = state.shared.last_moves[-1]
    if last_move.move_type != "answer" or not isinstance(last_move.content, Answer):
        return False

    # Check if answer is affirmative
    answer_content = last_move.content.content.lower()
    if answer_content not in ["yes", "yeah", "yep", "correct", "right", "true"]:
        return False

    # Check if top of QUD is an understanding question
    top_question = state.shared.qud[-1]
    if not isinstance(top_question, WhQuestion):
        return False

    # Understanding questions have predicate starting with "und_"
    return top_question.predicate.startswith("und_")


def _is_negative_answer_to_understanding_question(state: InformationState) -> bool:
    """Check if last move is answer(no) to an understanding question.

    Args:
        state: Current information state

    Returns:
        True if last move is no/negative answer to understanding question
    """
    if not state.shared.last_moves or not state.shared.qud:
        return False

    last_move = state.shared.last_moves[-1]
    if last_move.move_type != "answer" or not isinstance(last_move.content, Answer):
        return False

    # Check if answer is negative
    answer_content = last_move.content.content.lower()
    if answer_content not in ["no", "nope", "incorrect", "wrong", "false"]:
        return False

    # Check if top of QUD is an understanding question
    top_question = state.shared.qud[-1]
    if not isinstance(top_question, WhQuestion):
        return False

    # Understanding questions have predicate starting with "und_"
    return top_question.predicate.startswith("und_")


def _is_unhandled_icm(state: InformationState) -> bool:
    """Check if last move is an ICM move not handled by other rules.

    Args:
        state: Current information state

    Returns:
        True if last move is unhandled ICM
    """
    if not state.shared.last_moves:
        return False

    last_move = state.shared.last_moves[-1]
    # This will catch any ICM moves not matched by higher-priority rules
    return last_move.is_icm()


def _is_user_perception_negative(state: InformationState) -> bool:
    """Check if user is giving negative perception feedback.

    User saying "what?", "pardon?", "I didn't hear that", etc.

    Args:
        state: Current information state

    Returns:
        True if user is indicating perception failure
    """
    if not state.shared.last_moves:
        return False

    last_move = state.shared.last_moves[-1]

    # Check if it's from user
    if last_move.speaker == state.agent_id:
        return False

    # Check if it's perception negative ICM or similar utterance
    if last_move.is_icm():
        return (
            last_move.feedback_level == ActionLevel.PERCEPTION
            and last_move.polarity == Polarity.NEGATIVE
        )

    # Check for perception-related phrases
    if isinstance(last_move.content, str):
        content = last_move.content.lower()
        perception_phrases = ["what", "pardon", "sorry", "didn't hear", "come again"]
        return any(phrase in content for phrase in perception_phrases)

    return False


def _is_user_acceptance_negative(state: InformationState) -> bool:
    """Check if user is rejecting/correcting system's interpretation.

    User saying "no, that's wrong", "that's incorrect", etc.

    Args:
        state: Current information state

    Returns:
        True if user is rejecting system's content
    """
    if not state.shared.last_moves:
        return False

    last_move = state.shared.last_moves[-1]

    # Check if it's from user
    if last_move.speaker == state.agent_id:
        return False

    # Check if it's acceptance negative ICM
    if last_move.is_icm():
        return (
            last_move.feedback_level == ActionLevel.ACCEPTANCE
            and last_move.polarity == Polarity.NEGATIVE
        )

    # Check for rejection phrases
    if isinstance(last_move.content, str):
        content = last_move.content.lower()
        rejection_phrases = ["wrong", "incorrect", "that's not right", "no that's"]
        return any(phrase in content for phrase in rejection_phrases)

    return False


# Effect functions


def _integrate_perception_positive(state: InformationState) -> InformationState:
    """Integrate positive perception feedback (icm:per*pos).

    Marks the target utterance as perceived. This is the first level of grounding.

    Based on Larsson (2002) Section 3.6, Rule 3.1.

    Args:
        state: Current information state

    Returns:
        Updated information state with perception marked
    """
    new_state = state.clone()
    last_move = new_state.shared.last_moves[-1]

    # Add ICM move to move history
    new_state.shared.moves.append(last_move)

    # Update grounding status in metadata if target_move_index is specified
    if last_move.target_move_index is not None and last_move.target_move_index < len(
        new_state.shared.moves
    ):
        target_move = new_state.shared.moves[last_move.target_move_index]
        if "grounding_status" not in target_move.metadata:
            target_move.metadata["grounding_status"] = "perceived"

    return new_state


def _integrate_understanding_positive(state: InformationState) -> InformationState:
    """Integrate positive understanding feedback (icm:und*pos).

    Marks the target utterance as understood. This is the second level of grounding.

    Based on Larsson (2002) Section 3.6, Rule 3.2.

    Args:
        state: Current information state

    Returns:
        Updated information state with understanding marked
    """
    new_state = state.clone()
    last_move = new_state.shared.last_moves[-1]

    # Add ICM move to move history
    new_state.shared.moves.append(last_move)

    # Update grounding status in metadata
    if last_move.target_move_index is not None and last_move.target_move_index < len(
        new_state.shared.moves
    ):
        target_move = new_state.shared.moves[last_move.target_move_index]
        target_move.metadata["grounding_status"] = "understood"

    return new_state


def _integrate_acceptance_positive(state: InformationState) -> InformationState:
    """Integrate positive acceptance feedback (icm:acc*pos).

    Marks the target utterance as fully grounded and accepted. This is the
    final level of grounding.

    Based on Larsson (2002) Section 3.6, Rule 3.3.

    Args:
        state: Current information state

    Returns:
        Updated information state with acceptance marked
    """
    new_state = state.clone()
    last_move = new_state.shared.last_moves[-1]

    # Add ICM move to move history
    new_state.shared.moves.append(last_move)

    # Update grounding status to fully grounded
    if last_move.target_move_index is not None and last_move.target_move_index < len(
        new_state.shared.moves
    ):
        target_move = new_state.shared.moves[last_move.target_move_index]
        target_move.metadata["grounding_status"] = "grounded"

    # Mark content as accepted (could add to commitments if content is a proposition)
    if isinstance(last_move.content, str) and last_move.content.lower() in [
        "okay",
        "ok",
        "yes",
        "sure",
        "alright",
    ]:
        # Generic acceptance - full grounding achieved
        pass

    return new_state


def _integrate_perception_negative(state: InformationState) -> InformationState:
    """Integrate negative perception feedback (icm:per*neg).

    Indicates perception failure. The system should prepare to re-utter or
    request clarification.

    Based on Larsson (2002) Section 3.6, Rule 3.4.

    Args:
        state: Current information state

    Returns:
        Updated information state with perception failure marked
    """
    new_state = state.clone()
    last_move = new_state.shared.last_moves[-1]

    # Add ICM move to move history
    new_state.shared.moves.append(last_move)

    # Mark target move as not perceived
    if last_move.target_move_index is not None and last_move.target_move_index < len(
        new_state.shared.moves
    ):
        target_move = new_state.shared.moves[last_move.target_move_index]
        target_move.metadata["grounding_status"] = "perception_failed"
        target_move.metadata["needs_reutterance"] = True

    return new_state


def _integrate_understanding_negative(state: InformationState) -> InformationState:
    """Integrate negative understanding feedback (icm:und*neg).

    Indicates understanding failure. The system should prepare clarification.

    Based on Larsson (2002) Section 3.6, Rule 3.5.

    Args:
        state: Current information state

    Returns:
        Updated information state with understanding failure marked
    """
    new_state = state.clone()
    last_move = new_state.shared.last_moves[-1]

    # Add ICM move to move history
    new_state.shared.moves.append(last_move)

    # Mark target move as not understood
    if last_move.target_move_index is not None and last_move.target_move_index < len(
        new_state.shared.moves
    ):
        target_move = new_state.shared.moves[last_move.target_move_index]
        target_move.metadata["grounding_status"] = "understanding_failed"
        target_move.metadata["needs_clarification"] = True

    return new_state


def _track_icm_move(state: InformationState) -> InformationState:
    """Track any ICM move in move history.

    This is a catch-all for ICM moves that aren't handled by specific rules.
    Ensures all ICM feedback is recorded in the move history.

    Args:
        state: Current information state

    Returns:
        Updated information state with ICM move tracked
    """
    new_state = state.clone()
    last_move = new_state.shared.last_moves[-1]

    # Add to move history if not already added by specific handler
    if not new_state.shared.moves or new_state.shared.moves[-1] != last_move:
        new_state.shared.moves.append(last_move)

    return new_state


def _integrate_understanding_interrogative(state: InformationState) -> InformationState:
    """Integrate interrogative understanding feedback (icm:und*int).

    Raises an understanding question to QUD. The system is asking the user to confirm
    their interpretation, e.g., "To Paris, is that correct?"

    Based on Larsson (2002) Section 3.6, Rule 3.6.

    Args:
        state: Current information state

    Returns:
        Updated information state with understanding question on QUD
    """
    new_state = state.clone()
    last_move = new_state.shared.last_moves[-1]

    # Add ICM move to move history
    new_state.shared.moves.append(last_move)

    # Extract the content being confirmed from the ICM move
    # The content should describe what we're asking about
    if isinstance(last_move.content, str):
        # Create an understanding question based on the content
        # Format: "und_<content>" meaning "did you mean <content>?"
        und_question = WhQuestion(variable="x", predicate=f"und_{last_move.content}")
        new_state.shared.qud.append(und_question)
    elif isinstance(last_move.content, (WhQuestion, Answer)):
        # If content is already a question or answer, create understanding question about it
        content_str = str(last_move.content)
        und_question = WhQuestion(variable="x", predicate=f"und_{content_str}")
        new_state.shared.qud.append(und_question)

    return new_state


def _integrate_positive_icm_answer(state: InformationState) -> InformationState:
    """Integrate positive answer to understanding question.

    User said "yes" to confirmation question. Pop the understanding question and
    integrate the original content as if it was confirmed.

    Based on Larsson (2002) Section 3.6, Rule 3.8.

    Args:
        state: Current information state

    Returns:
        Updated information state with understanding question resolved
    """
    new_state = state.clone()
    last_move = new_state.shared.last_moves[-1]

    # Add answer to move history
    new_state.shared.moves.append(last_move)

    # Pop understanding question from QUD
    if new_state.shared.qud:
        und_question = new_state.shared.qud.pop()

        # Extract the original content from the understanding question
        # Format was: "und_<content>"
        if isinstance(und_question, WhQuestion) and und_question.predicate.startswith("und_"):
            confirmed_content: str = und_question.predicate[4:]  # Remove "und_" prefix

            # If the confirmed content looks like a question (issue), add it to QUD
            if "?" in confirmed_content or confirmed_content.startswith("?"):
                # This was confirming a question - push it to QUD
                try:
                    question = WhQuestion(variable="x", predicate=confirmed_content.strip("?"))
                    new_state.shared.qud.append(question)
                except Exception:
                    # If we can't parse it as a question, just note acceptance
                    pass
            else:
                # This was confirming a proposition - add to commitments
                new_state.shared.commitments.add(confirmed_content)

    return new_state


def _integrate_negative_icm_answer(state: InformationState) -> InformationState:
    """Integrate negative answer to understanding question.

    User said "no" to confirmation question. Pop the understanding question and
    acknowledge that the interpretation was incorrect.

    Based on Larsson (2002) Section 3.6, Rule 3.7.

    Args:
        state: Current information state

    Returns:
        Updated information state with understanding question resolved
    """
    new_state = state.clone()
    last_move = new_state.shared.last_moves[-1]

    # Add answer to move history
    new_state.shared.moves.append(last_move)

    # Pop understanding question from QUD
    if new_state.shared.qud:
        und_question = new_state.shared.qud.pop()

        # Extract the original content that was rejected
        # Format was: "und_<content>"
        if isinstance(und_question, WhQuestion) and und_question.predicate.startswith("und_"):
            rejected_content: str = und_question.predicate[4:]  # Remove "und_" prefix

            # Mark the interpretation as incorrect
            # The system should request clarification or re-ask
            # Store in beliefs so selection rules can handle it
            new_state.private.beliefs["rejected_interpretation"] = rejected_content
            new_state.private.beliefs["needs_reutterance"] = True

    return new_state


def _integrate_other_icm(state: InformationState) -> InformationState:
    """Integrate any other ICM move.

    Generic catch-all for ICM moves not handled by specific rules.

    Based on Larsson (2002) Section 3.6, Rule 3.10.

    Args:
        state: Current information state

    Returns:
        Updated information state with ICM tracked
    """
    new_state = state.clone()
    last_move = new_state.shared.last_moves[-1]

    # Add to move history
    if not new_state.shared.moves or new_state.shared.moves[-1] != last_move:
        new_state.shared.moves.append(last_move)

    return new_state


def _integrate_user_perception_negative(state: InformationState) -> InformationState:
    """Integrate user perception negative feedback.

    User indicated they didn't hear/perceive system's utterance (e.g., "what?").
    Retract last system move and prepare to re-utter.

    Based on Larsson (2002) Section 3.6, Rule 3.20.

    Args:
        state: Current information state

    Returns:
        Updated information state with perception failure handled
    """
    new_state = state.clone()
    last_move = new_state.shared.last_moves[-1]

    # Add ICM to move history
    new_state.shared.moves.append(last_move)

    # Find last system utterance and mark for re-utterance
    for i in range(len(new_state.shared.moves) - 1, -1, -1):
        move = new_state.shared.moves[i]
        if move.speaker == new_state.agent_id:
            # Mark for re-utterance
            move.metadata["perception_failed"] = True
            move.metadata["needs_reutterance"] = True
            # Store in beliefs so selection can handle it
            new_state.private.beliefs["last_utterance_failed"] = True
            new_state.private.beliefs["reutterance_content"] = str(move.content)
            break

    return new_state


def _integrate_user_acceptance_negative(state: InformationState) -> InformationState:
    """Integrate user acceptance negative feedback.

    User is rejecting system's interpretation or assertion (e.g., "no, that's wrong").
    Retract the rejected content from commitments.

    Based on Larsson (2002) Section 3.6, Rule 3.21.

    Args:
        state: Current information state

    Returns:
        Updated information state with rejection handled
    """
    new_state = state.clone()
    last_move = new_state.shared.last_moves[-1]

    # Add ICM to move history
    new_state.shared.moves.append(last_move)

    # Find the content being rejected (usually the last system assertion/answer)
    # Look through recent moves to find what user is rejecting
    for i in range(len(new_state.shared.moves) - 1, -1, -1):
        move = new_state.shared.moves[i]
        if move.speaker == new_state.agent_id and move.move_type in ["answer", "assert"]:
            # Try to extract the proposition that was asserted
            if isinstance(move.content, str):
                # Remove from commitments if present
                if move.content in new_state.shared.commitments:
                    new_state.shared.commitments.remove(move.content)
                # Mark for correction
                new_state.private.beliefs["rejected_content"] = move.content
                new_state.private.beliefs["needs_correction"] = True
                break

    return new_state
