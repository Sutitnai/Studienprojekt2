import serial as sr
from matplotlib import  pyplot as  plt
import  timeit as tmi
import statistics
import numpy as np

def convrertStrToListOfFloat(string: str) -> list[float]:
    """
    Convert a semicolon-separated string of numbers into a list of floats.
    
    Args:
    - string (str): Input string with semicolon-separated numbers.
    
    Returns:
    - list[float]: List of floats parsed from the input string. Non-convertible
      entries are replaced with 0.0.
    """

    bitsToMs = 40181.76
    floatMesuremnts = []  # Initialize an empty list to store float measurements
    strMesurements = string.split(";")  # Split the input string by semicolons
    for mesurement in strMesurements:
        try:
            x = float(mesurement)  # Convert each measurement to float
        except ValueError:
            x = 0.0  # If conversion fails, set the value to 0.0
        floatMesuremnts += [x/bitsToMs]  # Add the float value to the list
    return floatMesuremnts

def trackSerial(comPort: str, mesureTm: int) -> tuple[bool, dict[str, list]]:
    """
    Track and read sensor data from a serial port for a specified duration.
    
    Args:
    - comPort (str): The COM port to connect to.
    - mesureTm (int): Duration in seconds for which to read data.
    
    Returns:
    - tuple[bool, dict[str, list]]: A tuple containing a success flag and a dictionary
      with lists of sensor data for each axis ('X', 'Y', 'Z').
    """
    results = {"X": [], "Y": [], "Z": []}  # Initialize a dictionary to store results
    print("trying to connect to serial port")
    try:
        # Attempt to connect to the specified serial port
        serialPort = sr.Serial(port=comPort, baudrate=115200)
        print("connected")
    except sr.serialutil.SerialException:
        print("Connection failed")
        return False, results  # Return false if the connection fails

    print("monitoring Sensor...")    
    startTime = tmi.default_timer()  # Record the start time
    while (tmi.default_timer() - startTime) < float(mesureTm):
        remTime = round((mesureTm -(tmi.default_timer() - startTime)) / 60, 2) #calculates the remaining time for the mesurement
        print("\r>> Time remaining: {}min.".format(remTime), end='')  #updates the remaining time for the user
        if serialPort.in_waiting > 1:  # Check if there is data waiting in the serial buffer
            serialInput = serialPort.readline()  # Read a line of input from the serial port
            try:
                serialStr = serialInput.decode("Ascii")  # Decode the input as an ASCII string
            except UnicodeDecodeError:
                return False, results  # Return false if decoding fails
            currentResults = convrertStrToListOfFloat(serialStr)  # Convert the string to a list of floats

            j = 0
            for key in results.keys():
                results[key] += [currentResults[j]]  # Add the float values to the respective axis lists
                j += 1

    serialPort.close()  # Close the serial port
    print("finished.")

    return True, results  # Return the success flag and results


def calcMean(mesurementsDict: dict[str, list[float]]) -> list[float]:
    means = []
    for key in mesurementsDict.keys():
        mean = statistics.mean(mesurementsDict[key])
        means += [mean]
    
    return mean


def storData(means: list[float]):
    mesurements = {"Datetime": [], "mesurement": []}