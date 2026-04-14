import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch


def plot_convergence_generations(results, title="Convergence (generation-based)"):
    fig, ax = plt.subplots(figsize=(10, 5))

    for algo, label, color in [
        ("ea", "Simple EA", "tab:blue"),
        ("ma", "MA (EA + 2-opt)", "tab:orange"),
    ]:
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
    fig, ax = plt.subplots(figsize=(10, 5))

    max_time = max(
        max(r["time_history"][-1] for r in results[algo]) for algo in ("ea", "ma")
    )
    time_grid = np.linspace(0, max_time, 500)

    for algo, label, color in [
        ("ea", "Simple EA", "tab:blue"),
        ("ma", "MA (EA + 2-opt)", "tab:orange"),
    ]:
        interpolated = []
        for r in results[algo]:
            t = np.array(r["time_history"])
            d = np.array(r["best_distance_history"])
            interp = np.interp(time_grid, t, d)
            interpolated.append(interp)
        interpolated = np.array(interpolated)
        mean = interpolated.mean(axis=0)
        std = interpolated.std(axis=0)

        mean_gens = np.mean([r["generations"] for r in results[algo]])
        ax.plot(time_grid, mean, label=f"{label} (~{mean_gens:.0f} gens)", color=color)
        ax.fill_between(time_grid, mean - std, mean + std, alpha=0.2, color=color)

    ax.set_xlabel("Wall-clock time (s)")
    ax.set_ylabel("Best tour distance")
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    return fig


def plot_final_distances(results, title="Final best distances"):
    fig, ax = plt.subplots(figsize=(7, 5))

    ea_dists = [r["best_distance"] for r in results["ea"]]
    ma_dists = [r["best_distance"] for r in results["ma"]]

    bp = ax.boxplot(
        [ea_dists, ma_dists], labels=["Simple EA", "MA (EA + 2-opt)"], patch_artist=True
    )
    bp["boxes"][0].set_facecolor("tab:blue")
    bp["boxes"][1].set_facecolor("tab:orange")
    for box in bp["boxes"]:
        box.set_alpha(0.5)

    ax.set_ylabel("Best tour distance")
    ax.set_title(title)
    plt.tight_layout()
    return fig


def plot_tour(coords, tour, title="Tour", ax=None):
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
    fig, ax = plt.subplots(figsize=(7, 5))

    ea_times = [r["elapsed"] for r in results_gen["ea"]]
    ma_times = [r["elapsed"] for r in results_gen["ma"]]

    x = np.arange(2)
    ax.bar(
        x,
        [np.mean(ea_times), np.mean(ma_times)],
        yerr=[np.std(ea_times), np.std(ma_times)],
        color=["tab:blue", "tab:orange"],
        alpha=0.7,
        capsize=5,
    )
    ax.set_xticks(x)
    ax.set_xticklabels(["Simple EA", "MA (EA + 2-opt)"])
    ax.set_ylabel("Wall-clock time (s)")
    ax.set_title(title)
    plt.tight_layout()
    return fig


def plot_convergence_gen_ax(ax, results):
    for algo, label, color in [
        ("ea", "Simple EA", "tab:blue"),
        ("ma", "MA (EA + 2-opt)", "tab:orange"),
    ]:
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
    ax.legend()


def plot_convergence_timed_ax(ax, results):
    max_time = max(
        max(r["time_history"][-1] for r in results[algo]) for algo in ("ea", "ma")
    )
    time_grid = np.linspace(0, max_time, 500)
    for algo, label, color in [
        ("ea", "Simple EA", "tab:blue"),
        ("ma", "MA (EA + 2-opt)", "tab:orange"),
    ]:
        interpolated = []
        for r in results[algo]:
            t = np.array(r["time_history"])
            d = np.array(r["best_distance_history"])
            interp = np.interp(time_grid, t, d)
            interpolated.append(interp)
        interpolated = np.array(interpolated)
        mean = interpolated.mean(axis=0)
        std = interpolated.std(axis=0)
        mean_gens = np.mean([r["generations"] for r in results[algo]])
        ax.plot(time_grid, mean, label=f"{label} (~{mean_gens:.0f} gens)", color=color)
        ax.fill_between(time_grid, mean - std, mean + std, alpha=0.2, color=color)
    ax.set_xlabel("Wall-clock time (s)")
    ax.set_ylabel("Best tour distance")
    ax.legend()


