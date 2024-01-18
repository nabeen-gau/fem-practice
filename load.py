from dataclasses import dataclass
from point import Point


@dataclass
class Load:
    """
    x: float
    y: float
    m: float
    position: Point
    """
    x: float
    y: float
    m: float
    position: Point

    @property
    def values(self) -> tuple:
        return (self.x, self.y, self.m)

    def __add__(self, other: "Load"):
        return Load(self.x+other.x, self.y+other.y, self.m+other.m)

    def __sub__(self, other: "Load"):
        return Load(self.x-other.x, self.y-other.y, self.m-other.m)
