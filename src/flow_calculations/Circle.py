"""
Created on Sat Apr 8th 2017
retrieved on Fri Feb 21st 2020
from http://paulbourke.net/geometry/circlesphere/circle_intersection.py

Circle Intersection

@PythonVer: Tested in 2.7.10 and 3.6
@Author: Matt Woodhead

A note on angle convention:

                           +y

                           |    /
                           |   /
                           |  /   +ve Theta
                           | / )
±180 degrees    -x ----------------- +ve x    0 degrees
                           | \ )
                           |  \   -ve Theta
                           |   \
                           |    \

                          -y

The outputs are ordered from the angle of the lines drawn from the intersection
points to the centre of the first circle, from +180 degrees to -180 degrees.

"""
import math
try:
    from src.flow_calculations.point import Point
except ImportError:
    from point import Point

PRECISION = 5  # Decimal point precision


class Circle(object):
    """ An OOP implementation of a circle as an object """

    def __init__(self, xposition, yposition, radius):
        self.xpos = xposition
        self.ypos = yposition
        self.radius = radius

    def circle_intersect(self, circle2):
        """
        Intersection points of two circles using the construction of triangles
        as proposed by Paul Bourke, 1997.
        http://paulbourke.net/geometry/circlesphere/
        """
        X1, Y1 = self.xpos, self.ypos
        X2, Y2 = circle2.xpos, circle2.ypos
        R1, R2 = self.radius, circle2.radius

        Dx = X2-X1
        Dy = Y2-Y1
        D = round(math.sqrt(Dx**2 + Dy**2), PRECISION)
        # Distance between circle centres
        if D > R1 + R2:
            return "The circles do not intersect"
        elif D < math.fabs(R2 - R1):
            return "No Intersect - One circle is contained within the other"
        elif D == 0 and R1 == R2:
            return "No Intersect - The circles are equal and coincident"
        else:
            if D == R1 + R2 or D == R1 - R2:
                CASE = "The circles intersect at a single point"
            else:
                CASE = "The circles intersect at two points"
            chorddistance = (R1**2 - R2**2 + D**2)/(2*D)
            # distance from 1st circle's centre to the chord between intersects
            halfchordlength = math.sqrt(R1**2 - chorddistance**2)
            chordmidpointx = X1 + (chorddistance*Dx)/D
            chordmidpointy = Y1 + (chorddistance*Dy)/D
            I1 = Point(round(chordmidpointx + (halfchordlength*Dy)/D, PRECISION),
                  round(chordmidpointy - (halfchordlength*Dx)/D, PRECISION))
            theta1 = round(math.degrees(math.atan2(I1.y-Y1, I1.x-X1)),
                           PRECISION)
            I2 = Point(round(chordmidpointx - (halfchordlength*Dy)/D, PRECISION),
                  round(chordmidpointy + (halfchordlength*Dx)/D, PRECISION))
            theta2 = round(math.degrees(math.atan2(I2.y-Y1, I2.x-X1)),
                           PRECISION)
            if theta2 > theta1:
                I1, I2 = I2, I1
            return (I1, I2, CASE)

# Main program:
#C1 = Circle(0, 0, 10)
#C2 = Circle(10, 0, 10)

#print(C1.circle_intersect(C2))
