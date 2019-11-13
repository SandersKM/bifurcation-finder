from typing import *
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
        s1 = self.fl.network.getSources()[0]
        s2 = self.fl.network.getSources()[1]
        start = self.fl.network.getSourcePoints()[0]
        bifurcation = self.fl.network.getBifurcationPoints()[0]
        self.theta = [s1.getThetaSelf(start, bifurcation) + s1.getThetaSelf(start, bifurcation)]
        self.steps = [self.fl.oldBifurcationPoint.getX(), minimized]
        self.cost = [new_value]
        net: Network = fl.getNetwork()
        while i < self.max_iterations and abs(flow_diff) > self.difference_cuttoff:
            b = net.popBifurcation()
            bifurcation = Point(minimized, b.getY())
            net.addBifurcation(bifurcation)
            self.fl.updateNetwork(net)
            i += 1
            minimized = minimize_scalar(fl.calculateG).x
            self.steps.append(minimized)
            old_value: float = new_value
            new_value = self.fl.calculateG(minimized)
            flow_diff = new_value - old_value
            self.cost.append(new_value)
            self.theta.append(s1.getThetaSelf(start, bifurcation) + s1.getThetaSelf(start, bifurcation))
        return self.fl


