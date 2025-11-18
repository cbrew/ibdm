"""Diff engine for computing state changes.

Computes diffs between StateSnapshots by comparing fields and identifying
what was added, removed, or modified.
"""

from typing import Any

from ibdm.visualization.state_diff import ChangedField, ChangeType, StateDiff
from ibdm.visualization.state_snapshot import StateSnapshot


class DiffEngine:
    """Engine for computing diffs between state snapshots.

    Compares two snapshots field-by-field and generates a StateDiff with
    detailed change information.
    """

    # Fields to compare (tuples/lists)
    COLLECTION_FIELDS = [
        "qud",
        "commitments",
        "plan",
        "agenda",
        "issues",
        "overridden_questions",
        "actions",
    ]

    # Fields to compare (dicts)
    DICT_FIELDS = ["beliefs"]

    # Fields to compare (scalars)
    SCALAR_FIELDS = ["agent_id", "last_move"]

    def compute_diff(self, before: StateSnapshot, after: StateSnapshot) -> StateDiff:
        """Compute diff between two snapshots.

        Args:
            before: State before the change
            after: State after the change

        Returns:
            StateDiff with detailed change information
        """
        diff = StateDiff(before=before, after=after)

        # Compare collection fields
        for field_name in self.COLLECTION_FIELDS:
            changed_field = self._diff_collection(field_name, before, after)
            diff.changed_fields[field_name] = changed_field

        # Compare dict fields
        for field_name in self.DICT_FIELDS:
            changed_field = self._diff_dict(field_name, before, after)
            diff.changed_fields[field_name] = changed_field

        # Compare scalar fields
        for field_name in self.SCALAR_FIELDS:
            changed_field = self._diff_scalar(field_name, before, after)
            diff.changed_fields[field_name] = changed_field

        # Generate summary
        diff.summary = diff.format_summary()

        return diff

    def _diff_collection(
        self, field_name: str, before: StateSnapshot, after: StateSnapshot
    ) -> ChangedField:
        """Diff a collection field (list/tuple).

        Args:
            field_name: Name of the field
            before: Before state
            after: After state

        Returns:
            ChangedField with added/removed items
        """
        before_items = list(before.field_value(field_name))
        after_items = list(after.field_value(field_name))

        # Convert to sets for comparison (using id() for object identity)
        before_ids = {id(item): item for item in before_items}
        after_ids = {id(item): item for item in after_items}

        # Find added and removed by object identity
        added_ids = set(after_ids.keys()) - set(before_ids.keys())
        removed_ids = set(before_ids.keys()) - set(after_ids.keys())

        added_items = [after_ids[item_id] for item_id in added_ids]
        removed_items = [before_ids[item_id] for item_id in removed_ids]

        # Determine change type
        if added_items and removed_items:
            change_type = ChangeType.MODIFIED
        elif added_items:
            change_type = ChangeType.ADDED
        elif removed_items:
            change_type = ChangeType.REMOVED
        else:
            change_type = ChangeType.UNCHANGED

        return ChangedField(
            field_name=field_name,
            change_type=change_type,
            added_items=added_items,
            removed_items=removed_items,
            summary=self._format_collection_summary(field_name, added_items, removed_items),
        )

    def _diff_dict(
        self, field_name: str, before: StateSnapshot, after: StateSnapshot
    ) -> ChangedField:
        """Diff a dictionary field.

        Args:
            field_name: Name of the field
            before: Before state
            after: After state

        Returns:
            ChangedField with added/removed/modified keys
        """
        before_dict: dict[str, Any] = before.field_value(field_name)
        after_dict: dict[str, Any] = after.field_value(field_name)

        before_keys = set(before_dict.keys())
        after_keys = set(after_dict.keys())

        added_keys = after_keys - before_keys
        removed_keys = before_keys - after_keys
        common_keys = before_keys & after_keys

        # Find modified values
        modified_keys = [k for k in common_keys if before_dict[k] != after_dict[k]]

        # Build lists of changes
        added_items = [f"{k}={after_dict[k]}" for k in added_keys]
        removed_items = [f"{k}={before_dict[k]}" for k in removed_keys]
        modified_items = [(f"{k}={before_dict[k]}", f"{k}={after_dict[k]}") for k in modified_keys]

        # Determine change type
        if added_items and removed_items:
            change_type = ChangeType.MODIFIED
        elif added_items or modified_items:
            change_type = ChangeType.ADDED if added_items else ChangeType.MODIFIED
        elif removed_items:
            change_type = ChangeType.REMOVED
        else:
            change_type = ChangeType.UNCHANGED

        return ChangedField(
            field_name=field_name,
            change_type=change_type,
            added_items=added_items,
            removed_items=removed_items,
            modified_items=modified_items,
            summary=self._format_dict_summary(
                field_name, added_items, removed_items, modified_items
            ),
        )

    def _diff_scalar(
        self, field_name: str, before: StateSnapshot, after: StateSnapshot
    ) -> ChangedField:
        """Diff a scalar field.

        Args:
            field_name: Name of the field
            before: Before state
            after: After state

        Returns:
            ChangedField with before/after values
        """
        before_value = before.field_value(field_name)
        after_value = after.field_value(field_name)

        if before_value == after_value:
            change_type = ChangeType.UNCHANGED
        elif before_value is None:
            change_type = ChangeType.ADDED
        elif after_value is None:
            change_type = ChangeType.REMOVED
        else:
            change_type = ChangeType.MODIFIED

        return ChangedField(
            field_name=field_name,
            change_type=change_type,
            before_value=before_value,
            after_value=after_value,
            summary=self._format_scalar_summary(field_name, before_value, after_value, change_type),
        )

    def _format_collection_summary(
        self, field_name: str, added: list[Any], removed: list[Any]
    ) -> str:
        """Format summary for collection changes."""
        if not added and not removed:
            return f"{field_name}: no changes"
        parts = []
        if added:
            parts.append(f"+{len(added)}")
        if removed:
            parts.append(f"-{len(removed)}")
        return f"{field_name}: {'/'.join(parts)}"

    def _format_dict_summary(
        self,
        field_name: str,
        added: list[str],
        removed: list[str],
        modified: list[tuple[str, str]],
    ) -> str:
        """Format summary for dict changes."""
        if not added and not removed and not modified:
            return f"{field_name}: no changes"
        parts = []
        if added:
            parts.append(f"+{len(added)} keys")
        if removed:
            parts.append(f"-{len(removed)} keys")
        if modified:
            parts.append(f"~{len(modified)} modified")
        return f"{field_name}: {', '.join(parts)}"

    def _format_scalar_summary(
        self, field_name: str, before: Any, after: Any, change_type: ChangeType
    ) -> str:
        """Format summary for scalar changes."""
        if change_type == ChangeType.UNCHANGED:
            return f"{field_name}: unchanged"
        elif change_type == ChangeType.ADDED:
            return f"{field_name}: set to {after}"
        elif change_type == ChangeType.REMOVED:
            return f"{field_name}: cleared"
        else:
            return f"{field_name}: {before} → {after}"


# Convenience function
def compute_diff(before: StateSnapshot, after: StateSnapshot) -> StateDiff:
    """Compute diff between two state snapshots.

    Args:
        before: State before the change
        after: State after the change

    Returns:
        StateDiff with detailed change information
    """
    engine = DiffEngine()
    return engine.compute_diff(before, after)
