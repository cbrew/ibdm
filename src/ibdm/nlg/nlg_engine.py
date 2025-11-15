"""NLG Engine for natural language generation.

This module provides a standalone NLG engine that generates natural language
utterances from dialogue moves, returning structured NLG results.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Any

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
from ibdm.nlg.nlg_result import NLGResult

logger = logging.getLogger(__name__)


@dataclass
class NLGEngineConfig:
    """Configuration for NLG engine.

    Attributes:
        default_strategy: Default generation strategy ("template" | "plan_aware" | "llm")
        use_plan_awareness: Whether to use plan context for generation
        use_domain_descriptions: Whether to use domain model descriptions
    """

    default_strategy: str = "plan_aware"
    use_plan_awareness: bool = True
    use_domain_descriptions: bool = True


class NLGEngine:
    """Standalone NLG engine for natural language generation.

    This engine generates natural language utterances from dialogue moves
    and returns structured NLG results. It supports multiple generation
    strategies:
    - Template: Simple template-based generation
    - Plan-aware: Context-aware generation using active plans
    - LLM: LLM-based generation (future enhancement)

    The engine is stateless - it takes a DialogueMove and InformationState
    and returns an NLGResult.

    Example:
        >>> config = NLGEngineConfig()
        >>> engine = NLGEngine(config)
        >>> move = DialogueMove(move_type="greet", content="greeting", speaker="system")
        >>> result = engine.generate(move, state)
        >>> print(result.utterance_text)
        "Hello!"
    """

    def __init__(self, config: NLGEngineConfig | None = None):
        """Initialize the NLG engine.

        Args:
            config: NLG configuration (uses defaults if None)
        """
        self.config = config or NLGEngineConfig()
        logger.info("Initialized NLG engine")

    def generate(self, move: DialogueMove, state: InformationState) -> NLGResult:
        """Generate natural language utterance from dialogue move.

        This is the main entry point for NLG processing. It selects the
        appropriate generation strategy and produces the utterance.

        Args:
            move: The dialogue move to generate text for
            state: Current information state (for context)

        Returns:
            NLG result with generated text and metadata
        """
        start_time = time.time()

        # Determine generation strategy
        strategy = self._select_strategy(move, state)

        # Generate based on strategy
        if strategy == "plan_aware" and self.config.use_plan_awareness:
            utterance_text, generation_rule = self._generate_plan_aware(move, state)
        elif strategy == "template":
            utterance_text, generation_rule = self._generate_template(move, state)
        else:
            # Fallback to template
            utterance_text, generation_rule = self._generate_template(move, state)

        # Build result
        return NLGResult(
            utterance_text=utterance_text,
            strategy=strategy,
            generation_rule=generation_rule,
            tokens_used=0,  # No LLM tokens for template/plan_aware
            latency=time.time() - start_time,
        )

    def _select_strategy(self, move: DialogueMove, state: InformationState) -> str:
        """Select generation strategy based on move and state.

        Args:
            move: Dialogue move
            state: Information state

        Returns:
            Strategy name ("template" | "plan_aware" | "llm")
        """
        # Check if there's an active plan
        if self.config.use_plan_awareness and self._has_active_plan(state):
            # Use plan-aware for questions when we have a plan
            if move.move_type == "ask":
                return "plan_aware"

        # Default to template
        return "template"

    def _has_active_plan(self, state: InformationState) -> bool:
        """Check if there's an active plan.

        Args:
            state: Information state

        Returns:
            True if there's an active plan
        """
        for plan in state.private.plan:
            if plan.is_active():
                return True
        return False

    def _get_active_plan(self, state: InformationState) -> Plan | None:
        """Get currently active plan.

        Args:
            state: Information state

        Returns:
            Active plan or None
        """
        for plan in state.private.plan:
            if plan.is_active():
                return plan
        return None

    def _generate_template(self, move: DialogueMove, state: InformationState) -> tuple[str, str]:
        """Generate using template-based strategy.

        Args:
            move: Dialogue move
            state: Information state

        Returns:
            Tuple of (generated text, generation rule name)
        """
        move_type = move.move_type

        if move_type == "greet":
            if move.content == "greeting_response":
                return ("Hello! How can I help you today?", "generate_greeting")
            return ("Hello!", "generate_greeting")

        elif move_type == "quit":
            if move.content == "quit_response":
                return ("Goodbye! Have a great day!", "generate_quit")
            return ("Goodbye!", "generate_quit")

        elif move_type == "command":
            return (f"I understand: {move.content}", "generate_command")

        elif move_type == "ask":
            text = self._generate_generic_question(move.content)
            return (text, "generate_question")

        elif move_type == "answer":
            text = self._generate_answer(move.content)
            return (text, "generate_answer")

        elif move_type == "assert":
            content = str(move.content)
            text = content if content.endswith((".", "!", "?")) else f"{content}."
            return (text, "generate_assertion")

        else:
            return (str(move.content), "generate_default")

    def _generate_plan_aware(self, move: DialogueMove, state: InformationState) -> tuple[str, str]:
        """Generate using plan-aware strategy.

        Args:
            move: Dialogue move
            state: Information state

        Returns:
            Tuple of (generated text, generation rule name)
        """
        active_plan = self._get_active_plan(state)

        if not active_plan:
            # No active plan - fall back to template
            return self._generate_template(move, state)

        # Plan-driven generation for questions
        if move.move_type == "ask" and active_plan.plan_type == "nda_drafting":
            text = self._generate_nda_question(move.content, active_plan, state)
            return (text, "generate_nda_question")

        # Fall back to template for other cases
        return self._generate_template(move, state)

    def _generate_generic_question(
        self, question: WhQuestion | YNQuestion | AltQuestion | Any
    ) -> str:
        """Generate generic question text.

        Args:
            question: Question object

        Returns:
            Generated question text
        """
        if isinstance(question, WhQuestion):
            wh_word = question.constraints.get("wh_word", "what")

            # Special cases
            if question.predicate == "how_can_i_help":
                return "How can I help you?"
            elif question.predicate == "clarification_needed":
                return "Could you please clarify what you mean?"
            else:
                predicate = question.predicate.replace("_", " ")
                return f"{wh_word.capitalize()} {predicate}?"

        elif isinstance(question, YNQuestion):
            proposition = question.proposition.replace("_", " ")
            return f"{proposition.capitalize()}?"

        elif isinstance(question, AltQuestion):
            if len(question.alternatives) == 2:
                return f"{question.alternatives[0].capitalize()} or {question.alternatives[1]}?"
            else:
                alt_list = ", ".join(question.alternatives[:-1])
                return f"{alt_list.capitalize()}, or {question.alternatives[-1]}?"

        else:
            # Not a recognized question type
            return str(question)

    def _generate_nda_question(
        self,
        question: WhQuestion | YNQuestion | AltQuestion | Any,
        plan: Plan,
        state: InformationState,
    ) -> str:
        """Generate NDA-specific question with plan context.

        Args:
            question: Question object
            plan: Active NDA plan
            state: Information state

        Returns:
            Generated question text with context
        """
        completed, total = self._get_plan_progress(plan)
        domain = self._get_domain_for_plan(plan)

        # Generate based on question type and predicate
        if isinstance(question, WhQuestion):
            if question.predicate == "legal_entities":
                text = "What are the names of the parties entering into this NDA?"
            elif question.predicate == "date":
                text = "What is the effective date for the NDA?"
            elif question.predicate == "time_period":
                text = (
                    "How long should the confidentiality obligations last? "
                    "(e.g., '2 years', '5 years')"
                )
            else:
                # Try to get description from domain
                if (
                    domain
                    and self.config.use_domain_descriptions
                    and question.predicate in domain.predicates
                ):
                    text = f"{domain.predicates[question.predicate].description}?"
                else:
                    predicate = question.predicate.replace("_", " ")
                    text = f"What {predicate}?"

        elif isinstance(question, AltQuestion):
            if "mutual" in question.alternatives or "one-way" in question.alternatives:
                alt_text = " or ".join(question.alternatives)
                text = f"Should this be a {alt_text} NDA?"
            elif "California" in question.alternatives or "Delaware" in question.alternatives:
                if len(question.alternatives) == 2:
                    alt0 = question.alternatives[0]
                    alt1 = question.alternatives[1]
                    text = f"Which state's law should govern the NDA: {alt0} or {alt1}?"
                else:
                    states = ", ".join(question.alternatives[:-1])
                    last_alt = question.alternatives[-1]
                    text = f"Which state's law should govern the NDA: {states}, or {last_alt}?"
            else:
                text = self._generate_generic_question(question)

        else:  # YNQuestion
            text = self._generate_generic_question(question)

        # Add progress indicator
        if completed > 0:
            text = f"[Step {completed + 1} of {total}] {text}"

        return text

    def _generate_answer(self, answer: Answer | Any) -> str:
        """Generate answer text.

        Args:
            answer: Answer object or content

        Returns:
            Generated answer text
        """
        if isinstance(answer, Answer):
            content = answer.content

            if isinstance(content, bool):
                return "Yes." if content else "No."
            elif isinstance(content, str):
                if content.endswith((".", "!", "?")):
                    return content
                else:
                    if answer.question_ref and isinstance(answer.question_ref, WhQuestion):
                        return f"The answer is: {content}."
                    else:
                        return f"{content}."
            else:
                return str(content)
        else:
            return str(answer)

    def _get_plan_progress(self, plan: Plan) -> tuple[int, int]:
        """Get plan progress.

        Args:
            plan: Plan object

        Returns:
            Tuple of (completed_count, total_count)
        """
        if not plan.subplans:
            return (0, 0)

        completed = sum(1 for sp in plan.subplans if sp.status == "completed")
        total = len(plan.subplans)
        return (completed, total)

    def _get_domain_for_plan(self, plan: Plan) -> DomainModel | None:
        """Get domain model for plan.

        Args:
            plan: Plan object

        Returns:
            DomainModel instance or None
        """
        if plan.plan_type == "nda_drafting":
            from ibdm.domains.nda_domain import get_nda_domain

            return get_nda_domain()

        return None

    def __str__(self) -> str:
        """Return string representation."""
        return f"NLGEngine(strategy={self.config.default_strategy})"


def create_nlg_engine(config: NLGEngineConfig | None = None) -> NLGEngine:
    """Convenience function to create an NLG engine.

    Args:
        config: Optional configuration (uses defaults if None)

    Returns:
        Configured NLGEngine

    Example:
        >>> engine = create_nlg_engine()
        >>> move = DialogueMove(move_type="greet", content="greeting", speaker="system")
        >>> result = engine.generate(move, state)
    """
    return NLGEngine(config)
