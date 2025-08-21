import math
import secrets
import string
from typing import List

from physics import Vector, Chain


class BaseCreature:
    spine: Chain
    body_width: List[float]

    def __init__(self, origin: Vector, scale: float = 1.0) -> None:
        self.scale = scale
        self._id = ''.join(
            secrets.choice(string.ascii_letters + string.digits)
            for _ in range(5)
        )

    def resolve(self, pos: Vector) -> None:
        self.spine.resolve(pos)

    def get_pos_x(
            self,
            i: int,
            angle_offset: float,
            length_offset: float,
    ) -> float:
        return self.spine.joints[i].x \
            + math.cos(self.spine.angles[i] + angle_offset) \
            * (self.body_width[i] + length_offset)

    def get_pos_y(
            self,
            i: int,
            angle_offset: float,
            length_offset: float,
    ) -> float:
        return self.spine.joints[i].y \
            + math.sin(self.spine.angles[i] + angle_offset) \
            * (self.body_width[i] + length_offset)
