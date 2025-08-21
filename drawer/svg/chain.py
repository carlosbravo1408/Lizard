from typing import Union, List

import svgwrite
from svgwrite import animate

from .base_drawer import BaseDrawer
from physics import Chain as BaseChain, Vector


class Chain(BaseChain, BaseDrawer):
    def __init__(
            self,
            origin: Vector,
            joint_count: int,
            link_size: Union[float, List[float]],
            angle_constraint: float = -1
    ) -> None:
        super().__init__(origin, joint_count, link_size, angle_constraint)
        BaseDrawer.__init__(self)
        self._draw_group_name = "chain"
        self._line_color = "#ff4444"
        self._joint_color = "#ffff66"
        self._bg_color = "#1e1e1e"
        self._stroke_width = 6
        self._joint_radius = 8

    def record_frame(self) -> None:
        self._frames.append([(p.x, p.y) for p in self.joints])

    def to_group(
            self,
            dwg: svgwrite.Drawing,
            frame_skip:int = 1
    ) -> svgwrite.Drawing:
        chain_group = super().to_group(dwg, frame_skip)

        g_links = chain_group.add(dwg.g(
            id="links",
            stroke=self._line_color,
            fill="none",
            stroke_width=self._stroke_width,
            stroke_linecap="round"
        ))
        g_joints = chain_group.add(dwg.g(
            id="joints",
            fill=self._joint_color,
            stroke="none"
        ))

        joint_cx_lists = []
        joint_cy_lists = []
        for j in range(len(self.joints)):
            cx_vals = [
                f"{self._frames_to_use[f][j][0]:.3f}"
                for f in range(self._n_frames)
            ]
            cy_vals = [
                f"{self._frames_to_use[f][j][1]:.3f}"
                for f in range(self._n_frames)
            ]
            if self._n_frames == 1:
                cx_vals *= 2
                cy_vals *= 2
            joint_cx_lists.append(cx_vals)
            joint_cy_lists.append(cy_vals)

        link_vals = []
        for i in range(len(self.joints) - 1):
            x1 = [
                f"{self._frames_to_use[f][i][0]:.3f}"
                for f in range(self._n_frames)
            ]
            y1 = [
                f"{self._frames_to_use[f][i][1]:.3f}"
                for f in range(self._n_frames)
            ]
            x2 = [
                f"{self._frames_to_use[f][i + 1][0]:.3f}"
                for f in range(self._n_frames)
            ]
            y2 = [
                f"{self._frames_to_use[f][i + 1][1]:.3f}"
                for f in range(self._n_frames)
            ]
            if self._n_frames == 1:
                x1 *= 2
                y1 *= 2
                x2 *= 2
                y2 *= 2
            link_vals.append((x1, y1, x2, y2))

        for (x1_list, y1_list, x2_list, y2_list) in link_vals:
            line = dwg.line(
                start=(float(x1_list[0]), float(y1_list[0])),
                end=(float(x2_list[0]), float(y2_list[0])),
            )
            for attr, vals in zip(
                    ("x1", "y1", "x2", "y2"),
                    (x1_list, y1_list, x2_list, y2_list)
            ):
                line.add(animate.Animate(
                    attr,
                    dur=f"{self._duration:.4f}s",
                    values=";".join(vals),
                    keyTimes=self._key_times_str,
                    repeatCount="indefinite"
                ))
            g_links.add(line)

        for j in range(len(self.joints)):
            cx0 = float(joint_cx_lists[j][0])
            cy0 = float(joint_cy_lists[j][0])
            circ = dwg.circle(center=(cx0, cy0), r=self._joint_radius)
            for attr, vals in zip(
                    ("cx", "cy"),
                    (joint_cx_lists[j], joint_cy_lists[j])
            ):
                circ.add(animate.Animate(
                    attr,
                    dur=f"{self._duration:.4f}s",
                    values=";".join(vals),
                    keyTimes=self._key_times_str,
                    repeatCount="indefinite"
                ))
            g_joints.add(circ)

        return chain_group

    def save_svg(self, filename: str, width: int, height: int) -> None:
        dwg = svgwrite.Drawing(filename, size=(width, height))
        dwg.add(dwg.rect(
            insert=(0, 0), size=(width, height), fill=self._bg_color
        ))
        chain_group = self.to_group(dwg=dwg)
        dwg.add(chain_group)
        dwg.save()
