import math

from physics.vector import Vector


def constrain_distance(
        pos: Vector,
        anchor: Vector,
        constraint: float
) -> Vector:
    return anchor + (pos - anchor).set_mag(constraint)


def simplify_angle(angle: float) -> float:
    while angle >= math.tau:
        angle -= math.tau
    while angle < 0:
        angle += math.tau
    return angle


def relative_angle_diff(angle: float, anchor: float) -> float:
    angle = simplify_angle(angle + math.pi - anchor)
    anchor = math.pi
    return anchor - angle


def constrain_angle(angle: float, anchor: float, constraint: float) -> float:
    diff = relative_angle_diff(angle, anchor)
    if abs(diff) <= constraint:
        return simplify_angle(angle)
    if diff > constraint:
        return simplify_angle(anchor - constraint)
    return simplify_angle(anchor + constraint)
