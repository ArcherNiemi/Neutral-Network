
import pandas as pd

class dataPoint:
    def __init__(self, spikes: float, spots: float, poisonous: int):
        self.spikes = spikes
        self.spots = spots
        self.poisonous = poisonous

dp1: dataPoint = dataPoint(0.3,0.2,0.5)

def readDataSet(file):
    df = pd.read_csv(file)
    dataSet: list = []
    for i in range(df.shape[0]):
        dataSet.append(dataPoint(df.iloc[i]['spikes'],df.iloc[i]['spots'],df.iloc[i]['poisonous']))
    return dataSet