"""Answer accommodation for resolving elliptical answers.

Answer accommodation handles incomplete or fragment answers that require
context to be fully interpreted.
"""

from ibdm.core import AltQuestion, Answer, InformationState, Question, WhQuestion, YNQuestion


def resolve_elliptical_answer(answer_text: str, state: InformationState) -> Answer:
    """Resolve an elliptical (incomplete) answer using QUD context.

    This function handles:
    - Fragment answers (e.g., "Tomorrow" in response to "When?")
    - Short answers (e.g., "Coffee" in response to "Tea or coffee?")
    - Bare noun phrases (e.g., "Paris" in response to "Where is the Eiffel Tower?")

    Args:
        answer_text: The elliptical answer text
        state: Current information state (must have QUD for context)

    Returns:
        Resolved Answer object with proper content and question reference
    """
    if not state.shared.qud:
        # No context - return literal answer
        return Answer(content=answer_text.strip())

    top_qud = state.shared.top_qud()

    # Resolve based on question type
    if isinstance(top_qud, WhQuestion):
        return _resolve_wh_answer(answer_text, top_qud, state)
    elif isinstance(top_qud, YNQuestion):
        return _resolve_yn_answer(answer_text, top_qud, state)
    elif isinstance(top_qud, AltQuestion):
        return _resolve_alt_answer(answer_text, top_qud, state)
    else:
        # Unknown question type
        return Answer(content=answer_text.strip(), question_ref=top_qud)


def _resolve_wh_answer(answer_text: str, question: WhQuestion, state: InformationState) -> Answer:
    """Resolve an elliptical answer to a wh-question.

    Examples:
    - Q: "When is the meeting?" A: "Tomorrow" → "Tomorrow"
    - Q: "Where is Paris?" A: "France" → "France"
    - Q: "Who called?" A: "John" → "John"
    """
    # For wh-questions, fragment answers are usually just the value
    # Clean up the text
    cleaned = answer_text.strip()

    # Check if it's a complete sentence (has verb)
    words = cleaned.split()
    if len(words) > 2 and any(word.endswith(("s", "ed", "ing")) for word in words):
        # Looks like a complete answer
        content = cleaned
    else:
        # Fragment answer - use as-is but mark as fragment
        content = cleaned

    return Answer(
        content=content,
        question_ref=question,
        certainty=1.0,
    )


def _resolve_yn_answer(answer_text: str, question: YNQuestion, state: InformationState) -> Answer:
    """Resolve an elliptical answer to a yes/no question.

    Examples:
    - Q: "Is it raining?" A: "Yes" → True
    - Q: "Do you like coffee?" A: "I do" → True
    - Q: "Are you ready?" A: "Not yet" → False
    """
    text_lower = answer_text.lower().strip()

    # Check for explicit yes/no
    if text_lower in ["yes", "yeah", "yep", "yup", "sure", "absolutely"]:
        return Answer(content=True, question_ref=question)
    elif text_lower in ["no", "nope", "nah", "not really"]:
        return Answer(content=False, question_ref=question)

    # Check for positive indicators
    positive_words = ["do", "am", "is", "are", "was", "were", "will", "would"]
    if any(text_lower.startswith(word) for word in positive_words):
        return Answer(content=True, question_ref=question)

    # Check for negative indicators
    negative_words = ["don't", "not", "never", "won't", "wouldn't", "can't"]
    if any(word in text_lower for word in negative_words):
        return Answer(content=False, question_ref=question)

    # Ambiguous - return text but mark certainty as lower
    return Answer(content=text_lower, question_ref=question, certainty=0.7)


def _resolve_alt_answer(answer_text: str, question: AltQuestion, state: InformationState) -> Answer:
    """Resolve an elliptical answer to an alternative question.

    Examples:
    - Q: "Tea or coffee?" A: "Coffee" → "coffee"
    - Q: "Red, green, or blue?" A: "The blue one" → "blue"
    """
    text_lower = answer_text.lower().strip()

    # Check if answer contains one of the alternatives
    for alt in question.alternatives:
        if alt.lower() in text_lower or text_lower in alt.lower():
            return Answer(content=alt, question_ref=question)

    # Check for "first", "second", ordinal responses
    ordinals = ["first", "second", "third", "last"]
    ordinal_map = {"first": 0, "second": 1, "third": 2, "last": -1}

    for ordinal in ordinals:
        if ordinal in text_lower:
            idx = ordinal_map[ordinal]
            if -len(question.alternatives) <= idx < len(question.alternatives):
                return Answer(
                    content=question.alternatives[idx],
                    question_ref=question,
                )

    # Couldn't resolve - return as-is with lower certainty
    return Answer(content=text_lower, question_ref=question, certainty=0.6)


def expand_fragment_to_sentence(fragment: str | bool, question: Question) -> str:
    """Expand a fragment answer into a complete sentence.

    Args:
        fragment: The fragment answer (string or bool for YN questions)
        question: The question being answered

    Returns:
        A complete sentence form of the answer
    """
    if isinstance(question, WhQuestion):
        wh_word = question.constraints.get("wh_word", "").lower()

        if wh_word == "when":
            return f"It is {fragment}."
        elif wh_word == "where":
            return f"It is at {fragment}."
        elif wh_word == "who":
            return f"It is {fragment}."
        elif wh_word == "what":
            return f"It is {fragment}."
        else:
            return f"{fragment}."

    elif isinstance(question, YNQuestion):
        if isinstance(fragment, bool):
            return "Yes." if fragment else "No."
        return f"{fragment}."

    elif isinstance(question, AltQuestion):
        return f"The answer is {fragment}."

    else:
        return f"{fragment}."
