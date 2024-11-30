"""Condition Factories

A condition is a combination of multiple predicates.
"""

from typing import Any, Dict, List
from quicketl.src.common.dtos.time_travel.condition import Condition
from quicketl.src.common.dtos.time_travel.predicate import (
    Predicate,
)
from quicketl.src.common.factories.get_predicate import (
    get_predicate_from_text_predicate,
)


def get_condition(predicates: List[Dict[Any, Any] | Predicate]) -> Condition:

    for predicate in predicates:
        if not isinstance(predicate, Predicate) and not isinstance(
            predicate, dict
        ):
            raise

    try:
        return Condition(**{"predicates": predicates})
    except Exception as e:
        raise


def get_condition_from_text_predicates(predicates: List[str]):
    _predicates = []
    for predicate in predicates:
        _predicates.append(
            get_predicate_from_text_predicate(predicate=predicate)
        )

    return get_condition(predicates=_predicates)


def get_condition_from_text_condition(condition: str) -> Condition:

    predicates = condition.split("/")
    return get_condition_from_text_predicates(predicates=predicates)


def get_condition_from_text_conditions(
    conditions: List[str],
) -> List[Condition]:

    _conditions = []
    for condition in conditions:
        _conditions.append(
            get_condition_from_text_condition(condition=condition)
        )

    return _conditions


def join_conditions(conditions: List[Condition]):

    joined = " OR\n".join(
        [condition.multi_predicate for condition in conditions]
    )
    return f"({joined})"
