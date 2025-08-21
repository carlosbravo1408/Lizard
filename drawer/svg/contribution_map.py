from typing import List, Any

import numpy as np
import svgwrite
from svgwrite import animate

from drawer.base_contribution_map import BaseContributionMap
from drawer.bug_shape import BUG_SHAPE
from github_user_contrib import DailyContribution


class ContributionMap(BaseContributionMap):
    def __init__(
            self,
            days: List[DailyContribution],
            theme: str = "light"
    ) -> None:
        super().__init__(days, theme)
        self._cells_dict = {}
        self._cells_list = []

    def start_background(self, dwg: svgwrite.Drawing) -> None:
        for day in self._days:
            col, row = day.week_number, day.day_number
            x, y = self.cell2xy(col=col, row=row)
            rect = dwg.rect(
                insert=(x, y),
                size=(self._cell, self._cell),
                fill=self.colors[self.theme][day.quartile],
                id=f"cell-{col}-{row}",
                opacity=1,
                rx=4,
                ry=4
            )
            self._cells_dict[(col, row)] = {
                "rect": rect,
                "quartile": day.quartile,
                "dur": 0
            }
        self.add_bug_symbol(dwg)

    def remove_day(
            self,
            target: DailyContribution,
            elapsed_time: float
    ) -> None:
        col, row = target.week_number, target.day_number
        self._cells_dict[(col, row)]["dur"] = elapsed_time
        self._cells_list.append((col, row))

    def to_group(
            self,
            dwg: svgwrite.Drawing,
            total_elapsed_time: float
    ) -> svgwrite.Drawing:
        g_map = dwg.g(id="contribution-map")
        for (col, row), data in self._cells_dict.items():
            cell_group = dwg.g(id=f"cell-{col}-{row}")
            if data['dur'] > 0:
                color1 = self.colors[self.theme][data.get('quartile')]
                color2 = self.colors[self.theme][0]
                transition = data['dur'] / total_elapsed_time
                anim = animate.Animate(
                    attributeName="fill",
                    values=f"{color1};{color1};{color2};{color2}",
                    keyTimes=f"0;{transition};{transition};1",
                    begin="0s",
                    dur=f"{total_elapsed_time:.3f}s",
                    fill="freeze",
                    repeatCount="indefinite"
                )
                data["rect"].add(anim)
            cell_group.add(data.get("rect"))
            g_map.add(cell_group)

        for i, (col, row) in enumerate(self._cells_list):
            data = self._cells_dict[(col, row)]
            if data.get('quartile') > 0:
                self.place_bug(
                    dwg=dwg,
                    group=g_map,
                    col=col,
                    row=row,
                    start_time=data["dur"],
                    hide_time=self._cells_dict[self._cells_list[i + 1]]["dur"]
                    if i < len(self._cells_list) - 1
                    else data["dur"] + 0.25,
                    total_duration=total_elapsed_time,
                )
        return g_map

    def place_bug(
            self,
            dwg: svgwrite.Drawing,
            group: Any,
            row: int,
            col: int,
            start_time: float,
            hide_time: float,
            total_duration: float,
    ) -> None:
        x, y = self.cell2xy(col, row)
        use = dwg.use("#bug", insert=(x, y), size=(self._cell, self._cell))
        t0 = 0
        t1 = start_time / total_duration
        t2 = hide_time / total_duration
        t3 = 1.0
        values = "0;1;0;0"
        key_times_str = f"{t0:.3f};{t1:.3f};{t2:.3f};{t3:.3f}"
        use.add(animate.Animate(
            attributeName="opacity",
            dur=f"{total_duration:.3f}s",
            values=values,
            keyTimes=key_times_str,
            fill="freeze",
            repeatCount="indefinite",
            calcMode="discrete"
        ))
        group.add(use)

    def add_bug_symbol(self, dwg, symbol_id="bug") -> None:
        symbol = dwg.symbol(id=symbol_id)
        scale = self._cell / BUG_SHAPE.shape[0]
        for i in range(BUG_SHAPE.shape[0]):
            for j in range(BUG_SHAPE.shape[1]):
                if np.isnan(BUG_SHAPE[i, j]):
                    continue
                v = "#000000" if self.theme == "light" else "#ffffff"
                color = v if BUG_SHAPE[i, j] == 1 else "#c80000"
                symbol.add(dwg.rect(
                    insert=(j * scale, i * scale),
                    size=(scale, scale),
                    fill=color
                ))
        dwg.defs.add(symbol)
