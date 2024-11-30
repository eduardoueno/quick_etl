from quicketl.src.common.dtos.time_travel.predicate import (
    Predicate,
)
from quicketl.src.common.utils import get_operator


def get_predicate(column_name: str, operator: str, value: str) -> Predicate:
    try:
        return Predicate(
            **{"column_name": column_name, "operator": operator, "value": value}
        )
    except Exception as e:
        raise


def get_predicate_from_text_predicate(predicate: str):

    operator = get_operator(predicate)
    splitted = filter.split(operator)
    target = str(splitted[0]).strip()
    value = str(splitted[1]).strip()

    return get_predicate(column_name=target, operator=operator, value=value)
