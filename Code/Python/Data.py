import pandas as pd


class Data():
    def __init__(self) -> None:
        self.lastSensorReading = [] #acceleration for X,Y,Z
        self.data = {"X":[], "Y":[], "Z":[]}
        self.df = pd.DataFrame(self.data) #Dataframe wth sensor readings and timestemp
        self.threshhold = 0.2