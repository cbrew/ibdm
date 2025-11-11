"""Plan representations for Issue-Based Dialogue Management.

Plans represent dialogue goals and the strategies to achieve them.
They form a hierarchical structure with plans and subplans.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Plan:
    """Dialogue plan/goal.

    Plans represent dialogue objectives and can be hierarchically decomposed
    into subplans. Common plan types include: findout, raise, respond, perform.
    """

    plan_type: str
    """Type of plan: 'findout', 'raise', 'respond', 'perform', etc."""

    content: Any
    """Content of the plan (Question to find out, action to perform, etc.)"""

    status: str = "active"
    """Status: 'active', 'completed', 'abandoned'"""

    subplans: list["Plan"] = field(default_factory=lambda: [])
    """Subplans that help achieve this plan"""

    def __str__(self) -> str:
        """Return string representation."""
        subplans_str = f" [{len(self.subplans)} subplans]" if self.subplans else ""
        return f"Plan:{self.plan_type}({self.content}){subplans_str} [{self.status}]"

    def is_active(self) -> bool:
        """Check if plan is active."""
        return self.status == "active"

    def complete(self) -> None:
        """Mark plan as completed."""
        self.status = "completed"

    def abandon(self) -> None:
        """Mark plan as abandoned."""
        self.status = "abandoned"
