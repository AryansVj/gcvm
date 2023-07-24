import pygame
import random
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

port = "COM16"
baud_rate = 9600

# ser = serial.Serial(port, baud_rate)
# period = 100

file_name = "trial2_data.txt"
fh = open(file_name)

pygame.init()

WIDTH = 1000
HEIGHT = 600

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Animation")
clock = pygame.time.Clock()

centerX = WIDTH // 2
centerY = HEIGHT // 2

x_data = centerX
y_data = centerY

color = (255, 0, 0)

running = True
end = False
count = 0

while running and end == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    window.fill((0, 0, 0))


    try:
        # data = ser.readline().decode().rstrip()  # Read a line of serial data
        data = fh.readline().rstrip()   # Read a line from text data file
        vals = data.split(" : ")[1:]
        count+=1
        if len(data) < 1:
            end = True

    except:
        continue

    time.sleep(0.01)   
    # Update the position and color of the animated object based on input values
    try: 
        # X-Y Acceleration - Approaches Steady state
        x_data += float(vals[0])*5
        y_data += float(vals[1])*5

        # X-Y Acceleration Angle - Approaches Steady state
        # x_data += float(vals[6])*0.1    
        # y_data += (float(vals[7]))*0.1

        # Gyro acceleration (X-Y)
        # x_data = centerX + float(vals[3])
        # y_data = centerY + float(vals[4])
        
        # Gyro Angles
        # x_data = centerX + float(vals[8])
        # y_data = centerY + float(vals[9])

        # color = (255*(0.5 + float(vals[-1])/2), 250*(float(vals[-3])), 250*(float(vals[-2])))
        # print(vals[8:11])
    except:
        continue

    print("Going to Draw. Count: ", count)

    # Draw the animated object
    pygame.draw.circle(window, color, (x_data, y_data), 10)

    # Update the display
    pygame.display.flip()

    # Control the y_data rate
    clock.tick(60)

    # Quiting Mechanism (Tap all three touches)
    # if int(vals[-3]) == 1 and float(vals[-2]) == 1 and float(vals[-1]) == 1:
    #     running = False

# Quit pygame
pygame.quit()

fh.close()

print('\n')
print("Count ", count)