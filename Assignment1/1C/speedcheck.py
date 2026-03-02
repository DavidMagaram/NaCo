import pandas as pd
import numpy as np
import sys

input_file = sys.argv[1] if len(sys.argv) > 1 else 'myfile.txt'

df = pd.read_csv(input_file, sep='\t', names=['time', 'cellID', 'cellType', 'x', 'y'])

# Filter to only active/moving cells (cellType 1), exclude background (0) and obstacles (2)
df = df[df['cellType'] == 1]

print("="*50)
print("CELL MOVEMENT ANALYSIS (active cells only)")
print("="*50)

print(f"\nDataset: {len(df)} observations")
print(f"Time range: {df['time'].min()} - {df['time'].max()}")
print(f"Number of active cells: {df['cellID'].nunique()}")

speeds = []
for cell_id, group in df.groupby('cellID'):
    group = group.sort_values('time')
    dx = group['x'].diff()
    dy = group['y'].diff()
    dt = group['time'].diff()
    displacement = np.sqrt(dx**2 + dy**2)
    speed = displacement / dt
    speeds.append({
        'cellID': cell_id,
        'avg_speed': speed.mean(),
        'max_speed': speed.max(),
        'total_distance': displacement.sum()
    })

result = pd.DataFrame(speeds)

print("\n" + "-"*50)
print("SPEED STATISTICS (pixels/timestep)")
print("-"*50)
print(f"Mean speed across all cells:   {result['avg_speed'].mean():.4f}")
print(f"Std dev of cell speeds:        {result['avg_speed'].std():.4f}")
print(f"Fastest cell avg speed:        {result['avg_speed'].max():.4f}")
print(f"Slowest cell avg speed:        {result['avg_speed'].min():.4f}")

print("\n" + "-"*50)
print("DISTANCE STATISTICS (total pixels traveled)")
print("-"*50)
print(f"Mean distance per cell:        {result['total_distance'].mean():.2f}")
print(f"Max distance (most active):    {result['total_distance'].max():.2f}")
print(f"Min distance (least active):   {result['total_distance'].min():.2f}")

print("\n" + "="*50)
