import secrets
import string
from typing import List, Union

from physics.utils import constrain_angle, constrain_distance
from physics.vector import Vector


class Chain:
    """
    This class creates a chain in which the number of joints is specified,
    and the length of each linkage of said chain, either of a single size,
    or of a size defined in the constructor:\n

    ``┌───l₀───┬───l₁───┬───l₂───┬───l₃───┬──lₙ₋₁──┐
    ×────────×────────×────────×────────×───//───×
    j₀       j₁       j₂       j₃       j₄  //   jₙ``\n

    Where ``lₙ`` is the linkage number, ``jₙ`` is the join number\n

    Attributes
    ----------
    joints : List[Vector]
        List of Joints
    angles : List[float]
        List of angles
    """

    def __init__(
            self,
            origin: Vector,
            joint_count: int,
            link_size: Union[float, List[float]],
            angle_constraint: float = -1
    ) -> None:
        """
        Parameters
        ----------
        origin: `Vector`
            Origin of the chain
        joint_count: `int`
            Number of joints
        link_size: `float` or `list` [`float`]
            Size of the linkages, If defined as a float, all linkages will have
            the same length, if defined as a list of size `len(join_count)-1`,
            each bar will have its respective length
        angle_constraint: `float`
            Angle constraint of the chain, if not defined, it is assumed that there
            is no restriction
        """
        if isinstance(link_size, Union[int, float]):
            self._link_size = [link_size for _ in range(joint_count - 1)]
        elif isinstance(link_size, list):
            if len(link_size) == 1:
                self._link_size = [link_size[0] for _ in range(joint_count)]
            else:
                self._link_size = [link_size[i] for i in range(len(link_size))]
        self._angle_constraint = angle_constraint
        self.joints: List[Vector] = []
        self.angles: List[float] = []
        self._id = ''.join(
            secrets.choice(string.ascii_letters + string.digits)
            for _ in range(5)
        )
        self.joints.append(origin.copy())
        self.angles.append(0.0)
        for i in range(1, joint_count):
            self.joints.append(
                self.joints[i - 1] + Vector(0, self._link_size[i - 1])
            )
            self.angles.append(0.0)

    def resolve(self, pos: Vector) -> None:
        self.angles[0] = (pos - self.joints[0]).heading()
        self.joints[0] = pos
        for i in range(1, len(self.joints)):
            current_angle = (self.joints[i - 1] - self.joints[i]).heading()
            if i > 1 and self._angle_constraint > 0:
                self.angles[i] = constrain_angle(
                    current_angle, self.angles[i - 1], self._angle_constraint
                )
            else:
                self.angles[i] = current_angle
            self.joints[i] = self.joints[i - 1] - \
                             Vector.from_angle(self.angles[i]).set_mag(
                                 self._link_size[i - 1])

    def fabrik_resolve(self, pos: Vector, anchor: Vector) ->None:
        """
        “FABRIK”, or “Forwards and Backwards Reaching Inverse Kinematics”
        """
        self.joints[0] = pos
        for i in range(1, len(self.joints)):
            self.joints[i] = constrain_distance(
                self.joints[i], self.joints[i - 1], self._link_size[i - 1])

        self.joints[-1] = anchor
        for i in range(len(self.joints) - 2, -1, -1):
            self.joints[i] = constrain_distance(
                self.joints[i], self.joints[i + 1], self._link_size[i - 1])
