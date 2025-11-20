"""Legal domain model with RAG (Retrieval-Augmented Generation) support.

Demonstrates RAG pattern for legal question answering:
- Query formulation from user questions
- Document retrieval (mocked with realistic legal documents)
- Relevance filtering (some relevant, some not)
- Answer synthesis from retrieved documents

This domain supports legal consultation dialogues where users ask questions
like "what is the controlling law?" and the system retrieves and presents
relevant legal information.
"""

from typing import Any, cast

from ibdm.core.actions import Action, Proposition
from ibdm.core.domain import DomainModel
from ibdm.core.plans import Plan
from ibdm.core.questions import WhQuestion


def create_legal_domain() -> DomainModel:
    """Create legal consultation domain model with RAG support.

    Defines:
    • Predicates: jurisdiction, contract_type, legal_question, governing_law
    • Sorts: us_state, contract_kind, legal_topic
    • Plan builder: legal_consultation
    • RAG action: query_legal_database

    Returns:
        Configured DomainModel for legal consultation with RAG
    """
    domain = DomainModel(name="legal_consultation")

    # Define predicates
    domain.add_predicate(
        "jurisdiction",
        arity=1,
        arg_types=["us_state"],
        description="Legal jurisdiction for the matter",
    )
    domain.add_predicate(
        "contract_type",
        arity=1,
        arg_types=["contract_kind"],
        description="Type of contract being reviewed",
    )
    domain.add_predicate(
        "legal_question",
        arity=1,
        arg_types=["legal_topic"],
        description="Legal question or topic of interest",
    )
    domain.add_predicate(
        "governing_law",
        arity=1,
        arg_types=["us_state"],
        description="Controlling law for the contract",
    )

    # Define sorts
    domain.add_sort("us_state", ["California", "Delaware", "New York", "Texas", "Massachusetts"])
    domain.add_sort("contract_kind", ["employment", "nda", "service_agreement", "sales", "lease"])
    domain.add_sort(
        "legal_topic", ["governing_law", "liability", "termination", "arbitration", "damages"]
    )

    # Register plan builder
    domain.register_plan_builder("legal_consultation", _build_legal_consultation_plan)

    # Register RAG action functions
    domain.register_precond_function("query_legal_database", _check_query_legal_database_precond)
    domain.register_postcond_function("query_legal_database", _query_legal_database_postcond)

    # Note: Action executor (_execute_rag_query) is called directly from demo scripts
    # Domain model doesn't have register_action_executor method yet

    return domain


def _build_legal_consultation_plan(context: dict[str, Any]) -> Plan:
    """Build legal consultation plan.

    Creates a plan for answering legal questions via RAG.

    Args:
        context: Context dict with optional query details

    Returns:
        Plan with findout and perform subplans
    """
    subplans = [
        Plan(
            plan_type="findout",
            content=WhQuestion(variable="contract_type", predicate="contract_type"),
            status="active",
        ),
        Plan(
            plan_type="findout",
            content=WhQuestion(variable="jurisdiction", predicate="jurisdiction"),
            status="active",
        ),
        Plan(
            plan_type="findout",
            content=WhQuestion(variable="legal_question", predicate="legal_question"),
            status="active",
        ),
        Plan(
            plan_type="perform",
            content="query_legal_database",
            status="pending",
        ),
    ]

    return Plan(
        plan_type="legal_consultation",
        content="legal_research",
        status="active",
        subplans=subplans,
    )


# ============================================================================
# RAG Action Functions
# ============================================================================


def _check_query_legal_database_precond(action: Action, commitments: set[str]) -> tuple[bool, str]:
    """Check preconditions for querying legal database.

    Requires:
    - Contract type
    - Jurisdiction
    - Legal question

    Args:
        action: query_legal_database action
        commitments: Current commitments

    Returns:
        Tuple of (satisfied, error_message)
    """
    required_fields = ["contract_type", "jurisdiction", "legal_question"]

    missing_fields = []
    for field in required_fields:
        if not any(field in commit for commit in commitments):
            missing_fields.append(field)

    if missing_fields:
        return (False, f"Missing required information: {', '.join(missing_fields)}")

    return (True, "")


def _query_legal_database_postcond(action: Action) -> list[Proposition]:
    """Generate postconditions for RAG query.

    Creates propositions indicating:
    - Query executed
    - Documents retrieved
    - Answer synthesized

    Args:
        action: query_legal_database action

    Returns:
        List of postcondition propositions
    """
    query_id = action.parameters.get("query_id", "QUERY_001")
    num_docs = action.parameters.get("num_docs_retrieved", 5)
    num_relevant = action.parameters.get("num_docs_relevant", 2)

    return [
        Proposition(
            predicate="query_executed",
            arguments={
                "query_id": query_id,
                "docs_retrieved": num_docs,
                "docs_relevant": num_relevant,
            },
        ),
        Proposition(
            predicate="answer_synthesized",
            arguments={
                "query_id": query_id,
                "status": "ready",
            },
        ),
    ]


