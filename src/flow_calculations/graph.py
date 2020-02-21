import typing
from typing  import List, Dict
import math
try:
    from src.flow_calculations.node import Node, NodeType
    from src.flow_calculations.point import Point
except ImportError:
    from node import Node, NodeType
    from point import Point
    
# Assumptions:
# There is only one source node
# The source node has the cumulative weight of all other nodes
# The bifurcation node has the cumulative weight of the sources leading to it
# All edges start at source nodes

class Graph:

    def __init__(self, sources: (Node, Node), sink: Node, bifurcation: Point) -> None:
        self._sources: (Node, Node) = sources
        self._sink: Node = sink
        self._bifurcation: Node = bifurcation

    @property
    def sources(self):
        return self._sources

    @property
    def sink(self):
        return self._sink

    @property 
    def bifurcation(self):
        return self._bifurcation

    @bifurcation.setter
    def bifurcation(self, value: Node):
        self._bifurcation = value
    
    
   
