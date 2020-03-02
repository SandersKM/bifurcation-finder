from typing  import *
from sympy import *
from sympy.geometry import *
from functools import reduce
import math
import numpy as np   
import operator
try:
    from src.bernot_calculations.node import Node, NodeType
except ImportError:
    from node import Node, NodeType

class Bernot_Subgraph:

    def __init__(self, source1: Node, source2: Node, sink: Node, alpha: float):
        self.source1: Node = source1 # source1 should be the first in clockwise ordering
        self.source2: Node = source2 
        self.sink: Node = sink 
        self.alpha = alpha
        self.radius = self.get_circle_radius()
        self.center: Point = self.get_center()
        self.pivot_node = self.get_pivot_node()
        self.bifurcation = None

    def is_v_degeneracy(self, circle: Circle, endpoint: Point):
        return circle.encloses_point(endpoint)

    def get_closer_point(self, point1: Point, point2: Point, target: Point):
        if point1.distance(target) < point2.distance(target):
            return point1
        return point2

    def is_l_degeneracy(self, endpoint: Point, potential_bifurcation: Point, closest_source_to_sink: Point):
        if self.get_closer_point(potential_bifurcation, closest_source_to_sink, endpoint) == potential_bifurcation:
            return false
        return true

    def get_bifurcation_point(self, endpoint: Point):
        weight = self.source2.weight + self.source1.weight
        circ = Circle(self.center, self.radius)
        if self.is_v_degeneracy(circ, endpoint):
            #print("WHAT", endpoint)
            self.bifurcation = Node(weight, endpoint, NodeType.BIFURCATION)
        else:
            seg = Line(self.pivot_node.point, endpoint)
            intersect = circ.intersection(seg)
            if len(intersect) == 1:
                probable_bifurcation_point = intersect[0]
            else:
                probable_bifurcation_point = self.get_closer_point(intersect[0], intersect[1], self.sink.point)
            closest_source_to_sink = self.get_closer_point(self.source1.point, self.source2.point, self.sink.point)
            if (self.is_l_degeneracy(endpoint, probable_bifurcation_point, closest_source_to_sink)):
                self.bifurcation = Node(weight, closest_source_to_sink, NodeType.BIFURCATION)
            else:
                self.bifurcation = Node(weight, probable_bifurcation_point, NodeType.BIFURCATION)

    def get_pivot_node(self):
        #print("intersection: ", self.get_center())
        #print("rotation:", 2 * self.calculate_optimal_theta2())
        degree_radians = math.radians(2 * self.calculate_optimal_theta2())
        location = self.source2.point.rotate(degree_radians, self.center)
        #print("location: ", location)
        weight = self.source1.weight + self.source2.weight
        return Node(weight, location, NodeType.SOURCE)

    def get_center(self):
        circle1: Circle = Circle(Point(self.source1.point.x, self.source1.point.y), self.radius)
        circle2: Circle = Circle(Point(self.source2.point.x, self.source2.point.y), self.radius)
        intersect_result = circle1.intersection(circle2)
        intersect1: Point = intersect_result[0]
        intersect2: Point = intersect_result[1]
        sink_point: Point = Point(self.sink.point.x, self.sink.point.y)
        if (sink_point.distance(intersect1) < sink_point.distance(intersect2)):
            return intersect1
        return intersect2

    def get_circle_radius(self):
        numerator: float = abs(self.source1.point.distance(self.source2.point))
        denominator: float = 2 * math.sin(self.calculate_optimal_theta_combined())
        #print("radius:", numerator / denominator)
        return numerator / denominator
    
    def calculate_optimal_theta_combined(self):
        k1: float = self.get_k1()
        k2: float = self.get_k2()
        numerator: float = 1 - (k2 ** (2 * self.alpha)) - (k1 ** (2 * self.alpha))
        denominator: float =  2 * (k2 ** self.alpha) * (k1 ** self.alpha)
        cos_optimal: float = numerator / denominator
        angle: float = math.acos(cos_optimal)
        return math.degrees(angle)

    def calculate_optimal_theta(self, k_first: float, k_second: float) -> float:
        numerator: float = (k_first ** (2 * self.alpha)) + 1 - (k_second ** (2 * self.alpha))
        denominator: float =  2 * (k_first ** self.alpha)
        cos_optimal: float = numerator / denominator
        angle: float = math.acos(cos_optimal)
        return math.degrees(angle)

    def calculate_optimal_theta1(self) -> float:
        return self.calculate_optimal_theta(self.get_k1(), self.get_k2())

    def calculate_optimal_theta2(self) -> float:
        return self.calculate_optimal_theta(self.get_k2(), self.get_k1())

    def get_k1(self):
        return  (self.source1.weight / (self.source2.weight + self.source1.weight)) 

    def get_k2(self):
        return  (self.source2.weight / (self.source1.weight + self.source2.weight)) 