import pandas as pd
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('/home/ama/disertation_project/camera+hat/movement_log.csv')

# Separate PID and fixed-step data
pid_data = data[data['movement_type'] == 'PID']
fixed_data = data[data['movement_type'] == 'STEADY']

# Create comparison plot
plt.figure(figsize=(12,6))
plt.plot(pid_data['timestamp']-pid_data['timestamp'].min(), 
         pid_data['target_x'], 
         label='PID Control',
         linewidth=2)

'''plt.step(fixed_data['timestamp']-fixed_data['timestamp'].min(), 
        fixed_data['pan_angle'], 
        label='Fixed-Step',
        linewidth=2,
        where='post')  # Makes steps occur after the timestamp
'''

plt.plot(fixed_data['timestamp']-fixed_data['timestamp'].min(), 
        fixed_data['target_x'], 
        label='Fixed-Step',
        linewidth=2)  # Makes steps occur after the timestamp


# Formatting
plt.xlabel('Time (seconds)', fontsize=12)
plt.ylabel('error in x direction', fontsize=12)
plt.title('PID vs Fixed-Step Control Comparison', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# Save the figure (do this BEFORE plt.show())
plt.savefig('/home/ama/disertation_project/camera+hat/control_comparison.png', 
           dpi=300, 
           bbox_inches='tight', 
           facecolor='white')

# Optionally display it as well
plt.show()

print("Plot saved to /home/ama/control_comparison.png")