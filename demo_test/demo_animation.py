import pygame
import random
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import sleep

port = "COM16"
baud_rate = 9600

ser = serial.Serial(port, baud_rate)
period = 100

pygame.init()

WIDTH = 800
HEIGHT = 600

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Animation")
clock = pygame.time.Clock()

x_data = WIDTH // 2
y_data = HEIGHT // 2
color = (255, 0, 0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    window.fill((0, 0, 0))

    try:
        data = ser.readline().decode().rstrip()  # Read a line of serial data
        vals = data.split(" : ")
    except:
        continue

    # Update the position and color of the animated object based on input values
    try: 
        x_data += float(vals[0])*20    
        y_data += float(vals[1])*20
        color = (120, 250*(float(vals[3])), 250*(float(vals[4])))
        print(vals)
    except:
        continue

    # Draw the animated object
    pygame.draw.circle(window, color, (x_data, y_data), 10)

    # Update the display
    pygame.display.flip()

    # Control the y_data rate
    clock.tick(60)

# Quit pygame
pygame.quit()