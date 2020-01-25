from typing import *
from scipy.optimize import minimize
import math
import logging
try:
    from src.flow_calculations.node import Node, NodeType
    from src.flow_calculations.point import Point
    from src.flow_calculations.graph import Graph
    from src.flow_calculations.network import Network
except ImportError:
    from node import Node, NodeType
    from point import Point
    from graph import Graph
    from network import Network

class Flow:

    def __init__(self, network: Network, max_iterations: int = 10000, difference_cutoff: float = .000001):
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
                #print("max iterations exceeded")
                return False
            if abs(self.cost[-2] - self.cost[-1]) < self.difference_cutoff:
                #print(f"cuttoff diff: {self.cost[-2]}")
                return False
        return True

    def update_lists(self, bifurcation: Node):
        self.steps.append(bifurcation.point)
        self.cost.append(self.network.calculate_g(bifurcation.point.point_as_array()))
        self.theta.append(self.network.calculate_bifurcation_angle())
        #logging.warning(f"{self.steps[-1]}\t{self.cost[-1]}\t{self.theta[-1]}")
        
    def get_flow(self, verbose=False):
        i: int = 0
        graph: Graph = self.network.graph
        bifurcation = Node(0, graph.get_sink().point, NodeType.BIFURCATION)
        graph.add_node(bifurcation)
        self.update_lists(bifurcation)
        while self.should_repeat(i):
            graph.remove_node(bifurcation)
            #minimized = minimize(self.network.calculate_g, bifurcation.point.point_as_array(), method = 'Nelder-Mead', options={'disp': True})
            minimized = minimize(self.network.calculate_g, bifurcation.point.point_as_array(), method = 'Nelder-Mead')
            if verbose:
                logging.warning(minimized)
            bifurcation = Node(0, Point(minimized.x[0], minimized.x[1]), NodeType.BIFURCATION)
            graph.add_node(bifurcation)
            for source in graph.get_sources():
                graph.add_edge(source, bifurcation)
            graph.add_edge(bifurcation, graph.get_sink())
            self.network.graph = graph
            #print(graph)
            self.update_lists(bifurcation)
            i += 1
        return self.network

    def almostEqual(self, x, y, EPSILON=1e-5):
        return abs(x - y) < EPSILON

