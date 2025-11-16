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

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict.

        Returns:
            Dictionary representation suitable for JSON serialization
        """
        from ibdm.core.questions import Question

        # Convert content if it's a Question
        content = self.content
        if isinstance(content, Question):
            content = content.to_dict()

        return {
            "plan_type": self.plan_type,
            "content": content,
            "status": self.status,
            "subplans": [subplan.to_dict() for subplan in self.subplans],
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "Plan":
        """Reconstruct Plan from dict.

        Args:
            data: Dictionary representation from to_dict()

        Returns:
            Reconstructed Plan object
        """
        from ibdm.core.questions import Question

        # Reconstruct content if it's a Question dict
        content: Any = data.get("content")
        if isinstance(content, dict) and "type" in content:
            # Cast to dict[str, Any] for Question.from_dict()
            content_dict: dict[str, Any] = content  # type: ignore[assignment]
            content = Question.from_dict(content_dict)

        return Plan(
            plan_type=data.get("plan_type", ""),
            content=content,
            status=data.get("status", "active"),
            subplans=[Plan.from_dict(sp) for sp in data.get("subplans", [])],
        )