def _execute_rag_query(action: Action, state: Any) -> dict[str, Any]:
    """Execute RAG query (MOCKED implementation showing the pattern).

    This demonstrates the RAG pattern:
    1. Query formulation from user's legal question
    2. Document retrieval (returns multiple documents)
    3. Relevance scoring (some relevant, some not)
    4. Answer synthesis from relevant documents

    Args:
        action: query_legal_database action with query parameters
        state: Current information state

    Returns:
        Dictionary with retrieved documents and synthesized answer
    """
    # Extract query parameters
    contract_type = action.parameters.get("contract_type", "unknown")
    jurisdiction = action.parameters.get("jurisdiction", "unknown")
    legal_question = action.parameters.get("legal_question", "unknown")

    # Mock document database
    mock_legal_documents = [
        {
            "doc_id": "CAL_CIVIL_CODE_1646",
            "title": "California Civil Code § 1646 - Choice of Law",
            "content": (
                "A contract is to be interpreted according to the law and usage "
                "of the place where it is to be performed; or, if it does not "
                "indicate a place of performance, according to the law and usage "
                "of the place where it is made."
            ),
            "jurisdiction": "California",
            "relevance_score": 0.95
            if jurisdiction.lower() == "california" and "governing_law" in legal_question.lower()
            else 0.3,
            "tags": ["choice_of_law", "governing_law", "contract_interpretation"],
        },
        {
            "doc_id": "DEL_CODE_T6_2708",
            "title": "Delaware Code Title 6 § 2708 - Governing Law",
            "content": (
                "The parties may choose the law that will govern their contract. "
                "If they do not choose, the law of the state with the most "
                "significant relationship to the transaction governs."
            ),
            "jurisdiction": "Delaware",
            "relevance_score": 0.92
            if jurisdiction.lower() == "delaware" and "governing_law" in legal_question.lower()
            else 0.25,
            "tags": ["choice_of_law", "governing_law", "party_autonomy"],
        },
        {
            "doc_id": "NY_GEN_OBLIG_5_1401",
            "title": "New York General Obligations Law § 5-1401 - Choice of Law",
            "content": (
                "The parties to any contract may agree that the law of New York "
                "shall govern their rights and duties in whole or in part. "
                "Such an agreement is valid if the contract involves at least $250,000."
            ),
            "jurisdiction": "New York",
            "relevance_score": 0.90
            if jurisdiction.lower() == "new york" and "governing_law" in legal_question.lower()
            else 0.20,
            "tags": ["choice_of_law", "governing_law", "minimum_amount"],
        },
        {
            "doc_id": "RESTATEMENT_2D_CONTRACTS_187",
            "title": "Restatement (Second) of Contracts § 187 - Law of State Chosen by Parties",
            "content": (
                "The law of the state chosen by the parties to govern their "
                "contractual rights and duties will be applied, except where "
                "the chosen state has no substantial relationship to the parties "
                "or the transaction."
            ),
            "jurisdiction": "General",
            "relevance_score": 0.88 if "governing_law" in legal_question.lower() else 0.15,
            "tags": ["choice_of_law", "governing_law", "restatement"],
        },
        {
            "doc_id": "CAL_LAB_CODE_2802",
            "title": "California Labor Code § 2802 - Employer Reimbursement",
            "content": (
                "An employer shall indemnify their employee for all necessary "
                "expenditures or losses incurred by the employee in direct "
                "consequence of the discharge of their duties."
            ),
            "jurisdiction": "California",
            "relevance_score": 0.10,  # Not relevant to governing law questions
            "tags": ["employment", "reimbursement", "labor_law"],
        },
    ]

    # Filter and rank documents by relevance
    relevant_threshold = 0.5
    retrieved_docs = sorted(
        mock_legal_documents, key=lambda d: cast(float, d["relevance_score"]), reverse=True
    )
    relevant_docs = [
        doc for doc in retrieved_docs if cast(float, doc["relevance_score"]) >= relevant_threshold
    ]

    # Synthesize answer from relevant documents
    if relevant_docs:
        answer = _synthesize_answer_from_docs(relevant_docs, legal_question, jurisdiction)
    else:
        answer = (
            f"I could not find sufficient legal authority on {legal_question} "
            f"for {jurisdiction}. Consider consulting a licensed attorney."
        )

    # Update action parameters with results
    action.parameters["num_docs_retrieved"] = len(retrieved_docs)
    action.parameters["num_docs_relevant"] = len(relevant_docs)
    action.parameters["query_id"] = f"QUERY_{contract_type}_{jurisdiction}_{legal_question}"

    return {
        "query": legal_question,
        "jurisdiction": jurisdiction,
        "contract_type": contract_type,
        "retrieved_documents": retrieved_docs,
        "relevant_documents": relevant_docs,
        "synthesized_answer": answer,
        "num_total": len(retrieved_docs),
        "num_relevant": len(relevant_docs),
    }


def _synthesize_answer_from_docs(
    docs: list[dict[str, Any]], question: str, jurisdiction: str
) -> str:
    """Synthesize an answer from relevant documents.

    This is a simple mock synthesis. In a real system, this would use
    an LLM to generate a coherent answer from the retrieved documents.

    Args:
        docs: List of relevant document dictionaries
        question: User's legal question
        jurisdiction: Relevant jurisdiction

    Returns:
        Synthesized answer string
    """
    if not docs:
        return "No relevant information found."

    # Simple synthesis: concatenate top documents
    top_doc = docs[0]

    answer_parts = [
        f"Regarding {question} in {jurisdiction}:",
        "",
        f"The controlling law is governed by {top_doc['title']}:",
        f'"{top_doc["content"]}"',
    ]

    if len(docs) > 1:
        answer_parts.append("")
        answer_parts.append("Additional relevant authorities:")
        for doc in docs[1:]:
            answer_parts.append(f"• {doc['title']}")

    return "\n".join(answer_parts)


# ============================================================================
# Domain Singleton
# ============================================================================


_legal_domain: DomainModel | None = None


def get_legal_domain() -> DomainModel:
    """Get or create legal domain singleton.

    Returns:
        Singleton DomainModel instance for legal consultation
    """
    global _legal_domain
    if _legal_domain is None:
        _legal_domain = create_legal_domain()
    return _legal_domain
