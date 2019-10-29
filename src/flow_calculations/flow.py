from scipy.optimize import minimize_scalar
from node import Node
from point import Point
import numpy as np
import typing
from typing  import List
import math

# make a class to represent the network itself (nodes + bifurcation point?), then a class to analyze a flow

class Flow:

    def __init__(self, h: float, alpha: float, sourceNodeList: List[Node], sinkNode: Node, oldBifurcationPoint: Point):
        self.h: float = h
        self.alpha: float = alpha
        self.sinkNode: Node = sinkNode
        self.sourceNodeList: List[Node] = sourceNodeList
        self.oldBifurcationPoint: Point = oldBifurcationPoint

    def calculateG(self, newBifurcationPoint: float) -> float: 
        M: float = (self.calculateIndividualCost(newBifurcationPoint) + self.calculateCarpoolCost(newBifurcationPoint))**2
        fill: float = self.calculateFill(newBifurcationPoint)
        #print(f"{self.calculateIndividualCost(newBifurcationPoint)} , {self.calculateCarpoolCost(newBifurcationPoint)}")
        #print(f"{newBifurcationPoint} : {M} + {fill}")
        return fill + M

    def calculateFill(self, x) -> float: 
        totalArea: float = 0
        for node in self.sourceNodeList:
            triangle: float = ((self.oldBifurcationPoint.getX() - x) * (node.getWeight() ** self.alpha) * node.getPoint().getY()) / 2
            totalArea += triangle
        return (totalArea ** 2) / self.h 

    def calculateIndividualCost(self, x) -> float: 
        total: float = 0
        for node in self.sourceNodeList:
            total += ((x ** 2) + (node.getPoint().getY() - self.sinkNode.getPoint().getY())**2)**(1/2)
        return total 

    def calculateCarpoolCost(self, x) -> float: 
        edgeLength: float = ( self.sinkNode.getPoint().getX() - x )
        combinedWeight: float = 0
        for node in self.sourceNodeList:
            combinedWeight += node.getWeight()
        alphaAdjustedWeight: float = (combinedWeight ** self.alpha)
        return  alphaAdjustedWeight * edgeLength
    



h: float = 0.1
x0: float = 4
alpha: float = 0.5
sourceWeight = [1, 1]
sourceY = [1, 5]
sinkX: float = 4

sourceNodeList=[]
sourceNodeList.append(Node(1,Point(0,5)))
sourceNodeList.append(Node(1,Point(0,1)))

sinkNode=Node(2, Point(4,3))

flow = Flow(h, alpha, sourceNodeList, sinkNode, sinkNode.getPoint())
i = 0
minimized = minimize_scalar(flow.calculateG).x
print(f"minimized {i}: {minimized} \t {flow.calculateG(minimized)}\n")
while i < 1:
    flow = Flow(h, alpha, sourceNodeList, sinkNode, Point(minimized, 0))
    i += 1
    minimized = minimize_scalar(flow.calculateG).x
    if (i % 1 == 0):
        print(f"minimized {i}: {minimized} \t {flow.calculateG(minimized)} \t {sourceNodeList[0].getThetaSelf(sinkNode.getPoint(), Point(minimized, 2)) + sourceNodeList[1].getThetaSelf(sinkNode.getPoint(), Point(minimized, 2))}\n")


t1 = sourceNodeList[0].getThetaSelf(sinkNode.getPoint(), Point(minimized, 2))
st1 = sourceNodeList[0].thetaSelfShouldEqual(sourceNodeList[1], alpha)
print(f"{t1}  =? {st1}")
t2 = sourceNodeList[1].getThetaSelf(sinkNode.getPoint(), Point(minimized, 2))
st2 = sourceNodeList[1].thetaSelfShouldEqual(sourceNodeList[0], alpha)
print(f"{t2}  =? {st2}")
st3 = sourceNodeList[1].thetaAddedShouldEqual(sourceNodeList[1], alpha)
print(f"{t1  + t2} =? {st3}")
