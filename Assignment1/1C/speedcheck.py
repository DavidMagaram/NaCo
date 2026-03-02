import pandas as pd
import numpy as np
import subprocess
import glob
import os

CELLS = 50
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

def torus_diff(d, L):
    """Minimum image convention: wrap displacements to [-L/2, L/2]."""
    return ((d + L / 2) % L) - L / 2

def analyze(log_file, field_size=(200, 200)):
    """Analyze cell speeds and alignment from a simulation log."""
    df = pd.read_csv(log_file, sep='\t', names=['time', 'cellID', 'cellType', 'x', 'y'])
    # Filter to only active/moving cells (cellType 1), exclude background (0) and obstacles (2)
    df = df[df['cellType'] == 1]

    # Per-cell: compute velocity vectors using torus-aware displacements
    df = df.sort_values(['cellID', 'time'])
    df['dx'] = df.groupby('cellID')['x'].diff().transform(lambda d: torus_diff(d, field_size[0]))
    df['dy'] = df.groupby('cellID')['y'].diff().transform(lambda d: torus_diff(d, field_size[1]))
    df['dt'] = df.groupby('cellID')['time'].diff()
    df['displacement'] = np.sqrt(df['dx']**2 + df['dy']**2)
    df['speed'] = df['displacement'] / df['dt']

    # Per-cell summary
    per_cell = df.groupby('cellID').agg(
        avg_speed=('speed', 'mean'),
        max_speed=('speed', 'max'),
        total_distance=('displacement', 'sum')
    ).reset_index()

    # Alignment order parameter (Vicsek) per timestep:
    # phi(t) = |mean unit velocity vector| across all cells at time t
    # Ranges from 0 (random) to 1 (perfectly aligned)
    valid = df.dropna(subset=['dx', 'dy']).copy()
    valid = valid[valid['displacement'] > 0]
    valid['ux'] = valid['dx'] / valid['displacement']
    valid['uy'] = valid['dy'] / valid['displacement']
    alignment_per_t = valid.groupby('time').apply(
        lambda g: np.sqrt(g['ux'].mean()**2 + g['uy'].mean()**2)
    )
    mean_alignment = alignment_per_t.mean()
    std_alignment = alignment_per_t.std()

    return per_cell, mean_alignment, std_alignment

def print_stats(result, mean_alignment, std_alignment):
    """Print speed/distance/alignment statistics for a single run."""
    print(f"\n  Dataset: {len(result)} cells tracked")
    print(f"  Mean speed:     {result['avg_speed'].mean():.4f} px/step")
    print(f"  Std dev:        {result['avg_speed'].std():.4f}")
    print(f"  Fastest cell:   {result['avg_speed'].max():.4f}")
    print(f"  Slowest cell:   {result['avg_speed'].min():.4f}")
    print(f"  Mean distance:  {result['total_distance'].mean():.2f} px")
    print(f"  Alignment:      {mean_alignment:.4f} +/- {std_alignment:.4f}")

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
        result, mean_align, std_align = analyze(log_file)
        result['cells'] = CELLS
        result['obstacles'] = obs
        result['mean_alignment'] = mean_align
        result['std_alignment'] = std_align
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
            f.write(f"Alignment:      {mean_align:.4f} +/- {std_align:.4f}\n")

        print_stats(result, mean_align, std_align)
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
            'alignment': r['mean_alignment'].iloc[0],
            'alignment_std': r['std_alignment'].iloc[0],
        })

    # Print summary comparison
    print("=" * 50)
    print("SUMMARY COMPARISON")
    print("=" * 50)
    for s in summary:
        print(f"  Obs={s['obstacles']:>3}: "
              f"speed={s['mean_speed']:.4f} +/- {s['std_speed']:.4f}, "
              f"dist={s['mean_dist']:.2f}, "
              f"alignment={s['alignment']:.4f} +/- {s['alignment_std']:.4f}")

    # Write LaTeX table
    latex_file = os.path.join(RESULTS_DIR, "results_table.tex")
    with open(latex_file, "w") as f:
        f.write("\\begin{table}[h]\n")
        f.write("\\centering\n")
        f.write(f"\\caption{{Cell migration speed, distance, and alignment "
                f"for varying obstacle counts "
                f"($N={CELLS}$ cells).}}\n")
        f.write("\\label{tab:speedcheck}\n")
        f.write("\\begin{tabular}{r r r r r}\n")
        f.write("\\toprule\n")
        f.write("Obstacles & Mean Speed & Std Dev "
                "& Mean Distance & Alignment ($\\phi$) \\\\\n")
        f.write("\\midrule\n")
        for s in summary:
            f.write(f"{s['obstacles']} "
                    f"& {s['mean_speed']:.4f} "
                    f"& {s['std_speed']:.4f} "
                    f"& {s['mean_dist']:.2f} "
                    f"& {s['alignment']:.4f} $\\pm$ {s['alignment_std']:.4f} \\\\\n")
        f.write("\\bottomrule\n")
        f.write("\\end{tabular}\n")
        f.write("\\end{table}\n")

    print(f"\nLaTeX table written to {latex_file}")
    print("All experiments complete!")
