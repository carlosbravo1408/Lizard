import math


class Vector:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def copy(self) -> 'Vector':
        return Vector(self.x, self.y)

    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, k: float) -> 'Vector':
        return Vector(self.x * k, self.y * k)

    __rmul__ = __mul__

    def __truediv__(self, scalar: float) -> 'Vector':
        return Vector(self.x / scalar, self.y / scalar)

    def set_mag(self, mag: float) -> 'Vector':
        current_mag = self.mag()
        if current_mag != 0:
            scale = mag / current_mag
            self.x *= scale
            self.y *= scale
        return self

    def mag(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def heading(self) -> float:
        return math.atan2(self.y, self.x)

    def dist(self, o: 'Vector') -> float:
        return math.hypot(self.x - o.x, self.y - o.y)

    @staticmethod
    def from_angle(angle: float) -> 'Vector':
        return Vector(math.cos(angle), math.sin(angle))

    def __repr__(self) -> str:
        return f"Vector({self.x:.2f}, {self.y:.2f})"

    def normalize(self) -> 'Vector':
        mag = self.mag()
        if mag == 0:
            return Vector(0, 0)
        return self / mag

    def lerp(self, target: 'Vector', t: float) -> 'Vector':
        return self + (target - self) * t

    def const_velocity(self, target: 'Vector', velocity: float) -> 'Vector':
        dir = target - self
        dist = dir.mag()
        dir = dir / dist
        return self + dir * velocity

    def angle(self, other: 'Vector') -> float:
        theta = math.pi - (self.heading() - other.heading())
        if abs(theta) > math.tau:
            theta = theta % math.tau
        return theta
