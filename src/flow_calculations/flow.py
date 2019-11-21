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

    def __init__(self, fl: Network, max_iterations: int = 10000, difference_cuttoff: float = .0000001):
        self.fl: Network = fl
        self.max_iterations = max_iterations
        self.difference_cuttoff = difference_cuttoff
        self.steps = []
        self.cost = []
        self.theta = []

    def should_repeat(self, i: int, flow_diff: float):
        if i > self.max_iterations:
            return False
        #if abs(flow_diff) < self.difference_cuttoff:
        #    return False
        if self.theta[-1] > 90 - self.difference_cuttoff:
            return False
        return True
        
    def get_flow(self):
        i: int = 0
        flow_diff: float = 1
        minimized = minimize_scalar(self.fl.calculateG).x
        new_value = self.fl.calculateG(minimized)
        self.theta = [self.fl.calculateBifurcationAngle()]
        self.steps = [self.fl.oldBifurcationPoint.getX(), minimized]
        self.cost = [new_value]
        node_collection: Nodes = self.fl.getNodes()
        while self.should_repeat(i, flow_diff):
            b = node_collection.popBifurcation()
            bifurcation = Point(minimized, b.getY())
            node_collection.addBifurcation(bifurcation)
            self.fl.updateNodes(node_collection)
            i += 1
            minimized = minimize_scalar(self.fl.calculateG).x
            flow_diff = minimized - self.steps[-1]
            self.steps.append(minimized)
            self.cost.append(self.fl.calculateG(minimized))
            self.theta.append(self.fl.calculateBifurcationAngle())
        return self.fl


