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

x_data = [centerX, centerX, centerX, centerX]
y_data = [centerY, centerY, centerY, centerY]

color = (255, 0, 0)

running = True
end = False
count = 0
acc = []
accAng = []
gyroAcc = []
gyroAng = []

lpf_n = 4

def lpf(avg_lst:list, element, iter, n):
    """Using moving average"""

    lpf_res = 0
    for i in range(n):
        lpf_res += avg_lst[iter - i][element]

    return lpf_res/n

def hpf(old_val, hpf_lst:list, element, iter):
    hpf_res = old_val
    hpf_res += hpf_lst[iter][element] - hpf_lst[iter-1][element]

    return hpf_res

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
        if len(data) < 1:
            end = True
    except:
        continue

    time.sleep(0.01)   
    # Update the position and color of the animated object based on input values
    try: 
        # X-Y Acceleration - Approaches Steady state
        y_data[0] = centerY - float(vals[0])*50
        x_data[0] = centerX + float(vals[1])*50

        # X-Y Acceleration Angle - Approaches Steady state
        x_data[1] = centerX + float(vals[6])    
        y_data[1] = centerY + (float(vals[7]))

        # Gyro acceleration (X-Y)
        # x_data[2] += float(vals[3])*0.5
        # y_data[2] += float(vals[4])*0.5
        
        # Gyro Angles
        x_data[3] = centerX + float(vals[8])
        y_data[3] = centerY + float(vals[9])

        # color = (255*(0.5 + float(vals[-1])/2), 250*(float(vals[-3])), 250*(float(vals[-2])))
        # print(vals[8:11])
    except:
        continue

    print(x_data, y_data, "Count: ", count)

    acc.append((x_data[0], y_data[0]))
    accAng.append((x_data[1], y_data[1]))
    gyroAcc.append((float(vals[3]), float(vals[4])))
    gyroAng.append((x_data[3], y_data[3]))

    # Draw the animated object
    if count < lpf_n:
        x_data[2] = centerX
        y_data[2] = centerY
        pass
    else:
        #Low pass values
        x_data[0] = lpf(acc, 0, count, lpf_n)
        y_data[0] = lpf(acc, 1, count, lpf_n)
        
        x_data[1] = lpf(accAng, 0, count, lpf_n)
        y_data[1] = lpf(accAng, 1, count, lpf_n)

        x_data[3] = lpf(gyroAng, 0, count, lpf_n)
        y_data[3] = lpf(gyroAng, 1, count, lpf_n)

        #High pass values
        x_data[2] = hpf(x_data[2], gyroAcc, 0, count)
        y_data[2] = hpf(y_data[2], gyroAcc, 1, count)

    x = x_data[0]*0.55 + x_data[1]*0.1 + x_data[2]*0.05 + x_data[3]*0.2
    y = y_data[0]*0.55 + y_data[1]*0.1 + y_data[2]*0.05 + y_data[3]*0.2
        
    pygame.draw.circle(window, (255, 255, 255), (x, y), 10)

    pygame.draw.circle(window, (100, 0, 0), (x_data[0], y_data[0]), 10)
    pygame.draw.circle(window, (0, 100, 0), (x_data[1], y_data[1]), 10)
    pygame.draw.circle(window, (100, 100, 100), (x_data[2], y_data[2]), 10)
    pygame.draw.circle(window, (0, 0, 100), (x_data[3], y_data[3]), 10)

    # Update the display
    pygame.display.flip()

    # Control the y_data rate
    clock.tick(60)

    # Quiting Mechanism (Tap all three touches)
    # if int(vals[-3]) == 1 and float(vals[-2]) == 1 and float(vals[-1]) == 1:
    #     running = False

    count+=1

# Quit pygame
pygame.quit()

fh.close()

print('\n')
print("Count ", count)