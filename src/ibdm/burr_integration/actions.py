"""Burr actions for IBDM control loop.

This module defines the Burr actions that implement the four stages of
the IBDM control loop: interpret, integrate, select, and generate.
"""

from typing import Any

from burr.core import State, action

from ibdm.core import DialogueMove
from ibdm.engine import DialogueMoveEngine


@action(reads=["utterance", "speaker", "engine"], writes=["moves"])
def interpret(state: State) -> tuple[dict[str, Any], State]:
    """Interpret utterance into dialogue moves.

    Args:
        state: Current Burr state containing utterance, speaker, and engine

    Returns:
        Tuple of (result dict, updated state)
    """
    utterance: str = state["utterance"]
    speaker: str = state["speaker"]
    engine: DialogueMoveEngine = state["engine"]

    # Apply interpretation rules
    moves = engine.interpret(utterance, speaker)

    # Update state with moves
    result = {"moves": moves, "move_count": len(moves)}
    return result, state.update(moves=moves)


@action(reads=["moves", "engine"], writes=["integrated"])
def integrate(state: State) -> tuple[dict[str, Any], State]:
    """Integrate dialogue moves into information state.

    Args:
        state: Current Burr state containing moves and engine

    Returns:
        Tuple of (result dict, updated state)
    """
    moves: list[DialogueMove] = state["moves"]
    engine: DialogueMoveEngine = state["engine"]

    # Apply each move to update state
    for move in moves:
        engine.state = engine.integrate(move)

    # Mark as integrated
    result = {"integrated": True, "move_count": len(moves)}
    return result, state.update(integrated=True)


@action(reads=["engine"], writes=["response_move", "has_response"])
def select(state: State) -> tuple[dict[str, Any], State]:
    """Select next dialogue action.

    Args:
        state: Current Burr state containing engine

    Returns:
        Tuple of (result dict, updated state)
    """
    engine: DialogueMoveEngine = state["engine"]

    # Check if it's our turn
    if engine.state.control.next_speaker != engine.agent_id:
        result = {"has_response": False, "response_move": None}
        return result, state.update(has_response=False, response_move=None)

    # Select action using selection rules
    response_move = engine.select_action()

    has_response = response_move is not None
    result = {"has_response": has_response, "response_move": response_move}

    return result, state.update(has_response=has_response, response_move=response_move)


@action(reads=["response_move", "engine"], writes=["utterance_text"])
def generate(state: State) -> tuple[dict[str, Any], State]:
    """Generate utterance from dialogue move.

    Args:
        state: Current Burr state containing response_move and engine

    Returns:
        Tuple of (result dict, updated state)
    """
    response_move: DialogueMove | None = state["response_move"]
    engine: DialogueMoveEngine = state["engine"]

    if response_move is None:
        result = {"utterance_text": ""}
        return result, state.update(utterance_text="")

    # Generate utterance using generation rules
    utterance_text = engine.generate(response_move)

    # Update move content and integrate our own move
    response_move.content = utterance_text
    engine.state = engine.integrate(response_move)

    result = {"utterance_text": utterance_text}
    return result, state.update(utterance_text=utterance_text)


@action(reads=["engine"], writes=["ready"])
def initialize(state: State) -> tuple[dict[str, Any], State]:
    """Initialize the dialogue engine.

    Args:
        state: Current Burr state (may contain agent_id and rules)

    Returns:
        Tuple of (result dict, updated state with engine)
    """
    # Get initialization parameters from state if available
    agent_id = state.get("agent_id", "system")
    rules = state.get("rules", None)

    # Create engine
    engine = DialogueMoveEngine(agent_id=agent_id, rules=rules)

    result = {"ready": True, "agent_id": agent_id}
    return result, state.update(engine=engine, ready=True)


@action(reads=[], writes=["utterance", "speaker"])
def receive_input(state: State, utterance: str, speaker: str) -> tuple[dict[str, Any], State]:
    """Receive user input.

    Args:
        state: Current Burr state
        utterance: The input utterance
        speaker: ID of the speaker

    Returns:
        Tuple of (result dict, updated state)
    """
    result = {"utterance": utterance, "speaker": speaker}
    return result, state.update(utterance=utterance, speaker=speaker, integrated=False)


@action(reads=[], writes=[])
def idle(state: State) -> tuple[dict[str, Any], State]:
    """Idle state - waiting for input.

    Args:
        state: Current Burr state

    Returns:
        Tuple of (result dict, state unchanged)
    """
    result = {"status": "idle"}
    return result, state
