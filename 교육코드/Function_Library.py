"""
-------------------------------------------------------------------
  FILE NAME: Function_Library.py
  Copyright: Sungkyunkwan University, Automation Lab.
-------------------------------------------------------------------
  This file is included library class for below subject.
  1) Arduino
  2) LiDAR
  3) Camera
-------------------------------------------------------------------
  Authors: Jonghun Kim, YoungSoo Do, SungBhin Oh, HyeongKeun Hong

  Generated: 2022-11-10
  Revised: 2022-11-18
-------------------------------------------------------------------
  If you find some wrong code, plz contact me(Main Author: Jonghun Kim).
-------------------------------------------------------------------
  You should never modify this file during workshop exercise.
-------------------------------------------------------------------
"""

import sys
import cv2                           # pip install opencv
import time
import serial                        # pip install serial
import numpy as np                   # pip install numpy
import matplotlib.pyplot as plt      # pip install matplotlib
from rplidar import RPLidar          # pip install rplidar-roboticia


np.set_printoptions(threshold=sys.maxsize, linewidth=150)

"""------------------Arduino Variable------------------"""
WAIT_TIME = 2
"""----------------------------------------------------"""


"""-------------------LIDAR Variable-------------------"""
SCAN_TYPE = "normal"
SAMPLE_RATE = 10
MAX_BUFFER_SIZE = 3000
MIN_DISTANCE = 0
"""----------------------------------------------------"""


"""--------------Computer Vision Variable--------------"""
NULL = 0
VARIANCE = 30
SATURATION = 150
FORWARD_THRESHOLD = 0.3
RED, GREEN, BLUE, YELLOW = (0, 1, 2, 3)
FORWARD, LEFT, RIGHT = (0, 1, 2)
COLOR = ("RED", "GREEN", "BLUE", "YELLOW")
DIRECTION = ("FORWARD", "LEFT", "RIGHT")
HUE_THRESHOLD = ([4, 176], [40, 80], [110, 130], [20, 40])
"""-----------------------------------------------------"""


"""
-------------------------------------------------------------------
  CLASS PURPOSE: Arduino Exercise Library
  Author: SungBhin Oh
  Revised: 2022-11-14
-------------------------------------------------------------------
"""
# noinspection PyMethodMayBeStatic
class libARDUINO(object):
    def __init__(self):
        self.port = None
        self.baudrate = None
        self.wait_time = WAIT_TIME  # second unit

    # Arduino Serial USB Port Setting
    def init(self, port, baudrate):
        ser = serial.Serial()
        ser.port, self.port = port, port
        ser.baudrate, self.baudrate = baudrate, baudrate
        ser.open()
        time.sleep(self.wait_time)
        return ser


"""
-------------------------------------------------------------------
  CLASS PURPOSE: LiDAR Sensor Exercise Library
  Author: YoungSoo Do
  Revised: 2022-11-18
-------------------------------------------------------------------
"""
class libLIDAR(object):
    def __init__(self, port):
        self.rpm = 0
        self.lidar = RPLidar(port)
        self.scan = []

    def init(self):
        info = self.lidar.get_info()
        print(info)

    def getState(self):
        health = self.lidar.get_health()
        print(health)

    def scanning(self):
        scan_list = []
        iterator = self.lidar.iter_measures(SCAN_TYPE, MAX_BUFFER_SIZE)
        for new_scan, quality, angle, distance in iterator:
            if new_scan:
                if len(scan_list) > SAMPLE_RATE:
                    np_data = np.array(list(scan_list))
                    yield np_data[:, 1:]
                scan_list = []
            if distance > MIN_DISTANCE:
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


