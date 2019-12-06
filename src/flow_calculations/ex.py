from typing import *
from scipy.optimize import minimize
import math
import logging
try:
    from src.flow_calculations.node import Node
    from src.flow_calculations.point import Point
    from src.flow_calculations.vertices import Vertices
    from src.flow_calculations.network import Network
    from src.flow_calculations.network import Flow
except ImportError:
    from node import Node
    from point import Point
    from vertices import Vertices
    from network import Network
    from flow import Flow

def get_network():
    vertices = Vertices()
    vertices.add_source(Node(1,Point(5,1)))
    vertices.add_source(Node(1,Point(1,3)))
    vertices.add_sink(Node(2, Point(0,0)))
    vertices.add_bifurcation(Point(0, 0)) 
    return Network(0.1, 0.45, vertices)        

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