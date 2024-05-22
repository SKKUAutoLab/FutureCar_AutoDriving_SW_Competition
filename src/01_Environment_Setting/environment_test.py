from rplidar import RPLidar
import cv2
import serial
import time


ser = serial.Serial()
ser.port = 'COM7'            #for window #장치관리자 -> 포트확인
ser.baudrate = 9600
ser.open()
time.sleep(2)

print(cv2.__version__)
cap1 = cv2.VideoCapture(cv2.CAP_DSHOW)
print(cap1.isOpened())

lidar = RPLidar('COM6')
info = lidar.get_info()
print(info)
health = lidar.get_health()
print(health)

