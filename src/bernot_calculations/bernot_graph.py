from sympy import *
from sympy.geometry import *
import typing
from typing  import List, Dict
from functools import reduce
import math
import numpy as np   
import operator
try:
    from src.bernot_calculations.node import Node, NodeType
    from src.bernot_calculations.bernot_subgraph import Bernot_Subgraph
except ImportError:
    from node import Node, NodeType
    from bernot_subgraph import Bernot_Subgraph

class Bernot_Graph:

    def __init__(self, sources: [Node], sink: Node, alpha: float) -> None:
        self._sources: [Node] = sources
        self._sink: Node = sink
        self._alpha: float = alpha
        self.get_clockwise_ordering()
        self._subgraph_map = {}
        self.top_pivot = None
        self.edge_map = {}
        self.make_pivot_nodes()
        self.get_bifurcations(self.subgraph_map[str(self.top_pivot)], self.sink)
        self.print_final_graph()

    @property
    def sources(self):
        return self._sources

    @property
    def sink(self):
        return self._sink      

    @property
    def alpha(self):
        return self._alpha      

    @property
    def subgraph_map(self):
        return self._subgraph_map  

    def get_arctan(self, node):
        return math.atan2(node.point.x - self.sink.point.x, node.point.y - self.sink.point.y)

    def get_clockwise_ordering(self):
        self._sources = sorted(self.sources, key=lambda node: self.get_arctan(node))

    def get_next_subgraph(self, source_list):
        right_closeness = abs(source_list[0].get_distance_to(source_list[1]))
        left_closeness = abs(source_list[-1].get_distance_to(source_list[-2]))
        across_closeness = abs(source_list[-1].get_distance_to(source_list[0]))
        if right_closeness < left_closeness and right_closeness < across_closeness:
            return Bernot_Subgraph(source_list[0], source_list[2], self.sink, self.alpha)
        elif left_closeness < right_closeness and left_closeness < across_closeness:
            return Bernot_Subgraph(source_list[-2], source_list[-1], self.sink, self.alpha)
        return Bernot_Subgraph(source_list[-1], source_list[0], self.sink, self.alpha)
    
    def make_pivot_nodes(self):
        sources_copy = self.sources.copy()
        while len(sources_copy) > 1:
            subgraph = self.get_next_subgraph(sources_copy)
            #print(sources_copy, subgraph.source1, subgraph.source1 == sources_copy[1])
            sources_copy.remove(subgraph.source1)
            sources_copy.remove(subgraph.source2)
            sources_copy.append(subgraph.pivot_node)
            self._subgraph_map[str(subgraph.pivot_node)] = subgraph
        self.top_pivot = sources_copy[0]
    
    def get_bifurcations(self, subgraph: Bernot_Subgraph, endnode: Node):
        subgraph.get_bifurcation_point(endnode.point)
        endnode = subgraph.bifurcation
        if subgraph.source1.node_type == NodeType.PIVOT:
            self.get_bifurcations(self.subgraph_map[str(subgraph.source1)], endnode)
        if subgraph.source2.node_type == NodeType.PIVOT:
            self.get_bifurcations(self.subgraph_map[str(subgraph.source2)], endnode)
        
    def print_final_graph(self):
        for key in self._subgraph_map:
            s = self.subgraph_map[key]
            print("Subgraph with Sources: ", s.source1, s.source2)
            print("Pivot Point:", s.pivot_node.point.x.round(3), s.pivot_node.point.y.round(3))
            print("Bifurcation:", s.bifurcation.point.x.round(3), s.bifurcation.point.y.round(3))
            print("\n")

    
source1 = Node(1, Point(7, 5), NodeType.SOURCE)
source2 = Node(1, Point(5, 5), NodeType.SOURCE)
source3 = Node(1, Point(0, 5), NodeType.SOURCE)
sources = [source1, source2, source3]
sink = Node(3, Point(3, 2), NodeType.SINK)
bernot = Bernot_Graph( [source1, source2, source3], sink, 0.5)