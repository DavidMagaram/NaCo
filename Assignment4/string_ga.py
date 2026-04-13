"""
Core string search genetic algorithm for Exercise B.1.

GA specification:
- Tournament selection (parameter K)
- Alphabet: 26 lowercase + 26 uppercase letters
- Single-point crossover with probability p_c = 1
- Per-character mutation with rate mu
- Population size N = 200
- Generational replacement, no elitism
"""

import random
import string
import math
from collections import Counter

ALPHABET = string.ascii_lowercase + string.ascii_uppercase  # 52 characters


def random_individual(length):
    return [random.choice(ALPHABET) for _ in range(length)]


def fitness(individual, target):
    """Number of positions where individual matches the target."""
    return sum(a == b for a, b in zip(individual, target))


def tournament_selection(population, fitnesses, k):
    """Select one individual via tournament selection of size k."""
    indices = random.sample(range(len(population)), k)
    best = max(indices, key=lambda i: fitnesses[i])
    return population[best]


def single_point_crossover(parent1, parent2):
    """Single-point crossover producing two children."""
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2


def mutate(individual, mu):
    """Mutate each character independently with probability mu."""
    result = individual[:]
    for i in range(len(result)):
        if random.random() < mu:
            result[i] = random.choice(ALPHABET)
    return result


def shannon_entropy(population, position):
    """Compute Shannon entropy at a single position across the population."""
    chars = [ind[position] for ind in population]
    counts = Counter(chars)
    n = len(chars)
    entropy = 0.0
    for count in counts.values():
        freq = count / n
        if freq > 0:
            entropy -= freq * math.log2(freq)
    return entropy


def mean_hamming_distance(population, sample_size=50):
    """Mean pairwise Hamming distance over a random sample of pairs."""
    n = len(population)
    if n < 2:
        return 0.0
    pairs = min(sample_size, n * (n - 1) // 2)
    total = 0.0
    for _ in range(pairs):
        i, j = random.sample(range(n), 2)
        total += sum(a != b for a, b in zip(population[i], population[j]))
    return total / pairs


def mean_entropy(population):
    """Mean Shannon entropy averaged across all positions."""
    length = len(population[0])
    return sum(shannon_entropy(population, i) for i in range(length)) / length


def run_ga(target, K, mu, N=200, G_max=100, track_diversity=False, diversity_interval=10):
    """
    Run the string search GA.

    Returns:
        t_finish: generation at which target was found, or None if not found
        best_fitness_history: list of best fitness per generation
        diversity_history: list of (generation, mean_entropy, mean_hamming) if track_diversity
    """
    L = len(target)
    target_list = list(target)

    population = [random_individual(L) for _ in range(N)]
    best_fitness_history = []
    diversity_history = []

    for gen in range(G_max):
        fitnesses = [fitness(ind, target_list) for ind in population]
        best_fit = max(fitnesses)
        best_fitness_history.append(best_fit)

        if track_diversity and gen % diversity_interval == 0:
            ent = mean_entropy(population)
            ham = mean_hamming_distance(population)
            diversity_history.append((gen, ent, ham))

        # Check termination
        if best_fit == L:
            # Record final diversity snapshot
            if track_diversity:
                ent = mean_entropy(population)
                ham = mean_hamming_distance(population)
                diversity_history.append((gen, ent, ham))
            return gen, best_fitness_history, diversity_history

        # Create next generation
        new_population = []
        for _ in range(N // 2):
            p1 = tournament_selection(population, fitnesses, K)
            p2 = tournament_selection(population, fitnesses, K)
            c1, c2 = single_point_crossover(p1, p2)  # p_c = 1
            c1 = mutate(c1, mu)
            c2 = mutate(c2, mu)
            new_population.extend([c1, c2])

        population = new_population

    # Did not find target within G_max generations
    if track_diversity:
        fitnesses = [fitness(ind, target_list) for ind in population]
        ent = mean_entropy(population)
        ham = mean_hamming_distance(population)
        diversity_history.append((G_max, ent, ham))

    return None, best_fitness_history, diversity_history
