"""
Core TSP evolutionary algorithm and memetic algorithm for Exercise B.2.

Implements:
- Simple EA for TSP (tournament selection, order crossover, swap mutation)
- Memetic algorithm = EA + 2-opt local search
- Data loaders for custom and TSPLIB formats
"""

import random
import math
import numpy as np


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_tsp_coordinates(path):
    """Load coordinates from the custom file-tsp format (whitespace-separated x y per line)."""
    coords = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            coords.append((float(parts[0]), float(parts[1])))
    return np.array(coords)


def load_tsplib(path):
    """Load coordinates from a TSPLIB .tsp file (NODE_COORD_SECTION)."""
    coords = []
    reading = False
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line == "NODE_COORD_SECTION":
                reading = True
                continue
            if line in ("EOF", ""):
                if reading:
                    break
                continue
            if reading:
                parts = line.split()
                # format: index x y
                coords.append((float(parts[1]), float(parts[2])))
    return np.array(coords)


def compute_distance_matrix(coords):
    """Compute Euclidean distance matrix from coordinate array."""
    n = len(coords)
    dist = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            dx = coords[i, 0] - coords[j, 0]
            dy = coords[i, 1] - coords[j, 1]
            d = math.sqrt(dx * dx + dy * dy)
            dist[i, j] = d
            dist[j, i] = d
    return dist


# ---------------------------------------------------------------------------
# Tour evaluation
# ---------------------------------------------------------------------------

def tour_distance(tour, dist_matrix):
    """Total distance of a closed tour."""
    total = 0.0
    n = len(tour)
    for i in range(n):
        total += dist_matrix[tour[i], tour[(i + 1) % n]]
    return total


# ---------------------------------------------------------------------------
# Initialization
# ---------------------------------------------------------------------------

def random_tour(n):
    """Generate a random permutation tour of n cities."""
    tour = list(range(n))
    random.shuffle(tour)
    return tour


# ---------------------------------------------------------------------------
# Selection
# ---------------------------------------------------------------------------

def tournament_selection(population, fitnesses, k):
    """Select one individual via tournament selection (minimization: lower is better)."""
    indices = random.sample(range(len(population)), k)
    best = min(indices, key=lambda i: fitnesses[i])
    return population[best][:]


# ---------------------------------------------------------------------------
# Crossover: Order Crossover (OX)
# ---------------------------------------------------------------------------

def order_crossover(parent1, parent2):
    """Order crossover (OX) producing one child."""
    n = len(parent1)
    start, end = sorted(random.sample(range(n), 2))
    child = [None] * n
    # Copy segment from parent1
    child[start:end + 1] = parent1[start:end + 1]
    # Fill remaining from parent2 in order
    segment = set(parent1[start:end + 1])
    fill = [c for c in parent2 if c not in segment]
    idx = 0
    for i in range(n):
        if child[i] is None:
            child[i] = fill[idx]
            idx += 1
    return child


# ---------------------------------------------------------------------------
# Mutation: swap mutation
# ---------------------------------------------------------------------------

def swap_mutation(tour, mu):
    """With probability mu, swap two random positions in the tour."""
    if random.random() < mu:
        tour = tour[:]
        i, j = random.sample(range(len(tour)), 2)
        tour[i], tour[j] = tour[j], tour[i]
    return tour


# ---------------------------------------------------------------------------
# 2-opt local search
# ---------------------------------------------------------------------------

def two_opt(tour, dist_matrix, max_passes=5):
    """
    Apply 2-opt local search, stopping when no improvement is found or
    after max_passes full sweeps.

    Returns the improved tour and the number of edge evaluations performed.
    """
    tour = tour[:]
    n = len(tour)
    evals = 0
    for _ in range(max_passes):
        improved = False
        for i in range(n - 1):
            for j in range(i + 2, n):
                if j == n - 1 and i == 0:
                    continue  # skip reversing the whole tour
                # Cost of current edges
                d_old = (dist_matrix[tour[i], tour[i + 1]]
                         + dist_matrix[tour[j], tour[(j + 1) % n]])
                # Cost after reversing segment [i+1 .. j]
                d_new = (dist_matrix[tour[i], tour[j]]
                         + dist_matrix[tour[i + 1], tour[(j + 1) % n]])
                evals += 1
                if d_new < d_old:
                    tour[i + 1:j + 1] = tour[i + 1:j + 1][::-1]
                    improved = True
        if not improved:
            break
    return tour, evals


# ---------------------------------------------------------------------------
# EA runner
# ---------------------------------------------------------------------------

def run_ea(dist_matrix, N=100, G_max=500, K=5, p_c=0.8, mu=0.3,
           track_interval=1):
    """
    Run a simple generational EA for TSP.

    Returns:
        best_distance_history: best tour distance per generation
        best_tour: best tour found
        total_evals: total number of tour distance evaluations
    """
    n_cities = len(dist_matrix)
    population = [random_tour(n_cities) for _ in range(N)]
    fitnesses = [tour_distance(t, dist_matrix) for t in population]
    total_evals = N

    best_idx = min(range(N), key=lambda i: fitnesses[i])
    best_tour = population[best_idx][:]
    best_distance = fitnesses[best_idx]
    best_distance_history = [best_distance]

    for gen in range(1, G_max + 1):
        new_population = []
        for _ in range(N):
            p1 = tournament_selection(population, fitnesses, K)
            p2 = tournament_selection(population, fitnesses, K)
            if random.random() < p_c:
                child = order_crossover(p1, p2)
            else:
                child = p1[:]
            child = swap_mutation(child, mu)
            new_population.append(child)

        population = new_population
        fitnesses = [tour_distance(t, dist_matrix) for t in population]
        total_evals += N

        gen_best_idx = min(range(N), key=lambda i: fitnesses[i])
        if fitnesses[gen_best_idx] < best_distance:
            best_distance = fitnesses[gen_best_idx]
            best_tour = population[gen_best_idx][:]
        best_distance_history.append(best_distance)

    return best_distance_history, best_tour, total_evals


