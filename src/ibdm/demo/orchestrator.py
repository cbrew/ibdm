"""Demo-friendly dialogue orchestrator for Larsson control cycle.

This module provides a lightweight orchestrator that mirrors the Burr-based
state machine but is tailored for scripted demos where we bypass live NLU.
It keeps the ordering of Larsson's stages explicit:

    interpret (mocked) → integrate → select → generate

The orchestrator accepts DialogueMove objects that were already interpreted
from scenario data, applies the real integration/selection rules, and
optionally runs the production NLG engine for compare/replace modes.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import TYPE_CHECKING

from ibdm.core import DialogueMove, InformationState
from ibdm.engine.dialogue_engine import DialogueMoveEngine
from ibdm.rules import RuleSet

if TYPE_CHECKING:
    from ibdm.nlg import NLGEngine
    from ibdm.nlg.nlg_result import NLGResult


class DemoDialogueOrchestrator:
    """Run the Larsson dialogue cycle for scripted Business Demo scenarios."""

    def __init__(
        self,
        *,
        agent_id: str = "system",
        rules: RuleSet | None = None,
        nlg_engine: NLGEngine | None = None,
    ) -> None:
        self.engine = DialogueMoveEngine(agent_id=agent_id, rules=rules)
        self._state = InformationState(agent_id=agent_id)
        self._pending_system_move: DialogueMove | None = None
        self._nlg_engine = nlg_engine
        self._last_nlg_result: NLGResult | None = None

    @property
    def information_state(self) -> InformationState:
        """Expose the current InformationState (for visualization/reporting)."""

        return self._state

    @property
    def pending_system_move(self) -> DialogueMove | None:
        """Return the dialogue move selected during the select phase."""

        return self._pending_system_move

    def process_user_turn(self, moves: Sequence[DialogueMove]) -> DialogueMove | None:
        """Integrate user moves and run selection to prepare the next response."""

        self._apply_moves(moves)
        return self._prepare_system_move()

    def ensure_system_move(self) -> DialogueMove | None:
        """Ensure a system move is selected if it's the engine's turn."""

        if self._pending_system_move is not None:
            return self._pending_system_move

        if self._state.control.next_speaker == self.engine.agent_id:
            return self._prepare_system_move()

        return None

    def _apply_moves(self, moves: Iterable[DialogueMove]) -> None:
        for move in moves:
            self._state = self.engine.integrate(move, self._state)

    def _prepare_system_move(self) -> DialogueMove | None:
        self._pending_system_move, self._state = self.engine.select_action(self._state)
        self._last_nlg_result = None
        return self._pending_system_move

    def complete_system_turn(self) -> DialogueMove | None:
        """Integrate and clear the currently pending system move."""

        if self._pending_system_move is None:
            return None

        move = self._pending_system_move
        self._state = self.engine.integrate(move, self._state)
        self._pending_system_move = None
        self._last_nlg_result = None
        return move

    def generate_pending_system_utterance(self) -> NLGResult | None:
        """Run the NLG engine for the currently selected system move."""

        if self._nlg_engine is None or self._pending_system_move is None:
            return None

        self._last_nlg_result = self._nlg_engine.generate(self._pending_system_move, self._state)
        return self._last_nlg_result

    def generate_from_rules(self, move: DialogueMove | None = None) -> str:
        """Fallback text generation using Larsson generation rules."""

        if move is None:
            move = self._pending_system_move
        if move is None:
            return ""
        return self.engine.generate(move, self._state)

    def reset(self) -> None:
        """Reset orchestrator to a fresh InformationState."""

        self._state = InformationState(agent_id=self.engine.agent_id)
        self._pending_system_move = None
        self._last_nlg_result = None
