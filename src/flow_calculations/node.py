from point import Point
from enum import Enum
import typing

class NodeType(Enum):
    SOURCE: int = 1
    SINK: int = 2

class Node:
    """ A class used to represent a transportation network node.

    Attributes
    ----------
    weight : float
        weight of the given node
    point : Point
        (x, y) coordinate location of the node on a 2D plane
    nodeType: NodeType
        denotes whether node is a source or a sink

    Methods
    -------
    getWeight()
        Returns weight of the node
    getPoint()
        Returns (x, y) coordinate of the node
    getNodeType(other)
        Returns whether node is a source or sink
    """

    def __init__(self, weight: float, point: Point, nodeType: NodeType):
        self.weight: float = weight
        self.point: Point = point
        self.nodeType: NodeType = nodeType

    def getWeight(self):
        return self.weight
    
    def getPoint(self):
        return self.point

    def getNodeType(self):
        return self.nodeType
