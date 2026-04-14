import matplotlib.pyplot as plt
import numpy as np


def plot_fitness_curves(results, title="Best fitness over generations"):
    fig, ax = plt.subplots(figsize=(10, 5))

    max_len = max(len(r["fitness_history"]) for r in results)
    padded = []
    for r in results:
        h = list(r["fitness_history"])
        if len(h) < max_len:
            h.extend([h[-1]] * (max_len - len(h)))
        padded.append(h)
    arr = np.array(padded)

    gens = np.arange(max_len)
    median = np.median(arr, axis=0)
    lo = np.percentile(arr, 2.5, axis=0)
    hi = np.percentile(arr, 97.5, axis=0)

    ax.plot(gens, median, color="C0", linewidth=2, label="Median")
    ax.fill_between(gens, lo, hi, color="C0", alpha=0.2, label="95% CI")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Best fitness")
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    return fig


def plot_beeswarm(data_dict, G_max, title="t_finish distribution (beeswarm)"):
    fig, ax = plt.subplots(figsize=(8, 5))
    labels = list(data_dict.keys())
    added_found_label = False
    added_capped_label = False
    for i, label in enumerate(labels):
        values = data_dict[label]
        found = [v for v in values if v is not None]
        not_found_count = sum(1 for v in values if v is None)

        jitter = np.random.normal(0, 0.05, len(found))
        lbl = "Found" if not added_found_label and found else None
        if found:
            added_found_label = True
        ax.scatter(
            [i] * len(found) + jitter[: len(found)],
            found,
            alpha=0.7,
            s=50,
            zorder=3,
            color="C0",
            label=lbl,
        )
        if not_found_count > 0:
            jitter_nf = np.random.normal(0, 0.05, not_found_count)
            lbl_nf = (
                f"Not found (capped at {G_max})" if not added_capped_label else None
            )
            added_capped_label = True
            ax.scatter(
                [i] * not_found_count + jitter_nf,
                [G_max] * not_found_count,
                alpha=0.8,
                s=60,
                marker="^",
                color="red",
                zorder=3,
                label=lbl_nf,
            )

    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_ylabel("t_finish (generations)")
    ax.axhline(G_max, color="red", linestyle="--", alpha=0.3)
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    return fig


def plot_diversity(diversity_results, title_prefix="Diversity"):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    for label, runs in diversity_results.items():
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
    axes[0].set_title(f"{title_prefix} - Shannon entropy")
    axes[0].legend()

    axes[1].set_xlabel("Generation")
    axes[1].set_ylabel("Mean Hamming distance")
    axes[1].set_title(f"{title_prefix} - Hamming distance")
    axes[1].legend()

    plt.tight_layout()
    return fig


def plot_mu_sweep_single(ax, sweep_results, G_max, L, color="C0", label=None):
    mus = sorted(sweep_results.keys())
    for mu in mus:
        vals = sweep_results[mu]
        found = [v for v in vals if v is not None]
        n_capped = sum(1 for v in vals if v is None)

        jitter = (
            np.random.normal(0, (mus[1] - mus[0]) * 0.06, len(found))
            if len(mus) > 1
            else 0
        )
        if found:
            ax.scatter(
                mu + jitter[: len(found)]
                if hasattr(jitter, "__len__")
                else [mu] * len(found),
                found,
                alpha=0.5,
                s=30,
                color=color,
                zorder=3,
            )
        if n_capped > 0:
            jitter_c = (
                np.random.normal(0, (mus[1] - mus[0]) * 0.06, n_capped)
                if len(mus) > 1
                else 0
            )
            ax.scatter(
                mu + jitter_c[:n_capped]
                if hasattr(jitter_c, "__len__")
                else [mu] * n_capped,
                [G_max] * n_capped,
                alpha=0.7,
                s=40,
                marker="^",
                color="red",
                zorder=3,
            )

    means = []
    for mu in mus:
        vals = [v if v is not None else G_max for v in sweep_results[mu]]
        means.append(np.mean(vals))
    ax.plot(
        mus,
        means,
        marker="o",
        markersize=6,
        color=color,
        linewidth=1.5,
        alpha=0.8,
        label=label or "Mean",
        zorder=4,
    )


def plot_mu_vs_tfinish(sweep_results, G_max, L, K_label="K=2"):
    fig, ax = plt.subplots(figsize=(10, 5))
    mus = sorted(sweep_results.keys())
    mu_labels = [f"{mu * L:.1f}/L" for mu in mus]

    plot_mu_sweep_single(
        ax, sweep_results, G_max, L, color="C0", label=f"Mean ({K_label})"
    )

    ax.axhline(G_max, color="red", linestyle="--", alpha=0.3, label=f"G_max={G_max}")
    ax.scatter([], [], marker="^", color="red", s=40, label="Capped at G_max")

    ax.set_xticks(mus)
    ax.set_xticklabels(mu_labels, rotation=45)
    ax.set_xlabel("Mutation rate (mu)")
    ax.set_ylabel("t_finish (generations)")
    ax.set_title(f"Mutation rate vs. convergence time ({K_label})")
    ax.legend()
    plt.tight_layout()
    return fig


def plot_mu_sweep_comparison(results_k2, results_k5, G_max, L):
    fig, ax = plt.subplots(figsize=(10, 5))

    plot_mu_sweep_single(ax, results_k2, G_max, L, color="C0", label="K=2 (mean)")
    plot_mu_sweep_single(ax, results_k5, G_max, L, color="C1", label="K=5 (mean)")

    ax.axhline(G_max, color="red", linestyle="--", alpha=0.3, label=f"G_max={G_max}")
    ax.scatter([], [], marker="^", color="red", s=40, label="Capped at G_max")

    mu_labels = [f"{mu * L:.1f}/L" for mu in sorted(results_k2.keys())]
    ax.set_xticks(sorted(results_k2.keys()))
    ax.set_xticklabels(mu_labels, rotation=45)
    ax.set_xlabel("Mutation rate (mu)")
    ax.set_ylabel("t_finish (generations)")
    ax.set_title("Mutation rate vs. convergence time - K=2 vs K=5")
    ax.legend()
    plt.tight_layout()
    return fig
