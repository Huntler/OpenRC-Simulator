from functools import partial
from random import choices, randint, randrange
from random import random, uniform, seed
from typing import Callable, List, Tuple, Any

genome = Tuple[float, float]
population = List[genome]
FitnessFunc = Callable[[genome], float]
PopulateFunc = Callable[[], population]
SelectionFunc = Callable[[population, FitnessFunc], Tuple[genome, genome]]
CrossoverFunc = Callable[[genome, genome], Tuple[genome, genome]]
MutationFunc = Callable[[genome], genome]

seed(0)


def generate_genome(rand_range: float) -> genome:
    # rand_range depends on benchmark function
    return uniform(-rand_range, rand_range), uniform(0, rand_range)


def generate_population(size: int, rand_range: float) -> population:
    return [generate_genome(rand_range) for _ in range(size)]


def fitness(genome: genome, benchmark_func) -> float:
    return 10000 - benchmark_func(genome[0], genome[1])  # we want the minimum


def selection_pair(population: population, fitness_func: FitnessFunc) -> population:
    # select two genomes based on their fitness value
    return choices(
        population=population,
        weights=[fitness_func(genome) for genome in population],
        k=2
    )


def single_point_crossover(a: genome, b: genome) -> Tuple[genome, genome]:
    if len(a) != len(b):
        raise ValueError("Dimension of genomes a and b must match.")

    # if length to short, then crossover not needed
    length = len(a)
    if length < 2:
        return a, b

    # do a random crossover
    p = randint(1, length - 1)
    return a[0:p] + b[p:], b[0:p] + a[p:]


def mutation(genome: genome, num: int = 1, probability: float = 0.5) -> genome:
    # mutate the amount of values (num) in the genome with a given probability
    for _ in range(num):
        index = randrange(len(genome))
        # for benchmark test (index is 0 or 1)
        if index == 0:
            genome = genome[index] if random() > probability else abs(genome[index] - 1), genome[1]
        else:
            genome = genome[0], genome[index] if random() > probability else abs(genome[index] - 1)

    return genome


def run_evolution(populate_func: PopulateFunc,
                  fitness_func: FitnessFunc,
                  fitness_limit: float,
                  selection_func: SelectionFunc = selection_pair,
                  crossover_func: CrossoverFunc = single_point_crossover,
                  mutation_func: MutationFunc = mutation,
                  generation_limit: int = 1000,
                  ) -> tuple[list[tuple[float, float]], int, list[list[Any]]]:
    population = populate_func()

    # ignore
    # plotting
    history = []

    # run for (at most) as many generations as specified
    for i in range(generation_limit):
        print(f'{i}th run')

        # sort the population based on the genome's fitness
        population = sorted(
            population,
            key=lambda genome: fitness_func(genome),
            reverse=True
        )

        history.append(population)

        # if this generation includes a genome with the maximum fitness specified
        # then break -> best population found
        print(fitness_limit)
        print(population[0])
        print(fitness_func(population[0]))
        if fitness_limit + 0.1 >= fitness_func(population[0]) >= fitness_limit - 0.1:
            break

        # create a new generation based on the best two genomes
        next_generation = population[:2]
        for j in range(len(population) // 2 - 1):
            # also select parents from the old population
            parents = selection_func(population, fitness_func)

            # and create childrens using the crossover function
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])

            # do not forget to mutate those children to inject the evolutionary approach
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)

            # then add those children to the new generation
            next_generation += [offspring_a, offspring_b]

        # new generation build up -> repeat process
        population = next_generation
        history.append(population)

    # the best population was found (or the limit has been reached)
    # sort the population based on the genome's fitness and return it
    # together with the amount of generations simulated
    population = sorted(
        population,
        key=lambda genome: fitness_func(genome),
        reverse=True
    )

    return population, i, history

# if __name__ == "__main__":
#     population, generations = run_evolution(
#         populate_func=partial(
#             generate_population, size=15, rand_range=12
#         ),
#         fitness_func=partial(
#             fitness, benchmark_func=rosenbrock
#         ),
#         fitness_limit=0,
#         generation_limit=100,
#
#     )
#
#     print("number of generations:", generations)
#     print(population)
