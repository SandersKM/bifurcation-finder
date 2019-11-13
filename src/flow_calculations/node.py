from point import Point
import typing
import math

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
    getWeight()
        Returns weight of the node
    getPoint()
        Returns (x, y) coordinate of the node
    """

    def __init__(self, weight: float, point: Point):
        self.weight: float = weight
        self.point: Point = point

    def getWeight(self):
        return self.weight
    
    def getPoint(self):
        return self.point

    def getDistanceTo(self, other):
        return self.getPoint().calculateDistance(other.getPoint())
