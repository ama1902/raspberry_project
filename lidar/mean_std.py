import pandas as pd
import time
material='white'
# === CONFIGURATION ===
input_file = f'/home/ama/disertation_project/lidar/tf_luna_measurements_{material}.csv'
output_file = f'/home/ama/disertation_project/lidar/{material}_summary.csv'
import pandas as pd

# Read input CSV
df = pd.read_csv(input_file)

# Group by actual position and calculate statistics
summary = df.groupby("Position_cm").agg({
    "Distance_cm": ["mean", "std"],
    "strenght": ["mean", "std"]
}).reset_index()

# Flatten column headers
summary.columns = [
    "actual distance",
    "mean distance",
    "std distance",
    "mean strenght",
    "std strenght"
]

# Save to new CSV
summary.to_csv(output_file, index=False)
