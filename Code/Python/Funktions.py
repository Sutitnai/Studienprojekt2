import serial
import time as tm
import pandas as pd


from .ViewModel import ViewModel


class Funktions():

    def __init__(self) -> None:  
        self.vm = ViewModel()
        self.serialString = "" 
        self.lastStr = ""   
                              


    def checkThreshhold(self, mesurements:list) ->bool:
        """Checks if one of the values is outside of the given thrashhold."""
        ret = False
        for mesurement in mesurements:
            if mesurement >= self.vm.data.threshhold or mesurement <= -self.vm.data.threshhold:
                ret = True
            else:
                pass

        return ret


    def trackSerialPort(self):
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
                if convString == self.lastStr:
                    pass
                else:
                    #create list of the single mesurements seperatet by ;
                    strMesurements = convString.split(";")
                    
                    #create s list of floats from the list of strings
                    for number in strMesurements:
                        x = float(number)
                        numbMesurements = numbMesurements + [x]
                    
                    self.finishedMesurement = numbMesurements
                    self.checkThreshhold(numbMesurements)
                    self.vm.UpdateSensorReading(reading=numbMesurements)
                    if self.checkThreshhold:
                       self.trackData()

                        

    def trackData(self):
        if self.vm.data.lastSensorReading != self.finishedMesurement:
            self.vm.data.df.append(self.vm.data.lastSensorReading, ignore_index = True)