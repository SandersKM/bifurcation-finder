from typing import *
from node import Node
from point import Point
from network import Network
from flow import Flow
from scipy.optimize import minimize_scalar


class FlowMinimizer:

    def minimize_flow(self, fl: Flow):
        i: int = 0
        flow_diff: float = 1
        minimized = minimize_scalar(fl.calculateG).x
        new_value = fl.calculateG(minimized)
        while i < 1000 and abs(flow_diff) > .0000001:
            network.popBifurcation()
            network.addBifurcation(Point(minimized, 3))
            fl = Flow(h, alpha,network)
            i += 1
            minimized = minimize_scalar(fl.calculateG).x
            old_value: float = new_value
            new_value = fl.calculateG(minimized)
            flow_diff = new_value - old_value
        return flow




h: float = 0.1
alpha: float = 0.5
network = Network()
network.addSource(Node(1,Point(0,5)))
network.addSource(Node(1,Point(0,1)))
network.addSink(Node(2, Point(4,3)))
network.addBifurcation(Point(4,3))
flow = Flow(h, alpha, network)

m = FlowMinimizer().minimize_flow(flow)
print(m.network.getBifurcationPoints()[0].getX())
