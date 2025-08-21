from datetime import date
from typing import Union


Quartile = {
    "FOURTH_QUARTILE": 4,
    "THIRD_QUARTILE": 3,
    "SECOND_QUARTILE": 2,
    "FIRST_QUARTILE": 1,
    "NONE": 0
}


class DailyContribution:
    def __init__(
            self,
            _date: Union[str, date],
            contributions: int,
            week_number: int,
            day_number: int,
            quartile: str
    ) -> None:
        if isinstance(_date, date):
            self._date = _date
        elif isinstance(_date, str):
            self._date = date.fromisoformat(_date)
        self._quartile = Quartile[quartile]
        self._contributions = contributions
        self._week_number = week_number
        self._day_number = day_number

    @property
    def date(self) -> date:
        return self._date

    @property
    def contributions(self) -> int:
        return self._contributions

    @property
    def week_number(self) -> int:
        return self._week_number

    @property
    def day_number(self) -> int:
        return self._day_number

    @property
    def quartile(self) -> int:
        return self._quartile
