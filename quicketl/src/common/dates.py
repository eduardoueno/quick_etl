from typing import List, Optional
from datetime import datetime
from dateutil.relativedelta import relativedelta

from quicketl.src.common.constants import Window, Delay
from quicketl.src.common.utils import extract_numerical, look_for_in_enum


def stryear(date: datetime):
    return f"{str(date.year).rjust(4, '0')}"


def strmonth(date: datetime):
    return f"{str(date.month).rjust(2, '0')}"


def strday(date: datetime):
    return f"{str(date.day).rjust(2, '0')}"


def strdate(date: datetime):
    return f"{stryear(date)}{strmonth(date)}{strday(date)}"


def stryearmonth(date):
    return f"{stryear(date)}{strmonth(date)}"


def get_delay_type(delay: str):
    _delay = look_for_in_enum(delay, Delay)
    if not _delay:
        raise

    return _delay


def get_window_type(window: str):
    _window = look_for_in_enum(window, Window)
    if not _window:
        raise

    return _window


def get_window_value(window: str):

    # validate if window is actually a window
    if not look_for_in_enum(window, Window):
        raise

    return int(extract_numerical(window))


def get_delay_value(delay: str):

    # validate if delay is actually a delay
    if not look_for_in_enum(delay, Delay):
        raise

    return int(extract_numerical(delay))


def does_year_change(
    datetime: datetime, day: Optional[int] = None, month: Optional[int] = None
):
    if datetime.month - month < 0:
        return True

    if datetime.timetuple().tm_yday - day < 0:
        return True

    return False


def does_month_change(datetime: datetime, day: Optional[int] = None):
    if datetime.day - day < 0:
        return True

    return False


def lower_month_bondary(date: datetime):
    return date + relativedelta(day=1)


def upper_month_bondary(date: datetime):
    return date + relativedelta(day=31)


def lower_year_bondary(date: datetime):
    return date + relativedelta(day=1, month=1)


def upper_year_bondary(date: datetime):
    return date + relativedelta(
        day=31,
        month=12,
    )


def has_full_year(reference_date: datetime, dates: List[datetime]):
    """Checks if all days of the reference_date year are on the list"""
    pass


def has_full_month(reference_date: datetime, dates: List[datetime]):
    """Checks if all days of the reference_date month are on the list"""
    pass


def filter_month(
    reference_date: datetime, dates: List[datetime]
) -> List[datetime]:

    return [
        date
        for date in dates
        if date.year != reference_date.year
        and date.month != reference_date.month
    ]


def filter_year(
    reference_date: datetime, dates: List[datetime]
) -> List[datetime]:

    return [date for date in dates if date.year != reference_date.year]


def filter_day(reference_date: datetime, dates: List[datetime]):

    return [date for date in dates if date != reference_date]


def get_year_delay_date_range(
    reference_date: datetime, delay: str, window: str
):
    """calculates a start and end date when delay is yearly

    end_date is basically the reference_date with the year delay applied.
    start_date is the first day of the year if the window is yearly
    start_date is the first day of the month if the window is monthly
    start_date is the first day of the year if the window exceeds a year
    """

    delay_type = get_delay_type(delay=delay)

    if delay_type != Delay.YEAR:
        raise

    window_type = get_window_type(window=window)
    window_value = get_window_value(window=window)
    delay_value = get_delay_value(delay=delay)

    end_date = apply_delay(
        reference_date=reference_date, year_delay=delay_value
    )

    if window_type == Window.YEAR:
        start_date = apply_delay(
            reference_date=reference_date,
            year_delay=delay_value + window_value,
        )
        start_date = lower_year_bondary(start_date)
    elif window_type == Window.MONTH:
        if does_year_change(datetime=reference_date, month=window_value):
            start_date = lower_year_bondary(start_date)
        else:
            start_date = apply_delay(
                reference_date=reference_date,
                year_delay=delay_value,
                month_delay=window_value,
            )
            start_date = lower_month_bondary(start_date)
    elif window_type == Window.DAY:
        if does_year_change(datetime=reference_date, day=window_value):
            start_date = lower_year_bondary(start_date)
        else:
            start_date = apply_delay(
                reference_date=reference_date,
                year_delay=delay_value,
                day_delay=window_value,
            )
    else:
        raise

    return start_date, end_date


