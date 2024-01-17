from point import Point
import numpy as np


class Support:
    def __init__(self, position: Point):
        self.position = position

    def deformation(self):
        pass

    def get_fixicity(self, indices: tuple[int, int, int]) -> tuple:
        pass


class RollerSupport(Support):
    def __init__(self, position: Point, orientation: str = "y"):
        super().__init__(position)
        self.orientation = orientation

    def deformation(self) -> np.ndarray:
        if self.orientation == "y":
            return np.array([1, 0, 0])
        else:
            return np.array([0, 1, 0])

    def get_fixicity(self, indices: tuple[int, int, int]) -> tuple:
        if self.orientation == "y":
            return (indices[1], )
        else:
            return (indices[0], )

    def __repr__(self) -> str:
        return f"Roller Support at {self.position}"


class HingedSupport(Support):
    def __init__(self, position: Point):
        super().__init__(position)

    def deformation(self):
        return np.array([1, 1, 0])

    def get_fixicity(self, indices: tuple[int, int, int]) -> tuple:
        return (indices[0], indices[1])

    def __repr__(self) -> str:
        return f"Hinged Support at {self.position}"


class FixedSupport(Support):
    def __init__(self, position: Point):
        super().__init__(position)

    def deformation(self):
        return np.array([1, 1, 1])

    def get_fixicity(self, indices: tuple[int, int, int]) -> tuple:
        return indices

    def __repr__(self) -> str:
        return f"Fixed Support at {self.position}"
