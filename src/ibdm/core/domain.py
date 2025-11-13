"""Domain model for Issue-Based Dialogue Management.

Provides semantic grounding for predicates without requiring grammar-based parsing.
Inspired by py-trindikit but adapted for LLM-based NLU.

Based on:
- Larsson, S. (2002). Issue-based Dialogue Management. PhD Thesis.
- py-trindikit: https://github.com/heatherleaf/py-trindikit
"""

from dataclasses import dataclass, field
from typing import Any, Callable

from ibdm.core.answers import Answer
from ibdm.core.questions import Question, WhQuestion, YNQuestion
from ibdm.core.plans import Plan


@dataclass
class PredicateSpec:
    """Specification for a domain predicate.

    Defines the signature and semantics of a predicate used in dialogue.

    Attributes:
        name: Predicate name (e.g., "parties", "nda_type")
        arity: Number of arguments (typically 0 or 1 for IBDM)
        arg_types: List of type names for arguments (e.g., ["legal_entities"])
        description: Human-readable description for NLG

    Example:
        PredicateSpec(
            name="parties",
            arity=1,
            arg_types=["legal_entities"],
            description="Organizations entering into NDA"
        )
    """

    name: str
    arity: int
    arg_types: list[str] = field(default_factory=list)
    description: str = ""


