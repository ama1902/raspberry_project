from picamera2 import Picamera2, Preview
import time

picam2 = Picamera2()

camera_config = picam2.create_preview_configuration()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)})

picam2.configure(camera_config)

#picam2.start_preview(Preview.QTGL)
picam2.start()
time.sleep(2)
path='/home/ama/disertation_project/camera_setup_test/'
picam2.capture_file(path+"hd.jpg")

#picam2.start_and_capture_file(path+"hs2.jpg")
print(camera_config["main"]["size"])  # For still configuration, should be high (e.g. 4056x3040)
