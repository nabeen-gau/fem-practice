from dataclasses import dataclass
import numpy as np


@dataclass
class Point:
    x: int
    y: int

    def distance(self, other: "Point") -> float:
        return np.round(np.sqrt((self.x-other.x)**2 + (self.y-other.y)**2), 10)

    def slope(self, other: "Point") -> float:
        if self.x == other.x:
            return np.inf
        else:
            return np.round((other.y - self.y)/(other.x - self.x), 10)
