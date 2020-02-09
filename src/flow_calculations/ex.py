from typing import *
from scipy.optimize import minimize
import math
import numpy as np
import logging
try:
    from src.flow_calculations.node import Node, NodeType
    from src.flow_calculations.point import Point
    from src.flow_calculations.graph import Graph
    from src.flow_calculations.subgraph import Subgraph
    from src.flow_calculations.flow import Flow
    from src.flow_calculations.parameters import Parameters
except ImportError:
    from node import Node, NodeType
    from point import Point
    from graph import Graph
    from subgraph import Subgraph
    from flow import Flow
    from parameters import Parameters

def get_subgraph():
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
    params = Parameters(.2, 0.5)
    subgraph = Subgraph(params, graph)   
    subgraph.calculate_g(np.array([3.840210415833968, 3.000012521887091]))  
    return subgraph   

def make_steps():
    flow = Flow(get_subgraph())
    print(flow.subgraph.calculate_optimal_angle())
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