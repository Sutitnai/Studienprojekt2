import serial
import time as tm
import pandas as pd



data = {"X":[], "Y":[], "Z":[]}
mesurement = pd.DataFrame(data)
print(mesurement)
threshhold = 0.2
serialString = ""    
lastMesurement =[] 
lastStr = ""                      


def checkThreshhold(threshhold:float, mesurements: list[float]) ->bool:
    """Checks if one of the values is outside of the given thrashhold."""
    ret = False
    for mesurement in mesurements:
        if mesurement >= threshhold or mesurement <= -threshhold:
            ret = True
        else:
            pass

    return ret


serialPort = serial.Serial(port="COM3", baudrate=115200)
while(1):
    
    numbMesurements =[]
    # Wait until there is data waiting in the serial buffer
    if(serialPort.in_waiting > 0):
        #tm.sleep(0.025)
        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline()

        #convert sthe data to string
        convString = serialString.decode('Ascii')
        if convString == lastStr:
            pass
        else:
            #create list of the single mesurements seperatet by ;
            strMesurements = convString.split(";")
            
            #create s list of floats from the list of strings
            for number in strMesurements:
                x = float(number)
                numbMesurements = numbMesurements + [x]

            if lastMesurement == numbMesurements:
                pass
            else:
                lastMesurement = numbMesurements
                
                print(numbMesurements)
                print(checkThreshhold(threshhold=threshhold, mesurements=numbMesurements))
                
                
        
        
                
