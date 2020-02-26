from sympy import *
from sympy.geometry import *

c1 = Circle(Point(5, 5), 1.11857)
c2 = Circle(Point(7, 5), 1.11857)
print(c1.intersection(c2))
