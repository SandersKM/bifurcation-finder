import typing
from typing import Type
import math
import numpy as np
from enum import Enum

class Orientation(Enum):
    CLOCKWISE = 1           # right turn
    COUNTERCLOCKWISE = 2    # left turn
    COLINEAR = 3            # left turn


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

    # http://www.dcs.gla.ac.uk/~pat/52233/slides/Geometry1x1.pdf
    def orientation(self, joining_vertex, ending_vertex): 
        slope_starting_to_joining: float = (joining_vertex.y - self.y) / (joining_vertex.x - self.x)
        slope_joining_to_ending: float = (ending_vertex.y - joining_vertex.y) / (ending_vertex.x - joining_vertex.x)
        if slope_starting_to_joining > slope_joining_to_ending:
            return Orientation.CLOCKWISE
        elif slope_starting_to_joining < slope_joining_to_ending:
            return Orientation.COUNTERCLOCKWISE
        return Orientation.COLINEAR

    # https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python
    def rotate(self, origin, angle: float):
        """
        Rotate a point counterclockwise by a given angle around a given origin.

        The angle should be given in radians.
        """
        angle = math.radians(angle)
        qx = origin.x + math.cos(angle) * (self.x - origin.x) - math.sin(angle) * (self.y - origin.y)
        qy = origin.y + math.sin(angle) * (self.x - origin.x) + math.cos(angle) * (self.y - origin.y)
        return Point(qx, qy)

# Driver code 
"""
p1 = Point(0, 0) 
p2 = Point(4, 4) 
p3 = Point(1, 2) 
  
o = p1.orientation(p2, p3) 
  
if (o == 3): 
    print("Linear") 
elif (o == 1): 
    print("Clockwise") 
else: 
    print("CounterClockwise") 
"""