"""Serialization and deserialization for IBDM data structures.

Provides functions to convert IBDM objects to/from dictionaries and JSON.
Supports Questions, Answers, DialogueMoves, Plans, and InformationState.
"""

import json
from typing import Any, cast

from ibdm.core import (
    AltQuestion,
    Answer,
    ControlIS,
    DialogueMove,
    InformationState,
    Plan,
    PrivateIS,
    Question,
    SharedIS,
    WhQuestion,
    YNQuestion,
)


def question_to_dict(question: Question) -> dict[str, Any]:
    """Convert a Question to a dictionary.

    Args:
        question: Question object to convert

    Returns:
        Dictionary representation
    """
    if isinstance(question, WhQuestion):
        return {
            "type": "WhQuestion",
            "variable": question.variable,
            "predicate": question.predicate,
            "constraints": question.constraints,
        }
    elif isinstance(question, YNQuestion):
        return {
            "type": "YNQuestion",
            "proposition": question.proposition,
            "parameters": question.parameters,
        }
    elif isinstance(question, AltQuestion):
        return {"type": "AltQuestion", "alternatives": question.alternatives}
    else:
        raise ValueError(f"Unknown question type: {type(question)}")


def dict_to_question(data: dict[str, Any]) -> Question:
    """Convert a dictionary to a Question.

    Args:
        data: Dictionary representation

    Returns:
        Question object
    """
    qtype = data.get("type")
    if qtype == "WhQuestion":
        return WhQuestion(
            variable=data["variable"],
            predicate=data["predicate"],
            constraints=data.get("constraints", {}),
        )
    elif qtype == "YNQuestion":
        return YNQuestion(proposition=data["proposition"], parameters=data.get("parameters", {}))
    elif qtype == "AltQuestion":
        return AltQuestion(alternatives=data.get("alternatives", []))
    else:
        raise ValueError(f"Unknown question type: {qtype}")


def answer_to_dict(answer: Answer) -> dict[str, Any]:
    """Convert an Answer to a dictionary.

    Args:
        answer: Answer object to convert

    Returns:
        Dictionary representation
    """
    return {
        "content": answer.content,
        "question_ref": question_to_dict(answer.question_ref) if answer.question_ref else None,
        "certainty": answer.certainty,
    }


def dict_to_answer(data: dict[str, Any]) -> Answer:
    """Convert a dictionary to an Answer.

    Args:
        data: Dictionary representation

    Returns:
        Answer object
    """
    return Answer(
        content=data["content"],
        question_ref=dict_to_question(data["question_ref"]) if data.get("question_ref") else None,
        certainty=data.get("certainty", 1.0),
    )


def dialogue_move_to_dict(move: DialogueMove) -> dict[str, Any]:
    """Convert a DialogueMove to a dictionary.

    Args:
        move: DialogueMove object to convert

    Returns:
        Dictionary representation
    """
    content = move.content
    # Handle special content types
    if isinstance(content, Question):
        content = question_to_dict(content)
    elif isinstance(content, Answer):
        content = answer_to_dict(content)

    return {
        "move_type": move.move_type,
        "content": content,
        "speaker": move.speaker,
        "timestamp": move.timestamp,
    }


def dict_to_dialogue_move(data: dict[str, Any]) -> DialogueMove:
    """Convert a dictionary to a DialogueMove.

    Args:
        data: Dictionary representation

    Returns:
        DialogueMove object
    """
    content = data["content"]
    # Handle special content types
    if isinstance(content, dict) and "type" in content:
        content_dict = cast(dict[str, Any], content)
        if content_dict["type"] in ["WhQuestion", "YNQuestion", "AltQuestion"]:
            content = dict_to_question(content_dict)
        elif "certainty" in content_dict:  # Heuristic for Answer
            content = dict_to_answer(content_dict)

    return DialogueMove(
        move_type=data["move_type"],
        content=content,
        speaker=data["speaker"],
        timestamp=data["timestamp"],
    )


def plan_to_dict(plan: Plan) -> dict[str, Any]:
    """Convert a Plan to a dictionary.

    Args:
        plan: Plan object to convert

    Returns:
        Dictionary representation
    """
    content = plan.content
    if isinstance(content, Question):
        content = question_to_dict(content)

    return {
        "plan_type": plan.plan_type,
        "content": content,
        "status": plan.status,
        "subplans": [plan_to_dict(sp) for sp in plan.subplans],
    }


