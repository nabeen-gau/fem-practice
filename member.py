from point import Point
from section import Section
from material import Material
from node import Node
import numpy as np


class Member:
    begin_point: Point
    end_point: Point
    section: Section = Section(1, 1)
    material: Material = Material(1)

    def __init__(self, begin_node: Node, end_node: Node,
                 material: Material = None, section: Section = None):
        self.begin_node = begin_node
        self.end_node = end_node
        if material:
            self.material = material
        if section:
            self.section = section

    @property
    def length(self) -> float:
        return np.round(self.begin_node.distance(self.end_node), 10)

    @property
    def slope(self) -> float:
        return np.round(self.begin_node.slope(self.end_node), 10)

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
    def stiffness(self) -> np.ndarray:
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

    @property
    def stiffness_matrix(self) -> np.ndarray:
        return self.transformation_matrix.T@self.stiffness@self.transformation_matrix

    @property
    def transformation_matrix(self) -> np.ndarray:
        l = self.cosine
        m = self.sine
        return np.array([
            [l,     m,  0,  0,  0,  0],
            [-m,    l,  0,  0,  0,  0],
            [0,     0,  1,  0,  0,  0],
            [0,     0,  0,  l,  m,  0],
            [0,     0,  0,  -m, l,  0],
            [0,     0,  0,  0,  0,  1]
        ])
