from typing  import *
import math
import numpy as np
try:
    from src.flow_calculations.node import Node
    from src.flow_calculations.point import Point
    from src.flow_calculations.vertices import Vertices
except ImportError:
    from node import Node
    from point import Point
    from vertices import Vertices

class Network:

    def __init__(self, h: float, alpha: float, vertices: Vertices):
        self.h: float = h
        self.alpha: float = alpha
        self.vertices: Vertices = vertices
        self.bifurcation_point: Point = vertices.get_bifurcation_points()[0]

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
    def vertices(self) -> Vertices:
        return self._vertices

    @vertices.setter
    def vertices(self, value):
        self._vertices = value
        self.bifurcation_point = self.vertices.get_bifurcation_points()[0]

    def calculate_g(self, new_bifurcation_point_array: np.array) -> float:
        new_bifurcation_point = Point(new_bifurcation_point_array[0], new_bifurcation_point_array[1]) 
        M: float = (self.calculate_individual_cost(new_bifurcation_point) + self.calculate_carpool_cost(new_bifurcation_point.x))
        fill: float = self.calculate_fill(new_bifurcation_point.x)
        return fill + M**2

    def calculate_fill(self, x) -> float: 
        totalArea: float = 0
        for node in self.vertices.get_sources():
            triangle: float = ((self.bifurcation_point.x - x) * (node.weight ** self.alpha) * node.point.y) / 2
            totalArea += triangle
        return (totalArea ** 2) / self.h 

    def calculate_individual_cost(self, new_bifurcation_point) -> float: 
        total: float = 0
        for source in self.vertices.get_sources():
            length = new_bifurcation_point.get_distance_to(source.point)
            alpha_adjusted_weight: float = source.weight ** self.alpha
            total += length * alpha_adjusted_weight
        return total 

    def calculate_carpool_cost(self, x) -> float: 
        edge_length: float = ( self.vertices.get_sink_points()[0].x - x )
        combined_weight: float = 0
        for weight in self.vertices.get_source_weights():
            combined_weight += weight
        alpha_adjusted_weight: float = (combined_weight ** self.alpha)
        return  alpha_adjusted_weight * edge_length

    def calculate_bifurcation_angle(self) -> float:
        source_points = self.vertices.get_source_points()
        length_bif_s0 = source_points[0].get_distance_to(self.bifurcation_point)
        length_bif_s1 = source_points[1].get_distance_to(self.bifurcation_point)
        length_s0_s1 = source_points[0].get_distance_to(source_points[1])
        numerator = length_bif_s0**2 + length_bif_s1**2 - length_s0_s1**2
        denominator = 2 * length_bif_s0 * length_bif_s1
        cos_bif = numerator/denominator # Law of Cosines
        angle = math.acos(cos_bif)
        return math.degrees(angle)

    