def plot_final_distances_ax(ax, results):
    ea_dists = [r["best_distance"] for r in results["ea"]]
    ma_dists = [r["best_distance"] for r in results["ma"]]
    bp = ax.boxplot([ea_dists, ma_dists], labels=["Simple EA", "MA"], patch_artist=True)
    bp["boxes"][0].set_facecolor("tab:blue")
    bp["boxes"][1].set_facecolor("tab:orange")
    for box in bp["boxes"]:
        box.set_alpha(0.5)
    ax.set_ylabel("Best tour distance")


def plot_time_comparison_ax(ax, results_gen):
    ea_times = [r["elapsed"] for r in results_gen["ea"]]
    ma_times = [r["elapsed"] for r in results_gen["ma"]]
    x = np.arange(2)
    ax.bar(
        x,
        [np.mean(ea_times), np.mean(ma_times)],
        yerr=[np.std(ea_times), np.std(ma_times)],
        color=["tab:blue", "tab:orange"],
        alpha=0.7,
        capsize=5,
    )
    ax.set_xticks(x)
    ax.set_xticklabels(["Simple EA", "MA"])
    ax.set_ylabel("Wall-clock time (s)")


def plot_combined_convergence_gen(
    results_custom, results_tsplib, title="Convergence (same generations)"
):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))
    plot_convergence_gen_ax(ax1, results_custom)
    ax1.set_title("Custom 50-city")
    plot_convergence_gen_ax(ax2, results_tsplib)
    ax2.set_title("TSPLIB (eil51)")
    fig.suptitle(title, fontsize=13)
    plt.tight_layout()
    return fig


def plot_combined_convergence_timed(
    results_custom, results_tsplib, title="Convergence (same wall-clock time)"
):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))
    plot_convergence_timed_ax(ax1, results_custom)
    ax1.set_title("Custom 50-city")
    plot_convergence_timed_ax(ax2, results_tsplib)
    ax2.set_title("TSPLIB (eil51)")
    fig.suptitle(title, fontsize=13)
    plt.tight_layout()
    return fig


def plot_combined_final_distances(
    results_custom, results_tsplib, title="Final best distances"
):
    fig, ax = plt.subplots(figsize=(8, 5))

    data = [
        [r["best_distance"] for r in results_custom["ea"]],
        [r["best_distance"] for r in results_custom["ma"]],
        [r["best_distance"] for r in results_tsplib["ea"]],
        [r["best_distance"] for r in results_tsplib["ma"]],
    ]
    positions = [1, 2, 4, 5]
    colors = ["tab:blue", "tab:orange", "tab:blue", "tab:orange"]

    bp = ax.boxplot(data, positions=positions, patch_artist=True, widths=0.6)
    for box, color in zip(bp["boxes"], colors):
        box.set_facecolor(color)
        box.set_alpha(0.5)

    ax.set_xticks([1.5, 4.5])
    ax.set_xticklabels(["Custom 50-city", "TSPLIB (eil51)"])
    ax.set_ylabel("Best tour distance")
    ax.set_title(title)

    ax.legend(
        handles=[
            Patch(facecolor="tab:blue", alpha=0.5, label="Simple EA"),
            Patch(facecolor="tab:orange", alpha=0.5, label="MA (EA + 2-opt)"),
        ]
    )
    plt.tight_layout()
    return fig


def plot_combined_time_comparison(
    results_gen_custom,
    results_gen_tsplib,
    title="Wall-clock time per run (same generations)",
):
    fig, ax = plt.subplots(figsize=(8, 5))

    datasets = [
        ("Custom 50-city", results_gen_custom),
        ("TSPLIB (eil51)", results_gen_tsplib),
    ]
    x = np.arange(len(datasets))
    width = 0.35

    ea_means, ea_stds, ma_means, ma_stds = [], [], [], []
    for _, results in datasets:
        ea_t = [r["elapsed"] for r in results["ea"]]
        ma_t = [r["elapsed"] for r in results["ma"]]
        ea_means.append(np.mean(ea_t))
        ea_stds.append(np.std(ea_t))
        ma_means.append(np.mean(ma_t))
        ma_stds.append(np.std(ma_t))

    ax.bar(
        x - width / 2,
        ea_means,
        width,
        yerr=ea_stds,
        label="Simple EA",
        color="tab:blue",
        alpha=0.7,
        capsize=5,
    )
    ax.bar(
        x + width / 2,
        ma_means,
        width,
        yerr=ma_stds,
        label="MA (EA + 2-opt)",
        color="tab:orange",
        alpha=0.7,
        capsize=5,
    )

    ax.set_xticks(x)
    ax.set_xticklabels([name for name, _ in datasets])
    ax.set_ylabel("Wall-clock time (s)")
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    return fig


def summary_table(results, dataset_name):
    print(f"\n{'=' * 60}")
    print(f"  {dataset_name}")
    print(f"{'=' * 60}")
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
