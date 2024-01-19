import numpy as np
from point import Point
from material import Material
from section import Section
from support import Support, RollerSupport, HingedSupport, FixedSupport
from load import NodalLoad
# from displacement import Displacement
# from node import Node
from member import Member
from grid import PointCollection


class Frame:
    members: list[Member] = []
    DOF: int = 0
    nodes: PointCollection = None
    loads: list[NodalLoad] = []

    def __init__(self, *nodes):
        self.nodes = PointCollection(*nodes)

    def add_members(self, *members: Member):
        self.members = members

    def generate_force_vector(self):
        self.force_vector = np.zeros(self.DOF)
        for load in self.nodes.loads:
            if load:
                index = self.nodes.get_index(load.position)
                # 3 is for 3 loads Fx, Fy, M
                for ig, il in zip(self.nodes.dof_ids[index], range(3)):
                    self.force_vector[ig] = self.nodes.loads[index].values[il]

    def generate_displacement_vector(self):
        self.displacement_vector = np.zeros(self.DOF)

    def generate_global_stiffness_matrix(self):
        self.global_k = np.zeros((self.DOF, self.DOF))

        for member in self.members:
            local_k = member.stiffness_matrix
            begin_index = self.nodes.get_index(member.begin_node)
            end_index = self.nodes.get_index(member.end_node)
            iterable = [*self.nodes.dof_ids[begin_index],
                        *self.nodes.dof_ids[end_index]]
            for ig, il in zip(iterable, range(local_k.shape[0])):
                for jg, jl in zip(iterable, range(local_k.shape[1])):
                    self.global_k[ig, jg] += local_k[il, jl]

    def solve(self):
        self.DOF = 3 * self.nodes.item_count
        self.generate_global_stiffness_matrix()
        self.generate_force_vector()
        self.generate_displacement_vector()
        self.solve_for_unknowns()

    def solve_for_unknowns(self):
        free_dofs = self.nodes.get_free_points()
        specified_dofs = self.nodes.get_fixed_points()

        reduced_stiffness = self.global_k
        reduced_force = self.force_vector

        for index in reversed(specified_dofs):
            reduced_stiffness = np.delete(
                np.delete(reduced_stiffness, index, axis=0), index, axis=1)
            reduced_force = np.delete(reduced_force, index, axis=0)

        reduced_displacement = np.linalg.inv(reduced_stiffness)@reduced_force
        for i, index in enumerate(free_dofs):
            self.displacement_vector[index] = reduced_displacement[i]

        self.reaction_vector = self.global_k@self.displacement_vector - self.force_vector

        print("Reaction forces are:")
        for i in self.reaction_vector:
            print(np.round(i, 3))

    def add_supports(self, *supports: Support) -> None:
        self.supports = supports
        self.nodes.add_supports(*supports)

    def add_loads(self, *loads: NodalLoad) -> None:
        self.loads = loads
        self.nodes.add_loads(*loads)


if __name__ == "__main__":
    E = 2e11
    A = 1
    MOI = 24e-6

    material = Material(E)
    section = Section(A=A, I=MOI)

    n1 = Point(0, 0)
    n2 = Point(0, 5)
    n3 = Point(5, 5)
    n4 = Point(5, 0)

    m1 = Member(n1, n2, material=material, section=section)
    m2 = Member(n2, n3, material=material, section=section)
    m3 = Member(n3, n4, material=material, section=section)

    l1 = NodalLoad(20, 20, 0, n2)
    l2 = NodalLoad(30, -30, 0, n3)

    s1 = HingedSupport(n1)
    s2 = RollerSupport(n4)

    frame = Frame(n1, n2, n3, n4)
    frame.add_members(m1, m2, m3)
    frame.add_supports(s1, s2)
    frame.add_loads(l1, l2)
    frame.solve()
