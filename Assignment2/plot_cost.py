import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

L = 1000
r = 5
ns = [7, 10, 15]
runtimes = [44.7, 30.73, 25.8]  # minutes (44:42, 30:44, 25:48)

rows = []
for n, rt in zip(ns, runtimes):
    chunks = L // n
    windows_per_chunk = n - r + 1
    total_windows = chunks * windows_per_chunk
    rows.append({'n': n, 'Chunks per sequence': chunks,
                 'Windows per chunk': windows_per_chunk,
                 'Total windows': total_windows,
                 'Runtime (min)': rt})

df = pd.DataFrame(rows)
df['Config'] = df['n'].apply(lambda x: f'n={x}')

print(df[['Config', 'Chunks per sequence', 'Windows per chunk', 'Total windows', 'Runtime (min)']].to_string(index=False))

fig, axes = plt.subplots(1, 3, figsize=(13, 4))

palette = sns.color_palette('muted', 3)

# Plot 1: Chunks per sequence & Windows per chunk (grouped bar)
melted = df.melt(id_vars='Config', value_vars=['Chunks per sequence', 'Windows per chunk'],
                 var_name='Metric', value_name='Count')
sns.barplot(data=melted, x='Config', y='Count', hue='Metric', ax=axes[0], palette=palette[:2])
axes[0].set_title('Chunks & Windows per Chunk')
axes[0].set_ylabel('Count')
axes[0].set_xlabel('')
for container in axes[0].containers:
    axes[0].bar_label(container, fontsize=9, padding=2)

# Plot 2: Total windows
sns.barplot(data=df, x='Config', y='Total windows', ax=axes[1], color=palette[0])
axes[1].set_title('Total Matching Windows (L=1000, r=5)')
axes[1].set_ylabel('Total windows per sequence')
axes[1].set_xlabel('')
for container in axes[1].containers:
    axes[1].bar_label(container, fontsize=9, padding=2)

# Plot 3: Runtime
sns.barplot(data=df, x='Config', y='Runtime (min)', ax=axes[2], color=palette[1])
axes[2].set_title('Measured Runtime')
axes[2].set_ylabel('Runtime (minutes)')
axes[2].set_xlabel('')
for container in axes[2].containers:
    axes[2].bar_label(container, fmt='%.1f', fontsize=9, padding=2)

plt.tight_layout()
plt.savefig('/home/aaron/Projects/uni/NaturalComputing/Assignment2/cost_analysis.png', dpi=150)
print("\nSaved to cost_analysis.png")
