import copy
from typing import Optional, Tuple

import svgwrite

from drawer.svg import ContributionMap, Lizard
from github_user_contrib import GithubFetcher, DailyContribution
from physics import Vector


class ContributionGameSVG:
    _lizard_color = {
        "dark": "#a16e38",
        "light": "#40939d",
        "default": "#03ac13",
    }

    def __init__(
            self,
            user_name: str,
            token: str,
            theme: str = "light",
            lizard_color: Optional[str] = None,
    ) -> None:
        self._map = ContributionMap(
            GithubFetcher(user_name, token).get_daily_contributions(), theme
        )
        self._height = self._map.height
        self._width = self._map.width
        self._lizard = Lizard(
            Vector(-30, self._height // 2),
            0.25,
            color=self.get_lizard_color(theme)
            if lizard_color is None else lizard_color,
        )
        self._current_bug = None
        self._running = True
        self._fps = 60
        self._targets = copy.deepcopy(self._map.targets)
        self._lizard.start_recording(fps=self._fps)
        self._tpf = 1.0 / self._fps  # time per frame
        self._speed = 12
        self._current_target = None

    def get_lizard_color(self, theme: str) -> str:
        return self._lizard_color.get(theme, self._lizard_color["default"])

    def sort_contributions(self, target_cell: Tuple[int, int]) -> None:
        tx, ty = target_cell
        self._targets = sorted(self._targets, key=lambda item: (
            -item.contributions,
            (abs(item.week_number - tx) + abs(item.day_number - ty))
        ))

    def get_next_target(self) -> DailyContribution:
        cell = self._map.vector2cell(self._lizard.spine.joints[0].copy())
        self.sort_contributions(cell)
        return self._targets.pop(0)

    def has_enough_bugs(self) -> bool:
        return len(self._targets) > 0

    def move_lizard_to_target(self, target_pos) -> bool:
        dist = self._current_target.dist(target_pos)
        if dist > self._speed:
            self._current_target = Vector.const_velocity(
                self._current_target, target_pos, self._speed
            )
            self._lizard.resolve(self._current_target)
            return False
        else:
            self._current_target = target_pos.copy()
            self._lizard.resolve(self._current_target)
            return True

    def run(self) -> None:
        t = 0
        self._current_bug = self.get_next_target()
        self._current_target = self._lizard.spine.joints[0].copy()
        dwg = svgwrite.Drawing(
            f"contribution_map_animation_{self._map.theme}.svg",
            size=(self._map.width, self._map.height)
        )
        dwg.add(
            dwg.rect(
                insert=(0, 0),
                size=(self._map.width, self._map.height),
                fill="none"
            )
        )
        self._lizard.start_recording(fps=self._fps)
        self._running = True
        self._map.start_background(dwg)
        self._map.set_day_with_contribution(self._current_bug, self._tpf)
        while self._running:
            if self.has_enough_bugs() and self._current_bug is None:
                self._current_bug = self.get_next_target()
                self._map.set_day_with_contribution(self._current_bug,
                                                    t * self._tpf)
            if self._current_bug is not None:
                bx = self._current_bug.week_number
                by = self._current_bug.day_number
                target_px, target_py = self._map.cell_center(bx, by)
            if not self.has_enough_bugs() and self._current_bug is None:
                target_px, target_py = self._width + 300, self._height // 2
            if self.move_lizard_to_target(Vector(target_px, target_py)):
                if not self.has_enough_bugs() and self._current_bug is None:
                    self._running = False

                self._current_bug = None
            self._lizard.record_frame()
            t += 1

        dwg.add(self._map.to_group(dwg, t * self._tpf))
        dwg.add(self._lizard.to_group(dwg))
        dwg.save()
