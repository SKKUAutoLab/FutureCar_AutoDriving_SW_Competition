# LiDAR Lib
import Lib_LiDAR as LiDAR

if (__name__ == "__main__"):
    env = LiDAR.libLidar('COM4')
    env.init()
    count = 0

    for scan in env.scanning():

        scan = env.getAngleDistanceRange(scan, 330, 350, 200, 250)

        if len(scan) > 0:
            print(scan)
            print('stop')
            env.stop()
            break
        else:
            print('go')
        if count == 600:
            env.stop()
            break

        count += 1