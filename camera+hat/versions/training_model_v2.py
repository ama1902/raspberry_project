

import cv2
from picamera2 import Picamera2
import time
import numpy as np
picam2 = Picamera2()
dispW=600
dispH=300
picam2.preview_configuration.main.size = (dispW,dispH)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.controls.FrameRate=30
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()
fps=0
pos=(30,60)
font=cv2.FONT_HERSHEY_SIMPLEX
height=1.5
weight=3
myColor=(0,0,255)

TRAINING =0
MOUSE=1

def onTrack1(val):
    global hueLow
    hueLow=val
    print('Hue Low',hueLow)
def onTrack2(val):
    global hueHigh
    hueHigh=val
    print('Hue High',hueHigh)
def onTrack3(val):
    global satLow
    satLow=val
    print('Sat Low',satLow)
def onTrack4(val):
    global satHigh
    satHigh=val
    print('Sat High',satHigh)
def onTrack5(val):
    global valLow
    valLow=val
    print('Val Low',valLow)
def onTrack6(val):
    global valHigh
    valHigh=val
    print('Val High',valHigh)


def mouse_click(event,x,y,flags,param):
    global value1,value2  # Add this line to access and modify global variables
        
    if event == cv2.EVENT_LBUTTONDOWN:
        hsv_value = frameHSV[y, x]  # OpenCV uses row (y), column (x)
        print(f"HSV value at ({x}, {y}): {hsv_value}")


cv2.namedWindow('myTracker')

cv2.createTrackbar('Hue Low','myTracker',10,179,onTrack1)
cv2.createTrackbar('Hue High','myTracker',20,179,onTrack2)
cv2.createTrackbar('Sat Low','myTracker',100,255,onTrack3)
cv2.createTrackbar('Sat High','myTracker',255,255,onTrack4)
cv2.createTrackbar('Val Low','myTracker',100,255,onTrack5)
cv2.createTrackbar('Val High','myTracker',255,255,onTrack6)

method= TRAINING
while True:
    tStart=time.time()
    frame= picam2.capture_array()
    frame=cv2.flip(frame,-1)

    frameHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    cv2.putText(frame,str(int(fps))+' FPS',pos,font,height,myColor,weight)
    lowerBound=np.array([hueLow,satLow,valLow])
    upperBound=np.array([hueHigh,satHigh,valHigh])
    myMask=cv2.inRange(frameHSV,lowerBound,upperBound)
    myMaskSmall=cv2.resize(myMask,(int(dispW/2),int(dispH/2)))
    myObject=cv2.bitwise_and(frame,frame, mask=myMask)
    myObjectSmall=cv2.resize(myObject,(int(dispW/2),int(dispH/2)))
    if method == MOUSE:
        cv2.setMouseCallback('Camera', mouse_click)


    contours,junk=cv2.findContours(myMask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    if len(contours)>0:
        contours=sorted(contours,key=lambda x:cv2.contourArea(x),reverse=True)
        #cv2.drawContours(frame,contours,-1,(255,0,0),3)
        contour=contours[0]
        x,y,w,h=cv2.boundingRect(contour)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)

    cv2.imshow("Camera", frame)
    cv2.imshow('Mask',myMaskSmall)
    cv2.imshow('My Object',myObjectSmall)
    
    
    key = cv2.waitKey(1)
    if key == ord('q') or key == ord('Q'):
        break
    elif key == ord('m') or key == ord('M'):
        print('mouse mode on')
        method = MOUSE
    elif key == ord('t') or key == ord('T'):
        print('training mode on')
        method = TRAINING

    tEnd=time.time()
    loopTime=tEnd-tStart
    fps=.9*fps + .1*(1/loopTime)
cv2.destroyAllWindows()