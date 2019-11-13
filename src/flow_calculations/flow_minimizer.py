from typing import *
import math
from node import Node
from point import Point
from network import Network
from flow import Flow
from scipy.optimize import minimize_scalar


class FlowMinimizer:

    def __init__(self, fl: Flow, max_iterations: int = 10000, difference_cuttoff: float = .0000001):
        self.fl: Flow = fl
        self.max_iterations = max_iterations
        self.difference_cuttoff = difference_cuttoff
        self.steps = []
        self.cost = []
        self.theta = []
    

    def get_minimum_flow(self):
        i: int = 0
        flow_diff: float = 1
        minimized = minimize_scalar(self.fl.calculateG).x
        new_value = self.fl.calculateG(minimized)
        self.theta = [self.fl.calculateBifurcationAngle()]
        self.steps = [self.fl.oldBifurcationPoint.getX(), minimized]
        self.cost = [new_value]
        net: Network = self.fl.getNetwork()
        while i < self.max_iterations and (abs(flow_diff) > self.difference_cuttoff or abs(self.theta[-1] - 90) > 0.1):
            b = net.popBifurcation()
            bifurcation = Point(minimized, b.getY())
            net.addBifurcation(bifurcation)
            self.fl.updateNetwork(net)
            i += 1
            minimized = minimize_scalar(self.fl.calculateG).x
            flow_diff = minimized - self.steps[-1]
            self.steps.append(minimized)
            self.cost.append(self.fl.calculateG(minimized))
            self.theta.append(self.fl.calculateBifurcationAngle())
        return self.fl


