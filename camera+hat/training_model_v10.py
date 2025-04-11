import pantilthat
import time

# Set servo to 0° (or another starting position)
pantilthat.pan(0)
time.sleep(2.0)  # Allow servo to reach position

# Record start angle and time
start_angle = pantilthat.get_pan()
start_time = time.time()

# Command servo to move to 90° (or another large angle)
pantilthat.pan(90)

# Wait until servo reaches the target (or a set duration)
time.sleep(1.0)  # Adjust based on expected speed

# Measure final angle and time
end_angle = pantilthat.get_pan()
end_time = time.time()

# Calculate speed (°/sec)
distance = abs(end_angle - start_angle)
duration = end_time - start_time
actual_speed = distance / duration

print(f"Servo moved {distance}° in {duration:.2f} sec → Speed = {actual_speed:.2f}°/sec")