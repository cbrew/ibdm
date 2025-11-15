"""Generation rules for Issue-Based Dialogue Management.

Generation rules produce natural language utterances from dialogue moves.
They implement template-based and context-aware generation strategies.

Based on Larsson (2002) Issue-based Dialogue Management.
"""

from ibdm.core import (
    AltQuestion,
    Answer,
    DialogueMove,
    InformationState,
    Plan,
    WhQuestion,
    YNQuestion,
)
from ibdm.core.domain import DomainModel
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
        # Command generation (acknowledgment)
        UpdateRule(
            name="generate_command",
            preconditions=_is_command_move,
            effects=_generate_command_text,
            priority=9,
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


def _is_command_move(state: InformationState) -> bool:
    """Check if the move to generate is a command."""
    move = state.private.beliefs.get("_temp_generate_move")
    return isinstance(move, DialogueMove) and move.move_type == "command"


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


# Plan context helpers


def _get_active_plan(state: InformationState) -> Plan | None:
    """Get currently active plan, if any.

    Returns the first active plan from the plan stack, or None if no active plans.
    """
    for plan in state.private.plan:
        if plan.is_active():
            return plan
    return None


def _get_plan_progress(plan: Plan | None) -> tuple[int, int]:
    """Get plan progress (completed, total).

    Args:
        plan: Plan object

    Returns:
        Tuple of (completed_count, total_count)
    """
    if not plan or not plan.subplans:
        return (0, 0)

    completed = sum(1 for sp in plan.subplans if sp.status == "completed")
    total = len(plan.subplans)
    return (completed, total)


def _get_domain_for_plan(plan: Plan | None) -> DomainModel | None:
    """Get domain model for plan.

    Args:
        plan: Plan object

    Returns:
        DomainModel instance, or None if plan type not recognized
    """
    if not plan:
        return None

    if plan.plan_type == "nda_drafting":
        from ibdm.domains.nda_domain import get_nda_domain

        return get_nda_domain()

    return None


# Effect functions


def _generate_greeting_text(state: InformationState) -> InformationState:
    """Generate text for a greeting move."""
    new_state = state.clone()
    move = new_state.private.beliefs.get("_temp_generate_move")

    # Context-aware greeting
    if move is not None and move.content == "greeting_response":
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

    if move is not None and move.content == "quit_response":
        # Responding to quit
        text = "Goodbye! Have a great day!"
    else:
        # Initiating quit
        text = "Goodbye!"

    new_state.private.beliefs["_temp_generated_text"] = text
    return new_state


def _generate_command_text(state: InformationState) -> InformationState:
    """Generate text for a command move."""
    new_state = state.clone()
    move = new_state.private.beliefs.get("_temp_generate_move")

    # Acknowledge the command
    if move is not None:
        text = f"I understand: {move.content}"
    else:
        text = "I understand."

    new_state.private.beliefs["_temp_generated_text"] = text
    return new_state


def _generate_question_text(state: InformationState) -> InformationState:
    """Generate text for a question move with plan awareness."""
    new_state = state.clone()
    move = new_state.private.beliefs.get("_temp_generate_move")

    if move is None:
        new_state.private.beliefs["_temp_generated_text"] = "What?"
        return new_state

    question = move.content

    # Check for active plan
    active_plan = _get_active_plan(state)

    if active_plan:
        # Plan-driven generation
        if active_plan.plan_type == "nda_drafting":
            text = _generate_nda_question(question, active_plan, state)
        else:
            # Fallback for unknown plan types
            text = _generate_generic_question(question)
    else:
        # No active plan - use generic
        text = _generate_generic_question(question)

    new_state.private.beliefs["_temp_generated_text"] = text
    return new_state


def _generate_generic_question(question: WhQuestion | YNQuestion | AltQuestion) -> str:
    """Generate generic question text (existing logic).

    Args:
        question: Question object (WhQuestion, YNQuestion, or AltQuestion)

    Returns:
        Generated question text
    """
    if isinstance(question, WhQuestion):
        # Generate wh-question text
        wh_word = question.constraints.get("wh_word", "what")

        # Special case for common questions
        if question.predicate == "how_can_i_help":
            return "How can I help you?"
        elif question.predicate == "clarification_needed":
            return "Could you please clarify what you mean?"
        else:
            # Generic wh-question
            predicate = question.predicate.replace("_", " ")
            return f"{wh_word.capitalize()} {predicate}?"

    elif isinstance(question, YNQuestion):
        # Generate yes/no question text
        proposition = question.proposition.replace("_", " ")
        return f"{proposition.capitalize()}?"

    else:  # AltQuestion
        # Generate alternative question text
        if len(question.alternatives) == 2:
            return f"{question.alternatives[0].capitalize()} or {question.alternatives[1]}?"
        else:
            alt_list = ", ".join(question.alternatives[:-1])
            return f"{alt_list.capitalize()}, or {question.alternatives[-1]}?"


def _generate_nda_question(
    question: WhQuestion | YNQuestion | AltQuestion, plan: Plan, state: InformationState
) -> str:
    """Generate NDA-specific question with context and progress.

    Uses domain model descriptions for better phrasing and adds progress feedback.

    Args:
        question: Question object
        plan: Active NDA plan
        state: Information state

    Returns:
        Generated question text with context
    """
    completed, total = _get_plan_progress(plan)
    domain = _get_domain_for_plan(plan)

    # Get predicate description from domain (if available)
    predicate_desc = None
    if domain and isinstance(question, WhQuestion) and question.predicate in domain.predicates:
        predicate_desc = domain.predicates[question.predicate].description

    # Generate question based on predicate
    if isinstance(question, WhQuestion):
        if question.predicate == "legal_entities":
            # Parties question
            text = "What are the names of the parties entering into this NDA?"
        elif question.predicate == "date":
            # Effective date question
            text = "What is the effective date for the NDA?"
        elif question.predicate == "time_period":
            # Duration question
            text = (
                "How long should the confidentiality obligations last? (e.g., '2 years', '5 years')"
            )
        else:
            # Fallback to generic with predicate description
            if predicate_desc:
                text = f"{predicate_desc}?"
            else:
                predicate = question.predicate.replace("_", " ")
                text = f"What {predicate}?"

    elif isinstance(question, AltQuestion):
        # Alternative questions - use domain sorts if available
        if "mutual" in question.alternatives or "one-way" in question.alternatives:
            # NDA type question
            alt_text = " or ".join(question.alternatives)
            text = f"Should this be a {alt_text} NDA?"
        elif "California" in question.alternatives or "Delaware" in question.alternatives:
            # Jurisdiction question
            states = ", ".join(question.alternatives[:-1])
            last_state = question.alternatives[-1]
            if len(question.alternatives) == 2:
                first = question.alternatives[0]
                second = question.alternatives[1]
                text = f"Which state's law should govern the NDA: {first} or {second}?"
            else:
                text = f"Which state's law should govern the NDA: {states}, or {last_state}?"
        else:
            # Generic alternative question
            text = _generate_generic_question(question)

    else:  # YNQuestion
        # Yes/no questions
        text = _generate_generic_question(question)

    # Add progress indicator if not first question
    if completed > 0:
        text = f"[Step {completed + 1} of {total}] {text}"

    return text


def _generate_answer_text(state: InformationState) -> InformationState:
    """Generate text for an answer move."""
    new_state = state.clone()
    move = new_state.private.beliefs.get("_temp_generate_move")

    if move is None:
        new_state.private.beliefs["_temp_generated_text"] = "I don't have an answer."
        return new_state

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

    if move is None:
        new_state.private.beliefs["_temp_generated_text"] = "OK."
        return new_state

    content = move.content

    # Ensure proper sentence format
    if isinstance(content, str):
        text = content if content.endswith((".", "!", "?")) else f"{content}."
    else:
        text = f"{str(content)}."

    new_state.private.beliefs["_temp_generated_text"] = text
    return new_state
