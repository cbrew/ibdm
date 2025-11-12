# Task Classification and Domain-Specific NLU

## Overview

The task classification system provides semantic understanding of user intents within specific domains. Instead of simple keyword matching, it uses LLM-based classification to map natural language utterances to structured task representations.

## Architecture

### 1. Domain Model (`src/ibdm/nlu/task_classifier.py`)

Domains are semantic representations of dialogue contexts:

```python
@dataclass
class Domain:
    name: str                              # Domain identifier
    description: str                       # Natural language description
    supported_tasks: list[TaskType]        # Task types in this domain
    task_signatures: dict[TaskType, str]   # Semantic signatures
```

**Example - Legal Documents Domain:**
```python
LEGAL_DOCUMENTS_DOMAIN = Domain(
    name="legal_documents",
    description="Legal document drafting and review including NDAs, contracts, agreements",
    supported_tasks=[TaskType.DRAFT_DOCUMENT, TaskType.REVIEW_DOCUMENT],
    task_signatures={
        TaskType.DRAFT_DOCUMENT: "draft(document_type, parties, terms)",
        TaskType.REVIEW_DOCUMENT: "review(document_type, issues)",
    },
)
```

### 2. Task Types

Semantic task representations (enum):

```python
class TaskType(str, Enum):
    UNKNOWN = "unknown"
    DRAFT_DOCUMENT = "draft_document"
    REVIEW_DOCUMENT = "review_document"
    QUERY_INFORMATION = "query_information"
    BOOK_SERVICE = "book_service"
    CANCEL_SERVICE = "cancel_service"
    MODIFY_SERVICE = "modify_service"
```

### 3. TaskClassifier

LLM-powered classifier that maps utterances to semantic task representations:

```python
classifier = create_task_classifier(use_fast_model=True)
result = classifier.classify("I need to draft an NDA")
# Returns: TaskClassificationResult(
#     task_type="draft_document",
#     domain="legal_documents",
#     parameters={"document_type": "NDA"},
#     confidence=0.95
# )
```

**Key Features:**
- Uses Claude Haiku for fast, cost-effective classification
- Structured output via Pydantic models
- Domain-aware classification
- Parameter extraction from utterances
- Confidence scoring

### 4. Integration with Rules

Rule preconditions use task classification for semantic understanding:

```python
def _is_nda_request(state: InformationState) -> bool:
    """Check if utterance is requesting NDA document generation."""

    # Get or classify utterance
    result = classifier.classify(utterance)

    # Check semantic properties
    is_draft_task = result.task_type == TaskType.DRAFT_DOCUMENT.value
    is_legal_domain = result.domain == "legal_documents"
    is_nda = result.parameters.get("document_type", "").upper() in ["NDA", "NON-DISCLOSURE"]
    is_confident = result.confidence >= 0.7

    return all([is_draft_task, is_legal_domain, is_nda, is_confident])
```

**Benefits:**
- No keyword matching - pure semantic understanding
- Handles phrasing variations robustly
- Domain-specific intent recognition
- Confidence thresholding

## Usage Examples

### Basic Classification

```python
from ibdm.nlu.task_classifier import create_task_classifier

classifier = create_task_classifier()

# Various phrasings of the same intent
utterances = [
    "I need to draft an NDA",
    "Can you help me create a non-disclosure agreement?",
    "Let's prepare a confidentiality agreement",
]

for utterance in utterances:
    result = classifier.classify(utterance)
    print(f"Task: {result.task_type}")
    print(f"Domain: {result.domain}")
    print(f"Parameters: {result.parameters}")
    print(f"Confidence: {result.confidence}")
```

**Output:**
```
Task: draft_document
Domain: legal_documents
Parameters: {'document_type': 'NDA'}
Confidence: 0.95
```

### Custom Domains

```python
from ibdm.nlu.task_classifier import Domain, TaskType, create_task_classifier

# Define a restaurant booking domain
RESTAURANT_DOMAIN = Domain(
    name="restaurant_booking",
    description="Restaurant table reservation and booking management",
    supported_tasks=[
        TaskType.BOOK_SERVICE,
        TaskType.CANCEL_SERVICE,
        TaskType.MODIFY_SERVICE,
    ],
    task_signatures={
        TaskType.BOOK_SERVICE: "book(restaurant, time, party_size)",
        TaskType.CANCEL_SERVICE: "cancel(reservation_id)",
        TaskType.MODIFY_SERVICE: "modify(reservation_id, changes)",
    },
)

# Create classifier with multiple domains
classifier = create_task_classifier(
    domains=[LEGAL_DOCUMENTS_DOMAIN, RESTAURANT_DOMAIN]
)

result = classifier.classify("I need to book a table for 4 at 7pm")
# Returns: task_type="book_service", domain="restaurant_booking"
```