def get_month_delay_date_range(
    reference_date: datetime, delay: str, window: str
):
    """calculates a start and end date when delay is monthly

    end_date is basically the reference_date with the month delay applied.
    start_date is the first day of the year if the window is yearly
    start_date is the first day of the month if the window is monthly
    start_date is the first day of the month if the window exceeds a month
    """
    delay_type = get_delay_type(delay=delay)

    if delay_type != Delay.MONTH:
        raise

    window_type = get_window_type(window=window)
    window_value = get_window_value(window=window)
    delay_value = get_delay_value(delay=delay)

    end_date = apply_delay(
        reference_date=reference_date, month_delay=delay_value
    )

    if window_type == Window.YEAR:
        start_date = apply_delay(
            reference_date=reference_date,
            year_delay=window_value,
            month_delay=delay_value,
        )
        start_date = lower_year_bondary(start_date)
    elif window_type == Window.MONTH:
        start_date = apply_delay(
            reference_date=reference_date,
            month_delay=delay_value + window_value,
        )
        start_date = lower_month_bondary(start_date)
    elif window_value == Window.DAY:
        if does_month_change(datetime=reference_date, day=window_value):
            start_date = lower_month_bondary(start_date)
        else:
            start_date = apply_delay(
                reference_date=reference_date,
                month_delay=delay_value,
                day_delay=window_value,
            )
    else:
        raise

    return start_date, end_date


def get_day_delay_date_range(reference_date: datetime, delay: str, window: str):
    """calculates a start and end date when delay is daily

    end_date is basically the reference_date with the day delay applied.
    start_date is the first day of the year if the window is yearly
    start_date is the first day of the month if the window is monthly
    start_date is the any day if the window is daily
    """
    delay_type = get_delay_type(delay=delay)

    if delay_type != Delay.DAY:
        raise

    window_type = get_window_type(window=window)
    window_value = get_window_value(window=window)
    delay_value = get_delay_value(delay=delay)

    end_date = apply_delay(reference_date=reference_date, day_delay=delay_value)

    if window_type == Window.YEAR:
        start_date = apply_delay(
            reference_date=reference_date,
            year_delay=window_value,
            day_delay=delay_value,
        )
        start_date = lower_year_bondary(start_date)
    elif window_type == Window.MONTH:
        if does_year_change(datetime=reference_date, month=window_value):
            start_date = lower_year_bondary(start_date)
        else:
            start_date = apply_delay(
                reference_date=reference_date,
                month_delay=window_value,
                day_delay=delay_value,
            )
    elif window_value == Window.DAY:
        start_date = apply_delay(
            reference_date=reference_date,
            day_delay=delay_value + window_value,
        )
    else:
        raise

    return start_date, end_date


def get_date_range(reference_date: datetime, delay: str, window: str):
    """Calculates a start and end date

    Given a reference, delay and window, calculates a start and end date
    applying some common business logic.
    """
    delay_type = get_delay_type(delay=delay)

    if delay_type == Delay.YEAR:
        return get_year_delay_date_range(
            reference_date=reference_date, delay=delay, window=window
        )

    elif delay_type == Delay.MONTH:
        return get_month_delay_date_range(
            reference_date=reference_date, delay=delay, window=window
        )

    elif delay_type == Delay.DAY:
        return get_day_delay_date_range(
            reference_date=reference_date, delay=delay, window=window
        )
    else:
        raise


def apply_delay(
    reference_date: datetime,
    year_delay: Optional[int] = None,
    month_delay: Optional[int] = None,
    day_delay: Optional[int] = None,
) -> datetime:

    if year_delay is not None:
        delayed_date = reference_date - relativedelta(years=-year_delay)
    elif month_delay is not None:
        delayed_date = reference_date - relativedelta(months=-month_delay)
    elif day_delay is not None:
        delayed_date = reference_date - relativedelta(days=-day_delay)
    else:
        raise

    return delayed_date


def get_dates_between(start_date: datetime, end_date: datetime):

    date = start_date
    dates_between = []
    while date < end_date:
        dates_between.append(date)
        date = date + relativedelta(days=1)

    return sorted(dates_between)
