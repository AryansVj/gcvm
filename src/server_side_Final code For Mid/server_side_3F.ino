/// EE356 Product design Grp 09
/// Gesture Controlled mouse 
/// Arduino Code for ESP 32 Development kit 01


// For MPU6050 Sensor 
#include <MPU6050_tockn.h>
#include <Wire.h>

// For Bluetooth Connection 
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

// MPU6050 sensor 
MPU6050 mpu6050(Wire);

// Assigning the input & output ports and variable values 
const int Touchpower_1 = 4;
const int Touchpower_2 = 2;
const int Touchpower_3 = 15;

const int TouchpowerL_1 = 25;
const int TouchpowerL_2 = 26;
const int TouchpowerL_3 = 27;

const int inputPin_1 = 12;
const int inputPin_2 = 13;
const int inputPin_3 = 14;

int LeftClick  = 0;
int RightClick  = 0;
int ScrollClick  = 0;
int MouseVector[3] = {100,100,100};

int Xangle = 0;
int Yangle = 0;
int Zangle = 0;

int MappedX = 0; 
int MappedY = 0;
int MappedZ = 0;

// Bluetooth 
BLEServer* pServer = NULL;
BLECharacteristic* pCharacteristic = NULL;
bool deviceConnected = false;
bool oldDeviceConnected = false;
uint32_t value = 0;
uint8_t* val_cast = 0;

#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"

class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
    };

    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
    }
};


void setup() {

  pinMode(Touchpower_1, OUTPUT);
  pinMode(Touchpower_2, OUTPUT);
  pinMode(Touchpower_3, OUTPUT);

  pinMode(TouchpowerL_1, OUTPUT);
  pinMode(TouchpowerL_2, OUTPUT);
  pinMode(TouchpowerL_3, OUTPUT);

  
  pinMode(inputPin_1, INPUT);
  pinMode(inputPin_2, INPUT);
  pinMode(inputPin_3, INPUT);

 
  Serial.begin(115200);

  Wire.begin();
  mpu6050.begin();
  mpu6050.calcGyroOffsets(true);
  // Set accelerometer range to +/- 2g
  //mpu6050.setFullScaleAccelRange(MPU6050_ACCEL_FS_2);



  // Create the BLE Device
  BLEDevice::init("GCVM_Server");

  // Create the BLE Server
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());

  // Create the BLE Service
  BLEService *pService = pServer->createService(SERVICE_UUID);

  // Create a BLE Characteristic
  pCharacteristic = pService->createCharacteristic(
                      CHARACTERISTIC_UUID,
                      BLECharacteristic::PROPERTY_NOTIFY
                    );
                    
  // Create a BLE Descriptor
  pCharacteristic->addDescriptor(new BLE2902());

  // Start the service
  pService->start();

  // Start advertising
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(false);
  pAdvertising->setMinPreferred(0x0);  // set value to 0x00 to not advertise this parameter
  BLEDevice::startAdvertising();
  Serial.println("Waiting a client connection to notify...");
}

