from enum import Enum
from typing import Any, List

from pydantic import BaseModel

from quicketl.src.common.constants import Operator


def extract_numerical(value: str) -> int:
    return "".join(filter(str.isdigit, value))


def look_for_in_enum(value, enumerate: Enum):

    for kv in enumerate:
        if kv.value in value:
            return kv

    return False


def remove_dups(values: List[Any]):

    # Specific treatment for pydantic BaseModels
    if all([value for value in values if isinstance(value, BaseModel)]):
        dedups = []
        for value in values:
            if value not in dedups:
                dedups.append(value)
        return dedups

    return list(set(values))


def get_operator(filter_as_text: str) -> str:

    operator = look_for_in_enum(value=filter_as_text, enumerate=Operator)

    return operator.value
