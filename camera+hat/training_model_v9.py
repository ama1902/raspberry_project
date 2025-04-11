import pantilthat
import cv2
from picamera2 import Picamera2
import time
import numpy as np
import serial
import time

ser = serial.Serial("/dev/ttyS0", 115200)
lidar_distance='x'
picam2 = Picamera2()
dispW=800
dispH=600
picam2.preview_configuration.main.size = (dispW,dispH)
picam2.preview_configuration.main.format = "BGR888"
picam2.preview_configuration.controls.FrameRate=30
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()
fps=0
pos=(30,60)
pos2=(30,30)
font=cv2.FONT_HERSHEY_SIMPLEX
height=0.5
height2=1
weight=2
myColor=(0,0,255)
angle=0.5
pan_angle = 0.0
# positive going left
tilt_angle = 0.0
pantilthat.pan(pan_angle)
pantilthat.tilt(tilt_angle)

#PID
kp=0.1
ki=0
kd=0
prev_error_x, prev_error_y, prev_i_x, prev_i_y = 0, 0, 0, 0
integral_x = 0
integral_y = 0
prev_time = time.time()
max_speed = 5 


TRAINING =0
MOUSE=1
STEADY=2
PID =3

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
        #print(f"HSV value at ({x}, {y}): {hsv_value}")
        a=20
        hueLow = max(0, hsv_value[0] - a)
        hueHigh = min(255, hsv_value[0] + a)
        satLow = max(0, hsv_value[1] - a)
        satHigh = min(255, hsv_value[1] + a)
        valLow = max(0, hsv_value[2] - a)
        valHigh = min(255, hsv_value[2] + a)

        cv2.setTrackbarPos('Hue Low', 'myTracker', hueLow)
        cv2.setTrackbarPos('Hue High', 'myTracker', hueHigh)
        cv2.setTrackbarPos('Sat Low', 'myTracker', satLow)
        cv2.setTrackbarPos('Sat High', 'myTracker', satHigh)
        cv2.setTrackbarPos('Val Low', 'myTracker', valLow)
        cv2.setTrackbarPos('Val High', 'myTracker', valHigh)


cv2.namedWindow('myTracker')
cv2.moveWindow("My tracker", 650, 500)
cv2.createTrackbar('Hue Low','myTracker',1,179,onTrack1)
cv2.createTrackbar('Hue High','myTracker',1,179,onTrack2)
cv2.createTrackbar('Sat Low','myTracker',1,255,onTrack3)
cv2.createTrackbar('Sat High','myTracker',2,255,onTrack4)
cv2.createTrackbar('Val Low','myTracker',200,255,onTrack5)
cv2.createTrackbar('Val High','myTracker',255,255,onTrack6)


def pid(error, prev_error, integral, dt):
    """ Computes PID output as velocity instead of direct position """
    p = kp * error
    integral += error * dt  # Accumulate integral error
    i = ki * integral
    d = kd * ((error - prev_error) / dt) if dt > 0 else 0
    output = p + i + d
    return output, error, integral


def onTrackpid1(val):
    global kp
    kp = val / 100
    print('Kp:', kp)

def onTrackpid2(val):
    global ki
    ki = val / 1000
    print('Ki:', ki)

def onTrackpid3(val):
    global kd
    kd = val / 1000
    print('Kd:', kd)

cv2.namedWindow('PID_tuning')
cv2.createTrackbar('Kp', 'PID_tuning', 0, 1000, onTrackpid1)
cv2.createTrackbar('Ki', 'PID_tuning', 0, 100, onTrackpid2)
cv2.createTrackbar('Kd', 'PID_tuning', 0, 1000, onTrackpid3)

if ser.isOpen() == False:
    ser.open()


