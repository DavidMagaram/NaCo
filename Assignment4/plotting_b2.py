"""
Plotting utilities for Exercise B.2 — TSP EA vs Memetic Algorithm.
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_convergence_generations(results, title="Convergence (generation-based)"):
    """
    Plot best distance vs generation for EA and MA.
    Shows mean +/- std across runs.
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    for algo, label, color in [("ea", "Simple EA", "tab:blue"),
                                ("ma", "MA (EA + 2-opt)", "tab:orange")]:
        histories = [r["best_distance_history"] for r in results[algo]]
        max_len = max(len(h) for h in histories)
        padded = np.array([h + [h[-1]] * (max_len - len(h)) for h in histories])
        mean = padded.mean(axis=0)
        std = padded.std(axis=0)
        gens = np.arange(max_len)
        ax.plot(gens, mean, label=label, color=color)
        ax.fill_between(gens, mean - std, mean + std, alpha=0.2, color=color)

    ax.set_xlabel("Generation")
    ax.set_ylabel("Best tour distance")
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    return fig


def plot_convergence_timed(results, title="Convergence (time-based)"):
    """
    Plot best distance vs generation for EA and MA under equal time budgets.
    Shows mean +/- std across runs.
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    for algo, label, color in [("ea", "Simple EA", "tab:blue"),
                                ("ma", "MA (EA + 2-opt)", "tab:orange")]:
        histories = [r["best_distance_history"] for r in results[algo]]
        max_len = max(len(h) for h in histories)
        padded = np.array([h + [h[-1]] * (max_len - len(h)) for h in histories])
        mean = padded.mean(axis=0)
        std = padded.std(axis=0)
        gens = np.arange(max_len)
        ax.plot(gens, mean, label=label, color=color)
        ax.fill_between(gens, mean - std, mean + std, alpha=0.2, color=color)

    ax.set_xlabel("Generation (equal wall-clock time)")
    ax.set_ylabel("Best tour distance")
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    return fig


def plot_final_distances(results, title="Final best distances"):
    """
    Box plot comparing final best distances of EA vs MA.
    """
    fig, ax = plt.subplots(figsize=(7, 5))

    ea_dists = [r["best_distance"] for r in results["ea"]]
    ma_dists = [r["best_distance"] for r in results["ma"]]

    bp = ax.boxplot([ea_dists, ma_dists], labels=["Simple EA", "MA (EA + 2-opt)"],
                    patch_artist=True)
    bp["boxes"][0].set_facecolor("tab:blue")
    bp["boxes"][1].set_facecolor("tab:orange")
    for box in bp["boxes"]:
        box.set_alpha(0.5)

    ax.set_ylabel("Best tour distance")
    ax.set_title(title)
    plt.tight_layout()
    return fig


def plot_tour(coords, tour, title="Tour", ax=None):
    """Plot a TSP tour on a 2D coordinate map."""
    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 7))
    else:
        fig = ax.figure

    ordered = [coords[i] for i in tour] + [coords[tour[0]]]
    xs = [c[0] for c in ordered]
    ys = [c[1] for c in ordered]
    ax.plot(xs, ys, "o-", markersize=5, linewidth=1)
    for i, (x, y) in enumerate(coords):
        ax.annotate(str(i), (x, y), fontsize=6, ha="center", va="bottom")
    ax.set_title(title)
    ax.set_aspect("equal")
    return fig


def plot_time_comparison(results_gen, title="Time per run"):
    """
    Bar chart showing wall-clock time used by EA and MA in generation-based runs.
    """
    fig, ax = plt.subplots(figsize=(7, 5))

    ea_times = [r["elapsed"] for r in results_gen["ea"]]
    ma_times = [r["elapsed"] for r in results_gen["ma"]]

    x = np.arange(2)
    ax.bar(x, [np.mean(ea_times), np.mean(ma_times)],
           yerr=[np.std(ea_times), np.std(ma_times)],
           color=["tab:blue", "tab:orange"], alpha=0.7, capsize=5)
    ax.set_xticks(x)
    ax.set_xticklabels(["Simple EA", "MA (EA + 2-opt)"])
    ax.set_ylabel("Wall-clock time (s)")
    ax.set_title(title)
    plt.tight_layout()
    return fig


def summary_table(results, dataset_name):
    """Print a summary table of results."""
    print(f"\n{'='*60}")
    print(f"  {dataset_name}")
    print(f"{'='*60}")
    for algo, label in [("ea", "Simple EA"), ("ma", "MA (EA + 2-opt)")]:
        dists = [r["best_distance"] for r in results[algo]]
        print(f"  {label}:")
        print(f"    Best distance: {np.min(dists):.2f}")
        print(f"    Mean distance: {np.mean(dists):.2f} +/- {np.std(dists):.2f}")
        if "elapsed" in results[algo][0]:
            times = [r["elapsed"] for r in results[algo]]
            print(f"    Mean time:     {np.mean(times):.1f}s")
        if "generations" in results[algo][0]:
            gens = [r["generations"] for r in results[algo]]
            print(f"    Mean gens:     {np.mean(gens):.0f}")
    print()
