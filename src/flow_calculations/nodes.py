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
    
    def add_source(self, node: Node) -> None:
        self.sources.append(node)

    def add_sink(self, node: Node) -> None:
        self.sinks.append(node)

    def add_bifurcation(self, point: Point) -> None:
        self.bifurcations.append(point)

    def pop_bifurcation(self) -> Point:
        return self.bifurcations.pop()

    def get_sinks(self):
        return self.sinks

    def get_sources(self):
        return self.sources

    def get_sink_weights(self) -> List[float]:
        return [node.weight for node in self.sinks]

    def get_source_weights(self) -> List[float]:
        return [node.weight for node in self.sources]

    def get_sink_points(self) -> List[Point]:
        return [node.point for node in self.sinks]

    def get_source_points(self) -> List[Point]:
        return [node.point for node in self.sources]

    def get_bifurcation_points(self) -> List[Point]:
        return self.bifurcations