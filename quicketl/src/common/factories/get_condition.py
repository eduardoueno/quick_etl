"""Condition Factories

A condition is a combination of multiple predicates.
"""

from typing import List
from quicketl.src.common.dtos.time_travel.condition import Condition
from quicketl.src.common.dtos.time_travel.predicate import (
    Predicate,
)
from quicketl.src.common.factories.get_predicate import get_predicate
from quicketl.src.common.utils import get_operator


def get_condition(predicates: List[Predicate]) -> Condition:
    return Condition(**{"predicates": predicates})


def get_condition_from_text_predicates(predicates: List[str]):
    _predicates = []
    for predicate in predicates:
        operator = get_operator(predicate)
        splitted = filter.split(operator)
        target = splitted[0]
        value = splitted[1]
        _predicates.append(
            get_predicate(column_name=target, operator=operator, value=value)
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
