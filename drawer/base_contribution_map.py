from typing import List, Tuple

from github_user_contrib import DailyContribution
from physics import Vector


class BaseContributionMap:
    def __init__(self, days: List[DailyContribution], theme: str) -> None:
        self._days = days
        self.theme = theme
        self._cols = 55
        self._rows = 9
        self._cell = 24
        self._gap = 8
        self._pad = 16
        self._step = self._cell + self._gap
        self._width = self._pad * 2 + self._cols * self._step - self._gap
        self._height = self._pad * 2 + self._rows * self._step - self._gap
        self.targets = [d for d in days if d.contributions > 0]
        self._max_contribution = max(
            (d.contributions for d in self.targets), default=0)
        self.background_colors = {
            "light": "#ffffff",
            "dark": "#0d1117"
        }
        self.colors = {
            "light": {
                0: "#eff2f5",
                1: "#aceebb",
                2: "#4ac26b",
                3: "#2da44e",
                4: "#116329"
            },
            "dark": {
                0: "#151b23",
                1: "#033a16",
                2: "#196c2e",
                3: "#2ea043",
                4: "#56d364"
            }
        }

    def cell2xy(self, col: int, row: int) -> Tuple[int, int]:
        x = self._pad + (col + 1) * self._step
        y = self._pad + (row + 1) * self._step
        return x, y

    def cell_center(self, col: int, row: int) -> Tuple[int, int]:
        x, y = self.cell2xy(col, row)
        return x + self._cell // 2, y + self._cell // 2

    def vector2cell(self, vector: Vector) -> Tuple[int, int]:
        col = (vector.x - self._pad) // self._step - 1
        row = (vector.y - self._pad) // self._step - 1
        return int(col), int(row)

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    def sort_contributions(
            self,
            target_cell: Tuple[int, int]
    ) -> List[DailyContribution]:
        tx, ty = target_cell
        return sorted(self.targets, key=lambda item: (
            -item.contributions,
            -(abs(item.week_number - tx) + abs(item.day_number - ty))
        ))
