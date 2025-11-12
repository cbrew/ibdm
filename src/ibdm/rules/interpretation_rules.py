"""Interpretation rules for Issue-Based Dialogue Management.

Interpretation rules map utterances to dialogue moves. They recognize
questions, answers, assertions, and commands in natural language input.

Based on Larsson (2002) Issue-based Dialogue Management.
"""

import re

from ibdm.core import (
    AltQuestion,
    Answer,
    DialogueMove,
    InformationState,
    Plan,
    WhQuestion,
    YNQuestion,
)
from ibdm.rules.update_rules import UpdateRule


def create_interpretation_rules() -> list[UpdateRule]:
    """Create standard interpretation rules.

    Returns:
        List of interpretation rules
    """
    return [
        # Task accommodation - NDA generation (highest priority)
        UpdateRule(
            name="accommodate_nda_task",
            preconditions=_is_nda_request,
            effects=_create_nda_plan,
            priority=12,
            rule_type="interpretation",
        ),
        # Greetings (highest priority)
        UpdateRule(
            name="interpret_greeting",
            preconditions=_is_greeting,
            effects=_create_greeting_move,
            priority=10,
            rule_type="interpretation",
        ),
        # Quit/goodbye
        UpdateRule(
            name="interpret_quit",
            preconditions=_is_quit,
            effects=_create_quit_move,
            priority=10,
            rule_type="interpretation",
        ),
        # Wh-questions (what, where, when, who, why, how)
        UpdateRule(
            name="interpret_wh_question",
            preconditions=_is_wh_question,
            effects=_create_wh_question_move,
            priority=8,
            rule_type="interpretation",
        ),
        # Yes/No questions
        UpdateRule(
            name="interpret_yn_question",
            preconditions=_is_yn_question,
            effects=_create_yn_question_move,
            priority=7,
            rule_type="interpretation",
        ),
        # Alternative questions (X or Y?)
        UpdateRule(
            name="interpret_alt_question",
            preconditions=_is_alt_question,
            effects=_create_alt_question_move,
            priority=7,
            rule_type="interpretation",
        ),
        # Yes/No answers
        UpdateRule(
            name="interpret_yn_answer",
            preconditions=_is_yn_answer,
            effects=_create_yn_answer_move,
            priority=6,
            rule_type="interpretation",
        ),
        # Simple factual answers
        UpdateRule(
            name="interpret_answer",
            preconditions=_is_answer,
            effects=_create_answer_move,
            priority=5,
            rule_type="interpretation",
        ),
        # Assertions (lowest priority - only if nothing else matches)
        UpdateRule(
            name="interpret_assertion",
            preconditions=_is_assertion,
            effects=_create_assertion_move,
            priority=1,
            rule_type="interpretation",
        ),
    ]


# Precondition functions


def _is_nda_request(state: InformationState) -> bool:
    """Check if utterance is requesting NDA document generation."""
    utterance = state.private.beliefs.get("_temp_utterance", "").lower()
    # Look for patterns indicating NDA creation request
    nda_patterns = [
        "draft nda",
        "draft an nda",
        "create nda",
        "generate nda",
        "need an nda",
        "nda document",
        "nondisclosure agreement",
        "non-disclosure agreement",
    ]
    return any(pattern in utterance for pattern in nda_patterns)


def _is_greeting(state: InformationState) -> bool:
    """Check if utterance is a greeting."""
    utterance = state.private.beliefs.get("_temp_utterance", "").lower()
    greetings = ["hello", "hi", "hey", "greetings", "good morning", "good afternoon"]
    return any(greeting in utterance for greeting in greetings)


def _is_quit(state: InformationState) -> bool:
    """Check if utterance is a quit command."""
    utterance = state.private.beliefs.get("_temp_utterance", "").lower().strip()
    quit_words = ["quit", "exit", "bye", "goodbye", "see you"]
    return any(quit_word in utterance for quit_word in quit_words)


def _is_wh_question(state: InformationState) -> bool:
    """Check if utterance is a wh-question."""
    utterance = state.private.beliefs.get("_temp_utterance", "").lower()
    # Check for wh-words at the beginning
    wh_words = ["what", "where", "when", "who", "why", "how", "which"]
    return any(utterance.strip().startswith(wh) for wh in wh_words)


def _is_yn_question(state: InformationState) -> bool:
    """Check if utterance is a yes/no question."""
    utterance = state.private.beliefs.get("_temp_utterance", "").strip()
    if not utterance:
        return False

    # Check for question mark
    if not utterance.endswith("?"):
        return False

    # Check for auxiliary verbs at the beginning (typical Y/N question structure)
    utterance_lower = utterance.lower()
    auxiliaries = [
        "is",
        "are",
        "was",
        "were",
        "do",
        "does",
        "did",
        "can",
        "could",
        "will",
        "would",
        "should",
        "may",
        "might",
    ]
    return any(utterance_lower.startswith(aux + " ") for aux in auxiliaries)


