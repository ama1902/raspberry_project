import cv2
from picamera2 import Picamera2
import serial
import time
import threading
from queue import Queue
from datetime import datetime
import csv

# --- Constants ---
DISPLAY_WIDTH = 1920
DISPLAY_HEIGHT = 1080
FONT = cv2.FONT_HERSHEY_SIMPLEX
DATA_DIR = "/home/ama/disertation_project/lidar/"
LIDAR_TIMEOUT = 0.1  # seconds

# --- Global Variables ---
lidar_data = {'distance': 0, 'strength': 0, 'temperature': 0}
data_collection_active = False
exit_flag = False
data_queue = Queue()

'''class LidarController:
    def __init__(self):
        self.ser = None
        self.connected = False
        
    def connect(self):
        try:
            self.ser = serial.Serial("/dev/ttyS0", 115200, timeout=LIDAR_TIMEOUT)
            self.connected = True
            print("LiDAR connected successfully")
        except serial.SerialException as e:
            print(f"LiDAR connection failed: {e}")
            
    def read_data(self):
        if not self.connected:
            return None
            
        try:
            bytes_serial = self.ser.read(9)
            if len(bytes_serial) == 9 and bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59:
                distance = bytes_serial[2] + bytes_serial[3] * 256
                strength = bytes_serial[4] + bytes_serial[5] * 256
                temperature = (bytes_serial[6] + bytes_serial[7] * 256) / 8 - 256
                return distance, strength, temperature
        except Exception as e:
            print(f"LiDAR read error: {e}")
        return None
        
    def close(self):
        if self.connected:
            self.ser.close()
            self.connected = False
'''
def init_camera():
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(
        main={"size": (DISPLAY_WIDTH, DISPLAY_HEIGHT), "format": "RGB888"},
        controls={"FrameRate": 30}
    )
    picam2.configure(config)
    picam2.start()
    return picam2

'''def lidar_collection_thread(lidar, num_points=11, step=5, samples_per_point=50):
    global data_collection_active, lidar_data
    
    data_collection_active = True
    all_data = []
    
    for point in [i * step for i in range(num_points)]:
        print(f"\nMove to position {point}cm. Press Enter to start...")
        input()
        
        point_data = []
        start_time = time.time()
        
        while len(point_data) < samples_per_point and not exit_flag:
            result = lidar.read_data()
            if result:
                distance, strength, temperature = result
                timestamp = time.time() - start_time
                
                # Update global data
                lidar_data = {
                    'distance': distance,
                    'strength': strength,
                    'temperature': temperature
                }
                
                # Save to queue and local list
                data_point = (point, distance, strength, temperature, timestamp)
                data_queue.put(data_point)
                point_data.append(data_point)
                
                print(f"Point {point}cm: {distance}cm (Strength: {strength})")
        
        all_data.extend(point_data)
        
        if exit_flag:
            break

    # Save to CSV
    if all_data:
        filename = f"{DATA_DIR}lidar_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Position_cm', 'Distance_cm', 'Strength', 'Temperature_C', 'Timestamp_s'])
                writer.writerows(all_data)
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving data: {e}")
    
    data_collection_active = False
'''
def main():
    global exit_flag
    
    # Initialize hardware
    picam2 = init_camera()
    #lidar = LidarController()
    #lidar.connect()
    
    fps = 0
    last_time = time.time()
    
    try:
        while not exit_flag:
            # Calculate FPS
            current_time = time.time()
            loop_time = current_time - last_time
            fps = 0.9 * fps + 0.1 * (1 / loop_time)
            last_time = current_time
            
            # Get camera frame
            frame = picam2.capture_array()
            frame = cv2.flip(frame, -1)
            
            # Display LiDAR data
            #display_text = f"D: {lidar_data['distance']}cm S: {lidar_data['strength']}"
            #if lidar_data['temperature'] != 0:
            #    display_text += f" T: {lidar_data['temperature']:.1f}°C"
            
            #cv2.putText(frame, f"FPS: {fps:.1f}", (20, 30), FONT, 0.7, (0, 255, 0), 2)
            #cv2.putText(frame, display_text, (20, 60), FONT, 0.7, (0, 255, 0), 2)
            
            #if data_collection_active:
            #    cv2.putText(frame, "RECORDING", (20, 90), FONT, 0.7, (0, 0, 255), 2)
            
            cv2.imshow("LiDAR Camera", frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                exit_flag = True
            #elif key == ord('d') and lidar.connected and not data_collection_active:
             #   threading.Thread(
              #      target=lidar_collection_thread,
               #     args=(lidar,),
                #    daemon=True
                #).start()
                
    finally:
        # Cleanup
        picam2.stop()
        cv2.destroyAllWindows()
        lidar.close()
        print("Application closed")

if __name__ == "__main__":
    main()