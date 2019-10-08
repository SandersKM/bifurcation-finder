import { create, all } from 'mathjs'
import { parseExpression } from '@babel/parser'
//import { newtonRaphson } from 'root-finding'



export const calculateG = () => {
  let h = 0.1
  let x = 1.0
  let x0 = 1.1
  let alpha = 0.5
  let sourceWeight = [1, 1]
  let sourceY = [1, 1]
  let sinkX = 2
  let M = calculateTotalCosts(sourceY, x)
  let carpoolCost = calculateCarpoolCost(sourceWeight, alpha, sinkX, x);
  M = Math.pow(M + carpoolCost, 2)
  let fill = calculateFill(sourceWeight, alpha, sourceY, x0, x, h);
  //console.log(math.chain().derivative('x^2 + x', 'x'))
  rootG()
  return fill + M;
}

export const rootG = () => {
  const config = { }
  const math = create(all, config)
  let scope = {
    h: 0.1,
    alpha: 0.5,
    x0: 1.1,
    sourceWeight: [1, 1],
    sourceY: [1, 1],
    sinkX: 2
  }
  // calculate carpool cost
  let edgeLength = '(' + scope.sinkX.toString() + ' - x)'
  let combinedWeight = 0
  math.forEach(scope.sourceWeight, function(weight) {
    combinedWeight = combinedWeight + weight
  })
  let carpoolCost = (combinedWeight ** scope.alpha).toString() + "*" + edgeLength
  // calculate individual cost
  let totalIndCost = ""
  math.forEach(scope.sourceY, function(value) {
    totalIndCost = totalIndCost + "sqrt(" + value + " + x^2) + "
  })
  let M = '(' + totalIndCost + carpoolCost +')^2'


  // calculate fill
  let totalArea = ""
  math.forEach(math.range(0, scope.sourceWeight.length), function(i) {
    let triangle = "(((" + scope.x0 + " - x) *  " + ( ( ( scope.sourceWeight[i] ) ** scope.alpha ) * scope.sourceY[i]).toString() + ") / 2) "
    if (i !== 0) {
      triangle = " + " + triangle
    }
    totalArea = totalArea + triangle
  })
  let fill = "((( " + totalArea + ")^2) / " + scope.h.toString() + ")"
  let G = fill + " + " + M
  console.log(G) 
  console.log(math.derivative(G, "x").toString()) 
  
  scope.x = 1.0
  console.log(math.evaluate(G, scope))

}

function calculateFill(sourceWeight, alpha, sourceY, x0, x, h) {
  let totalArea = 0;
  for (let i = 0; i < sourceWeight.length; i++ ) {
    let triangle = ((x0 - x) * Math.pow(sourceWeight[i], alpha) * sourceY[i]) / 2;
    totalArea = totalArea + triangle;
  }
  return Math.pow(totalArea, 2) / h ;
}

function calculateTotalCosts(sourceY, x) {
  let total = 0
  for (let i = 0; i < sourceY.length; i++ ) {
    total = total + Math.sqrt(Math.pow(x, 2) + sourceY[i])
  }
  return total 
}

function calculateCarpoolCost(sourceWeight, alpha, sinkX, x) {
  let edgeLength = ( sinkX - x )
  let combinedWeight = sourceWeight.reduce(add)
  let alphaAdjustedWeight = Math.pow(combinedWeight, alpha)
  return  alphaAdjustedWeight * edgeLength
}

const add = (a, b) => a + b;
