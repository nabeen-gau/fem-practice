import numpy as np
from point import Point
from material import Material
from section import Section
from support import Support, RollerSupport, HingedSupport, FixedSupport
from load import Load
# from displacement import Displacement
from node import Node
from member import Member
from grid import PointCollection


class Frame:
    members: list[Member] = []
    DOF: int = 0
    nodes: PointCollection = None
    loads: list[Load] = []

    def __init__(self, *nodes):
        self.nodes = PointCollection(*nodes)

    def add_members(self, *members: Member):
        self.members = members

    def generate_global_stiffness_matrix(self):
        self.global_k = np.zeros((self.DOF, self.DOF))

        for member in self.members:
            local_k = member.stiffness_matrix
            print(local_k)
            print(member.nodes[0].indices)

        # print(self.global_k)

    def solve(self):
        self.DOF = 3 * self.nodes.item_count
        free_dofs = self.nodes.get_free_points()
        specified_dofs = self.nodes.get_fixed_points()

        print(free_dofs, specified_dofs)
        # self.generate_global_stiffness_matrix()

    def add_supports(self, *supports: Support) -> None:
        self.supports = supports
        self.nodes.add_supports(*supports)

    def add_loads(self, *loads: Load) -> None:
        self.loads = loads
        self.nodes.add_loads(*loads)


if __name__ == "__main__":
    E = 2e11
    A = 1
    MOI = 5e-6

    n1 = Point(0, 0)
    n2 = Point(5, 0)
    n3 = Point(10, 0)

    m1 = Member(n1, n2, material=Material(E), section=Section(A=A, I=MOI))
    m2 = Member(n2, n3, material=Material(E), section=Section(A=A, I=MOI))

    l1 = Load(0, -30, -25, n1)
    l2 = Load(0, -30-60, 25-50, n2)
    l3 = Load(0, -60, 50, n3)

    s1 = FixedSupport(n1)
    s2 = RollerSupport(n3)
    s3 = RollerSupport(n2)

    frame = Frame(n1, n2, n3)
    frame.add_members(m1, m2)
    frame.add_supports(s1, s2, s3)
    frame.add_loads(l1, l2, l3)
    frame.solve()
    print(m2.stiffness_matrix/8000)
