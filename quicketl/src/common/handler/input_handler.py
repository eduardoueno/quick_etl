from datetime import datetime
from typing import List

from quicketl.src.common.constants import Operator
from quicketl.src.common.dates import *
from quicketl.src.common.dtos.time_travel.available_date_columns import (
    AvailableDateColumns,
)
from quicketl.src.common.dtos.time_travel.condition import Condition
from quicketl.src.common.dtos.time_travel.predicate import Predicate
from quicketl.src.common.factories.get_condition import (
    get_condition,
    join_conditions,
)
from quicketl.src.common.factories.get_avl_date_columns import (
    get_available_date_columns,
)
from quicketl.src.common.dtos.contracts.input import Input

from quicketl.src.common.factories.get_predicate import (
    get_predicate,
    get_predicate_from_text_predicate,
)
from quicketl.src.common.utils import remove_dups


class InputHandler:

    def __init__(self):
        pass

    def get_categoric_conditions(self, contract: Input) -> List[Condition]:

        if not contract.colunas_particao_categorica:
            return []

        predicates = []
        for column in contract.colunas_particao_categorica:
            predicates.append(get_predicate_from_text_predicate(column.filtro))

        return predicates

    def get_conditions_from_ref(
        self,
        contract: Input,
        reference_date: datetime,
        available_date_columns: AvailableDateColumns,
    ) -> List[Condition]:
        start_date, end_date = get_date_range(
            reference_date=reference_date,
            delay=contract.defasagem,
            window=contract.intervalo_tempo,
        )

        if available_date_columns.date is not None:
            predicates = [
                get_predicate(
                    column_name=available_date_columns.date.nome,
                    operator=Operator.GREATER_EQUAL,
                    value=strdate(start_date),
                ),
                get_predicate(
                    column_name=available_date_columns.date.nome,
                    operator=Operator.LESS_EQUAL,
                    value=strdate(end_date),
                ),
            ]
            return [get_condition(predicates=predicates)]

        if available_date_columns.year_month is not None:
            predicates = [
                get_predicate(
                    column_name=available_date_columns.year_month.nome,
                    operator=Operator.GREATER_EQUAL,
                    value=stryearmonth(start_date),
                ),
                get_predicate(
                    column_name=available_date_columns.year_month.nome,
                    operator=Operator.LESS_EQUAL,
                    value=stryearmonth(end_date),
                ),
            ]
            return [get_condition(predicates=predicates)]

        # This is probably the most common case and with the worst non optimized
        # predicates. Thus we will work hard to increase readability
        dates_between = get_dates_between(
            start_date=start_date, end_date=end_date
        )

        conditions = []
        predicates = None

        # At first we assume we will iter through all dates.
        # No predicates have been calculated and thus, no conditions exist
        dates: List[datetime] = dates_between
        while True:

            # We processed all dates
            if not dates:
                break

            # We are not in the first iteration, and thus have predicates
            if predicates:
                conditions.append(get_condition(predicates=predicates))

            current_date: datetime = dates[0]
            predicates = []

            # The contract has a year column. Thus we will add its year predicate
            if available_date_columns.year is not None:
                predicates.append(
                    get_predicate(
                        column_name=available_date_columns.year,
                        operator=Operator.EQUAL,
                        value=current_date.year,
                    )
                )

                # If only the year predicate is enough, we filter dates and jump
                # to the next iteration
                if has_full_year(reference_date=current_date, dates=dates):
                    dates = filter_year(
                        reference_date=current_date, dates=dates
                    )
                    continue

            if available_date_columns.month is not None:
                predicates.append(
                    get_predicate(
                        column_name=available_date_columns.month,
                        operator=Operator.EQUAL,
                        value=current_date.month,
                    )
                )
                # If only the month predicate (and maybe the year predicate) is enough,
                # we filter dates and jump to the next iteration.
                if has_full_month(reference_date=current_date, dates=dates):
                    dates = filter_month(
                        reference_date=current_date, dates=dates
                    )
                    continue

            if available_date_columns.day is not None:
                predicates.append(
                    get_predicate(
                        column_name=available_date_columns.day,
                        operator=Operator.EQUAL,
                        value=current_date.day,
                    )
                )

            # At this point, we must assume that the day predicate cannot be ignored
            dates = filter_day(reference_date=current_date, dates=dates)

        return conditions

    def get_date_conditions(
        self,
        contract: Input,
        reference_dates: List[datetime],
    ) -> List[Condition]:

        if not contract.colunas_particao_data:
            return []

        available_date_columns = get_available_date_columns(
            contract.colunas_particao_data
        )
        # NOTE This isn't the optimal way, but in the grand scheme of things
        # it doesn't really matter because data processing will always take
        # longer than this calculations.

        conditions = []
        for reference_date in reference_dates:
            conditions = conditions + self.get_conditions_from_ref(
                contract=contract,
                reference_date=reference_date,
                available_date_columns=available_date_columns,
            )

        return remove_dups(conditions)

    def get_push_down(
        self,
        contract: Input,
        reference_dates: List[datetime],
    ) -> str:

        if (
            not contract.colunas_particao_categorica
            and not contract.colunas_particao_data
        ):
            return None

        date_conditions = self.get_date_conditions(
            contract=contract, reference_dates=reference_dates
        )

        categoric_conditions = self.get_categoric_conditions(contract=contract)

        if date_conditions and categoric_conditions:
            return f"{join_conditions(date_conditions)} AND {join_conditions(categoric_conditions)}"
        if date_conditions:
            return f"{join_conditions(date_conditions)}"
        if categoric_conditions:
            return f"{join_conditions(categoric_conditions)}"

        return None
