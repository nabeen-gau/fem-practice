from point import Point
from support import Support, FixedSupport, HingedSupport, RollerSupport
from load import NodalLoad


class PointCollection:
    id: list[int] = []
    points: list[Point] = []
    collection: dict[int: Point] = {}
    loads: list[NodalLoad] = []
    displacements: list[NodalLoad] = []
    supports: list[Support] = []
    dof_ids: list[tuple[int]] = []

    def __init__(self, *args: Point):
        """
        args is collection of points in tuple form \n
        For ex:
        p1 = Point(3, 4)
        p2 = Point(2, 3)

        p = PointCollection(p1, p2)
        """
        for index, arg in enumerate(args):
            self.id.append(index)
            self.points.append(arg)
            self.collection[index] = arg
            self.loads.append(None)
            self.displacements.append(None)
            self.supports.append(None)
            self.dof_ids.append((3*index, 3*index+1, 3*index+2))

    @property
    def item_count(self):
        return self.id[-1]+1

    def add_loads(self, *loads: NodalLoad):
        for load in loads:
            self.loads[self.get_index(load.position)] = load

    def add_supports(self, *supports: Support):
        for support in supports:
            self.supports[self.get_index(support.position)] = support

    def get_index(self, point: Point):
        return next((k for k, v in self.collection.items() if v == point), None)

    def get_free_points(self) -> list[int]:
        points = []
        fixed_pts = self.get_fixed_points()
        for i in range(3*self.item_count):
            if i not in fixed_pts:
                points.append(i)
        return points

    def get_fixed_points(self) -> list[int]:
        points = []
        for s, indices in zip(self.supports, self.dof_ids):
            if s:
                points.extend(s.get_fixicity(indices))
        return points


if __name__ == "__main__":
    p1 = Point(3, 4)
    p2 = Point(2, 3)

    p = PointCollection(p1, p2)
    print(p.collection)
    print(p.dof_ids)
