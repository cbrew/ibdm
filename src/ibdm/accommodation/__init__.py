"""Accommodation mechanisms for Issue-Based Dialogue Management.

Accommodation handles underspecified utterances, ellipsis resolution,
and plan inference to support natural conversational flow.
"""

from ibdm.accommodation.answer_accommodation import resolve_elliptical_answer
from ibdm.accommodation.plan_inference import infer_plan
from ibdm.accommodation.question_accommodation import accommodate_question
from ibdm.accommodation.task_accommodation import accommodate_task

__all__ = [
    "accommodate_question",
    "accommodate_task",
    "resolve_elliptical_answer",
    "infer_plan",
]
