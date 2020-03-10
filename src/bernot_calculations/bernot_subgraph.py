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

    def get_probable_bifurcation(self, circle: Circle, endpoint: Point):
        seg = Line(self.pivot_node.point, endpoint)
        intersect = circle.intersection(seg)
        if len(intersect) == 1:
            return intersect[0]
        return self.get_closer_point(intersect[0], intersect[1], endpoint)

    def get_bifurcation_point(self, endpoint: Point):
        weight = self.source2.weight + self.source1.weight
        circle = Circle(self.center, self.radius)
        if self.is_v_degeneracy(circle, endpoint):
            self.bifurcation = Node(weight, endpoint, NodeType.BIFURCATION)
        else:
            potential_bifurcation = self.get_probable_bifurcation(circle, endpoint)
            closest_to_endpoint = self.get_closer_point(
                self.source1.point, self.source2.point, endpoint)
            bifurcation_point = self.get_closer_point(
                potential_bifurcation, closest_to_endpoint, endpoint)
            self.bifurcation = Node(weight, bifurcation_point, NodeType.BIFURCATION)

    def get_pivot_node(self):
        degree_radians = 2 * self.calculate_optimal_theta2()
        print("Degree radians", degree_radians)
        print("Source2", self.source2.point.x.round(3))
        location = self.source2.point.rotate(degree_radians, self.center)
        weight = self.source1.weight + self.source2.weight
        return Node(weight, location, NodeType.PIVOT)

    def get_center(self):
        circle1: Circle = Circle(self.source1.point, self.radius)
        circle2: Circle = Circle(self.source2.point, self.radius)
        intersects = circle1.intersection(circle2)
        if (len(intersects) == 1):
            return intersects[0]
        return self.get_closer_point(intersects[0], intersects[1], self.sink.point)

    def get_circle_radius(self):
        numerator: float = abs(self.source1.get_distance_to(self.source2))
        denominator: float = 2 * math.sin(self.calculate_optimal_theta_combined())
        print("radius calcs,", numerator, denominator)
        return numerator / denominator
    
    # Returns angle in radians
    def calculate_optimal_theta_combined(self):
        k1: float = self.get_k1()
        k2: float = self.get_k2()
        numerator: float = 1 - (k2 ** (2 * self.alpha)) - (k1 ** (2 * self.alpha))
        denominator: float =  2 * (k2 ** self.alpha) * (k1 ** self.alpha)
        cos_optimal: float = numerator / denominator
        angle: float = math.acos(cos_optimal)
        print(math.degrees(angle))
        return angle

    # Returns angle in radians
    def calculate_optimal_theta(self, k_first: float, k_second: float) -> float:
        numerator: float = (k_first ** (2 * self.alpha)) + \
            1 - (k_second ** (2 * self.alpha))
        denominator: float =  2 * (k_first ** self.alpha)
        cos_optimal: float = numerator / denominator
        angle: float = math.acos(cos_optimal)
        return angle

    def calculate_optimal_theta1(self) -> float:
        return self.calculate_optimal_theta(self.get_k1(), self.get_k2())

    def calculate_optimal_theta2(self) -> float:
        return self.calculate_optimal_theta(self.get_k2(), self.get_k1())

    def get_k1(self):
        return  (self.source1.weight / (self.source2.weight + self.source1.weight)) 

    def get_k2(self):
        return  (self.source2.weight / (self.source1.weight + self.source2.weight)) 