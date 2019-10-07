import { create, all } from 'mathjs'
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
  const parser = math.parser()
  parser.set('h', 0.1)
  parser.set('x', 1.0)
  parser.set('alpha', 0.5)
  parser.set('x0', 1.1)
  parser.set('sourceWeight', [1, 1])
  parser.set('sourceY', [1, 1])
  parser.set('sinkX', 2)
  // calculate carpool cost
  parser.evaluate('edgeLength = sinkX - x')
  parser.set('combinedWeight', 0)
  math.forEach(parser.get('sourceWeight'), function(value) {
    parser.set('value', value)
    parser.evaluate("combinedWeight = combinedWeight + value")
  })
  parser.evaluate('alphaAdjustedWeight = combinedWeight^alpha')
  parser.evaluate('carpoolCost = alphaAdjustedWeight * edgeLength')
  // calculate individual cost
  parser.set("totalIndCost", 0)
  math.forEach(parser.get('sourceY'), function(value) {
    parser.set('value', value)
    parser.evaluate("totalIndCost = totalIndCost + sqrt(value + x^2)")
  })
  parser.evaluate('M = (totalIndCost + carpoolCost)^2')
  // calculate fill
  parser.set('totalArea', 0)
  math.forEach(math.range(1, parser.get('sourceWeight').length + 1), function(i) {
    parser.set('i', i)
    parser.evaluate("triangle = ((x0 - x) * ((sourceWeight[i])^alpha) * sourceY[i]) / 2")
    parser.evaluate('totalArea = totalArea + triangle')
  })
  parser.evaluate('fill = (totalArea^2)/h')
  parser.evaluate('G = fill + M')
  console.log(parser.get("G"))
  //return parser.get("sourceY")
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
