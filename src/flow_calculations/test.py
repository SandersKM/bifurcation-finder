import unittest
from src.flow_calculations.node import Node
from src.flow_calculations.point import Point
from src.flow_calculations.network import Network
from src.flow_calculations.flow import Flow
from scipy.optimize import minimize_scalar

class MyTest(unittest.TestCase):

    def testPoint(self):
        x = 4.4
        y = 5.5
        point = Point(x, y)
        self.assertEqual(point.getX(), x)
        self.assertEqual(point.getY(), y)

    def testPointDistance(self):
        point1 = Point(2, -3)
        point2 = Point(5, 1)
        self.assertEqual(point1.calculateDistance(point2), 5)


if __name__ == '__main__':
    unittest.main()


