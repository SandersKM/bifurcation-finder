import typing
import math
try:
    from src.flow_calculations.point import Point
except ImportError:
    from point import Point

class Node:
    """ A class used to represent a transportation network node.
    Attributes
    ----------
    weight : float
        weight of the given node
    point : Point
        (x, y) coordinate location of the node on a 2D plane
    Methods
    -------
    weight()
        Returns weight of the node
    point()
        Returns (x, y) coordinate of the node
    get_distance_to()
        Returns distance to another node
    """

    def __init__(self, weight: float, point: Point):
        self.weight: float = weight
        self.point: Point = point

    def __repr__(self):
        return f"{self.point}: {self.weight}"

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

    def get_distance_to(self, other) -> float:
        return self.point.get_distance_to(other.point)
