import serial as sr
import pandas as pd
import time as tm
from typing import Union
from datetime import datetime
from timeit  import default_timer
import keyboard

mesurementsTaken = 0
bitsToMs = 40181.76

def convrertStrToListOfFloat(string: str) -> list[float]:
    """
    Convert a semicolon-separated string of numbers into a list of floats.
    
    Args:
    - string (str): Input string with semicolon-separated numbers.
    
    Returns:
    - list[float]: List of floats parsed from the input string. Non-convertible
      entries are replaced with 0.0.
    """
    floatMesuremnts = []  # Initialize an empty list to store float measurements
    strMesurements = string.split(";")  # Split the input string by semicolons
    for mesurement in strMesurements:
        try:
            x = float(mesurement)  # Convert each measurement to float
        except ValueError:
            x = 0.0  # If conversion fails, set the value to 0.0
        floatMesuremnts += [x/bitsToMs]  # Add the float value to the list
    return floatMesuremnts

def correctionFaktor(comPort: str) -> list:
    """
    Calculate the correction factor for sensor data by averaging the readings over 60 samples.
    
    Args:
    - comPort (str): The COM port to connect to.
    
    Returns:
    - list: A list containing the correction factors for X, Y, and Z axes.
    """
    correction = [0, 0, 0]  # Initialize correction factor list
    sumList = [0, 0, 0]  # Initialize sum list for calculating average
    i = 0
    print("connecting to serial Port")
    try:
        # Attempt to connect to the specified serial port
        serialPort = sr.Serial(port=comPort, baudrate=115200)
        print("connected!!")
    except sr.serialutil.SerialException:
        print("Failed to connect to Serial Port")
    print("Calculating correction factor")
    while i <= 60:
        i += 1
        serialInput = serialPort.readline()  # Read a line of input from the serial port
        try:
            serialString = serialInput.decode('Ascii')  # Decode the input as an ASCII string
            currentMesurement = convrertStrToListOfFloat(serialString)  # Convert the string to a list of floats
            for j in range(len(sumList)):
                sumList[j] = sumList[j] + currentMesurement[j]  # Sum the measurements for each axis
        except UnicodeDecodeError:
            pass
        for j in range(len(sumList)):
            correction[j] = sumList[j] / 60  # Calculate the average for each axis
    print("X, Y, Z")
    print(correction)
    return correction

def checkThreshhold(threshhold: float, mesurements: list[float]) -> bool:
    """
    Check if any measurement exceeds the specified threshold.
    
    Args:
    - threshhold (float): The threshold value.
    - mesurements (list[float]): List of measurements.
    
    Returns:
    - bool: True if any measurement exceeds the threshold, otherwise False.
    """
    ret = False
    for mesurement in mesurements:
        if mesurement >= threshhold or mesurement <= -threshhold:
            ret = True
    return ret

def track(comPort: str, threshhold: float, mesureing_time: int) -> Union[bool, dict]:
    """
    Track all input from the serial port for a specified time. If there is movement over the threshold for more than 30 seconds, return the data; otherwise, return False.
    
    Args:
    - comPort (str): The COM port to connect to.
    - threshhold (float): The threshold value for detecting significant movement.
    - mesureing_time (int): The duration for monitoring in minutes.
    
    Returns:
    - Union[bool, dict]: Dictionary of measurements if movement is detected; otherwise, False.
    """
    mesurements = {"X": [], "Y": [], "Z": []}  # Initialize a dictionary to store measurements
    i = 0
    mesurementsOverThreshholde = 0
    print("Connecting to serial port...")
    try:
        # Attempt to connect to the specified serial port
        serialPort = sr.Serial(port=comPort, baudrate=115200)
        print("Connected")
        tm.sleep(0.07)  # Wait briefly to ensure the connection is established
    except sr.serialutil.SerialException:
        print("Connection failed")
        return False  # Return False if the connection fails
    print("Watching for earthquake...")
    start_time = default_timer()
    while (default_timer() - start_time) < float(mesureing_time * 60):
        if keyboard.is_pressed('esc'):
            print("Exiting measuring loop...")
            break

        remaining_time = round((mesureing_time * 60 - (default_timer() - start_time)) / 60, 2)
        print("\r>> Time remaining: {} min.".format(remaining_time), end='')  # Update the remaining time for the user
        if serialPort.in_waiting > 1:  # Check if there is data waiting in the serial buffer
            i += 1
            serialInput = serialPort.readline()  # Read a line of input from the serial port
            try:
                serialString = serialInput.decode('Ascii')  # Decode the input as an ASCII string
            except UnicodeDecodeError:
                return False  # Return False if there is a decoding error
            currentMesurement = convrertStrToListOfFloat(serialString)  # Convert the string to a list of floats
            for x in range(len(currentMesurement)):
                currentMesurement[x] = currentMesurement[x] - correction[x]  # Apply correction factor
            if checkThreshhold(mesurements=currentMesurement, threshhold=threshhold):
                mesurementsOverThreshholde += 1
            j = 0
            for key in mesurements.keys():
                mesurements[key] += [currentMesurement[j]]  # Add the measurements to the dictionary
                j += 1

    serialPort.close()  
    print(mesurementsOverThreshholde)
    if mesurementsOverThreshholde >= 60:  # Check if movement was detected for over 30 seconds
        return mesurements
    else:
        return False

def monitorEarthquake(comPort: str, filePath: str, threshhold: float, mesuring_time: int) -> bool:
    """
    Monitor for earthquakes and save the measurements if detected.
    
    Args:
    - comPort (str): The COM port to connect to.
    - filePath (str): The file path to save the data.
    - threshhold (float): The threshold value for detecting significant movement.
    - mesuring_time (int): The duration for monitoring in minutes.
    
    Returns:
    - bool: True if an earthquake is detected and data is saved, otherwise False.
    """
    mesurement = track(comPort=comPort, threshhold=threshhold, mesureing_time=mesuring_time)
    if mesurement == False:
        print("No earthquake detected.")
        return False
    else:
        currentMesurement = pd.DataFrame(mesurement)  # Convert the measurements to a DataFrame
        currentMesurement.to_csv(path_or_buf=filePath)  # Save the DataFrame to a CSV file
        print("Earthquake detected, saved to: " + filePath)
        return True

# Main execution
print("Welcome!!")
comPort = input("Please enter the COM port that is connected to the Sensor: ")
print("You've selected: " + comPort)
filePath = input("Please enter Path for saved Data: ")
print("You've selected: " + filePath)
threshhold = float(input("Please enter Threshold: "))
print("You've selected: " + str(threshhold))
mesuring_time = input("Enter the mesuring time in min: ")
print("Youve selected a mesuring time of {} min.".format(mesuring_time))
counter = -1

# Continuously monitor for earthquakes

while True:
    now = datetime.now()
    fileName = now.strftime("%y%m%d")
    date_time = now.strftime("%d.%m.%y %H:%M")
    print(date_time)
    fullPath = filePath + "/" + fileName + "_" + str(mesurementsTaken) + ".csv"
    counter += 1
    if not counter % 5:
        correction = correctionFaktor(comPort=comPort)  # Recalculate correction factor every 5 cycles
    if monitorEarthquake(comPort=comPort, filePath=fullPath, threshhold=threshhold, mesuring_time=int(mesuring_time)):
        mesurementsTaken += 1  # Increment the count of measurements taken
    else:
        pass


