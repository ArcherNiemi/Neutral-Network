import math
import random
from dataPoints import dataPoint
from dataPoints import readDataSet
from dataPoints import readFRCDataSet
import pandas as pd
import pickle
from datetime import datetime

class Layer:
    def __init__(self, numNodesIn, numNodesOut):
        self.numNodesIn = numNodesIn
        self.numNodesOut = numNodesOut

        self.weights = [[0 for _ in range(numNodesOut)] for _ in range(numNodesIn)]
        self.baises = [0] * numNodesOut
        self.costGradiantW = [[0 for _ in range(numNodesOut)] for _ in range(numNodesIn)]
        self.costGradiantB = [0] * numNodesOut

        self.activations = [0] * self.numNodesOut
        self.weightedInputs = [0] * self.numNodesOut
        self.inputs = [0] * self.numNodesIn

        self.initializeRandomWeights()

    def calculateOutputs(self, inputs):
        self.inputs = inputs
        for nodeOut in range(self.numNodesOut):
            weightedInput = self.baises[nodeOut]
            for nodeIn in range(self.numNodesIn):
                weightedInput += self.weights[nodeIn][nodeOut] * inputs[nodeIn]
            self.weightedInputs[nodeOut] = weightedInput
            self.activations[nodeOut] = self.activationFunction(weightedInput)
        return self.activations
    
    def activationFunction(self, weightedInput):
        return 1 / (1 + math.exp(-weightedInput))

    def nodeCost(self, outputActivation, expectedOutput):
        error = outputActivation - expectedOutput
        return error * error
    
    def applyGradiants(self, learnRate):
        for nodeOut in range(self.numNodesOut):
            self.baises[nodeOut] -= self.costGradiantB[nodeOut] * learnRate
            for nodeIn in range(self.numNodesIn):
                self.weights[nodeIn][nodeOut] -= self.costGradiantW[nodeIn][nodeOut] * learnRate

    def initializeRandomWeights(self):
        for nodeIn in range(self.numNodesIn):
            for nodeOut in range(self.numNodesOut):
                randomValue = random.uniform(-1, 1)
                self.weights[nodeIn][nodeOut] = randomValue / math.sqrt(self.numNodesIn)

    def calculateOutputLayerNodeValues(self, expectedOutputs):
        nodeValues = [0] * len(expectedOutputs)

        for i in range(len(expectedOutputs)):
            costDerivative = self.nodeCostDerivative(self.activations[i], expectedOutputs[i])
            activationDerivative = self.activationDerivative(self.weightedInputs[i])
            nodeValues[i] = activationDerivative * costDerivative

        return nodeValues

    def nodeCostDerivative(self, outputActivation, expectedOutput):
        return 2 * (outputActivation - expectedOutput)

    def activationDerivative(self, weightedInput):
        activation = self.activationFunction(weightedInput)
        return activation * (1 - activation)
    
    def updateGradiants(self, nodeValues):
        for nodeOut in range(self.numNodesOut):
            for nodeIn in range(self.numNodesIn):
                deritativeCostWrtWeight = self.inputs[nodeIn] * nodeValues[nodeOut]
                self.costGradiantW[nodeIn][nodeOut] += deritativeCostWrtWeight
            deritativeCostWrtBais = 1 * nodeValues[nodeOut]
            self.costGradiantB[nodeOut] += deritativeCostWrtBais

    def calculateHiddenLayerNodeValues(self, oldLayer, oldNodeValues):
        newNodeValues = [0] * self.numNodesOut
        for newNodeIndex in range(len(newNodeValues)):
            newNodeValue = 0
            for oldNodeIndex in range(len(oldNodeValues)):
                weightedInputDerivative = oldLayer.weights[newNodeIndex][oldNodeIndex]
                newNodeValue += weightedInputDerivative * oldNodeValues[oldNodeIndex]
            newNodeValue *= self.activationDerivative(self.weightedInputs[newNodeIndex])
            newNodeValues[newNodeIndex] = newNodeValue
        return newNodeValues
    
    def clearGradiants(self):
        self.costGradiantW = [[0 for _ in range(self.numNodesOut)] for _ in range(self.numNodesIn)]
        self.costGradiantB = [0] * self.numNodesOut

