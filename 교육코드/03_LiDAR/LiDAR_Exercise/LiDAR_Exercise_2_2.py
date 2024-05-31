# LiDAR Lib
import Lib_LiDAR as LiDAR

if (__name__ == "__main__"):
    env = LiDAR.libLidar('COM4')
    env.init()
    count = 0

    for scan in env.scanning():
        count += 1
        scan = env.getDistanceRange(scan, 150, 300)
        print('------------------------------------')
        print(scan)
        if count == 200:
            env.stop()
            break
