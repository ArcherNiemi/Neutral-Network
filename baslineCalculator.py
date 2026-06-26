from dataPoints import readFRCDataSet

def run():
    trainingDataSet = readFRCDataSet("FRCTrainingData.csv")
    testingDataSet = readFRCDataSet("FRCTestingData.csv")

    trainingCorrect = 0
    for i,dataPoint in enumerate(trainingDataSet):
        if((sum(dataPoint.inputs[:2]) > sum(dataPoint.inputs[3:]) and dataPoint.outputs[0] == 1) or (sum(dataPoint.inputs[:2]) < sum(dataPoint.inputs[3:]) and dataPoint.outputs[1] == 1)):
            trainingCorrect += 1
    
    testingCorrect = 0
    for i,dataPoint in enumerate(testingDataSet):
        if((sum(dataPoint.inputs[:2]) > sum(dataPoint.inputs[3:]) and dataPoint.outputs[0] == 1) or (sum(dataPoint.inputs[:2]) < sum(dataPoint.inputs[3:]) and dataPoint.outputs[1] == 1)):
            testingCorrect += 1
    print(f"training: {trainingCorrect/len(trainingDataSet)*100}%")
    print(f"testing: {testingCorrect/len(testingDataSet)*100}%")


if __name__ == "__main__":
    run()