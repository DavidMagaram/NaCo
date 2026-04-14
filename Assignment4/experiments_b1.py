import random

import numpy as np
from string_ga import (
    fitness,
    mutate,
    random_individual,
    run_ga,
    single_point_crossover,
    tournament_selection,
)

TARGET = "NaturalComputing"


def experiment_b1_1(n_runs=10, G_max=100, N=200):
    L = len(TARGET)
    mu = 1 / L
    K = 2
    results = []
    for i in range(n_runs):
        t_finish, history, _ = run_ga(TARGET, K=K, mu=mu, N=N, G_max=G_max)
        results.append(
            {
                "run": i,
                "t_finish": t_finish,
                "fitness_history": history,
            }
        )
        status = t_finish if t_finish is not None else f"not found in {G_max}"
        print(f"  Run {i + 1}/{n_runs}: t_finish = {status}")
    return results


def experiment_b1_2(n_runs=10, G_max=100, N=200):
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
                TARGET,
                K=K,
                mu=mu,
                N=N,
                G_max=G_max,
                track_diversity=True,
                diversity_interval=10,
            )
            runs.append(
                {
                    "t_finish": t_finish,
                    "fitness_history": history,
                    "diversity_history": diversity,
                }
            )
        all_results[label] = runs
        found = sum(1 for r in runs if r["t_finish"] is not None)
        print(f"    Found target in {found}/{n_runs} runs")
    return all_results


def experiment_b1_snapshots(
    G_max=200,
    N=200,
    K=2,
    snap_gens=(0, 10, 30, 60, 100),
    n_top=4,
    n_rand=3,
    seed=7,
):
    L = len(TARGET)
    mu_configs = {
        "mu=0": 0,
        "mu=1/L": 1 / L,
        "mu=3/L": 3 / L,
    }
    target_list = list(TARGET)
    all_snaps = {}
    rng = random.Random(seed)
    for label, mu in mu_configs.items():
        random.seed(rng.random())
        pop = [random_individual(L) for _ in range(N)]
        snaps = {}
        for g in range(G_max):
            fits = [fitness(ind, target_list) for ind in pop]
            if g in snap_gens:
                order = sorted(range(N), key=lambda i: -fits[i])
                top = [("".join(pop[i]), fits[i]) for i in order[:n_top]]
                sample_idx = random.sample(range(N), n_rand)
                rand = [("".join(pop[i]), fits[i]) for i in sample_idx]
                snaps[g] = {"top": top, "rand": rand}
            if max(fits) == L:
                break
            new_pop = []
            for _ in range(N // 2):
                p1 = tournament_selection(pop, fits, K)
                p2 = tournament_selection(pop, fits, K)
                c1, c2 = single_point_crossover(p1, p2)
                new_pop.extend([mutate(c1, mu), mutate(c2, mu)])
            pop = new_pop
        all_snaps[label] = snaps
    return all_snaps


def experiment_b1_5(n_runs=10, G_max=100, N=200):
    L = len(TARGET)
    K = 2
    mu_values = np.linspace(0, 10 / L, 11)
    results = {}
    for mu in mu_values:
        label = f"{mu * L:.1f}/L"
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
    L = len(TARGET)
    K = 5
    mu_values = np.linspace(0, 10 / L, 11)
    results = {}
    for mu in mu_values:
        label = f"{mu * L:.1f}/L"
        print(f"  Running mu = {label} (K=5)...")
        t_finishes = []
        for _ in range(n_runs):
            t_finish, _, _ = run_ga(TARGET, K=K, mu=mu, N=N, G_max=G_max)
            t_finishes.append(t_finish)
        results[mu] = t_finishes
        found = sum(1 for t in t_finishes if t is not None)
        print(f"    Found target in {found}/{n_runs} runs")
    return results