def dict_to_plan(data: dict[str, Any]) -> Plan:
    """Convert a dictionary to a Plan.

    Args:
        data: Dictionary representation

    Returns:
        Plan object
    """
    content = data["content"]
    if isinstance(content, dict) and "type" in content:
        content_dict = cast(dict[str, Any], content)
        if content_dict["type"] in ["WhQuestion", "YNQuestion", "AltQuestion"]:
            content = dict_to_question(content_dict)

    return Plan(
        plan_type=data["plan_type"],
        content=content,
        status=data["status"],
        subplans=[dict_to_plan(sp) for sp in data.get("subplans", [])],
    )


def information_state_to_dict(state: InformationState) -> dict[str, Any]:
    """Convert an InformationState to a dictionary.

    Args:
        state: InformationState object to convert

    Returns:
        Dictionary representation
    """
    return {
        "agent_id": state.agent_id,
        "private": {
            "plan": [plan_to_dict(p) for p in state.private.plan],
            "agenda": [dialogue_move_to_dict(m) for m in state.private.agenda],
            "beliefs": state.private.beliefs,
            "last_utterance": (
                dialogue_move_to_dict(state.private.last_utterance)
                if state.private.last_utterance
                else None
            ),
        },
        "shared": {
            "qud": [question_to_dict(q) for q in state.shared.qud],
            "commitments": list(state.shared.commitments),
            "last_moves": [dialogue_move_to_dict(m) for m in state.shared.last_moves],
        },
        "control": {
            "speaker": state.control.speaker,
            "next_speaker": state.control.next_speaker,
            "initiative": state.control.initiative,
            "dialogue_state": state.control.dialogue_state,
        },
    }


def dict_to_information_state(data: dict[str, Any]) -> InformationState:
    """Convert a dictionary to an InformationState.

    Args:
        data: Dictionary representation

    Returns:
        InformationState object
    """
    private_data = data["private"]
    shared_data = data["shared"]
    control_data = data["control"]

    private = PrivateIS(
        plan=[dict_to_plan(p) for p in private_data.get("plan", [])],
        agenda=[dict_to_dialogue_move(m) for m in private_data.get("agenda", [])],
        beliefs=private_data.get("beliefs", {}),
        last_utterance=(
            dict_to_dialogue_move(private_data["last_utterance"])
            if private_data.get("last_utterance")
            else None
        ),
    )

    shared = SharedIS(
        qud=[dict_to_question(q) for q in shared_data.get("qud", [])],
        commitments=set(shared_data.get("commitments", [])),
        last_moves=[dict_to_dialogue_move(m) for m in shared_data.get("last_moves", [])],
    )

    control = ControlIS(
        speaker=control_data.get("speaker", "user"),
        next_speaker=control_data.get("next_speaker", "system"),
        initiative=control_data.get("initiative", "mixed"),
        dialogue_state=control_data.get("dialogue_state", "active"),
    )

    return InformationState(
        agent_id=data["agent_id"], private=private, shared=shared, control=control
    )


# JSON serialization functions


def information_state_to_json(state: InformationState, indent: int | None = 2) -> str:
    """Convert an InformationState to JSON string.

    Args:
        state: InformationState object to convert
        indent: JSON indentation (None for compact)

    Returns:
        JSON string representation
    """
    return json.dumps(information_state_to_dict(state), indent=indent)


def json_to_information_state(json_str: str) -> InformationState:
    """Convert a JSON string to an InformationState.

    Args:
        json_str: JSON string representation

    Returns:
        InformationState object
    """
    data = json.loads(json_str)
    return dict_to_information_state(data)


def save_information_state(state: InformationState, filepath: str) -> None:
    """Save an InformationState to a JSON file.

    Args:
        state: InformationState object to save
        filepath: Path to the output file
    """
    with open(filepath, "w") as f:
        f.write(information_state_to_json(state))


def load_information_state(filepath: str) -> InformationState:
    """Load an InformationState from a JSON file.

    Args:
        filepath: Path to the input file

    Returns:
        InformationState object
    """
    with open(filepath) as f:
        return json_to_information_state(f.read())
