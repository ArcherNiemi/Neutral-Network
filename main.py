import random
import dataPoints
from dataPoints import readDataSet

input_size: int = 2
hidden_layer_size: int = 3
number_of_hidden_layers: int = 1
output_size: int = 1

dataFile1: str = 'poisonous.csv'
dataFile2: str = 'poisonous.csv2'

weights: list = []
biases: list = []
nodesIn: int
nodesOut: int
currentNode: int = -1
previous_nodes: list = []
data_set: list = []
accuracy: float = 0.5
one: int = 0
two: int = 0
og: bool
costGradientW = []
costGradientB = []
learnRate = 0.2

def run():
    setUp()
    for i in range(200):
        learn(data_set)
        if(i % 5 == 0):
            accuracyTemp = accuracy
            print("Accuracy:", accuracyTemp)
            print(totalCost(data_set))
    print(one)
    print(two)

def setUp():
    global  data_set
    makeRandomWeightsAndBiases()
    data_set = readDataSet(dataFile1)



def setUpPreviousNodes(dataPoint):
    global previous_nodes
    previous_nodes.clear
    for i in range(hidden_layer_size):
        previous_nodes.append(0)
    for i in range(input_size):
        previous_nodes[i] = dataPoint[i]

def makeRandomWeightsAndBiases():
    global weights
    global biases
    global costGradientB
    global costGradientW
    numberOfWeights = input_size * hidden_layer_size + (hidden_layer_size * hidden_layer_size) * (number_of_hidden_layers - 1) + (hidden_layer_size * output_size)
    numberOfBiases = hidden_layer_size * number_of_hidden_layers + output_size
    for i in range(numberOfWeights):
        weights.append(random.uniform(0,1))
    for i in range(numberOfBiases):
        biases.append(random.uniform(0,1))
    for i in range(len(weights)):
        costGradientW.append(0)
    for i in range(len(biases)):
        costGradientB.append(0)

def learn(data):
    global og
    og = True
    ogCost = totalCost(data)
    og = False
    h = 0.001
    for i in range(len(weights)):
        weights[i] += h
        deltaCost = totalCost(data) - ogCost
        weights[i] -= h
        costGradientW[i] = deltaCost / h
    for i in range(len(biases)):
        biases[i] += h
        deltaCost = totalCost(data) - ogCost
        biases[1] -= h
        costGradientB[i] = deltaCost / h
    apply()



def apply():
    for i in range(len(weights)):
        weights[i] -= costGradientW[i] * learnRate
    for i in range(len(biases)):
        biases[i] -= costGradientB[i] * learnRate

def nodeCost(output, expectedOutput):
    error = output - expectedOutput
    return error * error

def cost(dataPoint):
    global accuracy
    outputs = calculateOutputs(dataPoint)
    cost = 0
    for i in range(output_size):
        cost += nodeCost(outputs[i], dataPoint[2])
        if(og):
            findAccuracy(outputs[i], dataPoint[2])
    return cost

def totalCost(data):
    global accuracy
    totalCost = 0
    currentDataPoint: list = [0,0,0]
    if(og):
        accuracy = 0
    for i in range(int(len(data))):
        currentDataPoint[0] = data[i].spikes
        currentDataPoint[1] = data[i].spots
        currentDataPoint[2] = data[i].poisonous
        totalCost += cost(currentDataPoint)
    return totalCost / len(data)

def findAccuracy(output, expectedOutput):
    global accuracy
    roundedOutput = round(output)
    if(roundedOutput == expectedOutput):
        accuracy += 1



def calculateOutputs(dataPoint):
    global nodesIn
    global nodesOut
    global currentNode
    setUpPreviousNodes(dataPoint)
    currentNode = -1
    nodesIn = input_size
    nodesOut = hidden_layer_size
    calculateColumn()
    nodesIn = hidden_layer_size
    for i in range(number_of_hidden_layers - 1):
        calculateColumn()
    nodesOut = output_size
    calculateColumn()
    outputs: list = []
    for i in range(output_size):
        outputs.append(previous_nodes[i])
        if(outputs[i] > 1):
            outputs[i] = 1
    return outputs

def calculateColumn():
    global currentNode
    for i in range(nodesOut):
        previous_nodes[i] = calculateNode()
        currentNode += 1
 
def calculateNode():
    newNode = 0
    for i in range(nodesIn):
        newNode += previous_nodes[i] * weights[currentNode + i * nodesOut]
    newNode + biases[currentNode]
    return newNode

run()