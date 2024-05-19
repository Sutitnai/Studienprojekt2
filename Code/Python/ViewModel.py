from .Data import Data
from .Funktions import Funktions

class ViewModel():
    def __init__(self) -> None:
        self.data = Data()

    def UpdateSensorReading(self, reading:list):
        self.data.lastSensorReading = reading