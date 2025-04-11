import serial
import time
import pantilthat
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd

# Initialize serial connection to LiDAR
ser = serial.Serial("/dev/ttyS0", 115200)

# Global variables
distance = 0
pan_angle = 0
tilt_angle = 0
step = 0.5
pan_max = 25
pan_min = -25
tilt_max = 25
tilt_min = -25 

# List to store 3D points (x, y, z) and metadata
points = []

def read_lidar_data():
    """Read distance data from the LiDAR sensor."""
    global distance
    time.sleep(0.1)  # Small delay to allow data to be received
    counter = ser.in_waiting  # Count the number of bytes in the serial buffer
    if counter > 8:
        bytes_serial = ser.read(9)  # Read 9 bytes
        ser.reset_input_buffer()
        if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59:  # Check for correct header
            distance = bytes_serial[2] + bytes_serial[3] * 256  # Calculate distance
            strength = bytes_serial[4] + bytes_serial[5] * 256  # Signal strength (not used here)
            temperature = bytes_serial[6] + bytes_serial[7] * 256  # Temperature (not used here)
            temperature = (temperature / 8) - 256  # Convert temperature to Celsius
            print(f"Distance: {distance} cm, Temperature: {temperature} °C")

def calculate_3d_point(pan_angle, tilt_angle, distance):
    """Convert pan, tilt, and distance to 3D coordinates (x, y, z)."""
    pan_rad = np.radians(pan_angle)
    tilt_rad = np.radians(tilt_angle)
    
    x = distance * np.cos(tilt_rad) * np.cos(pan_rad)
    y = distance * np.cos(tilt_rad) * np.sin(pan_rad)
    z = distance * np.sin(tilt_rad)
    
    return x, y, z

def plot_point_cloud(points, filename):
    """
    Plot the 3D point cloud using matplotlib and save it as a PNG file.

    Parameters:
        points (list): List of 3D points as tuples (x, y, z).
        filename (str): Name of the output PNG file. Default is "point_cloud.png".
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Extract x, y, z coordinates from the points list
    x = [point[0] for point in points]
    y = [point[1] for point in points]
    z = [point[2] for point in points]
    
    # Create the 3D scatter plot
    ax.scatter(x, y, z, c='b', marker='o')
    ax.set_xlabel('X (cm)')
    ax.set_ylabel('Y (cm)')
    ax.set_zlabel('Z (cm)')
    
    # Save the plot as a PNG file
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Plot saved as {filename}")
    
    # Close the figure to free up memory
    plt.close(fig)

if __name__ == "__main__":
    try:
        # Loop through tilt angles
        for tilt in np.arange(tilt_min, tilt_max + step, step):
            pantilthat.tilt(tilt)  # Set tilt angle
            time.sleep(0.1)  # Allow time for the servo to move
            
            # Loop through pan angles
            for pan in np.arange(pan_min, pan_max + step, step):
                pantilthat.pan(pan)  # Set pan angle
                time.sleep(0.1)  # Allow time for the servo to move
                
                # Read LiDAR data
                read_lidar_data()
                
                # Calculate 3D coordinates
                x, y, z = calculate_3d_point(pan, tilt, distance)
                points.append((x, y, z, distance, pan, tilt))  # Store the 3D point with metadata
                
                print(f"Pan: {pan}, Tilt: {tilt}, Distance: {distance}, Point: ({x}, {y}, {z})")
        
        # Convert the points to a DataFrame
        df = pd.DataFrame(points, columns=['X', 'Y', 'Z', 'Distance', 'Pan', 'Tilt'])
        
        # Save the DataFrame to a Feather file
        feather_filename = "/home/ama/disertation_project/TF-Luna-LiDAR-Range-Sensor-Demo/point_cloud3.feather"
        df.to_feather(feather_filename)
        print(f"Data saved to Feather file: {feather_filename}")
        
        # Save the DataFrame to a CSV file
        csv_filename = "/home/ama/disertation_project/TF-Luna-LiDAR-Range-Sensor-Demo/point_cloud3.csv"
        df.to_csv(csv_filename, index=False)
        print(f"Data saved to CSV file: {csv_filename}")
        
        # Plot the point cloud
        print("Plotting point cloud...")
        print(f"Number of points collected: {len(points)}")
        plot_point_cloud(points, filename="/home/ama/disertation_project/TF-Luna-LiDAR-Range-Sensor-Demo/point_cloud3.png")

    except KeyboardInterrupt:
        print("Program interrupted by the user")
    finally:
        if ser.is_open:
            ser.close()
        print("Serial connection closed")
