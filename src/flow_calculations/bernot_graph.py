import typing
from typing  import List, Dict
from functools import reduce
import math
import numpy as np   
import operator
try:
    from src.flow_calculations.node import Node, NodeType
    from src.flow_calculations.point import Point
    from src.flow_calculations.parameters import Parameters
    from src.flow_calculations.bernot_subgraph import Bernot_Subgraph
except ImportError:
    from node import Node, NodeType
    from point import Point
    from parameters import Parameters
    from bernot_subgraph import Bernot_Subgraph

class Bernot_Graph:

    def __init__(self, parameters: Parameters, sources: [Node], sink: Node) -> None:
        self.parameters = parameters
        self._sources: [Node] = sources
        self._sink: Node = sink
        self.get_clockwise_ordering()
        self._subgraphs = []

    @property
    def sources(self):
        return self._sources

    @property
    def sink(self):
        return self._sink        

    def get_clockwise_ordering(self):
        center = tuple(map(operator.truediv, reduce(lambda x, y: map(operator.add, x, y), self.sources), [len(self.sources)] * 2))
        self.sources = sorted(self.sources, key=lambda coord: (-135 - math.degrees(math.atan2(*tuple(map(operator.sub, coord, center))[::-1]))) % 360)

    def get_next_subgraph(self):
        right_closeness = abs(self.sources[0].get_distance_to(self.sources[1]))
        left_closeness = abs(self.sources[-1].get_distance_to(self.sources[-2]))
        if right_closeness < left_closeness:
            return Bernot_Subgraph(self.parameters, self.sources[0], self.sources[2], self.sink)
        return Bernot_Subgraph(self.parameters, self.sources[-2], self.sources[-1], self.sink)
        

    
   
