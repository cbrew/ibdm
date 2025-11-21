"""Structured state trace utilities for scenario execution.

These helpers capture a turn-by-turn snapshot of the Larsson engine state
without converting back to scenario JSON. Snapshots can optionally be
serialized for later inspection or comparison with declared state_changes.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ibdm.core.information_state import InformationState


def _stringify_sequence(seq: list[Any]) -> list[str]:
    """Convert a list of domain objects into readable strings."""
    return [str(item) for item in seq]


@dataclass
class TraceRecord:
    """Single-turn snapshot of the dialogue state."""

    turn: int
    speaker: str
    move_type: str
    qud_top: str | None
    qud_stack: list[str]
    commitments: list[str]
    agenda: list[str]
    plan_stack: list[str]
    pending_system_move: str | None
    state_changes_expected: dict[str, Any] | None = None
    state_deltas: dict[str, Any] | None = None

    @classmethod
    def from_state(
        cls,
        *,
        turn: int,
        speaker: str,
        move_type: str,
        state: InformationState,
        pending_system_move: Any | None,
    ) -> TraceRecord:
        """Build a snapshot from the current InformationState."""

        qud_stack = _stringify_sequence(state.shared.qud)
        qud_top = qud_stack[-1] if qud_stack else None
        commitments = sorted(state.shared.commitments)
        agenda = _stringify_sequence(state.private.agenda)
        plan_stack = _stringify_sequence(state.private.plan)

        return cls(
            turn=turn,
            speaker=speaker,
            move_type=move_type,
            qud_top=qud_top,
            qud_stack=qud_stack,
            commitments=commitments,
            agenda=agenda,
            plan_stack=plan_stack,
            pending_system_move=str(pending_system_move) if pending_system_move else None,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-friendly dictionary."""
        return {
            "turn": self.turn,
            "speaker": self.speaker,
            "move_type": self.move_type,
            "qud_top": self.qud_top,
            "qud_stack": self.qud_stack,
            "commitments": self.commitments,
            "agenda": self.agenda,
            "plan_stack": self.plan_stack,
            "pending_system_move": self.pending_system_move,
            "state_changes_expected": self.state_changes_expected,
            "state_deltas": self.state_deltas,
        }


class StateTraceRecorder:
    """Collects trace records and optionally writes them to a file."""

    def __init__(self, output_path: Path | None = None) -> None:
        self.output_path = output_path
        self.records: list[TraceRecord] = []
        # Track last values to compute simple deltas
        self._last_commitments: set[str] = set()
        self._last_qud_top: str | None = None

    def record(
        self,
        *,
        turn: int,
        speaker: str,
        move_type: str,
        state: InformationState,
        pending_system_move: Any | None,
        expected_state_changes: dict[str, Any] | None = None,
    ) -> None:
        """Capture a snapshot for a turn."""
        record = TraceRecord.from_state(
            turn=turn,
            speaker=speaker,
            move_type=move_type,
            state=state,
            pending_system_move=pending_system_move,
        )
        record.state_changes_expected = expected_state_changes
        record.state_deltas = self._compute_deltas(record)
        self._last_commitments = set(record.commitments)
        self._last_qud_top = record.qud_top
        self.records.append(record)

    def flush(self) -> None:
        """Write collected records to disk if an output path is set."""
        if self.output_path is None:
            return

        lines = [json.dumps(record.to_dict()) for record in self.records]
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text("\n".join(lines))

    def _compute_deltas(self, record: TraceRecord) -> dict[str, Any]:
        """Compute coarse deltas (commitment adds/removals, qud top changes)."""
        current_commitments = set(record.commitments)
        added = sorted(current_commitments - self._last_commitments)
        removed = sorted(self._last_commitments - current_commitments)
        qud_changed = record.qud_top != self._last_qud_top

        return {
            "commitments_added": added,
            "commitments_removed": removed,
            "qud_changed": qud_changed,
            "qud_top": record.qud_top,
        }
