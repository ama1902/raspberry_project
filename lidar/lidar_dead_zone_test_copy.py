import serial
import time
import csv

# Serial port configuration
ser = None
CSV_FILE = "/home/ama/disertation_project/lidar/tf_luna_measurements_clear.csv"
MEASUREMENTS_PER_POSITION = 20
POSITIONS_CM = list(range(0, 101, 10))  # [0, 5, 10, ..., 50]

def read_distance():
    """Read distance from TF-Luna using your specified approach""" 
    if not ser.isOpen():
        ser.open()
        
    while True:
        counter = ser.in_waiting
        if counter > 8:
            bytes_serial = ser.read(9)
            ser.reset_input_buffer()
            # Python3 style reading
            if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59:
                distance = bytes_serial[2] + bytes_serial[3]*256
                strength = bytes_serial[4] + bytes_serial[5]*256
                
                time.sleep(0.5)  # Clear buffer after successful read
                ser.reset_input_buffer()
                return distance,strength
            
            # Python2 style reading (kept for compatibility)
            if bytes_serial[0] == "Y" and bytes_serial[1] == "Y":
                distL = int(bytes_serial[2].encode("hex"), 16)
                distH = int(bytes_serial[3].encode("hex"), 16)
                distance = distL + distH*256
                stL = int(bytes_serial[4].encode("hex"), 16)
                stH = int(bytes_serial[5].encode("hex"), 16)
                strength = stL + stH*256
                
                time.sleep(0.5)  # Clear buffer after successful read
                ser.reset_input_buffer()
                return distance,strength
        else:
            print('Waiting for data...')
            time.sleep(0.01)  # Small delay to prevent CPU overload
            continue  # This will continue the while loop
try:
    # Initialize serial port
    ser = serial.Serial("/dev/ttyS0", 115200)
    if not ser.isOpen():
        ser.open()

    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Position_cm", "Measurement_index", "Distance_cm",'strenght'])

        for pos in POSITIONS_CM:
            print(f"\nPosition: {pos} cm - Starting measurements...")
            
            for i in range(MEASUREMENTS_PER_POSITION):
                distance,strength = read_distance()
                writer.writerow([pos, i+1, distance,strength])
                print(f"  [{i+1}/{MEASUREMENTS_PER_POSITION}] Distance: {distance} cm")
                time.sleep(1)  # ~20Hz sample rate
            print(f"\nPosition: {pos} cm - FINISHED")
            print('move to next distance')
            time.sleep(4)
            print('starting next distance')
            time.sleep(2)
            
                
except KeyboardInterrupt:
    print("\nMeasurement interrupted by user")
    
except Exception as e:
    print(f"\nError occurred: {str(e)}")
    
finally:
    if ser and ser.isOpen():
        ser.close()
    print(f"\nAll data saved to {CSV_FILE}")