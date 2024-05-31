from rplidar import RPLidar     #pip install rplidar-roboticia
import numpy as np              #pip install numpy

class libLidar(object):
    def __init__(self, port):
        self.rpm = 0
        self.lidar = RPLidar(port)
        self.scan = []

    def init(self):
        info = self.lidar.get_info()
        print(info)
        health = self.lidar.get_health()
        print(health)

    def scanning(self):
        scan_list = []
        iterator = self.lidar.iter_measures('normal', 3000)
        for new_scan, quality, angle, distance in iterator:
            if new_scan:
                if len(scan_list) > 10:
                    np_data = np.array(list(scan_list))
                    yield np_data[:, 1:]
                scan_list = []
            if distance > 0:
                scan_list.append((quality, angle, distance))

    def stop(self):
        self.lidar.stop()
        self.lidar.stop_motor()
        self.lidar.disconnect()

    def setRPM(self, rpm):
        self.lidar.motor_speed = rpm

    def getRPM(self):
        return self.lidar.motor_speed

    def getAngleRange(self, scan, minAngle, maxAngle):
        data = np.array(scan)
        condition = np.where((data[:, 0] < maxAngle) & (data[:, 0] > minAngle))
        return data[condition]

    def getDistanceRange(self, scan, minDist, maxDist):
        data = np.array(scan)
        condition = np.where((data[:, 1] < maxDist) & (data[:, 1] > minDist))
        return data[condition]

    def getAngleDistanceRange(self, scan, minAngle, maxAngle, minDist, maxDist):
        data = np.array(scan)
        condition = np.where((data[:, 0] < maxAngle) & (data[:, 0] > minAngle) & (data[:, 1] < maxDist) & (data[:, 1] > minDist))
        return data[condition]

    def get_far_distance(self, scan, minAngle, maxAngle):
        datas = self.getAngleRange(scan, minAngle, maxAngle)
        max_idx = datas[:, 1].argmax()
        return datas[max_idx]

    def get_near_distance(self, scan, minAngle, maxAngle):
        datas = self.getAngleRange(scan, minAngle, maxAngle)
        min_idx = datas[:, 1].argmin()
        return datas[min_idx]


