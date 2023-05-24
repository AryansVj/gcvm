#include <BLEPeripheral.h>

// HTS service and characteristic UUIDs
#define HTS_SERVICE_UUID "00001809-0000-1000-8000-00805f9b34fb"
#define TEMPERATURE_CHAR_UUID "00002a1c-0000-1000-8000-00805f9b34fb"

// BLE server and characteristic objects
BLEPeripheral blePeripheral;
BLEService htsService(HTS_SERVICE_UUID);
BLECharacteristic temperatureChar(TEMPERATURE_CHAR_UUID, BLENotify);

void setup() {
  Serial.begin(115200);

  // Initialize the BLEPeripheral library
  blePeripheral.setLocalName("Temperature Server");
  blePeripheral.setAdvertisedServiceUuid(htsService.uuid());
  blePeripheral.addAttribute(htsService);
  blePeripheral.addAttribute(temperatureChar);

  // Set initial temperature characteristic value
  temperatureChar.writeValue(0);

  // Start the BLE server
  blePeripheral.begin();

  Serial.println("BLE server started");
}

void loop() {
  // Generate a random temperature value for demonstration
  int temperature = random(20, 40);

  // Update the temperature characteristic value
  temperatureChar.writeValue(temperature);

  // Notify clients about the updated temperature value
  temperatureChar.notify();

  delay(1000); // Adjust the delay as per your desired update rate
}
