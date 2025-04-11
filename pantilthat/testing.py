import cv2
import pantilthat

# Initialize pan and tilt angles
pan_angle = 0.0  # positive going left
tilt_angle = 0.0
pantilthat.pan(pan_angle)
pantilthat.tilt(tilt_angle)

# Start the control loop
ALIVE = True
while ALIVE:
    key = cv2.waitKey(1)  # Read the key press inside the loop

    if key == ord('w') or key == ord('W'):  # Increase tilt angle
        tilt_angle += 1
        if tilt_angle > 90:  # Limit tilt angle to max 90
            tilt_angle = 90
        pantilthat.tilt(tilt_angle)  # Apply the new tilt angle

    if key == ord('s') or key == ord('S'):  # Decrease tilt angle
        tilt_angle -= 1
        if tilt_angle < -90:  # Limit tilt angle to min -90
            tilt_angle = -90
        pantilthat.tilt(tilt_angle)  # Apply the new tilt angle

    if key == ord('a') or key == ord('A'):  # Pan left
        pan_angle -= 1
        if pan_angle < -90:  # Limit pan angle to min -90
            pan_angle = -90
        pantilthat.pan(pan_angle)  # Apply the new pan angle

    if key == ord('d') or key == ord('D'):  # Pan right
        pan_angle += 1
        if pan_angle > 90:  # Limit pan angle to max 90
            pan_angle = 90
        pantilthat.pan(pan_angle)  # Apply the new pan angle

    if key == ord('q') or key == ord('Q'):  # Quit the loop
        ALIVE = False

print("Program terminated.")