def _is_alt_question(state: InformationState) -> bool:
    """Check if utterance is an alternative question (X or Y?)."""
    utterance = state.private.beliefs.get("_temp_utterance", "")
    # Check for "or" pattern with question mark
    return " or " in utterance.lower() and utterance.strip().endswith("?")


def _is_yn_answer(state: InformationState) -> bool:
    """Check if utterance is a yes/no answer."""
    utterance = state.private.beliefs.get("_temp_utterance", "").lower().strip()
    yn_words = ["yes", "no", "yeah", "nope", "yep", "nah", "true", "false"]
    # Only match if it's a short response (to avoid false positives)
    return utterance in yn_words or (
        len(utterance.split()) <= 2 and any(yn in utterance for yn in yn_words)
    )


def _is_answer(state: InformationState) -> bool:
    """Check if utterance is likely an answer to the top QUD."""
    # An answer is likely if:
    # 1. There's a question on the QUD stack
    # 2. The utterance is not a question
    # 3. It's not a yes/no answer (those are handled separately)
    # 4. It's not too long (simple factual answers)
    if not state.shared.qud:
        return False

    # Exclude yes/no answers
    if _is_yn_answer(state):
        return False

    utterance = state.private.beliefs.get("_temp_utterance", "")
    if not utterance or utterance.strip().endswith("?"):
        return False

    # Prefer shorter utterances as answers
    word_count = len(utterance.split())
    return word_count <= 20  # Arbitrary threshold


def _is_assertion(state: InformationState) -> bool:
    """Check if utterance is an assertion (catch-all for unmatched utterances)."""
    # Only match if none of the specific patterns match
    return not (
        _is_greeting(state)
        or _is_quit(state)
        or _is_wh_question(state)
        or _is_yn_question(state)
        or _is_alt_question(state)
        or _is_yn_answer(state)
        or _is_answer(state)
    )


# Effect functions


def _create_greeting_move(state: InformationState) -> InformationState:
    """Create a greeting dialogue move."""
    new_state = state.clone()
    speaker = new_state.private.beliefs.get("_temp_speaker", "user")
    utterance = new_state.private.beliefs.get("_temp_utterance", "")

    move = DialogueMove(
        move_type="greet",
        content=utterance,
        speaker=speaker,
    )
    new_state.private.agenda.append(move)
    return new_state


def _create_quit_move(state: InformationState) -> InformationState:
    """Create a quit dialogue move."""
    new_state = state.clone()
    speaker = new_state.private.beliefs.get("_temp_speaker", "user")
    utterance = new_state.private.beliefs.get("_temp_utterance", "")

    move = DialogueMove(
        move_type="quit",
        content=utterance,
        speaker=speaker,
    )
    new_state.private.agenda.append(move)
    return new_state


def _create_wh_question_move(state: InformationState) -> InformationState:
    """Create a wh-question dialogue move."""
    new_state = state.clone()
    speaker = new_state.private.beliefs.get("_temp_speaker", "user")
    utterance = new_state.private.beliefs.get("_temp_utterance", "")

    # Extract wh-word and create a simple semantic representation
    utterance_lower = utterance.lower()
    wh_word = ""
    for word in ["what", "where", "when", "who", "why", "how", "which"]:
        if utterance_lower.strip().startswith(word):
            wh_word = word
            break

    # Extract predicate (simplified - just use the rest of the utterance)
    predicate = utterance.strip().rstrip("?").strip()

    question = WhQuestion(variable="x", predicate=predicate, constraints={"wh_word": wh_word})

    move = DialogueMove(
        move_type="ask",
        content=question,
        speaker=speaker,
    )
    new_state.private.agenda.append(move)
    return new_state


def _create_yn_question_move(state: InformationState) -> InformationState:
    """Create a yes/no question dialogue move."""
    new_state = state.clone()
    speaker = new_state.private.beliefs.get("_temp_speaker", "user")
    utterance = new_state.private.beliefs.get("_temp_utterance", "")

    # Use the utterance as the proposition
    proposition = utterance.strip().rstrip("?").strip()

    question = YNQuestion(proposition=proposition)

    move = DialogueMove(
        move_type="ask",
        content=question,
        speaker=speaker,
    )
    new_state.private.agenda.append(move)
    return new_state


