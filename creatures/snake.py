import math

from creatures.BaseCreature import BaseCreature
from physics import Vector, Chain


class Snake(BaseCreature):
    def __init__(self, origin: Vector, scale: float = 1.0) -> None:
        super().__init__(origin, scale)
        self.spine = Chain(
            origin=origin,
            joint_count=48,
            link_size=64 * scale,
            angle_constraint=math.pi / 8,
        )
        self.body_width = [
            (64 - i) * scale for i in range(48)
        ]
        self.body_width[0] = 64 * 1.1875 * scale
        self.body_width[1] = 64 * 1.25 * scale
