import math

import svgwrite
from svgwrite import animate

from creatures import Lizard as BaseLizard
from .base_drawer import BaseDrawer
from physics import Vector


class Lizard(BaseLizard, BaseDrawer):
    def __init__(
            self,
            origin: Vector,
            scale: float = 1.0,
            color: str = "#03ac13"
    ) -> None:
        super().__init__(origin, scale)
        BaseDrawer.__init__(self)
        self._draw_group_name = "lizard"
        self._background_color = "#1e1e1e"
        self._body_color = color

    def record_frame(self) -> None:
        body_path = []
        for i in range(len(self.spine.joints) - 1):
            j1, j2 = self.spine.joints[i], self.spine.joints[i + 1]
            r1, r2 = self.body_width[i] / 2, self.body_width[i + 1] / 2
            dx, dy = j2.x - j1.x, j2.y - j1.y
            l = math.hypot(dx, dy)
            if l == 0:
                continue
            nx, ny = -dy / l, dx / l
            body_path.append([(j1.x + nx * r1, j1.y + ny * r1),
                              (j1.x - nx * r1, j1.y - ny * r1),
                              (j2.x - nx * r2, j2.y - ny * r2),
                              (j2.x + nx * r2, j2.y + ny * r2)])
        arm_paths = []
        for arm in self.arms:
            points = [(j.x, j.y) for j in arm.joints]
            arm_paths.append(points)
        self._frames.append({
            "body": body_path,
            "arms": arm_paths,
            "head": (self.spine.joints[0].x, self.spine.joints[0].y)
        })

    def to_group(
            self,
            dwg: svgwrite.Drawing,
            frame_skip:int = 1
    ) -> svgwrite.Drawing:
        lizard_group = super().to_group(dwg, frame_skip)

        g_body = lizard_group.add(dwg.g(
            fill=self._body_color,
            stroke=self._body_color,
            stroke_width=3,
            stroke_linecap="round"
        ))
        g_arms = lizard_group.add(dwg.g(
            fill=self._body_color,
            stroke=self._body_color,
            stroke_width=6,
            stroke_linecap="round"
        ))
        g_head = lizard_group.add(dwg.g(
            fill=self._body_color,
            stroke=self._body_color,
            stroke_width=self.body_width[0],
            stroke_linecap="round"
        ))

        for poly_idx in range(len(self._frames_to_use[0]["body"])):
            values = []
            for f in range(self._n_frames):
                pts = self._frames_to_use[f]["body"][poly_idx]
                path_d = f"M{pts[0][0]:.2f},{pts[0][1]:.2f} "
                path_d += " ".join(f"L{x:.2f},{y:.2f}" for x, y in pts[1:])
                path_d += " Z"
                values.append(path_d)
            path = dwg.path(d=values[0])
            path.add(animate.Animate(
                "d",
                dur=f"{self._duration:.2f}s",
                values=";".join(values),
                keyTimes=self._key_times_str,
                fill="freeze",
                repeatCount="indefinite"
            ))
            g_body.add(path)

        for arm_idx in range(4):
            values = []
            for f in range(self._n_frames):
                pts = self._frames_to_use[f]["arms"][arm_idx]
                path_d = f"M{pts[0][0]:.2f},{pts[0][1]:.2f} "
                path_d += " ".join(f"L{x:.2f},{y:.2f}" for x, y in pts[1:])
                values.append(path_d)
            path = dwg.path(d=values[0])
            path.add(animate.Animate(
                "d",
                dur=f"{self._duration:.2f}s",
                values=";".join(values),
                keyTimes=self._key_times_str,
                fill="freeze",
                repeatCount="indefinite"
            ))
            g_arms.add(path)

        values = []
        for f in range(self._n_frames):
            x, y = self._frames_to_use[f]["head"]
            path_d = f"M{x:.2f},{y:.2f} L{x:.2f},{y:.2f}"
            values.append(path_d)
        head_path = dwg.path(d=values[0])
        head_path.add(animate.Animate(
            "d",
            dur=f"{self._duration:.2f}s",
            values=";".join(values),
            keyTimes=self._key_times_str,
            fill="freeze",
            repeatCount="indefinite"
        ))
        g_head.add(head_path)

        return lizard_group

    def save_svg(self, filename: str, width: int, height: int) -> None:
        dwg = svgwrite.Drawing(filename, size=(width, height))
        dwg.add(
            dwg.rect(
                insert=(0, 0),
                size=(width, height),
                fill="none"
            )
        )
        dwg.add(self.to_group(dwg))
        dwg.save()
