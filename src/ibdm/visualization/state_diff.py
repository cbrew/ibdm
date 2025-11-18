"""State diff representation for visualization.

Represents changes between two state snapshots, with detailed tracking
of what was added, removed, or modified in each field.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from ibdm.visualization.state_snapshot import StateSnapshot


class ChangeType(str, Enum):
    """Type of change in a field."""

    ADDED = "added"  # Item added to collection or field set from None
    REMOVED = "removed"  # Item removed from collection or field set to None
    MODIFIED = "modified"  # Item changed (for scalar values or nested objects)
    UNCHANGED = "unchanged"  # No change


@dataclass
class ChangedField:
    """Represents a change in a specific field.

    Attributes:
        field_name: Name of the field (e.g., "qud", "commitments")
        change_type: Type of change (added/removed/modified/unchanged)
        added_items: Items that were added (for collections)
        removed_items: Items that were removed (for collections)
        modified_items: Items that were modified (for collections of objects)
        before_value: Value before change (for scalar fields)
        after_value: Value after change (for scalar fields)
        summary: Human-readable summary of the change
    """

    field_name: str
    change_type: ChangeType
    added_items: list[Any] = field(default_factory=list)
    removed_items: list[Any] = field(default_factory=list)
    modified_items: list[tuple[Any, Any]] = field(default_factory=list)
    before_value: Any = None
    after_value: Any = None
    summary: str = ""

    def has_changes(self) -> bool:
        """Check if this field has any changes."""
        return (
            self.change_type != ChangeType.UNCHANGED
            or bool(self.added_items)
            or bool(self.removed_items)
            or bool(self.modified_items)
        )

    def change_count(self) -> int:
        """Count total number of changes."""
        return len(self.added_items) + len(self.removed_items) + len(self.modified_items)


@dataclass
class StateDiff:
    """Diff between two state snapshots.

    Computes and stores differences between before/after states for all
    relevant fields. Used for delta visualization and change tracking.

    Attributes:
        before: Snapshot before the change
        after: Snapshot after the change
        changed_fields: Dictionary of field name -> ChangedField
        summary: High-level summary of changes
    """

    before: StateSnapshot
    after: StateSnapshot
    changed_fields: dict[str, ChangedField] = field(default_factory=dict)
    summary: str = ""

    def has_changes(self) -> bool:
        """Check if there are any changes between states."""
        return any(cf.has_changes() for cf in self.changed_fields.values())

    def get_changed_field(self, field_name: str) -> ChangedField | None:
        """Get change information for a specific field."""
        return self.changed_fields.get(field_name)

    def changed_field_names(self) -> list[str]:
        """Get list of field names that changed."""
        return [name for name, cf in self.changed_fields.items() if cf.has_changes()]

    def total_change_count(self) -> int:
        """Count total number of changes across all fields."""
        return sum(cf.change_count() for cf in self.changed_fields.values())

    def format_summary(self) -> str:
        """Generate a summary of changes.

        Returns:
            Human-readable summary like "3 changes: QUD +1, commitments +2"
        """
        if not self.has_changes():
            return "No changes"

        changes = []
        for name in self.changed_field_names():
            cf = self.changed_fields[name]
            added = len(cf.added_items)
            removed = len(cf.removed_items)
            modified = len(cf.modified_items)

            if added and removed:
                changes.append(f"{name} +{added}/-{removed}")
            elif added:
                changes.append(f"{name} +{added}")
            elif removed:
                changes.append(f"{name} -{removed}")
            elif modified:
                changes.append(f"{name} ~{modified}")

        total = self.total_change_count()
        return f"{total} changes: {', '.join(changes)}"

    def __str__(self) -> str:
        """Return string representation."""
        return (
            f"StateDiff(t{self.before.timestamp}→t{self.after.timestamp}, {self.format_summary()})"
        )
