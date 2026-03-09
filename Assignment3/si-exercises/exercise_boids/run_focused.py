#!/usr/bin/env python3
"""Run focused boids experiments with 25 repeats on the most relevant configs."""

import subprocess
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
NODE_SCRIPT = os.path.join(SCRIPT_DIR, "node-boids.js")

NUM_REPEATS = 25

# innerR irrelevant (sep=0), fix it at 10. Vary alignment, cohesion, outerR.
configs = []
for outer_r in [25, 40]:
    for align in [0, 0.33, 0.66, 1]:
        for cohes in [0, 0.33, 0.66, 1]:
            configs.append((10, outer_r, align, cohes, 0, 150))

print(f"Running {len(configs)} configs x {NUM_REPEATS} repeats = {len(configs)*NUM_REPEATS} runs")

results = []
for i, (ir, or_, al, co, se, n) in enumerate(configs):
    orders = []
    nns = []
    for _ in range(NUM_REPEATS):
        cmd = ["node", NODE_SCRIPT, "--i", str(ir), "--o", str(or_),
               "--a", str(al), "--c", str(co), "--s", str(se),
               "--N", str(n), "--T", "300"]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        for line in r.stdout.strip().split("\n"):
            parts = line.split(",")
            if parts[0] == "300":
                orders.append(float(parts[1]))
                nns.append(float(parts[2]))

    avg_order = sum(orders) / len(orders)
    avg_nn = sum(nns) / len(nns)
    ratio = avg_order / avg_nn if avg_nn > 0.001 else 0
    results.append((avg_order, avg_nn, ratio, ir, or_, al, co, se))
    print(f"  [{i+1}/{len(configs)}] oR={or_} a={al} c={co} -> order={avg_order:.4f} nn={avg_nn:.4f}")

print("\n" + "=" * 90)
print(f"{'':>14} {'oR':>4} {'align':>6} {'cohes':>6} {'sep':>5} | {'order':>8} {'nn':>8} {'ratio':>8}")
print("-" * 90)

best_order = max(results, key=lambda x: x[0])
print(f"{'Best Order':>14} {best_order[4]:>4} {best_order[5]:>6} {best_order[6]:>6} {best_order[7]:>5} | {best_order[0]:>8.4f} {best_order[1]:>8.4f} {best_order[2]:>8.4f}")

valid_nn = [r for r in results if r[0] > 0.05]
best_nn = min(valid_nn, key=lambda x: x[1])
print(f"{'Best NN-dist':>14} {best_nn[4]:>4} {best_nn[5]:>6} {best_nn[6]:>6} {best_nn[7]:>5} | {best_nn[0]:>8.4f} {best_nn[1]:>8.4f} {best_nn[2]:>8.4f}")

best_r = max(results, key=lambda x: x[2])
print(f"{'Best Ratio':>14} {best_r[4]:>4} {best_r[5]:>6} {best_r[6]:>6} {best_r[7]:>5} | {best_r[0]:>8.4f} {best_r[1]:>8.4f} {best_r[2]:>8.4f}")
