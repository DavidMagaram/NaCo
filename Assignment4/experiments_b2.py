import os
import time
from concurrent.futures import ProcessPoolExecutor

from tsp_ea import (
    load_tsp_coordinates,
    load_tsplib,
    compute_distance_matrix,
    run_ea,
    run_ma,
    run_ea_timed,
    run_ma_timed,
)

N_WORKERS = max(1, os.cpu_count() - 1)


def load_dataset(name, path):
    if name == "file-tsp":
        coords = load_tsp_coordinates(path)
    else:
        coords = load_tsplib(path)
    dist_matrix = compute_distance_matrix(coords)
    return coords, dist_matrix


def run_ea_gen(args):
    dist_matrix, i, N, G_max, K, p_c, mu = args
    t0 = time.time()
    history, best_tour, total_evals = run_ea(
        dist_matrix, N=N, G_max=G_max, K=K, p_c=p_c, mu=mu
    )
    elapsed = time.time() - t0
    return {
        "run": i,
        "best_distance_history": history,
        "best_distance": history[-1],
        "elapsed": elapsed,
    }


def run_ma_gen(args):
    dist_matrix, i, N, G_max, K, p_c, mu = args
    t0 = time.time()
    history, best_tour, total_evals = run_ma(
        dist_matrix, N=N, G_max=G_max, K=K, p_c=p_c, mu=mu
    )
    elapsed = time.time() - t0
    return {
        "run": i,
        "best_distance_history": history,
        "best_distance": history[-1],
        "elapsed": elapsed,
    }


def run_ea_timed_worker(args):
    dist_matrix, i, time_budget, N, K, p_c, mu = args
    history, best_tour, gens, time_hist = run_ea_timed(
        dist_matrix, time_budget=time_budget, N=N, K=K, p_c=p_c, mu=mu
    )
    return {
        "run": i,
        "best_distance_history": history,
        "time_history": time_hist,
        "best_distance": history[-1],
        "generations": gens,
    }


def run_ma_timed_worker(args):
    dist_matrix, i, time_budget, N, K, p_c, mu = args
    history, best_tour, gens, time_hist = run_ma_timed(
        dist_matrix, time_budget=time_budget, N=N, K=K, p_c=p_c, mu=mu
    )
    return {
        "run": i,
        "best_distance_history": history,
        "time_history": time_hist,
        "best_distance": history[-1],
        "generations": gens,
    }


def experiment_generations(
    dist_matrix, n_runs=10, N=100, G_max=200, K=5, p_c=0.8, mu=0.3
):
    results = {"ea": [], "ma": []}

    print(f"  Running simple EA ({n_runs} runs, {N_WORKERS} workers)...")
    args = [(dist_matrix, i, N, G_max, K, p_c, mu) for i in range(n_runs)]
    with ProcessPoolExecutor(max_workers=N_WORKERS) as pool:
        for r in pool.map(run_ea_gen, args):
            results["ea"].append(r)
            print(
                f"    Run {r['run'] + 1}/{n_runs}: best = {r['best_distance']:.2f}, time = {r['elapsed']:.1f}s"
            )

    print(f"  Running memetic algorithm ({n_runs} runs, {N_WORKERS} workers)...")
    with ProcessPoolExecutor(max_workers=N_WORKERS) as pool:
        for r in pool.map(run_ma_gen, args):
            results["ma"].append(r)
            print(
                f"    Run {r['run'] + 1}/{n_runs}: best = {r['best_distance']:.2f}, time = {r['elapsed']:.1f}s"
            )

    return results


def experiment_timed(
    dist_matrix, n_runs=10, time_budget=30.0, N=100, K=5, p_c=0.8, mu=0.3
):
    results = {"ea": [], "ma": []}

    print(
        f"  Running simple EA (budget={time_budget:.1f}s, {n_runs} runs, {N_WORKERS} workers)..."
    )
    args = [(dist_matrix, i, time_budget, N, K, p_c, mu) for i in range(n_runs)]
    with ProcessPoolExecutor(max_workers=N_WORKERS) as pool:
        for r in pool.map(run_ea_timed_worker, args):
            results["ea"].append(r)
            print(
                f"    Run {r['run'] + 1}/{n_runs}: best = {r['best_distance']:.2f}, gens = {r['generations']}"
            )

    print(
        f"  Running MA (budget={time_budget:.1f}s, {n_runs} runs, {N_WORKERS} workers)..."
    )
    with ProcessPoolExecutor(max_workers=N_WORKERS) as pool:
        for r in pool.map(run_ma_timed_worker, args):
            results["ma"].append(r)
            print(
                f"    Run {r['run'] + 1}/{n_runs}: best = {r['best_distance']:.2f}, gens = {r['generations']}"
            )

    return results
