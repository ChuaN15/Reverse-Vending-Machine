import numpy as np
import cv2
import serial
import subprocess
import requests
import json
import time
import random

Quit = 0

try:
    ser = serial.Serial('COM7', 9600)
    ser.flushInput()
    print ("arduino connected")

    time.sleep(5)

    cap = cv2.VideoCapture(0)

    i = 0
    fistTime = 0
    isfirst = 0
    nextuser = 0

    while (True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        if i < 10:
            i = i + 1
        elif i >= 10:
            if fistTime == 0:
                cv2.imwrite('image.png', frame)
                firstTime = 1
                break

    # When everything done, release the capture
    cap.release()

    original = cv2.imread('image.png', 0)
    w, h = original.shape[:2]
    print(w, h)

    cap = cv2.VideoCapture(0)

    ReadOrWrite = 1

    # response = requests.get("http://10.105.13.77:8080/smartduskbin/calcitem.php")

    counter = 0
    startCounting = False

    firstDetect = True

    ReadyForNext = True

    previousData = 0

    storageCheck = 0

    HaveFull = False

    currentItem = 0
    previousItem = 0

    counterForNextProcess = 0
    startCountingForProcess = False

    # time.sleep(10)

    while(True):
        '''if(nextuser == 1):
            if ser.inWaiting() > 0:
                data = ord(ser.read())

                if (data == 55):
                    #HaveFull = False
                    storageCheck = 1

                if (data == 54):
                    try:
                        if(previousData != 54):
                            #HaveFull = True
                            response2 = requests.get("http://192.168.43.10:50016/home/inventoryfull")
                            todos2 = json.loads(response2.text)
                    except:
                        print ("email error.")
                    storageCheck = 2'''

        while (nextuser == 0):
            area = 0

            '''try:
                response = requests.get("http://192.168.43.10:8080/smartduskbin/calcitem.php")
                todos = json.loads(response.text)
                print (todos)
                if "rue" in response.text:
                    ReadOrWrite = 1
                    print("same")
                else:
                    ReadOrWrite = 0
                    print("not same")
            except:
                print ("Failed to connect to server")'''

            if ser.inWaiting() > 0:
                data = ord(ser.read())
                #print(data)

                '''if (data == 113): # q
                    print "q receive"
                    try:
                        response = requests.get("http://192.168.43.10:8080/smartduskbin/UpdateInventory.php?Type=Bottle&Level=0")
                    except:
                        print ("Failed to connect to server")

                if (data == 119): # w
                    print "w receive"
                    try:
                        response = requests.get("http://192.168.43.10:8080/smartduskbin/UpdateInventory.php?Type=Bottle&Level=1")
                    except:
                        print ("Failed to connect to server")

                if (data == 101): # e
                    print "e receive"
                    try:
                        response2 = requests.get("http://localhost:50016/Home/inventoryfull")
                        response = requests.get("http://192.168.43.10:8080/smartduskbin/UpdateInventory.php?Type=Bottle&Level=2")
                    except:
                        print ("Failed to connect to server")

                if (data == 97): # a
                    print "a receive"
                    try:
                        response = requests.get("http://192.168.43.10:8080/smartduskbin/UpdateInventory.php?Type=Can&Level=0")
                    except:
                        print ("Failed to connect to server")

                if (data == 115): # s
                    print "s receive"
                    try:
                        response = requests.get("http://192.168.43.10:8080/smartduskbin/UpdateInventory.php?Type=Can&Level=1")
                    except:
                        print ("Failed to connect to server")

                if (data == 100): # d
                    print "d receive"
                    try:
                        response2 = requests.get("http://localhost:50016/Home/inventoryfull")
                        response = requests.get("http://192.168.43.10:8080/smartduskbin/UpdateInventory.php?Type=Can&Level=2")
                    except:
                        print ("Failed to connect to server")

                if (data == 122): # z
                    print "z receive"
                    try:
                        response = requests.get("http://192.168.43.10:8080/smartduskbin/UpdateInventory.php?Type=Box&Level=0")
                    except:
                        print ("Failed to connect to server")

                if (data == 120): # x
                    print "x receive"
                    try:
                        response = requests.get("http://192.168.43.10:8080/smartduskbin/UpdateInventory.php?Type=Box&Level=1")
                    except:
                        print ("Failed to connect to server")

                if (data == 99): # c
                    print "c receive"
                    try:
                        response2 = requests.get("http://localhost:50016/Home/inventoryfull")
                        response = requests.get("http://192.168.43.10:8080/smartduskbin/UpdateInventory.php?Type=Box&Level=2")
                    except:
                        print ("Failed to connect to server")'''

                if (data == 50):  #receive data if the first process has been complete
                    ReadyForNext = True
                    isfirst = 0
                    # print ("123")

                if (data == 52):
                    ReadyForNext = False
                    isfirst = 1

                if (data == 55):
                    #HaveFull = False
                    storageCheck = 1

                if (data == 54):  #receive data if the storage has been full
                    try:
                        if(previousData != 54):
                            #HaveFull = True
                            response2 = requests.get("http://localhost:50016/Home/inventoryfull")
                            todos2 = json.loads(response2.text)
                    except:
                        print ("email error.")
                    storageCheck = 2

                data = 0;
                previousData = data

            # Capture frame-by-frame
            ret, frame = cap.read()
            w1, h1 = frame.shape[:2]

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # gray = cv2.GaussianBlur(gray, (21, 21), 0)
            diff = cv2.absdiff(gray, original)

            # diff[diff <= 50] = 0
            # diff[diff > 50] = 255

            ret, thresh = cv2.threshold(diff, 12, 255, 0)

            im2, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # print ReadyForNext

            '''if (startCountingForProcess):
                if (counterForNextProcess > 500):
                    print("okayyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
                    startCountingForProcess = False
                    counterForNextProcess = 0
                else:
                    counterForNextProcess += 1'''

            if len(contours) > 0:

                M = cv2.moments(im2)

                c = max(contours, key=cv2.contourArea)
                xMax, yMax, wMax, hMax = cv2.boundingRect(c)

                area = cv2.contourArea(c)
                # area = (abs(xMax + wMax) - xMax) * (abs(yMax + hMax) - yMax)

                if (area > 600):
                    # print("contour  detected")
                    # cv2.drawContours(frame, c, -1, (0, 255, 0), 3)
                    # cv2.rectangle(frame, (xMax, yMax), (xMax + wMax, yMax + hMax), (255, 0, 0), 2)
                    # print(M)

                    if (M['m00']):
                        approx = cv2.approxPolyDP(c,0.01*cv2.arcLength(c,True),True)
                        #approx = 4
                        cx = int(M['m10'] / M['m00'])
                        cy = int(M['m01'] / M['m00'])
                        cv2.circle(frame, (cx, cy), 10, (0, 0, 255), -1)

                        # cv2.putText(frame, str(area), (cx - 50, cy - 50), cv2.FONT_HERSHEY_COMPLEX, 0.5,(255, 255, 255), 2)

                        if area > 13000 and area < 38000:
                            # if (not startCountingForProcess):
                            #         ReadyForNext = True

                            ReadyForNext = True

                            if (firstDetect):
                                firstDetect = False
                                startCounting = True

                            if (startCounting == True):
                                if (previousItem == currentItem):
                                    counter = counter + 1
                                else:
                                    counter = 0

                            ser.write('k'.encode())
                            ser.flush()
                            cv2.putText(frame, "Air Kotak", (cx - 25, cy - 25), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2)
                            cv2.putText(frame, str(area), (cx - 50, cy - 50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2)
                            previousItem = currentItem

                            if (counter >= 80):
                                # print "kotak detected uollss"
                                try:
                                    response2 = requests.get("http://192.168.43.10:8080/smartduskbin/insertitem.php?type=box")
                                except:
                                    print("Sorry, not connected to the server")


                                firstDetect = True
                                startCounting = False
                                # startCountingForProcess = True
                                counter = 0
                                ser.write('2'.encode())
                                ser.flush()
                                ReadyForNext = False
                                data = 0
                                isfirst = 0
                                time.sleep(6)

                        elif area > 8000 and area < 13000:
                    

                            ReadyForNext = True

                            if (firstDetect):
                                firstDetect = False
                                startCounting = True

                            if (startCounting == True):
                                if (previousItem == currentItem):
                                    counter = counter+1
                                else:
                                    counter = 0

                            ser.write('y'.encode())
                            ser.flush()
                            cv2.putText(frame, "tin", (cx - 25, cy - 25), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2)
                            cv2.putText(frame, str(area), (cx - 50, cy - 50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2)
                            previousItem = currentItem

                            if (counter >= 80):
                                # print "tin detected uollss"

                                try:
                                    response2 = requests.get("http://192.168.43.10:8080/smartduskbin/insertitem.php?type=tin")
                                except:
                                    print("Sorry, not connected to the server")


                                firstDetect = True
                                startCounting = False
                                # startCountingForProcess = True
                                counter = 0
                                ser.write('1'.encode())
                                ser.flush()
                                ReadyForNext = False
                                data = 0
                                isfirst = 0
                                time.sleep(6)

                        elif area > 900 and area < 8000:

                            if (firstDetect):
                                firstDetect = False
                                startCounting = True


                            if (startCounting == True):
                                if (previousItem == currentItem):
                                    counter = counter + 1
                                else:
                                    counter = 0

                            ser.write('y'.encode())
                            ser.flush()
                            cv2.putText(frame, "bottle", (cx - 25, cy - 25), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2)
                            # cv2.putText(frame, random.randrange(65,98), (cx - 50, cy - 50), cv2.FONT_HERSHEY_COMPLEX, 0.5,(255, 255, 255), 2)
                            cv2.putText(frame, str(area), (cx - 50, cy - 50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2)
                            previousItem = currentItem
                            if (counter >= 60):
                                # print "bottle detected uollss"

                                try:
                                    response2 = requests.get("http://192.168.43.10:8080/smartduskbin/insertitem.php?type=bottle")
                                    todos2 = json.loads(response2.text)
                                except:
                                    print("Sorry, not connected to the server")


                                firstDetect = True
                                startCounting = False
                                # startCountingForProcess = True
                                counter = 0
                                ser.write('0'.encode())
                                ser.flush()
                                ReadyForNext = False
                                data = 0
                                time.sleep(6)

                        else:
                            previousItem = 0
                            currentItem = 0
                            ser.write('n'.encode())
                            ser.flush()

                    else:
                        ser.write('n'.encode())
                        ser.flush()
                        previousItem = 0
                        currentItem = 0
                        cx = 0
                        cy = 0
                else:
                    ser.write('n'.encode())
                    ser.flush()
            else:
                ser.write('n'.encode())
                ser.flush()
                # print("Sorry no contours here")

            cv2.imshow('frame', frame)
            # cv2.imshow('a', a)
            # cv2.imshow('blur', blur)
            # cv2.imshow('diff', diff)
            cv2.imshow('thresh', thresh)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                Quit = 1
                break

        if (Quit):
            break

    cv2.destroyAllWindows()

except:
    print("Arduino not connected!")


