from point import Point
from load import Load
from support import Support


class Node:
    point: Point
    load: Load
    support: Support
    indices: tuple[int]

    def __init__(self, x, y):
        self.point = Point(x, y)

    def distance(self, other: "Node") -> float:
        return self.point.distance(other.point)
