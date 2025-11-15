"""Domain definitions for IBDM.

Each domain provides:
- Predicate definitions (semantic grounding)
- Sort constraints (valid values)
- Plan builders (dialogue plans for tasks)
"""

from ibdm.domains.nda_domain import get_nda_domain
from ibdm.domains.travel_domain import get_travel_domain

__all__ = [
    "get_nda_domain",
    "get_travel_domain",
]
