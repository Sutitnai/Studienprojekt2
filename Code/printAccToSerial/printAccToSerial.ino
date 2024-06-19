#include "Nicla_System.h"
#include "Arduino_BHY2.h"

SensorXYZ accelerometer(SENSOR_ID_ACC);
SensorXYZ gyro(SENSOR_ID_GYRO); 

float acc_X_correction = 0;
float acc_Y_correction = 0;
float acc_Z_correction = 0;
float bitToMs = 1; //40181.76;

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
  delay(2000);
  //correctSensorOffset();
}

void loop() {
  if (!Serial){
    givePythonSomeTime();
  }
  
  // deffines all the values later used
  float current_acc_x;
  float current_acc_y;
  float current_acc_z;



  

  BHY2.update();
  // getts the current vallues for the x,y,z-Axis for the acellerometer and Gyro and converts them to m/s^2 and °/s

  current_acc_x = accelerometer.x();
  current_acc_y = accelerometer.y();
  current_acc_z = accelerometer.z();

  // Printing values to the Serialport seperatet by ";"" in order use the split() funktion in python to create a list of seperatet values.
  Serial.print(current_acc_x/bitToMs ), Serial.print(";"), Serial.print(current_acc_y/bitToMs ), Serial.print(";"), Serial.println(current_acc_z/bitToMs);

  delay(50);

  
  

  
}
