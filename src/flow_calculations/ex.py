from typing import *
from scipy.optimize import minimize
import math
import numpy as np
import logging
try:
    from src.flow_calculations.node import Node, NodeType
    from src.flow_calculations.point import Point
    from src.flow_calculations.graph import Graph
    from src.flow_calculations.network import Network
    from src.flow_calculations.network import Flow
except ImportError:
    from node import Node, NodeType
    from point import Point
    from graph import Graph
    from network import Network
    from flow import Flow

def get_network():
    graph = Graph()
    source1 = Node(1,Point(0,1), NodeType.SOURCE)
    source2 = Node(1,Point(0,5), NodeType.SOURCE)
    sink = Node(2, Point(4,3), NodeType.SINK)
    bifurcation = Node(0, Point(4,3), NodeType.BIFURCATION) 
    graph.add_node(source1)
    graph.add_node(source2)
    graph.add_node(sink)
    graph.add_node(bifurcation) 
    graph.add_edge(source1, bifurcation)
    graph.add_edge(source2, bifurcation)
    graph.add_edge(bifurcation, sink)
    network = Network(.2, 0.5, graph)   
    network.calculate_g(np.array([3.840210415833968, 3.000012521887091]))  
    return network   

def make_steps():
    flow = Flow(get_network())
    print(flow.network.calculate_optimal_angle())
    flow.get_flow()
    steps = flow.steps
    theta = flow.theta
    cost = flow.cost
    print(steps[-1])
    print(theta[-1])
    print(cost[-1])

def test():
    make_steps()

test()