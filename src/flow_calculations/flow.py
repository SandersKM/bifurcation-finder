from src.flow_calculations.node import Node
from src.flow_calculations.point import Point
from src.flow_calculations.network import Network
from typing  import *
import math

# make a class to represent the network itself (nodes + bifurcation point?), then a class to analyze a flow

class Flow:

    def __init__(self, h: float, alpha: float, network: Network):
        self.h: float = h
        self.alpha: float = alpha
        self.network: Network = network
        self.oldBifurcationPoint: Point = network.getBifurcationPoints()[0]

    def getNetwork(self) -> Network:
        return self.network

    def updateNetwork(self, network: Network) -> None:
        self.network = network
        self.oldBifurcationPoint = network.getBifurcationPoints()[0]

    def calculateG(self, newBifurcationPoint: float) -> float: 
        M: float = (self.calculateIndividualCost(newBifurcationPoint) + self.calculateCarpoolCost(newBifurcationPoint))**2
        fill: float = self.calculateFill(newBifurcationPoint)
        return fill + M

    def calculateFill(self, x) -> float: 
        totalArea: float = 0
        for node in self.network.getSources():
            triangle: float = ((self.oldBifurcationPoint.getX() - x) * (node.getWeight() ** self.alpha) * node.getPoint().getY()) / 2
            totalArea += triangle
        return (totalArea ** 2) / self.h 

    def calculateIndividualCost(self, x) -> float: 
        total: float = 0
        sinkPointY = self.network.getSinkPoints()[0].getY()
        for point in self.network.getSourcePoints():
            total += ((x ** 2) + (point.getY() - sinkPointY)**2)**(1/2)
        return total 

    def calculateCarpoolCost(self, x) -> float: 
        edgeLength: float = ( self.network.getSinkPoints()[0].getX() - x )
        combinedWeight: float = 0
        for weight in self.network.getSourceWeights():
            combinedWeight += weight
        alphaAdjustedWeight: float = (combinedWeight ** self.alpha)
        return  alphaAdjustedWeight * edgeLength

    def calculateBifurcationAngle(self) -> float:
        sourcePoints = self.network.getSourcePoints()
        length_bif_s0 = sourcePoints[0].calculateDistance(self.oldBifurcationPoint)
        length_bif_s1 = sourcePoints[1].calculateDistance(self.oldBifurcationPoint)
        length_s0_s1 = sourcePoints[0].calculateDistance(sourcePoints[1])
        numerator = length_bif_s0**2 + length_bif_s1**2 - length_s0_s1**2
        denominator = 2 * length_bif_s0 * length_bif_s1
        cos_bif = numerator/denominator # Law of Cosines
        angle = math.acos(cos_bif)
        # return f"s0: {length_bif_s0}, s1:{length_bif_s1}, a:{length_s0_s1}, num:{numerator}, den:{denominator}, cos:{cos_bif}, ang:{math.degrees(angle)}"
        return math.degrees(angle)

    

