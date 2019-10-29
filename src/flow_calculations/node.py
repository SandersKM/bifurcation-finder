from point import Point
from enum import Enum
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

    def __getK1(self, other) -> float:
        return self.getWeight() / (self.getWeight() + other.getWeight())

    def __getK2(self, other) -> float:
        return other.getWeight() / (self.getWeight() + other.getWeight()) 

    def thetaSelfShouldEqual(self, other, alpha: float):
        k1: float = (self.__getK1(other))**(2*alpha)
        k2: float = (self.__getK2(other))**(2*alpha)
        print(f"K1: {k1} K2: {k2}")
        print((k1 + 1 - k2) / (2 * k1))
        return math.degrees((k1 + 1 - k2) / (2 * k1))

    def thetaOtherShouldEqual(self, other, alpha: float):
        k1: float = (self.__getK1(other))**(2*alpha)
        k2: float = (self.__getK2(other))**(2*alpha)
        return math.degrees((k2 + 1 - k1) / (2 * k2))

    def thetaAddedShouldEqual(self, other, alpha: float):
        k1: float = (self.__getK1(other))**(2*alpha)
        k2: float = (self.__getK2(other))**(2*alpha)
        return math.degrees((1 - k1 - k2) / (2 * k1 * k2))

    def getThetaSelf(self, start: Point, bifurcation: Point):
        bifurcationAngle = math.atan2(bifurcation.getY()-start.getY(), bifurcation.getX()-start.getX())
        selfAngle = math.atan2(self.getPoint().getY()-start.getY(), self.getPoint().getX()-start.getX())
        return math.degrees(math.cos(bifurcationAngle - selfAngle))