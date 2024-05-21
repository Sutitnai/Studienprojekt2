import serial as sr
import pandas as pd
import time as tm

mesurementsTaken = 0




def convrertStrToListOfFloat(string: str) -> list[float]:
    floatMesuremnts = []
    strMesurements = string.split(";")
    for mesurement in strMesurements:
        x = float(mesurement)
        floatMesuremnts += [x]
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

def trackFiveMin(comPort:str, threshhold: float ):
    """Tracks all the input from the serial port for 5min. if there is movement for over 30sec it returns the dict else it returns False."""
    mesurements = {"X":[], "Y":[], "Z":[]}
    i = 0
    mesurementsOverThreshholde = 0
    print("conecting to serialport...")
    serialPort = sr.Serial(port=comPort, baudrate=115200)
    print("Watching for earthquake....")
    while i <= 6000:
        i = i + 1
        currentMesurement = trackSerialPort(serialPort=serialPort)
        if checkThreshhold(mesurements=currentMesurement, threshhold=threshhold):
            mesurementsOverThreshholde += 1
        j = 0
        for key in mesurements.keys():
            mesurements[key] += [currentMesurement[j]]
            j += 1
    serialPort.close()  
    if mesurementsOverThreshholde >= 600:
        return mesurements
    else:
        return False
    
def monitorEarthquake(comPort: str, filePath:str, threshhold:float) -> bool:
    mesurement = trackFiveMin(comPort=comPort, threshhold=threshhold)
    if mesurement == False:
        print("No earthquake deteckted in the last 5 min.")
        return False
    else:
        currentMesurement = pd.DataFrame(mesurement)
        currentMesurement.to_csv(path_or_buf=filePath)
        print("Earthquake deteckted saved to: " + filePath)
        return True





print("Welcome!!")
comPort = input("Please enter the COM port that is conected to the Sensor: ")
print("Youve Selected: " + comPort)
filePath = input("Please enter Path for saved Data: ")
print("Youve Selected: " + filePath)
threshhold = float(input("Please enter Threshhold: "))
print("Youve Selected: " + str(threshhold))


while(1):
    pathUsed = filePath + "/mesurement" + str(mesurementsTaken)
    if monitorEarthquake(comPort=comPort, filePath=pathUsed, threshhold=threshhold):
        mesurementsTaken += 1
    else:
        pass