def _create_alt_question_move(state: InformationState) -> InformationState:
    """Create an alternative question dialogue move."""
    new_state = state.clone()
    speaker = new_state.private.beliefs.get("_temp_speaker", "user")
    utterance = new_state.private.beliefs.get("_temp_utterance", "")

    # Extract alternatives by splitting on "or"
    text = utterance.strip().rstrip("?").strip()
    # Simple split (could be more sophisticated)
    alternatives = [alt.strip() for alt in re.split(r"\s+or\s+", text, flags=re.IGNORECASE)]

    question = AltQuestion(alternatives=alternatives)

    move = DialogueMove(
        move_type="ask",
        content=question,
        speaker=speaker,
    )
    new_state.private.agenda.append(move)
    return new_state


def _create_yn_answer_move(state: InformationState) -> InformationState:
    """Create a yes/no answer dialogue move."""
    new_state = state.clone()
    speaker = new_state.private.beliefs.get("_temp_speaker", "user")
    utterance = new_state.private.beliefs.get("_temp_utterance", "").lower().strip()

    # Convert to boolean
    is_positive = any(word in utterance for word in ["yes", "yeah", "yep", "true"])

    # Reference the top QUD if available
    question_ref = new_state.shared.top_qud() if new_state.shared.qud else None

    answer = Answer(content=is_positive, question_ref=question_ref)

    move = DialogueMove(
        move_type="answer",
        content=answer,
        speaker=speaker,
    )
    new_state.private.agenda.append(move)
    return new_state


def _create_answer_move(state: InformationState) -> InformationState:
    """Create an answer dialogue move."""
    new_state = state.clone()
    speaker = new_state.private.beliefs.get("_temp_speaker", "user")
    utterance = new_state.private.beliefs.get("_temp_utterance", "")

    # Reference the top QUD if available
    question_ref = new_state.shared.top_qud() if new_state.shared.qud else None

    answer = Answer(content=utterance.strip(), question_ref=question_ref)

    move = DialogueMove(
        move_type="answer",
        content=answer,
        speaker=speaker,
    )
    new_state.private.agenda.append(move)
    return new_state


def _create_assertion_move(state: InformationState) -> InformationState:
    """Create an assertion dialogue move (fallback)."""
    new_state = state.clone()
    speaker = new_state.private.beliefs.get("_temp_speaker", "user")
    utterance = new_state.private.beliefs.get("_temp_utterance", "")

    move = DialogueMove(
        move_type="assert",
        content=utterance.strip(),
        speaker=speaker,
    )
    new_state.private.agenda.append(move)
    return new_state


def _create_nda_plan(state: InformationState) -> InformationState:
    """Create a hierarchical plan for NDA document generation.

    This creates a findout plan with ordered subplans for each NDA requirement:
    1. findout(parties) - WhQuestion
    2. findout(nda_type) - AltQuestion["mutual", "one-way"]
    3. findout(effective_date) - WhQuestion
    4. findout(duration) - WhQuestion
    5. findout(governing_law) - AltQuestion["California", "Delaware"]
    6. confirm(generate_document) - YNQuestion
    """
    new_state = state.clone()

    # Create subplans for each NDA requirement
    subplans = [
        Plan(
            plan_type="findout",
            content=WhQuestion(variable="parties", predicate="legal_entities"),
            status="active",
        ),
        Plan(
            plan_type="findout",
            content=AltQuestion(alternatives=["mutual", "one-way"]),
            status="active",
        ),
        Plan(
            plan_type="findout",
            content=WhQuestion(variable="effective_date", predicate="date"),
            status="active",
        ),
        Plan(
            plan_type="findout",
            content=WhQuestion(variable="duration", predicate="time_period"),
            status="active",
        ),
        Plan(
            plan_type="findout",
            content=AltQuestion(alternatives=["California", "Delaware"]),
            status="active",
        ),
        Plan(
            plan_type="findout",
            content=YNQuestion(proposition="generate_document"),
            status="active",
        ),
    ]

    # Create the main NDA plan
    nda_plan = Plan(
        plan_type="findout",
        content="nda_requirements",
        status="active",
        subplans=subplans,
    )

    # Store the plan in private.plan (it's a list)
    new_state.private.plan.append(nda_plan)

    # Initialize document type in beliefs
    new_state.private.beliefs["document_type"] = "NDA"

    # Create a request move representing the user's task request
    speaker = new_state.private.beliefs.get("_temp_speaker", "user")
    utterance = new_state.private.beliefs.get("_temp_utterance", "")
    move = DialogueMove(
        move_type="request",
        content=utterance,
        speaker=speaker,
    )
    new_state.private.agenda.append(move)

    return new_state
