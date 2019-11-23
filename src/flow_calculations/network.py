from typing  import *
import math
try:
    from src.flow_calculations.node import Node
    from src.flow_calculations.point import Point
    from src.flow_calculations.nodes import Nodes
except ImportError:
    from node import Node
    from point import Point
    from nodes import Nodes

class Network:

    def __init__(self, h: float, alpha: float, nodes: Nodes):
        self.h: float = h
        self.alpha: float = alpha
        self.nodes: Nodes = nodes
        self.bifurcation_point: Point = nodes.get_bifurcation_points()[0]

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

    @property
    def nodes(self) -> Nodes:
        return self._nodes

    @nodes.setter
    def nodes(self, value):
        self._nodes = value
        self.bifurcation_point = self.nodes.get_bifurcation_points()[0]

    def calculate_g(self, new_bifurcation_point: float) -> float: 
        M: float = (self.calculate_individual_cost(new_bifurcation_point) + self.calculate_carpool_cost(new_bifurcation_point))
        fill: float = self.calculate_fill(new_bifurcation_point)
        return fill + M**2

    def calculate_fill(self, x) -> float: 
        totalArea: float = 0
        for node in self.nodes.get_sources():
            triangle: float = ((self.bifurcation_point.x - x) * (node.weight ** self.alpha) * node.point.y) / 2
            totalArea += triangle
        return (totalArea ** 2) / self.h 

    def calculate_individual_cost(self, x) -> float: 
        total: float = 0
        sink_point_y = self.nodes.get_sink_points()[0].y
        for point in self.nodes.get_source_points():
            total += ((x ** 2) + (point.y - sink_point_y)**2)**(1/2)
        return total 

    def calculate_carpool_cost(self, x) -> float: 
        edge_length: float = ( self.nodes.get_sink_points()[0].x - x )
        combined_weight: float = 0
        for weight in self.nodes.get_source_weights():
            combined_weight += weight
        alpha_adjusted_weight: float = (combined_weight ** self.alpha)
        return  alpha_adjusted_weight * edge_length

    def calculate_bifurcation_angle(self) -> float:
        source_points = self.nodes.get_source_points()
        length_bif_s0 = source_points[0].get_distance_to(self.bifurcation_point)
        length_bif_s1 = source_points[1].get_distance_to(self.bifurcation_point)
        length_s0_s1 = source_points[0].get_distance_to(source_points[1])
        numerator = length_bif_s0**2 + length_bif_s1**2 - length_s0_s1**2
        denominator = 2 * length_bif_s0 * length_bif_s1
        cos_bif = numerator/denominator # Law of Cosines
        angle = math.acos(cos_bif)
        return math.degrees(angle)

    

