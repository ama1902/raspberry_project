
import pantilthat
import numpy as np
from time import sleep
import cv2
from picamera2 import Picamera2
import time
pan_angle = 0.0# positive going left
tilt_angle = 0.0
pantilthat.pan(pan_angle)
pantilthat.tilt(tilt_angle)
display_width = 640
display_height = 480
fps=0
pos=(30,60)
font=cv2.FONT_HERSHEY_SIMPLEX
height=1.5
weight=3
myColor=(0,0,255)
target_x = 320  # Initial center position
target_y = 240

# Start video capture
picam2= Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()
#source = cv2.VideoCapture(0)
#source.set(cv2.CAP_PROP_FRAME_WIDTH, display_width)
#source.set(cv2.CAP_PROP_FRAME_HEIGHT, display_height)
cv2.namedWindow("Camera Preview")

try:
    while True:
        tStart=time.time()    


        frame= picam2.capture_array()
        frame=cv2.flip(frame,-1)
        #frameHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        cv2.putText(frame,str(int(fps))+' FPS',pos,font,height,myColor,weight)
#--------------------
        key = cv2.waitKey(1)  # Read the key press inside the loop

        if key == ord('s') or key == ord('S'):  # Increase tilt angle, camera GOES DOWN
            tilt_angle += 1
            if tilt_angle > 90:  # Limit tilt angle to max 90
                tilt_angle = 90
            pantilthat.tilt(tilt_angle)  # Apply the new tilt angle

        if key == ord('W') or key == ord('w'):  # Decrease tilt angle, camera GOES UP
            tilt_angle -= 1
            if tilt_angle < -90:  # Limit tilt angle to min -90
                tilt_angle = -90
            pantilthat.tilt(tilt_angle)  # Apply the new tilt angle

        if key == ord('D') or key == ord('d'):  # Pan RIGHT
            pan_angle -= 1
            if pan_angle < -90:  # Limit pan angle to min -90
                pan_angle = -90
            pantilthat.pan(pan_angle)  # Apply the new pan angle

        if key == ord('A') or key == ord('a'):  # Pan LEFT
            pan_angle += 1
            if pan_angle > 90:  # Limit pan angle to max 90
                pan_angle = 90
            pantilthat.pan(pan_angle)  # Apply the new pan angle

        if key == ord('q') or key == ord('Q'):  # Quit the loopat.tilt(tilt_angle)
            break




    #print(f"Pan: {pan_angle}, Tilt: {tilt_angle}")

#------------------------
        # Display the frame
        cv2.imshow("Camera Preview", frame)
        tEnd=time.time()
        loopTime=tEnd-tStart
        fps=.9*fps + .1*(1/loopTime)
finally:
    # Release resources
    picam2.close()
    cv2.destroyAllWindows()
