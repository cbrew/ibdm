"""Domain model for Issue-Based Dialogue Management.

Provides semantic grounding for predicates without requiring grammar-based parsing.
Inspired by py-trindikit but adapted for LLM-based NLU.

Based on:
- Larsson, S. (2002). Issue-based Dialogue Management. PhD Thesis.
- py-trindikit: https://github.com/heatherleaf/py-trindikit
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from ibdm.core.actions import Action, Proposition
from ibdm.core.answers import Answer
from ibdm.core.plans import Plan
from ibdm.core.questions import Question


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
    arg_types: list[str] = field(default_factory=lambda: [])
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
        self._plan_builders: dict[str, Callable[[dict[str, Any]], Plan]] = {}
        self._dependencies: dict[str, set[str]] = {}  # predicate -> {prerequisite predicates}
        self._postcond_functions: dict[
            str, Callable[[Action], list[Proposition]]
        ] = {}  # action_name -> postcond function

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

    def register_plan_builder(self, task: str, builder: Callable[[dict[str, Any]], Plan]):
        """Register plan builder function for task.

        Plan builders create dialogue plans for specific tasks.

        Args:
            task: Task identifier (e.g., "nda_drafting")
            builder: Function that takes context dict and returns Plan

        Example:
            >>> def build_nda_plan(context: dict[str, Any]) -> Plan:
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
            return getattr(prop, "predicate") == getattr(question, "predicate")
        return False

    def get_plan(self, task: str, context: dict[str, Any] | None = None) -> Plan:
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

        predicate_name = getattr(question, "predicate")
        pred_spec = self.predicates.get(predicate_name)
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
            Rejects empty values regardless of type.
            For sorts with enumerated values, could check membership.
        """
        # Always reject None or empty string values
        if value is None or str(value).strip() == "":
            return False

        if type_name in self.sorts:
            # For sorts with enumerated values, could check membership
            # For now, we already validated non-empty above
            return True

        # Unknown type - accept any non-empty value
        return True

    def add_dependency(self, predicate: str, depends_on: str | list[str]):
        """Register question dependency.

        Defines that questions about `predicate` depend on questions about
        `depends_on` being answered first.

        Based on Larsson (2002) Section 4.6.4 - DependentIssueAccommodation.

        Args:
            predicate: The dependent predicate (e.g., "price")
            depends_on: One or more prerequisite predicates (e.g., "departure_city")

        Example:
            >>> domain.add_dependency("price", ["departure_city", "travel_date"])
            >>> domain.add_dependency("hotel_price", "destination")
        """
        if isinstance(depends_on, str):
            depends_on = [depends_on]

        if predicate not in self._dependencies:
            self._dependencies[predicate] = set()

        self._dependencies[predicate].update(depends_on)

    def depends(self, question1: Question, question2: Question) -> bool:
        """Check if question1 depends on question2.

        Based on Larsson (2002) Section 4.6.4:
        Q1 depends on Q2 if answering Q2 is a prerequisite for answering Q1.

        Args:
            question1: The dependent question
            question2: The potential prerequisite question

        Returns:
            True if question1 depends on question2

        Example:
            >>> q_price = WhQuestion(variable="x", predicate="price")
            >>> q_city = WhQuestion(variable="y", predicate="departure_city")
            >>> domain.depends(q_price, q_city)  # True if dependency registered
        """
        # Extract predicates from questions
        pred1 = getattr(question1, "predicate", None)
        pred2 = getattr(question2, "predicate", None)

        if not pred1 or not pred2:
            return False

        # Check if pred1 depends on pred2
        return pred2 in self._dependencies.get(pred1, set())

    def get_dependencies(self, question: Question) -> list[str]:
        """Get all prerequisite predicates for a question.

        Args:
            question: Question to check

        Returns:
            List of predicate names that must be answered first

        Example:
            >>> q_price = WhQuestion(variable="x", predicate="price")
            >>> domain.get_dependencies(q_price)
            ['departure_city', 'travel_date']
        """
        predicate = getattr(question, "predicate", None)
        if not predicate:
            return []

        return list(self._dependencies.get(predicate, set()))

    def incompatible(self, prop1: str, prop2: str) -> bool:
        """Check if two propositions/commitments are incompatible.

        Based on Larsson (2002) Section 4.6.6 - QuestionReaccommodation.
        Two propositions are incompatible if they provide conflicting answers
        to the same question.

        Args:
            prop1: First proposition (commitment string, format "question: answer")
            prop2: Second proposition (commitment string)

        Returns:
            True if propositions are incompatible

        Example:
            >>> domain.incompatible(
            ...     "travel_date: april 5th",
            ...     "travel_date: april 4th"
            ... )  # True (different dates for same question)
            >>> domain.incompatible(
            ...     "travel_date: april 5th",
            ...     "destination: London"
            ... )  # False (different questions)

        Note:
            Simple heuristic: same question predicate + different answers = incompatible.
            Domain-specific implementations can override for more sophisticated
            compatibility checking (e.g., semantic similarity, value ranges).
        """
        # Extract question and answer from each proposition
        q1, a1 = self._parse_commitment(prop1)
        q2, a2 = self._parse_commitment(prop2)

        # Not incompatible if can't parse either
        if not q1 or not q2:
            return False

        # Not incompatible if different questions
        if q1 != q2:
            return False

        # Incompatible if same question but different answers
        # Normalize for comparison (strip whitespace, lowercase)
        a1_norm = a1.strip().lower() if a1 else ""
        a2_norm = a2.strip().lower() if a2 else ""

        return a1_norm != a2_norm

    def _parse_commitment(self, commitment: str) -> tuple[str | None, str | None]:
        """Parse commitment string into question and answer.

        Args:
            commitment: Commitment string (format "question: answer")

        Returns:
            Tuple of (question_str, answer_str), or (None, None) if invalid

        Example:
            >>> domain._parse_commitment("travel_date: april 5th")
            ("travel_date", "april 5th")
        """
        if ":" not in commitment:
            return (None, None)

        parts = commitment.split(":", 1)
        if len(parts) != 2:
            return (None, None)

        question_str = parts[0].strip()
        answer_str = parts[1].strip()

        return (question_str, answer_str)

    def get_question_from_commitment(self, commitment: str) -> Question | None:
        """Extract question object from commitment string.

        Based on Larsson (2002) Section 4.6.6 - used for reaccommodation.

        Args:
            commitment: Commitment string (format "question: answer")

        Returns:
            Question object, or None if can't extract

        Example:
            >>> q = domain.get_question_from_commitment("travel_date: april 5th")
            >>> q.predicate  # "travel_date"

        Note:
            Reconstructs WhQuestion from predicate name in commitment.
            Assumes commitments use predicate names as question identifiers.
        """
        question_str, _ = self._parse_commitment(commitment)
        if not question_str:
            return None

        # Try to match against known predicates
        # Check if it's a WhQuestion predicate (most common case)
        if question_str in self.predicates:
            from ibdm.core import WhQuestion

            return WhQuestion(predicate=question_str, variable="X")

        # Check if it matches string representation of a question
        # (for questions with constraints or other attributes)
        # For now, just create basic WhQuestion
        from ibdm.core import WhQuestion

        return WhQuestion(predicate=question_str, variable="X")

    def register_postcond_function(
        self,
        action_name: str,
        postcond_fn: Callable[[Action], list[Proposition]],
    ):
        """Register postcondition generator for an action.

        Based on Larsson (2002) Section 5.3.2 (Actions and Postconditions).

        Args:
            action_name: Name of the action (e.g., "book_hotel", "generate_draft")
            postcond_fn: Function that takes Action and returns list of Propositions

        Example:
            >>> def book_hotel_postconds(action: Action) -> list[Proposition]:
            ...     hotel_id = action.parameters.get("hotel_id", "unknown")
            ...     return [Proposition(
            ...         predicate="booked",
            ...         arguments={"hotel_id": hotel_id}
            ...     )]
            >>> domain.register_postcond_function("book_hotel", book_hotel_postconds)
        """
        self._postcond_functions[action_name] = postcond_fn

    def has_postcond_function(self, action_name: str) -> bool:
        """Check if a postcondition function is registered for an action.

        Args:
            action_name: Name of the action to check

        Returns:
            True if a postcondition function is registered
        """
        return action_name in self._postcond_functions

    def postcond(self, action: Action) -> list[Proposition]:
        """Get postconditions for an action.

        Returns propositions that become true after successful action execution.
        These are typically added to commitments after the action executes.

        Based on Larsson (2002) Section 5.3.2 (Actions and Postconditions).

        Args:
            action: Action to get postconditions for

        Returns:
            List of Propositions that will be true after action execution.
            Returns empty list if no postcondition function registered.

        Example:
            >>> action = Action(
            ...     action_type=ActionType.BOOK,
            ...     name="book_hotel",
            ...     parameters={"hotel_id": "H123", "check_in": "2025-01-05"}
            ... )
            >>> postconds = domain.postcond(action)
            >>> # [Proposition(predicate="booked", arguments={"hotel_id": "H123"})]
        """
        # Check if we have a registered postcondition function
        if action.name in self._postcond_functions:
            return self._postcond_functions[action.name](action)

        # Fallback: use action's declared postconditions
        if action.postconditions:
            return self._parse_postconditions_to_propositions(action)

        # No postconditions available
        return []

    def _parse_postconditions_to_propositions(self, action: Action) -> list[Proposition]:
        """Convert action's string postconditions to Proposition objects.

        Internal helper for postcond() method.

        Args:
            action: Action with postconditions list

        Returns:
            List of Proposition objects parsed from action.postconditions

        Example:
            >>> action = Action(
            ...     action_type=ActionType.BOOK,
            ...     name="book_hotel",
            ...     postconditions=["booked(hotel_id=H123)", "confirmed(booking=true)"]
            ... )
            >>> props = domain._parse_postconditions_to_propositions(action)
            >>> len(props)  # 2
        """
        propositions: list[Proposition] = []

        for postcond_str in action.postconditions:
            # Parse postcondition string (e.g., "booked(hotel_id=H123)")
            # Simple parser for predicate(arg=value) format
            if "(" in postcond_str and postcond_str.endswith(")"):
                # Extract predicate and arguments
                parts = postcond_str.split("(", 1)
                predicate = parts[0].strip()
                args_str = parts[1].rstrip(")")

                # Parse arguments
                arguments: dict[str, Any] = {}
                if args_str:
                    # Simple key=value parser
                    for arg in args_str.split(","):
                        arg = arg.strip()
                        if "=" in arg:
                            key, value = arg.split("=", 1)
                            arguments[key.strip()] = value.strip()

                prop = Proposition(
                    predicate=predicate,
                    arguments=arguments,
                )
                propositions.append(prop)
            else:
                # Simple predicate without arguments
                prop = Proposition(
                    predicate=postcond_str.strip(),
                    arguments={},
                )
                propositions.append(prop)

        return propositions

    def __repr__(self) -> str:
        """String representation of domain model."""
        return (
            f"DomainModel(name={self.name!r}, "
            f"predicates={len(self.predicates)}, "
            f"sorts={len(self.sorts)}, "
            f"plan_builders={len(self._plan_builders)}, "
            f"dependencies={len(self._dependencies)}, "
            f"postcond_functions={len(self._postcond_functions)})"
        )
