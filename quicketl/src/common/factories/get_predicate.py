from quicketl.src.common.dtos.time_travel.predicate import (
    Predicate,
)


def get_predicate(column_name, operator, value) -> Predicate:

    return Predicate(
        **{"column_name": column_name, "operator": operator, "value": value}
    )
