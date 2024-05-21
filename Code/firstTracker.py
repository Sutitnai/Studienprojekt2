import serial as sr
import pandas as pd
import time as tm

mesurementsTaken = 0




def convrertStrToListOfFloat(string: str) -> list[float]:
    floatMesuremnts = []
    strMesurements = string.split(";")
    for mesurement in strMesurements:
        x = float(mesurement)
        floatMesuremnts += x
    return floatMesuremnts

def trackSerialPort(serialPort:sr.Serial) -> list[float]:
    if serialPort.in_waiting > 1:
        serialInput = serialPort.readline()
        serialString = serialInput.decode('Ascii')
        mesurements = convrertStrToListOfFloat(serialString)
        return mesurements
        

def checkThreshhold(threshhold: float, mesurements: list[float]) -> bool:
    ret = False
    for mesurement in mesurements:
        if mesurement >= threshhold or mesurement <= - threshhold:
            ret = True
        else:
            pass
    return ret

print("Welcome!!")
comPort = input("Please enter the COM port that is conected to the Sensor: ")
filePath = input("Please enter Path vor saved Data: ")
print("Connecnting to serial Port....")
serialPort = sr.Serial(port=comPort, baudrate=115200)
print("wachting for earthquakes...")
#while(1):
