import math
import matplotlib.pyplot as plt

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

def main():
    file_name = "../demo_test/trial1_data.txt"
    fh = open(file_name)

    iter = 0
    time = []
    init_roll = 0
    init_pitch = 0

    roll = init_roll
    pitch = init_pitch
    dt = 0.1
    alpha = 0.1

    data = {
        "accel": [],
        "gyro": [],
        "compl": []
    }
    while True:
        try:
            (accel, gyro) = get_data(fh)
        except TypeError:
            if get_data(fh) == 1:
                break
        (aroll, apitch) = accel_angle(accel[0], accel[1], accel[2])
        (groll, gpitch) = gyro_angle(roll, pitch, gyro[0], gyro[1], dt)

        (roll, pitch) = complimetary_filter(aroll, apitch, groll, gpitch, alpha)

        data["accel"].append((aroll, apitch))
        data["gyro"].append((groll, gpitch))
        data["compl"].append((roll, pitch))

        print(f"Roll: {roll}, Pitch: {pitch}    Count: {iter}")

        time.append(iter)
        iter +=1
    
    plt.plot(time, data["accel"], 'r')
    plt.plot(time, data["gyro"], 'g')
    plt.plot(time, data["compl"], 'k')

    plt.show()

main()