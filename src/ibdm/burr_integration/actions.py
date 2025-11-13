"""Burr actions for IBDM control loop.

This module defines the Burr actions that implement the four stages of
the IBDM control loop: interpret, integrate, select, and generate.
"""

from typing import Any

from burr.core import State, action

from ibdm.core import DialogueMove, InformationState
from ibdm.engine import DialogueMoveEngine


@action(reads=["utterance", "speaker", "information_state", "engine"], writes=["moves"])
def interpret(state: State) -> tuple[dict[str, Any], State]:
    """Interpret utterance into dialogue moves.

    Args:
        state: Current Burr state containing utterance, speaker, information_state, and engine

    Returns:
        Tuple of (result dict, updated state)
    """
    utterance: str = state["utterance"]
    speaker: str = state["speaker"]
    info_state_dict: dict = state["information_state"]
    engine: DialogueMoveEngine = state["engine"]

    # Convert dict to InformationState object
    info_state = InformationState.from_dict(info_state_dict)

    # Apply interpretation rules with explicit state (Phase 2: stateless methods)
    moves = engine.interpret(utterance, speaker, info_state)

    # Convert moves to dicts for storage
    moves_dicts = [m.to_dict() for m in moves]

    # Update state with moves as dicts
    result = {"moves": moves_dicts, "move_count": len(moves)}
    return result, state.update(moves=moves_dicts)


@action(reads=["moves", "information_state", "engine"], writes=["information_state", "integrated"])
def integrate(state: State) -> tuple[dict[str, Any], State]:
    """Integrate dialogue moves into information state.

    Args:
        state: Current Burr state containing moves, information_state, and engine

    Returns:
        Tuple of (result dict, updated state with updated information_state)
    """
    moves_dicts: list[dict] = state["moves"]
    info_state_dict: dict = state["information_state"]
    engine: DialogueMoveEngine = state["engine"]

    # Convert from dicts to objects
    moves = [DialogueMove.from_dict(m) for m in moves_dicts]
    info_state = InformationState.from_dict(info_state_dict)

    # Apply each move to update state (Phase 2: functional style)
    updated_info_state = info_state
    for move in moves:
        updated_info_state = engine.integrate(move, updated_info_state)

    # Convert back to dict for storage
    updated_info_state_dict = updated_info_state.to_dict()

    # Mark as integrated
    result = {"integrated": True, "move_count": len(moves)}
    return result, state.update(information_state=updated_info_state_dict, integrated=True)


@action(
    reads=["information_state", "engine"],
    writes=["information_state", "response_move", "has_response"],
)
def select(state: State) -> tuple[dict[str, Any], State]:
    """Select next dialogue action.

    Args:
        state: Current Burr state containing information_state and engine

    Returns:
        Tuple of (result dict, updated state)
    """
    info_state_dict: dict = state["information_state"]
    engine: DialogueMoveEngine = state["engine"]

    # Convert from dict to object
    info_state = InformationState.from_dict(info_state_dict)

    # Check if it's our turn
    if info_state.control.next_speaker != engine.agent_id:
        result = {"has_response": False, "response_move": None}
        return result, state.update(has_response=False, response_move=None)

    # Select action using selection rules (Phase 2: pure function)
    response_move, updated_info_state = engine.select_action(info_state)

    # Convert back to dicts for storage
    updated_info_state_dict = updated_info_state.to_dict()
    response_move_dict = response_move.to_dict() if response_move else None

    has_response = response_move is not None
    result = {"has_response": has_response, "response_move": response_move_dict}

    return result, state.update(
        information_state=updated_info_state_dict,
        has_response=has_response,
        response_move=response_move_dict,
    )


@action(
    reads=["response_move", "information_state", "engine"],
    writes=["information_state", "utterance_text"],
)
def generate(state: State) -> tuple[dict[str, Any], State]:
    """Generate utterance from dialogue move.

    Args:
        state: Current Burr state containing response_move, information_state, and engine

    Returns:
        Tuple of (result dict, updated state with updated information_state)
    """
    response_move_dict: dict | None = state["response_move"]
    info_state_dict: dict = state["information_state"]
    engine: DialogueMoveEngine = state["engine"]

    if response_move_dict is None:
        result = {"utterance_text": ""}
        return result, state.update(utterance_text="")

    # Convert from dicts to objects
    response_move = DialogueMove.from_dict(response_move_dict)
    info_state = InformationState.from_dict(info_state_dict)

    # Generate utterance using generation rules (Phase 2: pure function)
    utterance_text = engine.generate(response_move, info_state)

    # Update move content and integrate our own move
    response_move.content = utterance_text
    updated_info_state = engine.integrate(response_move, info_state)

    # Convert back to dict for storage
    updated_info_state_dict = updated_info_state.to_dict()

    result = {"utterance_text": utterance_text}
    return result, state.update(
        information_state=updated_info_state_dict, utterance_text=utterance_text
    )


@action(reads=[], writes=["information_state", "engine", "ready"])
def initialize(state: State) -> tuple[dict[str, Any], State]:
    """Initialize the dialogue engine and information state.

    Args:
        state: Current Burr state (may contain agent_id, rules, and engine_class)

    Returns:
        Tuple of (result dict, updated state with engine and information_state)
    """
    # Get initialization parameters from state if available
    agent_id = state.get("agent_id", "system")
    rules = state.get("rules", None)
    engine_class = state.get("engine_class", DialogueMoveEngine)
    engine_config = state.get("engine_config", None)

    # Create initial InformationState and convert to dict for Burr State
    information_state = InformationState(agent_id=agent_id)
    information_state_dict = information_state.to_dict()

    # Create engine with appropriate class
    if engine_config is not None:
        # For NLUDialogueEngine or other engines that need config
        engine = engine_class(agent_id=agent_id, rules=rules, config=engine_config)
    else:
        # For basic DialogueMoveEngine
        engine = engine_class(agent_id=agent_id, rules=rules)

    result = {"ready": True, "agent_id": agent_id}
    return result, state.update(engine=engine, information_state=information_state_dict, ready=True)


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
