#include "Nicla_System.h"
#include "Arduino_BHY2.h"

SensorXYZ accelerometer(SENSOR_ID_ACC);
SensorXYZ gyro(SENSOR_ID_GYRO); 

void givePythonSomeTime(){
  while(!Serial){

  }
  delay(500);
}

void setup() {
  //activates Serialport and the Accelerometer and Gyro on the Nicla Sens ME
  Serial.begin(115200);
  BHY2.begin();

  accelerometer.begin();
  gyro.begin();
}

void loop() {
  if (!Serial){
    givePythonSomeTime();
  }
  
  // deffines all the values later used
  float current_acc_x = 0;
  float current_acc_y;
  float current_acc_z;
  float bitToMs = 40181.76;



  

  BHY2.update();
  // getts the current vallues for the x,y,z-Axis for the acellerometer and Gyro and converts them to m/s^2 and °/s
  current_acc_x = accelerometer.x()/(bitToMs);
  current_acc_y = accelerometer.y()/(bitToMs);
  current_acc_z = accelerometer.z()/bitToMs;

  // Printing values to the Serialport seperatet by ";"" in order use the split() funktion in python to create a list of seperatet values.
  Serial.print(current_acc_x), Serial.print(";"), Serial.print(current_acc_y), Serial.print(";"), Serial.println(current_acc_z);

  delay(50);

  
  

  
}
