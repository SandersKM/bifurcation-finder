from typing import *
from scipy.optimize import minimize_scalar
import math
try:
    from src.flow_calculations.node import Node
    from src.flow_calculations.point import Point
    from src.flow_calculations.nodes import Nodes
    from src.flow_calculations.network import Network
except ImportError:
    from node import Node
    from point import Point
    from nodes import Nodes
    from network import Network

class Flow:

    def __init__(self, network: Network, max_iterations: int = 10000, difference_cuttoff: float = .0000001):
        self.network: Network = network
        self.max_iterations = max_iterations
        self.difference_cuttoff = difference_cuttoff
        self.steps = []
        self.cost = []
        self.theta = []

    def should_repeat(self, i: int):
        if i > self.max_iterations:
            return False
        if self.theta[-1] > 90 - self.difference_cuttoff:
            return False
        return True

    def update_lists(self, minimized: float):
        self.steps.append(minimized)
        self.cost.append(self.network.calculate_g(minimized))
        self.theta.append(self.network.calculate_bifurcation_angle())
        
    def get_flow(self):
        i: int = 0
        node_collection: Nodes = self.network.nodes
        self.update_lists(node_collection.bifurcations[0].x)
        while self.should_repeat(i):
            b = node_collection.pop_bifurcation()
            minimized = minimize_scalar(self.network.calculate_g).x
            bifurcation = Point(minimized, b.y)
            node_collection.add_bifurcation(bifurcation)
            self.network.nodes = node_collection
            self.update_lists(minimized)
            i += 1
        return self.network


