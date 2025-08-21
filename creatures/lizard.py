import math

from physics.chain import Chain
from physics.vector import Vector
from .BaseCreature import BaseCreature


class Lizard(BaseCreature):
    def __init__(
            self,
            origin: Vector,
            scale: float = 1.0
    ) -> None:
        super().__init__(origin, scale)
        self.spine = Chain(
            origin=origin,
            joint_count=18,
            link_size=[
                64 * self.scale * i for i in [
                    0.7, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 0.6, 0.6,
                    0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6
                ]
            ],
            angle_constraint=math.pi / 8
        )

        self.arms = [
            Chain(origin, 3, 52 * self.scale) for _ in range(4)
        ]
        self.arm_desired = [Vector(0, 0) for _ in range(4)]
        self.body_width = [
            70 * self.scale * i for i in [
                0.70, 1.00, 0.50, 1.00, 1.00, 1.00, 1.00, 0.70, 0.50,
                0.35, 0.30, 0.25, 0.23, 0.21, 0.20, 0.20, 0.20, 0.10
            ]
        ]
        self.resolve(self.spine.joints[0])

    def resolve(self, pos: Vector) -> None:
        super().resolve(pos)

        for i in range(len(self.arms)):
            side = 1 if i % 2 == 0 else -1
            body_index = 3 if i < 2 else 6
            angle = math.pi / 4 if i < 2 else math.pi / 3
            desired_pos = Vector(
                self.get_pos_x(body_index, angle * side, 80 * self.scale),
                self.get_pos_y(body_index, angle * side, 80 * self.scale)
            )
            if desired_pos.dist(self.arm_desired[i]) > 200 * self.scale:
                self.arm_desired[i] = desired_pos
            x = self.get_pos_x(body_index, math.pi / 2 * side, -35 * self.scale)
            y = self.get_pos_y(body_index, math.pi / 2 * side, -35 * self.scale)
            anchor = Vector(x, y)
            interp = Vector.lerp(
                self.arms[i].joints[0], self.arm_desired[i], 1)
            self.arms[i].fabrik_resolve(interp, anchor)
