from typing import List
from pydantic import BaseModel, StrictStr, computed_field

from quicketl.src.common.constants import Operator


class Predicate(BaseModel):
    """A simple predicate"""

    column_name: StrictStr
    operator: Operator
    value: StrictStr

    @computed_field
    @property
    def predicate(self) -> str:
        return f"{self.column_name}{self.operator.value}{self.value}"
