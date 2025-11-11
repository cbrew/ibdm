"""Question accommodation for resolving underspecified questions.

Question accommodation resolves questions that reference previous context
or are incomplete, making them fully specified for QUD management.
"""

from ibdm.core import InformationState, Question, WhQuestion, YNQuestion


def accommodate_question(question: Question, state: InformationState) -> Question:
    """Accommodate an underspecified question using dialogue context.

    This function resolves:
    - Anaphoric references (e.g., "What about it?" referencing previous topic)
    - Follow-up questions (e.g., "And the time?" after asking about a meeting)
    - Underspecified wh-questions (e.g., "What?" requiring context)

    Args:
        question: The question to accommodate
        state: Current information state with context

    Returns:
        Accommodated (fully specified) question
    """
    if isinstance(question, WhQuestion):
        return _accommodate_wh_question(question, state)
    elif isinstance(question, YNQuestion):
        return _accommodate_yn_question(question, state)
    else:
        # For other question types, return as-is
        return question


def _accommodate_wh_question(question: WhQuestion, state: InformationState) -> WhQuestion:
    """Accommodate a wh-question using context.

    Resolves:
    - Bare wh-words ("What?" → infer predicate from context)
    - Anaphoric references ("What about it?" → resolve "it")
    - Follow-up questions ("And the price?" → infer entity from previous question)
    """
    predicate = question.predicate.lower()

    # Handle bare wh-questions (e.g., just "what?")
    if len(predicate.split()) <= 2 and question.constraints.get("wh_word"):
        # Try to infer predicate from previous context
        if state.shared.qud:
            top_qud = state.shared.top_qud()
            if isinstance(top_qud, WhQuestion):
                # Reuse the predicate from top QUD
                return WhQuestion(
                    variable=question.variable,
                    predicate=top_qud.predicate,
                    constraints={
                        **question.constraints,
                        "accommodated": True,
                        "source": "qud_context",
                    },
                )

        # Try to infer from last moves
        if state.shared.last_moves:
            last_move = state.shared.last_moves[-1]
            if last_move.move_type == "assert":
                # Asking about the assertion
                return WhQuestion(
                    variable=question.variable,
                    predicate=f"clarify({last_move.content})",
                    constraints={
                        **question.constraints,
                        "accommodated": True,
                        "source": "last_assertion",
                    },
                )

    # Handle anaphoric references (pronouns like "it", "that")
    if any(pron in predicate for pron in ["it", "that", "this", "them"]):
        # Resolve pronoun to previous topic
        if state.shared.qud:
            top_qud = state.shared.top_qud()
            if isinstance(top_qud, WhQuestion):
                # Replace pronoun with actual predicate
                resolved_predicate = predicate
                for pron in ["it", "that", "this", "them"]:
                    if pron in predicate:
                        resolved_predicate = resolved_predicate.replace(pron, top_qud.predicate)

                return WhQuestion(
                    variable=question.variable,
                    predicate=resolved_predicate,
                    constraints={
                        **question.constraints,
                        "accommodated": True,
                        "resolved_anaphora": True,
                    },
                )

    # Follow-up questions with "and" (e.g., "And the price?")
    if predicate.startswith("and "):
        predicate = predicate[4:]  # Remove "and "

        # Get context from previous question
        entity = None
        if state.shared.qud:
            top_qud = state.shared.top_qud()
            if isinstance(top_qud, WhQuestion):
                # Extract entity from previous question
                entity = _extract_entity(top_qud.predicate)

        if entity:
            return WhQuestion(
                variable=question.variable,
                predicate=f"{predicate} of {entity}",
                constraints={
                    **question.constraints,
                    "accommodated": True,
                    "follow_up": True,
                },
            )

    # No accommodation needed
    return question


def _accommodate_yn_question(question: YNQuestion, state: InformationState) -> YNQuestion:
    """Accommodate a yn-question using context.

    Resolves anaphoric references in the proposition.
    """
    proposition = question.proposition.lower()

    # Handle anaphoric references
    if any(pron in proposition for pron in ["it", "that", "this"]):
        # Resolve pronoun to previous topic
        if state.shared.qud:
            top_qud = state.shared.top_qud()
            if isinstance(top_qud, WhQuestion):
                # Replace pronoun with predicate
                resolved_prop = proposition
                for pron in ["it", "that", "this"]:
                    if pron in proposition:
                        resolved_prop = resolved_prop.replace(pron, top_qud.predicate)

                return YNQuestion(
                    proposition=resolved_prop,
                    parameters={
                        **question.parameters,
                        "accommodated": True,
                        "resolved_anaphora": True,
                    },
                )

    # No accommodation needed
    return question


def _extract_entity(predicate: str) -> str | None:
    """Extract entity from a predicate string.

    Simple heuristic: look for noun-like words at the end.
    """
    words = predicate.split()
    if len(words) > 1:
        # Return last word (often the entity)
        return words[-1]
    return None
