import random
import string
import math
from collections import Counter

ALPHABET = string.ascii_lowercase + string.ascii_uppercase


def random_individual(length):
    return [random.choice(ALPHABET) for _ in range(length)]


def fitness(individual, target):
    return sum(a == b for a, b in zip(individual, target))


def tournament_selection(population, fitnesses, k):
    indices = random.sample(range(len(population)), k)
    best = max(indices, key=lambda i: fitnesses[i])
    return population[best]


def single_point_crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2


def mutate(individual, mu):
    result = individual[:]
    for i in range(len(result)):
        if random.random() < mu:
            result[i] = random.choice(ALPHABET)
    return result


def shannon_entropy(population, position):
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
    length = len(population[0])
    return sum(shannon_entropy(population, i) for i in range(length)) / length


def run_ga(
    target, K, mu, N=200, G_max=100, track_diversity=False, diversity_interval=10
):
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

        if best_fit == L:
            if track_diversity:
                ent = mean_entropy(population)
                ham = mean_hamming_distance(population)
                diversity_history.append((gen, ent, ham))
            return gen, best_fitness_history, diversity_history

        new_population = []
        for _ in range(N // 2):
            p1 = tournament_selection(population, fitnesses, K)
            p2 = tournament_selection(population, fitnesses, K)
            c1, c2 = single_point_crossover(p1, p2)
            c1 = mutate(c1, mu)
            c2 = mutate(c2, mu)
            new_population.extend([c1, c2])

        population = new_population

    if track_diversity:
        fitnesses = [fitness(ind, target_list) for ind in population]
        ent = mean_entropy(population)
        ham = mean_hamming_distance(population)
        diversity_history.append((G_max, ent, ham))

    return None, best_fitness_history, diversity_history