class NeuralNetwork:
    def __init__(self, layerSizes):
        layers = []
        for i in range(len(layerSizes) - 1):
            layers.append(Layer(layerSizes[i],layerSizes[i+1]))
        self.layers = layers

    def calculateOutputs(self, inputs):
        for i,layer in enumerate(self.layers):
            inputs = layer.calculateOutputs(inputs)
        return inputs

    def classify(self,inputs):
        outputs = self.calculateOutputs(inputs)
        return outputs.index(max(outputs))
    
    def dataPointCost(self, dataPoint):
        outputs = self.calculateOutputs(dataPoint.inputs)
        outputLayer = self.layers[-1]

        cost = 0
        for nodeOut in range(len(outputs)):
            cost += outputLayer.nodeCost(outputs[nodeOut], dataPoint.outputs[nodeOut])

        return cost
    
    def cost(self, data):
        totalCost = 0

        for i,dataPoint in enumerate(data):
            totalCost += self.dataPointCost(dataPoint)
        
        return totalCost / len(data)

    def learn(self, trainingData, learnRate):
        h = 0.01
        originalCost = self.cost(trainingData)

        for i,layer in enumerate(self.layers):
            
            for nodeIn in range(layer.numNodesIn):
                for nodeOut in range(layer.numNodesOut):
                    layer.weights[nodeIn][nodeOut] += h
                    deltaCost = self.cost(trainingData) - originalCost
                    layer.weights[nodeIn][nodeOut] -= h
                    layer.costGradiantW[nodeIn][nodeOut] = deltaCost / h

            for baisIndex in range(len(layer.baises)):
                layer.baises[baisIndex] += h
                deltaCost = self.cost(trainingData) - originalCost
                layer.baises[baisIndex] -= h
                layer.costGradiantB[baisIndex] = deltaCost / h
    
        self.applyAllGradiants(learnRate)

    def fastLearn(self, trainingData, learnRate):
        for i,dataPoint in enumerate(trainingData):
            self.updateAllGradiants(dataPoint)
        self.applyAllGradiants(learnRate / len(trainingData))
        self.clearAllGradiants()

    def applyAllGradiants(self,learnRate):
        for i,layer in enumerate(self.layers):
            layer.applyGradiants(learnRate)

    def updateAllGradiants(self,dataPoint):
        self.calculateOutputs(dataPoint.inputs)

        outputLayer = self.layers[-1]
        nodeValues = outputLayer.calculateOutputLayerNodeValues(dataPoint.outputs)
        outputLayer.updateGradiants(nodeValues)

        for hiddenLayerIndex in range(len(self.layers)-2, -1, -1):
            hiddenLayer = self.layers[hiddenLayerIndex]
            nodeValues = hiddenLayer.calculateHiddenLayerNodeValues(self.layers[hiddenLayerIndex+1], nodeValues)
            hiddenLayer.updateGradiants(nodeValues)

    def clearAllGradiants(self):
        for i,layer in enumerate(self.layers):
            layer.clearGradiants()

    def percentCorrect(self, data):
        amount = 0
        for i,dataPoint in enumerate(data):
            output = self.classify(dataPoint.inputs)
            correctOutput = dataPoint.outputs.index(max(dataPoint.outputs))
            if(output == correctOutput):
                amount += 1
        return amount / len(data) * 100

    def save(self, name):
        with open(name, "wb") as f:
            pickle.dump(self, f)

def loadNN(name):
    with open(name, "rb") as f:
        return pickle.load(f)

def run():
    start = datetime.now()
    neuralNetwork = NeuralNetwork([6,4,2])
    dataSet = readFRCDataSet("FRCTrainingData.csv")
    for i in range(20000):
        neuralNetwork.fastLearn(random.sample(dataSet, 100), 0.1)
        if(i % 10 == 0):
            print(neuralNetwork.cost(dataSet))
            print(neuralNetwork.percentCorrect(dataSet))
    testingDataSet = readFRCDataSet("FRCTestingData.csv")
    print("testing")
    print(neuralNetwork.cost(testingDataSet))
    print(neuralNetwork.percentCorrect(testingDataSet))
    end = datetime.now()
    print(f"Time: {end - start}")
    neuralNetwork.save("frcNetwork.pkl")

if __name__ == "__main__":
    run()