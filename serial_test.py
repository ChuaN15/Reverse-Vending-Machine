import serial
import cv2

try:
    ser = serial.Serial('COM7', 9600)
    print ("arduino connected")
except:
    print ("arduino not connected")
    



    