import unittest
from typing import *
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

class MyTest(unittest.TestCase):

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
        node1 = Node(weight, point1)
        self.assertEqual(node1.weight, weight)
        self.assertEqual(node1.point, point1)

    def test_node_distance(self):
        point1 = Point(2, -3)
        point2 = Point(5, 1)
        node1 = Node(1, point1)
        node2 = Node(1, point2)
        self.assertEqual(node1.get_distance_to(node2), 5)


if __name__ == '__main__':
    unittest.main()


