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

#def trackSerialPort(serialPort:sr.Serial) -> list[float]:
    if serialPort.in_waiting > 1:
        serialInput = serialPort.readline()
        if len(serialInput) > 0:
            serialString = serialInput.decode('Ascii')
            mesurements = convrertStrToListOfFloat(serialString)
        else:
            tm.sleep(0.05)
            trackSerialPort(serialPort=serialPort)
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
    try:
        serialPort = sr.Serial(port=comPort, baudrate=115200)
    except sr.serialutil.SerialException:
        print("Conection failed")
    print("Watching for earthquake....")
    while i <= 6000:
        i = i + 1
        if serialPort.in_waiting > 1:
            print("t")
            serialInput = serialPort.readline()
            serialString = serialInput.decode('Ascii')
            currentMesurement = convrertStrToListOfFloat(serialString)
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
fileName = input("Please select a file name: ")
filePath = input("Please enter Path for saved Data: ")
print("Youve Selected: " + filePath)
threshhold = float(input("Please enter Threshhold: "))
print("Youve Selected: " + str(threshhold))

fullPathe = filePath + "/" + fileName
while(1):
    pathUsed = filePath + "/mesurement" + str(mesurementsTaken)
    if monitorEarthquake(comPort=comPort, filePath=fullPathe, threshhold=threshhold):
        mesurementsTaken += 1
    else:
        tm.sleep(5)