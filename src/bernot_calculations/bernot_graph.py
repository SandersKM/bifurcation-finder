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
    SIG_FIGS = 3

    def __init__(self, sources: [Node], sink: Node, alpha: float) -> None:
        self._sink: Node = sink
        self._sources: [Node] = self.get_clockwise_ordering(sources)
        self._alpha: float = alpha
        self._subgraph_map = {}
        self.top_pivot = None
        self.edge_map = {}
        starting_points = [self.round_node(node) for node in sources]
        starting_points.append(self.round_node(sink))
        self.visualization_steps = [("start", {"points": starting_points})]
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
        return math.atan2(node.point.x - self.sink.point.x, \
            node.point.y - self.sink.point.y)


    def get_clockwise_ordering(self, nodes):
        return sorted(nodes, key=lambda node: self.get_arctan(node))

    def subgraph_with_sources(self, source1: Node, source2:Node):
        return Bernot_Subgraph(source1, source2, self.sink, self.alpha)

    def get_next_subgraph(self, source_list):
        if (len(source_list) == 2):
            return self.subgraph_with_sources(source_list[0], source_list[1])
        right_closeness = abs(source_list[0].get_distance_to(source_list[1]))
        left_closeness = abs(source_list[-1].get_distance_to(source_list[-2]))
        across_closeness = abs(source_list[-1].get_distance_to(source_list[0]))
        if right_closeness < left_closeness and right_closeness < across_closeness:
            return self.subgraph_with_sources(source_list[0], source_list[1])
        elif left_closeness < right_closeness and left_closeness < across_closeness:
            return self.subgraph_with_sources(source_list[-2], source_list[-1])
        return self.subgraph_with_sources(source_list[-1], source_list[0])

    def round_point(self, point: Point):
        return Point( self.round(point.x) , self.round(point.y))

    def round_node(self, node: Node):
        return Node(node.weight, self.round_point(node.point), node.node_type)

    def round(self, n: float):
        return n.round(Bernot_Graph.SIG_FIGS)

    def make_pivot_visualization_steps(self, subgraph: Bernot_Subgraph):
        points = self.visualization_steps[-1][1]["points"].copy()
        circles = [(self.round_point(subgraph.source1.point), self.round(subgraph.radius)), \
            (self.round_point(subgraph.source2.point), self.round(subgraph.radius))]
        self.visualization_steps.append(("get circles", {"points": points, "circles": circles}))
        center_circle = [(self.round_point(subgraph.center), self.round(subgraph.radius))]
        self.visualization_steps.append(("get intersection circle", {"points": points, "circles": circles + center_circle}))
        pivot = [self.round_node(subgraph.pivot_node)]
        self.visualization_steps.append(("get pivot", {"points": points + pivot, "circles": center_circle}))
        points2 = points.copy()
        print("points2: ", points2)
        print("removing:", self.round_node(subgraph.source1), self.round_node(subgraph.source2))
        points2.remove(self.round_node(subgraph.source2))
        points2.remove(self.round_node(subgraph.source1))
        self.visualization_steps.append(("collapse points", {"points": points2 + pivot}))
        
    def make_pivot_nodes(self):
        startnodes = self.sources.copy()
        while len(startnodes) > 1:
            subgraph = self.get_next_subgraph(startnodes)
            startnodes.remove(subgraph.source1)
            startnodes.remove(subgraph.source2)
            self.make_pivot_visualization_steps(subgraph)
            startnodes.append(subgraph.pivot_node)
            startnodes = self.get_clockwise_ordering(startnodes)
            self._subgraph_map[str(subgraph.pivot_node)] = subgraph
        self.top_pivot = startnodes[0]
        print("top pivot", self.top_pivot)
    
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
            print("Circle: center:(", s.center.x.round(3), s.center.y.round(3), ") radius: ", s.radius.round(3))
            print("Pivot Point:", s.pivot_node.point.x.round(3), s.pivot_node.point.y.round(3))
            print("Bifurcation:", s.bifurcation.point.x.round(3), s.bifurcation.point.y.round(3))
            print("\n")

'''


source1 = Node(5, Point(1,5), NodeType.SOURCE)
source2 = Node(2, Point(3,4), NodeType.SOURCE)
sources = [source1, source2]
sink = Node(7, Point(0,0), NodeType.SINK)
bernot = Bernot_Graph( [source1, source2], sink, 0.5)

source1 = Node(5, Point(1,4), NodeType.SOURCE)
source2 = Node(2, Point(5,1), NodeType.SOURCE)
sources = [source1, source2]
sink = Node(7, Point(0,0), NodeType.SINK)
bernot = Bernot_Graph( [source1, source2], sink, 0.5)
'''


#source1 = Node(1, Point(0, 4), NodeType.SOURCE)
#source2 = Node(1, Point(2,4), NodeType.SOURCE)
#source3 = Node(1, Point(4, 3), NodeType.SOURCE)
#sources = [source1, source2, source3]
#sink = Node(3, Point(3, 0), NodeType.SINK)
#bernot = Bernot_Graph( [source1, source2, source3], sink, 0.5)