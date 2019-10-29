from node import Node
from point import Point
import numpy as np
import typing
from typing  import List
import math

class Network:

    def __init__(self) -> None:
        self.sources: List[Node] = []
        self.sinks: List[Node] = []
        self.bifurcations: List[Point] = []
    
    def addSource(self, node: Node) -> None:
        self.sources.append(node)

    def addSink(self, node: Node) -> None:
        self.sinks.append(node)

    def addBifurcation(self, point: Point) -> None:
        self.bifurcations.append(point)

    def getSinks(self):
        return self.sinks

    def getSources(self):
        return self.sources

    def getSinkWeights(self):
        return [node.getWeight() for node in self.sinks]

    def getSourceWeights(self):
        return [node.getWeight() for node in self.sources]

    def getSinkPoints(self):
        return [node.getPoint() for node in self.sinks]

    def getSourcePoints(self):
        return [node.getPoint() for node in self.sources]

    def getBifurcationPoints(self):
        return self.bifurcations