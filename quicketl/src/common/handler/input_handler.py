from datetime import datetime
from typing import List

from quicketl.src.common.constants import Operator
from quicketl.src.common.dates import *
from quicketl.src.common.dtos.time_travel.available_date_columns import (
    AvailableDateColumns,
)
from quicketl.src.common.dtos.time_travel.condition import Condition
from quicketl.src.common.dtos.time_travel.predicate import Predicate
from quicketl.src.common.factories.get_condition import get_condition
from quicketl.src.common.factories.get_avl_date_columns import (
    get_available_date_columns,
)
from quicketl.src.common.dtos.contracts.input import Input

from quicketl.src.common.factories.get_predicate import get_predicate
from quicketl.src.common.utils import remove_dups


class InputHandler:

    def __init__(self):
        pass

    def get_categoric_predicate(self, contract: Input) -> List[Condition]:
        pass

    def get_conditions_from_date(
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

    def get_date_conditions(
        self,
        contract: Input,
        reference_dates: List[datetime],
    ) -> List[Condition]:
        available_date_columns = get_available_date_columns(
            contract.colunas_particao_data
        )
        # NOTE This isn't the optimal way, but in the grand scheme of things
        # it doesn't really matter because data processing will always take
        # longer than this calculations.

        predicates = []
        for reference_date in reference_dates:
            predicates.append(
                self.get_conditions_from_date(
                    contract=contract,
                    reference_date=reference_date,
                    available_date_columns=available_date_columns,
                )
            )

        return remove_dups(predicates)

    def get_push_down(
        self,
        contract: Input,
        reference_dates: List[datetime],
    ) -> str:

        date_predicates = self.get_date_conditions(
            contract=contract, reference_dates=reference_dates
        )

        categoric_predicates = self.get_categoric_predicate(contract=contract)
