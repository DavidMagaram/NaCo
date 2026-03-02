import pandas as pd
import numpy as np
import subprocess
import glob
import os

CELLS = 120
OBSTACLE_COUNTS = [0, 9, 25, 49]
RESULTS_DIR = "results"

def run_simulation(cells, obstacles):
    """Run Final_final4.js and return the log filename."""
    log_file = os.path.join(RESULTS_DIR, f"log_cells{cells}_obs{obstacles}.txt")
    print(f"  Running simulation...")
    with open(log_file, "w") as f:
        subprocess.run(
            ["node", "Final_final4.js", "--cells", str(cells), "--obstacles", str(obstacles)],
            stdout=f, check=True
        )
    return log_file

def make_gif(cells, obstacles):
    """Create a gif from the simulation frames."""
    gif_file = os.path.join(RESULTS_DIR, f"output_cells{cells}_obs{obstacles}.gif")
    print(f"  Creating gif...")
    subprocess.run([
        "ffmpeg", "-y", "-framerate", "10", "-start_number", "0",
        "-i", "img/simulation-t%d.png",
        "-vf", "split[s0][s1];[s0]palettegen=max_colors=256:stats_mode=full[p];[s1][p]paletteuse=dither=floyd_steinberg",
        gif_file
    ], check=True, capture_output=True)
    return gif_file

def analyze_speeds(log_file):
    """Analyze cell speeds from a simulation log. Returns a DataFrame of per-cell stats."""
    df = pd.read_csv(log_file, sep='\t', names=['time', 'cellID', 'cellType', 'x', 'y'])
    # Filter to only active/moving cells (cellType 1), exclude background (0) and obstacles (2)
    df = df[df['cellType'] == 1]

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

    return pd.DataFrame(speeds)

def print_stats(result, cells, obstacles):
    """Print speed/distance statistics for a single run."""
    print(f"\n  Dataset: {len(result)} cells tracked")
    print(f"  Mean speed:     {result['avg_speed'].mean():.4f} px/step")
    print(f"  Std dev:        {result['avg_speed'].std():.4f}")
    print(f"  Fastest cell:   {result['avg_speed'].max():.4f}")
    print(f"  Slowest cell:   {result['avg_speed'].min():.4f}")
    print(f"  Mean distance:  {result['total_distance'].mean():.2f} px")

def clean_images():
    for f in glob.glob("img/*.png"):
        os.remove(f)

if __name__ == "__main__":
    os.makedirs(RESULTS_DIR, exist_ok=True)

    all_results = []

    for obs in OBSTACLE_COUNTS:
        print("=" * 50)
        print(f"cells={CELLS}, obstacles={obs}")
        print("=" * 50)

        clean_images()
        log_file = run_simulation(CELLS, obs)
        gif_file = make_gif(CELLS, obs)
        result = analyze_speeds(log_file)
        result['cells'] = CELLS
        result['obstacles'] = obs
        all_results.append(result)

        # Save per-run stats
        stats_file = os.path.join(RESULTS_DIR, f"speedcheck_cells{CELLS}_obs{obs}.txt")
        with open(stats_file, "w") as f:
            f.write(f"cells={CELLS}, obstacles={obs}\n")
            f.write(f"Mean speed:     {result['avg_speed'].mean():.4f}\n")
            f.write(f"Std dev:        {result['avg_speed'].std():.4f}\n")
            f.write(f"Fastest cell:   {result['avg_speed'].max():.4f}\n")
            f.write(f"Slowest cell:   {result['avg_speed'].min():.4f}\n")
            f.write(f"Mean distance:  {result['total_distance'].mean():.2f}\n")

        print_stats(result, CELLS, obs)
        print(f"  -> {gif_file}, {stats_file}")
        print()

    # Build summary table
    summary = []
    for r in all_results:
        obs = r['obstacles'].iloc[0]
        summary.append({
            'obstacles': obs,
            'mean_speed': r['avg_speed'].mean(),
            'std_speed': r['avg_speed'].std(),
            'max_speed': r['avg_speed'].max(),
            'min_speed': r['avg_speed'].min(),
            'mean_dist': r['total_distance'].mean(),
        })

    # Print summary comparison
    print("=" * 50)
    print("SUMMARY COMPARISON")
    print("=" * 50)
    for s in summary:
        print(f"  Obs={s['obstacles']:>3}: "
              f"speed={s['mean_speed']:.4f} +/- {s['std_speed']:.4f}, "
              f"dist={s['mean_dist']:.2f}")

    # Write LaTeX table
    latex_file = os.path.join(RESULTS_DIR, "results_table.tex")
    with open(latex_file, "w") as f:
        f.write("\\begin{table}[h]\n")
        f.write("\\centering\n")
        f.write(f"\\caption{{Cell migration speed and distance "
                f"for varying obstacle counts "
                f"($N={CELLS}$ cells).}}\n")
        f.write("\\label{tab:speedcheck}\n")
        f.write("\\begin{tabular}{r r r r r r}\n")
        f.write("\\toprule\n")
        f.write("Obstacles & Mean Speed & Std Dev "
                "& Max Speed & Min Speed & Mean Distance \\\\\n")
        f.write("\\midrule\n")
        for s in summary:
            f.write(f"{s['obstacles']} "
                    f"& {s['mean_speed']:.4f} "
                    f"& {s['std_speed']:.4f} "
                    f"& {s['max_speed']:.4f} "
                    f"& {s['min_speed']:.4f} "
                    f"& {s['mean_dist']:.2f} \\\\\n")
        f.write("\\bottomrule\n")
        f.write("\\end{tabular}\n")
        f.write("\\end{table}\n")

    print(f"\nLaTeX table written to {latex_file}")
    print("All experiments complete!")
