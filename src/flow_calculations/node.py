import typing
import math
from enum import Enum
try:
    from src.flow_calculations.point import Point
except ImportError:
    from point import Point

class NodeType(Enum):
    SOURCE = 1
    SINK = 2
    BIFURCATION = 3

class Node:
    """ A class used to represent a transportation network node.
    Attributes
    ----------
    weight : float
        weight of the given node
    point : Point
        (x, y) coordinate location of the node on a 2D plane
    node_type : NodeType
        Enum value that denotes whether the node is a source, sink, or bifurcation
    Methods
    -------
    weight()
        Returns weight of the node
    point()
        Returns (x, y) coordinate of the node
    get_distance_to()
        Returns distance to another node
    """

    def __init__(self, weight: float, point: Point, node_type: NodeType):
        self.weight: float = weight
        self.point: Point = point
        self.node_type: NodeType = node_type

    def __repr__(self):
        return f"<{self.node_type.name}, {self.point}, {self.weight}>"

    @property
    def weight(self) -> float:
        return self._weight

    @weight.setter
    def weight(self, value) -> None:
        self._weight: float = value
    
    @property
    def point(self) -> Point:
        return self._point

    @point.setter
    def point(self, value) -> None:
        self._point: Point = value

    @property
    def node_type(self) -> NodeType:
        return self._node_type

    @node_type.setter
    def node_type(self, value) -> None:
        self._node_type: NodeType = value

    def get_distance_to(self, other) -> float:
        return self.point.get_distance_to(other.point)
