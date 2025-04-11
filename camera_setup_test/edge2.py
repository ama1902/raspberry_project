import cv2
import numpy as np
from picamera2 import Picamera2
import time

# Picamera2 initialization
picam2 = Picamera2()

dispH = 720
dispW= 1280
picam2.preview_configuration.main.size = (dispW, dispH)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.controls.FrameRate = 30
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# Constants
PREVIEW = 0
BLUR = 1
FEATURES = 2
CANNY = 3

feature_params = dict(maxCorners=500, qualityLevel=0.2, minDistance=15, blockSize=9)
image_filter = PREVIEW
alive = True

win_name = "Camera Filters"
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(win_name, dispW, dispH)
result = None

while alive:
    frame = picam2.capture_array()
    #frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert to BGR
    frame = cv2.flip(frame, -1)

    if image_filter == PREVIEW:
        result = frame
    elif image_filter == CANNY:
        result = cv2.Canny(frame, 80, 150)
    elif image_filter == BLUR:
        result = cv2.blur(frame, (13, 13))
    elif image_filter == FEATURES:
        result = frame
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners = cv2.goodFeaturesToTrack(frame_gray, **feature_params)
        if corners is not None:
            for x, y in np.float32(corners).reshape(-1, 2):
                x, y = int(x), int(y)
                cv2.circle(result, (x, y), 10, (0, 255, 0), 1)

    cv2.imshow(win_name, result)

    key = cv2.waitKey(1)
    if key == ord("Q") or key == ord("q") or key == 27:
        alive = False
    elif key == ord("C") or key == ord("c"):
        image_filter = CANNY
    elif key == ord("B") or key == ord("b"):
        image_filter = BLUR
    elif key == ord("F") or key == ord("f"):
        image_filter = FEATURES
    elif key == ord("P") or key == ord("p"):
        image_filter = PREVIEW

    time.sleep(1 / 30)  # Maintain 30 FPS

cv2.destroyAllWindows()
