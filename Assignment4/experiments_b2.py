"""
Experiment runners for Exercise B.2 — Memetic algorithms for TSP.

Each function runs an experiment and returns structured results for plotting.
"""

import time
import numpy as np
from tsp_ea import (
    load_tsp_coordinates,
    load_tsplib,
    compute_distance_matrix,
    run_ea,
    run_ma,
    run_ea_timed,
    run_ma_timed,
    tour_distance,
)


def load_dataset(name, path):
    """Load a TSP dataset by name. Returns (coords, dist_matrix)."""
    if name == "file-tsp":
        coords = load_tsp_coordinates(path)
    else:
        coords = load_tsplib(path)
    dist_matrix = compute_distance_matrix(coords)
    return coords, dist_matrix


def experiment_generations(dist_matrix, n_runs=10, N=100, G_max=200, K=5,
                           p_c=0.8, mu=0.3):
    """
    B.2 generation-based comparison: run EA and MA for the same number of
    generations. This is the UNFAIR comparison to motivate time-based runs.

    Returns dict with 'ea' and 'ma' keys, each mapping to a list of run dicts.
    """
    results = {"ea": [], "ma": []}

    print("  Running simple EA...")
    for i in range(n_runs):
        t0 = time.time()
        history, best_tour, total_evals = run_ea(
            dist_matrix, N=N, G_max=G_max, K=K, p_c=p_c, mu=mu)
        elapsed = time.time() - t0
        results["ea"].append({
            "run": i,
            "best_distance_history": history,
            "best_distance": history[-1],
            "elapsed": elapsed,
        })
        print(f"    Run {i+1}/{n_runs}: best = {history[-1]:.2f}, time = {elapsed:.1f}s")

    print("  Running memetic algorithm (EA + 2-opt)...")
    for i in range(n_runs):
        t0 = time.time()
        history, best_tour, total_evals = run_ma(
            dist_matrix, N=N, G_max=G_max, K=K, p_c=p_c, mu=mu)
        elapsed = time.time() - t0
        results["ma"].append({
            "run": i,
            "best_distance_history": history,
            "best_distance": history[-1],
            "elapsed": elapsed,
        })
        print(f"    Run {i+1}/{n_runs}: best = {history[-1]:.2f}, time = {elapsed:.1f}s")

    return results


def experiment_timed(dist_matrix, n_runs=10, time_budget=30.0, N=100, K=5,
                     p_c=0.8, mu=0.3):
    """
    B.2 fair comparison: run EA and MA with the same wall-clock time budget.

    Returns dict with 'ea' and 'ma' keys.
    """
    results = {"ea": [], "ma": []}

    print(f"  Running simple EA (time budget = {time_budget}s)...")
    for i in range(n_runs):
        history, best_tour, gens = run_ea_timed(
            dist_matrix, time_budget=time_budget, N=N, K=K, p_c=p_c, mu=mu)
        results["ea"].append({
            "run": i,
            "best_distance_history": history,
            "best_distance": history[-1],
            "generations": gens,
        })
        print(f"    Run {i+1}/{n_runs}: best = {history[-1]:.2f}, gens = {gens}")

    print(f"  Running MA (time budget = {time_budget}s)...")
    for i in range(n_runs):
        history, best_tour, gens = run_ma_timed(
            dist_matrix, time_budget=time_budget, N=N, K=K, p_c=p_c, mu=mu)
        results["ma"].append({
            "run": i,
            "best_distance_history": history,
            "best_distance": history[-1],
            "generations": gens,
        })
        print(f"    Run {i+1}/{n_runs}: best = {history[-1]:.2f}, gens = {gens}")

    return results