# ---------------------------------------------------------------------------
# MA runner (EA + 2-opt)
# ---------------------------------------------------------------------------

def run_ma(dist_matrix, N=100, G_max=500, K=5, p_c=0.8, mu=0.3,
           track_interval=1):
    """
    Run a memetic algorithm (EA + 2-opt) for TSP.

    Returns:
        best_distance_history: best tour distance per generation
        best_tour: best tour found
        total_evals: total number of tour distance evaluations (including 2-opt)
    """
    n_cities = len(dist_matrix)
    population = [random_tour(n_cities) for _ in range(N)]

    # Apply 2-opt to initial population
    total_evals = 0
    for i in range(N):
        population[i], evals = two_opt(population[i], dist_matrix)
        total_evals += evals

    fitnesses = [tour_distance(t, dist_matrix) for t in population]
    total_evals += N

    best_idx = min(range(N), key=lambda i: fitnesses[i])
    best_tour = population[best_idx][:]
    best_distance = fitnesses[best_idx]
    best_distance_history = [best_distance]

    for gen in range(1, G_max + 1):
        new_population = []
        for _ in range(N):
            p1 = tournament_selection(population, fitnesses, K)
            p2 = tournament_selection(population, fitnesses, K)
            if random.random() < p_c:
                child = order_crossover(p1, p2)
            else:
                child = p1[:]
            child = swap_mutation(child, mu)

            # Apply 2-opt local search to each child
            child, evals = two_opt(child, dist_matrix)
            total_evals += evals

            new_population.append(child)

        population = new_population
        fitnesses = [tour_distance(t, dist_matrix) for t in population]
        total_evals += N

        gen_best_idx = min(range(N), key=lambda i: fitnesses[i])
        if fitnesses[gen_best_idx] < best_distance:
            best_distance = fitnesses[gen_best_idx]
            best_tour = population[gen_best_idx][:]
        best_distance_history.append(best_distance)

    return best_distance_history, best_tour, total_evals


# ---------------------------------------------------------------------------
# Fair comparison runner: time-based (same wall-clock time)
# ---------------------------------------------------------------------------

def run_ea_timed(dist_matrix, time_budget, N=100, K=5, p_c=0.8, mu=0.3):
    """
    Run EA until wall-clock time budget (seconds) is exhausted.
    Returns best_distance_history (per generation), best_tour, generations_run.
    """
    import time

    n_cities = len(dist_matrix)
    population = [random_tour(n_cities) for _ in range(N)]
    fitnesses = [tour_distance(t, dist_matrix) for t in population]

    best_idx = min(range(N), key=lambda i: fitnesses[i])
    best_tour = population[best_idx][:]
    best_distance = fitnesses[best_idx]
    best_distance_history = [best_distance]

    start = time.time()
    gen = 0
    while time.time() - start < time_budget:
        gen += 1
        new_population = []
        for _ in range(N):
            p1 = tournament_selection(population, fitnesses, K)
            p2 = tournament_selection(population, fitnesses, K)
            if random.random() < p_c:
                child = order_crossover(p1, p2)
            else:
                child = p1[:]
            child = swap_mutation(child, mu)
            new_population.append(child)

        population = new_population
        fitnesses = [tour_distance(t, dist_matrix) for t in population]

        gen_best_idx = min(range(N), key=lambda i: fitnesses[i])
        if fitnesses[gen_best_idx] < best_distance:
            best_distance = fitnesses[gen_best_idx]
            best_tour = population[gen_best_idx][:]
        best_distance_history.append(best_distance)

    return best_distance_history, best_tour, gen


def run_ma_timed(dist_matrix, time_budget, N=100, K=5, p_c=0.8, mu=0.3):
    """
    Run MA until wall-clock time budget (seconds) is exhausted.
    Returns best_distance_history (per generation), best_tour, generations_run.
    """
    import time

    n_cities = len(dist_matrix)
    population = [random_tour(n_cities) for _ in range(N)]

    start = time.time()

    # Apply 2-opt to initial population
    for i in range(N):
        population[i], _ = two_opt(population[i], dist_matrix)

    fitnesses = [tour_distance(t, dist_matrix) for t in population]

    best_idx = min(range(N), key=lambda i: fitnesses[i])
    best_tour = population[best_idx][:]
    best_distance = fitnesses[best_idx]
    best_distance_history = [best_distance]

    gen = 0
    while time.time() - start < time_budget:
        gen += 1
        new_population = []
        for _ in range(N):
            p1 = tournament_selection(population, fitnesses, K)
            p2 = tournament_selection(population, fitnesses, K)
            if random.random() < p_c:
                child = order_crossover(p1, p2)
            else:
                child = p1[:]
            child = swap_mutation(child, mu)
            child, _ = two_opt(child, dist_matrix)
            new_population.append(child)

        population = new_population
        fitnesses = [tour_distance(t, dist_matrix) for t in population]

        gen_best_idx = min(range(N), key=lambda i: fitnesses[i])
        if fitnesses[gen_best_idx] < best_distance:
            best_distance = fitnesses[gen_best_idx]
            best_tour = population[gen_best_idx][:]
        best_distance_history.append(best_distance)

    return best_distance_history, best_tour, gen
