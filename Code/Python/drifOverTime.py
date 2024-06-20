import serial
from matplotlib import pyplot as plt
import timeit
import statistics
import numpy as np
import pickle
from datetime import datetime

def convert_str_to_list_of_float(string: str) -> list[float]:
    """
    Convert a semicolon-separated string of numbers into a list of floats.

    Args:
    - string (str): Input string with semicolon-separated numbers.

    Returns:
    - list[float]: List of floats parsed from the input string. Non-convertible
      entries are replaced with 0.0.
    """
    bits_to_ms = 40181.76
    float_measurements = []  # Initialize an empty list to store float measurements
    str_measurements = string.split(";")  # Split the input string by semicolons
    for measurement in str_measurements:
        try:
            x = float(measurement)  # Convert each measurement to float
        except ValueError:
            x = 0.0  # If conversion fails, set the value to 0.0
        float_measurements.append(x / bits_to_ms)  # Add the float value to the list
    while len(float_measurements) < 3:
        float_measurements.append(0.0)
    return float_measurements

def track_serial(com_port: str, measure_time: int) -> tuple[bool, dict[str, list[float]]]:
    """
    Track and read sensor data from a serial port for a specified duration.

    Args:
    - com_port (str): The COM port to connect to.
    - measure_time (int): Duration in seconds for which to read data.

    Returns:
    - tuple[bool, dict[str, list[float]]]: A tuple containing a success flag and a dictionary
      with lists of sensor data for each axis ('X', 'Y', 'Z').
    """
    results = {"X": [], "Y": [], "Z": []}  # Initialize a dictionary to store results
    print("Trying to connect to serial port")
    try:
        # Attempt to connect to the specified serial port
        serial_port = serial.Serial(port=com_port, baudrate=115200)
        print("Connected")
    except serial.serialutil.SerialException:
        print("Connection failed")
        return False, results  # Return false if the connection fails

    print("Monitoring sensor...")    
    start_time = timeit.default_timer()  # Record the start time
    while (timeit.default_timer() - start_time) < float(measure_time):
        remaining_time = round((measure_time - (timeit.default_timer() - start_time)) / 60, 2)
        print("\r>> Time remaining: {} min.".format(remaining_time), end='')  # Update the remaining time for the user
        if serial_port.in_waiting > 1:  # Check if there is data waiting in the serial buffer
            serial_input = serial_port.readline()  # Read a line of input from the serial port
            try:
                serial_str = serial_input.decode("Ascii")  # Decode the input as an ASCII string
            except UnicodeDecodeError:
                print("Unicode Error")
                pass
            current_results = convert_str_to_list_of_float(serial_str)  # Convert the string to a list of floats

            for i, key in enumerate(results.keys()):
                results[key].append(current_results[i])  # Add the float values to the respective axis lists

    serial_port.close()  # Close the serial port
    print("Finished.")

    return True, results  # Return the success flag and results

def calc_mean(measurements_dict: dict[str, list[float]]) -> list[float]:
    """
    Calculate the mean of the measurements for each axis.

    Args:
    - measurements_dict (dict): Dictionary containing lists of measurements for each axis.

    Returns:
    - list[float]: List of mean values for each axis.
    """
    means = []
    for key in measurements_dict.keys():
        mean = statistics.mean(measurements_dict[key])
        means.append(mean)
    return means 

def calc_basline(com_port: str):
    """
    Calculate the baseline measurement for drift correction.

    Args:
    - com_port (str): The COM port to connect to.

    Returns:
    - None
    """
    print("Finding Baseline for drift...")
    success_flag, baseline_dict = track_serial(com_port=com_port, measure_time=30)
    if success_flag:
        baseline = calc_mean(baseline_dict)
    else:
        baseline = calc_basline(com_port=com_port)
        print("Failed retrying")
    print("Your Baseline is:")
    print(baseline)
    with open("saved_baseline.pkl", "wb") as f:
        pickle.dump(baseline, f)
    print("Saved baseline.")

def create_storage_for_data():
    """
    Create a storage file for measurement data.
    """
    measurements = {"Datetime": [], "measurement": []}
    with open("saved_measurement.pkl", "wb") as file:
        pickle.dump(measurements, file)
        print('Data has been saved.')

def save_data(measurements: list[float]):
    """
    Save the measurement data to a file.

    Args:
    - measurements (list[float]): List of measurement data to be saved.
    """
    with open("saved_measurement.pkl", "rb") as file:
        measurements_dict = pickle.load(file)

    now = datetime.now()
    dt_string = now.strftime("%H:%M:%S")
    measurements_dict["Datetime"].append(dt_string)
    measurements_dict["measurement"].append(measurements)
    with open("saved_measurement.pkl", "wb") as file:
        pickle.dump(measurements_dict, file)

def plot_data():
    """
    Plot the measurement data.
    """
    with open("saved_measurement.pkl", "rb") as file:
        measurements_dict = pickle.load(file)
    
    with open("saved_baseline.pkl", "rb") as file:
        baseline = pickle.load(file)

    list_x, list_y, list_z = [], [], []
    for measurement in measurements_dict["measurement"]:
        list_x.append(measurement[0] - baseline[0])
        list_y.append(measurement[1] - baseline[1])
        list_z.append(measurement[2] - baseline[2])

    plt.plot(measurements_dict["Datetime"], list_x, label="X")
    plt.plot(measurements_dict["Datetime"], list_y, label="Y")
    plt.plot(measurements_dict["Datetime"], list_z, label="Z")

    plt.legend()
    plt.xlabel("Time")
    plt.ylabel("Sensor readings in m/s^2")
    plt.title("Sensor Drift")
    plt.xticks(rotation=25)
    plt.show()

def handle_measurements(com_port: str, measuring_time: int, num_measurements: int):
    """
    Handle the process of taking and saving multiple measurements.

    Args:
    - com_port (str): The COM port to connect to.
    - measuring_time (int): Time duration for each measurement in seconds.
    - num_measurements (int): Number of measurements to take.
    """
    calc_basline(com_port=com_port)
    for i in range(num_measurements):
        remaining_measurements = num_measurements - i
        print("Measurements remaining: " + str(remaining_measurements))
        success_flag, measurements_dict = track_serial(com_port=com_port, measure_time=measuring_time)
        if success_flag:
            save_data(calc_mean(measurements_dict))
        else:
            print("Failed!")
    
    print("Finished all measurements, plotting now...")
    plot_data()
    print("Done")

if __name__ == "__main__":
    print("Welcome")
    com_port = input("Enter the COM port: ")
    print("You've selected: " + com_port)
    measuring_time = input("Enter the time you want to measure in seconds: ")
    print("Your measuring time is: " + measuring_time)
    num_measurements = input("Enter the number of measurements: ")
    print("You've selected " + num_measurements + " measurements.")
    handle_measurements(com_port=com_port, measuring_time=int(measuring_time), num_measurements=int(num_measurements))