void loop() {
  
  digitalWrite(Touchpower_1, HIGH);
  digitalWrite(Touchpower_2, HIGH);
  digitalWrite(Touchpower_3, HIGH);

  digitalWrite(TouchpowerL_1, LOW);
  digitalWrite(TouchpowerL_2, LOW);
  digitalWrite(TouchpowerL_3, LOW);
  
  mpu6050.update();
  int Xangle = mpu6050.getAngleX();
  int Yangle = mpu6050.getAngleY();
  int Zangle = mpu6050.getAngleZ();


  if(MouseVector[0]<2000 &&  MouseVector[0]>= 100  ){
    MouseVector[0]= MouseVector[0]+ Xangle;
  } else if( Xangle >0 && MouseVector[0]<=100){
    MouseVector[0]= MouseVector[0]+ Xangle; 
  } else if (Xangle <0 && MouseVector[0]>=2000){
    MouseVector[0]= MouseVector[0]+ Xangle;
  } else {
    MouseVector[0]= MouseVector[0];
  }
  
  
  if(MouseVector[1]<1150 &&  MouseVector[1]>=100  ){
    MouseVector[1]= MouseVector[1]+ Yangle;
  } else if( Yangle > 0 && MouseVector[1]<=100){
    MouseVector[1]= MouseVector[1]+ Yangle; 
  } else if (Yangle <0 && MouseVector[1]>=1150){
    MouseVector[1]= MouseVector[1]+ Yangle;
  } else {
    MouseVector[1]= MouseVector[1];
  }
  

  if(MouseVector[2]<640 &&  MouseVector[2]>=100  ){
    MouseVector[2]= MouseVector[2]+ Zangle;
  } else if( Zangle >0 && MouseVector[2]<=100){
    MouseVector[2]= MouseVector[2]+ Zangle; 
  } else if (Zangle <0 && MouseVector[2]>=640){
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
///////////////////////////////////////////////////////////////
  // mapping the co ordinate values to usable X,Y cordinates 
  
  if(MouseVector[0]<100){
    MappedX = 0;
  } else if(MouseVector[0]> 2000){
    MappedX = 1915 ;
  } else{
    MappedX = MouseVector[0]-100 ;
  }
  
   if(MouseVector[1]<100){
    MappedY = 0;
  } else if(MouseVector[1]> 1150){
    MappedY = 1050;
  } else{
    MappedY = MouseVector[1]-100 ;
  }

  /////////////////////////////////////////////////////////////////


  Serial.print(" MappedX: ");
  Serial.print(MappedX);
  Serial.print(" MappedY : ");
  Serial.println(MappedY);


  //////////////////////////////////////////

  // Serial.print("Xvalue  : ");
  // Serial.print(MouseVector[0]);
  // Serial.print("\tYvalue : ");
  // Serial.print(MouseVector[1]);
  // Serial.print("\tZvalue  : ");
  // Serial.println(MouseVector[2]);

  //////////////////////////////////////////
  
  Serial.print("Left Click  : ");
  Serial.print(LeftClick);
  Serial.print("\tRight Click : ");
  Serial.print(RightClick);
  Serial.print("\tScroll Click : ");
  Serial.println(ScrollClick);


//  ///////////////////////////////////////////
//
  Serial.print("angleX : ");
  Serial.print(mpu6050.getAngleX());
  Serial.print("\tangleY : ");
  Serial.print(mpu6050.getAngleY());
  Serial.print("\tangleZ : ");
  Serial.println(mpu6050.getAngleZ());

  uint8_t byte1 = MappedX/8;
  uint8_t byte2 = MappedY/8;
  uint8_t byte3 = 0b00000000;

  byte3 |= ScrollClick;
  byte3 <<= 1;
  byte3 |= RightClick;
  byte3 <<= 1;
  byte3 |= LeftClick;
  
  Serial.print("X cord: ");
  Serial.print(byte1);
  Serial.print(" | Y cord: ");
  Serial.print(byte2);
  Serial.print(" | Clicks: ");
  Serial.print(byte3);
  Serial.println("");
  
  // Shift the bytes and create the 32-bit value
  value = 0;
  value |= (uint32_t)byte1 << 24;
  value |= (uint32_t)byte2 << 16;
  value |= (uint32_t)byte3 << 8;

  // value = MouseVector[0];
   // notify changed value
   if (deviceConnected) {
        val_cast = (uint8_t*)&value;
        pCharacteristic->setValue(val_cast, 4);
        pCharacteristic->notify();

        pCharacteristic->setValue((uint8_t*)&value, 4);

        // Get the characteristic value as a byte array
        std::string characteristicValue = pCharacteristic->getValue();
        
        // Print the characteristic value as a byte array
        Serial.print("Value: ");
        Serial.print(value);
        
        Serial.println("");
        Serial.print("Characteristic value: ");
        for (size_t i = 0; i < characteristicValue.length(); i++) {
          Serial.print(characteristicValue[i], HEX);
          Serial.print(" ");
        };
        Serial.println("");
        ////value++;
        
        delay(3); // 


        
    }
    // disconnecting
    if (!deviceConnected && oldDeviceConnected) {
        delay(500); // give the bluetooth stack the chance to get things ready
        pServer->startAdvertising(); // restart advertising
        Serial.println("start advertising");
        oldDeviceConnected = deviceConnected;
    }
    // connecting
    if (deviceConnected && !oldDeviceConnected) {
        // do stuff here on connecting
        oldDeviceConnected = deviceConnected;
    }
    
    delay(400);
}
