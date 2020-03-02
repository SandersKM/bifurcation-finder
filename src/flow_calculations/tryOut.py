from sympy import *
from sympy.geometry import *

c1 = Circle(Point(5, 5), 1.11857)
c2 = Circle(Point(7, 5), 1.11857)
c3 = Circle(Point(2.874, 3.871), 3.088)
c4 = Circle(Point(6, 4.5), 1.119)
endpoint = Point(3, 2)
#print(c1.intersection(c2)[0])
#print(Polygon(Point(5, 5), Point(0, 5), Point(3, 2)).intersection(Point(1,4)))
#print(c1.intersection(Line(Point(5, 5), Point(3, 2))))
print(c4.encloses_point(endpoint))