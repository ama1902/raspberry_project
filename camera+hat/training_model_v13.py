#this version only canny edge
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


hueLow = 80
hueHigh = 150
def onTrack1(val):
    global hueLow
    hueLow=val
    print('Hue Low',hueLow)
def onTrack2(val):
    global hueHigh
    hueHigh=val
    print('Hue High',hueHigh)
cv2.namedWindow('myTracker')
cv2.createTrackbar('Hue Low','myTracker',1,179,onTrack1)
cv2.createTrackbar('Hue High','myTracker',1,179,onTrack2)


TRAINING =0
MOUSE=1
STEADY=2
PID =3


if ser.isOpen() == False:
    ser.open()

HSV=0
CANNY=1
method= TRAINING
training_method = STEADY
detection = CANNY


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
    canny_low = hueLow
    canny_high = hueHigh
        
    # Convert to grayscale and blur
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    
    # Apply Canny edge detection
    edges = cv2.Canny(blurred, canny_low, canny_high)
    
    # For visualization
    edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    myMaskSmall = cv2.resize(edges_bgr, (int(dispW/2), int(dispH/2)))
    cv2.putText(frame,str(int(fps))+' FPS',pos,font,height,myColor,weight)
    cv2.putText(frame,lidar_distance,pos2,font,height2,myColor,weight)
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Filter out small contours
        contours = [c for c in contours if cv2.contourArea(c) > 100]
        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            target_x = x + (w/2)
            target_y = y + (h/2)
    
        # For display purposes (if you still want to show the mask
###########################################################
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
                current_pan_angle=pan_angle
                current_tilt_angle=tilt_angle
        myMask = edges  # This is a binary image (0 or 255)
        myMaskSmall = cv2.resize(myMask, (int(dispW/2), int(dispH/2)))
        myObjectSmall = cv2.bitwise_and(frame, frame, mask=myMask)
        myObjectSmall = cv2.resize(myObjectSmall, (int(dispW/2), int(dispH/2)))
        # Modified PID section
    cv2.imshow("Camera", frame)
    cv2.moveWindow("Camera", 0, 0)


    # Canny mode displays - show edges and edge-based object
    cv2.imshow('Edges', myMaskSmall)  # Shows the Canny edges
    cv2.imshow('Edge Object', myObjectSmall)  # Shows original image masked by edges
    cv2.moveWindow("Edges", 0, dispH)
    cv2.moveWindow("Edge Object", dispW, 0)

    
    key = cv2.waitKey(1)
    if key == ord('q') or key == ord('Q'):
        if ser != None:
            ser.close()
        break
    elif key == ord('S') or key == ord('s'):
        print('steady mode on')
        training_method = STEADY

    tEnd=time.time()
    loopTime=tEnd-tStart
    fps=0.9*fps + .1*(1/loopTime)
cv2.destroyAllWindows()


