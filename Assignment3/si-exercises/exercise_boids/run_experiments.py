#!/usr/bin/env python3
"""Run boids simulation with different parameter combinations and log results."""

import subprocess
import itertools
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
NODE_SCRIPT = os.path.join(SCRIPT_DIR, "node-boids.js")
LOG_FILE = os.path.join(SCRIPT_DIR, "experiment_results.log")

# Parameter grid - adjust these to explore different values
param_grid = {
    "innerRadius": [5, 10, 20],
    "outerRadius": [25, 40],
    "alignment": [0, 0.33, 0.66, 1],
    "cohesion": [0, 0.33, 0.66, 1],
    "separation": [0, 0.33, 0.66, 1],
    "N": [150],
}

TIMESTEPS = 300
NUM_REPEATS = 3  # repeat each config to average over randomness


def run_boids(inner_r, outer_r, alignment, cohesion, separation, n_boids):
    """Run a single boids simulation, return parsed output lines."""
    cmd = [
        "node", NODE_SCRIPT,
        "--i", str(inner_r),
        "--o", str(outer_r),
        "--a", str(alignment),
        "--c", str(cohesion),
        "--s", str(separation),
        "--N", str(n_boids),
        "--T", str(TIMESTEPS),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        return None
    lines = result.stdout.strip().split("\n")
    return lines


def main():
    keys = list(param_grid.keys())
    values = list(param_grid.values())
    combos = list(itertools.product(*values))
    total = len(combos) * NUM_REPEATS

    print(f"Running {len(combos)} parameter combinations x {NUM_REPEATS} repeats = {total} runs")

    with open(LOG_FILE, "w") as f:
        f.write(f"Boids Experiment Log - {datetime.now().isoformat()}\n")
        f.write(f"Repeats per config: {NUM_REPEATS}\n")
        f.write("=" * 80 + "\n\n")

        for idx, combo in enumerate(combos):
            params = dict(zip(keys, combo))
            inner_r = params["innerRadius"]
            outer_r = params["outerRadius"]
            alignment = params["alignment"]
            cohesion = params["cohesion"]
            separation = params["separation"]
            n_boids = params["N"]

            # Skip invalid combos where inner >= outer
            if inner_r >= outer_r:
                continue

            header = (
                f"Config #{idx+1}: "
                f"innerR={inner_r}, outerR={outer_r}, "
                f"align={alignment}, cohesion={cohesion}, separation={separation}, "
                f"N={n_boids}"
            )
            print(header)
            f.write(header + "\n")
            f.write("-" * 60 + "\n")
            f.write(f"{'repeat':<8} {'time':<8} {'order_param':<20} {'nn_distance':<20}\n")

            for repeat in range(NUM_REPEATS):
                lines = run_boids(inner_r, outer_r, alignment, cohesion, separation, n_boids)
                if lines is None:
                    f.write(f"  repeat {repeat+1}: FAILED\n")
                    continue
                for line in lines:
                    parts = line.split(",")
                    t, order, nn_dist = parts[0], parts[1], parts[2]
                    f.write(f"{repeat+1:<8} {t:<8} {order:<20} {nn_dist:<20}\n")

            f.write("\n")
            f.flush()

    print(f"\nDone! Results written to {LOG_FILE}")


if __name__ == "__main__":
    main()
