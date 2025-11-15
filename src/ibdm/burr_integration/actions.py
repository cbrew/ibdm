"""Burr actions for IBDM control loop.

This module defines the Burr actions that implement the four stages of
the IBDM control loop: interpret, integrate, select, and generate.
"""

from typing import TYPE_CHECKING, Any

from burr.core import State, action

from ibdm.burr_integration.nlu_context import NLUContext
from ibdm.core import DialogueMove, InformationState
from ibdm.engine import DialogueMoveEngine

if TYPE_CHECKING:
    from ibdm.nlg import NLGEngine
    from ibdm.nlg.nlg_result import NLGResult
    from ibdm.nlu import NLUEngine
    from ibdm.nlu.nlu_result import NLUResult


@action(
    reads=["information_state", "nlu_engine", "nlu_context"],
    writes=["utterance", "speaker", "nlu_result", "nlu_context"],
)
def nlu(state: "State[Any]", utterance: str, speaker: str) -> tuple[dict[str, Any], "State[Any]"]:
    """Process utterance through NLU engine.

    This is the entry point for the 6-stage pipeline. It receives user input
    as parameters (not from state), processes through NLU, and writes both
    the input and results to state for subsequent actions.

    Args:
        state: Current Burr state with information_state, nlu_engine, and nlu_context
        utterance: User utterance (input parameter)
        speaker: Speaker ID (input parameter)

    Returns:
        Tuple of (result dict, updated state with utterance, speaker, nlu_result, nlu_context)
    """
    info_state_dict: dict[str, Any] = state["information_state"]  # type: ignore[index]
    nlu_engine: NLUEngine = state["nlu_engine"]  # type: ignore[index]

    # Get NLU context from state (or create empty if not present)
    nlu_context_dict: dict[str, Any] = state.get("nlu_context", NLUContext.create_empty().to_dict())  # type: ignore[assignment, attr-defined]
    nlu_context = NLUContext.from_dict(nlu_context_dict)

    # Convert dict to InformationState object
    info_state = InformationState.from_dict(info_state_dict)

    # Process utterance through NLU engine
    nlu_result: NLUResult
    updated_nlu_context: NLUContext
    nlu_result, updated_nlu_context = nlu_engine.process(
        utterance, speaker, info_state, nlu_context
    )

    # Convert to dicts for Burr State storage
    nlu_result_dict = nlu_result.to_dict()
    updated_nlu_context_dict = updated_nlu_context.to_dict()

    # Build result
    result = {
        "dialogue_act": nlu_result.dialogue_act,
        "confidence": nlu_result.confidence,
        "latency": nlu_result.latency,
    }

    # Write inputs to state for subsequent actions, along with NLU results
    return result, state.update(
        utterance=utterance,
        speaker=speaker,
        nlu_result=nlu_result_dict,
        nlu_context=updated_nlu_context_dict,
    )


