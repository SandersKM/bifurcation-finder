from typing import *
from scipy.optimize import minimize
import math
import logging
try:
    from src.flow_calculations.node import Node
    from src.flow_calculations.point import Point
    from src.flow_calculations.vertices import Vertices
    from src.flow_calculations.network import Network
except ImportError:
    from node import Node
    from point import Point
    from vertices import Vertices
    from network import Network

class Flow:

    def __init__(self, network: Network, max_iterations: int = 10000, difference_cutoff: float = .01):
        self.network: Network = network
        self.max_iterations = max_iterations
        self.difference_cutoff = difference_cutoff
        self.optimal_angle: float = network.calculate_optimal_angle()
        self.steps = []
        self.cost = []
        self.theta = []

    def should_repeat(self, i: int):
        if i > 0:
            if i > self.max_iterations:
                return False
            if self.cost[-2] - self.cost[-1] > self.difference_cutoff:
                return False
        return True

    def update_lists(self, bifurcation: Point):
        self.steps.append(bifurcation)
        self.cost.append(self.network.calculate_g(bifurcation.point_as_array()))
        self.theta.append(self.network.calculate_bifurcation_angle())
        #logging.warning(f"{self.steps[-1]}\t{self.cost[-1]}\t{self.theta[-1]}")
        
    def get_flow(self, verbose=False):
        i: int = 0
        node_collection: Vertices = self.network.vertices
        self.update_lists(node_collection.bifurcations[0])
        # checks for L shape criteria - based on cost?
        while self.should_repeat(i):
            b = node_collection.pop_bifurcation()
            minimized = minimize(self.network.calculate_g, b.point_as_array(), method = 'Nelder-Mead')
            if verbose:
                logging.warning(minimized)
            bifurcation = Point(minimized.x[0], minimized.x[1])
            node_collection.add_bifurcation(bifurcation)
            self.network.vertices = node_collection
            self.update_lists(bifurcation)
            i += 1
        return self.network

