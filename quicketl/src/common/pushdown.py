from datetime import datetime
from typing import List

from quicketl.src.common.dtos.time_travel.available_date_columns import (
    AvailableDateColumns,
)
from quicketl.src.common.dtos.time_travel.predicate import Condition


def get_predicates_from_dates(
    dates: List[datetime],
    available_date_columns: AvailableDateColumns,
    optimize: bool = True,
) -> List[Condition]:
    pass
