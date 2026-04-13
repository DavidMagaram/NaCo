"""
Experiment runners for Exercise B.1.

Each function runs one of the sub-exercises and returns structured results
ready for plotting.
"""

import numpy as np
from string_ga import run_ga

TARGET = "NaturalComputing"  # 16 characters, ~15 as requested


def experiment_b1_1(n_runs=10, G_max=100, N=200):
    """
    B.1.1: K=2, mu=1/L, 10 runs. Measure t_finish.
    """
    L = len(TARGET)
    mu = 1 / L
    K = 2
    results = []
    for i in range(n_runs):
        t_finish, history, _ = run_ga(TARGET, K=K, mu=mu, N=N, G_max=G_max)
        results.append({
            "run": i,
            "t_finish": t_finish,
            "fitness_history": history,
        })
        status = t_finish if t_finish is not None else f"not found in {G_max}"
        print(f"  Run {i+1}/{n_runs}: t_finish = {status}")
    return results


def experiment_b1_2(n_runs=10, G_max=100, N=200):
    """
    B.1.2: Compare mu=0, mu=1/L, mu=3/L with K=2.
    Returns dict mapping mu_label -> list of t_finish values.
    """
    L = len(TARGET)
    K = 2
    mu_configs = {
        "mu=0": 0,
        "mu=1/L": 1 / L,
        "mu=3/L": 3 / L,
    }
    all_results = {}
    for label, mu in mu_configs.items():
        print(f"  Running {label}...")
        t_finishes = []
        for i in range(n_runs):
            t_finish, _, _ = run_ga(TARGET, K=K, mu=mu, N=N, G_max=G_max)
            t_finishes.append(t_finish)
        all_results[label] = t_finishes
        found = sum(1 for t in t_finishes if t is not None)
        print(f"    Found target in {found}/{n_runs} runs")
    return all_results


def experiment_b1_3(n_runs=10, G_max=100, N=200):
    """
    B.1.3: Rerun B.1.1 and B.1.2 with diversity tracking.
    Returns dict mapping mu_label -> list of run dicts with diversity data.
    """
    L = len(TARGET)
    K = 2
    mu_configs = {
        "mu=0": 0,
        "mu=1/L": 1 / L,
        "mu=3/L": 3 / L,
    }
    all_results = {}
    for label, mu in mu_configs.items():
        print(f"  Running {label} with diversity tracking...")
        runs = []
        for i in range(n_runs):
            t_finish, history, diversity = run_ga(
                TARGET, K=K, mu=mu, N=N, G_max=G_max,
                track_diversity=True, diversity_interval=10,
            )
            runs.append({
                "t_finish": t_finish,
                "fitness_history": history,
                "diversity_history": diversity,
            })
        all_results[label] = runs
        found = sum(1 for r in runs if r["t_finish"] is not None)
        print(f"    Found target in {found}/{n_runs} runs")
    return all_results


def experiment_b1_5(n_runs=10, G_max=100, N=200):
    """
    B.1.5: Sweep mu from 0 to higher values, measure t_finish. K=2.
    """
    L = len(TARGET)
    K = 2
    mu_values = np.linspace(0, 10 / L, 11)  # 0, 1/L, 2/L, ... 10/L
    results = {}
    for mu in mu_values:
        label = f"{mu*L:.1f}/L"
        print(f"  Running mu = {label}...")
        t_finishes = []
        for _ in range(n_runs):
            t_finish, _, _ = run_ga(TARGET, K=K, mu=mu, N=N, G_max=G_max)
            t_finishes.append(t_finish)
        results[mu] = t_finishes
        found = sum(1 for t in t_finishes if t is not None)
        print(f"    Found target in {found}/{n_runs} runs")
    return results


def experiment_b1_6(n_runs=10, G_max=100, N=200):
    """
    B.1.6: Repeat B.1.5 with K=5.
    """
    L = len(TARGET)
    K = 5
    mu_values = np.linspace(0, 10 / L, 11)
    results = {}
    for mu in mu_values:
        label = f"{mu*L:.1f}/L"
        print(f"  Running mu = {label} (K=5)...")
        t_finishes = []
        for _ in range(n_runs):
            t_finish, _, _ = run_ga(TARGET, K=K, mu=mu, N=N, G_max=G_max)
            t_finishes.append(t_finish)
        results[mu] = t_finishes
        found = sum(1 for t in t_finishes if t is not None)
        print(f"    Found target in {found}/{n_runs} runs")
    return results
