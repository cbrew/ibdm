"""Persistence and serialization for IBDM data structures.

This module provides functions for serializing and deserializing IBDM objects
to/from dictionaries, JSON, and files.
"""

from ibdm.persistence.serialization import (
    answer_to_dict,
    dialogue_move_to_dict,
    dict_to_answer,
    dict_to_dialogue_move,
    dict_to_information_state,
    dict_to_plan,
    dict_to_question,
    information_state_to_dict,
    information_state_to_json,
    json_to_information_state,
    load_information_state,
    plan_to_dict,
    question_to_dict,
    save_information_state,
)

__all__ = [
    # Question serialization
    "question_to_dict",
    "dict_to_question",
    # Answer serialization
    "answer_to_dict",
    "dict_to_answer",
    # DialogueMove serialization
    "dialogue_move_to_dict",
    "dict_to_dialogue_move",
    # Plan serialization
    "plan_to_dict",
    "dict_to_plan",
    # InformationState serialization
    "information_state_to_dict",
    "dict_to_information_state",
    "information_state_to_json",
    "json_to_information_state",
    # File operations
    "save_information_state",
    "load_information_state",
]
