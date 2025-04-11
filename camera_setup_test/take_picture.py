from picamera2 import Picamera2, Preview
import time
import pantilthat

pan_angle = 0.0# positive going left
tilt_angle = 0.0
pantilthat.pan(pan_angle)
pantilthat.tilt(tilt_angle)


picam2 = Picamera2()

camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)

#picam2.start_preview(Preview.QTGL)
picam2.start()
time.sleep(2)
path='/home/ama/disertation_project/camera_setup_test/'
picam2.capture_file(path+"lidar_view.jpg")

picam2.start_and_capture_file(path+"test.jpg")
