
import pantilthat
import cv2
from picamera2 import Picamera2
import time
import numpy as np
picam2 = Picamera2()
dispW=400
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
angle=0.5

pan_angle = 0.0# positive going left
tilt_angle = 0.0
pantilthat.pan(pan_angle)
pantilthat.tilt(tilt_angle)


TRAINING =0
MOUSE=1


# Initialize trackbar values
hueLow = 0
hueHigh = 17
satLow = 0
satHigh = 2
valLow = 220
valHigh = 255


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
    global hueLow, hueHigh, satLow, satHigh, valLow, valHigh
    if event == cv2.EVENT_LBUTTONDOWN: #even is clicking left mouse
        hsv_value = frameHSV[y, x]  # extract hsv value
        print(f"HSV value at ({x}, {y}): {hsv_value}")
        hueLow = max(0, hsv_value[0] - 10)
        hueHigh = min(255, hsv_value[0] + 10)
        satLow = max(0, hsv_value[1] - 10)
        satHigh = min(255, hsv_value[1] + 10)
        valLow = max(0, hsv_value[2] - 10)
        valHigh = min(255, hsv_value[2] + 10)

        cv2.setTrackbarPos('Hue Low', 'myTracker', hueLow)
        cv2.setTrackbarPos('Hue High', 'myTracker', hueHigh)
        cv2.setTrackbarPos('Sat Low', 'myTracker', satLow)
        cv2.setTrackbarPos('Sat High', 'myTracker', satHigh)
        cv2.setTrackbarPos('Val Low', 'myTracker', valLow)
        cv2.setTrackbarPos('Val High', 'myTracker', valHigh)


cv2.namedWindow('myTracker')

cv2.createTrackbar('Hue Low','myTracker',1,179,onTrack1)
cv2.createTrackbar('Hue High','myTracker',1,179,onTrack2)
cv2.createTrackbar('Sat Low','myTracker',1,255,onTrack3)
cv2.createTrackbar('Sat High','myTracker',2,255,onTrack4)
cv2.createTrackbar('Val Low','myTracker',200,255,onTrack5)
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
    contours,junk=cv2.findContours(myMask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #conotour function
    if len(contours)>0: # find countors
        contours=sorted(contours,key=lambda x:cv2.contourArea(x),reverse=True) # order from biggest to smallest contour
        #cv2.drawContours(frame,contours,-1,(255,0,0),3)
        contour=contours[0] #select first contour
        x,y,w,h=cv2.boundingRect(contour) # create contour
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3) # draw blue rectangle

        target_x=x+(w/2)
        target_y=y+(h/2)
        error_x = target_x - (dispW/2)
        error_y = target_y - (dispH/2)
        print(f'err_x = {target_x} - {dispW/2} = {error_x}')
        print('---------------------'+f'err_y = {target_y} - {dispH/2} = {error_y}')
        
        if abs(error_x) > 20:

            if error_x < 0: #needs to go left
                pan_angle= pan_angle +angle
                if pan_angle>90:
                    pan_angle=90
                pantilthat.pan(pan_angle)   
            if error_x > 0: #needs to go right
                pan_angle -= angle
                if pan_angle < -90:  # Limit pan angle to min -90
                    pan_angle = -90
                pantilthat.pan(pan_angle)  # Apply the new pan angle
        if abs(error_y) > 20: 
            if error_y > 0: #needs to go down
                tilt_angle += angle
                if tilt_angle > 90:  # Limit tilt angle to max 90
                    tilt_angle = 90
                pantilthat.tilt(tilt_angle)  # Apply the new tilt angle
    
            if error_y < 0: #needs to go up
                tilt_angle -= angle
                if tilt_angle < -90:  # Limit tilt angle to min -90
                    tilt_angle = -90
                pantilthat.tilt(tilt_angle)  # Apply the new tilt angle





    cv2.imshow("Camera", frame)
    cv2.imshow('Mask',myMaskSmall)
    cv2.imshow('My Object',myObjectSmall)
    
    
    key = cv2.waitKey(1)
    if key == ord('q') or key == ord('Q'):
        break
    elif key == ord('m') or key == ord('M'):
        print('extract hsv mode on')
        method = MOUSE
    elif key == ord('t') or key == ord('T'):
        print('training mode on')
        method = TRAINING

    tEnd=time.time()
    loopTime=tEnd-tStart
    fps=0.9*fps + .1*(1/loopTime)
cv2.destroyAllWindows()