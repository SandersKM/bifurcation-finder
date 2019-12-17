from typing  import *
import math
import numpy as np
import copy
try:
    from src.flow_calculations.node import Node, NodeType
    from src.flow_calculations.point import Point
    from src.flow_calculations.graph import Graph
except ImportError:
    from node import Node, NodeType
    from point import Point
    from graph import Graph

class CostCalculator:

    def __init__(self, old: Graph, h: float, alpha: float):
        self.h: float = h
        self.alpha: float = alpha
        self.old: Graph = old
        self.new: Point = None

    @property
    def h(self):
        return self._h
    
    @h.setter
    def h(self, value):
        self._h = value

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        self._alpha = value 

    def add_new_graph(self, new_bifurcation_arr: np.array):
        new_bifurcation = Node(0, Point(new_bifurcation_arr[0], new_bifurcation_arr[1]), NodeType.BIFURCATION)
        self.new = copy.deepcopy(self.old)
        self.new.remove_bifurcations()
        self.new.add_node(new_bifurcation) 
        for source in self.new.get_sources():
            self.new.add_edge(source, new_bifurcation)
        self.new.add_edge(new_bifurcation, self.new.get_sink())

    def calculate_g(self, new_bifurcation_arr: np.array) -> float:
        new_bifurcation = Point(new_bifurcation_arr[0], new_bifurcation_arr[1]) 
        cost: float = self.calculate_transportation_cost(new_bifurcation)
        fill: float = self.calculate_fill(new_bifurcation)
        #print(f"new_bifurcation: {new_bifurcation}, cost: {cost}, fill: {fill}")
        return (cost**2) + ((fill ** 2) / self.h)

    # Using the Shoelace Formula
    def calculate_triangle_area(self, a: Point, b: Point, c: Point) -> float:
        if (a == b or b == c or a == c):
            return 0
        return abs((1 / 2) * (
            a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y)))

    def calculate_fill(self, new_bifurcation) -> float: 
        sink: Node = self.old.get_sink()
        fill: float = 0
        for node in self.old.get_sources():
            old_area: float = self.calculate_triangle_area(
                self.bifurcation_point, sink.point, node.point)
            new_area: float = self.calculate_triangle_area(
                new_bifurcation, sink.point, node.point)
            area_diff: float = abs(old_area - new_area)
            alpha_adjusted_weight = node.weight ** self.alpha
            fill += area_diff * alpha_adjusted_weight
        return fill

    def calculate_transportation_cost(self, new_bifurcation) -> float:
        individual_cost = self.calculate_individual_cost(new_bifurcation)
        carpool_cost = self.calculate_carpool_cost(new_bifurcation)
        return individual_cost + carpool_cost

    def calculate_individual_cost(self, new_bifurcation) -> float: 
        cost: float = 0
        for source in self.old.get_sources():
            cost += self.calculate_edge_cost(source, new_bifurcation)
        return cost 

    def calculate_carpool_cost(self, new_bifurcation) -> float: 
        sink: Node = self.old.get_sink()
        return self.calculate_edge_cost(sink, new_bifurcation)

    def calculate_edge_cost(self, node: Node, new_bifurcation: Point) -> float:
        length: float = new_bifurcation.get_distance_to(node.point)
        alpha_adjusted_weight: float = (node.weight ** self.alpha)
        return length * alpha_adjusted_weight

    def calculate_bifurcation_angle(self) -> float:
        source_points = self.old.get_source_points()
        length_bif_s0 = source_points[0].get_distance_to(self.bifurcation_point)
        length_bif_s1 = source_points[1].get_distance_to(self.bifurcation_point)
        length_s0_s1 = source_points[0].get_distance_to(source_points[1])
        numerator = length_bif_s0**2 + length_bif_s1**2 - length_s0_s1**2
        denominator = 2 * length_bif_s0 * length_bif_s1
        cos_bif = numerator/denominator # Law of Cosines
        angle = math.acos(cos_bif)
        return math.degrees(angle)

    def calculate_optimal_angle(self):
        m: List[float] = self.old.get_source_weights()
        k0: float = (m[0] / (m[1] + m[0])) 
        k1: float = (m[1] / (m[1] + m[0]))
        numerator: float = 1 - (k1 ** (2 * self.alpha)) - (k0 ** (2 * self.alpha))
        denominator: float =  2 * (k1 ** self.alpha) * (k0 ** self.alpha)
        cos_optimal: float = numerator / denominator
        angle: float = math.acos(cos_optimal)
        return math.degrees(angle)

    