@action(
    reads=["nlu_result", "speaker", "information_state", "engine"],
    writes=["moves"],
)
def interpret(state: "State[Any]") -> tuple[dict[str, Any], "State[Any]"]:
    """Interpret NLU result into dialogue moves.

    In the 6-stage pipeline, this action reads nlu_result from state
    (produced by the nlu() action) and creates DialogueMoves from it.

    Args:
        state: Current Burr state with nlu_result, speaker, information_state, engine

    Returns:
        Tuple of (result dict, updated state with moves)
    """
    nlu_result_dict: dict[str, Any] | None = state.get("nlu_result")  # type: ignore[assignment, attr-defined]
    speaker: str = state["speaker"]  # type: ignore[index]
    info_state_dict: dict[str, Any] = state["information_state"]  # type: ignore[index]
    engine: DialogueMoveEngine = state["engine"]  # type: ignore[index]

    # Convert dict to InformationState object
    info_state = InformationState.from_dict(info_state_dict)

    # Check if we have nlu_result (6-stage pipeline)
    if nlu_result_dict is not None:
        # Import locally within function to avoid circular imports at module level
        # This works because ibdm.nlu module is fully initialized by the time
        # this function runs (it's only called after app is built)
        import ibdm.nlu.nlu_result

        # Convert nlu_result dict to NLUResult object
        nlu_result = ibdm.nlu.nlu_result.NLUResult.from_dict(nlu_result_dict)

        # Use new interpret_from_nlu_result method
        moves = engine.interpret_from_nlu_result(nlu_result, speaker, info_state)

        # Convert moves to dicts for storage
        moves_dicts: list[dict[str, Any]] = [m.to_dict() for m in moves]

        # Update state with moves
        result = {"moves": moves_dicts, "move_count": len(moves)}
        return result, state.update(moves=moves_dicts)

    # Backward compatibility: if no nlu_result, try old interpretation methods
    utterance: str = state.get("utterance", "")  # type: ignore[assignment]

    # Check if engine supports NLU context (Phase 4: NLU state integration)
    if hasattr(engine, "interpret_with_nlu_context"):
        # Get NLU context from state (or create empty if not present)
        nlu_context_dict: dict[str, Any] = state.get(
            "nlu_context", NLUContext.create_empty().to_dict()
        )  # type: ignore[assignment, attr-defined]
        nlu_context = NLUContext.from_dict(nlu_context_dict)

        # Use NLU-aware interpretation
        moves_list: list[DialogueMove]
        updated_nlu_context: NLUContext
        moves_list, updated_nlu_context = engine.interpret_with_nlu_context(  # type: ignore[attr-defined]
            utterance, speaker, info_state, nlu_context
        )

        # Convert moves and NLU context to dicts for storage
        moves_dicts = [m.to_dict() for m in moves_list]
        updated_nlu_context_dict: dict[str, Any] = updated_nlu_context.to_dict()

        # Update state with moves and NLU context
        result = {"moves": moves_dicts, "move_count": len(moves_list)}
        return result, state.update(moves=moves_dicts, nlu_context=updated_nlu_context_dict)
    else:
        # Use standard interpretation (backward compatibility)
        moves_list = engine.interpret(utterance, speaker, info_state)

        # Convert moves to dicts for storage
        moves_dicts = [m.to_dict() for m in moves_list]

        # Update state with moves as dicts
        result = {"moves": moves_dicts, "move_count": len(moves_list)}
        return result, state.update(moves=moves_dicts)


@action(reads=["moves", "information_state", "engine"], writes=["information_state", "integrated"])
def integrate(state: "State[Any]") -> tuple[dict[str, Any], "State[Any]"]:
    """Integrate dialogue moves into information state.

    Args:
        state: Current Burr state containing moves, information_state, and engine

    Returns:
        Tuple of (result dict, updated state with updated information_state)
    """
    moves_dicts: list[dict[str, Any]] = state["moves"]  # type: ignore[index]
    info_state_dict: dict[str, Any] = state["information_state"]  # type: ignore[index]
    engine: DialogueMoveEngine = state["engine"]  # type: ignore[index]

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
def select(state: "State[Any]") -> tuple[dict[str, Any], "State[Any]"]:
    """Select next dialogue action.

    Args:
        state: Current Burr state containing information_state and engine

    Returns:
        Tuple of (result dict, updated state)
    """
    info_state_dict: dict[str, Any] = state["information_state"]  # type: ignore[index]
    engine: DialogueMoveEngine = state["engine"]  # type: ignore[index]

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
    reads=["response_move", "information_state", "nlg_engine"],
    writes=["utterance_text", "nlg_result"],
)
def nlg(state: "State[Any]") -> tuple[dict[str, Any], "State[Any]"]:
    """Generate natural language utterance from dialogue move.

    Args:
        state: Current Burr state containing response_move, information_state, and nlg_engine

    Returns:
        Tuple of (result dict, updated state with utterance_text and nlg_result)
    """
    response_move_dict: dict[str, Any] | None = state["response_move"]  # type: ignore[index]
    info_state_dict: dict[str, Any] = state["information_state"]  # type: ignore[index]
    nlg_engine: NLGEngine = state["nlg_engine"]  # type: ignore[index]

    if response_move_dict is None:
        result = {"utterance_text": ""}
        return result, state.update(utterance_text="")

    # Convert from dicts to objects
    response_move = DialogueMove.from_dict(response_move_dict)
    info_state = InformationState.from_dict(info_state_dict)

    # Generate utterance using NLG engine
    nlg_result: NLGResult = nlg_engine.generate(response_move, info_state)

    # Convert to dict for Burr State storage
    nlg_result_dict = nlg_result.to_dict()

    # Build result
    result = {
        "utterance_text": nlg_result.utterance_text,
        "strategy": nlg_result.strategy,
        "latency": nlg_result.latency,
    }

    return result, state.update(
        utterance_text=nlg_result.utterance_text, nlg_result=nlg_result_dict
    )


