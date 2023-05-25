import asyncio
from bleak import BleakScanner, BleakClient

# UUID of the service and characteristic to interact with
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

async def scan_for_device():
    devices = await BleakScanner.discover()
    if len(devices) == 0:
        print("No Devices found")
        return None
    
    for device in devices:
        if device.name is None:
            print("Device name is None")
            continue

        if "VIRAJ" in device.name:
            print("Device found")
            print(f"Device is {device}")
            return device
    return None

async def interact_with_device(device):
    async with BleakClient(device) as client:
        # Check if the service with the specified UUID is available
        for s in client.services:
            if s.uuid.lower() == SERVICE_UUID.lower():
                service = s
            print("Service Matchd")

            # Check if the characteristic with the specified UUID is available in the service
            if CHARACTERISTIC_UUID.lower() in service.characteristics:
                characteristic = service.characteristics[CHARACTERISTIC_UUID.lower()]
                print("Characteristic Matchd")

                # Enable notifications for the characteristic
                await client.start_notify(characteristic)

                # Receive characteristic value as the device notifies for 10 seconds
                end_time = asyncio.get_event_loop().time() + 10.0
                while asyncio.get_event_loop().time() < end_time:
                    notification = await client.wait_for_notification()
                    value = notification.data
                    print(f"Received value: {value}")

                # Disconnect from the device after 10 seconds
                await client.disconnect()
        else:
            for service in client.services:
                print(service.uuid)
            print("Unmatched Service, Disconnecting")
            await client.disconnect()

async def main():
    print("Discovering...")
    device = await scan_for_device()
    if device:
        await interact_with_device(device)
    else:
        print("ESP32 device not found.")

asyncio.run(main())
