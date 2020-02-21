from typing  import *
import math
import numpy as np
try:
    from src.flow_calculations.node import Node, NodeType
    from src.flow_calculations.point import Point
    from src.flow_calculations.graph import Graph
    from src.flow_calculations.parameters import Parameters
except ImportError:
    from node import Node, NodeType
    from point import Point
    from graph import Graph
    from parameters import Parameters

class Bernot_Subgraph:

    def __init__(self, parameters: Parameters, source1: Node, source2: Node, bifurcation: Point):
        self.params: Parameters = parameters
        self.source1 = source1
        self.source2 = source2
        self.bifurcation_point: Point = bifurcation

    # Using the Shoelace Formula
    def calculate_triangle_area(self, a: Point, b: Point, c: Point) -> float:
        if (a == b or b == c or a == c):
            return 0
        return abs((1 / 2) * (
            a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y)))

    def get_circle_radius(self):
        numerator: float = abs(self.source1.point.get_distance_to(self.source2))
        denominator: float = 2 * math.sin(self.calculate_optimal_theta_combined())
        return numerator / denominator
    
    def calculate_optimal_theta_combined(self):
        k1: float = self.get_k1()
        k2: float = self.get_k2()
        numerator: float = 1 - (k2 ** (2 * self.params.alpha)) - (k1 ** (2 * self.params.alpha))
        denominator: float =  2 * (k2 ** self.params.alpha) * (k1 ** self.params.alpha)
        cos_optimal: float = numerator / denominator
        angle: float = math.acos(cos_optimal)
        return math.degrees(angle)

    def calculate_optimal_theta(self, k_first: float, k_second: float) -> float:
        numerator: float = (k_first ** (2 * self.params.alpha)) + 1 - (k_second ** (2 * self.params.alpha))
        denominator: float =  2 * (k_first ** self.params.alpha)
        cos_optimal: float = numerator / denominator
        angle: float = math.acos(cos_optimal)
        return math.degrees(angle)

    def calculate_optimal_theta1(self) -> float:
        return self.calculate_optimal_theta(self.get_k1, self.get_k2)

    def calculate_optimal_theta2(self) -> float:
        return self.calculate_optimal_theta(self.get_k2, self.get_k1)

    def get_k1(self):
        return  (self.source1.weight / (self.source2.weight + self.source1.weight)) 

    def get_k2(self):
        return  (self.source2.weight / (self.source1.weight + self.source2.weight)) 

    

    

