from scipy.optimize import minimize_scalar
import numpy as np
import typing
import math

# this needs to be a class

class Flow:

    def __init__(self, h: float, alpha: float, x0: float, sourceWeight: float, sourceY: float, sinkX: float):
        self.h: float = h
        self.alpha: float = alpha
        self.x0: float = x0
        self.sourceWeight: float = sourceWeight
        self.sourceY: float = sourceY
        self.sinkX: float = sinkX

    def calculateG(self, x: float) -> float: 
        M: float = (self.calculateTotalCosts(x) + self.calculateCarpoolCost(x))**2
        fill: float = self.calculateFill(x)
        return fill + M

    def calculateFill(self, x) -> float: 
        totalArea: float = 0
        for i in range(len(self.sourceWeight)):
            triangle: float = ((self.x0 - x) * (self.sourceWeight[i] ** self.alpha) * self.sourceY[i]) / 2
            totalArea += triangle
        return (totalArea ** 2) / h 

    def calculateTotalCosts(self, x) -> float: 
        total: float = 0
        for i in range(len(self.sourceY)):
            total += ((x ** 2) + self.sourceY[i])**(1/2)
        return total 

    def calculateCarpoolCost(self, x) -> float: 
        edgeLength: float = ( self.sinkX - x )
        combinedWeight: float = 0
        for weight in self.sourceWeight:
            combinedWeight += weight
        alphaAdjustedWeight: float = (combinedWeight ** self.alpha)
        return  alphaAdjustedWeight * edgeLength


h: float = 0.1
x0: float = 1.1
alpha: float = 0.5
sourceWeight = [1, 1]
sourceY = [1, 1]
sinkX: float = 2

flow = Flow(h, alpha, x0, sourceWeight, sourceY, sinkX)
x = flow.calculateG(1.0779255502301148)
print(x)
y = minimize_scalar(flow.calculateG)
print(y.x)