import typing
from typing import Type
import math

class Point:
    """ A class used to represent an (x, y) coorinate point.
    Attributes
    ----------
    x : float
        x-coordinate of a point on a 2D plane
    y : float
        y-coordinate of a point on a 2D plane
    Methods
    -------
    x()
        Returns float x-coordinate
    y()
        Returns float y-coordinate
    get_distance_to(other)
        Calculates Euclidean distance between this point and the other point
    """

    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    @property
    def x(self) -> float:
        return self._x

    @x.getter
    def x(self, value: float) -> None:
        self._x = value

    @property
    def y(self) -> float:
        return self._y

    @y.getter
    def y(self, value: float) -> None:
        self._y = value

    def get_distance_to(self, other) -> float:
        """
        Parameters
        ----------
        other : Point
            Another object of the Point class
        
        Returns
        -------
        float
            Euclidean distance between this point and the other point
        """
        
        x_diff: float = (self.x - other.x)
        y_diff: float = (self.y - other.y)
        return math.sqrt(x_diff**2 + y_diff**2)