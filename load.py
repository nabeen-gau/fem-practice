from dataclasses import dataclass
from point import Point
from member import Member


@dataclass
class NodalLoad:
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

    def __add__(self, other: "NodalLoad"):
        return NodalLoad(self.x+other.x, self.y+other.y, self.m+other.m)

    def __sub__(self, other: "NodalLoad"):
        return NodalLoad(self.x-other.x, self.y-other.y, self.m-other.m)


@dataclass
class MemberLoad:
    start_value: float
    end_value: float
    member: Member

    def __add__(self, other: "MemberLoad"):
        return MemberLoad(self.start_value+other.start_value,
                          self.end_value+other.end_value,
                          self.member)

    def __sub__(self, other: "MemberLoad"):
        return MemberLoad(self.start_value-other.start_value,
                          self.end_value-other.end_value,
                          self.member)