method= TRAINING
training_method = STEADY
while True:
    #------------------------------------------------
    counter = ser.in_waiting # count the number of bytes of the serial port
    if counter > 8:
        bytes_serial = ser.read(9)
        ser.reset_input_buffer()
        
        if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59: # python3
            distance = bytes_serial[2] + bytes_serial[3]*256
            strength = bytes_serial[4] + bytes_serial[5]*256
            temperature = bytes_serial[6] + bytes_serial[7]*256 # For TFLuna
            temperature = (temperature/8) - 256
            lidar_distance="D:"+ str(distance) + "cm S:" + str(strength)
            if temperature != 0:
                lidar_distance="D:"+ str(distance) + "cm S:" + str(strength) + " CT:" + str(temperature)+ "℃"
            
            ser.reset_input_buffer()
    #-----------------------------------------------
    tStart=time.time()
    frame= picam2.capture_array()
    frame=cv2.flip(frame,-1)

    frameHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    cv2.putText(frame,str(int(fps))+' FPS',pos,font,height,myColor,weight)
    cv2.putText(frame,lidar_distance,pos2,font,height2,myColor,weight)
    lowerBound=np.array([hueLow,satLow,valLow])
    upperBound=np.array([hueHigh,satHigh,valHigh])

    myMask=cv2.inRange(frameHSV,lowerBound,upperBound)
    myMaskSmall=cv2.resize(myMask,(int(dispW/2),int(dispH/2)))
    myObject=cv2.bitwise_and(frame,frame, mask=myMask)
    myObjectSmall=cv2.resize(myObject,(int(dispW/2),int(dispH/2)))
    #if method == MOUSE:
        #cv2.setMouseCallback('Camera', mouse_click)
    contours,junk=cv2.findContours(myMask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #conotour function
    if len(contours)>0: # find countors
        contours=sorted(contours,key=lambda x:cv2.contourArea(x),reverse=True) # order from biggest to smallest contour
        #cv2.drawContours(frame,contours,-1,(255,0,0),3)
        contour=contours[0] #select first contour
        x,y,w,h=cv2.boundingRect(contour) # create contour
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3) # draw blue rectangle

        target_x=x+(w/2)
        target_y=y+(h/2)

        #print(f'err_x = {target_x} - {dispW/2} = {error_x}')
        #print('---------------------'+f'err_y = {target_y} - {dispH/2} = {error_y}')
        if training_method == STEADY:
            error_x = target_x - (dispW/2)
            error_y = target_y - (dispH/2)
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
        

        # Modified PID section
        if training_method == PID:
            current_time = time.time()
            dt = current_time - prev_time
            prev_time = current_time
            error_x = (dispW/2) - target_x
            error_y = target_y-(dispH/2) 
    
            norm_error_x = error_x / (dispW/2)
            norm_error_y = error_y / (dispH/2)
            
            # Get PID outputs
            pan_speed, prev_error_x, integral_x = pid(norm_error_x, prev_error_x, integral_x, dt)
            tilt_speed, prev_error_y, integral_y = pid(norm_error_y, prev_error_y, integral_y, dt)
            
            # Apply more aggressive scaling (try values between 20-50)
            scaling_factor = 30
            pan_speed *= scaling_factor
            tilt_speed *= scaling_factor
            
            # Limit speeds
            max_speed = 100  # Increased from 5
            pan_speed = max(-max_speed, min(max_speed, pan_speed))
            tilt_speed = max(-max_speed, min(max_speed, tilt_speed))
            
            # Update angles (ensure dt is reasonable)
            dt = max(0.001, min(0.1, dt))  # Clamp dt to avoid extremes
            pan_angle += pan_speed * dt
            tilt_angle += tilt_speed * dt
            
            # Limit angles
            pan_angle = max(-90, min(90, pan_angle))
            tilt_angle = max(-90, min(90, tilt_angle))
            
            # Move servos
            pantilthat.pan(pan_angle)
            pantilthat.tilt(tilt_angle)
    cv2.imshow("Camera", frame)
    cv2.imshow('Mask',myMaskSmall)
    cv2.imshow('My Object',myObjectSmall)
    cv2.moveWindow("Camera", 0, 0) 
    cv2.moveWindow("Mask", 0, dispH) 
    cv2.moveWindow("My Object", dispW, 0) 
    
    
    
    key = cv2.waitKey(1)
    if key == ord('q') or key == ord('Q'):
        if ser != None:
            ser.close()
        break
    elif key == ord('m') or key == ord('M'):
        print('extract hsv mode on')
        method = MOUSE
        cv2.setMouseCallback('Camera', mouse_click)
    elif key == ord('t') or key == ord('T'):
        print('training mode on')
        method = TRAINING
        cv2.setMouseCallback('Camera', lambda *args:None)
    elif key == ord('S') or key == ord('s'):
        print('steady mode on')
        training_method = STEADY
    elif key == ord('p') or key == ord('P'):
        print('PID mode on')
        training_method = PID

    tEnd=time.time()
    loopTime=tEnd-tStart
    fps=0.9*fps + .1*(1/loopTime)
cv2.destroyAllWindows()


