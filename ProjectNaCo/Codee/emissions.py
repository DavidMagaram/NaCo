import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Load data
df = pd.read_csv('emissions.csv')

# 2. Map original project names to the ones used in the report
name_map = {
    'Phase_2_identity': 'Identity',
    'Phase_2_gradient-start': 'Gradient-start',
    'Phase_1_Gradient': 'Gradient',
    'Phase_2_random': 'White Noise'
}

# Filter and rename
df_filtered = df[df['project_name'].isin(name_map.keys())].copy()
df_filtered['Method'] = df_filtered['project_name'].map(name_map)

# Ensure the categorical order matches the report
df_filtered['Method'] = pd.Categorical(
    df_filtered['Method'], 
    categories=['Identity', 'Gradient-start', 'Gradient', 'White Noise'], 
    ordered=True
)
df_filtered = df_filtered.sort_values('Method')

# 3. Create the Summary Table
table_df = df_filtered[['Method', 'emissions', 'duration', 'energy_consumed']].copy()
table_df.columns = ['Method', 'Emissions', 'Duration', 'Energy Consumed']

# Save the table to a CSV file (emissions_table.csv)
table_df.to_csv('emissions_table.csv', index=False)

# 4. Create the Bar Plot
methods = table_df['Method'].tolist()
emissions = df_filtered['emissions'].values
cpu_energy_x2 = df_filtered['cpu_energy'].values * 2  # Multiplied by 2 for dual CPUs
gpu_energy = df_filtered['gpu_energy'].values
ram_energy = df_filtered['ram_energy'].values

x = np.arange(len(methods))
width = 0.2  # Width of the bars

fig, ax = plt.subplots(figsize=(10, 6))

rects1 = ax.bar(x - 1.5*width, emissions, width, label='Total Emissions')
rects2 = ax.bar(x - 0.5*width, cpu_energy_x2, width, label='CPU Energy x 2')
rects3 = ax.bar(x + 0.5*width, gpu_energy, width, label='GPU Energy')
rects4 = ax.bar(x + 1.5*width, ram_energy, width, label='RAM Energy')

ax.set_ylabel('Value (kgCO2e / kWh)')
ax.set_title('Emissions and Compute Energy Consumption by Method')
ax.set_xticks(x)
ax.set_xticklabels(methods)
ax.legend()

plt.tight_layout()
plt.savefig('emissions_plot.png')