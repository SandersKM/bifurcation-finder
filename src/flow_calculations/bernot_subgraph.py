from typing  import *
from functools import reduce
import math
import numpy as np   
import operator
try:
    from src.flow_calculations.node import Node, NodeType
    from src.flow_calculations.point import Point
    from src.flow_calculations.graph import Graph
    from src.flow_calculations.parameters import Parameters
    from src.flow_calculations.circle import Circle
except ImportError:
    from node import Node, NodeType
    from point import Point
    from graph import Graph
    from parameters import Parameters
    from circle import Circle

class Bernot_Subgraph:

    def __init__(self, parameters: Parameters, source1: Node, source2: Node, sink: Node):
        self.params: Parameters = parameters
        self.source1: Node = source1 
        self.source2: Node = source2 
        self.get_clockwise_ordering()
        self.sink: Node = sink

    # source1 should be the first in clockwise ordering
    def get_clockwise_ordering(self):
        atan2_source1 = math.atan2(source1.point.x - sink.point.x, source1.point.y - sink.point.y)
        atan2_source2 = math.atan2(source2.point.x - sink.point.x, source2.point.y - sink.point.y)
        print(atan2_source1, atan2_source2)
        if atan2_source1 > atan2_source2:
            sources = (source2, source1)
            print(sources)
            self.source1 = sources[0]
            self.source2 = sources[1]    

    def get_pivot_point(self):
        return self.source2.point.rotate(self.get_source_circle_intersection(), 2 * self.calculate_optimal_theta2())

    def get_source_circle_intersection(self):
        radius: float = self.get_circle_radius()
        circle1: Circle = Circle(self.source1.point.x, self.source1.point.y, radius)
        circle2: Circle = Circle(self.source2.point.x, self.source2.point.y, radius)
        intersect_result = circle1.circle_intersect(circle2)
        intersect1 = intersect_result[0]
        intersect2 = intersect_result[1]
        if (self.sink.point.get_distance_to(intersect1) < self.sink.point.get_distance_to(intersect2)):
            return intersect1
        return intersect2

    def get_circle_radius(self):
        numerator: float = abs(self.source1.point.get_distance_to(self.source2.point))
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
        return self.calculate_optimal_theta(self.get_k1(), self.get_k2())

    def calculate_optimal_theta2(self) -> float:
        return self.calculate_optimal_theta(self.get_k2(), self.get_k1())

    def get_k1(self):
        return  (self.source1.weight / (self.source2.weight + self.source1.weight)) 

    def get_k2(self):
        return  (self.source2.weight / (self.source1.weight + self.source2.weight)) 
    
source1 = Node(1, Point(7, 5), NodeType.SOURCE)
source2 = Node(1, Point(5, 5), NodeType.SOURCE)
sink = Node(2, Point(3, 2), NodeType.SINK)
params = Parameters(.01, .5)
bernot = Bernot_Subgraph(params, source1, source2, sink)
print(bernot.source1, bernot.source2)

'''
    def get_clockwise_ordering(self):
        coords = [source1, source2]
        center = tuple(map(operator.truediv, reduce(lambda x, y: map(operator.add, x, y), coords), [len(coords)] * 2))
        sorted(coords, key=lambda coord: (-135 - math.degrees(math.atan2(*tuple(map(operator.sub, coord, center))[::-1]))) % 360)
'''