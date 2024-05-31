# LiDAR Lib
import Lib_LiDAR as LiDAR

if (__name__ == "__main__"):
    env = LiDAR.libLidar('COM4')
    env.init()
    count = 0

    for scan in env.scanning():
        count += 1
        scan = env.getAngleDistanceRange(scan, 330, 350, 200, 250)
        print('------------------------------------')
        print(scan)
        if count == 100:
            env.stop()
            break
