
//////////////////////////////////////////////////////////
#include <MPU6050_tockn.h>
#include <Wire.h>

MPU6050 mpu6050(Wire);


// Assigning the input & output ports 
const int Touchpower_1 = 4;
const int Touchpower_2 = 5;
const int Touchpower_3 = 6;
const int inputPin_1 = 8;
const int inputPin_2 = 9;
const int inputPin_3 = 10;

int LeftClick  = 0;
int RightClick  = 0;
int ScrollClick  = 0;
int MouseVector[3] = {0,0,0};

int Xangle = 0;
int Yangle = 0;
int Zangle = 0;



  /////////////////////////////////////////////

void setup() {
  pinMode(Touchpower_1, OUTPUT);
  pinMode(Touchpower_2, OUTPUT);
  pinMode(Touchpower_3, OUTPUT);
  pinMode(inputPin_1, INPUT);
  pinMode(inputPin_2, INPUT);
  pinMode(inputPin_3, INPUT);
  
  //////////////////////////////////////////////
  
  Serial.begin(19200);
  Wire.begin();
  mpu6050.begin();
  mpu6050.calcGyroOffsets(true);
  // Set accelerometer range to +/- 2g
  //mpu6050.setFullScaleAccelRange(MPU6050_ACCEL_FS_2);
}

  ///////////////////////////////////////////////




void loop() {
  digitalWrite(Touchpower_1, HIGH);
  digitalWrite(Touchpower_2, HIGH);
  digitalWrite(Touchpower_3, HIGH);
  
  mpu6050.update();

  ////////////////////////////////////////////
  
  int Xangle = mpu6050.getAngleX();
  int Yangle = mpu6050.getAngleX();
  int Zangle = mpu6050.getAngleX();

  
  if(MouseVector[0]<1000){
    MouseVector[0]= MouseVector[0]+ Xangle;
  } else {
    MouseVector[0]= MouseVector[0];
  }
  
  if(MouseVector[1]<800){
    MouseVector[1]= MouseVector[1]+ Yangle;
  } else {
    MouseVector[1]= MouseVector[1];
  }
  

  if(MouseVector[0]<800){
    MouseVector[2]= MouseVector[2]+ Zangle;
  } else {
    MouseVector[2]= MouseVector[2];
  }

  //////////////////////////////////////////////

  
  int inputValueLC = digitalRead(inputPin_1);
  
  if (inputValueLC == HIGH) {
    LeftClick = 1;
  } else {
    LeftClick = 0;
  }
  /////////////////////////////////////////////

  
  int inputValueRC = digitalRead(inputPin_2);
  
  if (inputValueRC == HIGH) {
    RightClick = 1;
  } else {
    RightClick = 0;
  }

  ////////////////////////////////////////////
  
  int inputValueSC = digitalRead(inputPin_3);
  
  if (inputValueSC == HIGH) {
    ScrollClick = 1;
  } else {
    ScrollClick = 0;
  }
  //////////////////////////////////////////

  Serial.print("Xvalue  : ");
  Serial.println(MouseVector[0]);
  Serial.print("\tYvalue : ");
  Serial.print(MouseVector[1]);
  Serial.print("\tZvalue  : ");
  Serial.print(MouseVector[2]);

  //////////////////////////////////////////
  
  Serial.print("Left Click  : ");
  Serial.println(LeftClick);
  Serial.print("\tRight Click : ");
  Serial.print(RightClick);
  Serial.print("\tScroll Click : ");
  Serial.print(ScrollClick);


  ///////////////////////////////////////////

  Serial.print("angleX : ");
  Serial.println(mpu6050.getAngleX());
  Serial.print("\tangleY : ");
  Serial.print(mpu6050.getAngleY());
  Serial.print("\tangleZ : ");
  Serial.print(mpu6050.getAngleZ());

  delay(200);
}
