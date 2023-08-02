import math
import matplotlib.pyplot as plt
import pygame
import serial

def get_data(mode, handle):
    """Get data from a recorded txt fle"""
    if mode == "txt":
        data = handle.readline().rstrip()
    elif mode == "serial":
        if not handle.readline().decode().strip().startswith(":"):
            return 2
        data = handle.readline().decode().strip()

    vals = data.split(" : ")[1:]
    if len(data) > 0:
        #Accelerometer x,y,z readings 
        accel = [float(vals[0]), float(vals[1]), float(vals[2])]
        #Gyro x,y readings
        gyro = [float(vals[3]), float(vals[4])]

        return (accel, gyro)
    else:
        return 1

def accel_angle(ax, ay, az):
    """
    Get roll and pitch angles in degrees from accelerometer readings using trignometry
    between Accelerometer body frame and world frame
    """

    g = math.sqrt(ax**2 + ay**2 + az**2)
    rad2deg = 180/math.pi
    aroll = math.atan2(ay,az)*rad2deg
    apitch = math.asin(ax/g)*rad2deg

    return (aroll, apitch)

def gyro_angle(roll_prev, pitch_prev, gx, gy, dt):
    """
    Get roll and pitch angles in degrees from gyroscope readings using integration
    """

    groll = roll_prev + gx*dt
    gpitch = pitch_prev + gy*dt

    return (groll, gpitch)

def complimetary_filter(aroll, apitch, groll, gpitch, alpha):
    roll = alpha*aroll + (1-alpha)*groll
    pitch = alpha*apitch + (1-alpha)*gpitch

    return (roll, pitch)

lpf_list = []

def lpf_result(n):
    global lpf_list

    lpf_roll = 0
    lpf_pitch = 0

    for i in range(n):
        lpf_roll += lpf_list[i][0]
        lpf_pitch += lpf_list[i][1]
    
    return (lpf_roll/n, lpf_pitch/n)


def plot_data(angle, time, data, iter, alpha):
    """To Plot the data for deemonstration and observations"""
    
    data_set_roll = [[], [], [], []]
    data_set_pitch = [[], [], [], []]

    for i in range(iter):
        data_set_roll[0].append(data["accel"][i][0])
        data_set_pitch[0].append(data["accel"][i][1])

        data_set_roll[1].append(data["gyro"][i][0])
        data_set_pitch[1].append(data["gyro"][i][1])

        data_set_roll[2].append(data["compl"][i][0])
        data_set_pitch[2].append(data["compl"][i][1])

        data_set_roll[3].append(data["lpf_compl"][i][0])
        data_set_pitch[3].append(data["lpf_compl"][i][1])
    
    if angle == "Roll":
        data = data_set_roll
    else:
        data = data_set_pitch

    plt.plot(time, data[0], 'r-.', label="Accelerometer angle")
    plt.plot(time, data[1], 'g-.', label="Gyroscope angle")
    plt.plot(time, data[2], 'b-.', label="Complementary filtered angle")
    plt.plot(time, data[3], 'k', label="LPF Complementary filtered angle")

    plt.title(f"{angle} angle estimation with complimentary filter (alpha = {alpha})")
    plt.xlabel("time /s")
    plt.ylabel(f"{angle} Angle /deg")
    plt.legend()
    plt.grid(1)

    plt.show()

def main():
    mode = "serial"
    if mode == "txt":
        #Data from txt file
        file_name = "../demo_test/trial2_data.txt"
        handle = open(file_name)
    elif mode == "serial":
        #Data from serial input
        port = "COM16"
        baud_rate = 9600
        handle = serial.Serial(port, baud_rate)

    #Pygame Animation
    window_size = (1000, 600)
    centerX = window_size[0]//2
    centerY = window_size[1]//2
    
    pygame.init()
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("IMU output demonstration")

    clock = pygame.time.Clock()

    running = True

    iter = 0
    time = []
    init_roll = 0
    init_pitch = 0

    roll = init_roll
    pitch = init_pitch
    dt = 0.1
    alpha = 0.05    # Complimentary filter parameter
    n = 10   # LPF moving avg window size

    data = {
        "accel": [],
        "gyro": [],
        "compl": [],
        "lpf_compl": []
    }

    posX_ = centerX
    posY_ = centerY

    posX = centerX
    posY = centerY
    
    aposX = centerX
    aposY = centerY

    gposX = centerX
    gposY = centerY

    while True:

        #Pygame benchmarks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if running == False:
            break

        #To break loop when data file ended
        try:
            (accel, gyro) = get_data(mode, handle)
        except TypeError:
            if get_data(mode, handle) == 2:
                print("Calibrating")
                continue
            elif get_data(mode, handle) == 1:
                break
        (aroll, apitch) = accel_angle(accel[0], accel[1], accel[2])
        (groll, gpitch) = gyro_angle(roll, pitch, gyro[0], gyro[1], dt)

        (roll, pitch) = complimetary_filter(aroll, apitch, groll, gpitch, alpha)
        lpf_list.append((roll, pitch))

        # if not iter < n:
        #     lpf_list.pop(0)
        #     (roll, pitch) = lpf_result(n)

        data["accel"].append((aroll, apitch))
        data["gyro"].append((groll, gpitch))
        data["compl"].append((roll, pitch))
        # data["lpf_compl"].append((roll, pitch))

        print(f"Roll: {roll}, Pitch: {pitch*10}    Count: {iter}")

        time.append(iter*dt)

        #Pygame animation

        # Position via integration (Dead reckoning)
        posX_ = centerX + data["compl"][-1][0]
        posY_ = centerY - data["compl"][-1][1]*10

        # posX += data["lpf_compl"][-1][0]*0.05
        # posY -= data["lpf_compl"][-1][1]*0.05

        aposX = centerX + data["accel"][-1][0]
        aposY = centerY - data["accel"][-1][1]

        gposX = centerX + data["gyro"][-1][0]
        gposY = centerY - data["gyro"][-1][1]

        # Position via derect angle
        # posX_ = centerX + data["compl"][-1][0]
        # posY_ = centerY - data["compl"][-1][1]*10

        # posX = centerX + data["lpf_compl"][-1][0]
        # posY = centerY + data["lpf_compl"][-1][1]

        window.fill((0,0,0))
        pygame.draw.circle(window, (50,50,50), (centerX, centerY), 5)  # Center Reference dot
        pygame.draw.circle(window, (255, 255, 255), (posX_, posY_), 15) 
        # pygame.draw.circle(window, (200,0,0), (aposX, aposY), 10) 
        # pygame.draw.circle(window, (0,200,0), (gposX, gposY), 10) 
        # pygame.draw.circle(window, (255,255,255), (posX, posY), 10)

        pygame.display.flip()
        clock.tick(60)

        iter +=1

    handle.close()

    #plot_data("Pitch", time, data, iter, alpha)
    pygame.quit()

main()