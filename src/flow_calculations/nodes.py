import typing
from typing  import List
import math
try:
    from src.flow_calculations.node import Node
    from src.flow_calculations.point import Point
except ImportError:
    from node import Node
    from point import Point
    
class Nodes:

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

    def popBifurcation(self) -> Point:
        return self.bifurcations.pop()

    def getSinks(self) -> List[Nodes]:
        return self.sinks

    def getSources(self) -> List[Nodes]:
        return self.sources

    def getSinkWeights(self) -> List[float]:
        return [node.weight for node in self.sinks]

    def getSourceWeights(self) -> List[float]:
        return [node.weight for node in self.sources]

    def getSinkPoints(self) -> List[Point]:
        return [node.point for node in self.sinks]

    def getSourcePoints(self) -> List[Point]:
        return [node.point for node in self.sources]

    def getBifurcationPoints(self) -> List[Point]:
        return self.bifurcations