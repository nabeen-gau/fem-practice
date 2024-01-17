from dataclasses import dataclass
from load import Load


@dataclass
class Displacement:
    x: float
    y: float
    r: float

    def __add__(self, other: "Load"):
        return Displacement(self.x+other.x, self.y+other.y, self.r+other.r)

    def __sub__(self, other: "Load"):
        return Displacement(self.x-other.x, self.y-other.y, self.r-other.r)