@action(
    reads=["response_move", "information_state", "nlg_engine", "engine"],
    writes=["information_state", "utterance_text", "nlg_result"],
)
def generate(state: "State[Any]") -> tuple[dict[str, Any], "State[Any]"]:
    """Generate utterance from dialogue move.

    In the 6-stage pipeline, this action uses nlg_engine if available.
    Falls back to engine.generate() for backward compatibility.

    Args:
        state: Current Burr state containing response_move, information_state, nlg_engine, engine

    Returns:
        Tuple of (result dict, updated state with utterance_text)
    """
    response_move_dict: dict[str, Any] | None = state["response_move"]  # type: ignore[index]
    info_state_dict: dict[str, Any] = state["information_state"]  # type: ignore[index]
    nlg_engine: NLGEngine | None = state.get("nlg_engine")  # type: ignore[assignment, attr-defined]
    engine: DialogueMoveEngine = state["engine"]  # type: ignore[index]

    if response_move_dict is None:
        result = {"utterance_text": ""}
        return result, state.update(utterance_text="")

    # Convert from dicts to objects
    response_move = DialogueMove.from_dict(response_move_dict)
    info_state = InformationState.from_dict(info_state_dict)

    # Prefer NLG engine (6-stage pipeline)
    if nlg_engine is not None:
        # Use NLG engine
        nlg_result: NLGResult = nlg_engine.generate(response_move, info_state)
        utterance_text = nlg_result.utterance_text

        # Store NLG result in state
        nlg_result_dict = nlg_result.to_dict()

        # Update move content and integrate our own move
        response_move.content = utterance_text
        updated_info_state = engine.integrate(response_move, info_state)

        # Convert back to dict for storage
        updated_info_state_dict = updated_info_state.to_dict()

        result = {
            "utterance_text": utterance_text,
            "strategy": nlg_result.strategy,
            "latency": nlg_result.latency,
        }
        return result, state.update(
            information_state=updated_info_state_dict,
            utterance_text=utterance_text,
            nlg_result=nlg_result_dict,
        )
    else:
        # Fallback: use engine's generation rules (backward compatibility)
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


@action(reads=[], writes=["information_state", "engine", "nlu_context", "ready"])
def initialize(state: "State[Any]") -> tuple[dict[str, Any], "State[Any]"]:
    """Initialize the dialogue engine, information state, and NLU context.

    Args:
        state: Current Burr state (may contain agent_id, rules, and engine_class)

    Returns:
        Tuple of (result dict, updated state with engine, information_state, and nlu_context)
    """
    # Get initialization parameters from state
    # engine_class is always provided by create_dialogue_application
    agent_id: str = state.get("agent_id", "system")  # type: ignore[assignment]
    rules = state.get("rules", None)  # type: ignore[attr-defined]
    engine_class = state["engine_class"]  # type: ignore[index]
    engine_config = state.get("engine_config", None)  # type: ignore[attr-defined]

    # Create initial InformationState and convert to dict for Burr State
    information_state = InformationState(agent_id=agent_id)
    information_state_dict = information_state.to_dict()

    # Create empty NLU context for Phase 4: NLU state integration
    nlu_context = NLUContext.create_empty()
    nlu_context_dict = nlu_context.to_dict()

    # Create engine with appropriate class
    if engine_config is not None:
        # For NLUDialogueEngine or other engines that need config
        engine = engine_class(agent_id=agent_id, rules=rules, config=engine_config)
    else:
        # For basic DialogueMoveEngine
        engine = engine_class(agent_id=agent_id, rules=rules)

    result = {"ready": True, "agent_id": agent_id}
    return result, state.update(
        engine=engine,
        information_state=information_state_dict,
        nlu_context=nlu_context_dict,
        ready=True,
    )
