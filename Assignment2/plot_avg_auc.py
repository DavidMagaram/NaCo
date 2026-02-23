import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = {
    'n': [7, 7, 10, 10, 15, 15],
    'Dataset': ['snd-cert', 'snd-unm'] * 3,
    'Split 1': [0.9774, 0.9900, 0.9728, 0.9804, 0.9756, 0.9900],
    'Split 2': [0.9841, 0.9630, 0.9820, 0.9821, 0.9832, 0.9732],
    'Split 3': [0.9748, 0.9854, 0.9838, 0.9846, 0.9746, 0.9760],
}

df = pd.DataFrame(data)
df['Mean AUC'] = df[['Split 1', 'Split 2', 'Split 3']].mean(axis=1)
df['Config'] = df['n'].apply(lambda x: f'n={x}, r=5')

print(df[['Config', 'Dataset', 'Mean AUC']].to_string(index=False))

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(7, 4))

sns.barplot(data=df, x='Config', y='Mean AUC', hue='Dataset', ax=ax, palette='muted')

ax.set_ylim(0.96, 1.0)
ax.set_ylabel('Mean AUC (across 3 splits)')
ax.set_xlabel('')
ax.set_title('Average AUC by Configuration (Chunked Training, r=5)')

for container in ax.containers:
    ax.bar_label(container, fmt='%.4f', fontsize=8, padding=2)

plt.tight_layout()
plt.savefig('/home/aaron/Projects/uni/NaturalComputing/Assignment2/avg_auc_by_config.png', dpi=150)
print("\nSaved to avg_auc_by_config.png")
