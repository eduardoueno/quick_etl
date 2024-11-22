from typing import List

from quicketl.src.common.constants import DateFormat
from quicketl.src.common.dtos.contracts.column import DateColumn
from quicketl.src.common.dtos.time_travel.available_date_columns import (
    AvailableDateColumns,
)


def get_available_date_columns(
    date_columns: List[DateColumn],
) -> AvailableDateColumns:

    available_date_columns = AvailableDateColumns()

    for column in date_columns:

        if (
            DateFormat.YEAR.value in column.formato
            and DateFormat.MONTH.value in column.formato
            and DateFormat.DAY.value in column.formato
        ):
            available_date_columns.date = column

        elif (
            DateFormat.YEAR.value in column.formato
            and DateFormat.MONTH.value in column.formato
        ):
            available_date_columns.year_month = column

        elif (
            DateFormat.YEAR.value in column.formato
            and DateFormat.DAY.value in column.formato
        ):
            available_date_columns.year_day = column

        elif (
            DateFormat.MONTH.value in column.formato
            and DateFormat.DAY.value in column.formato
        ):
            available_date_columns.month_day = column

        elif column.formato == DateFormat.YEAR.value:
            available_date_columns.year = column

        elif column.formato == DateFormat.MONTH.value:
            available_date_columns.month = column

        elif column.formato == DateFormat.DAY.value:
            available_date_columns.day = column

        else:
            raise

    return available_date_columns
