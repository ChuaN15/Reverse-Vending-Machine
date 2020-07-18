import numpy as np
import cv2
import serial
import subprocess
import requests
import json

Quit = 0

try :
    ser = serial.Serial('COM7', 9600)
    ser.flushInput()
    print ("arduino connected")
    
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
    
    #response = requests.get("http://10.105.13.77:8080/smartduskbin/calcitem.php")

    counter = 0
    startCounting = False
    firstDetect = True
    
    ReadyForNext = True
    
    StartButton = True
    previousData = 0
    
    storageCheck = 0
    
    HaveFull = False
    
    while(True):
        if(nextuser == 1):
            if ser.inWaiting() > 0:
                data = ord(ser.read())
                if (data == 49):
                    if (StartButton==True):
                        nextuser = 0
                        ReadOrWrite = 1
			try:
                        	response2 = requests.get("http://10.105.13.77:8080/smartduskbin/inserttask.php")
                        	todos2 = json.loads(response2.text)
			except:
				print("Sorry, not connected to the server")
                        ReadOrWrite = 1
                    elif (StartButton==False):
                        ReadOrWrite = 0
                        
                if (data == 55):
                    #HaveFull = False
                    storageCheck = 1
                
                '''if (data == 54):
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
                
                if (data == 49):
                    if (StartButton==True):
			try:
                        	response2 = requests.get("http://10.105.13.77:8080/smartduskbin/inserttask.php")
                        	todos2 = json.loads(response2.text)
			except:
				print("Sorry, not connected to the server")
                        ReadOrWrite = 1
                    elif (StartButton==False):
                        ReadOrWrite = 0
                            
                if (data == 51):
                    if (not previousData == 51):
                        if (StartButton==True):
			    try:
                            	response2 = requests.get("http://10.105.13.77:8080/smartduskbin/endtask.php")
                            	todos2 = json.loads(response2.text)
			    except:
				print("Sorry, not connected to the server")
                            ReadOrWrite = 1
                            nextuser = 1
                        elif (StartButton==False):
                            ReadOrWrite = 0
                                    
                if (data == 50):
                    ReadyForNext = True
                    isfirst = 0
                
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
                    storageCheck = 2

                previousData = data
                
            # Capture frame-by-frame
            ret, frame = cap.read()
            w1, h1 = frame.shape[:2]

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            diff = cv2.absdiff(original, gray)

            # diff[diff <= 50] = 0
            # diff[diff > 50] = 255

            ret, thresh = cv2.threshold(diff, 50, 255, 0)

            im2, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            if len(contours) > 0:

                M = cv2.moments(im2)

                c = max(contours, key=cv2.contourArea)
                xMax, yMax, wMax, hMax = cv2.boundingRect(c)

                area = cv2.contourArea(c)

                if (area > 10000):
                    print("contour  detected")
                    cv2.drawContours(frame, c, -1, (0, 255, 0), 3)
                    cv2.rectangle(frame, (xMax, yMax), (xMax + wMax, yMax + hMax), (255, 0, 0), 2)
                    # print(M)
                    if (M['m00']):
			approx = cv2.approxPolyDP(c,0.01*cv2.arcLength(c,True),True)
			#approx = 4
                        cx = int(M['m10'] / M['m00'])
                        cy = int(M['m01'] / M['m00'])
                        cv2.circle(frame, (cx, cy), 10, (0, 0, 255), -1)
			if len(approx)==4:
				if (ReadyForNext):
		                        if (ReadOrWrite):
		                            if (firstDetect):
		                                firstDetect = False
		                                startCounting = True
		                                
		                            if (startCounting == True):
		                                counter = counter+1
		                        
				ser.write('k'.encode())
				cv2.putText(frame, "Air Kotak", (cx - 25, cy - 25), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2)
				cv2.putText(frame, str(area), (cx - 50, cy - 50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2)

				if isfirst==0:
					try:
		                        	response2 = requests.get("http://10.105.13.77:8080/smartduskbin/insertitem.php?type=kotak")
		                        	todos2 = json.loads(response2.text)
					except:
						print("Sorry, not connected to the server")
		                        isfirst = 1
				if (counter == 8):
		                        firstDetect = True
		                        startCounting = False
		                        counter = 0
		                        ser.write('1'.encode())
		                        ReadyForNext = False
		                        data = 48
			else:
		                if area > 45000 and area < 65000:
		                    if (ReadyForNext):
		                        if (ReadOrWrite):
		                            if (firstDetect):
		                                firstDetect = False
		                                startCounting = True
		                                
		                            if (startCounting == True):
		                                counter = counter+1
		                        
		                    ser.write('y'.encode())
		                    cv2.putText(frame, "tin", (cx - 25, cy - 25), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2)
		                    cv2.putText(frame, str(area), (cx - 50, cy - 50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2)
		                    if isfirst==0:
					try:
		                        	response2 = requests.get("http://10.105.13.77:8080/smartduskbin/insertitem.php?type=tin")
		                        	todos2 = json.loads(response2.text)
					except:
						print("Sorry, not connected to the server")
		                        isfirst = 1
		                    if (counter == 8):
		                        firstDetect = True
		                        startCounting = False
		                        counter = 0
		                        ser.write('1'.encode())
		                        ReadyForNext = False
		                        data = 48
		                elif area > 65000 and area < 80000:
		                    if (ReadyForNext):
		                        if (ReadOrWrite):
		                            if (firstDetect):
		                                firstDetect = False
		                                startCounting = True
		                                
		                            if (startCounting == True):
		                                counter = counter+1
		                            
		                    ser.write('y'.encode())
		                    cv2.putText(frame, "bottle", (cx - 25, cy - 25), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2)
		                    cv2.putText(frame, str(area), (cx - 50, cy - 50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2)
		                    
		                    if isfirst==0:
					try:
		                        	response2 = requests.get("http://10.105.13.77:8080/smartduskbin/insertitem.php?type=bottle")
		                        	todos2 = json.loads(response2.text)
					except:
						print("Sorry, not connected to the server")
		                        isfirst = 1
		                    if (counter == 8):
		                        firstDetect = True
		                        startCounting = False
		                        counter = 0 
		                        ser.write('0'.encode())
		                        ReadyForNext = False
		                        data = 48
		                else:
		                    firstTimeEver = 1
		                    ser.write('n'.encode())
                    else:
			ser.write('n'.encode())
			cx = 0
			cy = 0
                else:
                    ser.write('n'.encode())
            else:
		ser.write('n'.encode())
		print("Sorry no contours here")

            cv2.imshow('frame', frame)
            # cv2.imshow('a', a)
            # cv2.imshow('blur', blur)
            # cv2.imshow('gray', gray)
            # cv2.imshow('thresh', thresh)

            if cv2.waitKey(1) & 0xFF == ord('q'):
		Quit = 1
            	break

	if (Quit):
		break

    cv2.destroyAllWindows()
	
except:
	print("Arduino not connected!")


