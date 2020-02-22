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

    def get_arctan(self, node):
        return math.atan2(node.point.x - self.sink.point.x, node.point.y - self.sink.point.y)

    def get_clockwise_ordering(self):
        self._sources = sorted(self.sources, key=lambda node: self.get_arctan(node))

    def get_next_subgraph(self):
        right_closeness = abs(self.sources[0].get_distance_to(self.sources[1]))
        left_closeness = abs(self.sources[-1].get_distance_to(self.sources[-2]))
        across_closeness = abs(self.sources[-1].get_distance_to(self.sources[0]))
        if right_closeness < left_closeness and right_closeness < across_closeness:
            return Bernot_Subgraph(self.parameters, self.sources[0], self.sources[2], self.sink)
        elif left_closeness < right_closeness and left_closeness < across_closeness:
            return Bernot_Subgraph(self.parameters, self.sources[-2], self.sources[-1], self.sink)
        return Bernot_Subgraph(self.parameters, self.sources[-1], self.sources[0], self.sink)
    
    def create_subgraphs(self):
        while len(self.sources) > 1:
            print(self.sources)
            subgraph = self.get_next_subgraph()
            self.sources.remove(subgraph.source1)
            self.sources.remove(subgraph.source2)
            self.sources.append(subgraph.pivot_node)

    
source1 = Node(1, Point(7, 5), NodeType.SOURCE)
source2 = Node(1, Point(5, 5), NodeType.SOURCE)
source3 = Node(1, Point(0, 5), NodeType.SOURCE)
sources = [source1, source2, source3]
sink = Node(2, Point(3, 2), NodeType.SINK)
params = Parameters(.01, .5)
bernot = Bernot_Graph(params, [source1, source2, source3], sink)
bernot.create_subgraphs()