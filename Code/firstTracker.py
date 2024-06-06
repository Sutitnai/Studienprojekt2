import serial as sr
import pandas as pd
import time as tm
from typing import Union

mesurementsTaken = 0




def convrertStrToListOfFloat(string: str) -> list[float]:
    floatMesuremnts = []
    strMesurements = string.split(";")
    for mesurement in strMesurements:
        try:
            x = float(mesurement)
        except ValueError:
            x = 0.0
        
        floatMesuremnts += [x]
    return floatMesuremnts


        
def correctionFaktor(comPort: str) -> list:
    correction = [0,0,0]
    sumList = [0,0,0]
    i = 0
    print("connecting to serial Port")
    try:
        serialPort = sr.Serial(port=comPort, baudrate=115200)
        print("conected!!")
    except sr.serialutil.SerialException:
        print("Faild to conect to Serial Port")
    print("Calculating corection faktor")
    while i <= 60:
        i+= 1
        serialInput = serialPort.readline()
        try:
            serialString = serialInput.decode('Ascii')
            currentMesurement = convrertStrToListOfFloat(serialString)
            for j in range(len(sumList)):
                sumList[j] = sumList[j] + currentMesurement[j]
        except UnicodeDecodeError:
            pass
        for j in range(len(sumList)):
            correction[j] = sumList[j]/100
    print("X,Y,Z")
    print(correction)
    return correction

def checkThreshhold(threshhold: float, mesurements: list[float]) -> bool:
    ret = False
    for mesurement in mesurements:
        if mesurement >= threshhold or mesurement <= - threshhold:
            ret = True
        else:
            pass
    print(ret)
    return ret

def track(comPort:str, threshhold: float ) -> Union[bool, dict]:
    """Tracks all the input from the serial port for 5min. if there is movement for over 30sec it returns the dict else it returns False."""
    mesurements = {"X":[], "Y":[], "Z":[]}
    i = 0
    mesurementsOverThreshholde = 0
    print("conecting to serialport...")
    try:
        serialPort = sr.Serial(port=comPort, baudrate=115200)
        print("Conected")
        tm.sleep(0.07)
    except sr.serialutil.SerialException:
        print("Conection failed")
    print("Watching for earthquake....")
    while i <= 1200:
        if serialPort.in_waiting > 1:
            i = i + 1
            serialInput = serialPort.readline()
            try:
                serialString = serialInput.decode('Ascii')
            except UnicodeDecodeError:
                return False
            currentMesurement = convrertStrToListOfFloat(serialString)
            for x in range(len(currentMesurement)):
                currentMesurement[x] = currentMesurement[x] - correction[x]
            if checkThreshhold(mesurements=currentMesurement, threshhold=threshhold):
                mesurementsOverThreshholde += 1
            j = 0
            for key in mesurements.keys():
                mesurements[key] += [currentMesurement[j]]
                j += 1

    serialPort.close()  
    print(mesurementsOverThreshholde)
    if mesurementsOverThreshholde >= 60:
        return mesurements
    else:
        return False
    
def monitorEarthquake(comPort: str, filePath:str, threshhold:float) -> bool:
    mesurement = track(comPort=comPort, threshhold=threshhold)
    if mesurement == False:
        print("No earthquake deteckted.")
        return False
    else:
        currentMesurement = pd.DataFrame(mesurement)
        currentMesurement.to_csv(path_or_buf=filePath)
        print("Earthquake deteckted saved to: " + filePath)
        return True





print("Welcome!!")
comPort = input("Please enter the COM port that is conected to the Sensor: ")
print("Youve Selected: " + comPort)
fileName = input("Please select a file name: ")
filePath = input("Please enter Path for saved Data: ")
print("Youve Selected: " + filePath)
threshhold = float(input("Please enter Threshhold: "))
print("Youve Selected: " + str(threshhold))
counter = -1


while(1):
    fullPathe = filePath + "/" + fileName + "_" + str(mesurementsTaken) +".csv"
    counter += 1
    if not counter % 5:
        correction = correctionFaktor(comPort=comPort)
    if monitorEarthquake(comPort=comPort, filePath=fullPathe, threshhold=threshhold):
        mesurementsTaken += 1
    else:
        pass