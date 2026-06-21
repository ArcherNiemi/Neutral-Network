
import pandas as pd

class dataPoint:
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs

def readDataSet(file):
    df = pd.read_csv(file)
    dataSet: list = []
    for i in range(df.shape[0]):
        dataSet.append(dataPoint([df.iloc[i]['spikes'],df.iloc[i]['spots']],[opposite(df.iloc[i]['poisonous']), df.iloc[i]['poisonous']]))
    return dataSet

def readFRCDataSet(file):
    df = pd.read_csv(file)
    dataSet: list = []
    for i in range(df.shape[0]):
        dataSet.append(dataPoint([df.iloc[i]['Red 1'],df.iloc[i]['Red 2'],df.iloc[i]['Red 3'],df.iloc[i]['Blue 1'],df.iloc[i]['Blue 2'],df.iloc[i]['Blue 3']],[df.iloc[i]['Red Win'],df.iloc[i]['Blue Win']]))
    return dataSet

def opposite(value):
    if(value == 1):
        return 0
    else:
        return 1