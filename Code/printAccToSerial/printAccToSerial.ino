#include "Nicla_System.h"
#include "Arduino_BHY2.h"

SensorXYZ accelerometer(SENSOR_ID_ACC);
SensorXYZ gyro(SENSOR_ID_GYRO); 

float acc_X_correction = 0;
float acc_Y_correction = 0;
float acc_Z_correction = 0;
float bitToMs = 40181.76;

void givePythonSomeTime(){
  while(!Serial){

  }
  delay(500);
}

void correctSensorOffset(){
  float sum_X = 0;
  float sum_Y = 0;
  float sum_Z = 0;
  int i;
  float n = 400;
  for (i=0;i<n;i++){
    sum_X = sum_X + accelerometer.x()/bitToMs;
    sum_Y = sum_Y + accelerometer.y()/bitToMs;
    sum_Z = sum_Z +accelerometer.z()/bitToMs;
    delay(50);
  }
  acc_X_correction = sum_X/n;
  acc_Y_correction = sum_Y/n;
  acc_Z_correction = sum_Z/n;
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

  current_acc_x = accelerometer.x()/(bitToMs);
  current_acc_y = accelerometer.y()/(bitToMs);
  current_acc_z = accelerometer.z()/bitToMs;

  // Printing values to the Serialport seperatet by ";"" in order use the split() funktion in python to create a list of seperatet values.
  Serial.print(current_acc_x - acc_X_correction), Serial.print(";"), Serial.print(current_acc_y - acc_Y_correction), Serial.print(";"), Serial.println(current_acc_z - acc_Z_correction);

  delay(50);

  
  

  
}
