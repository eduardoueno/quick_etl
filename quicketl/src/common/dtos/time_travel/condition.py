from typing import List
from pydantic import BaseModel, computed_field

from quicketl.src.common.dtos.time_travel.predicate import Predicate


class Condition(BaseModel):
    """multiple predicates"""

    predicates: List[Predicate]

    @computed_field
    @property
    def multi_predicate(self) -> str:
        return " AND ".join(
            [predicate.predicate for predicate in self.predicates]
        )
