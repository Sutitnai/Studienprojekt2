#include "Nicla_System.h"
#include "Arduino_BHY2.h"

SensorXYZ accelerometer(SENSOR_ID_ACC);
SensorXYZ gyro(SENSOR_ID_GYRO); 



void setup() {
  //activates Serialport and the Accelerometer and Gyro on the Nicla Sens ME
  Serial.begin(115200);
  while (!Serial){};
  BHY2.begin();

  accelerometer.begin();
  gyro.begin();
}

void loop() {
  // deffines all the values later used
  float total_acc_x = 0;
  float total_acc_y = 0;
  float total_acc_z = 0;
  float total_gyro_x = 0;
  float total_gyro_y = 0;
  float total_gyro_z = 0;
  float current_acc_x = 0;
  float current_acc_y;
  float current_acc_z;
  float current_gyro_x;
  float current_gyro_y;
  float current_gyro_z; 
  float bitToMs = 40181.76;
  int bitToRads = 15.4;
  int i;
  while(!Serial){

  }
  for(i=0; i<1001;i++){
    int startTime = millis();
    BHY2.update();
    // getts the current vallues for the x,y,z-Axis for the acellerometer and Gyro and converts them to m/s^2 and °/s
    current_acc_x = accelerometer.x()/(bitToMs);
    current_acc_y = accelerometer.y()/(bitToMs);
    current_acc_z = accelerometer.z()/bitToMs;
    current_gyro_x = gyro.x()/bitToRads;
    current_gyro_y = gyro.y()/bitToRads;
    current_gyro_z = gyro.z()/bitToRads;
    //Adds the colected values to average the drift
    total_acc_x = total_acc_x + current_acc_x;
    total_acc_y = total_acc_y + current_acc_y;
    total_acc_z = total_acc_z + current_acc_z;
    total_gyro_x = total_gyro_x + current_gyro_x;
    total_gyro_y = total_gyro_y + current_gyro_y;
    total_gyro_z = total_gyro_z + current_gyro_z;
    //Prints current Acceleration and Rotation to Serialport
    Serial.println("ACC:");
    Serial.print("X: "), Serial.print(current_acc_x), Serial.print("\t Y: "), Serial.print(current_acc_y), Serial.print("\t Z: "), Serial.println(current_acc_z);
    Serial.println("GYRO:");
    Serial.print("X: "), Serial.print(current_gyro_z), Serial.print("\t Y: "), Serial.print(current_gyro_y), Serial.print("\t Z:  "), Serial.println(current_gyro_x);
    //Waits for sensor to update
    while (millis()-startTime < 100){
      delay(1);
    }
  }
  //Prints the drift to serialport
  Serial.println("acceleration drift in m/s:");
  Serial.print("X: "), Serial.print(total_acc_x/1000), Serial.print("\t Y: "), Serial.print(total_acc_y/1000), Serial.print("\t Z: "), Serial.println(total_acc_z/1000);
  Serial.println("gyroscope drift in m/s:");
 Serial.print("X: "), Serial.print(total_gyro_x/1000), Serial.print("\t Y: "), Serial.print(total_gyro_y/1000), Serial.print("\t Z:  "), Serial.println(total_gyro_z/1000);

  delay(30000);
  
}
