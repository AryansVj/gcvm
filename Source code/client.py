import asyncio
from bleak import BleakScanner, BleakClient
from pynput.mouse import Button,Controller
import pyautogui as pg
import pygame
import struct
import tkinter as tk

# UUID of the service and characteristic to interact with
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

#variables
rigthbutton = 0
leftbutton = 0
x = 100
y = 100
scroll =0
scrolllength =0
fh = open("demo_test/recdata.txt", "w")

#Pygame Animation

root = tk.Tk()
window_size = (root.winfo_screenwidth(), root.winfo_screenheight())
root.destroy()  # Close the temporary tkinter window

centerX = window_size[0]//2
centerY = window_size[1]//2

Xval = 0
Yval = 0

# pygame.init()
# window = pygame.display.set_mode(window_size)
# pygame.display.set_caption("IMU output demonstration")

# clock = pygame.time.Clock()

running = True

# Discovering and finding the device
async def scan_for_device():
    devices = await BleakScanner.discover()
    if len(devices) == 0:
        print("No Devices found")
        return None
    
    for device in devices:
        if device.name is None:
            print("Device name is None")
            continue

        if "GCVM_Server" in device.name:
            print("Device found")
            print(f"Device is {device}")
            return device
    return None

# Callback function to handle data received by notifications
def notification_callback(sender: int, data: bytearray,):
    global Xval
    global Yval
    # feed = data.decode()
    feed = struct.unpack('<i', data)[0]
    # feed_int = int(feed, 16)
    feed_bin = bin(feed)

    # print(f"Notification received {feed}")
    # print(data)
    click_byte = feed & 15
    x_byte = ((feed >> 4) & 16383) - 500
    y_byte = ((feed >> 18) & 16383) - 500  # Masking and bit shifting

    y_bits = bin(y_byte)
    x_bits = bin(x_byte)

    # Logging  
    fh.write(f"{data}   {feed}    {feed_bin}    {x_byte}    {y_byte}        {click_byte} \n")
    
    print(f"Received {feed}")

    correction_offset = 655    # Two's compliment correction offset. Decimal equivalant of -1

    Xval += x_byte*0.1
    Yval += y_byte*0.1 -10
    
    print(f"{data}   {feed}    {x_byte}  - {Xval}     {y_byte}  -  {Yval}    {click_byte}")

    mouse = Controller()
    mouse.position = ((Xval, Yval))

    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         running = False

    #     if running == False:
    #         break
    
    # window.fill((0,0,0))
    # pygame.draw.circle(window, (255,255,255), (Xval, Yval), 10)
    
    # pygame.display.flip()
    # clock.tick(60)

    if(click_byte < 4):
        # click the mouse
        time = 1         # time the button clicks
        if(click_byte == 2):
            mouse.click(Button.right, time)
        elif(click_byte == 1):
            mouse.click(Button.left, time)

    elif(click_byte == 4):
        scrolllength = x
        pg.scroll(-1*(Yval*0.5))

    time_count = 0

    while time_count < 10:
        #take the position of the mouse
        pos = mouse.position
        # print(pos)
        
        time_count += 1
                

async def interact_with_device(device):
    async with BleakClient(device) as client:
        # Check if the service with the specified UUID is available
        service = None
        for s in client.services:
            if s.uuid.lower() == SERVICE_UUID.lower():
                service = s
                print("Service Matchd")
                break
            
        if service is None:
            await client.disconnect()
            print("No matching service found. Client Disconnected")
        
        else:
            # Check if the characteristic with the specified UUID is available in the service
            for c in service.characteristics:
                if c.uuid.lower() == CHARACTERISTIC_UUID.lower():
                    characteristic = c
                    print("Characteristic Matchd")

                # Enable notifications for the characteristic
                await client.start_notify(characteristic, notification_callback)

                # Receive characteristic value as the device notifies for 10 seconds
                time_count = 0
                while time_count < 60:
                    await asyncio.sleep(1)
                    time_count += 1

                # Disconnect from the device after 10 seconds
                await client.disconnect()
                print("Client Disconnected")

async def main():
    count = 0
    timeout = 5
    print("Discovering...")
    device = await scan_for_device()
    if device:
        while True:
            try:
                await interact_with_device(device)
            except:
                if count < timeout:
                    count +=1
                    print(f"Attempt {count} failed. Retrying...")
                    continue
                else:
                    print("TIMEOUT. Connection Failed.")
                    break
    else:
        print("ESP32 device not found.")

asyncio.run(main())

fh.close()
# pygame.quit()

# is this edit was in my branch