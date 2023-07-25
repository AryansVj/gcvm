import math
import matplotlib.pyplot as plt
import pygame

def get_data(fh):
    """Get data from a recorded txt fle"""
    data = fh.readline().rstrip()
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

def plot_data(angle, time, data, alpha):
    """To Plot the data for deemonstration and observations"""

    plt.plot(time, data["accel"], 'r-.', label="Accelerometer angle")
    plt.plot(time, data["gyro"], 'g-.', label="Gyroscope angle")
    plt.plot(time, data["compl"], 'k', label="Complementary filtered angle")

    plt.title(f"{angle} angle estimation with complimentary filter (alpha = {alpha})")
    plt.xlabel("time /s")
    plt.ylabel(f"{angle} Angle /deg")
    plt.legend()
    plt.grid(1)

    plt.show()

def main():
    file_name = "../demo_test/trial2_data.txt"
    fh = open(file_name)

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
    alpha = 0.05

    data = {
        "accel": [],
        "gyro": [],
        "compl": []
    }

    posX = centerX
    posY = centerY

    while True:

        #Pygame benchmarks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if running == False:
            break

        #To break loop when data file ended
        try:
            (accel, gyro) = get_data(fh)
        except TypeError:
            if get_data(fh) == 1:
                break
        (aroll, apitch) = accel_angle(accel[0], accel[1], accel[2])
        (groll, gpitch) = gyro_angle(roll, pitch, gyro[0], gyro[1], dt)

        (roll, pitch) = complimetary_filter(aroll, apitch, groll, gpitch, alpha)

        data["accel"].append((apitch, aroll))
        data["gyro"].append((gpitch, groll))
        data["compl"].append((pitch, roll))

        print(f"Roll: {roll}, Pitch: {pitch}    Count: {iter}")

        time.append(iter*dt)

        #Pygame animation

        #Position via integration (Dead reckoning)
        # posX += data["compl"][-1][0]*0.1
        # posY += data["compl"][-1][1]*0.1

        #Position via derect angle
        posX = centerX + data["compl"][-1][0]
        posY = centerY + data["compl"][-1][1]

        window.fill((0,0,0))
        pygame.draw.circle(window, (50,50,50), (centerX, centerY), 10)
        pygame.draw.circle(window, (255,255,255), (posX, posY), 10)

        pygame.display.flip()
        clock.tick(60)

        iter +=1

    fh.close()

    # plot_data("Pitch", time, data, alpha)
    pygame.quit()

main()