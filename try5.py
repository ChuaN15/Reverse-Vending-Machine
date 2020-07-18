import numpy as np
import cv2
import serial
import subprocess
import requests
import json

dev=subprocess.check_output("ls/dev/ttyUSB*",shell=True)
#print(dev.strip().decode('ascii'))#convertbinarytostring
ser=serial.Serial(dev.strip().decode('ascii'),9600)
ser.flushInput()
print("arduinoconnected")

cap=cv2.VideoCapture(0)

i=0
fistTime=0
isfirst=0

while(True):
#Captureframe-by-frame
    ret,frame=cap.read()

    ifi<10:
    i=i+1
    elifi>=10:
    iffistTime==0:
    cv2.imwrite('image.png',frame)
    firstTime=1
break

    #Wheneverythingdone,releasethecapture
    cap.release()

    original=cv2.imread('image.png',0)
    w,h=original.shape[:2]
    print(w,h)

    cap=cv2.VideoCapture(0)

    ReadOrWrite=0

    response=requests.get("http://192.168.43.10:8080/smartduskbin/calcitem.php")

    #acceptNext=1

    firstTimeEver=1
    counter=0

    while(True):
    area=0
    if(ReadOrWrite==0):
    try:
    response=requests.get("http://192.168.43.10:8080/smartduskbin/calcitem.php")
    todos=json.loads(response.text)
    print(todos)
    if"rue"inresponse.text:
    ReadOrWrite=1
    print("same")
    else:
    ReadOrWrite=0
    print("notsame")
    except:
    print("Failedtoconnecttoserver")

    '''ifser.inWaiting()>0:
    data=ord(ser.read())
    #print(data)
    if(data==49):
    acceptNext=1
    else:
    acceptNext=0'''


    #Captureframe-by-frame
    ret,frame=cap.read()
    w1,h1=frame.shape[:2]

    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)
    diff=cv2.absdiff(original,gray)

    #diff[diff<=50]=0
    #diff[diff>50]=255

    ret,thresh=cv2.threshold(diff,50,255,0)

    im2,contours,hierarchy=cv2.findContours(thresh.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    iflen(contours)>0:

    M=cv2.moments(im2)

    c=max(contours,key=cv2.contourArea)
    xMax,yMax,wMax,hMax=cv2.boundingRect(c)

    area=cv2.contourArea(c)

    if(area>10000):
    print("contourdetected")
    cv2.drawContours(frame,c,-1,(0,255,0),3)
    cv2.rectangle(frame,(xMax,yMax),(xMax+wMax,yMax+hMax),(255,0,0),2)
    #print(M)
    if(M['m00']):
    cx=int(M['m10']/M['m00'])
    cy=int(M['m01']/M['m00'])
    cv2.circle(frame,(cx,cy),10,(0,0,255),-1)
    ifarea>45000andarea<65000:
    counter=counter+1
    ser.write('y'.encode())
    cv2.putText(frame,"tin",(cx-25,cy-25),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),2)
    cv2.putText(frame,str(area),(cx-50,cy-50),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),2)
    ifisfirst==0:
    response2=requests.get("http://192.168.43.10:8080/smartduskbin/insert.php?type=tin")
    todos2=json.loads(response2.text)
    isfirst=1
    ifReadOrWrite==1:
    if"rue"inresponse.text:
    ser.write('1'.encode())
    ReadOrWrite=0
    #data=48
    #time.sleep(1)
    elifarea>65000andarea<80000:
    #counter=counter+1
    ser.write('y'.encode())
    cv2.putText(frame,"bottle",(cx-25,cy-25),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),2)
    cv2.putText(frame,str(area),(cx-50,cy-50),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),2)

    '''ifisfirst==0:
    response2=requests.get("http://192.168.43.10:8080/smartduskbin/insert.php?type=bottle")
    todos2=json.loads(response2.text)
    isfirst=1'''

    ifReadOrWrite==1:
    #ifcounter==300:
    iffirstTimeEver==1:
    ser.write('0'.encode())
    firstTimeEver=0

    #acceptNext=0
    ReadOrWrite=0
    data=48
    counter=0
    #time.sleep(1)
    print("botol")
    else:
    #firstTimeEver=1
    ser.write('n'.encode())
    else:
    ser.write('n'.encode())
    cx=0
    cy=0
    else:
    ser.write('n'.encode())
    else:
    ser.write('n'.encode())
    print("Sorrynocontourshere")

    cv2.imshow('frame',frame)
    #cv2.imshow('a',a)
    #cv2.imshow('blur',blur)
    #cv2.imshow('gray',gray)
    #cv2.imshow('thresh',thresh)
    ifcv2.waitKey(1)&0xFF==ord('q'):
    break

    cv2.waitKey(0)
    cv2.destroyAllWindows()