### Integration with Rules

```python
from ibdm.rules.update_rules import UpdateRule

# Create interpretation rule using task classification
UpdateRule(
    name="accommodate_booking_task",
    preconditions=lambda state: _is_booking_request(state),
    effects=lambda state: _create_booking_plan(state),
    priority=12,
    rule_type="interpretation",
)

def _is_booking_request(state: InformationState) -> bool:
    """Check if utterance is a booking request."""
    classifier = _get_task_classifier()
    result = classifier.classify(state.private.beliefs["_temp_utterance"])

    return (
        result.task_type == TaskType.BOOK_SERVICE.value
        and result.domain == "restaurant_booking"
        and result.confidence >= 0.7
    )
```

## Performance

### Model Selection

- **Claude Haiku (default)**: Fast, cost-effective classification
  - Latency: ~200-500ms
  - Cost: $1 per million input tokens, $5 per million output tokens
  - Accuracy: ~95% for well-defined domains

- **Claude Sonnet (optional)**: Higher accuracy for complex cases
  - Use when: Domain boundaries are ambiguous
  - Set: `create_task_classifier(use_fast_model=False)`

### Caching

Classification results are cached in `state.private.beliefs["_cached_task_classification"]` to avoid redundant LLM calls:

```python
# First rule checks and caches
cached_task = state.private.beliefs.get("_cached_task_classification")
if cached_task:
    result = cached_task  # Use cached result
else:
    result = classifier.classify(utterance)  # Call LLM
    state.private.beliefs["_cached_task_classification"] = result  # Cache
```

## Extending the System

### Adding New Domains

1. Define the domain:
```python
FLIGHT_BOOKING_DOMAIN = Domain(
    name="flight_booking",
    description="Flight reservation and travel planning",
    supported_tasks=[TaskType.BOOK_SERVICE, TaskType.CANCEL_SERVICE],
    task_signatures={
        TaskType.BOOK_SERVICE: "book(origin, destination, date, passengers)",
    },
)
```

2. Add to classifier:
```python
classifier = create_task_classifier(
    domains=[LEGAL_DOCUMENTS_DOMAIN, FLIGHT_BOOKING_DOMAIN]
)
```

3. Create domain-specific rules:
```python
UpdateRule(
    name="accommodate_flight_booking",
    preconditions=_is_flight_booking,
    effects=_create_flight_plan,
    priority=12,
)
```

### Adding New Task Types

1. Extend the enum:
```python
class TaskType(str, Enum):
    # ... existing types
    SCHEDULE_MEETING = "schedule_meeting"
    GENERATE_REPORT = "generate_report"
```

2. Add to domain's supported tasks:
```python
domain.supported_tasks.append(TaskType.SCHEDULE_MEETING)
domain.task_signatures[TaskType.SCHEDULE_MEETING] = "schedule(attendees, time, topic)"
```

## Design Principles

1. **Semantic Representation**: Tasks are semantic, not syntactic
   - Bad: Check if utterance contains "draft" and "NDA"
   - Good: Classify intent as `draft_document` with `document_type=NDA`

2. **Domain-Specific**: Each domain has clear boundaries and task signatures
   - Domains: legal_documents, restaurant_booking, flight_booking
   - Tasks within domains: draft_document, review_document (legal)

3. **Separation of Concerns**:
   - NLU layer: Language → Semantic representation (TaskClassifier)
   - Dialogue layer: Semantic representation → Action (Rules)

4. **Robustness**: Handle natural language variations
   - "I need an NDA" ✓
   - "Can you help me create a non-disclosure agreement?" ✓
   - "Let's draft a confidentiality doc" ✓

5. **Confidence-Based**: Always check confidence thresholds
   - Low confidence → Clarification question
   - High confidence → Execute task accommodation

## Related Documentation

- `demos/RULE_DRIVEN_PLAN.md` - Rule-driven dialogue architecture
- `src/ibdm/nlu/task_classifier.py` - Implementation
- `src/ibdm/rules/interpretation_rules.py` - Rule integration
- `CLAUDE.md` - Development policies (Policy #9: LiteLLM integration)
