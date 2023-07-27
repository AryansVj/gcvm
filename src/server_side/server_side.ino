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
const int inputPin_1 = 12;
const int inputPin_2 = 13;
const int inputPin_3 = 14;

int LeftClick  = 0;
int RightClick  = 0;
int ScrollClick  = 0;
int MouseVector[2] = {100,100};

int Xangle = 0;
int Yangle = 0;

int MappedX = 0; 
int MappedY = 0;

float centerX = 1000/2;
float centerY = 600/2;

int16_t byte1 = 0;
int16_t byte2 = 0;
int8_t byte3 = 0;

// Bluetooth 
BLEServer* pServer = NULL;
BLECharacteristic* pCharacteristic = NULL;
bool deviceConnected = false;
bool oldDeviceConnected = false;
int32_t value = 0;
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
  
  mpu6050.update();
  int Xangle = mpu6050.getAngleX();
  int Yangle = mpu6050.getAngleY();

  MouseVector[0] = centerX + Xangle;
  MouseVector[1] = centerY + Yangle;
  
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

//
  Serial.print("angleX : ");
  Serial.print(Xangle);
  Serial.print("\tangleY : ");
  Serial.print(Yangle);
  
  byte1 = MouseVector[0];
  byte2 = MouseVector[1];
  byte3 = 0b00000000;

  byte3 |= ScrollClick;
  byte3 <<= 1;
  byte3 |= RightClick;
  byte3 <<= 1;
  byte3 |= LeftClick;
 
  // Shift the bytes and create the 32-bit value
  value = 0;
  value |= (int32_t)byte1 << 18;
  value |= (int32_t)byte2 << 4;
  value |= (int32_t)byte3;

  Serial.println(value);
  
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
    
    delay(100);
}
