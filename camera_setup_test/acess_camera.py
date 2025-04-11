from picamera2 import Picamera2
import cv2

# Initialize the Pi Camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)  # Camera resolution
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")

# Start the camera
picam2.start()

win_name = 'Pi Camera Preview'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)  # Enable resizing
cv2.resizeWindow(win_name, 1280, 720)        # Set window size

try:
    while cv2.waitKey(1) != 27:  # Escape key to exit
        # Capture frame from Pi Camera
        frame = picam2.capture_array()
        # Display the frame
        cv2.imshow(win_name, frame)

finally:
    # Stop the camera and close the window
    picam2.stop()
    cv2.destroyAllWindows()
