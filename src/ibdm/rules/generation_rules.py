"""Generation rules for Issue-Based Dialogue Management.

Generation rules produce natural language utterances from dialogue moves.
They implement template-based and context-aware generation strategies.

Based on Larsson (2002) Issue-based Dialogue Management.
"""

from ibdm.core import AltQuestion, Answer, DialogueMove, InformationState, WhQuestion, YNQuestion
from ibdm.rules.update_rules import UpdateRule


def create_generation_rules() -> list[UpdateRule]:
    """Create standard generation rules.

    Returns:
        List of generation rules
    """
    return [
        # Greeting generation
        UpdateRule(
            name="generate_greeting",
            preconditions=_is_greeting_move,
            effects=_generate_greeting_text,
            priority=10,
            rule_type="generation",
        ),
        # Quit generation
        UpdateRule(
            name="generate_quit",
            preconditions=_is_quit_move,
            effects=_generate_quit_text,
            priority=10,
            rule_type="generation",
        ),
        # Question generation (ask moves)
        UpdateRule(
            name="generate_question",
            preconditions=_is_ask_move,
            effects=_generate_question_text,
            priority=8,
            rule_type="generation",
        ),
        # Answer generation
        UpdateRule(
            name="generate_answer",
            preconditions=_is_answer_move,
            effects=_generate_answer_text,
            priority=8,
            rule_type="generation",
        ),
        # Assertion generation
        UpdateRule(
            name="generate_assertion",
            preconditions=_is_assertion_move,
            effects=_generate_assertion_text,
            priority=7,
            rule_type="generation",
        ),
    ]


# Precondition functions


def _is_greeting_move(state: InformationState) -> bool:
    """Check if the move to generate is a greeting."""
    move = state.private.beliefs.get("_temp_generate_move")
    return isinstance(move, DialogueMove) and move.move_type == "greet"


def _is_quit_move(state: InformationState) -> bool:
    """Check if the move to generate is a quit."""
    move = state.private.beliefs.get("_temp_generate_move")
    return isinstance(move, DialogueMove) and move.move_type == "quit"


def _is_ask_move(state: InformationState) -> bool:
    """Check if the move to generate is a question."""
    move = state.private.beliefs.get("_temp_generate_move")
    return isinstance(move, DialogueMove) and move.move_type == "ask"


def _is_answer_move(state: InformationState) -> bool:
    """Check if the move to generate is an answer."""
    move = state.private.beliefs.get("_temp_generate_move")
    return isinstance(move, DialogueMove) and move.move_type == "answer"


def _is_assertion_move(state: InformationState) -> bool:
    """Check if the move to generate is an assertion."""
    move = state.private.beliefs.get("_temp_generate_move")
    return isinstance(move, DialogueMove) and move.move_type == "assert"


# Effect functions


def _generate_greeting_text(state: InformationState) -> InformationState:
    """Generate text for a greeting move."""
    new_state = state.clone()
    move = new_state.private.beliefs.get("_temp_generate_move")

    # Context-aware greeting
    if move.content == "greeting_response":
        # Responding to a greeting
        text = "Hello! How can I help you today?"
    else:
        # Initiating greeting
        text = "Hello!"

    new_state.private.beliefs["_temp_generated_text"] = text
    return new_state


def _generate_quit_text(state: InformationState) -> InformationState:
    """Generate text for a quit move."""
    new_state = state.clone()
    move = new_state.private.beliefs.get("_temp_generate_move")

    if move.content == "quit_response":
        # Responding to quit
        text = "Goodbye! Have a great day!"
    else:
        # Initiating quit
        text = "Goodbye!"

    new_state.private.beliefs["_temp_generated_text"] = text
    return new_state


def _generate_question_text(state: InformationState) -> InformationState:
    """Generate text for a question move."""
    new_state = state.clone()
    move = new_state.private.beliefs.get("_temp_generate_move")

    question = move.content
    text = ""

    if isinstance(question, WhQuestion):
        # Generate wh-question text
        wh_word = question.constraints.get("wh_word", "what")

        # Special case for common questions
        if question.predicate == "how_can_i_help":
            text = "How can I help you?"
        elif question.predicate == "clarification_needed":
            text = "Could you please clarify what you mean?"
        else:
            # Generic wh-question
            predicate = question.predicate.replace("_", " ")
            text = f"{wh_word.capitalize()} {predicate}?"

    elif isinstance(question, YNQuestion):
        # Generate yes/no question text
        proposition = question.proposition.replace("_", " ")
        text = f"{proposition.capitalize()}?"

    elif isinstance(question, AltQuestion):
        # Generate alternative question text
        if len(question.alternatives) == 2:
            text = f"{question.alternatives[0].capitalize()} or {question.alternatives[1]}?"
        else:
            alt_list = ", ".join(question.alternatives[:-1])
            text = f"{alt_list.capitalize()}, or {question.alternatives[-1]}?"

    else:
        # Fallback to string representation
        text = str(question)

    new_state.private.beliefs["_temp_generated_text"] = text
    return new_state


def _generate_answer_text(state: InformationState) -> InformationState:
    """Generate text for an answer move."""
    new_state = state.clone()
    move = new_state.private.beliefs.get("_temp_generate_move")

    answer = move.content

    if isinstance(answer, Answer):
        content = answer.content

        # Generate appropriate text based on answer type
        if isinstance(content, bool):
            text = "Yes." if content else "No."
        elif isinstance(content, str):
            # Check if it's already a complete sentence
            if content.endswith((".", "!", "?")):
                text = content
            else:
                # Add context if we have the question
                if answer.question_ref:
                    if isinstance(answer.question_ref, WhQuestion):
                        text = f"The answer is: {content}."
                    else:
                        text = f"{content}."
                else:
                    text = f"{content}."
        else:
            # For other types, convert to string
            text = str(content)
    else:
        # Fallback
        text = str(answer)

    new_state.private.beliefs["_temp_generated_text"] = text
    return new_state


def _generate_assertion_text(state: InformationState) -> InformationState:
    """Generate text for an assertion move."""
    new_state = state.clone()
    move = new_state.private.beliefs.get("_temp_generate_move")

    content = move.content

    # Ensure proper sentence format
    if isinstance(content, str):
        text = content if content.endswith((".", "!", "?")) else f"{content}."
    else:
        text = f"{str(content)}."

    new_state.private.beliefs["_temp_generated_text"] = text
    return new_state
