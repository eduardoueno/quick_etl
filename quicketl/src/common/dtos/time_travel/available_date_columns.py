from typing import Optional
from quicketl.src.common.dtos.contracts.column import DateColumn


class AvailableDateColumns:
    """
    Informs which date formats are available in a contract
    """

    _date: Optional[DateColumn]
    _year_month: Optional[DateColumn]
    _year: Optional[DateColumn]
    _month: Optional[DateColumn]
    _day: Optional[DateColumn]

    def __init__(self):
        self._date = None
        self._year_month = None
        self._year = None
        self._month = None
        self._day = None

    def check_for_year(self):
        if (
            self._date is None
            and self._year is None
            and self._year_month is None
        ):
            return True
        else:
            return False

    def check_for_month(self):
        if (
            self._date is None
            and self._month is None
            and self._year_month is None
        ):
            return True
        else:
            return False

    def check_for_day(self):
        if self._date is None and self._day is None:
            return True
        else:
            return False

    @property
    def date(self):
        return self._date

    @property
    def year_month(self):
        return self._year_month

    @property
    def year(self):
        return self._year

    @property
    def month(self):
        return self._month

    @property
    def day(self):
        return self._day

    @date.setter
    def date(self, value: DateColumn):
        if (
            self.check_for_year()
            and self.check_for_month()
            and self.check_for_day()
        ):
            self._date = value
        else:
            raise

    @year_month.setter
    def year_month(self, value: DateColumn):
        if self.check_for_year() and self.check_for_month():
            self._year_month = value
        else:
            raise

    @year.setter
    def year(self, value: DateColumn):
        if self.check_for_year():
            self._year = value
        else:
            raise

    @month.setter
    def month(self, value: DateColumn):
        if self.check_for_month():
            self._month = value
        else:
            raise

    @day.setter
    def day(self, value: DateColumn):
        if self.check_for_day():
            self._day = value
        else:
            raise
