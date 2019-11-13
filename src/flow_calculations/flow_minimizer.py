from typing import *
from node import Node
from point import Point
from network import Network
from flow import Flow
from scipy.optimize import minimize_scalar


class FlowMinimizer:

    def get_minimum_flow(self, fl: Flow, max_iterations: int = 10000, difference_cuttoff: float = .0000001):
        i: int = 0
        flow_diff: float = 1
        minimized = minimize_scalar(fl.calculateG).x
        new_value = fl.calculateG(minimized)
        s1 = fl.network.getSources()[0]
        s2 = fl.network.getSources()[1]
        start = fl.network.getSourcePoints()[0]
        bifurcation = fl.network.getBifurcationPoints()[0]
        s1.getThetaSelf(start, b)
        print(f"new value = {new_value} \t minimized = {minimized} \t {s1.getThetaSelf(start, b) + s1.getThetaSelf(start, b)}")
        net: Network = fl.getNetwork()
        while i < max_iterations and abs(flow_diff) > difference_cuttoff:
            b = net.popBifurcation()
            bifurcation = Point(minimized, b.getY())
            net.addBifurcation(bifurcation)
            fl.updateNetwork(net)
            i += 1
            minimized = minimize_scalar(fl.calculateG).x
            old_value: float = new_value
            new_value = fl.calculateG(minimized)
            flow_diff = new_value - old_value
            print(f"new value = {new_value} \t minimized = {minimized} \t {s1.getThetaSelf(start, b) + s1.getThetaSelf(start, b)}")
        return fl

    def get_flow_steps(self, fl: Flow, max_iterations: int = 10000, difference_cuttoff: float = .0000001):
        i: int = 0
        flow_diff: float = 1
        minimized = minimize_scalar(fl.calculateG).x
        new_value = fl.calculateG(minimized)
        flow_steps = [fl.oldBifurcationPoint.getX(), minimized]
        net: Network = fl.getNetwork()
        while i < max_iterations and abs(flow_diff) > difference_cuttoff:
            net.popBifurcation()
            net.addBifurcation(Point(minimized, 3))
            fl.updateNetwork(net)
            i += 1
            minimized = minimize_scalar(fl.calculateG).x
            flow_steps.append(minimized)
            old_value: float = new_value
            new_value = fl.calculateG(minimized)
            flow_diff = new_value - old_value
        return flow_steps

