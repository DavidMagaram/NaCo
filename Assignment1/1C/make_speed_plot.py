import matplotlib.pyplot as plt
import numpy as np

obstacles = [0, 9, 25, 49]

# Data from tables in the report
baseline_speed = [0.0347, 0.0340, 0.0324, 0.0300]
baseline_std   = [0.0075, 0.0094, 0.0070, 0.0107]
adjusted_speed = [0.1168, 0.1100, 0.1094, 0.1008]
adjusted_std   = [0.0070, 0.0116, 0.0095, 0.0131]

fig, ax = plt.subplots(figsize=(5, 3.5))

ax.errorbar(obstacles, baseline_speed, yerr=baseline_std, fmt='o-', capsize=4, label=r'Baseline ($\mathrm{Max_{act}}=20$)', color='#1f77b4')
ax.errorbar(obstacles, adjusted_speed, yerr=adjusted_std, fmt='s-', capsize=4, label=r'Adjusted ($\mathrm{Max_{act}}=60$)', color='#d62728')

ax.set_xlabel('Number of obstacles')
ax.set_ylabel('Average speed (pixels/step)')
ax.set_xticks(obstacles)
ax.legend()
ax.set_ylim(bottom=0)
ax.grid(True, alpha=0.3)
fig.tight_layout()

fig.savefig('report_images/speed_vs_obstacles.png', dpi=200)
print("Saved to report_images/speed_vs_obstacles.png")
