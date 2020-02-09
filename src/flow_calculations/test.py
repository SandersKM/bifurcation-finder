import unittest
from typing import *
import math
import logging
try:
    from src.flow_calculations.node import Node, NodeType
    from src.flow_calculations.point import Point
    from src.flow_calculations.graph import Graph
    from src.flow_calculations.subgraph import Subgraph
    from src.flow_calculations.subgraph import Flow
except ImportError:
    from node import Node, NodeType
    from point import Point
    from graph import Graph
    from subgraph import Subgraph
    from flow import Flow

class UnitTest(unittest.TestCase):

    def test_point(self):
        x = 4.4
        y = 5.5
        point = Point(x, y)
        self.assertEqual(point.x, x)
        self.assertEqual(point.y, y)

    def test_point_distance(self):
        point1 = Point(2, -3)
        point2 = Point(5, 1)
        self.assertEqual(point1.get_distance_to(point2), 5)

    def test_node(self):
        weight = 5
        point1 = Point(2, -3)
        node_type = NodeType.SOURCE
        node1 = Node(weight, point1, node_type)
        self.assertEqual(node1.weight, weight)
        self.assertEqual(node1.point, point1)
        self.assertEqual(node1.node_type, NodeType.SOURCE)

    def test_node_distance(self):
        point1 = Point(2, -3)
        point2 = Point(5, 1)
        node1 = Node(1, point1, NodeType.SOURCE)
        node2 = Node(1, point2, NodeType.SOURCE)
        self.assertEqual(node1.get_distance_to(node2), 5)

    def test_subgraph(self):
        graph = Graph()
        graph.add_source(Node(1,Point(5,1), NodeType.SOURCE))
        graph.add_source(Node(1,Point(1,3), NodeType.SOURCE))
        graph.add_sink(Node(2, Point(0,0), NodeType.SINK))
        graph.add_bifurcation(Point(0, 0)) 
        subgraph = Subgraph(0.1, 0.5, graph)     
        self.assertEqual(subgraph.alpha, 0.5)
        self.assertEqual(subgraph.h, 0.1)
        self.assertEqual(len(subgraph.graph.sinks), 1)
        self.assertEqual(len(subgraph.graph.sources), 2)
        self.assertEqual(len(subgraph.graph.bifurcations), 1)
        self.assertEqual(subgraph.calculate_optimal_angle(), 90)
        subgraph_2 = Subgraph(0.000001, 0.45, graph) 
        self.assertEqual(subgraph_2.calculate_optimal_angle(), 93.83980058897298)  

    def test_flow_a(self):
        graph = Graph()
        graph.add_source(Node(1,Point(5,1), NodeType.SOURCE))
        graph.add_source(Node(1,Point(1,3), NodeType.SOURCE))
        graph.add_sink(Node(2, Point(0,0), NodeType.SINK))
        graph.add_bifurcation(Point(0, 0)) 
        subgraph = Subgraph(0.000001, 0.5, graph)
        flow = Flow(subgraph)
        flow.get_flow()
        steps = flow.steps
        theta = flow.theta
        cost = flow.cost
        self.assertLessEqual(len(steps), flow.max_iterations)
        self.assertGreaterEqual(theta[-1], 90 - 0.2)
        self.assertLessEqual(cost[-1], cost[-2] + flow.difference_cutoff)

if __name__ == '__main__':
    unittest.main()


