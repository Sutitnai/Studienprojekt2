import serial
import time

serialPort = serial.Serial(port="COM3", baudrate=115200)

threshhold = 0.2
serialString = ""    
lastMesurement =[]                       
numbMesurements =[]

def checkThreshhold(threshhold:float, mesurements: list[float]) ->bool:
    """Checks if one of the values is outside of the given thrashhold."""
    ret = False
    for mesurement in mesurements:
        if mesurement >= threshhold or mesurement <= -threshhold:
            ret = True
        else:
            pass

    return ret

#some changes to see how git reacts

while(1):

    # Wait until there is data waiting in the serial buffer
    if(serialPort.in_waiting > 0):

        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline()

        #convert sthe data to string
        convString = serialString.decode('Ascii')
       
       #create list of the single mesurements seperatet by ;
        strMesurements = convString.split(";")

        #create s list of floats from the list of strings
        for number in strMesurements:
            x = float(number)
            numbMesurements = numbMesurements + [x]

    if lastMesurement == numbMesurements:
        lastMesurement = numbMesurements
    else:
        lastMesurement = numbMesurements
        print(numbMesurements)
        print(checkThreshhold(threshhold=threshhold, mesurements=numbMesurements))
        
        
        
        
                
