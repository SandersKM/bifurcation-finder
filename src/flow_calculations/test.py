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


h: float = 0.1
x0: float = 4
alpha: float = 0.5
sourceWeight = [1, 1]
sourceY = [1, 5]
sinkX: float = 4


network = Network()
network.addSource(Node(1,Point(0,5)))
network.addSource(Node(1,Point(0,1)))

network.addSink(Node(2, Point(4,3)))

network.addBifurcation(Point(4,3))

flow = Flow(h, alpha, network)
i = 0
minimized = minimize_scalar(flow.calculateG).x
print(f"minimized {i}: {minimized} \t {flow.calculateG(minimized)}\n")
while i < 1000:
    network.popBifurcation()
    network.addBifurcation(Point(minimized, 3))
    flow = Flow(h, alpha,network)
    i += 1
    minimized = minimize_scalar(flow.calculateG).x
    if (i % 1 == 0):
        print(f"minimized {i}: {minimized} \t {flow.calculateG(minimized)}")