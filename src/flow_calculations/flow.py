from scipy.optimize import minimize_scalar
from node import Node
from point import Point
from network import Network
import numpy as np
import typing
from typing  import List
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
    

