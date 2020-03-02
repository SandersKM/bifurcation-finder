from sympy import *
from sympy.geometry import *
import typing
from typing  import List, Dict
from functools import reduce
import math
import numpy as np   
import operator
try:
    from src.flow_calculations.node import Node, NodeType
    from src.flow_calculations.parameters import Parameters
    from src.flow_calculations.bernot_subgraph import Bernot_Subgraph
except ImportError:
    from node import Node, NodeType
    from parameters import Parameters
    from bernot_subgraph import Bernot_Subgraph

class Bernot_Graph:

    def __init__(self, parameters: Parameters, sources: [Node], sink: Node) -> None:
        self.parameters = parameters
        self._sources: [Node] = sources
        self._sink: Node = sink
        self.get_clockwise_ordering()
        self._subgraphs = self.get_subgraphs()
        self.edge_map = {}
        self.get_bifurcations()
        self.print_final_graph()

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

    def get_next_subgraph(self, source_list):
        right_closeness = abs(source_list[0].get_distance_to(source_list[1]))
        left_closeness = abs(source_list[-1].get_distance_to(source_list[-2]))
        across_closeness = abs(source_list[-1].get_distance_to(source_list[0]))
        if right_closeness < left_closeness and right_closeness < across_closeness:
            return Bernot_Subgraph(self.parameters, source_list[0], source_list[2], self.sink)
        elif left_closeness < right_closeness and left_closeness < across_closeness:
            return Bernot_Subgraph(self.parameters, source_list[-2], source_list[-1], self.sink)
        return Bernot_Subgraph(self.parameters, source_list[-1], source_list[0], self.sink)
    
    def get_subgraphs(self):
        subgraphs = []
        sources_copy = self.sources.copy()
        while len(sources_copy) > 1:
            subgraph = self.get_next_subgraph(sources_copy)
            subgraphs.append(subgraph)
            #print(sources_copy, subgraph.source1, subgraph.source1 == sources_copy[1])
            sources_copy.remove(subgraph.source1)
            sources_copy.remove(subgraph.source2)
            sources_copy.append(subgraph.pivot_node)
        return subgraphs
    
    def get_bifurcations(self):
        # lol I need to make this better so that pivot points are labeled somehow
        # like a dictionary?
        end_nodes = [self.sink]

        for i in range(len(self._subgraphs)):
            subgraph: Bernot_Subgraph = self._subgraphs[-i]
            endpoint = sorted(end_nodes, key=lambda node: node.get_distance_to(subgraph.pivot_node))[0]
            #if len(Triangle(subgraph.sink.point, subgraph.source2.point, subgraph.source1.point).intersection(subgraph.pivot_node.point)) > 0:
            
            subgraph.get_bifurcation_point(endpoint.point)
            end_nodes.append(subgraph.bifurcation)
        
        # if there are things left in sources copy, add them as edges straight to the sink

    def print_final_graph(self):
        for s in self._subgraphs:
            print("Subgraph with Sources: ", s.source1, s.source2)
            print("Pivot Point:", s.pivot_node.point.x.round(3), s.pivot_node.point.y.round(3))
            print("Bifurcation:", s.bifurcation.point.x.round(3), s.bifurcation.point.y.round(3))
            print("\n")

    
source1 = Node(1, Point(7, 5), NodeType.SOURCE)
source2 = Node(1, Point(5, 5), NodeType.SOURCE)
source3 = Node(1, Point(0, 5), NodeType.SOURCE)
sources = [source1, source2, source3]
sink = Node(2, Point(3, 2), NodeType.SINK)
params = Parameters(.01, .5)
bernot = Bernot_Graph(params, [source1, source2, source3], sink)

