import unittest
from node import Node
from point import Point
from network import Network

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