"""
-------------------------------------------------------------------
  CLASS PURPOSE: Camera Sensor Exercise Library
  Author: Jonghun Kim
  Revised: 2022-11-12
-------------------------------------------------------------------
"""
# noinspection PyMethodMayBeStatic
class libCAMERA(object):
    def __init__(self):
        self.capnum = 0
        self.row, self.col, self.dim = (0, 0, 0)

    def loop_break(self):
        if cv2.waitKey(10) & 0xFF == ord('q'):
            print("Camera Reading is ended.")
            return True
        else:
            return False

    def file_read(self, img_path):
        return np.array(cv2.imread(img_path))

    def rgb_conversion(self, img):
        return cv2.cvtColor(img.copy(), cv2.COLOR_BGR2RGB)

    def hsv_conversion(self, img):
        return cv2.cvtColor(img.copy(), cv2.COLOR_BGR2HSV)

    def gray_conversion(self, img):
        return cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)

    def color_extract(self, img, idx):
        result = img.copy()

        for i in range(RED+GREEN+BLUE):
            if i != idx:
                result[:, :, i] = np.zeros([self.row, self.col])

        return result

    def extract_rgb(self, img, print_enable=False):
        self.row, self.col, self.dim = img.shape

        img = self.rgb_conversion(img)

        # Image Color Separating
        img_red = self.color_extract(img, RED)
        img_green = self.color_extract(img, GREEN)
        img_blue = self.color_extract(img, BLUE)

        if print_enable:
            plt.figure(figsize=(12, 4))
            imgset = [img_red, img_green, img_blue]
            imglabel = ["RED", "GREEN", "BLUE"]

            for idx in range(RED+GREEN+BLUE):
                plt.subplot(1, 3, idx + 1)
                plt.xlabel(imglabel[idx])
                plt.imshow(imgset[idx])
            plt.show()

        return img_red[:, :, RED], img_green[:, :, GREEN], img_blue[:, :, BLUE]

    def initial_setting(self, cam0port=0, cam1port=1, capnum=1):
        # OpenCV Initial Setting
        print("OpenCV Version:", cv2.__version__)
        channel0 = None
        channel1 = None
        self.capnum = capnum

        if capnum == 1:
            channel0 = cv2.VideoCapture(cv2.CAP_DSHOW + cam0port)
            if channel0.isOpened():
                print("Camera Channel0 is enabled!")
        elif capnum == 2:
            channel0 = cv2.VideoCapture(cv2.CAP_DSHOW + cam0port)
            if channel0.isOpened():
                print("Camera Channel0 is enabled!")

            channel1 = cv2.VideoCapture(cv2.CAP_DSHOW + cam1port)
            if channel1.isOpened():
                print("Camera Channel1 is enabled!")

        return channel0, channel1

    def camera_read(self, cap1, cap2=None):
        result, capset = [], [cap1, cap2]

        for idx in range(0, self.capnum):
            ret, frame = capset[idx].read()
            result.extend([ret, frame])

        return result

    def image_show(self, frame0, frame1=None):
        if frame1 is None:
            cv2.imshow('frame0', frame0)
        else:
            cv2.imshow('frame0', frame0)
            cv2.imshow('frame1', frame1)

    def color_filtering(self, img, roi=None, print_enable=False):
        self.row, self.col, self.dim = img.shape

        hsv_img = self.hsv_conversion(img)
        h, s, v = cv2.split(hsv_img)

        s_cond = s > SATURATION
        if roi is RED:
            h_cond = (h < HUE_THRESHOLD[roi][0]) | (h > HUE_THRESHOLD[roi][1])
        else:
            h_cond = (h > HUE_THRESHOLD[roi][0]) & (h < HUE_THRESHOLD[roi][1])

        v[~h_cond], v[~s_cond] = 0, 0
        hsv_image = cv2.merge([h, s, v])
        result = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

        if print_enable:
            self.image_show(result)

        return result

    def gaussian_blurring(self, img, kernel_size=(None, None)):
        return cv2.GaussianBlur(img.copy(), kernel_size, 0)

    def canny_edge(self, img, lth, hth):
        return cv2.Canny(img.copy(), lth, hth)

    def histogram_equalization(self, gray):
        return cv2.equalizeHist(gray)

    def hough_transform(self, img, rho=None, theta=None, threshold=None, mll=None, mlg=None, mode="lineP"):
        if mode == "line":
            return cv2.HoughLines(img.copy(), rho, theta, threshold)
        elif mode == "lineP":
            return cv2.HoughLinesP(img.copy(), rho, theta, threshold, lines=np.array([]),
                                   minLineLength=mll, maxLineGap=mlg)
        elif mode == "circle":
            return cv2.HoughCircles(img.copy(), cv2.HOUGH_GRADIENT, dp=1, minDist=80,
                                    param1=200, param2=10, minRadius=40, maxRadius=100)

    def morphology(self, img, kernel_size=(None, None), mode="opening"):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)

        if mode == "opening":
            dst = cv2.erode(img.copy(), kernel)
            return cv2.dilate(dst, kernel)
        elif mode == "closing":
            dst = cv2.dilate(img.copy(), kernel)
            return cv2.erode(dst, kernel)
        elif mode == "gradient":
            return cv2.morphologyEx(img.copy(), cv2.MORPH_GRADIENT, kernel)

    def point_analyze(self, gray, line, point_gap, len_threshold):
        disparity = [0, 0]

        for idx in range(2):
            yplus = line[idx + 1] + point_gap if line[idx + 1] + point_gap < self.row else self.row - 1
            yminus = line[idx + 1] - point_gap if line[idx + 1] - point_gap >= 0 else 0

            if yplus < 0 or yminus >= self.row:
                break
            elif yplus >= self.row or yminus < 0:
                break

            disparity[idx] = np.abs(gray[yplus][line[idx]] - gray[yminus][line[idx]])

        if np.average(disparity) > len_threshold:
            return True
        else:
            return False

    def object_detection(self, img, sample=0, mode="circle", print_enable=False):
        result = None
        replica = img.copy()

        for color in (RED, YELLOW, GREEN):
            extract = self.color_filtering(img, roi=color, print_enable=True)
            gray = self.gray_conversion(extract)
            circles = self.hough_transform(gray, mode=mode)
            if circles is not None:
                for circle in circles[0]:
                    center, count = (int(circle[0]), int(circle[1])), 0

                    hsv_img = self.hsv_conversion(img)
                    h, s, v = cv2.split(hsv_img)

                    # Searching the surrounding pixels
                    for res in range(sample):
                        x, y = int(center[1] - sample / 2), int(center[0] - sample / 2)
                        s_cond = s[x][y] > SATURATION
                        if color is RED:
                            h_cond = (h[x][y] < HUE_THRESHOLD[color][0]) | (h[x][y] > HUE_THRESHOLD[color][1])
                            count += 1 if h_cond and s_cond else count
                        else:
                            h_cond = (h[x][y] > HUE_THRESHOLD[color][0]) & (h[x][y] < HUE_THRESHOLD[color][1])
                            count += 1 if h_cond and s_cond else count

                    if count > sample / 2:
                        result = COLOR[color]
                        cv2.circle(replica, center, int(circle[2]), (0, 0, 255), 2)

        if print_enable:
            if result is not None:
                print("Traffic Light: ", result)
            self.image_show(replica)

        return result

    def edge_detection(self, img, width=0, height=0, gap=0, threshold=0, print_enable=False):
        prediction = None
        replica = img.copy()
        self.row, self.col, self.dim = img.shape

        gray_scale = self.gray_conversion(img)
        hist = self.histogram_equalization(gray_scale)
        dst = self.morphology(hist, (2, 2), mode="opening")

        blurring = self.gaussian_blurring(dst, (5, 5))
        canny = self.canny_edge(blurring, 100, 200)

        lines = self.hough_transform(canny, 1, np.pi/180, 50, 10, 20, mode="lineP")

        if lines is not None:
            new_lines, real_lines = [], []
            for line in lines:
                xa, ya, xb, yb = line[0]

                # x range : 0 ~ self.col / y range : 0 ~ self.row
                if np.abs(yb - ya) > height and np.abs(xb - xa) < width:
                    if self.point_analyze(blurring, line[0], gap, threshold):
                        for idx in range(len(new_lines)):
                            if np.abs(new_lines[:][idx][1] - ya) < VARIANCE:
                                if np.abs(new_lines[:][idx][3] - yb) < VARIANCE:

                                    grad = (xb - xa) / -(yb - ya)  # the third quadrant

                                    if np.abs(grad) < FORWARD_THRESHOLD:
                                        prediction = FORWARD
                                    elif grad > 0:
                                        prediction = RIGHT
                                    elif grad < 0:
                                        prediction = LEFT

                                    # real_lines.append([xa, ya, xb, yb])
                                    cv2.line(replica, (xa, ya), (xb, yb), color=[0, 0, 255], thickness=2)
                        new_lines.append([xa, ya, xb, yb])
            if print_enable:
                if prediction is not None:
                    print("Vehicle Direction: ", DIRECTION[prediction])
                self.image_show(replica)

        return prediction
