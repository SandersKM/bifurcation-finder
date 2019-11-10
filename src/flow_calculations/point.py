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
    getX()
        Returns x-coordinate
    getY()
        Returns y-coordinate
    calculateDistance(other)
        Calculates Euclidean distance between this point and the other point
    """

    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y

    def getX(self) -> float:
        return self.x
    
    def getY(self) -> float:
        return self.y

    def calculateDistance(self, other) -> float:
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
        
        xDiff: float = (self.x - other.x)
        yDiff: float = (self.y - other.y)
        return math.sqrt(xDiff**2 + yDiff**2)