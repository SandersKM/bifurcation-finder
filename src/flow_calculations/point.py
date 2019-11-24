import typing
from typing import Type
import math
import numpy as np

class Point():
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
        self._x: float = x
        self._y: float = y

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = value

    def point_as_array(self):
        return np.array([self.x, self.y])

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