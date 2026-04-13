"""
Plotting utilities for Exercise B.1.
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_fitness_curves(results, title="Best fitness over generations"):
    """Plot best fitness per generation for multiple runs."""
    fig, ax = plt.subplots(figsize=(10, 5))
    for r in results:
        label = f"Run {r['run']}"
        ax.plot(r["fitness_history"], alpha=0.5, label=label)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Best fitness")
    ax.set_title(title)
    ax.legend(fontsize=7, ncol=2)
    plt.tight_layout()
    return fig


def plot_beeswarm(data_dict, G_max, title="t_finish distribution (beeswarm)"):
    """
    Beeswarm-style strip plot of t_finish values.
    None values (target not found) are plotted at G_max with a distinct marker.

    data_dict: {label: [t_finish or None, ...]}
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    labels = list(data_dict.keys())
    for i, label in enumerate(labels):
        values = data_dict[label]
        found = [v for v in values if v is not None]
        not_found_count = sum(1 for v in values if v is None)

        # Jitter for visibility
        jitter = np.random.normal(0, 0.05, len(found))
        ax.scatter(
            [i] * len(found) + jitter[:len(found)], found,
            alpha=0.7, s=40, zorder=3, label=f"{label} (found)" if i == 0 else None,
        )
        if not_found_count > 0:
            jitter_nf = np.random.normal(0, 0.05, not_found_count)
            ax.scatter(
                [i] * not_found_count + jitter_nf, [G_max] * not_found_count,
                alpha=0.7, s=40, marker="x", color="red", zorder=3,
            )

    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_ylabel("t_finish (generations)")
    ax.axhline(G_max, color="red", linestyle="--", alpha=0.3, label=f"G_max={G_max}")
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    return fig


def plot_diversity(diversity_results, title_prefix="Diversity"):
    """
    Plot mean entropy and mean Hamming distance over generations for each mu config.

    diversity_results: {label: [run_dicts]} where each run_dict has 'diversity_history'
                       as [(gen, entropy, hamming), ...]
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    for label, runs in diversity_results.items():
        # Aggregate diversity across runs: collect all snapshots, group by generation
        all_gens = {}
        for run in runs:
            for gen, ent, ham in run["diversity_history"]:
                if gen not in all_gens:
                    all_gens[gen] = {"ent": [], "ham": []}
                all_gens[gen]["ent"].append(ent)
                all_gens[gen]["ham"].append(ham)

        gens = sorted(all_gens.keys())
        mean_ent = [np.mean(all_gens[g]["ent"]) for g in gens]
        mean_ham = [np.mean(all_gens[g]["ham"]) for g in gens]

        axes[0].plot(gens, mean_ent, marker="o", markersize=3, label=label)
        axes[1].plot(gens, mean_ham, marker="o", markersize=3, label=label)

    axes[0].set_xlabel("Generation")
    axes[0].set_ylabel("Mean Shannon entropy")
    axes[0].set_title(f"{title_prefix} — Shannon entropy")
    axes[0].legend()

    axes[1].set_xlabel("Generation")
    axes[1].set_ylabel("Mean Hamming distance")
    axes[1].set_title(f"{title_prefix} — Hamming distance")
    axes[1].legend()

    plt.tight_layout()
    return fig


def plot_mu_vs_tfinish(sweep_results, G_max, L, K_label="K=2"):
    """
    Plot mu vs mean t_finish from a sweep experiment.
    None values count as G_max for the mean.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    mus = sorted(sweep_results.keys())
    mu_labels = [f"{mu*L:.1f}/L" for mu in mus]
    means = []
    for mu in mus:
        vals = [v if v is not None else G_max for v in sweep_results[mu]]
        means.append(np.mean(vals))

    ax.plot(mus, means, marker="o")
    ax.set_xticks(mus)
    ax.set_xticklabels(mu_labels, rotation=45)
    ax.set_xlabel("Mutation rate (mu)")
    ax.set_ylabel(f"Mean t_finish (capped at G_max={G_max})")
    ax.set_title(f"Mutation rate vs. convergence time ({K_label})")
    plt.tight_layout()
    return fig


def plot_mu_sweep_comparison(results_k2, results_k5, G_max, L):
    """Plot mu vs t_finish for K=2 and K=5 side by side."""
    fig, ax = plt.subplots(figsize=(10, 5))

    for results, label in [(results_k2, "K=2"), (results_k5, "K=5")]:
        mus = sorted(results.keys())
        means = []
        for mu in mus:
            vals = [v if v is not None else G_max for v in results[mu]]
            means.append(np.mean(vals))
        ax.plot(mus, means, marker="o", label=label)

    mu_labels = [f"{mu*L:.1f}/L" for mu in sorted(results_k2.keys())]
    ax.set_xticks(sorted(results_k2.keys()))
    ax.set_xticklabels(mu_labels, rotation=45)
    ax.set_xlabel("Mutation rate (mu)")
    ax.set_ylabel(f"Mean t_finish (capped at G_max={G_max})")
    ax.set_title("Mutation rate vs. convergence time — K=2 vs K=5")
    ax.legend()
    plt.tight_layout()
    return fig
