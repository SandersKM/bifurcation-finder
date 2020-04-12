from sympy import *
from sympy.geometry import *
import typing
from typing  import List, Dict
from functools import reduce
import math
import numpy as np   
import operator
try:
    from src.bernot_calculations.bernot_node import BerNode, NodeType
    from src.bernot_calculations.bernot_subgraph import Bernot_Subgraph
except ImportError:
    from bernot_node import BerNode, NodeType
    from bernot_subgraph import Bernot_Subgraph

class Bernot_Graph:
    SIG_FIGS = 3

    def __init__(self, sources: [BerNode], sink: BerNode, alpha: float) -> None:
        self._sink: BerNode = sink
        self._sources: [BerNode] = self.get_clockwise_ordering(sources)
        self._alpha: float = alpha
        self._subgraph_map = {}
        self.top_pivot = None
        self.edge_map = {}
        starting_points = [self.round_node(node) for node in sources]
        starting_points.append(self.round_node(sink))
        self.visualization_steps = [("start", {"points": starting_points})]
        self.make_pivot_nodes()
        self.get_bifurcations(self.subgraph_map[str(self.top_pivot)], self.sink)
        last_visualization_values = self.visualization_steps[-1][1]
        last_label = "Final network. M alpha Cost: " +  str(self.get_M_alpha(last_visualization_values["segments"]))
        self.visualization_steps[len(self.visualization_steps) - 1] = (last_label, last_visualization_values)
        #self.print_final_graph()

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

    def get_M_alpha(self, segments):
        M_alpha = 0
        for seg in segments.keys(): 
            length: float = float(abs(seg[0].distance(seg[1])))
            weight: float = segments[seg]
            M_alpha += (weight**self.alpha) * length
        return round(M_alpha, Bernot_Graph.SIG_FIGS)

    def get_arctan(self, node):
        return math.atan2(node.point.x - self.sink.point.x, \
            node.point.y - self.sink.point.y)

    def get_clockwise_ordering(self, nodes):
        return sorted(nodes, key=lambda node: self.get_arctan(node))

    def subgraph_with_sources(self, source1: BerNode, source2:BerNode):
        return Bernot_Subgraph(source1, source2, self.sink, self.alpha)

    def is_only_pivots(self, source_list):
        for i in range(len(source_list)):
            if source_list[i].node_type == NodeType.SOURCE:
                return False
        return True

    def get_next_subgraph_only_pivots(self, source_list):
        right_closeness = abs(source_list[0].get_distance_to(source_list[1]))
        left_closeness = abs(source_list[-1].get_distance_to(source_list[-2]))
        across_closeness = abs(source_list[-1].get_distance_to(source_list[0]))
        if right_closeness < left_closeness and right_closeness < across_closeness:
            sorted_nodes = self.get_clockwise_ordering([source_list[0], source_list[1]])
            return self.subgraph_with_sources(sorted_nodes[0], sorted_nodes[1])
        elif left_closeness < right_closeness and left_closeness < across_closeness:
            sorted_nodes = self.get_clockwise_ordering(source_list[-2], source_list[-1])
            return self.subgraph_with_sources(sorted_nodes[0], sorted_nodes[1])
        sorted_nodes = self.get_clockwise_ordering(source_list[-1], source_list[0])
        return self.subgraph_with_sources(sorted_nodes[0], sorted_nodes[1])

    def get_next_subgraph(self, source_list):
        if (len(source_list) == 2):
            return (True, self.subgraph_with_sources(source_list[0], source_list[1]))
        if self.is_only_pivots(source_list):
            return self.get_next_subgraph_only_pivots(source_list)
        farthest_source_from_sink = None
        max_distance = 0
        for i in range(len(source_list)):
            if source_list[i].node_type == NodeType.SOURCE:
                this_distance = source_list[i].get_distance_to(self.sink)
                if  this_distance > max_distance:
                    max_distance = this_distance
                    farthest_source_from_sink = source_list[i]
        next_closest_source = None
        min_distance = float("inf")
        for i in range(len(source_list)):
            this_distance = source_list[i].get_distance_to(farthest_source_from_sink)
            if  this_distance < min_distance and (source_list[i] != farthest_source_from_sink):
                min_distance = this_distance
                next_closest_source = source_list[i]
        if min_distance >= farthest_source_from_sink.get_distance_to(self.sink):
            self.make_line_to_sink(farthest_source_from_sink)
            return (False, farthest_source_from_sink)
        sorted_nodes = self.get_clockwise_ordering([farthest_source_from_sink, next_closest_source])
        return (True, self.subgraph_with_sources(sorted_nodes[0], sorted_nodes[1]))

    def make_line_to_sink(self, node):
        if not ("segments" in self.visualization_steps[-1][1]):
            segments = {}
        else:
            segments = self.visualization_steps[-1][1]["segments"].copy()
        segments[(self.round_point(self.sink.point), self.round_point(node.point))] = node.weight
        self.visualization_steps.append(("connect isolated point", {"points": self.visualization_steps[-1][1]["points"], "segments": segments}))

    def round_point(self, point: Point):
        return Point( self.round(point.x) , self.round(point.y))

    def round_node(self, node: BerNode):
        return BerNode(node.weight, self.round_point(node.point), node.node_type)

    def round(self, n: float):
        return n.round(Bernot_Graph.SIG_FIGS)

    def make_pivot_visualization_steps(self, subgraph: Bernot_Subgraph):
        if not ("segments" in self.visualization_steps[-1][1]):
            segments = {}
        else:
            segments = self.visualization_steps[-1][1]["segments"].copy()
        points = self.visualization_steps[-1][1]["points"].copy()
        circles = [(self.round_point(subgraph.source1.point), self.round(subgraph.radius)), \
            (self.round_point(subgraph.source2.point), self.round(subgraph.radius))]
        self.visualization_steps.append(("get circles", {"points": points, "circles": circles, "segments": segments}))
        center_circle = [(self.round_point(subgraph.center), self.round(subgraph.radius))]
        self.visualization_steps.append(("get intersection circle", {"points": points, \
            "circles": circles + center_circle, "segments": segments}))
        pivot = [self.round_node(subgraph.pivot_node)]
        self.visualization_steps.append(("get pivot", {"points": points + pivot,\
             "circles": center_circle, "segments": segments}))
        points2 = points.copy()
        points2.remove(self.round_node(subgraph.source2))
        points2.remove(self.round_node(subgraph.source1))
        self.visualization_steps.append(("collapse points", {"points": points2 + pivot, "segments": segments}))

    def make_bifurcation_visualization_steps(self, subgraph: Bernot_Subgraph, endnode: BerNode):
        points = self.visualization_steps[-1][1]["points"].copy()
        points.append(self.round_node(subgraph.bifurcation))
        center_circle = [(self.round_point(subgraph.center), self.round(subgraph.radius))]
        big_line = (self.round_point(subgraph.pivot_node.point), self.round_point(endnode.point))
        segments = self.visualization_steps[-1][1]["segments"].copy()
        if big_line not in segments:
            segments[big_line] = None
        self.visualization_steps.append(("bifurcation point found at (" +\
             str(round(subgraph.bifurcation.point.x, Bernot_Graph.SIG_FIGS)) + \
                  ", " + str(round(subgraph.bifurcation.point.y, Bernot_Graph.SIG_FIGS)) + ")", \
                      {"points": points, "circles": center_circle, "segments": segments}))
        segments2 = segments.copy()
        del segments2[big_line]
        segments2[(self.round_point(endnode.point), self.round_point(subgraph.bifurcation.point))] = subgraph.bifurcation.weight
        segments2[(self.round_point(subgraph.source1.point), self.round_point(subgraph.bifurcation.point))] = subgraph.source1.weight
        segments2[(self.round_point(subgraph.source2.point), self.round_point(subgraph.bifurcation.point))] = subgraph.source2.weight
        points2 = points.copy()
        points2.remove(self.round_node(subgraph.pivot_node))
        points2.append(self.round_node(subgraph.source1))
        points2.append(self.round_node(subgraph.source2))
        self.visualization_steps.append(("connect bifurcation", {"points": points2, "segments": segments2}))
        
    def make_pivot_nodes(self):
        startnodes = self.sources.copy()
        while len(startnodes) > 1:
            is_subgraph, result = self.get_next_subgraph(startnodes)
            if is_subgraph:
                startnodes.remove(result.source1)
                startnodes.remove(result.source2)
                self.make_pivot_visualization_steps(result)
                startnodes.append(result.pivot_node)
                startnodes = self.get_clockwise_ordering(startnodes)
                self._subgraph_map[str(result.pivot_node)] = result
            else:
                startnodes.remove(result)
        self.top_pivot = startnodes[0]
    
    def get_bifurcations(self, subgraph: Bernot_Subgraph, endnode: BerNode):
        subgraph.get_bifurcation_point(endnode.point)
        print(subgraph.bifurcation)
        self.make_bifurcation_visualization_steps(subgraph, endnode)
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