class DomainModel:
    """Lightweight domain model for IBDM.

    Provides semantic grounding for dialogue management without requiring
    grammar-based parsing. This is the missing layer identified in py-trindikit
    analysis.

    The domain model bridges:
    • NLU's generic entities (ORGANIZATION, TEMPORAL, etc.)
    • IBDM's semantic predicates (legal_entities, effective_date, etc.)

    Provides:
    • Predicate definitions with types
    • Sort constraints (semantic types with valid values)
    • Semantic operations (relevant, resolves)
    • Plan retrieval via registered builders

    Does NOT provide:
    • Grammar-based parsing (use LLM-based NLU instead)
    • Compositional semantics (accept emergent semantics from LLM)
    • Database integration (can add later if needed)

    Based on py-trindikit's Domain class but adapted for modern LLM approach.

    Example:
        >>> domain = DomainModel(name="nda_drafting")
        >>> domain.add_predicate("parties", arity=1, arg_types=["legal_entities"])
        >>> domain.add_sort("nda_kind", ["mutual", "one-way"])
        >>> domain.register_plan_builder("nda_drafting", build_nda_plan)
        >>> plan = domain.get_plan("nda_drafting", {})
    """

    def __init__(self, name: str):
        """Initialize domain model.

        Args:
            name: Domain name (e.g., "nda_drafting", "contract_drafting")
        """
        self.name = name
        self.predicates: dict[str, PredicateSpec] = {}
        self.sorts: dict[str, list[str]] = {}
        self._plan_builders: dict[str, Callable[[dict], Plan]] = {}

    def add_predicate(
        self,
        name: str,
        arity: int,
        arg_types: list[str] | None = None,
        description: str = "",
    ):
        """Register predicate with type signature.

        Args:
            name: Predicate name
            arity: Number of arguments
            arg_types: Type names for arguments (optional)
            description: Human-readable description (optional)

        Example:
            >>> domain.add_predicate(
            ...     "parties",
            ...     arity=1,
            ...     arg_types=["legal_entities"],
            ...     description="Organizations entering into NDA"
            ... )
        """
        self.predicates[name] = PredicateSpec(
            name=name,
            arity=arity,
            arg_types=arg_types or [],
            description=description,
        )

    def add_sort(self, name: str, individuals: list[str]):
        """Register semantic sort with valid values.

        Sorts define semantic types and their valid values.

        Args:
            name: Sort name (e.g., "nda_kind", "us_state")
            individuals: List of valid values

        Example:
            >>> domain.add_sort("nda_kind", ["mutual", "one-way"])
            >>> domain.add_sort("us_state", ["California", "Delaware", "New York"])
        """
        self.sorts[name] = individuals

    def register_plan_builder(self, task: str, builder: Callable[[dict], Plan]):
        """Register plan builder function for task.

        Plan builders create dialogue plans for specific tasks.

        Args:
            task: Task identifier (e.g., "nda_drafting")
            builder: Function that takes context dict and returns Plan

        Example:
            >>> def build_nda_plan(context: dict) -> Plan:
            ...     return Plan(plan_type="nda_drafting", subplans=[...])
            >>> domain.register_plan_builder("nda_drafting", build_nda_plan)
        """
        self._plan_builders[task] = builder

    def resolves(self, answer: Answer, question: Question) -> bool:
        """Check if answer resolves question (with type checking).

        Delegates to Question.resolves_with() but adds domain-level
        type validation using predicate specs and sorts.

        This is a key method from py-trindikit that enables domain-independent
        update rules.

        Args:
            answer: Answer object
            question: Question object

        Returns:
            True if answer resolves question and passes type checking

        Example:
            >>> question = WhQuestion(variable="x", predicate="parties")
            >>> answer = Answer(content="Acme Corp, Beta Inc")
            >>> domain.resolves(answer, question)  # True
            >>> answer_invalid = Answer(content="42")
            >>> domain.resolves(answer_invalid, question)  # True (basic type check)
        """
        # First check basic resolution
        if not question.resolves_with(answer):
            return False

        # Then check types if predicate defined
        return self._check_types(answer, question)

    def relevant(self, prop: Any, question: Question) -> bool:
        """Check semantic relevance.

        Simple heuristic: same predicate = relevant.
        Can be overridden in domain-specific implementations.

        From py-trindikit: used to filter propositions that might resolve
        a question.

        Args:
            prop: Proposition or answer object
            question: Question object

        Returns:
            True if proposition is relevant to question

        Example:
            >>> question = WhQuestion(variable="x", predicate="parties")
            >>> prop = Answer(content="Acme Corp", question_ref=question)
            >>> domain.relevant(prop, question)  # True (same predicate)
        """
        if hasattr(prop, "predicate") and hasattr(question, "predicate"):
            return prop.predicate == question.predicate
        return False

    def get_plan(self, task: str, context: dict | None = None) -> Plan:
        """Get dialogue plan for task.

        Dispatches to registered plan builder. This replaces hardcoded
        plan creation with domain-driven approach.

        Args:
            task: Task identifier
            context: Optional context dict for plan building

        Returns:
            Plan object

        Raises:
            ValueError: If no plan builder registered for task

        Example:
            >>> plan = domain.get_plan("nda_drafting", {})
            >>> assert plan.plan_type == "nda_drafting"
            >>> assert len(plan.subplans) == 5
        """
        if task not in self._plan_builders:
            raise ValueError(f"No plan builder registered for task: {task}")

        return self._plan_builders[task](context or {})

    def _check_types(self, answer: Answer, question: Question) -> bool:
        """Verify answer value has correct type.

        Internal method for type checking based on predicate specs and sorts.

        Args:
            answer: Answer object
            question: Question object

        Returns:
            True if answer type is valid for question predicate
        """
        # Get predicate spec
        if not hasattr(question, "predicate"):
            return True

        pred_spec = self.predicates.get(question.predicate)
        if not pred_spec:
            return True  # No spec, accept

        # Type checking logic
        if pred_spec.arg_types:
            expected_type = pred_spec.arg_types[0]
            return self._value_has_type(answer.content, expected_type)

        return True

    def _value_has_type(self, value: Any, type_name: str) -> bool:
        """Check if value belongs to sort.

        Internal method for type validation.

        Args:
            value: Value to check
            type_name: Expected type/sort name

        Returns:
            True if value is valid for type

        Note:
            Current implementation is permissive - accepts any non-empty value.
            More sophisticated checking can be added based on domain requirements.
        """
        if type_name in self.sorts:
            # For sorts with enumerated values, could check membership
            # For now, accept any non-empty value for sorts
            return value is not None and str(value).strip() != ""
        return True  # Unknown type, accept

    def __repr__(self) -> str:
        """String representation of domain model."""
        return (
            f"DomainModel(name={self.name!r}, "
            f"predicates={len(self.predicates)}, "
            f"sorts={len(self.sorts)}, "
            f"plan_builders={len(self._plan_builders)})"
        )
