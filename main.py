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


@dataclass
class Material:
    E: float


@dataclass
class Section:
    A: float
    I: float


class Support:
    def __init__(self, position: Point):
        self.position = position

    def deformation(self):
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

    def __repr__(self) -> str:
        return f"Roller Support at {self.position}"


class HingedSupport(Support):
    def __init__(self, position: Point):
        super().__init__(position)

    def deformation(self):
        return np.array([1, 1, 0])

    def __repr__(self) -> str:
        return f"Hinged Support at {self.position}"


class FixedSupport(Support):
    def __init__(self, position: Point):
        super().__init__(position)

    def deformation(self):
        return np.array([1, 1, 1])

    def __repr__(self) -> str:
        return f"Fixed Support at {self.position}"


@dataclass
class Load:
    x: float
    y: float
    m: float
    position: Point

    def __add__(self, other: "Load"):
        return Load(self.x+other.x, self.y+other.y, self.m+other.m)

    def __sub__(self, other: "Load"):
        return Load(self.x-other.x, self.y-other.y, self.m-other.m)


@dataclass
class Displacement:
    x: float
    y: float
    r: float

    def __add__(self, other: "Load"):
        return Displacement(self.x+other.x, self.y+other.y, self.r+other.r)

    def __sub__(self, other: "Load"):
        return Displacement(self.x-other.x, self.y-other.y, self.r-other.r)


class Member:
    begin_point: Point
    end_point: Point
    section: Section = Section(1, 1)
    material: Material = Material(1)

    def __init__(self, begin_point: Point, end_point: Point):
        self.begin_point = begin_point
        self.end_point = end_point

    @property
    def length(self) -> float:
        return np.round(self.begin_point.distance(self.end_point), 10)

    @property
    def slope(self) -> float:
        return np.round(self.begin_point.slope(self.end_point), 10)

    @property
    def sine(self) -> float:
        return np.round(np.sin(np.arctan(self.slope)), 10)

    @property
    def cosine(self) -> float:
        return np.round(np.cos(np.arctan(self.slope)), 10)

    @property
    def ei(self) -> float:
        return self.material.E * self.section.I

    @property
    def ea(self) -> float:
        return self.material.E * self.section.A

    @property
    def stiffness_matrix(self) -> np.ndarray:
        t1 = self.ea/self.length
        t2 = 12*self.ei/self.length**3
        t3 = 6*self.ei/self.length**2
        t4 = 4*self.ei/self.length
        t5 = 2*self.ei/self.length

        return np.array([
            [t1,    0,      0,      -t1,    0,      0],
            [0,     t2,     t3,     0,      -t2,    t3],
            [0,     t3,     t4,     0,      -t3,    t5],
            [-t1,   0,      0,      t1,     0,      0],
            [0,     -t2,    -t3,    0,      t2,     -t3],
            [0,     t3,     t5,     0,      -t3,    t4]
        ])


@dataclass
class Node:
    point: Point
    load: Load
    support: Support


class Frame:
    members: list[Member] = []
    connections: list[tuple[Member, 2]] = []
    global_k: np.ndarray = None
    supports: list[Support] = []
    loads: list[Load] = []
    nodes: list[Node] = []
    nodes_id_dict: dict[int: Node] = {}

    def __init__(self, *nodes):
        for index, node in enumerate(nodes):
            self.nodes.append(Node(node, None, None))
            self.nodes_id_dict[self.nodes_id_dict.__len__()] = node

    def add_members(self, *members: Member):
        self.members.extend(members)

    def generate_global_stiffness_matrix(self):
        pass

    def solve(self):
        DOF = 3 * len(self.nodes)
        free_dofs = []
        specified_dofs = []

        for index, node in enumerate(self.nodes):
            if node.support == None:
                free_dofs.extend([3*index, 3*index+1, 3*index+2])
            if isinstance(node.support, RollerSupport):
                if node.support.orientation == "y":
                    free_dofs.append(3*index)
                    free_dofs.append(3*index+2)
                else:
                    free_dofs.append(3*index+1)
                    free_dofs.append(3*index+2)

            if isinstance(node.support, HingedSupport):
                free_dofs.append(3*index+2)

        for index in range(DOF):
            if index not in free_dofs:
                specified_dofs.append(index)

        self.generate_global_stiffness_matrix()

    def add_supports(self, *supports: Support) -> None:
        for support in supports:
            index = next((k for k, v in self.nodes_id_dict.items() if v == support.position), None)
            self.nodes[index].support = support
            self.supports.append(support)

    def add_load(self, *loads: Load) -> None:
        for load in loads:
            self.loads.append(load)
            index = next((k for k, v in self.nodes_id_dict.items() if v == load.position), None)
            self.nodes[index].load = load


if __name__ == "__main__":
    n1 = Point(0, 4)
    n2 = Point(3, 4)
    n3 = Point(0, 0)
    n4 = Point(3, 0)
    n5 = Point(6, 0)

    ma = Member(n1, n2)
    mb = Member(n1, n3)
    mc = Member(n2, n5)
    md = Member(n2, n4)
    me = Member(n2, n5)
    mf = Member(n3, n4)
    mg = Member(n4, n5)

    f1 = Load(10, 0, 0, n2)
    f2 = Load(0, -10, 0, n4)
    s1 = HingedSupport(n1)
    s2 = RollerSupport(n3, orientation="x")
    s3 = HingedSupport(n5)

    frame = Frame(n1, n2, n3, n4, n5)
    frame.add_members(ma, mb, mc, md, me, mf, mg)
    frame.add_supports(s1, s2, s3)
    frame.add_load(f1, f2)
    # for i in frame.nodes:
    #    print(i)
    frame.solve()
