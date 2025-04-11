
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

def mouse_click(event,x,y,flags,param):
    global target_x,target_y  # Add this line to access and modify global variables
        
    if event == cv2.EVENT_MOUSEMOVE:
        target_x=x
        target_y=y


# Start video capture
picam2= Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()
#source = cv2.VideoCapture(0)
#source.set(cv2.CAP_PROP_FRAME_WIDTH, display_width)
#source.set(cv2.CAP_PROP_FRAME_HEIGHT, display_height)
cv2.namedWindow("Camera Preview")
cv2.setMouseCallback("Camera Preview", mouse_click)


try:
    while True:
        tStart=time.time()    


        frame= picam2.capture_array()
        frame=cv2.flip(frame,-1)
        #frameHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        cv2.putText(frame,str(int(fps))+' FPS',pos,font,height,myColor,weight)
#--------------------
        width= display_width/2
        height= display_width/2
        error_x = target_x - width
        error_y = target_y - height
        print(width,'-',target_x,'=',error_x,'and',pan_angle)
        if abs(error_x) > 30:
            if error_x > 0:
                pan_angle= pan_angle -1
                if pan_angle<-90:
                    pan_angle=-90
                pantilthat.pan(pan_angle)    
            if error_x < 0:
                pan_angle= pan_angle +1
                if pan_angle>90:
                    pan_angle=90
                pantilthat.pan(pan_angle)
        if abs(error_y) > 30:
            if error_y > 0:
                tilt_angle= tilt_angle +1
                if tilt_angle>90:
                    tilt_angle=90
                pantilthat.tilt(tilt_angle)    
            if error_y < 0:
                tilt_angle= tilt_angle -1
                if tilt_angle<-90:
                    tilt_angle=-90
                pantilthat.tilt(tilt_angle)




    #print(f"Pan: {pan_angle}, Tilt: {tilt_angle}")

#------------------------
        # Display the frame
        cv2.imshow("Camera Preview", frame)
        
        # Break loop on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        tEnd=time.time()
        loopTime=tEnd-tStart
        fps=.9*fps + .1*(1/loopTime)
finally:
    # Release resources
    picam2.close()
    cv2.destroyAllWindows()
